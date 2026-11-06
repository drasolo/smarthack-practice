"""Residual detector: how far each meter sits below what it should have used.

Expected use is the meter's own median profile (by weekend or weekday and time of day), scaled
each day by how the other meters moved, so weather and holidays cancel out. A scan over windows
then finds the strongest sustained shortfall, on the whole day and on each part of the day.

Normal behaviour that looks like loss is discounted: a household that is away leaves a flat base
load, and heating that fades through spring declines from the first day. Labels are never read.
"""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

from common import config
from ml import detect

SLOTS = 96
WINDOWS = (5, 7, 10, 14, 21, 30)
BANDS = ((0, 24), (24, 48), (48, 72), (72, 96))  # six hours each, in 15-minute slots
MIN_SHORTFALL_DAY = 0.10  # below this a sustained gap is ordinary variation
MIN_SHORTFALL_BAND = 0.25
TAU_DAY, TAU_BAND, TAU_SPIKE = 14.0, 16.0, 16.0
AWAY_DISCOUNT = 0.25
DRIFT_DISCOUNT = 0.35
MIN_SIGMA = 0.03
MIN_PEERS = 5
SPIKE_TAIL_Z = 6.0  # the largest of about a thousand ordinary hours lands near here
MIN_SCORE_NAMED = 0.3  # weaker than this, naming a pattern would overclaim


def _undo_counter(kwh: pd.Series) -> pd.Series:
    """A cumulative register never falls and ends far above its typical step. Diff it."""
    known = kwh.dropna()
    if len(known) < 10:
        return kwh
    steps = known.diff().dropna()
    typical = steps.median()
    if typical > 0 and (steps >= 0).mean() > 0.99 and known.iloc[-1] > 50 * typical:
        return kwh.diff().clip(lower=0)
    return kwh


def _clean(readings: pd.DataFrame) -> pd.DataFrame:
    """Duplicates averaged and registers differenced, so scores and evidence read the same use."""
    clean = readings.groupby(["meter_id", "ts"], as_index=False)["kwh"].mean()
    clean["kwh"] = clean.groupby("meter_id")["kwh"].transform(_undo_counter)
    return clean


def _to_quarter_hours(clean: pd.DataFrame) -> pd.DataFrame:
    """Coarser data (hourly, say) is spread evenly over its 15-minute slots."""
    step = clean.groupby("meter_id")["ts"].diff().median()
    parts = int(round(step / pd.Timedelta(minutes=15))) if pd.notna(step) else 1
    if parts <= 1:
        return clean
    spread = clean.loc[clean.index.repeat(parts)].copy()
    offset = spread.groupby(level=0).cumcount()
    spread["ts"] += pd.to_timedelta(offset * 15, unit="min")
    spread["kwh"] /= parts
    return spread.reset_index(drop=True)


def _grid(clean: pd.DataFrame, tz: str = config.TIMEZONE) -> tuple[dict, list, np.ndarray]:
    """One days-by-slots array per meter, plus the days and a weekend flag per day."""
    clean = _to_quarter_hours(clean)
    local = clean["ts"].dt.tz_convert(tz)
    clean["day"] = local.dt.date
    clean["slot"] = local.dt.hour * 4 + local.dt.minute // 15
    # Every calendar day, so a date with no readings stays a gap instead of joining its neighbours.
    days = list(pd.date_range(clean["day"].min(), clean["day"].max(), freq="D").date)
    day_at = {d: i for i, d in enumerate(days)}
    grids = {}
    for meter_id, g in clean.groupby("meter_id"):
        grid = np.full((len(days), SLOTS), np.nan)
        # Mean, so the repeated hour of the autumn DST day counts once.
        cells = g.groupby(["day", "slot"])["kwh"].mean()
        rows = [day_at[d] for d in cells.index.get_level_values("day")]
        grid[rows, cells.index.get_level_values("slot")] = cells.to_numpy()
        grids[meter_id] = grid
    weekend = np.array([d.weekday() >= 5 for d in days])
    return grids, days, weekend


def _profile(grid: np.ndarray, weekend: np.ndarray) -> np.ndarray:
    """Median by slot, weekdays and weekends apart. Survives anomalies under half the days."""
    out = np.zeros_like(grid)
    for mask in (weekend, ~weekend):
        if mask.any():
            out[mask] = np.nan_to_num(_nanmedian(grid[mask]))
    return out


def _nanmedian(rows: np.ndarray) -> np.ndarray:
    """Median per column, NaN for an all-empty column (the spring DST hour) without a warning."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        return np.nanmedian(rows, axis=0)


def _ratio(actual: np.ndarray, expected: np.ndarray, slots: tuple[int, int]) -> np.ndarray:
    """Actual over expected per day inside a slot range. NaN when under half of it was read."""
    part_a, part_e = actual[:, slots[0] : slots[1]], expected[:, slots[0] : slots[1]]
    seen = np.isfinite(part_a)
    total_e = np.where(seen, part_e, 0.0).sum(axis=1)
    enough = (seen.mean(axis=1) >= 0.5) & (total_e > 0)
    out = np.full(len(actual), np.nan)
    out[enough] = np.nansum(part_a[enough], axis=1) / total_e[enough]
    return out


def _sigma(errors: np.ndarray) -> float:
    known = errors[np.isfinite(errors)]
    if len(known) == 0:
        return MIN_SIGMA
    return max(1.4826 * float(np.median(np.abs(known - np.median(known)))), MIN_SIGMA)


def _scan(errors: np.ndarray, floor: float) -> tuple[float, int, int]:
    """Strongest sustained shortfall: z, first day, last day. Zero when no gap passes the floor."""
    sigma = _sigma(errors)
    series = pd.Series(-errors)
    best = (0.0, 0, 0)
    for window in WINDOWS:
        if window > len(series):
            continue
        mean = series.rolling(window, min_periods=int(np.ceil(0.7 * window))).mean().to_numpy()
        gap = np.where(mean >= floor, mean, 0.0)
        at = int(np.nanargmax(gap)) if np.isfinite(gap).any() else -1
        if at < 0:
            continue
        z = float(gap[at]) * np.sqrt(window) / sigma
        if z > best[0]:
            best = (z, max(at - window + 1, 0), at)
    return best


def _looks_away(actual, expected, first: int, last: int) -> bool:
    """Flat base load where the profile has peaks: nobody home, not a meter problem."""
    part_a, part_e = actual[first : last + 1], expected[first : last + 1]
    read = np.isfinite(part_a).sum(axis=0)
    seen = read > 0  # a slot can be unread for the whole window: the DST hour, a gap
    a = np.nansum(part_a, axis=0)[seen] / read[seen]
    e = part_e.mean(axis=0)[seen]
    if len(a) < SLOTS / 2 or e.sum() == 0 or e.std() < 0.2 * e.mean():  # no peaks to lose
        return False
    level = a.sum() / e.sum()
    flat = a.std() < 1e-12 or np.corrcoef(a, e)[0, 1] < 0.3
    return level < 0.6 and flat


def _drifts_all_period(errors: np.ndarray) -> bool:
    """Falls as fast in the first half as in the second: a season fading, not a break."""
    days = np.flatnonzero(np.isfinite(errors))
    if len(days) < 14:
        return False
    half = days[len(days) // 2]
    early, late = days[days < half], days[days >= half]
    slope_early = np.polyfit(early, errors[early], 1)[0]
    slope_late = np.polyfit(late, errors[late], 1)[0]
    return slope_early < -0.004 and slope_late < -0.004 and slope_early < 0.3 * slope_late


def _spike(actual: np.ndarray, expected: np.ndarray) -> tuple[float, int]:
    """Biggest one-hour jump over expected, in the meter's own noise, and the day it fell on."""
    used = pd.Series(actual.ravel()).rolling(4, min_periods=4).sum()
    # Floored at the meter's mean, so a quiet night slot can't turn noise into a large ratio.
    floor = max(float(np.nanmean(expected)), 1e-6) * 4
    wanted = pd.Series(expected.ravel()).rolling(4, min_periods=4).sum().clip(lower=floor)
    excess = ((used - wanted) / wanted).to_numpy()
    if not np.isfinite(excess).any():
        return 0.0, 0
    at = int(np.nanargmax(excess))
    return max(float(excess[at]) / _sigma(excess) - SPIKE_TAIL_Z, 0.0), at // SLOTS


def _zero_days(actual: np.ndarray, expected: np.ndarray) -> tuple[int, tuple[int, int]]:
    """Days with at least a quarter of the expected intervals at exactly zero, and their span."""
    hit = []
    for i, (a, e) in enumerate(zip(actual, expected, strict=True)):
        known = np.isfinite(a) & (e > 0)
        if known.sum() >= SLOTS / 2 and (a[known] == 0).mean() >= 0.25:
            hit.append(i)
    return len(hit), (hit[0], hit[-1]) if hit else (0, 0)


def _is_step_across_day(errors: np.ndarray, band_errors: list, first: int, last: int) -> bool:
    """True when the shortfall is there from its first days and in every part of the day."""
    opening = -errors[first : first + 3]
    if not np.isfinite(opening).any():
        return False
    gap = float(np.nanmean(-errors[first : last + 1]))
    if gap <= 0:
        return False
    parts = [
        np.nanmean(-b[first : last + 1])
        for b in band_errors
        if np.isfinite(b[first : last + 1]).any()
    ]
    return float(np.nanmean(opening)) >= 0.6 * gap and min(parts) >= 0.5 * gap


def _missing_kwh(grid: np.ndarray, expected: np.ndarray, first: int, last: int) -> float:
    """Expected minus actual, over the intervals that were read. A gap in the data isn't loss."""
    actual, wanted = grid[first : last + 1], expected[first : last + 1]
    read = np.isfinite(actual)
    return max(float(wanted[read].sum() - actual[read].sum()), 0.0)


def _meter_signals(grid, weekend, factor) -> dict:
    expected = _profile(grid, weekend) * factor[:, None]
    errors = _ratio(grid, expected, (0, SLOTS)) - 1
    band_errors = [_ratio(grid, expected, band) - 1 for band in BANDS]
    day_z, first, last = _scan(errors, MIN_SHORTFALL_DAY)
    band_z, band_first, band_last = max(
        (_scan(e, MIN_SHORTFALL_BAND) for e in band_errors), key=lambda found: found[0]
    )
    spike_z, spike_day = _spike(grid, expected)
    zero_count, zero_span = _zero_days(grid, expected)

    signals = {
        "day": float(1 - np.exp(-day_z / TAU_DAY)),
        "band": float(1 - np.exp(-band_z / TAU_BAND)),
        "spike": float(1 - np.exp(-spike_z / TAU_SPIKE)),
        "zero": min(zero_count / 5, 1.0) if zero_count >= 2 else 0.0,
    }
    if signals["zero"] == 0:
        if day_z and _looks_away(grid, expected, first, last):
            signals["day"] *= AWAY_DISCOUNT
            signals["band"] *= AWAY_DISCOUNT
        if _drifts_all_period(errors):
            signals["day"] *= DRIFT_DISCOUNT
            signals["band"] *= DRIFT_DISCOUNT

    channel = max(signals, key=signals.get)
    window = {
        "day": (first, last),
        "band": (band_first, band_last),
        "spike": (spike_day, spike_day),
        "zero": zero_span,
    }[channel]
    return {
        "channel": channel,
        "score": signals[channel],
        "window": window,
        "missing_kwh": 0.0 if channel == "spike" else _missing_kwh(grid, expected, *window),
        "step": _is_step_across_day(errors, band_errors, *window),
    }


def _kind(found: dict, row: dict) -> str:
    """Only the kinds the evidence backs. Anything else, like part-of-day loss, stays other."""
    if found["score"] < MIN_SCORE_NAMED:
        return "other"
    if found["channel"] == "zero":
        return "flatline_zero" if row["zero_days"] > 0 else "other"
    if found["channel"] == "spike":
        return "spike" if row["spike_ratio"] > 1 else "other"
    return "sudden_drop" if found["step"] else "other"


def score(readings: pd.DataFrame) -> pd.DataFrame:
    """Same columns as detect.score, plus missing_kwh, ranked by this model's score."""
    clean = _clean(readings)
    base = detect.score(clean).set_index("meter_id")
    grids, days, weekend = _grid(clean)
    ratios = [_ratio(grid, _profile(grid, weekend), (0, SLOTS)) for grid in grids.values()]
    factor = np.ones(len(days))  # with too few peers the median is the meter itself
    if len(grids) >= MIN_PEERS:
        factor = np.nan_to_num(_nanmedian(np.vstack(ratios)), nan=1.0)
        factor = np.where(factor > 0, factor, 1.0)

    daily = detect.daily_totals(clean)
    rows = []
    for meter_id, grid in grids.items():
        found = _meter_signals(grid, weekend, factor)
        row = base.loc[meter_id].to_dict()
        row["meter_id"] = meter_id
        row["score"] = round(found["score"], 3)
        row["missing_kwh"] = round(found["missing_kwh"], 1)
        row["start"], row["end"] = days[found["window"][0]], days[found["window"][1]]
        if found["channel"] != "spike":
            # Evidence describes the window this model found, not the baseline's last two weeks.
            g = daily[daily["meter_id"] == meter_id]
            inside = g["day"].between(row["start"], row["end"])
            before = float(np.nan_to_num(g.loc[~inside, "kwh"].median()))
            during = float(np.nan_to_num(g.loc[inside, "kwh"].median()))
            row["baseline_kwh_day"] = round(before, 1)
            row["recent_kwh_day"] = round(during, 1)
            row["change_pct"] = round((during - before) / before * 100, 1) if before > 0 else 0.0
        row["kind"] = _kind(found, row)
        rows.append(row)
    out = pd.DataFrame(rows).sort_values("score", ascending=False, ignore_index=True)
    out["rank"] = out.index + 1
    return out

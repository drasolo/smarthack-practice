"""Synthetic 15-minute smart-meter sample with labelled anomalies and the usual data traps.

Labelled anomalies (data/sample/labels.csv): sudden drops, zero runs, short spikes.
Traps, not labelled: a cumulative register, a missing day, scattered missing intervals,
duplicate rows, and the spring DST day (92 local intervals).

Meters M0041 on are harder: small, gradual, past or shape-only anomalies the baseline misses,
plus normal meters that look odd (vacation, new heater, noise, closed on weekends). They use
their own random stream, so the first 40 meters stay exactly as they were.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from common import config

SEED = 26
N_METERS = 40
N_HARD = 80
DAYS = 45
START = "2026-03-15"  # local days; 2026-03-29 is the spring DST change in Romania


def _shape(hours: np.ndarray) -> np.ndarray:
    morning = 0.6 * np.exp(-(((hours - 8) / 1.5) ** 2))
    evening = 1.0 * np.exp(-(((hours - 19.5) / 2.0) ** 2))
    return 0.4 + morning + evening


def build(seed: int = SEED) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    tz = config.TIMEZONE
    start = pd.Timestamp(START, tz=tz)
    # End in local wall time: start + 45 * 24h would overshoot by the hour DST removes.
    end = (pd.Timestamp(START) + pd.Timedelta(days=DAYS)).tz_localize(tz)
    ts_local = pd.date_range(start, end, freq="15min", inclusive="left")
    hours = ts_local.hour.to_numpy() + ts_local.minute.to_numpy() / 60
    # Day number from local wall time; tz-aware midnights differ by 23h across the DST change.
    wall = ts_local.tz_localize(None)
    day_index = (wall.normalize() - pd.Timestamp(START)).days.to_numpy()
    weekend = np.where(ts_local.dayofweek.to_numpy() >= 5, 1.15, 1.0)

    ids = [f"M{i:04d}" for i in range(1, N_METERS + 1)]
    order = rng.permutation(N_METERS)
    roles = (
        ["sudden_drop"] * 3
        + ["flatline_zero"] * 2
        + ["spike"] * 2
        + ["cumulative", "missing_day", "missing_scattered", "duplicates"]
    )
    role_of = {ids[order[i]]: role for i, role in enumerate(roles)}

    frames, labels = [], []
    for meter_id in ids:
        scale = rng.lognormal(np.log(0.12), 0.3)
        daily_noise = rng.normal(1, 0.08, DAYS)[day_index]
        kwh = scale * _shape(hours) * weekend * daily_noise * rng.normal(1, 0.15, len(hours))
        kwh = np.clip(kwh, 0, None)
        role = role_of.get(meter_id)
        day = lambda d: ts_local[day_index == d][0].date()  # noqa: E731

        if role == "sudden_drop":
            first = DAYS - 12
            kwh[day_index >= first] *= 0.25
            labels.append((meter_id, role, day(first), day(DAYS - 1)))
        elif role == "flatline_zero":
            first = int(rng.integers(15, 22))
            kwh[(day_index >= first) & (day_index < first + 7)] = 0.0
            labels.append((meter_id, role, day(first), day(first + 6)))
        elif role == "spike":
            d = int(rng.integers(DAYS - 10, DAYS - 1))
            at = np.flatnonzero((day_index == d) & (hours >= 20))[:4]
            kwh[at] *= 12
            labels.append((meter_id, role, day(d), day(d)))
        elif role == "cumulative":
            kwh = np.cumsum(kwh)
        elif role == "missing_day":
            kwh[day_index == 30] = np.nan
        elif role == "missing_scattered":
            kwh[rng.random(len(kwh)) < 0.02] = np.nan

        frame = pd.DataFrame({"meter_id": meter_id, "ts": ts_local.tz_convert("UTC"), "kwh": kwh})
        if role == "duplicates":
            frame = pd.concat([frame, frame.sample(8, random_state=seed)])
        frames.append(frame)

    meters = pd.DataFrame(
        {
            "meter_id": ids,
            "region": rng.choice(["Muntenia", "Banat", "Dobrogea"], N_METERS),
            "segment": rng.choice(
                ["household", "household", "household", "small_business"], N_METERS
            ),
        }
    )
    hard_frames, hard_meters, hard_labels = _harder(seed, ts_local, hours, day_index, weekend)
    readings = pd.concat(frames + hard_frames, ignore_index=True)
    readings["kwh"] = readings["kwh"].round(3)
    readings = readings.sort_values(["meter_id", "ts"], ignore_index=True)
    meters = pd.concat([meters, hard_meters], ignore_index=True)
    labels += hard_labels
    label_frame = pd.DataFrame(labels, columns=["meter_id", "kind", "start", "end"])
    return readings, meters, label_frame.sort_values("meter_id", ignore_index=True)


# Labelled role -> label kind. Kinds stay inside contract.schema.Kind.
HARD_LABELLED = {
    "small_drop": ("sudden_drop", 4),  # -30% over the last 12 days
    "gradual_drop": ("other", 4),  # slides to -45% over the last 3 weeks
    "past_drop": ("sudden_drop", 3),  # same daily shape at 40% for 12 days, then back
    "hidden_pv": ("other", 4),  # midday import near zero on sunny days
    "daytime_bypass": ("other", 3),  # 08-22h at 70%, nights untouched
    "partial_zero": ("flatline_zero", 2),  # zeros 00-12h for 6 days, mid-period
    "small_spike": ("spike", 2),  # one evening at 4x
}
# Normal meters that look odd. Not labelled: a detector that flags them is wrong.
HARD_NORMAL = {
    "vacation": 2,  # away mid-period: flat base load, no peaks
    "vacation_recent": 3,  # away for the last 8 days: the classic false alarm
    "spring_heating": 6,  # electric heating fading out through spring
    "new_heater": 3,
    "noisy": 4,
    "closed_weekends": 3,
}


def _harder(seed, ts_local, hours, day_index, weekend):
    rng = np.random.default_rng(seed + 1)
    ids = [f"M{i:04d}" for i in range(N_METERS + 1, N_METERS + N_HARD + 1)]
    roles = [r for r, (_, n) in HARD_LABELLED.items() for _ in range(n)]
    roles += [r for r, n in HARD_NORMAL.items() for _ in range(n)]
    role_of = dict(zip(rng.permutation(ids), roles, strict=False))
    day = lambda d: ts_local[day_index == d][0].date()  # noqa: E731
    daytime = (hours >= 8) & (hours < 22)

    frames, labels = [], []
    for meter_id in ids:
        role = role_of.get(meter_id)
        scale = rng.lognormal(np.log(0.12), 0.3)
        noise_day, noise = (0.2, 0.35) if role == "noisy" else (0.08, 0.15)
        daily_noise = rng.normal(1, noise_day, DAYS)[day_index]
        week = np.where(ts_local.dayofweek.to_numpy() >= 5, 0.3, 1.0)
        week = week if role == "closed_weekends" else weekend
        kwh = scale * _shape(hours) * week * daily_noise * rng.normal(1, noise, len(hours))
        span = None

        if role == "small_drop":
            span = (DAYS - 12, DAYS - 1)
            kwh[day_index >= span[0]] *= 0.7
        elif role == "gradual_drop":
            span = (DAYS - 21, DAYS - 1)
            kwh *= 1 - 0.45 * np.clip((day_index - span[0]) / 20, 0, 1)
        elif role == "past_drop":
            first = int(rng.integers(10, 18))
            span = (first, first + 11)
            kwh[(day_index >= span[0]) & (day_index <= span[1])] *= 0.4
        elif role == "hidden_pv":
            first = int(rng.integers(20, 30))
            span = (first, DAYS - 1)
            sunny = rng.random(DAYS) < 0.7
            midday = (hours >= 10) & (hours < 16) & (day_index >= first)
            kwh[midday] *= np.where(sunny[day_index[midday]], 0.05, 0.6)
        elif role == "daytime_bypass":
            span = (DAYS - 20, DAYS - 1)
            kwh[daytime & (day_index >= span[0])] *= 0.7
        elif role == "partial_zero":
            first = int(rng.integers(12, 25))
            span = (first, first + 5)
            kwh[(hours < 12) & (day_index >= span[0]) & (day_index <= span[1])] = 0.0
        elif role == "small_spike":
            d = int(rng.integers(DAYS - 10, DAYS - 1))
            span = (d, d)
            kwh[np.flatnonzero((day_index == d) & (hours >= 20))[:4]] *= 4
        elif role in ("vacation", "vacation_recent"):
            # Away from home: a flat base load (fridge), no morning or evening peak.
            away = (day_index >= DAYS - 8) if role == "vacation_recent" else (day_index >= 12)
            away &= day_index < (DAYS if role == "vacation_recent" else 22)
            kwh[away] = scale * 0.25 * rng.normal(1, 0.1, int(away.sum()))
        elif role == "spring_heating":
            kwh *= 1 + 1.2 * (1 - day_index / (DAYS - 1))
        elif role == "new_heater":
            kwh[day_index >= DAYS - 14] *= 1.5

        if span is not None:
            labels.append((meter_id, HARD_LABELLED[role][0], day(span[0]), day(span[1])))
        kwh = np.clip(kwh, 0, None)
        frames.append(
            pd.DataFrame({"meter_id": meter_id, "ts": ts_local.tz_convert("UTC"), "kwh": kwh})
        )

    meters = pd.DataFrame(
        {
            "meter_id": ids,
            "region": rng.choice(["Muntenia", "Banat", "Dobrogea"], N_HARD),
            "segment": [
                "small_business" if role_of.get(m) == "closed_weekends" else "household"
                for m in ids
            ],
        }
    )
    return frames, meters, labels


def main() -> None:
    readings, meters, labels = build()
    out = config.SAMPLE_DIR
    out.mkdir(parents=True, exist_ok=True)
    readings.to_parquet(out / "readings.parquet", index=False)
    meters.to_csv(out / "meters.csv", index=False)
    labels.to_csv(out / "labels.csv", index=False)
    print(f"wrote {len(readings):,} readings, {len(meters)} meters, {len(labels)} labels to {out}")


if __name__ == "__main__":
    main()

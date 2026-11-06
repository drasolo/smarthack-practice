"""Baseline anomaly scorer: three plain signals on daily totals.

This is the bar a real model has to beat, not the solution. Each signal maps to 0..1 and the
meter's score is the strongest one.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import numpy as np
import pandas as pd

from common import config
from contract.schema import Anomaly, AnomalyList, Evidence, Period

RECENT_DAYS = 14


def daily_totals(readings: pd.DataFrame, tz: str = config.TIMEZONE) -> pd.DataFrame:
    """kWh per meter per local day. A day with no readings stays NaN; it is not a zero day."""
    days = readings.assign(day=readings["ts"].dt.tz_convert(tz).dt.date)
    return days.groupby(["meter_id", "day"], as_index=False)["kwh"].sum(min_count=1)


def _longest_zero_run(days: pd.Series, values: pd.Series) -> tuple[int, object, object]:
    """Length, first and last day of the longest run of zero days. A NaN day breaks the run."""
    best = (0, None, None)
    run, run_start = 0, None
    for day, value in zip(days, values, strict=True):
        if value == 0:
            if run == 0:
                run_start = day
            run += 1
            if run > best[0]:
                best = (run, run_start, day)
        else:
            run = 0
    return best


def score(readings: pd.DataFrame, recent_days: int = RECENT_DAYS) -> pd.DataFrame:
    daily = daily_totals(readings)
    last_day = daily["day"].max()
    cutoff = last_day - timedelta(days=recent_days - 1)

    by_meter = readings.dropna(subset=["kwh"]).groupby("meter_id")["kwh"]
    p95 = by_meter.quantile(0.95)
    peak_idx = by_meter.idxmax()
    peaks = readings.loc[peak_idx, ["meter_id", "ts", "kwh"]].set_index("meter_id")

    rows = []
    for meter_id, g in daily.groupby("meter_id"):
        g = g.sort_values("day")
        baseline = g.loc[g["day"] < cutoff, "kwh"].median()
        recent = g.loc[g["day"] >= cutoff, "kwh"].median()
        change = (recent - baseline) / baseline * 100 if baseline and baseline > 0 else 0.0
        zero_days, zero_start, zero_end = _longest_zero_run(g["day"], g["kwh"])
        peak = peaks.loc[meter_id] if meter_id in peaks.index else None
        peak_kwh = float(peak["kwh"]) if peak is not None else 0.0
        ratio = peak_kwh / p95[meter_id] if meter_id in p95.index and p95[meter_id] > 0 else 0.0

        signals = {
            "sudden_drop": float(np.clip(-change / 100, 0, 1)),
            "flatline_zero": min(zero_days / 5, 1.0) if zero_days >= 2 else 0.0,
            "spike": float(np.clip((ratio - 4) / 8, 0, 1)),
        }
        kind = max(signals, key=signals.get)
        top = signals[kind]
        if top < 0.2:
            kind = "other"
        if kind == "flatline_zero":
            start, end = zero_start, zero_end
        elif kind == "spike" and peak is not None:
            start = end = peak["ts"].tz_convert(config.TIMEZONE).date()
        else:
            start, end = cutoff, last_day
        # A flatline's evidence covers its own days, so an old one doesn't read as "recent equals
        # baseline". Other kinds keep the recent window (a spike day's total would contradict
        # the spike explanation, which says daily use stays normal).
        inside = g["day"].between(start, end) if kind == "flatline_zero" else g["day"] >= cutoff
        # An empty side (a meter at zero for the whole period) has a NaN median; report it as 0.
        base_e = np.nan_to_num(g.loc[~inside, "kwh"].median())
        during = np.nan_to_num(g.loc[inside, "kwh"].median())
        change_e = (during - base_e) / base_e * 100 if base_e > 0 else 0.0
        rows.append(
            {
                "meter_id": meter_id,
                "score": round(top, 3),
                "kind": kind,
                "start": start,
                "end": end,
                "baseline_kwh_day": round(float(base_e), 1),
                "recent_kwh_day": round(float(during), 1),
                "change_pct": round(float(change_e), 1),
                "drop_14d_pct": round(float(change), 1),  # naive ranking in evals, not evidence
                "zero_days": int(zero_days),
                "max_kwh_interval": round(peak_kwh, 2),
                "spike_ratio": round(float(ratio), 1),
            }
        )
    out = pd.DataFrame(rows).sort_values("score", ascending=False, ignore_index=True)
    out.insert(0, "rank", out.index + 1)
    return out


def to_anomaly(row: pd.Series) -> Anomaly:
    return Anomaly(
        rank=int(row["rank"]),
        meter_id=str(row["meter_id"]),
        score=float(row["score"]),
        kind=row["kind"],
        period=Period(start=row["start"], end=row["end"]),
        evidence=Evidence(
            **{k: row[k] for k in Evidence.model_fields},
        ),
    )


def to_contract(scores: pd.DataFrame, limit: int, source: str) -> AnomalyList:
    items = [to_anomaly(row) for _, row in scores.head(limit).iterrows()]
    return AnomalyList(items=items, source=source, generated_at=datetime.now(UTC))

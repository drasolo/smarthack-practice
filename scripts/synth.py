"""Synthetic 15-minute smart-meter sample with labelled anomalies and the usual data traps.

Labelled anomalies (data/sample/labels.csv): sudden drops, zero runs, short spikes.
Traps, not labelled: a cumulative register, a missing day, scattered missing intervals,
duplicate rows, and the spring DST day (92 local intervals).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from common import config

SEED = 26
N_METERS = 40
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

    readings = pd.concat(frames, ignore_index=True)
    readings["kwh"] = readings["kwh"].round(3)
    readings = readings.sort_values(["meter_id", "ts"], ignore_index=True)
    meters = pd.DataFrame(
        {
            "meter_id": ids,
            "region": rng.choice(["Muntenia", "Banat", "Dobrogea"], N_METERS),
            "segment": rng.choice(
                ["household", "household", "household", "small_business"], N_METERS
            ),
        }
    )
    label_frame = pd.DataFrame(labels, columns=["meter_id", "kind", "start", "end"])
    return readings, meters, label_frame.sort_values("meter_id", ignore_index=True)


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

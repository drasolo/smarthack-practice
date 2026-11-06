from datetime import timedelta

import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from common import config
from evals.metrics import average_precision, precision_at_k
from ml import detect, learned
from ml.load import load_labels, read_readings
from scripts.synth import build


def test_learned_detects_a_profile_shift_with_unchanged_daily_totals():
    rng = np.random.default_rng(12)
    ts = pd.date_range("2026-01-01", periods=35 * 96, freq="15min", tz=config.TIMEZONE)
    hour = ts.hour.to_numpy()
    recent = ts >= ts.max() - timedelta(days=13)
    frames = []
    for i in range(24):
        kwh = (0.2 + 0.1 * (hour >= 18)) * rng.uniform(0.8, 1.2)
        kwh *= rng.normal(1, 0.015, len(ts))
        if i == 0:
            for day in ts[recent].normalize().unique():
                at = ts.normalize() == day
                kwh[at] = np.roll(kwh[at], 12 * 4)
        frames.append(
            pd.DataFrame(
                {
                    "meter_id": f"meter-{i}",
                    "ts": ts.tz_convert("UTC"),
                    "kwh": kwh,
                }
            )
        )
    readings = pd.concat(frames, ignore_index=True)
    baseline = detect.score(readings).set_index("meter_id")
    result = learned.score(readings)
    assert result.iloc[0]["meter_id"] == "meter-0"
    assert result.iloc[0]["kind"] == "other"
    assert abs(baseline.loc["meter-0", "drop_14d_pct"]) < 2
    assert list(result.columns) == list(detect.score(readings).columns)
    assert result["rank"].tolist() == list(range(1, len(result) + 1))
    assert np.isfinite(result["score"]).all()
    detect.to_contract(result, len(result), "sample")
    assert_frame_equal(
        result.set_index("meter_id").drop(columns=["score", "rank"]).sort_index(),
        baseline.drop(columns=["score", "rank"]).sort_index(),
    )
    assert_frame_equal(result, learned.score(readings.sample(frac=1, random_state=1)))


def test_learned_keeps_missing_readings_distinct_from_zero():
    ts = pd.date_range("2026-01-01", periods=30 * 96, freq="15min", tz="UTC")
    readings = pd.concat(
        [
            pd.DataFrame({"meter_id": "zero", "ts": ts, "kwh": 0.0}),
            pd.DataFrame({"meter_id": "missing", "ts": ts, "kwh": np.nan}),
        ],
        ignore_index=True,
    )
    result = learned.score(readings).set_index("meter_id")
    assert result.loc["zero", "zero_days"] > 0
    assert result.loc["missing", "zero_days"] == 0
    assert np.isfinite(result.select_dtypes("number")).all().all()
    detect.to_contract(result.reset_index(), 2, "sample")


def test_learned_finds_changes_among_vacations_and_seasonal_variation():
    rng = np.random.default_rng(19)
    ts = pd.date_range("2026-01-01", periods=45 * 96, freq="15min", tz=config.TIMEZONE)
    hours = ts.hour.to_numpy() + ts.minute.to_numpy() / 60
    days = (ts.tz_localize(None).normalize() - pd.Timestamp("2026-01-01")).days.to_numpy()
    shape = 0.4 + 0.6 * np.exp(-(((hours - 8) / 1.5) ** 2)) + np.exp(-(((hours - 19.5) / 2) ** 2))
    values = shape * rng.normal(1, 0.04, (40, len(ts)))
    values[0, days >= 33] *= 0.3
    values[1, (days >= 15) & (days < 21) & (hours < 12)] = 0
    away = (days >= 12) & (days < 22)
    values[2, away] = rng.normal(0.25, 0.025, away.sum())
    values[3] *= 1 + 1.2 * (1 - days / 44)
    ids = [f"meter-{i:02d}" for i in range(40)]
    readings = pd.DataFrame(
        {
            "meter_id": np.repeat(ids, len(ts)),
            "ts": np.tile(ts.tz_convert("UTC"), len(ids)),
            "kwh": values.ravel(),
        }
    )
    top = set(learned.score(readings).head(10)["meter_id"])
    assert {ids[0], ids[1]} <= top


@pytest.mark.parametrize("seed", [None, 42, 73, 91])
def test_learned_improves_both_ranking_metrics_on_the_harder_sample(seed):
    if seed is None:
        readings = read_readings(config.SAMPLE_DIR / "readings.parquet")
        labels = load_labels("sample")
    else:
        readings, _, labels = build(seed)
    relevant = set(labels["meter_id"])
    baseline = list(detect.score(readings)["meter_id"])
    ranked = list(learned.score(readings)["meter_id"])
    assert precision_at_k(ranked, relevant, 10) > precision_at_k(baseline, relevant, 10)
    assert average_precision(ranked, relevant) > average_precision(baseline, relevant)

"""Residual detector: same shape as the baseline, better ranking, normal behaviour left alone."""

import numpy as np
import pandas as pd
import pytest

from common import config
from evals.metrics import average_precision, precision_at_k
from ml import detect, residual
from ml.load import load_labels, read_readings
from scripts import synth


@pytest.fixture(scope="module")
def sample():
    readings = read_readings(config.SAMPLE_DIR / "readings.parquet")
    return readings, residual.score(readings), load_labels("sample")


def _flat_profile(days=30):
    shape = 0.4 + np.exp(-(((np.arange(residual.SLOTS) / 4 - 19) / 2) ** 2))
    return np.tile(shape, (days, 1))


def test_same_columns_as_baseline_plus_missing_kwh(sample):
    readings, scores, _ = sample
    assert set(detect.score(readings).columns) | {"missing_kwh"} == set(scores.columns)
    assert list(scores["rank"]) == list(range(1, len(scores) + 1))
    assert scores["score"].is_monotonic_decreasing
    assert scores["score"].between(0, 1).all()
    assert (scores["missing_kwh"] >= 0).all()


def test_every_row_fits_the_contract(sample):
    _, scores, _ = sample
    for _, row in scores.iterrows():
        anomaly = detect.to_anomaly(row)
        assert anomaly.period.start <= anomaly.period.end


def test_beats_baseline_on_the_sample(sample):
    readings, scores, labels = sample
    relevant = set(labels["meter_id"])
    ours, base = list(scores["meter_id"]), list(detect.score(readings)["meter_id"])
    assert precision_at_k(ours, relevant, 10) > precision_at_k(base, relevant, 10)
    assert average_precision(ours, relevant) > average_precision(base, relevant)


def test_beats_baseline_on_a_seed_it_never_saw():
    readings, _, labels = synth.build(7)
    relevant = set(labels["meter_id"])
    ours = list(residual.score(readings)["meter_id"])
    base = list(detect.score(readings)["meter_id"])
    assert average_precision(ours, relevant) > average_precision(base, relevant)


def test_scan_window_stays_inside_the_period():
    errors = np.zeros(30)
    errors[:3] = -0.6  # short drop in the very first days: rolling windows are still partial
    z, first, last = residual._scan(errors, residual.MIN_SHORTFALL_DAY)
    assert z > 0
    assert 0 <= first <= last


def test_steady_use_has_no_shortfall():
    assert residual._scan(np.zeros(30), residual.MIN_SHORTFALL_DAY)[0] == 0


def test_flat_base_load_reads_as_away_and_a_scaled_profile_does_not():
    expected = _flat_profile()
    away = expected.copy()
    away[10:20] = 0.1
    assert residual._looks_away(away, expected, 10, 19)
    loss = expected.copy()
    loss[10:20] *= 0.4
    assert not residual._looks_away(loss, expected, 10, 19)


def test_fade_over_the_whole_period_is_drift_and_a_late_break_is_not():
    days = np.arange(45)
    assert residual._drifts_all_period(-0.012 * days)
    late_break = np.where(days >= 30, -0.4, 0.0)
    assert not residual._drifts_all_period(late_break)


def test_cumulative_register_becomes_steps():
    steps = np.full(200, 0.25)
    undone = residual._undo_counter(pd.Series(steps.cumsum()))
    assert undone.iloc[1:].round(6).eq(0.25).all()
    plain = pd.Series(steps)
    assert residual._undo_counter(plain).equals(plain)


def test_one_hour_spike_is_found_on_its_day():
    expected = _flat_profile()
    rng = np.random.default_rng(1)
    actual = expected * rng.normal(1, 0.1, expected.shape)
    actual[20, 76:80] *= 4
    z, day = residual._spike(actual, expected)
    assert z > 0
    assert day == 20


def test_hourly_data_still_ranks_above_baseline(sample):
    readings, _, labels = sample
    hourly = (
        readings.set_index("ts")
        .groupby("meter_id")["kwh"]
        .resample("1h")
        .sum(min_count=4)
        .reset_index()
    )
    relevant = set(labels["meter_id"])
    ours = list(residual.score(hourly)["meter_id"])
    base = list(detect.score(hourly)["meter_id"])
    assert average_precision(ours, relevant) > average_precision(base, relevant)


def test_a_lone_meter_keeps_its_own_drop():
    days = pd.date_range("2026-03-02", periods=30, freq="D", tz="UTC")
    ts = pd.date_range(days[0], periods=30 * 96, freq="15min")
    kwh = np.where(ts >= days[20], 0.04, 0.1) + np.random.default_rng(2).normal(0, 0.002, len(ts))
    readings = pd.DataFrame({"meter_id": "M1", "ts": ts, "kwh": kwh})
    assert residual.score(readings)["score"].iloc[0] > 0.5


def _quarter_hours(days=30):
    local = pd.date_range("2026-03-02", periods=days * 96, freq="15min", tz=config.TIMEZONE)
    return local.tz_convert("UTC")


def test_register_evidence_shows_the_fall_in_use():
    ts = _quarter_hours()
    use = np.where(ts >= ts[20 * 96], 0.04, 0.1) * np.random.default_rng(3).normal(1, 0.02, len(ts))
    readings = pd.DataFrame({"meter_id": "M1", "ts": ts, "kwh": use.cumsum()})
    row = residual.score(readings).iloc[0]
    assert row["kind"] == "sudden_drop"
    assert row["change_pct"] < -40
    assert row["baseline_kwh_day"] < 15


def test_unread_intervals_are_not_counted_as_missing_energy():
    expected = np.ones((10, residual.SLOTS))
    grid = np.full_like(expected, 0.4)
    grid[:, :24] = np.nan
    assert residual._missing_kwh(grid, expected, 0, 9) == pytest.approx(432)


def test_a_date_with_no_readings_stays_a_gap():
    ts = _quarter_hours(10)
    kept = ts[(ts < ts[4 * 96]) | (ts >= ts[6 * 96])]
    clean = pd.DataFrame({"meter_id": "M1", "ts": kept, "kwh": 0.1})
    grids, days, _ = residual._grid(clean)
    assert len(days) == 10
    assert np.isnan(grids["M1"][4:6]).all()
    assert np.isfinite(grids["M1"][7]).all()

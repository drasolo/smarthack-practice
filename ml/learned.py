"""Isolation Forest on changes in daily use and the local intraday profile.

Fits the received meter cohort without labels. Scores are relative anomaly scores, not
probabilities. The baseline supplies measured evidence and the existing anomaly kinds.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from common import config
from ml import detect


def _features(readings: pd.DataFrame, evidence: pd.DataFrame) -> pd.DataFrame:
    daily = detect.daily_totals(readings).pivot(index="meter_id", columns="day", values="kwh")
    calendar = pd.date_range(min(daily.columns), max(daily.columns)).date
    daily = daily.reindex(columns=calendar)
    typical = daily.median(axis=1).replace(0, np.nan)
    relative = daily.div(typical, axis=0)
    local = readings["ts"].dt.tz_convert(config.TIMEZONE)
    intervals = readings.assign(day=local.dt.date, hour=local.dt.hour)
    grouped = intervals.groupby(["meter_id", "day"])["kwh"]
    stats = grouped.agg(["mean", "std", "count"])
    cv = (stats["std"] / stats["mean"].replace(0, np.nan)).unstack("day")
    # A proportional drop preserves peaks; an away household often becomes a flat base load.
    shape_retained = cv.div(cv.median(axis=1).replace(0, np.nan), axis=0).clip(upper=1)
    weekly = relative.T.rolling(7, min_periods=3).median().T
    weekly_shape = shape_retained.T.rolling(7, min_periods=3).median().T
    velocity = weekly.diff(7, axis=1)
    loss = (-velocity).clip(lower=0)
    features = (
        evidence.set_index("meter_id").reindex(daily.index)[["zero_days", "spike_ratio"]].copy()
    )
    features["weekly_drop"] = (loss * weekly_shape).max(axis=1)
    features["slope_change"] = (
        (-velocity.diff(7, axis=1)).clip(lower=0) * loss.gt(0) * weekly_shape
    ).max(axis=1)
    zero = intervals["kwh"].eq(0).groupby([intervals["meter_id"], intervals["day"]]).sum()
    features["partial_zero"] = (zero / stats["count"]).groupby(level="meter_id").max()

    hourly = intervals.groupby(["meter_id", "day", "hour"])["kwh"].mean()
    hourly = hourly.unstack("hour").reindex(columns=range(24))
    morning = hourly.loc[:, 6:9].mean(axis=1).replace(0, np.nan)
    noon = hourly.loc[:, 10:15].mean(axis=1)
    ratio = (noon / morning).unstack("day")
    noon_reference = ratio.median(axis=1).replace(0, np.nan)
    features["noon_morning_loss"] = (
        1 - ratio.T.rolling(3, min_periods=2).median().min().div(noon_reference)
    ).clip(lower=0)
    night = hourly.loc[:, 0:5].mean(axis=1)
    daytime = hourly.loc[:, 8:21].mean(axis=1).replace(0, np.nan)
    ratio = (night / daytime).unstack("day")
    night_reference = ratio.median(axis=1).replace(0, np.nan)
    gain = ratio.div(night_reference, axis=0).sub(1).clip(lower=0)
    short_shape = shape_retained.T.rolling(3, min_periods=2).median().T
    features["night_day_gain"] = (gain.T.rolling(3, min_periods=2).median().T * short_shape).max(
        axis=1
    )
    # Missing history is unknown, not a zero day or a change of profile.
    return features.replace([np.inf, -np.inf], np.nan).fillna(0).sort_index()


def score(readings: pd.DataFrame) -> pd.DataFrame:
    out = detect.score(readings)
    features = _features(readings, out)
    forest = IsolationForest(n_estimators=256, random_state=26)
    forest.fit(features)
    scores = pd.Series(-forest.score_samples(features), index=features.index)
    out["score"] = out["meter_id"].map(scores)
    out = out.sort_values(["score", "meter_id"], ascending=[False, True], ignore_index=True)
    out["rank"] = out.index + 1
    return out

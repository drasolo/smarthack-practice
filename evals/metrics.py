"""Metrics for the pitch table. Ranking metrics for anomalies, error metrics for forecasts."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def precision_at_k(ranked: Sequence[str], relevant: set[str], k: int) -> float:
    top = list(ranked)[:k]
    return sum(item in relevant for item in top) / k if k else 0.0


def recall_at_k(ranked: Sequence[str], relevant: set[str], k: int) -> float:
    top = set(list(ranked)[:k])
    return len(top & relevant) / len(relevant) if relevant else 0.0


def average_precision(ranked: Sequence[str], relevant: set[str]) -> float:
    hits, total = 0, 0.0
    for i, item in enumerate(ranked, start=1):
        if item in relevant:
            hits += 1
            total += hits / i
    return total / len(relevant) if relevant else 0.0


def mae(actual: Sequence[float], predicted: Sequence[float]) -> float:
    a, p = np.asarray(actual, float), np.asarray(predicted, float)
    return float(np.nanmean(np.abs(a - p)))


def wape(actual: Sequence[float], predicted: Sequence[float]) -> float:
    """Weighted absolute percentage error: total error over total actual. Safe with zeros."""
    a, p = np.asarray(actual, float), np.asarray(predicted, float)
    return float(np.nansum(np.abs(a - p)) / np.nansum(np.abs(a)))


def error_cost_lei(
    actual: Sequence[float], predicted: Sequence[float], lei_per_kwh: float
) -> float:
    """What forecast error costs if every kWh off is bought or sold at `lei_per_kwh`."""
    a, p = np.asarray(actual, float), np.asarray(predicted, float)
    return float(np.nansum(np.abs(a - p)) * lei_per_kwh)

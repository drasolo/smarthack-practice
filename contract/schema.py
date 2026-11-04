"""The contract between ml, api and ui. Change it only after telling the group (AGENTS.md)."""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

Kind = Literal["sudden_drop", "flatline_zero", "spike", "other"]
Source = Literal["sample", "real", "mock"]


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Health(Strict):
    status: Literal["ok"]
    source: Source
    llm: str


class Period(Strict):
    start: date
    end: date


class Evidence(Strict):
    """Numbers the detector saw. The explanation may use these and nothing else."""

    baseline_kwh_day: float
    recent_kwh_day: float
    change_pct: float
    zero_days: int
    max_kwh_interval: float
    spike_ratio: float


class Anomaly(Strict):
    rank: int
    meter_id: str
    score: float
    kind: Kind
    period: Period
    evidence: Evidence


class AnomalyList(Strict):
    items: list[Anomaly]
    source: Source
    generated_at: datetime


class Point(Strict):
    ts: datetime
    kwh: float | None


class Series(Strict):
    meter_id: str
    points: list[Point]


class ExplainRequest(Strict):
    meter_id: str


class Explanation(Strict):
    """Also the LLM's output schema, so keep it flat and constraint-free."""

    summary: str
    reasons: list[str]
    next_step: str
    confidence: Literal["low", "medium", "high"]


class ExplainResponse(Strict):
    meter_id: str
    explanation: Explanation
    model: str

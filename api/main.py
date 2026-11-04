"""HTTP API for the UI. Shapes come from contract/schema.py; USE_MOCKS=1 serves contract/mocks."""

from __future__ import annotations

import json
from functools import lru_cache

import pandas as pd
from fastapi import FastAPI, HTTPException

from api.explain import explain_anomaly
from common import config, llm
from contract.schema import (
    AnomalyList,
    ExplainRequest,
    ExplainResponse,
    Health,
    Point,
    Series,
)
from ml import detect
from ml.load import load_default

app = FastAPI(title="smarthack-practice")


@lru_cache(maxsize=1)
def state() -> tuple[pd.DataFrame, pd.DataFrame, str]:
    readings, source = load_default()
    return readings, detect.score(readings), source


def mock(name: str) -> dict:
    return json.loads((config.MOCKS_DIR / name).read_text(encoding="utf-8"))


@app.get("/health", response_model=Health)
def health() -> Health:
    source = "mock" if config.USE_MOCKS else state()[2]
    return Health(status="ok", source=source, llm=llm.provider_name())


@app.get("/anomalies", response_model=AnomalyList)
def anomalies(limit: int = 10) -> AnomalyList:
    if config.USE_MOCKS:
        return AnomalyList.model_validate(mock("anomalies.json"))
    _, scores, source = state()
    return detect.to_contract(scores, limit, source)


@app.get("/meters/{meter_id}/series", response_model=Series)
def series(meter_id: str, days: int = 14) -> Series:
    if config.USE_MOCKS:
        return Series.model_validate(mock("series.json"))
    readings = state()[0]
    meter = readings[readings["meter_id"] == meter_id]
    if meter.empty:
        raise HTTPException(404, f"unknown meter {meter_id}")
    meter = meter[meter["ts"] > meter["ts"].max() - pd.Timedelta(days=days)]
    points = [
        Point(ts=ts, kwh=None if pd.isna(kwh) else float(kwh))
        for ts, kwh in zip(meter["ts"], meter["kwh"], strict=True)
    ]
    return Series(meter_id=meter_id, points=points)


@app.post("/explain", response_model=ExplainResponse)
def explain(request: ExplainRequest) -> ExplainResponse:
    if config.USE_MOCKS:
        return ExplainResponse.model_validate(mock("explain.json"))
    scores = state()[1]
    row = scores[scores["meter_id"] == request.meter_id]
    if row.empty:
        raise HTTPException(404, f"unknown meter {request.meter_id}")
    anomaly = detect.to_anomaly(row.iloc[0])
    return ExplainResponse(
        meter_id=request.meter_id,
        explanation=explain_anomaly(anomaly),
        model=llm.provider_name(),
    )

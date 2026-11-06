"""Fast checks on the shared pieces. Add a test here for every bug the dry run finds."""

import json

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from common import config, pii
from contract import schema
from evals.metrics import average_precision, precision_at_k, recall_at_k, wape
from ml import detect
from ml.load import load_labels, read_readings


@pytest.fixture(autouse=True)
def offline_llm(monkeypatch, tmp_path):
    monkeypatch.setattr(config, "LLM_PROVIDER", "fake")
    monkeypatch.setattr(config, "LOG_DIR", tmp_path)


@pytest.fixture(scope="module")
def sample():
    return read_readings(config.SAMPLE_DIR / "readings.parquet")


def test_pii_mask():
    text = "Ion, ion.pop@mail.ro, 0722123456, CNP 1960101123456, RO49AAAA1B31007593840000"
    masked = pii.mask(text)
    assert pii.find(masked) == []
    assert "<EMAIL>" in masked and "<PHONE>" in masked and "<CNP>" in masked


def test_metrics():
    ranked = ["a", "b", "c", "d"]
    assert precision_at_k(ranked, {"a", "c"}, 2) == 0.5
    assert recall_at_k(ranked, {"a", "c"}, 4) == 1.0
    assert average_precision(ranked, {"a", "c"}) == pytest.approx((1 + 2 / 3) / 2)
    assert wape([10, 0, 10], [8, 1, 12]) == pytest.approx(0.25)


@pytest.mark.parametrize("name", ["health", "anomalies", "series", "explain"])
def test_mocks_match_contract(name):
    model = {
        "health": schema.Health,
        "anomalies": schema.AnomalyList,
        "series": schema.Series,
        "explain": schema.ExplainResponse,
    }[name]
    model.model_validate(json.loads((config.MOCKS_DIR / f"{name}.json").read_text("utf-8")))


def test_detector_ranks_labelled_meters_on_top(sample):
    labels = load_labels("sample")
    top = set(detect.score(sample).head(10)["meter_id"])
    assert set(labels["meter_id"]) <= top


def test_missing_day_is_not_a_zero_day(sample):
    daily = detect.daily_totals(sample)
    assert daily["kwh"].isna().any(), "sample should contain a fully missing day"
    assert not (daily["kwh"].isna() & daily["kwh"].eq(0)).any()


def test_spring_dst_day_has_92_intervals(sample):
    one = sample[sample["meter_id"] == sample["meter_id"].iloc[0]]
    local_days = one["ts"].dt.tz_convert(config.TIMEZONE).dt.date
    assert local_days.value_counts()[pd.Timestamp("2026-03-29").date()] == 92


def test_ui_renders_on_mocks(monkeypatch):
    """With no API running, the page falls back to contract/mocks and must render cleanly."""
    from streamlit.testing.v1 import AppTest

    monkeypatch.setattr(config, "API_URL", "http://127.0.0.1:9")
    page = AppTest.from_file(str(config.ROOT / "ui" / "app.py"), default_timeout=60).run()
    assert not page.exception
    assert page.title[0].value == "Contoare suspecte"
    assert len(page.dataframe) == 1


def test_api_follows_contract():
    from api.main import app

    client = TestClient(app)
    schema.Health.model_validate(client.get("/health").json())
    listing = schema.AnomalyList.model_validate(client.get("/anomalies?limit=5").json())
    meter = listing.items[0].meter_id
    schema.Series.model_validate(client.get(f"/meters/{meter}/series").json())
    schema.ExplainResponse.model_validate(client.post("/explain", json={"meter_id": meter}).json())
    assert client.post("/explain", json={"meter_id": "nope"}).status_code == 404


def test_grounded_ignores_meter_ids(sample):
    from evals.run import grounded

    items = detect.to_contract(detect.score(sample), 10, "sample").items
    a = next(i for i in items if i.meter_id == "M0024")
    text = f"Contorul M0024 a raportat zero {a.evidence.zero_days} zile la rând."
    e = schema.Explanation(summary=text, reasons=["x"], next_step="Vizită.", confidence="high")
    assert grounded(e, a)


def test_flatline_evidence_describes_its_period(sample):
    row = detect.score(sample).set_index("meter_id").loc["M0014"]
    assert row["kind"] == "flatline_zero"
    assert row["recent_kwh_day"] == 0 and row["change_pct"] == -100 and row["baseline_kwh_day"] > 0

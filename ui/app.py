"""Streamlit demo: ranked meters, a chart and an explanation for the selected one.

Reads the API; if the API is down it falls back to contract/mocks so UI work never waits.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import httpx  # noqa: E402
import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

from common import config  # noqa: E402

KINDS = {
    "sudden_drop": "scădere bruscă",
    "flatline_zero": "zero continuu",
    "spike": "vârf",
    "other": "altceva",
}


def mock(name: str) -> dict:
    return json.loads((config.MOCKS_DIR / name).read_text(encoding="utf-8"))


@st.cache_data(ttl=300, show_spinner=False)
def api(method: str, path: str, body: str | None = None) -> dict | None:
    try:
        r = httpx.request(
            method,
            config.API_URL + path,
            content=body,
            headers={"content-type": "application/json"},
            timeout=60,
        )
        r.raise_for_status()
        return r.json()
    except httpx.HTTPError:
        return None


st.set_page_config(page_title="Contoare suspecte", layout="wide")
health = api("GET", "/health") or mock("health.json")
st.title("Contoare suspecte")
st.caption(f"Date: {health['source']} · LLM: {health['llm']} · API: {config.API_URL}")

data = api("GET", "/anomalies?limit=10") or mock("anomalies.json")
items = data["items"]
table = pd.DataFrame(
    [
        {
            "loc": a["rank"],
            "contor": a["meter_id"],
            "tip": KINDS[a["kind"]],
            "scor": a["score"],
            "schimbare %": a["evidence"]["change_pct"],
            "zile zero": a["evidence"]["zero_days"],
            "de la": a["period"]["start"],
            "până la": a["period"]["end"],
        }
        for a in items
    ]
)
st.dataframe(table, hide_index=True)

meter = st.selectbox("Contor", [a["meter_id"] for a in items])
left, right = st.columns([2, 1])

series = api("GET", f"/meters/{meter}/series?days=14") or mock("series.json")
points = pd.DataFrame(series["points"])
points["ts"] = pd.to_datetime(points["ts"])
left.subheader("Ultimele 14 zile (kWh pe interval)")
left.line_chart(points.set_index("ts")["kwh"])

result = api("POST", "/explain", json.dumps({"meter_id": meter})) or mock("explain.json")
explanation = result["explanation"]
right.subheader("Explicație")
right.write(explanation["summary"])
for reason in explanation["reasons"]:
    right.markdown(f"- {reason}")
right.markdown(f"**Pas următor:** {explanation['next_step']}")
right.caption(
    f"Încredere: {explanation['confidence']} · model: {result['model']} · "
    "Propunere AI; decizia de inspecție o ia un om."
)

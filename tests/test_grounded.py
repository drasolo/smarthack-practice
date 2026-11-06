"""Hand-written explanations: the grounded metric must pass the good ones and catch the bad ones."""

from datetime import date

import pytest

from api.explain import _template
from contract.schema import Anomaly, Evidence, Explanation, Period
from evals.run import grounded

EVIDENCE = {
    "flatline_zero": Evidence(
        baseline_kwh_day=6.3,
        recent_kwh_day=0.0,
        change_pct=-100.0,
        zero_days=7,
        max_kwh_interval=0.24,
        spike_ratio=1.7,
    ),
    "sudden_drop": Evidence(
        baseline_kwh_day=9.6,
        recent_kwh_day=2.3,
        change_pct=-75.9,
        zero_days=0,
        max_kwh_interval=0.31,
        spike_ratio=1.6,
    ),
    "spike": Evidence(
        baseline_kwh_day=7.4,
        recent_kwh_day=8.1,
        change_pct=8.9,
        zero_days=0,
        max_kwh_interval=2.19,
        spike_ratio=13.2,
    ),
    "other": Evidence(
        baseline_kwh_day=9.4,
        recent_kwh_day=8.6,
        change_pct=-8.4,
        zero_days=0,
        max_kwh_interval=0.34,
        spike_ratio=1.7,
    ),
}


def anomaly(kind: str) -> Anomaly:
    period = Period(start=date(2026, 1, 1), end=date(2026, 1, 31))
    return Anomaly(
        rank=1,
        meter_id="M0042",
        score=1.0,
        kind=kind,
        period=period,
        evidence=EVIDENCE[kind],
    )


def say(summary: str, *reasons: str) -> Explanation:
    return Explanation(
        summary=summary, reasons=list(reasons) or ["x"], next_step="Vizită.", confidence="high"
    )


@pytest.mark.parametrize("kind", EVIDENCE)
def test_template_explanations_are_grounded(kind):
    a = anomaly(kind)
    assert grounded(_template(a), a)


@pytest.mark.parametrize(
    ("kind", "text"),
    [
        # a number that is not in the evidence
        ("sudden_drop", "Consumul contorului M0042 a scăzut cu 40%."),
        # rounded too far: -75.9% is not "aproape 80%"
        ("sudden_drop", "Consumul a scăzut cu aproape 80%, de la 9.6 kWh."),
        # true numbers, but not the drop itself
        ("sudden_drop", "Înainte, consumul era de 9.6 kWh pe zi."),
        # true numbers, but never says how long it was at zero
        ("flatline_zero", "Consumul tipic era de 6.3 kWh pe zi, acum e 0."),
        # invents a duration
        ("flatline_zero", "Contorul a raportat zero timp de 10 zile."),
        # a spike explanation that only talks about the daily level
        ("spike", "Consumul zilnic a fost de 8.1 kWh, față de 7.4 kWh."),
        # the ratio is invented
        ("spike", "Un interval de 2.19 kWh, de 20 de ori peste normal."),
        # "other" still may not invent numbers
        ("other", "Consumul a scăzut cu 25% în ultima lună."),
    ],
)
def test_bad_explanations_are_caught(kind, text):
    assert not grounded(say(text), anomaly(kind))


def test_numeric_meter_id_does_not_erase_evidence():
    a = anomaly("flatline_zero").model_copy(update={"meter_id": "7"})  # zero_days is also 7
    assert grounded(_template(a), a)


@pytest.mark.parametrize(
    ("meter_id", "text", "ok"),
    [
        ("42", "Contorul 42 a raportat zero consum timp de 7 zile.", True),
        ("7", "Contorul 7 a raportat zero consum.", False),  # the ID is not the duration
        ("42", "Contorul #42 a raportat zero consum timp de 7 zile.", True),
        ("M42", "Contorul M42- a raportat zero consum timp de 7 zile.", True),
    ],
)
def test_meter_id_mentions(meter_id, text, ok):
    a = anomaly("flatline_zero").model_copy(update={"meter_id": meter_id})
    assert grounded(say(text), a) is ok


@pytest.mark.parametrize(
    ("kind", "text"),
    [
        ("sudden_drop", "Consumul a scăzut cu 75.9%, la 2.3 kWh pe zi."),
        ("sudden_drop", "Consumul a scăzut la 2,3 kWh pe zi."),  # Romanian decimal comma
        ("flatline_zero", "Zero consum timp de 7 zile la rând."),
        ("spike", "Un vârf de 13.2 ori peste nivelul obișnuit."),
        ("other", "Niciun semnal clar."),
    ],
)
def test_good_hand_written_explanations_pass(kind, text):
    assert grounded(say(text), anomaly(kind))

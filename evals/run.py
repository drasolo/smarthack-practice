"""Build the evaluation table the pitch shows. Writes evals/results/latest.md.

Detection: our scorer against a naive baseline, on labelled data.
Explanations: four checks on the top meters' explanations (schema, grounded numbers, no PII,
language).
"""

from __future__ import annotations

import re
from datetime import datetime

from api.explain import explain_anomaly
from common import config, llm, pii
from contract.schema import Anomaly, Explanation
from evals.metrics import average_precision, precision_at_k, recall_at_k
from ml import detect
from ml.load import load_default, load_labels

K = 10
EXPLAINED = 5
_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}\.\d{1,2}\.\d{4}\b")
_NUMBER = re.compile(r"(?<!\w)-?\d+(?:[.,]\d+)?")  # not digits glued to letters, like M0024
_ROMANIAN = ("ă", "â", "î", "ș", "ț", " și ", " în ", " de ")


def grounded(explanation: Explanation, anomaly: Anomaly) -> bool:
    """Every number in the text matches an evidence value (or its absolute value, or K)."""
    allowed = [float(v) for v in anomaly.evidence.model_dump().values()]
    allowed += [abs(v) for v in allowed] + [float(K), 14.0]
    text = " ".join([explanation.summary, *explanation.reasons, explanation.next_step])
    for raw in _NUMBER.findall(_DATE.sub(" ", text)):
        value = float(raw.replace(",", "."))
        if not any(abs(value - a) <= max(0.051, 0.01 * abs(a)) for a in allowed):
            return False
    return True


def detection_rows(scores, labels) -> list[str]:
    if labels is None:
        return ["No labels for this data, so no detection metrics. Inject labelled anomalies."]
    relevant = set(labels["meter_id"])
    ours = list(scores["meter_id"])
    naive = list(scores.sort_values("drop_14d_pct")["meter_id"])  # biggest recent drop first
    row = lambda name, ranked: (  # noqa: E731
        f"| {name} | {precision_at_k(ranked, relevant, K):.2f} | "
        f"{recall_at_k(ranked, relevant, K):.2f} | {average_precision(ranked, relevant):.2f} |"
    )
    return [
        f"Labelled anomalies: {len(relevant)} of {len(ours)} meters.",
        "",
        f"| ranking | precision@{K} | recall@{K} | average precision |",
        "| --- | --- | --- | --- |",
        row("baseline scorer (ml/detect.py)", ours),
        row("naive: biggest drop first", naive),
    ]


def explanation_rows(scores) -> list[str]:
    anomalies = [detect.to_anomaly(r) for _, r in scores.head(EXPLAINED).iterrows()]
    checks = {"valid schema": 0, "numbers grounded in evidence": 0, "no PII in output": 0}
    language = "written in Romanian" if config.LLM_LANGUAGE == "ro" else None
    if language:
        checks[language] = 0
    for anomaly in anomalies:
        explanation = explain_anomaly(anomaly)  # schema-validated by construction
        checks["valid schema"] += 1
        checks["numbers grounded in evidence"] += grounded(explanation, anomaly)
        text = explanation.model_dump_json()
        checks["no PII in output"] += not pii.find(text)
        if language:
            checks[language] += any(marker in f" {text.lower()} " for marker in _ROMANIAN)
    n = len(anomalies)
    return [
        f"LLM: {llm.provider_name()}, top {n} meters.",
        "",
        "| check | passed |",
        "| --- | --- |",
        *[f"| {name} | {passed}/{n} |" for name, passed in checks.items()],
    ]


def build() -> str:
    readings, source = load_default()
    scores = detect.score(readings)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return "\n".join(
        [
            f"# Evaluation ({stamp}, data: {source})",
            "",
            "## Detection",
            "",
            *detection_rows(scores, load_labels(source)),
            "",
            "## Explanations",
            "",
            *explanation_rows(scores),
            "",
        ]
    )


def main() -> None:
    report = build()
    config.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (config.RESULTS_DIR / "latest.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()

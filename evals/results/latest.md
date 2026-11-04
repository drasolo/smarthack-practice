# Evaluation (2026-11-04 19:25, data: sample)

## Detection

Labelled anomalies: 7 of 40 meters.

| ranking | precision@10 | recall@10 | average precision |
| --- | --- | --- | --- |
| baseline scorer (ml/detect.py) | 0.70 | 1.00 | 1.00 |
| naive: biggest drop first | 0.30 | 0.43 | 0.52 |

## Explanations

LLM: fake, top 5 meters.

| check | passed |
| --- | --- |
| valid schema | 5/5 |
| numbers grounded in evidence | 5/5 |
| no PII in output | 5/5 |
| written in Romanian | 5/5 |

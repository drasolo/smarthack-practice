# Evals

`uv run dev.py eval` runs `evals/run.py` and writes `results/latest.md`, the table the pitch
shows.

- **Detection:** precision@10, recall@10 and average precision against labels, for our scorer
  and for a naive baseline. The sample has labels. For real data, inject labelled anomalies and
  write `DATA_DIR/processed/labels.csv` (see the `eval-table` skill).
- **Explanations:** for the top 5 meters, the share of explanations that pass four checks:
  valid schema, every number found in the evidence, no PII, written in Romanian.
- `metrics.py` also has forecast metrics (MAE, WAPE, error cost in lei) in case the challenge is
  a forecast.

The checks pass trivially with the `fake` provider. Run with a real model before the pitch.

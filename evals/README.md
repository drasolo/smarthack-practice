# Evals

`uv run dev.py eval` runs `evals/run.py` and writes `results/latest.md`, the table the pitch
shows.

- **Detection:** precision@10, recall@10 and average precision against labels, for the baseline
  scorer, the learned detector and a naive ranking. The sample has labels. For real data, inject
  labelled anomalies and write `DATA_DIR/processed/labels.csv` (see the `eval-table` skill).
- **Explanations:** separately for each detector's top 5 meters, the share passing four checks:
  valid schema, every number found in the evidence, no PII, written in Romanian.
- `metrics.py` also has forecast metrics (MAE, WAPE, error cost in lei) in case the challenge is
  a forecast.

The checks pass trivially with the `fake` provider. Run with a real model before the pitch.

`ml/learned.py` fits an Isolation Forest on the received cohort without reading labels. Its
features describe weekly drops, changes in slope, interval zeros and changes in the local
intraday profile. It returns the baseline's measured evidence and existing kinds, so it can
use the same contract. Its score is relative to the cohort, not a calibrated probability.
The API still uses `ml/detect.py`; the learned detector is an evaluation candidate.
The reported gain is on synthetic data. Unusual normal behavior can still rank highly.

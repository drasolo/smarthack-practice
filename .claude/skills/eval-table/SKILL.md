---
name: eval-table
description: Build or refresh the evaluation table the pitch shows. Use after a model or prompt change, before the pitch, or when someone asks how good the solution is.
---

# Evaluation table

1. Run `uv run dev.py eval`. It writes `evals/results/latest.md`.
2. Keep a baseline row next to every metric. Judges trust a number only next to a simple
   alternative (for anomalies "biggest drop first", for forecasts "same day last week").
3. Real data has no labels: inject labelled anomalies into a copy of it (scale a meter's
   consumption down, zero a week, add a spike), save the labels as
   `DATA_DIR/processed/labels.csv`, and measure on that.
4. Keep the four explanation checks: valid schema, numbers grounded in the evidence, no PII,
   language. Smoke runs them on the templates. Before the pitch, run them once more on a real
   login with `LLM_PROVIDER=claude`.
5. Copy the final table into `pitch/outline.md` under Evaluation, with one sentence on what it
   means in lei, hours or inspector visits.

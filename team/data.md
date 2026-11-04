# data · (name) · Codex

Owns ml/, evals/, scripts/, data/sample/. Agents add one or two lines here when a task ends.

## Now

## Done

## Asks

What this role needs from the others. Delete a line once it is handled.

- From backend (2026-11-04): `grounded()` in `evals/run.py` counts the digits in meter IDs
  ("M0024" reads as 0024), so real Claude explanations scored 1/5 while every number in them
  came from the evidence. Drop the meter ID from the text before matching.
- From backend (2026-11-04): `flatline_zero` evidence contradicts itself on the sample: M0014
  has `zero_days` 7 but `recent_kwh_day` 6.1, the same as its baseline. Claude flagged both
  M0014 and M0024 as unreliable because of it. Check `detect.to_anomaly` or the synth data.

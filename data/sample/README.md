# Synthetic sample

Made by `uv run dev.py synth` (`scripts/synth.py`, fixed seed). Safe for agents to read; it holds
no real customer.

- `readings.parquet`: 40 meters, 45 local days from 2026-03-15, 15-minute intervals, columns
  `meter_id`, `ts` (UTC), `kwh`.
- `meters.csv`: `meter_id`, `region`, `segment`.
- `labels.csv`: the injected anomalies (`meter_id`, `kind`, `start`, `end`). Only evals and tests
  should read it; a detector that looks at it is cheating.

It contains the traps real data has: the spring DST day, a cumulative register, a fully
missing day, scattered missing intervals and duplicate rows. Run `uv run dev.py profile
data/sample/readings.parquet` to see them.

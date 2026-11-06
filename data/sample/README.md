# Synthetic sample

Made by `uv run dev.py synth` (`scripts/synth.py`, fixed seed). Safe for agents to read; it holds
no real customer.

- `readings.parquet`: 120 meters, 45 local days from 2026-03-15, 15-minute intervals, columns
  `meter_id`, `ts` (UTC), `kwh`.
- `meters.csv`: `meter_id`, `region`, `segment`.
- `labels.csv`: the injected anomalies (`meter_id`, `kind`, `start`, `end`). Only evals and tests
  should read it; a detector that looks at it is cheating.

It contains the traps real data has: the spring DST day, a cumulative register, a fully
missing day, scattered missing intervals and duplicate rows. Run `uv run dev.py profile
data/sample/readings.parquet` to see them.

Meters M0001-M0040 hold the easy anomalies the baseline finds. Meters M0041-M0120 are harder:
small or gradual drops, a drop that ended weeks ago, hidden solar at midday, a daytime bypass,
zeros for half of each day, a small spike. They also hold unlabelled normal meters that look
suspicious: people away on holiday, electric heating fading out in spring, a new heater, noisy
meters, shops closed at weekends. The baseline flags the holidays and the heating; a real model
should not. The roles and their sizes are in `scripts/synth.py`.

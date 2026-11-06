# Context

The facts every agent needs and nobody should have to re-explain. Owned by everyone: change a
section only after posting to `@all` on the board.

## Brief

Practice brief (Thursday dry run, 2.5 hours): **find the 10 most anomalous households in a
smart-meter dataset and explain each one in plain Romanian to a field inspector.**

- Data: `data/sample/` (synthetic, labelled) to start. The data role then loads London smart
  meters (`uv run dev.py fetch london`, half-hourly) and injects labelled anomalies into a subset,
  since the real set has no labels.
- Done means: the UI lists the top 10 with a chart and an explanation each, the eval table shows
  precision@10 against a baseline, and the 3-minute demo runs without help.
- On the day, replace this section with the real brief, word for word, and a one-line summary.

## Glossary

- **POD**: point of delivery, one meter location. Our `meter_id`.
- **Interval**: one reading period. 15 minutes at PPC (96 per day), 30 minutes in London.
- **DST day**: last Sunday of March has 92 intervals of 15 minutes, last Sunday of October 100.
- **Cumulative register**: a meter that reports a running total. Diff it before use.
- **Prosumer**: a client that also exports power (negative or separate export values).
- **PZU**: the Romanian day-ahead market (prices per hour or per 15 minutes).

## Data

Clean readings table, the only shape `ml/` hands to the rest:

| column | type | note |
| --- | --- | --- |
| `meter_id` | string | anonymised |
| `ts` | timestamp, UTC | start of the interval |
| `kwh` | float or null | null means missing, never 0 |

Meters table: `meter_id`, `region`, `segment`. Labels (practice only): `meter_id`, `kind`,
`start`, `end`.

Findings from `ppc-data` go here: step, time zone, DST behaviour, missing values, counters.

## Contract

`contract/schema.py` is the source of truth, `contract/mocks/` holds one example per response.

- `GET /health` returns `Health`: data source (`sample`, `real` or `mock`) and LLM in use.
- `GET /anomalies?limit=10` returns `AnomalyList`: ranked meters with score, kind, period and
  evidence numbers.
- `GET /meters/{meter_id}/series?days=14` returns `Series`: interval points for the chart.
- `POST /explain` with `{"meter_id": "..."}` returns `ExplainResponse`: summary, reasons, next
  step and confidence, written from the evidence only.

## Decisions

One line each, newest last: date, decision, why.

- 2026-11-04: Python, FastAPI and Streamlit, one language for all three roles. Fastest path to
  a demo on data.
- 2026-11-04: real data outside the repo in `DATA_DIR`, so every Emdash worktree shares it and
  agents can't read raw rows by accident.
- 2026-11-04: offline `fake` LLM provider by default, so smoke and evals run without a key.
- 2026-11-04: `claude` LLM provider: the app calls Claude through each person's own Claude
  Code login, so real explanations need no API key. A handoff switches to `anthropic` and a key.
- 2026-11-04: roles own folders and agents don't belong to roles. Each of us has a different mix
  of Claude Code, Codex and Antigravity, and some run several at once.
- 2026-11-04: the board (issue #1) replaces `team/*.md` for claims, done posts and asks. Files
  only reached the others after a merge; the board is live.
- 2026-11-04: a different agent from the author reviews every branch before Dragoș merges it.
  Different models miss different things.

# smarthack-practice

Practice run for SmartHack 2026 (PPC challenge, 7-8 Nov). Three people, each driving AI agents:
Claude Code, Codex and Antigravity. This file is the shared context for all of them. Keep it
short. Details live in CONTEXT.md.

Check line: if someone asks "which repo is this?", answer "smarthack-practice, AGENTS.md loaded".

## What we build

CONTEXT.md > Brief says what. `pitch/demo-script.md` is the spec: a feature that isn't in the
demo waits. Background on the event, PPC and our preparation is in `docs/`: start at
`docs/README.md`, and follow `docs/reguli-pentru-documente.md` when you change anything there.

## Who owns what

| Role | Folders | Agent |
| --- | --- | --- |
| backend (Dragoș) | `api/`, `common/`, `dev.py`, merges into `main` | Claude Code in Emdash |
| data | `ml/`, `evals/`, `scripts/`, `data/sample/` | Codex |
| ui | `ui/`, `pitch/` | Antigravity |
| everyone | `contract/`, `CONTEXT.md` | change only after telling the group |

Edit only your owner's folders. If you need a change somewhere else, write it under "Asks" in
`team/<owner>.md` and tell your human.

## Commands

Run from the repo root. `uv run` creates the environment on first use.

- `uv run dev.py smoke`: the one check (lint, tests, API and UI boot, eval table). Nobody says
  "done" without running it and pasting the last lines.
- `uv run dev.py run`: API on `$EMDASH_PORT` (default 8000), UI on the next port (default 8501).
- `uv run dev.py eval`: writes `evals/results/latest.md`.
- `uv run dev.py profile <file>`: short profile of a dataset (step, intervals per day, nulls vs
  zeros, counters, duplicates).
- `uv run dev.py synth`: regenerates the synthetic sample in `data/sample/`.
- `uv add <pkg>`: the only way to add a dependency. Tell the group.

## Data rules

- Real data lives outside the repo in `DATA_DIR` (default `~/smarthack-data`). Never open, cat or
  head anything under `DATA_DIR/raw`. Use `dev.py profile` or a DuckDB aggregate instead.
- Read `data/sample/` and the schema in CONTEXT.md > Data.
- Prompts get aggregates, never raw customer rows. `common/llm.py` masks PII and logs every call.

## Working rules

- One task, one branch. Small commits prefixed by area: `api:`, `ml:`, `ui:`, `eval:`, `docs:`.
- Build against `contract/mocks/` until the real piece lands. A contract change updates
  `contract/schema.py`, the mocks and CONTEXT.md > Contract in the same commit.
- When a task ends, add one or two lines to `team/<your role>.md`: done, next, asks.
- A decision gets one line in CONTEXT.md > Decisions, with the reason.
- Replies stay short: what changed, the smoke output, what's next.

## Skills

In `.agents/skills/` (Codex and Antigravity read it). `uv run dev.py sync-skills` copies them to
`.claude/skills/` for Claude Code. Edit only the `.agents` copy.

- `ppc-data`: first-hour checks on a new dataset.
- `demo-check`: smoke plus a walk through the demo script.
- `eval-table`: refresh the evaluation table for the pitch.
- `pitch-qa`: jury questions and rehearsal.

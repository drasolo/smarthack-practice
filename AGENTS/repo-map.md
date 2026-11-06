# Repo map

What each folder holds and where new information goes. Who owns each folder is in AGENTS.md >
People and folders. When a top-level folder appears or changes purpose, update this file in the
same commit.

## Where to look

| To find | Read |
| --- | --- |
| The current brief, glossary, data schema, API contract, decisions | `CONTEXT.md` |
| What the demo must show (the spec) | `pitch/demo-script.md` |
| Pitch structure, likely jury questions | `pitch/outline.md`, `pitch/judge-qa.md` |
| The event, its rules and schedule, PPC, themes, ideas, the 24-hour plan, open questions | `docs/README.md`, which indexes `docs/` |
| Laptop setup, Emdash, the dry run | `README.md` |
| Board use, commands, data rules | `AGENTS.md` |
| How a task goes from start to merge | `AGENTS/workflow.md` |
| Claude Code additions | `CLAUDE.md` |

## Folders

| Folder | Holds |
| --- | --- |
| `AGENTS/` | Instructions for working in the repo: this map and the workflow |
| `.agents/` | Skills and Antigravity hooks. A different folder from `AGENTS/`, despite the name |
| `.claude/`, `.codex/` | Agent settings and hooks. `.claude/skills/` is a generated copy of `.agents/skills/` |
| `api/` | FastAPI app and the explanation endpoint |
| `common/` | Code shared across roles: config, LLM access, PII masking, the board |
| `contract/` | API schema and the mocks built against it |
| `data/sample/` | Synthetic labelled sample, safe to read. Real data lives outside the repo |
| `docs/` | Background reference, in Romanian, under the rules in `docs/reguli-pentru-documente.md` |
| `evals/` | Metrics, the eval runner and the table in `results/latest.md` |
| `ml/` | Data loading and the detection model |
| `pitch/` | Demo script, pitch outline, jury questions |
| `scripts/` | One-off tools behind `dev.py`: fetch, profile, synth, skill sync |
| `tests/` | Tests that smoke runs |
| `ui/` | Streamlit app |

## Where new information goes

| New information | Goes in |
| --- | --- |
| A decision and its reason | One line in `CONTEXT.md` > Decisions |
| A new term | `CONTEXT.md` > Glossary |
| The real brief, on the day | `CONTEXT.md` > Brief, word for word |
| A new data column or dataset shape | `CONTEXT.md` > Data |
| An endpoint or field change | `contract/schema.py`, the mocks and `CONTEXT.md` > Contract, in one commit |
| A fact about the event, PPC or the market | The matching file in `docs/` |
| Status, a request, a finding from a run | The board |
| A change to how we work | `AGENTS/workflow.md` |
| A rule every agent needs in every session | `AGENTS.md` |

Keep each fact in one place and link to it from anywhere else. Change the existing text; git keeps
the old version.

## Generated files

- `evals/results/latest.md`: only `uv run dev.py eval` writes it. Smoke builds the table and leaves
  the file alone. Commit it when you refresh the table on purpose.
- `.claude/skills/`: edit `.agents/skills/`, then run `uv run dev.py sync-skills`.
- `.board-state.json`: unread state for one checkout, ignored by git.

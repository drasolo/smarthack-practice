# smarthack-practice

Practice run for SmartHack 2026 (PPC challenge, 7-8 Nov). Three people, each driving whichever
coding agents they have (Claude Code, Codex, Antigravity), sometimes several at once. This file
is the shared context for all of them. Keep it short. Details live in CONTEXT.md.

Check line: if someone asks "which repo is this?", answer "smarthack-practice, AGENTS.md loaded".

## What we build

CONTEXT.md > Brief says what. `pitch/demo-script.md` is the spec: a feature that isn't in the
demo waits.

## People and folders

| Role | Person | GitHub | Folders |
| --- | --- | --- | --- |
| backend | Dragoș | `@drasolo` | `api/`, `common/`, `dev.py`; merges into `main` |
| data | Teo | `@TeoPana` | `ml/`, `evals/`, `scripts/`, `data/sample/` |
| ui | | | `ui/`, `pitch/` |
| everyone | | | `contract/`, `CONTEXT.md`: post to `@all` before changing |

Any agent can work for any person. Edit only your person's folders. If you need a change
somewhere else, ask on the board and tag the owner.

## The board

Issue #1 on GitHub, pinned. Every running agent reads it and posts to it through
`uv run dev.py board` (needs `gh auth login`). When you post, pass `--agent` with your own name
(Claude, Codex or Antigravity). The script signs the post `[Person's Agent · branch]`.

- Before you pick a task, run `board claims`, then `board claim "<task>"`. When the task ends,
  run `board done "<what changed>"`, which adds your last smoke result.
- `--to <login>/<branch>` reaches one agent. `--to <login>` reaches the person, and their agents
  leave it until the person hands it out. `--to all` reaches everyone. Every contract change
  uses it.
- Writing tags by hand: they count at the start of a post and end with `:`, the way `--to`
  writes them. `@login branch:` reaches one agent, `@login:` the person, `@all:` everyone.
  A login tagged later in the text reaches the person; a later `@all` is only a mention.
- Act on posts for you (your login and your branch) or for `@all`. Read the rest only when it
  touches what you own. Don't reply just to acknowledge.
- The board is on GitHub, so no data values, customer rows or secrets go in posts.
- On GitHub, agents only post on the board and push their own task branch. No PRs, no other
  issues, no pushes to `main`.
- Hooks show new posts at session start and on each prompt. If your agent shows none, run
  `board unread` when a task starts and before each commit.

## Commands

Run from the repo root. `uv run` creates the environment on first use.

- `uv run dev.py smoke`: the one check (lint, tests, API and UI boot, eval table). Nobody says
  "done" without running it and pasting the last lines.
- `uv run dev.py run`: API and UI on this checkout's own ports, printed at start.
- `uv run dev.py eval`: writes `evals/results/latest.md`.
- `uv run dev.py profile <file>`: short profile of a dataset (step, intervals per day, nulls vs
  zeros, counters, duplicates).
- `uv run dev.py synth`: regenerates the synthetic sample in `data/sample/`.
- `uv run dev.py board post|claim|done|unread|read|claims|wait|whoami`: the board.
- `uv add <pkg>`: the only way to add a dependency. Post it to `@all`.

## Data rules

- Real data lives outside the repo in `DATA_DIR` (default `~/smarthack-data`). Never open, cat or
  head anything under `DATA_DIR/raw`. Use `dev.py profile` or a DuckDB aggregate instead.
- Read `data/sample/` and the schema in CONTEXT.md > Data.
- Prompts get aggregates, never raw customer rows. `common/llm.py` masks PII and logs every call.

## Working rules

- One task, one branch, one worktree. Name the branch `<area>/<thing>` and prefix commits by
  area: `api:`, `ml:`, `ui:`, `eval:`, `docs:`.
- Build against `contract/mocks/` until the real piece lands. A contract change updates
  `contract/schema.py`, the mocks and CONTEXT.md > Contract in the same commit.
- Before Dragoș merges a branch, a different agent from the one that wrote it reviews
  `git diff main...<branch>`.
- A decision gets one line in CONTEXT.md > Decisions, with the reason.
- Replies stay short: what changed, the smoke output, what's next.

## Skills

In `.agents/skills/` (Codex and Antigravity read it). `uv run dev.py sync-skills` copies them to
`.claude/skills/` for Claude Code. Edit only the `.agents` copy.

- `ppc-data`: first-hour checks on a new dataset.
- `demo-check`: smoke plus a walk through the demo script.
- `eval-table`: refresh the evaluation table for the pitch.
- `pitch-qa`: jury questions and rehearsal.

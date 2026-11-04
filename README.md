# smarthack-practice

Practice repo for SmartHack 2026 (PPC challenge). We use it Thursday for a 2.5-hour dry run.
After the retro, the hackathon repo (`../event`) is made from it with the fixes. Agents start at
AGENTS.md; this page is for the three of us.

## Setup (each laptop, about 10 minutes)

1. Install uv. Windows: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`.
   macOS: `curl -LsSf https://astral.sh/uv/install.sh | sh`.
2. Clone the repo and run `uv run dev.py smoke`. The first run installs everything. It must end
   with `SMOKE OK`.
3. Copy `.env.example` to `.env`. Only the laptop that runs the real LLM needs
   `ANTHROPIC_API_KEY`; without it everything runs on the offline `fake` provider.
4. Open the repo in your agent and ask "which repo is this?". The answer must be
   "smarthack-practice, AGENTS.md loaded".
   - Codex and Antigravity read `AGENTS.md` and `.agents/skills/` on their own.
   - Claude Code reads `CLAUDE.md`, which imports `AGENTS.md`. Run `uv run dev.py sync-skills`
     once so it sees the skills too.

The data role also runs `uv run dev.py fetch london` the evening before (about 800 MB).

## Roles

| Role | Person | Folders | Agent |
| --- | --- | --- | --- |
| backend and integration | Dragoș | `api/`, `common/`, `dev.py` | Claude Code in Emdash |
| data and ML | | `ml/`, `evals/`, `scripts/` | Codex |
| UI, demo and pitch | | `ui/`, `pitch/` | Antigravity |

Status lives in `team/<role>.md`. Agents append to it when a task ends, so anyone can read where
the others are without asking.

## Git

- One private GitHub repo. `main` always demos.
- Work on branches named `<role>/<thing>` and push them. Dragoș merges into `main` every 60 to
  90 minutes, after smoke passes and a cross-model review. Then everyone runs
  `git pull --rebase origin main`.
- Folder ownership keeps conflicts rare. Changes to `contract/` or CONTEXT.md get announced in
  the group chat first.

## Emdash and the Work view (Dragoș's laptop)

- Add the `practice` folder as a project through the folder picker. `.emdash.json` makes every
  task copy `.env`, run `uv sync`, and start the app on that task's own ports.
- One Emdash task per slice, at most three at once. The Work view (Ctrl+I) shows the SmartHack
  plans and issues, and Ctrl+Shift+U jumps to the next agent waiting for an answer.
- In the project settings, set the worktree directory to
  `C:\Users\drago\Documents\uni\smarthack_ppc_26\worktrees`. Worktrees then sit inside the
  SmartHack folder, so conversations in them land on the SmartHack project in the Work view.

## Dry run (Thursday, 2.5 hours)

| time | what |
| --- | --- |
| 0:00 | Each person asks their agent the check question. Everyone reads CONTEXT.md > Brief. |
| 0:10 | Agree on the contract. It already exists: change it now or not at all. |
| 0:20 | data: profile London, write the loader, inject labelled anomalies. ui: UI on mocks (`USE_MOCKS=1`). backend: explanation prompt on the real LLM, three Emdash tasks in parallel. |
| 1:15 | First merge into `main`. Everyone pulls and runs smoke. |
| 1:45 | Eval table on London data. |
| 2:10 | Three-minute demo and three jury questions (`pitch-qa`). |
| 2:20 | Retro, ten minutes: keep, change, drop. One line each under CONTEXT.md > Decisions. |

## After the dry run

The event repo is made from this one, with the retro applied. It keeps everything except the
practice brief and the practice-only code. The SmartHack rules say nothing about code written
before the event, so ask the organizers whether a prepared skeleton is fine before Saturday.

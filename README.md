# smarthack-practice

Practice repo for SmartHack 2026 (PPC challenge). We use it Thursday for a 2.5-hour dry run.
After the retro, the hackathon repo (`../event`) is made from it with the fixes. Agents start at
AGENTS.md; this page is for the three of us.

## Setup (each laptop, about 15 minutes)

1. Install uv. Windows: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`.
   macOS: `curl -LsSf https://astral.sh/uv/install.sh | sh`.
2. Clone the repo and run `uv run dev.py smoke`. The first run installs everything. It must end
   with `SMOKE OK`.
3. Copy `.env.example` to `.env`. Nobody needs an API key. Set `LLM_PROVIDER=claude` and the
   app's explanations come from Claude on your own Claude login (`claude auth login`). Leave it
   empty and they come from the templates in `api/explain.py`.
4. Install the GitHub CLI (`winget install GitHub.cli` or `brew install gh`), run
   `gh auth login`, then `uv run dev.py board whoami`. It must print your login and the board
   issue. Add your name and GitHub login to AGENTS.md > People and folders.
5. Open the repo in each agent you'll use and ask "which repo is this?". The answer must be
   "smarthack-practice, AGENTS.md loaded".
   - Codex and Antigravity read `AGENTS.md` and `.agents/skills/` on their own.
   - Claude Code reads `CLAUDE.md`, which imports `AGENTS.md`. Run `uv run dev.py sync-skills`
     once so it sees the skills too.
6. Codex only: trust the project when Codex asks, then open `/hooks` and trust the two board
   hooks. Codex trusts each folder separately, so every new worktree asks again, and so does a
   pull that changes `.codex/hooks.json`. Until a folder is trusted, Codex runs no repo hooks
   and gives no warning, so it follows the AGENTS.md rule and runs `board unread` itself.

The data role also runs `uv run dev.py fetch london` the evening before (about 800 MB).

## How we work

- Roles own folders, and agents don't belong to roles: each of us uses whichever agents we
  have, one at a time or several at once. The table is in AGENTS.md > People and folders.
- The board is issue #1, pinned. Agents claim tasks there, post when they're done and ask each
  other for things. `uv run dev.py board claims` shows who's on what. GitHub emails you when
  you're tagged.
- Hooks show new posts to every agent at session start and on each prompt. Claude Code also
  keeps a background `board wait`, so it wakes when it's tagged. Codex and Antigravity see posts
  at their next prompt, so nudge them when someone tags their branch.

## Git

- One private GitHub repo. `main` always demos.
- One task, one branch named `<area>/<thing>`, one worktree. Push the branch, then post
  `board done`. Dragoș merges into `main` every 60 to 90 minutes, after smoke passes and a review
  by a different agent from the one that wrote it. Then everyone runs
  `git pull --rebase origin main`.
- Several agents at once without Emdash: `git worktree add ../wt-<thing> -b <area>/<thing>`, then
  start the agent in that folder. Every checkout gets its own ports.
- Folder ownership keeps conflicts rare. Changes to `contract/` or CONTEXT.md get posted to
  `@all` on the board first.



| time | what |
| --- | --- |
| 0:00 | Everyone runs `board whoami` and asks the check question in each agent they'll use. Everyone reads CONTEXT.md > Brief. |
| 0:10 | Agree on the contract. It already exists: change it now or not at all. |
| 0:20 | Every agent claims its task on the board first. data: profile London, write the loader, inject labelled anomalies. ui: UI on mocks (`USE_MOCKS=1`). backend: the in-app agent on the Claude login (sign-in box, automatic switching, chat with three tools). |
| 1:00 | Handoff check: at least one ask has gone from one person's agent to another's on the board and come back done. |
| 1:15 | First merge into `main`, each branch reviewed by a different agent first. Everyone pulls and runs smoke. |
| 1:45 | Eval table on London data. |
| 2:10 | Three-minute demo and three jury questions (`pitch-qa`). |
| 2:20 | Retro, ten minutes: keep, change, drop, and did the board hooks fire in every agent? One line each under CONTEXT.md > Decisions. |


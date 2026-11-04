@AGENTS.md

## Claude Code only

- Before merging a branch into `main`, run `/codex:review --base main` and fix or note what it
  finds. Codex-written code gets a Claude review the same way.
- Run `uv run dev.py sync-skills` after pulling changes to `.agents/skills/`.
- For screenshots of the UI, use the chrome-devtools MCP on the URL `dev.py run` prints.

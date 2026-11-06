@AGENTS.md

## Claude Code only

- Keep one background `uv run dev.py board wait` running (unless `BOARD_WAIT=off`). When it
  returns, act on what's for you, then start it again.
- `/codex:review --base main` gets a Codex review of your branch from inside Claude Code. That's
  the different-agent review a Claude-written branch needs before it merges.
- Run `uv run dev.py sync-skills` after pulling changes to `.agents/skills/`.
- For screenshots of the UI, use the chrome-devtools MCP on the URL `dev.py run` prints.

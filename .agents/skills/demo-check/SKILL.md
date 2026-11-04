---
name: demo-check
description: Check that the demo works end to end. Use before merging into main, before a team sync, before recording the backup video, and whenever someone asks "does it work".
---

# Demo check

1. Run `uv run dev.py smoke`. It must end with `SMOKE OK`. Paste the last 15 lines.
2. Start the app with `uv run dev.py run` and open the UI URL it prints.
3. Walk `pitch/demo-script.md` step by step in a browser (Antigravity's browser agent, or the
   chrome-devtools MCP in Claude Code). Save a screenshot of the main screen to
   `evals/results/screens/`.
4. Report each demo step as OK or broken, with the error for broken ones.

Fix nothing in another owner's folders. Put the problem under "Asks" in `team/<owner>.md`.

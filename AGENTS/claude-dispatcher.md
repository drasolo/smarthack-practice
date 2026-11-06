# Claude as dispatcher

Codex and Antigravity don't wake up by themselves when a board post arrives (AGENTS.md > Hooks and
setup per agent). So on each laptop one Claude Code session is the dispatcher. It watches the board
and wakes that person's other agents, so the person doesn't relay messages by hand. The person does
the setup once. Tested on Linux with Codex 0.167 on 6 Nov; Windows and Antigravity are untested.

## Who is the dispatcher

- One Claude Code session per laptop: the one its person names. If nobody named one, the Claude
  in the main checkout.
- It handles only its own person's agents on its own laptop. Each person uses their own logins
  and quotas.
- The other agents stay full agents. They claim, build, run smoke and post by themselves, as
  AGENTS.md says. The dispatcher doesn't do their tasks and doesn't commit for them.

## What the dispatcher does

1. Keeps one `board wait` running, as CLAUDE.md says. Other Claude sessions of the same person
   keep their own.
2. When a post is for one of its person's Codex branches (`<login>/<codex branch>`), it wakes
   that Codex session:

   ```
   codex queue --thread <session id> --resume --message "New board posts for you. Act on them as AGENTS.md says."
   ```

   The queued message starts a new turn in the running Codex session, and Codex's prompt hook
   shows the unread posts. In the test, Codex answered on the board 20 seconds later.
3. When its person hands Codex a task through Claude, the dispatcher first posts the task to
   `--to <login>/<codex branch>`, so it is on the board, then wakes Codex as in step 2.
4. For the review a Claude-written branch needs (AGENTS/workflow.md, step 7), it can run
   `codex review --base origin/main` in that branch's worktree. It is read-only. The dispatcher
   posts the findings to the author.

## Find the Codex session id

The id is the UUID at the end of the newest session file whose `cwd` is Codex's worktree:

```
grep -l '"cwd":"<codex worktree path>"' $(ls -t ~/.codex/sessions/*/*/*/*.jsonl) | head -1
```

If that finds nothing, ask your person.

## Setup check

At session start the dispatcher checks these. If one is missing, it tells its person what to do.
The person does the setup; agents don't edit `~/.codex`.

- Codex is set up as in AGENTS.md > Hooks and setup per agent: main checkout trusted, board hooks
  approved, network for `gh`.
- A Codex session runs in its own worktree, on its own branch.
- `codex queue` reaches it: send a test message asking Codex to answer on the board.
- Antigravity has no tested way to wake it from outside. Its person writes to it.

## Limits

- In the sandbox, `.git` is read-only, so Codex's commits and pushes wait for its person's
  approval. With the person away, Codex's work stays uncommitted until they come back.
- The dispatcher sends Codex only board posts addressed to it and tasks its person asked for.

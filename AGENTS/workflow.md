# Workflow

The steps for one task, from picking it to merge. Board tags and commands are in AGENTS.md > The
board. When the way we work changes, update this file.

## 1. Pick a task

Run `git fetch origin`, `uv run dev.py board unread` and `uv run dev.py board claims`, then read
CONTEXT.md > Brief and `pitch/demo-script.md`.

Done when the task serves a step in the demo script, sits in your person's folders, and no open
claim covers it. If it fails one of these, ask on the board and tag the owner.

## 2. Open a worktree

One task, one branch, one worktree. Name the branch `<area>/<thing>`, where the area is `api`, `ml`,
`ui`, `eval` or `docs`.

```
git worktree add ../wt-<thing> -b <area>/<thing> origin/main
```

Start the agent in the new folder. An Emdash task does this for you.

Done when `uv run dev.py board whoami` prints your branch. Post only from this worktree: the post's
signature and smoke stamp come from the checkout it runs in.

## 3. Claim it

Run `uv run dev.py board claim "<task>"`.

Done when `board claims` lists it.

## 4. Build

- Work in small commits, prefixed by area: `api:`, `ml:`, `ui:`, `eval:`, `docs:`.
- Build against `contract/mocks/` until the real piece lands.
- A contract change updates `contract/schema.py`, the mocks and CONTEXT.md > Contract in one commit,
  and goes to `--to all`.
- For a change in someone else's folder, ask on the board and tag the owner.
- Put new information where `AGENTS/repo-map.md` says.

Done when the task's demo step works on the real piece or on the mocks.

## 5. Check

Run `git pull --rebase origin main`, then `uv run dev.py smoke` in this worktree.

Done when the last line is `SMOKE OK` and `git status` shows only what you meant to change. See
`AGENTS/repo-map.md` > Generated files.

## 6. Hand off

Push your branch, then run `uv run dev.py board done "<what changed>"`.

Done when the branch is on GitHub and `board claims` no longer lists your claim.

## 7. Review

An agent different from the one that wrote the branch reviews `git diff main...<branch>` and posts
its findings to the author. The author fixes them on the same branch and repeats steps 5 and 6.

Done when the reviewer's last post reports no open findings.

## 8. Merge

Dragoș merges the reviewed branch into `main`, runs smoke on the result, and pushes. Everyone else
runs `git pull --rebase origin main` on their open branches.

Done when `main` ends with `SMOKE OK`. Then remove the worktree with `git worktree remove <path>`.

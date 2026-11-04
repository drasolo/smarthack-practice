"""The agent board: one pinned GitHub issue that every running agent reads and posts to.

`uv run dev.py board <command>`, on top of the GitHub CLI (`gh auth login` once):

  post TEXT    sign and post: [Person's Agent · branch] TEXT
  claim TEXT   "claim: TEXT", before you start a task
  done TEXT    "done: TEXT", when it ends, with this checkout's last smoke result
  unread       posts since this checkout last looked; marks them read
  read         the last posts (-n N, default 20)
  claims       claims with no done post yet
  wait         blocks until a post for you, your human or @all arrives, then prints it
  whoami       login, repo, board issue and branch: checks the setup

Posting takes --agent NAME (Claude, Codex, Antigravity) and --to LOGIN[/BRANCH] or --to all,
repeatable. TEXT "-" reads stdin. Env: BOARD_REPO (owner/name, default from the git remote),
BOARD_ISSUE (default 1), BOARD_WAIT=off (no background-wait reminder for Claude Code).

A post is for you when it tags your login plus your branch, or @all. A tag with only your login
is for your human. Unread state lives in this checkout's git dir, so every worktree (every agent)
has its own.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

from common import config

AGENTS = {"claude": "Claude", "codex": "Codex", "antigravity": "Antigravity"}
FIRST_RUN_POSTS = 5
OTHER_LINES = 10

_PREFIX = re.compile(r"^\[(?P<who>[^\]]+?)\s+·\s+(?P<branch>[^\]\s]+)\]\s*")
_LOGIN = re.compile(r"^@([A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)[:,]?$")
_BRANCH = re.compile(r"^[\w.-]+/[\w./-]*[\w-][:,]?$")
_ANY_TAG = re.compile(r"(?<![\w@])@([A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)")
_KIND = re.compile(r"^(claim|done)\s*:", re.IGNORECASE)

TIMEOUT = 20.0  # seconds per gh call; hooks lower it so a prompt never waits long


class BoardError(RuntimeError):
    pass


# --- talking to git and gh -------------------------------------------------------------------


def _run(cmd: list[str], stdin: str | None = None, timeout: float | None = None) -> str:
    try:
        done = subprocess.run(
            cmd,
            input=stdin,
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=config.ROOT,
            timeout=timeout or TIMEOUT,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise BoardError(f"{cmd[0]} failed: {error}") from error
    if done.returncode != 0:
        raise BoardError(done.stderr.strip() or f"{cmd[0]} exited {done.returncode}")
    return done.stdout


def _git(*args: str) -> str:
    return _run(["git", *args]).strip()


def _gh(*args: str, stdin: str | None = None) -> str:
    return _run(["gh", *args], stdin=stdin)


# --- who and where -----------------------------------------------------------------------------


@dataclass
class Me:
    login: str
    name: str
    branch: str
    repo: str
    issue: int

    @property
    def comments(self) -> str:
        return f"repos/{self.repo}/issues/{self.issue}/comments"


def repo_from_remote(url: str) -> str:
    match = re.search(r"github\.com[:/]+([^/]+/[^/]+?)(?:\.git)?/?$", url.strip())
    if not match:
        raise BoardError(f"origin is not a GitHub repo ({url!r}); set BOARD_REPO=owner/name")
    return match.group(1)


def people(agents_md: str) -> dict[str, str]:
    """GitHub login (lowercase) to person name, from the People table in AGENTS.md."""
    rows = [line for line in agents_md.splitlines() if line.lstrip().startswith("|")]
    header = next((r for r in rows if "GitHub" in r), None)
    if header is None:
        return {}
    cols = [c.strip().lower() for c in header.strip().strip("|").split("|")]
    if "person" not in cols or "github" not in cols:
        return {}
    who, gh = cols.index("person"), cols.index("github")
    names: dict[str, str] = {}
    for row in rows[rows.index(header) + 1 :]:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) <= max(who, gh):
            continue
        login = cells[gh].strip("`").lstrip("@").lower()
        if login and cells[who] and not set(login) <= {"-", ":"}:
            names[login] = cells[who]
    return names


def state_path() -> Path:
    return Path(_git("rev-parse", "--absolute-git-dir")) / "smarthack-board.json"


def load_state() -> dict:
    try:
        return json.loads(state_path().read_text("utf-8"))
    except (OSError, ValueError):
        return {}


def save_state(state: dict) -> None:
    state_path().write_text(json.dumps(state, indent=2), "utf-8")


def me() -> Me:
    state = load_state()
    repo = os.getenv("BOARD_REPO") or repo_from_remote(_git("remote", "get-url", "origin"))
    login = state.get("login") if state.get("repo") == repo else None
    if not login:
        login = _gh("api", "user", "--jq", ".login").strip()
        save_state(state | {"login": login, "repo": repo})
    try:
        names = people((config.ROOT / "AGENTS.md").read_text("utf-8"))
    except OSError:
        names = {}
    return Me(
        login=login,
        name=names.get(login.lower(), login),
        branch=_git("branch", "--show-current") or "detached",
        repo=repo,
        issue=int(os.getenv("BOARD_ISSUE") or 1),
    )


# --- posts -------------------------------------------------------------------------------------


@dataclass
class Post:
    id: int
    login: str
    created: str
    updated: str
    body: str
    who: str | None = None  # "Dragoș's Codex", from the signature
    branch: str | None = None  # the posting agent's branch
    text: str = ""  # the body after the signature
    tags: set[tuple[str, str | None]] = field(default_factory=set)  # (login, branch or None)
    everyone: bool = False

    @property
    def message(self) -> str:
        """The text after the address block."""
        return " ".join(self.text.split()[_address(self.text)[2] :])

    @property
    def kind(self) -> str | None:
        match = _KIND.match(self.message)
        return match.group(1).lower() if match else None


def _address(text: str) -> tuple[set[tuple[str, str | None]], bool, int]:
    """The leading address block, like "@ana ui/chat, @all:": tags, @all, tokens it uses.

    Each @login may be followed by one branch, which picks out one agent of that person.
    """
    tokens = text.split()
    tags: set[tuple[str, str | None]] = set()
    everyone, i = False, 0
    while i < len(tokens):
        match = _LOGIN.match(tokens[i])
        if not match:
            break
        login, ends = match.group(1).lower(), tokens[i].endswith((":", ","))
        i += 1
        if login == "all":
            everyone = True
            continue
        branch = None
        if not ends and i < len(tokens) and _BRANCH.match(tokens[i]):
            branch = tokens[i].rstrip(":,")
            i += 1
        tags.add((login, branch))
    return tags, everyone, i


def parse(comment: dict) -> Post:
    body = comment.get("body") or ""
    post = Post(
        id=int(comment["id"]),
        login=(comment.get("user") or {}).get("login", ""),
        created=comment.get("created_at", ""),
        updated=comment.get("updated_at") or comment.get("created_at", ""),
        body=body,
    )
    text = body
    match = _PREFIX.match(body)
    if match:
        post.who, post.branch = match.group("who").strip(), match.group("branch")
        text = body[match.end() :]
    post.text = text
    post.tags, post.everyone, used = _address(text)
    # Tags anywhere else in the text reach the person, never a specific agent.
    for login in _ANY_TAG.findall(" ".join(text.split()[used:])):
        if login.lower() == "all":
            post.everyone = True
        else:
            post.tags.add((login.lower(), None))
    return post


def classify(post: Post, me: Me) -> str:
    """own, you, human or other, seen from this checkout's agent."""
    login = me.login.lower()
    if post.login.lower() == login and post.branch == me.branch:
        return "own"
    if (login, me.branch) in post.tags or post.everyone:
        return "you"
    if (login, None) in post.tags:
        return "human"
    return "other"


def compose(name: str, agent: str, branch: str, text: str, to: list[str] | None = None) -> str:
    tags = []
    for target in to or []:
        login, _, target_branch = target.lstrip("@").partition("/")
        tags.append("@all" if login.lower() == "all" else f"@{login} {target_branch}".rstrip())
    address = ", ".join(tags) + ": " if tags else ""
    return f"[{name}'s {agent} · {branch}] {address}{text.strip()}"


def open_claims(posts: list[Post]) -> list[Post]:
    """Each agent's latest claim that no later done post from the same branch closes."""
    claims: dict[tuple[str, str], Post] = {}
    for post in sorted(posts, key=lambda p: p.id):
        if not post.branch:
            continue
        key = (post.login.lower(), post.branch)
        if post.kind == "claim":
            claims[key] = post
        elif post.kind == "done":
            claims.pop(key, None)
    return sorted(claims.values(), key=lambda p: p.id)


# --- fetching ----------------------------------------------------------------------------------


def fetch(me: Me, since: str | None = None) -> list[Post]:
    path = f"{me.comments}?per_page=100" + (f"&since={since}" if since else "")
    pages = json.loads(_gh("api", "--paginate", "--slurp", path) or "[]")
    comments = [c for page in pages for c in (page if isinstance(page, list) else [page])]
    return sorted((parse(c) for c in comments), key=lambda p: p.id)


def fetch_last(me: Me, n: int) -> list[Post]:
    count = int(_gh("api", f"repos/{me.repo}/issues/{me.issue}", "--jq", ".comments").strip())
    if count == 0:
        return []
    last_page = math.ceil(count / 100)
    pages = range(max(1, last_page - math.ceil(n / 100)), last_page + 1)
    comments = []
    for page in pages:
        comments += json.loads(_gh("api", f"{me.comments}?per_page=100&page={page}") or "[]")
    return sorted((parse(c) for c in comments), key=lambda p: p.id)[-n:]


# --- rendering ---------------------------------------------------------------------------------


def _when(stamp: str) -> str:
    try:
        return (
            datetime.fromisoformat(stamp.replace("Z", "+00:00")).astimezone().strftime("%a %H:%M")
        )
    except ValueError:
        return stamp


def line(post: Post, limit: int | None = None) -> str:
    body = post.body if post.who else f"[{post.login}] {post.body}"
    body = " ".join(body.split())
    if limit and len(body) > limit:
        body = body[: limit - 1] + "…"
    return f"- #{post.id} {_when(post.created)} {body}"


def render(posts: list[Post], me: Me, header: bool = True) -> str:
    groups: dict[str, list[Post]] = {"you": [], "human": [], "other": []}
    for post in posts:
        kind = classify(post, me)
        if kind != "own":
            groups[kind].append(post)
    total = sum(len(g) for g in groups.values())
    if not total:
        return ""
    out = [f"Board (issue #{me.issue}): {total} new post{'s' * (total != 1)}."] if header else []
    if groups["you"]:
        out += ["For you (act on these):", *(line(p) for p in groups["you"])]
    if groups["human"]:
        out += [
            f"For your human (@{me.login} without a branch; wait until they hand it out):",
            *(line(p) for p in groups["human"]),
        ]
    if groups["other"]:
        shown = groups["other"][-OTHER_LINES:]
        out += ["Other posts (act only if they touch what you own):"]
        out += [line(p, 140) for p in shown]
        if len(groups["other"]) > len(shown):
            out.append(f"- and {len(groups['other']) - len(shown)} older; `board read` shows them")
    return "\n".join(out)


def render_claims(claims: list[Post]) -> str:
    if not claims:
        return "Open claims: none."
    return "\n".join(
        ["Open claims:"]
        + [f"- {c.branch} · {c.who} · {_KIND.sub('', c.message).strip()}" for c in claims]
    )


# --- commands ----------------------------------------------------------------------------------


def unread(event: str = "prompt", agent: str | None = None) -> str:
    """New posts since this checkout last looked, marked read. At session start also the claims."""
    who = me()
    state = load_state()
    first = "last_id" not in state
    posts = fetch(who) if first or event == "start" else fetch(who, state.get("since"))
    last_id = state.get("last_id", 0)
    new = [p for p in posts if p.id > last_id]
    if first:
        new = new[-FIRST_RUN_POSTS:]
    if posts:
        state["last_id"] = max(last_id, posts[-1].id)
        state["since"] = max([state.get("since") or ""] + [p.updated for p in posts])
    save_state(state)

    text = render(new, who)
    if event != "start":
        return text
    parts = [
        f"Agent board: issue #{who.issue} in {who.repo}. You post as "
        f"[{who.name}'s <Agent> · {who.branch}] with `uv run dev.py board post --agent <Agent>`.",
        render_claims(open_claims(posts)),
    ]
    if text:
        parts.append(text)
    if agent == "claude" and os.getenv("BOARD_WAIT", "").lower() != "off":
        parts.append(
            "Keep one background `uv run dev.py board wait` running. When it returns, act on "
            "what's for you, then start it again."
        )
    return "\n".join(parts)


def post(text: str, agent: str | None, to: list[str] | None = None) -> str:
    agent = _agent_name(agent)
    who = me()
    body = compose(who.name, agent, who.branch, text, to)
    sent = json.loads(
        _gh(
            "api",
            "--method",
            "POST",
            who.comments,
            "--input",
            "-",
            stdin=json.dumps({"body": body}),
        )
    )
    return f"posted #{sent['id']}: {body}"


def _agent_name(agent: str | None) -> str:
    agent = agent or os.getenv("BOARD_AGENT") or ("Claude" if os.getenv("CLAUDECODE") else None)
    if not agent:
        raise BoardError("say which agent you are: --agent Claude, Codex or Antigravity")
    return AGENTS.get(agent.lower(), agent)


def record_smoke(result: str) -> None:
    """Called by `dev.py smoke`, so a done post can carry the result."""
    state = load_state()
    state["smoke"] = {
        "result": result,
        "at": datetime.now(UTC).isoformat(timespec="seconds"),
        "head": _git("rev-parse", "HEAD"),
    }
    save_state(state)


def smoke_note() -> str:
    smoke = load_state().get("smoke")
    if not smoke:
        return "smoke: not run in this checkout"
    note = f"smoke: {smoke['result']} at {_when(smoke['at'])}"
    try:
        if smoke.get("head") != _git("rev-parse", "HEAD"):
            note += ", before the latest commit"
    except BoardError:
        pass
    return note


def wait(interval: float = 30) -> str:
    """Poll until a post for this agent, its human or @all arrives. Errors just retry later.

    Other posts seen on the way are printed with it and marked read, so none get skipped.
    """
    cursor, seen, delay = None, {}, interval
    while True:
        try:
            who = me()
            state = load_state()
            if "last_id" not in state:  # first look from this checkout: start from now
                posts = fetch(who)
                state["last_id"] = posts[-1].id if posts else 0
                state["since"] = max((p.updated for p in posts), default=None)
                save_state(state)
            cursor = cursor or state.get("since")
            posts = fetch(who, cursor)
            if posts:
                cursor = max([cursor or ""] + [p.updated for p in posts])
            for p in posts:
                if p.id > state["last_id"]:
                    seen[p.id] = p
            fresh = [seen[i] for i in sorted(seen)]
            if any(classify(p, who) in {"you", "human"} for p in fresh):
                state["last_id"] = fresh[-1].id
                state["since"] = cursor
                save_state(state)
                return render(fresh, who)
            delay = interval
        except BoardError:
            delay = min(delay * 2, 300)
        time.sleep(delay)


def whoami() -> str:
    who = me()
    title = _gh("api", f"repos/{who.repo}/issues/{who.issue}", "--jq", ".title").strip()
    return "\n".join(
        [
            f"login: {who.login} ({who.name})",
            f"board: {who.repo} issue #{who.issue}, {title!r}",
            f"branch: {who.branch}",
            f"state: {state_path()}",
        ]
    )


def hook(agent: str, event: str, stdin: str = "") -> str:
    """What a hook prints. Never raises: a broken board must never block a prompt."""
    global TIMEOUT
    TIMEOUT = 8.0
    try:
        payload = json.loads(stdin) if stdin.strip() else {}
    except ValueError:
        payload = {}
    if agent == "antigravity" and event == "prompt" and payload.get("invocationNum", 0) != 0:
        return (
            "{}"  # Antigravity's PreInvocation runs before every model call; only the first counts
        )
    try:
        text = unread(event, agent)
    except Exception:  # noqa: BLE001
        text = ""
    if agent == "antigravity":
        steps = [{"systemMessage": {"systemMessage": text}}] if text else []
        return json.dumps({"injectSteps": steps} if steps else {})
    return text


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="dev.py board",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("post", "claim", "done"):
        cmd = sub.add_parser(name)
        cmd.add_argument("text", nargs="+")
        cmd.add_argument("--agent")
        cmd.add_argument("--to", action="append", default=[])
    cmd = sub.add_parser("unread")
    cmd.add_argument("--hook", choices=sorted(AGENTS))
    cmd.add_argument("--event", choices=["start", "prompt"], default="prompt")
    sub.add_parser("read").add_argument("-n", type=int, default=20)
    sub.add_parser("claims")
    sub.add_parser("wait").add_argument("--interval", type=float, default=30)
    sub.add_parser("whoami")
    args = parser.parse_args(argv)

    if args.command == "unread" and args.hook:
        stdin = "" if sys.stdin is None or sys.stdin.isatty() else sys.stdin.read()
        out = hook(args.hook, args.event, stdin)
        if out:
            print(out)
        return 0
    try:
        if args.command in {"post", "claim", "done"}:
            text = sys.stdin.read() if args.text == ["-"] else " ".join(args.text)
            if args.command == "claim":
                text = f"claim: {text}"
            elif args.command == "done":
                text = f"done: {text.rstrip('. ')}. {smoke_note()}"
            print(post(text, args.agent, args.to))
        elif args.command == "unread":
            print(unread(args.event) or "No new posts.")
        elif args.command == "read":
            who = me()
            print("\n".join(line(p) for p in fetch_last(who, args.n)) or "The board is empty.")
        elif args.command == "claims":
            print(render_claims(open_claims(fetch(me()))))
        elif args.command == "wait":
            print(wait(args.interval))
        elif args.command == "whoami":
            print(whoami())
    except BoardError as error:
        print(f"board: {error}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130
    return 0

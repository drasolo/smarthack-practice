"""The agent board with gh and git faked: signing, addressing, claims, unread state, hooks."""

import json

import pytest

from common import board, config

LOGIN, BRANCH = "drasolo", "api/agent-board"


def comment(i, body, login=LOGIN):
    stamp = f"2026-11-05T10:{i:02d}:00Z"
    return {
        "id": i,
        "user": {"login": login},
        "body": body,
        "created_at": stamp,
        "updated_at": stamp,
    }


@pytest.fixture
def fake(monkeypatch, tmp_path):
    """A fake board: `fake.comments` is the issue, `fake.posted` what was sent."""

    class Fake:
        comments: list[dict] = []
        posted: list[str] = []
        broken = False

    def gh(*args, stdin=None):
        if Fake.broken:
            raise board.BoardError("gh: not logged in")
        if args[:2] == ("api", "user"):
            return LOGIN + "\n"
        if "--method" in args:
            body = json.loads(stdin)["body"]
            Fake.posted.append(body)
            Fake.comments.append(comment(len(Fake.comments) + 100, body))
            return json.dumps({"id": len(Fake.comments) + 99})
        path = args[-1]
        since = path.split("since=")[1] if "since=" in path else ""
        page = [c for c in Fake.comments if c["updated_at"] >= since]
        return json.dumps([page])

    git_dir = tmp_path / "gitdir"
    git_dir.mkdir()
    answers = {
        ("rev-parse", "--absolute-git-dir"): str(git_dir),
        ("remote", "get-url", "origin"): "https://github.com/drasolo/smarthack-practice.git",
        ("branch", "--show-current"): BRANCH,
        ("rev-parse", "HEAD"): "abc123",
    }
    monkeypatch.setattr(board, "_gh", gh)
    monkeypatch.setattr(board, "_git", lambda *args: answers[args])
    monkeypatch.delenv("BOARD_REPO", raising=False)
    monkeypatch.delenv("BOARD_ISSUE", raising=False)
    Fake.comments, Fake.posted = [], []
    return Fake


def me(branch=BRANCH):
    return board.Me(LOGIN, "Dragoș", branch, "drasolo/smarthack-practice", 1)


def test_compose_signs_and_addresses():
    body = board.compose("Dragoș", "Codex", "ml/loader", "mock ready", ["drasolo/api/chat", "all"])
    assert body == "[Dragoș's Codex · ml/loader] @drasolo api/chat, @all: mock ready"
    post = board.parse(comment(1, body))
    assert (post.who, post.branch) == ("Dragoș's Codex", "ml/loader")
    assert post.tags == {("drasolo", "api/chat")} and post.everyone
    assert post.message == "mock ready"


@pytest.mark.parametrize(
    "body, expected",
    [
        ("[Ana's Codex · ml/x] @drasolo api/agent-board: your turn", "you"),
        ("[Ana's Codex · ml/x] @all: contract changed", "you"),
        ("[Ana's Codex · ml/x] @drasolo: can you look?", "human"),
        ("[Ana's Codex · ml/x] the loader is in, thanks @drasolo", "human"),
        ("[Ana's Codex · ml/x] @drasolo api/chat: for your other agent", "other"),
        ("[Ana's Codex · ml/x] claim: London loader", "other"),
        ("[Dragoș's Claude · api/agent-board] claim: the board", "own"),
        ("plain comment from the GitHub page, @drasolo", "human"),
    ],
)
def test_classify(body, expected):
    login = "ana" if body.startswith("[Ana") else LOGIN
    assert board.classify(board.parse(comment(1, body, login)), me()) == expected


def test_open_claims_close_on_done():
    posts = [
        board.parse(comment(1, "[Ana's Codex · ml/loader] claim: London loader", "ana")),
        board.parse(comment(2, "[Dragoș's Claude · api/board] claim: the board")),
        board.parse(
            comment(3, "[Ana's Codex · ml/loader] done: loader merged. smoke: SMOKE OK", "ana")
        ),
        board.parse(comment(4, "[Ana's Codex · ml/labels] claim: inject labels", "ana")),
    ]
    assert [p.branch for p in board.open_claims(posts)] == ["api/board", "ml/labels"]
    assert "the board" in board.render_claims(board.open_claims(posts))


def test_people_table_from_agents_md():
    names = board.people((config.ROOT / "AGENTS.md").read_text("utf-8"))
    assert names.get("drasolo") == "Dragoș"


def test_unread_first_run_then_only_new(fake):
    fake.comments = [comment(i, f"[Ana's Codex · ml/x] note {i}", "ana") for i in range(1, 9)]
    first = board.unread()
    assert "note 8" in first and "note 3" not in first  # first look shows the last five
    assert board.unread() == ""  # nothing new
    fake.comments.append(comment(20, "[Ana's Codex · ml/x] @drasolo api/agent-board: ping", "ana"))
    fake.comments.append(comment(21, f"[Dragoș's Claude · {BRANCH}] my own post"))
    text = board.unread()
    assert "For you" in text and "ping" in text and "my own post" not in text


def test_post_and_done_carry_signature_and_smoke(fake, monkeypatch):
    monkeypatch.delenv("CLAUDECODE", raising=False)
    monkeypatch.delenv("BOARD_AGENT", raising=False)
    with pytest.raises(board.BoardError):
        board.post("hello", None)
    board.record_smoke("SMOKE OK")
    assert board.main(["done", "board script", "--agent", "codex"]) == 0
    assert fake.posted[-1].startswith(
        f"[Dragoș's Codex · {BRANCH}] done: board script. smoke: SMOKE OK"
    )


def test_start_lists_claims_and_reminds_claude(fake):
    fake.comments = [comment(1, "[Ana's Codex · ml/loader] claim: London loader", "ana")]
    text = board.unread("start", "claude")
    assert "ml/loader · Ana's Codex · London loader" in text
    assert "board wait" in text


def test_antigravity_hook_runs_once_per_prompt(fake):
    fake.comments = [comment(1, "[Ana's Codex · ml/x] @all: contract changed", "ana")]
    assert board.hook("antigravity", "prompt", json.dumps({"invocationNum": 2})) == "{}"
    out = json.loads(board.hook("antigravity", "prompt", json.dumps({"invocationNum": 0})))
    assert "contract changed" in out["injectSteps"][0]["systemMessage"]["systemMessage"]
    assert board.hook("antigravity", "prompt", json.dumps({"invocationNum": 0})) == "{}"


def test_hooks_stay_silent_when_gh_fails(fake):
    fake.broken = True
    assert board.hook("claude", "start") == ""
    assert board.hook("codex", "prompt") == ""
    assert board.hook("antigravity", "start") == "{}"


def test_port_blocks_are_stable_and_differ(tmp_path):
    a, b = tmp_path / "practice", tmp_path / "worktrees" / "agent-board"
    assert config.port_block(a) == config.port_block(a)
    assert config.port_block(a) != config.port_block(b)
    assert all(
        40000 <= config.port_block(p) < 50000 and config.port_block(p) % 10 == 0 for p in (a, b)
    )

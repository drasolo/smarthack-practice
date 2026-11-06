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
        if "--slurp" in args or "--paginate" in args:  # like gh 2.45, Ubuntu's apt version
            raise board.BoardError("unknown flag: --slurp")
        path = args[-1]
        query = dict(part.split("=", 1) for part in path.partition("?")[2].split("&") if part)
        matching = [c for c in Fake.comments if c["updated_at"] >= query.get("since", "")]
        page, size = int(query.get("page", 1)), int(query.get("per_page", 100))
        return json.dumps(matching[(page - 1) * size : page * size])

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
        # review fixes: a later @all is a mention, a path after a tag is text
        ("[Ana's Codex · ml/x] claim: contract tweak, will post to @all first", "other"),
        ("[Ana's Codex · ml/x] @drasolo api/app.py crashes on load", "human"),
        ("[Ana's Codex · ml/x] @drasolo thanks, the loader works", "human"),
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


def test_path_after_a_tag_stays_in_the_message():
    post = board.parse(comment(1, "[Ana's Codex · ml/x] @drasolo ui/app.py crashes on load", "ana"))
    assert post.tags == {("drasolo", None)}
    assert post.message == "ui/app.py crashes on load"


def test_agent_on_main_can_be_reached():
    body = board.compose("Ana", "Codex", "ml/x", "pull please", ["drasolo/main"])
    post = board.parse(comment(1, body, "ana"))
    assert board.classify(post, me("main")) == "you"
    assert post.message == "pull please"


def test_read_marker_only_moves_forward_and_keeps_other_keys(fake):
    board.record_smoke("SMOKE OK")
    board.mark_read(10, "2026-11-05T10:10:00Z")
    board.mark_read(5, "2026-11-05T10:05:00Z")  # a slower process finishing late
    state = board.load_state()
    assert (state["last_id"], state["since"]) == (10, "2026-11-05T10:10:00Z")
    assert state["smoke"]["result"] == "SMOKE OK"
    assert not list(board.state_path().parent.glob("*.tmp"))


def test_wait_retries_when_gh_returns_garbage(fake, monkeypatch):
    calls = {"n": 0}
    real_gh = board._gh

    def flaky(*args, stdin=None):
        if args[:2] != ("api", "user") and "--method" not in args:
            calls["n"] += 1
            if calls["n"] == 1:
                return "<html>proxy error</html>"
        return real_gh(*args, stdin=stdin)

    monkeypatch.setattr(board, "_gh", flaky)
    monkeypatch.setattr(board.time, "sleep", lambda seconds: None)
    board.save_state({"last_id": 0})
    fake.comments = [comment(1, f"[Ana's Codex · ml/x] @drasolo {BRANCH}: ping", "ana")]
    assert "ping" in board.wait(interval=0)
    assert board.load_state()["last_id"] == 1


def test_ui_port_alone_is_honoured(monkeypatch):
    import dev

    monkeypatch.delenv("EMDASH_PORT", raising=False)
    monkeypatch.delenv("API_PORT", raising=False)
    monkeypatch.setenv("UI_PORT", "8501")
    monkeypatch.setattr(config, "UI_PORT", 8501)
    assert dev.ports()[1] == 8501


def test_fetch_reads_every_page_without_slurp(fake):
    fake.comments = [comment(i, f"[Ana's Codex · ml/x] note {i}", "ana") for i in range(1, 251)]
    assert [p.id for p in board.fetch(me())] == list(range(1, 251))

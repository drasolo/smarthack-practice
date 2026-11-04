"""The `claude` provider, with the CLI faked. The real call is checked by `LLM_PROVIDER=claude
uv run dev.py eval`."""

import json
import subprocess

import pytest

from common import claude_cli, config, llm
from contract.schema import Explanation


@pytest.fixture(autouse=True)
def fresh_login_check(monkeypatch, tmp_path):
    monkeypatch.setattr(claude_cli, "_plan_checked", False)
    monkeypatch.setattr(config, "LOG_DIR", tmp_path)


def fake_cli(monkeypatch, auth: dict, result: dict) -> list:
    calls = []

    def run(args, stdin="", timeout=60):
        calls.append((args, stdin))
        out = auth if args[0] == "auth" else result
        return subprocess.CompletedProcess(args, 0, stdout=json.dumps(out), stderr="")

    monkeypatch.setattr(claude_cli, "_run", run)
    return calls


def test_env_never_carries_an_api_key(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "test")
    monkeypatch.setenv("CLAUDE_CODE_OAUTH_TOKEN", "")
    env = claude_cli._env()
    assert not {"ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "CLAUDE_CODE_OAUTH_TOKEN"} & set(env)


def test_ask_json_returns_the_structured_output(monkeypatch):
    calls = fake_cli(
        monkeypatch,
        {"authMethod": "claude.ai"},
        {"is_error": False, "structured_output": {"title": "x"}},
    )
    assert claude_cli.ask_json({"type": "object"}, "sys", "the question") == {"title": "x"}
    args, stdin = calls[-1]
    assert args[args.index("--json-schema") + 1] == '{"type": "object"}'
    assert stdin == "the question"


def test_refuses_a_login_that_is_not_a_plan(monkeypatch):
    fake_cli(monkeypatch, {"authMethod": "api_key"}, {})
    with pytest.raises(claude_cli.ClaudeCLIError, match="not a Claude plan"):
        claude_cli.ask_json({}, "sys", "user")


def test_error_result_raises(monkeypatch):
    fake_cli(monkeypatch, {"authMethod": "claude.ai"}, {"is_error": True, "result": "limit hit"})
    with pytest.raises(claude_cli.ClaudeCLIError, match="limit hit"):
        claude_cli.ask_json({}, "sys", "user")


def test_llm_ask_validates_the_claude_answer(monkeypatch):
    monkeypatch.setattr(config, "LLM_PROVIDER", "claude")
    answer = {
        "summary": "s",
        "reasons": ["r1", "r2"],
        "next_step": "n",
        "confidence": "high",
    }
    fake_cli(monkeypatch, {"authMethod": "claude.ai"}, {"structured_output": answer})
    result = llm.ask(Explanation, "sys", "user", fake=lambda: None)
    assert result == Explanation.model_validate(answer)

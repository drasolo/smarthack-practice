"""Call Claude through the Claude Code CLI on a Claude plan login, with no API key.

Self-contained: copy this file into any Python project. It needs the `claude` CLI signed in
with `claude auth login`, or CLAUDE_CODE_OAUTH_TOKEN set to a token from `claude setup-token`
on a machine where nobody can sign in. Each call counts against that account's plan limits.

A login is personal. Everyone signs in with their own account. An app that other people use
needs an API key instead, so hand a project off by switching it to one.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from typing import Any

PLAN_LOGINS = {"claude.ai", "oauth_token"}
_API_VARS = ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")
_plan_checked = False


class ClaudeCLIError(RuntimeError):
    pass


def _env() -> dict[str, str]:
    # A key left in the environment would make the CLI bill the API instead of the plan.
    env = {k: v for k, v in os.environ.items() if k not in _API_VARS}
    if not env.get("CLAUDE_CODE_OAUTH_TOKEN"):
        env.pop("CLAUDE_CODE_OAUTH_TOKEN", None)
    return env


def _run(args: list[str], stdin: str = "", timeout: float = 60) -> subprocess.CompletedProcess:
    exe = shutil.which("claude")
    if exe is None:
        raise ClaudeCLIError("Claude Code isn't installed: https://code.claude.com/docs/en/setup")
    # An empty working folder, so no CLAUDE.md or project settings end up in the prompt.
    with tempfile.TemporaryDirectory() as cwd:
        return subprocess.run(
            [exe, *args],
            input=stdin,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout,
            cwd=cwd,
            env=_env(),
        )


def login() -> dict[str, Any]:
    """`claude auth status` as a dict: loggedIn, authMethod, subscriptionType and more."""
    done = _run(["auth", "status"], timeout=30)
    try:
        return json.loads(done.stdout)
    except json.JSONDecodeError:
        return {"loggedIn": False, "authMethod": "none"}


def require_plan_login() -> None:
    global _plan_checked
    if _plan_checked:
        return
    method = login().get("authMethod", "none")
    if method == "none":
        raise ClaudeCLIError("Claude Code isn't signed in. Run `claude auth login`.")
    if method not in PLAN_LOGINS:
        raise ClaudeCLIError(
            f"Claude Code is signed in with {method!r}, not a Claude plan. "
            "Run `claude auth login` and pick your Claude account."
        )
    _plan_checked = True


def ask_json(
    schema: dict[str, Any],
    system: str,
    user: str,
    *,
    model: str = "sonnet",
    effort: str | None = None,
    timeout: float = 180,
) -> dict[str, Any]:
    """Return a dict that matches the JSON `schema`. No tools, no MCP, no saved session."""
    require_plan_login()
    args = [
        "-p",
        "--model", model,
        "--system-prompt", system,
        "--json-schema", json.dumps(schema),
        "--output-format", "json",
        "--tools", "",
        "--strict-mcp-config",
        "--disable-slash-commands",
        "--no-session-persistence",
        "--setting-sources", "",
    ]  # fmt: skip
    if effort:
        args += ["--effort", effort]
    done = _run(args, stdin=user, timeout=timeout)
    try:
        out = json.loads(done.stdout)
    except json.JSONDecodeError:
        raise ClaudeCLIError(f"claude exited {done.returncode}: {done.stderr[-500:]}") from None
    data = out.get("structured_output")
    if out.get("is_error") or not isinstance(data, dict):
        raise ClaudeCLIError(f"claude returned no structured output: {out.get('result')!r}")
    return data

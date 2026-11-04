"""Ask an LLM for structured output, with PII masking and a call log.

Providers: "anthropic" (Claude through the official SDK) and "fake" (offline and deterministic,
used by tests and smoke). Pick one with LLM_PROVIDER. Another provider is one more function with
the same signature as `_anthropic`.
"""

from __future__ import annotations

import json
import time
from collections.abc import Callable
from datetime import UTC, datetime

from pydantic import BaseModel

from common import config
from common.pii import mask

# Models that accept the server-side refusal fallback (fallbacks="default").
_FALLBACK_MODELS = {"claude-fable-5-1", "claude-opus-5-5", "claude-opus-5", "claude-sonnet-5-5"}


class LLMRefused(RuntimeError):
    pass


def provider_name() -> str:
    return "fake" if config.LLM_PROVIDER == "fake" else config.LLM_MODEL


def ask[T: BaseModel](schema: type[T], system: str, user: str, *, fake: Callable[[], T]) -> T:
    """Return `schema` filled in by the model. `fake` builds the offline answer."""
    user = mask(user)
    started = time.perf_counter()
    if config.LLM_PROVIDER == "fake":
        result = fake()
    elif config.LLM_PROVIDER == "anthropic":
        result = _anthropic(schema, system, user)
    else:
        raise RuntimeError(f"unknown LLM_PROVIDER {config.LLM_PROVIDER!r}")
    _log(system, user, result, time.perf_counter() - started)
    return result


def _anthropic[T: BaseModel](schema: type[T], system: str, user: str) -> T:
    import anthropic

    extra: dict = {}
    if config.LLM_MODEL in _FALLBACK_MODELS:
        # On a policy decline the API reruns the request on a suitable model in the same call.
        extra = {"betas": ["server-side-fallback-2026-07-01"], "fallbacks": "default"}
    response = anthropic.Anthropic().beta.messages.create(
        model=config.LLM_MODEL,
        max_tokens=16000,
        system=system,
        messages=[{"role": "user", "content": user}],
        output_config={
            "effort": config.LLM_EFFORT,
            "format": {"type": "json_schema", "schema": schema.model_json_schema()},
        },
        **extra,
    )
    if response.stop_reason == "refusal":
        raise LLMRefused(str(getattr(response, "stop_details", None)))
    text = next(block.text for block in response.content if block.type == "text")
    return schema.model_validate_json(text)


def _log(system: str, user: str, result: BaseModel, seconds: float) -> None:
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    row = {
        "at": datetime.now(UTC).isoformat(timespec="seconds"),
        "model": provider_name(),
        "seconds": round(seconds, 2),
        "system": system,
        "user": user,
        "output": result.model_dump(mode="json"),
    }
    with open(config.LOG_DIR / "llm_calls.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

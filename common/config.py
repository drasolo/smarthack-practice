"""Settings shared by api, ml, ui and evals. Everything comes from env vars or .env."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

DATA_DIR = Path(os.getenv("DATA_DIR") or Path.home() / "smarthack-data").expanduser()
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
LOG_DIR = DATA_DIR / "logs"
SAMPLE_DIR = ROOT / "data" / "sample"
MOCKS_DIR = ROOT / "contract" / "mocks"
RESULTS_DIR = ROOT / "evals" / "results"

# Emdash gives each task its own block of ports in EMDASH_PORT, so parallel worktrees don't
# collide. Outside Emdash the usual defaults apply.
_BASE = int(os.getenv("EMDASH_PORT") or 0)
API_PORT = int(os.getenv("API_PORT") or (_BASE or 8000))
UI_PORT = int(os.getenv("UI_PORT") or (_BASE + 1 if _BASE else 8501))
API_URL = os.getenv("API_URL") or f"http://127.0.0.1:{API_PORT}"

USE_MOCKS = os.getenv("USE_MOCKS", "").lower() in {"1", "true", "yes"}
TIMEZONE = os.getenv("TIMEZONE") or "Europe/Bucharest"

LLM_PROVIDER = os.getenv("LLM_PROVIDER") or (
    "anthropic" if os.getenv("ANTHROPIC_API_KEY") else "fake"
)
LLM_MODEL = os.getenv("LLM_MODEL") or "claude-opus-5-5"
LLM_EFFORT = os.getenv("LLM_EFFORT") or "low"
LLM_LANGUAGE = os.getenv("LLM_LANGUAGE") or "ro"

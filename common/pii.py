"""Mask personal data before any text leaves the laptop for an LLM."""

from __future__ import annotations

import re

# Order matters: IBANs contain long digit runs that the CNP pattern would otherwise eat.
PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("EMAIL", re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")),
    ("IBAN", re.compile(r"\bRO\d{2}[A-Z]{4}[A-Z0-9]{16}\b", re.IGNORECASE)),
    ("CNP", re.compile(r"\b[1-8]\d{12}\b")),
    ("PHONE", re.compile(r"(?<!\d)(?:\+40|0040|0)7\d{8}(?!\d)")),
]


def mask(text: str) -> str:
    for label, pattern in PATTERNS:
        text = pattern.sub(f"<{label}>", text)
    return text


def find(text: str) -> list[str]:
    """Labels of the personal data still present in `text` (used by evals)."""
    return [label for label, pattern in PATTERNS if pattern.search(text)]

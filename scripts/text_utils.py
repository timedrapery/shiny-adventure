#!/usr/bin/env python3
"""Shared text helpers for term-processing scripts."""

from __future__ import annotations

import unicodedata


def normalize_term(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    stripped = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    lowered = stripped.lower().replace(" ", "_").replace("-", "_")
    return "".join(ch for ch in lowered if ch.isalnum() or ch == "_")


def safe_text(value: str) -> str:
    return value.encode("ascii", "backslashreplace").decode("ascii")

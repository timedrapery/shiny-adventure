#!/usr/bin/env python3
"""Helpers for reading and writing term files across the terms tree."""

from __future__ import annotations

from pathlib import Path


def iter_term_files(terms_dir: Path) -> list[Path]:
    return sorted(path for path in terms_dir.rglob("*.json") if path.is_file())


def destination_for_record(terms_dir: Path, record: dict[str, object], normalized_term: str) -> Path:
    entry_type = record.get("entry_type")
    if entry_type in {"major", "minor"}:
        return terms_dir / str(entry_type) / f"{normalized_term}.json"
    return terms_dir / f"{normalized_term}.json"

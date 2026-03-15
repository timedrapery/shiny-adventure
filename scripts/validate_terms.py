#!/usr/bin/env python3
"""Validate term JSON files against the project schema."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("Missing dependency: jsonschema")
    print("Install it with: python -m pip install jsonschema")
    sys.exit(1)

try:
    from scripts.term_store import iter_term_files
except ModuleNotFoundError:
    from term_store import iter_term_files


REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schema" / "PALI_TERM_SCHEMA.json"
TERMS_DIR = REPO_ROOT / "terms"


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def collect_validation_failures(terms_dir: Path) -> tuple[list[str], list[str]]:
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    failures: list[str] = []
    warnings: list[str] = []
    normalized_index: dict[str, list[str]] = defaultdict(list)
    term_index: dict[str, list[str]] = defaultdict(list)
    preferred_translation_index: dict[str, list[str]] = defaultdict(list)

    term_files = iter_term_files(terms_dir)
    for term_file in term_files:
        try:
            data = load_json(term_file)
        except json.JSONDecodeError as exc:
            failures.append(f"{term_file}: invalid JSON: {exc}")
            continue

        errors = sorted(validator.iter_errors(data), key=lambda err: list(err.path))
        for error in errors:
            path = ".".join(str(part) for part in error.path) or "<root>"
            failures.append(f"{term_file}: {path}: {error.message}")

        if not isinstance(data, dict):
            continue

        normalized_term = data.get("normalized_term")
        if isinstance(normalized_term, str):
            normalized_index[normalized_term].append(term_file.name)
            if normalized_term != term_file.stem:
                failures.append(
                    f"{term_file}: normalized_term '{normalized_term}' does not match filename stem '{term_file.stem}'"
                )

        term = data.get("term")
        if isinstance(term, str):
            term_index[term].append(term_file.name)

        if data.get("entry_type") == "major":
            preferred = data.get("preferred_translation")
            if isinstance(preferred, str) and preferred.strip():
                preferred_translation_index[preferred.strip()].append(term_file.stem)

    for normalized_term, filenames in sorted(normalized_index.items()):
        if len(filenames) > 1:
            failures.append(
                f"normalized_term '{normalized_term}' is duplicated across files: {', '.join(sorted(filenames))}"
            )

    for term, filenames in sorted(term_index.items()):
        if len(filenames) > 1:
            failures.append(
                f"term '{term}' is duplicated across files: {', '.join(sorted(filenames))}"
            )

    for preferred_translation, stems in sorted(preferred_translation_index.items()):
        if len(stems) > 1:
            warnings.append(
                "major preferred_translation collision "
                f"'{preferred_translation}': {', '.join(sorted(stems))}"
            )

    return failures, warnings


def main() -> int:
    if not SCHEMA_PATH.exists():
        print(f"ERROR: Schema file not found: {SCHEMA_PATH}")
        return 1

    if not TERMS_DIR.exists():
        print(f"ERROR: Terms directory not found: {TERMS_DIR}")
        return 1

    term_files = iter_term_files(TERMS_DIR)
    if not term_files:
        print("WARNING: No term files found in terms/")
        return 0

    failures, warnings = collect_validation_failures(TERMS_DIR)

    if failures:
        print("Schema validation failed:\n")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Validated {len(term_files)} term file(s) successfully.")
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

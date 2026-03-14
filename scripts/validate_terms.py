#!/usr/bin/env python3
"""Validate term JSON files against the project schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("Missing dependency: jsonschema")
    print("Install it with: python -m pip install jsonschema")
    sys.exit(1)


REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schema" / "PALI_TERM_SCHEMA.json"
TERMS_DIR = REPO_ROOT / "terms"


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    if not SCHEMA_PATH.exists():
        print(f"ERROR: Schema file not found: {SCHEMA_PATH}")
        return 1

    if not TERMS_DIR.exists():
        print(f"ERROR: Terms directory not found: {TERMS_DIR}")
        return 1

    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    failures: list[str] = []

    term_files = sorted(TERMS_DIR.glob("*.json"))
    if not term_files:
        print("WARNING: No term files found in terms/")
        return 0

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

    if failures:
        print("Schema validation failed:\n")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Validated {len(term_files)} term file(s) successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

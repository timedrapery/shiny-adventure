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
    from scripts.text_utils import normalize_term
except ModuleNotFoundError:
    from term_store import iter_term_files
    from text_utils import normalize_term


REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schema" / "PALI_TERM_SCHEMA.json"
TERMS_DIR = REPO_ROOT / "terms"


def stem_key(value: str) -> str:
    return value.replace("-", "_").casefold()


def related_term_keys(data: dict[str, object]) -> set[str]:
    related = data.get("related_terms")
    if not isinstance(related, list):
        return set()
    return {normalize_term(item) for item in related if isinstance(item, str)}


def has_explicit_preferred_disambiguation(
    grouped: list[tuple[str, dict[str, object]]],
) -> bool:
    if len(grouped) < 2:
        return False

    keys = {stem_key(stem): related_term_keys(data) for stem, data in grouped}
    stems = set(keys)
    return all(any(other in keys[stem] for other in stems - {stem}) for stem in stems)


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
    canonical_term_index: dict[str, list[tuple[str, str]]] = defaultdict(list)
    preferred_translation_index: dict[str, list[tuple[str, dict[str, object]]]] = defaultdict(list)

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
            canonical_term_index[normalize_term(term)].append((term, term_file.name))

        if data.get("entry_type") == "major":
            preferred = data.get("preferred_translation")
            if isinstance(preferred, str) and preferred.strip():
                preferred_translation_index[preferred.strip()].append((term_file.stem, data))

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

    for canonical_term, term_entries in sorted(canonical_term_index.items()):
        distinct_terms = sorted({term for term, _filename in term_entries})
        if len(distinct_terms) < 2:
            continue
        filenames = sorted({filename for _term, filename in term_entries})
        failures.append(
            f"canonical term '{canonical_term}' is duplicated across files with variant spellings: "
            f"{', '.join(filenames)}"
        )

    for preferred_translation, grouped in sorted(preferred_translation_index.items()):
        if len(grouped) > 1 and not has_explicit_preferred_disambiguation(grouped):
            warnings.append(
                "major preferred_translation collision "
                f"'{preferred_translation}': {', '.join(sorted(stem for stem, _data in grouped))}"
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

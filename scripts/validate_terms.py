#!/usr/bin/env python3
"""Validate term JSON files against the project schema."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
import re

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("Missing dependency: jsonschema")
    print("Install it with: python -m pip install jsonschema")
    sys.exit(1)

try:
    from scripts.repair_guidance import (
        RepairDiagnostic,
        diagnostics_as_json,
        field_examples,
        field_snippet,
        print_diagnostics,
        RELATIONSHIP_EXAMPLES,
    )
    from scripts.term_store import iter_term_files
    from scripts.text_utils import normalize_term
except ModuleNotFoundError:
    from repair_guidance import (
        RepairDiagnostic,
        diagnostics_as_json,
        field_examples,
        field_snippet,
        print_diagnostics,
        RELATIONSHIP_EXAMPLES,
    )
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


def repo_relpath(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def top_level_field(path: str) -> str:
    if path in {"", "<root>"}:
        return path
    return path.split(".", 1)[0].split("[", 1)[0]


def compact_message(diagnostic: RepairDiagnostic) -> str:
    if diagnostic.file:
        return f"{diagnostic.file}: {diagnostic.summary}"
    return diagnostic.summary


def required_field_from_message(message: str) -> str | None:
    match = re.search(r"'([^']+)' is a required property", message)
    if not match:
        return None
    return match.group(1)


def unexpected_field_from_message(message: str) -> str | None:
    match = re.search(r"'([^']+)' was unexpected", message)
    if not match:
        return None
    return match.group(1)


def schema_error_diagnostic(term_file: Path, error: object) -> RepairDiagnostic:
    path = ".".join(str(part) for part in error.path) or "<root>"
    relpath = repo_relpath(term_file)
    root_field = top_level_field(path)
    examples = field_examples(root_field if root_field != "<root>" else "notes")

    if error.validator == "required":
        missing_field = required_field_from_message(error.message)
        if missing_field is None:
            missing_field = "<unknown>"
        qualified_field = (
            missing_field if path == "<root>" else f"{path}.{missing_field}"
        )
        snippet = field_snippet(top_level_field(qualified_field))
        fix = f"Add a non-empty `{qualified_field}` value."
        if snippet:
            fix += f" Minimal compliant shape: {snippet}"
        return RepairDiagnostic(
            severity="error",
            category="Schema",
            code="schema_required_field",
            rule="Required schema field must be present",
            file=relpath,
            summary=f"Missing `{qualified_field}`",
            why="Missing required structure means validators, drift checks, and generated surfaces cannot rely on the record shape.",
            fix=fix,
            examples=examples,
        )

    if error.validator == "type":
        expected_type = error.schema.get("type", "the schema-defined type")
        snippet = field_snippet(root_field)
        fix = f"Replace `{path}` with a `{expected_type}` value that matches the schema."
        if snippet:
            fix += f" Minimal compliant shape: {snippet}"
        return RepairDiagnostic(
            severity="error",
            category="Schema",
            code="schema_type_mismatch",
            rule="Schema field must use the expected type",
            file=relpath,
            summary=f"`{path}` has the wrong type; expected `{expected_type}`",
            why="Type mismatches make the record unreadable to automation even when the field name is present.",
            fix=fix,
            examples=examples,
        )

    if error.validator == "enum":
        allowed = ", ".join(repr(item) for item in error.validator_value)
        return RepairDiagnostic(
            severity="error",
            category="Schema",
            code="schema_invalid_enum",
            rule="Schema enum fields must use a supported value",
            file=relpath,
            summary=f"`{path}` uses an unsupported value",
            why="Unsupported enum values break status, part-of-speech, and policy vocabularies that the repo treats as closed sets.",
            fix=f"Replace `{path}` with one of the allowed values: {allowed}.",
            examples=examples,
        )

    if error.validator == "additionalProperties":
        unexpected = unexpected_field_from_message(error.message) or "unexpected field"
        return RepairDiagnostic(
            severity="error",
            category="Schema",
            code="schema_unexpected_field",
            rule="Live term records cannot carry undeclared schema fields",
            file=relpath,
            summary=f"Unexpected field `{unexpected}` is not allowed by the schema",
            why="Undeclared fields create private data shapes that the rest of the repository does not validate or govern.",
            fix=f"Remove `{unexpected}` or move its content into an existing governed field such as `notes`, `context_rules`, or `translation_policy` when appropriate.",
            examples=examples,
        )

    if error.validator == "pattern":
        return RepairDiagnostic(
            severity="error",
            category="Schema",
            code="schema_pattern_mismatch",
            rule="Schema pattern fields must use the repository slug format",
            file=relpath,
            summary=f"`{path}` does not match the required schema pattern",
            why="Pattern mismatches usually break filename alignment, indexing, and deterministic lookup.",
            fix=f"Rewrite `{path}` to match the repository slug format required by the schema.",
            examples=examples,
        )

    if error.validator == "minLength":
        snippet = field_snippet(root_field)
        fix = f"Populate `{path}` with a non-empty string."
        if snippet:
            fix += f" Minimal compliant shape: {snippet}"
        return RepairDiagnostic(
            severity="error",
            category="Schema",
            code="schema_empty_string",
            rule="Schema string fields must not be empty",
            file=relpath,
            summary=f"`{path}` is present but empty",
            why="Empty strings look structurally present while still failing to encode any governed policy.",
            fix=fix,
            examples=examples,
        )

    return RepairDiagnostic(
        severity="error",
        category="Schema",
        code=f"schema_{error.validator}",
        rule="Term records must satisfy the live JSON schema",
        file=relpath,
        summary=f"`{path}` violates the schema: {error.message}",
        why="The schema is the repository's minimum structural contract for safe automation.",
        fix=f"Repair `{path}` so it satisfies the schema rule reported above, then rerun `python scripts/validate_terms.py --strict`.",
        examples=examples,
    )


def invalid_json_diagnostic(term_file: Path, exc: json.JSONDecodeError) -> RepairDiagnostic:
    relpath = repo_relpath(term_file)
    return RepairDiagnostic(
        severity="error",
        category="Schema",
        code="invalid_json",
        rule="Term records must be valid JSON",
        file=relpath,
        summary=f"invalid JSON near line {exc.lineno}, column {exc.colno}",
        why="If the file cannot be parsed, no other governance check can trust its content.",
        fix="Repair the JSON syntax at the reported location, then rerun schema validation before changing policy fields.",
        examples=("terms/major/dukkha.json",),
    )


def normalized_term_mismatch_diagnostic(
    term_file: Path, normalized_term: str
) -> RepairDiagnostic:
    relpath = repo_relpath(term_file)
    return RepairDiagnostic(
        severity="error",
        category="Schema",
        code="normalized_term_filename_mismatch",
        rule="`normalized_term` must match the filename stem",
        file=relpath,
        summary=(
            f"`normalized_term` `{normalized_term}` does not match filename stem "
            f"`{term_file.stem}`"
        ),
        why="Filename and normalized slug mismatches break deterministic lookup, navigation generation, and cross-script indexing.",
        fix=f"Either rename the file to `{normalized_term}.json` or change `normalized_term` to `{term_file.stem}` so both slugs match exactly.",
        examples=("terms/major/sati.json",),
    )


def duplicate_normalized_term_diagnostic(
    normalized_term: str, filenames: list[str]
) -> RepairDiagnostic:
    return RepairDiagnostic(
        severity="error",
        category="Schema",
        code="duplicate_normalized_term",
        rule="`normalized_term` values must be unique across the repository",
        summary=f"`normalized_term` `{normalized_term}` is duplicated across files: {', '.join(sorted(filenames))}",
        why="A duplicated slug makes file routing and machine lookup ambiguous.",
        fix="Keep one authoritative slug for the shared headword. Rename or merge the conflicting records so each live file has a unique `normalized_term`.",
        examples=("terms/major/sati.json",),
    )


def duplicate_term_diagnostic(term: str, filenames: list[str]) -> RepairDiagnostic:
    return RepairDiagnostic(
        severity="error",
        category="Schema",
        code="duplicate_term",
        rule="Displayed headwords must not be duplicated across live files",
        summary=f"term '{term}' is duplicated across files: {', '.join(sorted(filenames))}",
        why="Duplicate live headwords create competing policy records for the same displayed term.",
        fix="Merge the records or split them into genuinely distinct headwords with distinct `term` values and filenames.",
        examples=RELATIONSHIP_EXAMPLES,
    )


def canonical_duplicate_term_diagnostic(
    canonical_term: str, filenames: list[str]
) -> RepairDiagnostic:
    return RepairDiagnostic(
        severity="error",
        category="Schema",
        code="duplicate_canonical_term",
        rule="One canonical Pāli headword cannot appear in multiple live spellings",
        summary=(
            f"canonical term '{canonical_term}' is duplicated across files with variant "
            f"spellings: {', '.join(sorted(filenames))}"
        ),
        why="Variant live spellings split governance across files and invite silent drift in downstream use.",
        fix="Choose one canonical displayed spelling for the live entry, merge the duplicates, and keep alternates in notes or controlled alternates rather than in separate files.",
        examples=("terms/major/sankhara.json",),
    )


def preferred_collision_diagnostic(
    preferred_translation: str, stems: list[str]
) -> RepairDiagnostic:
    return RepairDiagnostic(
        severity="warning",
        category="Schema",
        code="major_preferred_translation_collision",
        rule="Shared major preferred translations need explicit disambiguation",
        summary=(
            f"major preferred_translation collision '{preferred_translation}': "
            f"major entries share `{preferred_translation}` without explicit disambiguation: "
            f"{', '.join(sorted(stems))}"
        ),
        why="If multiple major lemmas share a default rendering without family-level contrast, translators and drift checks lose the governing distinction.",
        fix="Either differentiate the preferred renderings or link the lemmas to each other in `related_terms` on both sides and explain the contrast in notes/context_rules.",
        examples=RELATIONSHIP_EXAMPLES,
    )


def collect_validation_diagnostics(
    terms_dir: Path,
) -> tuple[list[RepairDiagnostic], list[RepairDiagnostic], int]:
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    failures: list[RepairDiagnostic] = []
    warnings: list[RepairDiagnostic] = []
    normalized_index: dict[str, list[str]] = defaultdict(list)
    term_index: dict[str, list[str]] = defaultdict(list)
    canonical_term_index: dict[str, list[tuple[str, str]]] = defaultdict(list)
    preferred_translation_index: dict[str, list[tuple[str, dict[str, object]]]] = defaultdict(list)

    term_files = iter_term_files(terms_dir)
    for term_file in term_files:
        try:
            data = load_json(term_file)
        except json.JSONDecodeError as exc:
            failures.append(invalid_json_diagnostic(term_file, exc))
            continue

        errors = sorted(validator.iter_errors(data), key=lambda err: list(err.path))
        for error in errors:
            failures.append(schema_error_diagnostic(term_file, error))

        if not isinstance(data, dict):
            continue

        normalized_term = data.get("normalized_term")
        if isinstance(normalized_term, str):
            normalized_index[normalized_term].append(term_file.name)
            if normalized_term != term_file.stem:
                failures.append(normalized_term_mismatch_diagnostic(term_file, normalized_term))

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
                duplicate_normalized_term_diagnostic(normalized_term, filenames)
            )

    for term, filenames in sorted(term_index.items()):
        if len(filenames) > 1:
            failures.append(duplicate_term_diagnostic(term, filenames))

    for canonical_term, term_entries in sorted(canonical_term_index.items()):
        distinct_terms = sorted({term for term, _filename in term_entries})
        if len(distinct_terms) < 2:
            continue
        filenames = sorted({filename for _term, filename in term_entries})
        failures.append(canonical_duplicate_term_diagnostic(canonical_term, filenames))

    for preferred_translation, grouped in sorted(preferred_translation_index.items()):
        if len(grouped) > 1 and not has_explicit_preferred_disambiguation(grouped):
            warnings.append(
                preferred_collision_diagnostic(
                    preferred_translation,
                    [stem for stem, _data in grouped],
                )
            )

    return failures, warnings, len(term_files)


def collect_validation_failures(terms_dir: Path) -> tuple[list[str], list[str]]:
    failures, warnings, _count = collect_validation_diagnostics(terms_dir)
    return (
        [compact_message(diagnostic) for diagnostic in failures],
        [compact_message(diagnostic) for diagnostic in warnings],
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit a JSON report with actionable repair guidance.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on warnings as well as errors.",
    )
    if argv is None and __name__ != "__main__":
        argv = []
    args = parser.parse_args(argv)

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

    failures, warnings, record_count = collect_validation_diagnostics(TERMS_DIR)

    if args.json:
        payload = {
            "term_files": record_count,
            "errors": diagnostics_as_json(failures),
            "warnings": diagnostics_as_json(warnings),
        }
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        if failures:
            print("Schema validation failed:\n")
            print_diagnostics("Errors", failures)
        if warnings:
            print("Schema validation warnings:\n")
            print_diagnostics("Warnings", warnings)
        if not failures and not warnings:
            print(f"Validated {record_count} term file(s) successfully.")

    if failures:
        return 1
    if warnings and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

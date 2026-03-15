#!/usr/bin/env python3
"""Detect translation drift across term entries."""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path

try:
    from scripts.text_utils import normalize_term, safe_text
    from scripts.term_store import iter_term_files
    from scripts.validate_terms import collect_validation_failures
except ModuleNotFoundError:
    from text_utils import normalize_term, safe_text
    from term_store import iter_term_files
    from validate_terms import collect_validation_failures


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
RULE_BEARING_FIELDS = (
    "notes",
    "context_rules",
    "related_terms",
    "example_phrases",
    "alternative_translations",
    "discouraged_translations",
    "sutta_references",
    "tags",
    "authority_basis",
    "translation_policy",
)
RULE_POLICY_FIELDS = (
    "default_scope",
    "when_not_to_apply",
    "compound_inheritance",
    "drift_risk",
)
CONTEXT_SENSITIVE_TAGS = {"context-sensitive"}
RULE_LANGUAGE_MARKERS = (
    "default",
    "context",
    "render",
    "translation",
    "untranslated",
    "compound",
    "drift",
    "avoid",
    "prefer",
)


@dataclass(frozen=True)
class TermRecord:
    path: Path
    stem: str
    data: dict[str, object]


@dataclass(frozen=True)
class Finding:
    severity: str
    category: str
    code: str
    message: str
    path: str | None = None


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_term_records(terms_dir: Path = TERMS_DIR) -> list[TermRecord]:
    records: list[TermRecord] = []
    for path in iter_term_files(terms_dir):
        data = load_json(path)
        if isinstance(data, dict):
            records.append(TermRecord(path=path, stem=path.stem, data=data))
    return records


def canonical_key(value: str) -> str:
    return normalize_term(value)


def normalized_stem_key(value: str) -> str:
    return value.casefold().replace("-", "").replace("_", "")


def english_key(value: str) -> str:
    return " ".join(value.casefold().split())


def is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def is_non_empty_list(value: object) -> bool:
    return isinstance(value, list) and len(value) > 0


def has_rule_language(text: str) -> bool:
    lowered = text.casefold()
    return any(marker in lowered for marker in RULE_LANGUAGE_MARKERS)


def related_term_keys(record: TermRecord) -> set[str]:
    related = record.data.get("related_terms")
    if not isinstance(related, list):
        return set()
    return {canonical_key(item) for item in related if isinstance(item, str)}


def add_finding(
    findings: list[Finding],
    severity: str,
    category: str,
    code: str,
    message: str,
    *,
    path: Path | None = None,
) -> None:
    findings.append(
        Finding(
            severity=severity,
            category=category,
            code=code,
            message=message,
            path=str(path.relative_to(REPO_ROOT)) if path is not None else None,
        )
    )


def check_schema(records: list[TermRecord], findings: list[Finding]) -> None:
    del records
    for failure in collect_validation_failures(TERMS_DIR):
        add_finding(findings, "error", "Schema", "schema_violation", failure)


def check_conflicting_preferred_translations(
    records: list[TermRecord], findings: list[Finding]
) -> None:
    by_lemma: dict[str, list[TermRecord]] = defaultdict(list)
    for record in records:
        term = record.data.get("term")
        if isinstance(term, str):
            by_lemma[canonical_key(term)].append(record)

    for lemma_key, grouped in sorted(by_lemma.items()):
        preferreds = {
            english_key(value): value
            for value in (
                record.data.get("preferred_translation")
                for record in grouped
            )
            if isinstance(value, str)
        }
        if len(preferreds) > 1:
            message = (
                f"lemma '{lemma_key}' has conflicting preferred translations: "
                f"{', '.join(sorted(preferreds.values()))}"
            )
            for record in grouped:
                add_finding(
                    findings,
                    "warning",
                    "Preferred Translation",
                    "conflicting_preferred_translation",
                    message,
                    path=record.path,
                )


def check_duplicate_preferred_renderings(
    records: list[TermRecord], findings: list[Finding]
) -> None:
    by_rendering: dict[str, list[TermRecord]] = defaultdict(list)
    for record in records:
        if record.data.get("entry_type") != "major":
            continue
        preferred = record.data.get("preferred_translation")
        if isinstance(preferred, str):
            by_rendering[english_key(preferred)].append(record)

    for rendering_key, grouped in sorted(by_rendering.items()):
        if len(grouped) < 2:
            continue

        canonical_terms = {
            canonical_key(term)
            for term in (
                record.data.get("term")
                for record in grouped
            )
            if isinstance(term, str)
        }
        if len(canonical_terms) < 2:
            continue

        preferred = grouped[0].data.get("preferred_translation")
        if isinstance(preferred, str) and canonical_key(preferred) in canonical_terms:
            continue

        stems = {record.stem for record in grouped}
        keys = {record.stem: related_term_keys(record) for record in grouped}
        all_cross_related = True
        for stem in stems:
            others = stems - {stem}
            if not any(other in keys[stem] for other in others):
                all_cross_related = False
                break
        if all_cross_related:
            continue

        message = (
            f"preferred rendering '{preferred}' is shared by multiple major lemmas without explicit disambiguation: "
            f"{', '.join(sorted(record.stem for record in grouped))}"
        )
        for record in grouped:
            add_finding(
                findings,
                "warning",
                "Preferred Translation",
                "duplicate_preferred_rendering",
                message,
                path=record.path,
            )


def check_rule_bearing_fields(records: list[TermRecord], findings: list[Finding]) -> None:
    for record in records:
        data = record.data
        if data.get("entry_type") != "major":
            continue

        for field in RULE_BEARING_FIELDS:
            value = data.get(field)
            if field == "translation_policy":
                if not isinstance(value, dict):
                    add_finding(
                        findings,
                        "error",
                        "Rule Coverage",
                        "missing_rule_field",
                        f"major entry is missing required rule-bearing field '{field}'",
                        path=record.path,
                    )
                    continue
                for policy_field in RULE_POLICY_FIELDS:
                    policy_value = value.get(policy_field)
                    if policy_field == "compound_inheritance":
                        if policy_value not in {"inherit", "case-by-case", "blocked"}:
                            add_finding(
                                findings,
                                "error",
                                "Rule Coverage",
                                "missing_translation_policy_field",
                                f"major entry translation_policy is missing required field '{policy_field}'",
                                path=record.path,
                            )
                    elif not is_non_empty_string(policy_value):
                        add_finding(
                            findings,
                            "error",
                            "Rule Coverage",
                            "missing_translation_policy_field",
                            f"major entry translation_policy is missing required field '{policy_field}'",
                            path=record.path,
                        )
                continue

            if field == "notes":
                if not is_non_empty_string(value):
                    add_finding(
                        findings,
                        "error",
                        "Rule Coverage",
                        "missing_rule_field",
                        f"major entry is missing required rule-bearing field '{field}'",
                        path=record.path,
                    )
                continue

            if not is_non_empty_list(value):
                add_finding(
                    findings,
                    "error",
                    "Rule Coverage",
                    "missing_rule_field",
                    f"major entry is missing required rule-bearing field '{field}'",
                    path=record.path,
                )


def check_alternate_consistency(records: list[TermRecord], findings: list[Finding]) -> None:
    for record in records:
        data = record.data
        preferred = data.get("preferred_translation")
        alternatives = data.get("alternative_translations")
        discouraged = data.get("discouraged_translations")
        if not isinstance(preferred, str):
            continue

        alt_map: dict[str, str] = {}
        disc_map: dict[str, str] = {}
        if isinstance(alternatives, list):
            alt_map = {
                english_key(value): value for value in alternatives if isinstance(value, str)
            }
        if isinstance(discouraged, list):
            disc_map = {
                english_key(value): value for value in discouraged if isinstance(value, str)
            }

        preferred_key = english_key(preferred)
        if preferred_key in alt_map:
            add_finding(
                findings,
                "error",
                "Alternates",
                "preferred_listed_as_alternate",
                "preferred_translation is duplicated in alternative_translations",
                path=record.path,
            )
        if preferred_key in disc_map:
            add_finding(
                findings,
                "error",
                "Alternates",
                "preferred_listed_as_discouraged",
                "preferred_translation is also listed in discouraged_translations",
                path=record.path,
            )

        overlap = sorted(set(alt_map) & set(disc_map))
        for key in overlap:
            add_finding(
                findings,
                "warning",
                "Alternates",
                "alternate_discouraged_overlap",
                f"rendering '{alt_map[key]}' appears in both alternative_translations and discouraged_translations",
                path=record.path,
            )

        context_rules = data.get("context_rules")
        if not isinstance(context_rules, list):
            continue

        for rule in context_rules:
            if not isinstance(rule, dict):
                continue
            rendering = rule.get("rendering")
            if not isinstance(rendering, str):
                continue
            rendering_key = english_key(rendering)
            if rendering_key in disc_map:
                add_finding(
                    findings,
                    "warning",
                    "Alternates",
                    "context_rule_uses_discouraged_rendering",
                    f"context rule uses discouraged rendering '{rendering}'",
                    path=record.path,
                )


def check_context_sensitive_notes(
    records: list[TermRecord], findings: list[Finding]
) -> None:
    for record in records:
        tags = record.data.get("tags")
        if not isinstance(tags, list) or not CONTEXT_SENSITIVE_TAGS.intersection(tags):
            continue

        context_rules = record.data.get("context_rules")
        if not isinstance(context_rules, list) or len(context_rules) < 2:
            add_finding(
                findings,
                "error",
                "Context Rules",
                "context_sensitive_missing_rules",
                "context-sensitive entry must include at least two context_rules",
                path=record.path,
            )
            continue

        for index, rule in enumerate(context_rules, start=1):
            if not isinstance(rule, dict) or not is_non_empty_string(rule.get("notes")):
                add_finding(
                    findings,
                    "error",
                    "Context Rules",
                    "context_sensitive_missing_note",
                    f"context-sensitive entry is missing notes on context_rules[{index}]",
                    path=record.path,
                )

        policy = record.data.get("translation_policy")
        if not isinstance(policy, dict) or not is_non_empty_string(policy.get("when_not_to_apply")):
            add_finding(
                findings,
                "error",
                "Context Rules",
                "context_sensitive_missing_policy",
                "context-sensitive entry must explain when_not_to_apply in translation_policy",
                path=record.path,
            )


def check_headword_normalization(records: list[TermRecord], findings: list[Finding]) -> None:
    by_canonical_term: dict[str, list[TermRecord]] = defaultdict(list)

    for record in records:
        term = record.data.get("term")
        normalized_term = record.data.get("normalized_term")
        if not isinstance(term, str) or not isinstance(normalized_term, str):
            continue

        by_canonical_term[canonical_key(term)].append(record)

        if unicodedata.normalize("NFC", term) != term:
            add_finding(
                findings,
                "warning",
                "Headword Normalization",
                "non_nfc_term",
                "term is not NFC-normalized",
                path=record.path,
            )

        if canonical_key(term).replace("_", "") != normalized_stem_key(normalized_term):
            add_finding(
                findings,
                "warning",
                "Headword Normalization",
                "normalized_term_mismatch",
                f"normalized_term '{safe_text(normalized_term)}' does not match the canonical normalization of term '{safe_text(term)}'",
                path=record.path,
            )

    for canonical_term, grouped in sorted(by_canonical_term.items()):
        display_terms = sorted(
            {
                term
                for term in (
                    record.data.get("term")
                    for record in grouped
                )
                if isinstance(term, str)
            }
        )
        if len(display_terms) > 1:
            message = (
                f"canonical headword '{canonical_term}' appears with inconsistent displayed spelling/diacritics: "
                f"{', '.join(safe_text(term) for term in display_terms)}"
            )
            for record in grouped:
                add_finding(
                    findings,
                    "warning",
                    "Headword Normalization",
                    "inconsistent_term_spelling",
                    message,
                    path=record.path,
                )


def check_major_entry_rule_strength(records: list[TermRecord], findings: list[Finding]) -> None:
    for record in records:
        data = record.data
        if data.get("entry_type") != "major":
            continue

        notes = data.get("notes")
        context_rules = data.get("context_rules")
        translation_policy = data.get("translation_policy")
        authority_basis = data.get("authority_basis")

        weak_notes = not is_non_empty_string(notes) or len(notes.strip()) < 120 or not has_rule_language(notes)
        weak_context = not isinstance(context_rules, list) or len(context_rules) < 2
        weak_policy = not isinstance(translation_policy, dict) or not is_non_empty_string(
            translation_policy.get("drift_risk")
        )
        weak_authority = not isinstance(authority_basis, list) or len(authority_basis) == 0

        if weak_notes and weak_context and weak_policy and weak_authority:
            add_finding(
                findings,
                "warning",
                "Rule Strength",
                "major_entry_too_definitional",
                "major entry looks definitional rather than rule-bearing; strengthen notes, context_rules, authority_basis, or translation_policy",
                path=record.path,
            )


def collect_findings(terms_dir: Path = TERMS_DIR) -> tuple[list[Finding], int]:
    if not terms_dir.exists():
        return (
            [
                Finding(
                    severity="error",
                    category="Setup",
                    code="missing_terms_dir",
                    message=f"terms directory not found: {terms_dir}",
                )
            ],
            0,
        )

    records = load_term_records(terms_dir)
    findings: list[Finding] = []

    check_schema(records, findings)
    check_conflicting_preferred_translations(records, findings)
    check_duplicate_preferred_renderings(records, findings)
    check_rule_bearing_fields(records, findings)
    check_alternate_consistency(records, findings)
    check_context_sensitive_notes(records, findings)
    check_headword_normalization(records, findings)
    check_major_entry_rule_strength(records, findings)

    findings.sort(key=lambda item: (item.severity, item.category, item.path or "", item.code, item.message))
    return findings, len(records)


def findings_by_severity(findings: list[Finding]) -> tuple[list[Finding], list[Finding]]:
    errors = [finding for finding in findings if finding.severity == "error"]
    warnings = [finding for finding in findings if finding.severity == "warning"]
    return errors, warnings


def print_group(title: str, findings: list[Finding]) -> None:
    if not findings:
        return
    print(f"{title}:")
    for finding in findings:
        location = f"{finding.path}: " if finding.path else ""
        print(f"- [{finding.code}] {location}{safe_text(finding.message)}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit a JSON report instead of human-readable text.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on warnings as well as errors.",
    )
    args = parser.parse_args()

    findings, record_count = collect_findings()
    errors, warnings = findings_by_severity(findings)

    if args.json:
        report = {
            "term_files": record_count,
            "errors": [asdict(finding) for finding in errors],
            "warnings": [asdict(finding) for finding in warnings],
        }
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        if errors:
            print("Translation drift check failed:\n")
            print_group("Errors", errors)
        if warnings:
            print("Translation drift warnings:\n")
            print_group("Warnings", warnings)
        if not errors and not warnings:
            print(f"Translation drift check passed for {record_count} term file(s).")

    if errors:
        return 1
    if warnings and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Detect translation drift across term entries."""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

try:
    from scripts.repair_guidance import (
        RepairDiagnostic,
        diagnostics_as_json,
        field_examples,
        field_snippet,
        print_diagnostics,
        CLUSTER_DOC_EXAMPLES,
        MAJOR_POLICY_EXAMPLES,
        RELATIONSHIP_EXAMPLES,
        STATUS_EXAMPLES,
    )
    from scripts.text_utils import normalize_term, safe_text
    from scripts.term_store import iter_term_files
    from scripts.validate_terms import collect_validation_failures
except ModuleNotFoundError:
    from repair_guidance import (
        RepairDiagnostic,
        diagnostics_as_json,
        field_examples,
        field_snippet,
        print_diagnostics,
        CLUSTER_DOC_EXAMPLES,
        MAJOR_POLICY_EXAMPLES,
        RELATIONSHIP_EXAMPLES,
        STATUS_EXAMPLES,
    )
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
    relpath = None
    if path is not None:
        try:
            relpath = path.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            relpath = path.as_posix()
    findings.append(
        Finding(
            severity=severity,
            category=category,
            code=code,
            message=message,
            path=relpath,
        )
    )


def check_schema(
    terms_dir: Path, records: list[TermRecord], findings: list[Finding]
) -> None:
    del records
    failures, _warnings = collect_validation_failures(terms_dir)
    for failure in failures:
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
                    "error",
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
                "error",
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
                    "error",
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

        distinct_renderings = {
            english_key(rule.get("rendering"))
            for rule in context_rules
            if isinstance(rule, dict) and is_non_empty_string(rule.get("rendering"))
        }
        if len(distinct_renderings) < 2:
            add_finding(
                findings,
                "error",
                "Context Rules",
                "context_sensitive_indistinct_renderings",
                "context-sensitive entry must use at least two distinct renderings across context_rules",
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


def check_default_rendering_coverage(
    records: list[TermRecord], findings: list[Finding]
) -> None:
    for record in records:
        data = record.data
        if data.get("entry_type") != "major":
            continue

        preferred = data.get("preferred_translation")
        context_rules = data.get("context_rules")
        if not is_non_empty_string(preferred) or not isinstance(context_rules, list):
            continue

        preferred_key = english_key(preferred)
        renderings = {
            english_key(rule.get("rendering"))
            for rule in context_rules
            if isinstance(rule, dict) and is_non_empty_string(rule.get("rendering"))
        }
        if preferred_key not in renderings:
            add_finding(
                findings,
                "error",
                "Context Rules",
                "preferred_not_covered_by_context_rules",
                "major entry context_rules do not include the preferred_translation as an explicit rendering",
                path=record.path,
            )


def check_headword_normalization(records: list[TermRecord], findings: list[Finding]) -> None:
    by_canonical_term: dict[str, list[TermRecord]] = defaultdict(list)

    for record in records:
        term = record.data.get("term")
        normalized_term = record.data.get("normalized_term")
        part_of_speech = record.data.get("part_of_speech")
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

        if (
            part_of_speech not in {"compound", "phrase", "expression"}
            and canonical_key(term).replace("_", "") != normalized_stem_key(normalized_term)
        ):
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

    check_schema(terms_dir, records, findings)
    check_conflicting_preferred_translations(records, findings)
    check_duplicate_preferred_renderings(records, findings)
    check_rule_bearing_fields(records, findings)
    check_alternate_consistency(records, findings)
    check_context_sensitive_notes(records, findings)
    check_default_rendering_coverage(records, findings)
    check_headword_normalization(records, findings)
    check_major_entry_rule_strength(records, findings)

    findings.sort(key=lambda item: (item.severity, item.category, item.path or "", item.code, item.message))
    return findings, len(records)


def findings_by_severity(findings: list[Finding]) -> tuple[list[Finding], list[Finding]]:
    errors = [finding for finding in findings if finding.severity == "error"]
    warnings = [finding for finding in findings if finding.severity == "warning"]
    return errors, warnings


def finding_to_diagnostic(finding: Finding) -> RepairDiagnostic:
    file = finding.path

    if finding.code == "schema_violation":
        return RepairDiagnostic(
            severity=finding.severity,
            category=finding.category,
            code=finding.code,
            file=file,
            rule="Drift checking requires schema-clean term data",
            summary=finding.message,
            why="A schema-broken record cannot be trusted for any higher-level drift analysis.",
            fix="Fix the schema error first with `python scripts/validate_terms.py --strict`, then rerun the drift check.",
            examples=MAJOR_POLICY_EXAMPLES,
        )

    if finding.code == "conflicting_preferred_translation":
        return RepairDiagnostic(
            severity=finding.severity,
            category=finding.category,
            code=finding.code,
            file=file,
            rule="One canonical lemma cannot carry multiple preferred translations",
            summary=finding.message,
            why="Conflicting defaults for the same lemma leave translators and automation without a single house standard.",
            fix="Review all records for this lemma together in the same pass. Preserve the existing stable policy unless a governed family review intentionally changes it, and align `preferred_translation`, `context_rules`, `discouraged_translations`, and `related_terms` together.",
            examples=("terms/major/sankhara.json", "terms/major/dukkha.json"),
        )

    if finding.code == "duplicate_preferred_rendering":
        return RepairDiagnostic(
            severity=finding.severity,
            category=finding.category,
            code=finding.code,
            file=file,
            rule="Distinct major lemmas need explicit disambiguation before sharing a default rendering",
            summary=finding.message,
            why="Shared defaults without documented contrast invite silent substitution between related terms.",
            fix="Either differentiate the preferred renderings or make the shared rendering explicit by linking the lemmas to each other in `related_terms` on both sides and explaining the contrast in `notes` or `context_rules`.",
            examples=RELATIONSHIP_EXAMPLES,
        )

    if finding.code in {"missing_rule_field", "missing_translation_policy_field"}:
        field = finding.message.rsplit("'", 2)[1] if "'" in finding.message else "policy field"
        snippet = field_snippet(field)
        fix = f"Add a non-empty `{field}` value."
        if snippet:
            fix += f" Minimal compliant shape: {snippet}"
        return RepairDiagnostic(
            severity=finding.severity,
            category=finding.category,
            code=finding.code,
            file=file,
            rule="Major entries must keep the full rule-bearing surface intact",
            summary=finding.message,
            why="If a major entry loses a governing field, the record stops acting as enforceable policy and falls back toward glossary prose.",
            fix=fix,
            examples=field_examples(field),
        )

    if finding.code in {
        "preferred_listed_as_alternate",
        "preferred_listed_as_discouraged",
        "alternate_discouraged_overlap",
        "context_rule_uses_discouraged_rendering",
    }:
        return RepairDiagnostic(
            severity=finding.severity,
            category=finding.category,
            code=finding.code,
            file=file,
            rule="Allowed, preferred, and discouraged renderings must not contradict each other",
            summary=finding.message,
            why="Contradictory rendering metadata destroys the entry's ability to govern downstream translation choices.",
            fix="Keep one rendering in one lane only: preferred, allowed alternate, or discouraged. If the contrast is context-bound, record it in `context_rules` without also discouraging the same rendering.",
            examples=("terms/major/dukkha.json", "terms/major/sati.json"),
        )

    if finding.code in {
        "context_sensitive_missing_rules",
        "context_sensitive_missing_note",
        "context_sensitive_indistinct_renderings",
        "context_sensitive_missing_policy",
        "preferred_not_covered_by_context_rules",
    }:
        return RepairDiagnostic(
            severity=finding.severity,
            category=finding.category,
            code=finding.code,
            file=file,
            rule="Context-sensitive policy must be explicit in `context_rules`",
            summary=finding.message,
            why="Context-sensitive terms are major drift vectors unless the repo records both the default and the controlled departures from it.",
            fix=f"Add or revise `context_rules` so the preferred rendering is explicitly covered and each context shift includes a short note. Minimal compliant shape: {field_snippet('context_rules')}",
            examples=field_examples("context_rules"),
        )

    if finding.code in {
        "normalized_term_mismatch",
        "non_nfc_term",
        "inconsistent_term_spelling",
    }:
        return RepairDiagnostic(
            severity=finding.severity,
            category=finding.category,
            code=finding.code,
            file=file,
            rule="Headword normalization must stay deterministic",
            summary=finding.message,
            why="Normalization drift makes it harder for scripts and contributors to tell whether two records are the same governed headword.",
            fix="Keep one canonical displayed spelling and one matching normalized slug. Repair the term or slug rather than letting variants accumulate.",
            examples=("terms/major/sankhara.json",),
        )

    if finding.code == "major_entry_too_definitional":
        return RepairDiagnostic(
            severity=finding.severity,
            category=finding.category,
            code=finding.code,
            file=file,
            rule="Major entries must read as policy, not just definition",
            summary=finding.message,
            why="Definition-only majors do not tell a later contributor what to preserve when nearby terms or compounds put pressure on the default.",
            fix="Strengthen the same record by adding explicit rule-bearing notes, clearer `context_rules`, provenance in `authority_basis`, or a more specific `translation_policy` drift-risk note.",
            examples=MAJOR_POLICY_EXAMPLES,
        )

    return RepairDiagnostic(
        severity=finding.severity,
        category=finding.category,
        code=finding.code,
        file=file,
        rule=f"{finding.category} rule failed",
        summary=finding.message,
        why="This finding marks a translation-governance contradiction that the repo will not merge silently.",
        fix="Repair the smallest safe surface that removes the contradiction, then rerun `python scripts/check_translation_drift.py --strict`.",
        examples=MAJOR_POLICY_EXAMPLES,
    )


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
    error_diagnostics = [finding_to_diagnostic(finding) for finding in errors]
    warning_diagnostics = [finding_to_diagnostic(finding) for finding in warnings]

    if args.json:
        report = {
            "term_files": record_count,
            "errors": diagnostics_as_json(error_diagnostics),
            "warnings": diagnostics_as_json(warning_diagnostics),
        }
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        if errors:
            print("Translation drift check failed:\n")
            print_diagnostics("Errors", error_diagnostics)
        if warnings:
            print("Translation drift warnings:\n")
            print_diagnostics("Warnings", warning_diagnostics)
        if not errors and not warnings:
            print(f"Translation drift check passed for {record_count} term file(s).")

    if errors:
        return 1
    if warnings and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

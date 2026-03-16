#!/usr/bin/env python3
"""Run editorial lint checks against term JSON files."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

try:
    from scripts.text_utils import normalize_term, safe_text
    from scripts.term_store import iter_term_files
except ModuleNotFoundError:
    from text_utils import normalize_term, safe_text
    from term_store import iter_term_files


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
GENERIC_AUTHORITY_SOURCES = {"Repository editorial record"}
STABILIZED_RULE_TERMS = {
    "anatta",
    "ayatana",
    "bhava",
    "dhamma",
    "ditthi",
    "ditthupadana",
    "dukkha",
    "jati",
    "jhana",
    "khandha",
    "mano",
    "mana",
    "namarupa",
    "nibbana",
    "nirodha",
    "paccaya",
    "panna",
    "paticcasamuppada",
    "rupa",
    "samadhi",
    "sankhara",
    "sakkaya",
    "sati",
    "tanha",
    "upadana",
    "attavadupadana",
    "asmimana",
    "vedana",
    "vicara",
    "vinnana",
    "vitakka",
}


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_terms(terms_dir: Path = TERMS_DIR) -> dict[str, dict[str, object]]:
    terms: dict[str, dict[str, object]] = {}
    for path in iter_term_files(terms_dir):
        data = load_json(path)
        if not isinstance(data, dict):
            continue
        terms[normalize_term(path.stem)] = data
    return terms


def check_missing_related_terms(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    for stem, data in sorted(terms.items()):
        related_terms = data.get("related_terms", [])
        if not isinstance(related_terms, list):
            continue
        for related in related_terms:
            if not isinstance(related, str):
                continue
            target = normalize_term(related)
            if target not in terms:
                issues.append(
                    f"{stem}.json: related term '{safe_text(related)}' does not resolve to a local entry"
                )
    return issues


def check_one_way_related_terms(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    for stem, data in sorted(terms.items()):
        if data.get("entry_type") == "minor" and data.get("part_of_speech") in {"phrase", "expression"}:
            continue
        related_terms = data.get("related_terms", [])
        if not isinstance(related_terms, list):
            continue
        for related in related_terms:
            if not isinstance(related, str):
                continue
            target = normalize_term(related)
            if target not in terms:
                continue
            reverse_related = terms[target].get("related_terms", [])
            if not isinstance(reverse_related, list):
                reverse_related = []
            reverse_stems = {normalize_term(item) for item in reverse_related if isinstance(item, str)}
            if stem not in reverse_stems:
                issues.append(
                    f"{stem}.json -> {target}.json: related_terms link is not reciprocal"
                )
    return issues


def check_missing_sutta_references(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    for stem, data in sorted(terms.items()):
        entry_type = data.get("entry_type")
        status = data.get("status")
        references = data.get("sutta_references", [])
        if (
            entry_type == "major"
            and status in {"reviewed", "stable"}
            and (not isinstance(references, list) or len(references) == 0)
        ):
            issues.append(
                f"{stem}.json: major {status} entry is missing sutta_references"
            )
    return issues


def check_untranslated_preferences(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    for stem, data in sorted(terms.items()):
        untranslated = data.get("untranslated_preferred")
        gloss = data.get("gloss_on_first_occurrence")
        if untranslated is True and not isinstance(gloss, str):
            issues.append(
                f"{stem}.json: untranslated_preferred is true but gloss_on_first_occurrence is missing"
            )
    return issues


def check_suspicious_placeholders(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    text_fields = (
        "term",
        "preferred_translation",
        "literal_meaning",
        "definition",
        "gloss_on_first_occurrence",
    )
    for stem, data in sorted(terms.items()):
        for field in text_fields:
            value = data.get(field)
            if isinstance(value, str) and "?" in value:
                issues.append(
                    f"{stem}.json: field '{field}' contains '?' placeholder text; check for encoding loss"
                )
    return issues


def check_mojibake_patterns(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    suspicious = (
        "Ã",
        "Ä",
        "Å",
        "â€™",
        "â€œ",
        "â€",
        "á¹",
        "�",
    )

    def walk(value: object, path: str) -> None:
        if isinstance(value, str):
            for needle in suspicious:
                if needle in value:
                    issues.append(
                        f"{path}: contains suspicious mojibake sequence '{safe_text(needle)}'"
                    )
                    break
            return
        if isinstance(value, list):
            for index, item in enumerate(value):
                walk(item, f"{path}[{index}]")
            return
        if isinstance(value, dict):
            for key, item in value.items():
                walk(item, f"{path}.{key}")

    for stem, data in sorted(terms.items()):
        walk(data, f"{stem}.json")
    return issues


def check_stabilized_term_policy(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    required_list_fields = ("context_rules", "related_terms", "example_phrases", "sutta_references")

    for stem in sorted(STABILIZED_RULE_TERMS):
        data = terms.get(stem)
        if data is None:
            issues.append(f"{stem}.json: stabilized drift-danger term is missing")
            continue

        if data.get("entry_type") != "major":
            issues.append(f"{stem}.json: stabilized drift-danger term must be a major entry")

        status = data.get("status")
        if status not in {"reviewed", "stable"}:
            issues.append(
                f"{stem}.json: stabilized drift-danger term must be reviewed or stable"
            )

        notes = data.get("notes")
        if not isinstance(notes, str) or not notes.strip():
            issues.append(
                f"{stem}.json: stabilized drift-danger term must include rule-bearing notes"
            )

        for field in required_list_fields:
            value = data.get(field)
            if not isinstance(value, list) or len(value) == 0:
                issues.append(
                    f"{stem}.json: stabilized drift-danger term must include non-empty {field}"
                )

        context_rules = data.get("context_rules")
        if isinstance(context_rules, list) and len(context_rules) < 2:
            issues.append(
                f"{stem}.json: stabilized drift-danger term must include at least two context_rules"
            )

    return issues


def check_translation_policy_consistency(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    for stem, data in sorted(terms.items()):
        policy = data.get("translation_policy")
        if not isinstance(policy, dict):
            continue

        untranslated = data.get("untranslated_preferred") is True
        leave_untranslated_when = policy.get("leave_untranslated_when")
        default_scope = policy.get("default_scope")
        drift_risk = policy.get("drift_risk")
        inheritance = policy.get("compound_inheritance")

        if untranslated and not isinstance(leave_untranslated_when, str):
            issues.append(
                f"{stem}.json: untranslated-preferred policy should explain leave_untranslated_when in translation_policy"
            )

        if data.get("entry_type") == "major":
            if not isinstance(default_scope, str):
                issues.append(
                    f"{stem}.json: major entry with translation_policy should include default_scope"
                )
            if not isinstance(drift_risk, str):
                issues.append(
                    f"{stem}.json: major entry with translation_policy should include drift_risk"
                )
            if inheritance == "inherit":
                notes = data.get("notes")
                context_rules = data.get("context_rules")
                notes_text = notes.lower() if isinstance(notes, str) else ""
                context_mentions_compounds = False
                if isinstance(context_rules, list):
                    context_mentions_compounds = any(
                        isinstance(rule, dict)
                        and isinstance(rule.get("context"), str)
                        and "compound" in rule["context"].lower()
                        for rule in context_rules
                    )
                if "compound" not in notes_text and not context_mentions_compounds:
                    issues.append(
                        f"{stem}.json: translation_policy sets compound_inheritance to inherit but notes/context_rules do not mention compounds"
                    )

    return issues


def check_authority_basis_consistency(terms: dict[str, dict[str, object]]) -> list[str]:
    issues: list[str] = []
    for stem, data in sorted(terms.items()):
        authority_basis = data.get("authority_basis")
        if authority_basis is None:
            continue
        if not isinstance(authority_basis, list) or len(authority_basis) == 0:
            issues.append(
                f"{stem}.json: authority_basis is present but empty"
            )
            continue

        notes = data.get("notes")
        notes_text = notes.lower() if isinstance(notes, str) else ""
        for index, item in enumerate(authority_basis, start=1):
            if not isinstance(item, dict):
                continue
            source = item.get("source")
            if isinstance(source, str):
                if source in GENERIC_AUTHORITY_SOURCES:
                    continue
                source_token = source.lower().split()[0]
                if source_token not in notes_text:
                    issues.append(
                        f"{stem}.json: authority_basis[{index}] source '{safe_text(source)}' is not reflected in notes"
                    )

    return issues


def print_group(title: str, issues: list[str]) -> None:
    if not issues:
        return
    print(f"{title}:")
    for issue in issues:
        print(f"- {safe_text(issue)}")
    print()


def collect_lint_results(
    terms: dict[str, dict[str, object]],
    *,
    enforce_stabilized_terms: bool = True,
) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    errors = defaultdict(list)
    warnings = defaultdict(list)

    resolution_issues = check_missing_related_terms(terms)
    reciprocal_issues = check_one_way_related_terms(terms)
    reference_issues = check_missing_sutta_references(terms)
    gloss_issues = check_untranslated_preferences(terms)
    placeholder_issues = check_suspicious_placeholders(terms)
    mojibake_issues = check_mojibake_patterns(terms)
    stabilized_term_issues = (
        check_stabilized_term_policy(terms) if enforce_stabilized_terms else []
    )
    translation_policy_issues = check_translation_policy_consistency(terms)
    authority_basis_issues = check_authority_basis_consistency(terms)

    if resolution_issues:
        errors["Resolution"].extend(resolution_issues)
    if placeholder_issues:
        errors["Encoding"].extend(placeholder_issues)
    if mojibake_issues:
        errors["Encoding"].extend(mojibake_issues)
    if stabilized_term_issues:
        errors["Stabilized Terms"].extend(stabilized_term_issues)
    if translation_policy_issues:
        errors["Translation Policy"].extend(translation_policy_issues)
    if authority_basis_issues:
        errors["Authority Basis"].extend(authority_basis_issues)
    if reciprocal_issues:
        warnings["Reciprocal Links"].extend(reciprocal_issues)
    if reference_issues:
        warnings["References"].extend(reference_issues)
    if gloss_issues:
        warnings["Glossing"].extend(gloss_issues)

    return dict(errors), dict(warnings)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on warnings as well as errors.",
    )
    args = parser.parse_args()

    if not TERMS_DIR.exists():
        print(f"ERROR: Terms directory not found: {TERMS_DIR}")
        return 1

    terms = load_terms()
    if not terms:
        print("WARNING: No term files found in terms/")
        return 0

    errors, warnings = collect_lint_results(terms)

    if errors:
        print("Editorial lint failed:\n")
        for title, issues in errors.items():
            print_group(title, issues)
        return 1

    if warnings:
        print("Editorial lint warnings:\n")
        for title, issues in warnings.items():
            print_group(title, issues)
        if args.strict:
            return 1
        total = sum(len(items) for items in warnings.values())
        print(f"Completed with {total} warning(s).")
        return 0

    print(f"Editorial lint passed for {len(terms)} term file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

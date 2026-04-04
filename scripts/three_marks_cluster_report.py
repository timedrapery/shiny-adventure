#!/usr/bin/env python3
"""Audit and generate translator-facing outputs for the three-marks cluster."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from scripts.term_store import iter_term_files
    from scripts.text_utils import safe_text
except ModuleNotFoundError:
    from term_store import iter_term_files
    from text_utils import safe_text


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
OUTPUT_DIR = REPO_ROOT / "docs" / "generated"

HEADWORD_TERMS = [
    "anicca",
    "dukkha",
    "anatta",
]

SUPPORTING_TERMS = [
    "sankhara",
    "sankhata",
    "dhamma",
]

PRACTICE_TERMS = [
    "anicca-sanna",
    "dukkha-sanna",
    "anatta-sanna",
    "aniccanupassana",
    "dukkhanupassana",
    "anattanupassana",
]

FORMULA_TERMS = [
    "anicca-sabbe-sankhara",
    "dukkha-sabbe-sankhara",
    "sabbe-dhamma-anatta",
    "sabbe-sankhata-anicca",
    "yam-aniccam-tam-dukkham-yam-dukkham-tad-anatta",
]

EXPECTED_PREFERRED_TRANSLATIONS = {
    "anicca": "impermanent",
    "dukkha": "dissatisfaction",
    "anatta": "not-self",
    "sankhara": "putting things together",
    "sankhata": "conditioned",
    "dhamma": "dhamma",
    "anicca-sanna": "perception of impermanence",
    "dukkha-sanna": "perception of dissatisfaction",
    "anatta-sanna": "perception of not-self",
    "aniccanupassana": "contemplation of impermanence",
    "dukkhanupassana": "contemplation of dissatisfaction",
    "anattanupassana": "contemplation of not-self",
    "anicca-sabbe-sankhara": "all that has been put together is impermanent",
    "dukkha-sabbe-sankhara": "all that has been put together is unsatisfactory",
    "sabbe-dhamma-anatta": "all phenomena are not-self",
    "sabbe-sankhata-anicca": "all conditioned things are impermanent",
    "yam-aniccam-tam-dukkham-yam-dukkham-tad-anatta": (
        "what is impermanent is dissatisfaction; what is dissatisfaction is not-self"
    ),
}


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_terms(terms_dir: Path = TERMS_DIR) -> dict[str, dict[str, object]]:
    terms: dict[str, dict[str, object]] = {}
    for path in iter_term_files(terms_dir):
        data = load_json(path)
        if isinstance(data, dict):
            terms[path.stem] = data
    return terms


def missing_terms(terms: dict[str, dict[str, object]], stems: list[str]) -> list[str]:
    return [stem for stem in stems if stem not in terms]


def example_source_gaps(terms: dict[str, dict[str, object]], stems: list[str]) -> list[str]:
    gaps: list[str] = []
    for stem in stems:
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        examples = data.get("example_phrases")
        if not isinstance(examples, list) or not examples:
            gaps.append(stem)
            continue
        if any(not isinstance(item, dict) or not item.get("source") for item in examples):
            gaps.append(stem)
    return gaps


def weak_authority_terms(terms: dict[str, dict[str, object]], stems: list[str]) -> list[str]:
    weak: list[str] = []
    for stem in stems:
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        authority = data.get("authority_basis")
        if not isinstance(authority, list) or len(authority) < 2:
            weak.append(stem)
    return weak


def thin_terms(terms: dict[str, dict[str, object]], stems: list[str]) -> list[str]:
    thin: list[str] = []
    for stem in stems:
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        notes = data.get("notes")
        related = data.get("related_terms")
        examples = data.get("example_phrases")
        if (
            not isinstance(notes, str)
            or not notes.strip()
            or not isinstance(related, list)
            or not related
            or not isinstance(examples, list)
            or not examples
        ):
            thin.append(stem)
    return thin


def preferred_rendering_mismatches(terms: dict[str, dict[str, object]]) -> list[str]:
    mismatches: list[str] = []
    for stem, expected in EXPECTED_PREFERRED_TRANSLATIONS.items():
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        actual = data.get("preferred_translation")
        if actual != expected:
            mismatches.append(f"{stem}: expected '{expected}', found '{actual}'")
    return mismatches


def contains_all(blob: str, tokens: list[str]) -> bool:
    return all(token in blob for token in tokens)


def formula_override_identity_missing(terms: dict[str, dict[str, object]]) -> list[str]:
    missing: list[str] = []
    expectations = {
        "sankhara": ["three-marks formulae", "that which has been put together"],
        "sankhata": ["conditioned", "impermanent"],
        "dhamma": ["phenomenon"],
        "anicca-sabbe-sankhara": ["impermanent", "put together"],
        "dukkha-sabbe-sankhara": ["unsatisfactory", "put together"],
        "sabbe-dhamma-anatta": ["phenomena", "not-self"],
        "sabbe-sankhata-anicca": ["conditioned things", "impermanent"],
        "yam-aniccam-tam-dukkham-yam-dukkham-tad-anatta": ["impermanent", "dissatisfaction", "not-self"],
    }
    for stem, tokens in expectations.items():
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        blob = json.dumps(data, ensure_ascii=False).casefold()
        if not contains_all(blob, tokens):
            missing.append(stem)
    return missing


def build_report(terms: dict[str, dict[str, object]]) -> dict[str, object]:
    all_priority = HEADWORD_TERMS + SUPPORTING_TERMS + PRACTICE_TERMS + FORMULA_TERMS
    return {
        "summary": {
            "headwords_present": len(HEADWORD_TERMS) - len(missing_terms(terms, HEADWORD_TERMS)),
            "headwords_expected": len(HEADWORD_TERMS),
            "supporting_terms_present": len(SUPPORTING_TERMS) - len(missing_terms(terms, SUPPORTING_TERMS)),
            "supporting_terms_expected": len(SUPPORTING_TERMS),
            "practice_terms_present": len(PRACTICE_TERMS) - len(missing_terms(terms, PRACTICE_TERMS)),
            "practice_terms_expected": len(PRACTICE_TERMS),
            "formula_terms_present": len(FORMULA_TERMS) - len(missing_terms(terms, FORMULA_TERMS)),
            "formula_terms_expected": len(FORMULA_TERMS),
        },
        "errors": {
            "missing_headwords": missing_terms(terms, HEADWORD_TERMS),
            "missing_supporting_terms": missing_terms(terms, SUPPORTING_TERMS),
            "missing_practice_terms": missing_terms(terms, PRACTICE_TERMS),
            "missing_formula_terms": missing_terms(terms, FORMULA_TERMS),
            "cluster_example_source_gaps": example_source_gaps(terms, all_priority),
        },
        "warnings": {
            "headwords_with_thin_authority_basis": weak_authority_terms(terms, HEADWORD_TERMS),
            "practice_terms_still_thin": thin_terms(terms, PRACTICE_TERMS),
            "formula_terms_still_thin": thin_terms(terms, FORMULA_TERMS),
            "preferred_rendering_mismatches": preferred_rendering_mismatches(terms),
            "formula_override_identity_missing": formula_override_identity_missing(terms),
        },
    }


def render_glossary(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Three Marks Cluster Glossary",
        "",
        "| Role | Pali | Default | Allowed alternates | Discouraged |",
        "| --- | --- | --- | --- | --- |",
    ]
    grouped_terms = (
        [("Headword", stem) for stem in HEADWORD_TERMS]
        + [("Support", stem) for stem in SUPPORTING_TERMS]
        + [("Practice", stem) for stem in PRACTICE_TERMS]
        + [("Formula", stem) for stem in FORMULA_TERMS]
    )
    for role, stem in grouped_terms:
        data = terms[stem]
        alts = ", ".join(data.get("alternative_translations", []))
        discouraged = ", ".join(data.get("discouraged_translations", []))
        lines.append(
            f"| {role} | {data.get('term')} | {data.get('preferred_translation')} | {alts or '-'} | {discouraged or '-'} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_contemplation_sheet(terms: dict[str, dict[str, object]]) -> str:
    triads = [
        ("anicca", "anicca-sanna", "aniccanupassana", "anicca-sabbe-sankhara"),
        ("dukkha", "dukkha-sanna", "dukkhanupassana", "dukkha-sabbe-sankhara"),
        ("anatta", "anatta-sanna", "anattanupassana", "sabbe-dhamma-anatta"),
    ]
    lines = [
        "# Three Marks Contemplation Sheet",
        "",
        "| Mark | Perception | Contemplation | Governing formula |",
        "| --- | --- | --- | --- |",
    ]
    for headword, perception, contemplation, formula in triads:
        lines.append(
            f"| {terms[headword].get('preferred_translation')} | {terms[perception].get('preferred_translation')} | "
            f"{terms[contemplation].get('preferred_translation')} | {terms[formula].get('preferred_translation')} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_formula_sheet(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Three Marks Formula Sheet",
        "",
        f"- `{terms['anicca-sabbe-sankhara']['term']}` -> `{terms['anicca-sabbe-sankhara']['preferred_translation']}`",
        "  Keep `saṅkhārā` on its result-side reading here rather than the dependent-arising process sense.",
        f"- `{terms['dukkha-sabbe-sankhara']['term']}` -> `{terms['dukkha-sabbe-sankhara']['preferred_translation']}`",
        "  Let the formula use adjective-grade English without silently resetting the headword policy elsewhere.",
        f"- `{terms['sabbe-dhamma-anatta']['term']}` -> `{terms['sabbe-dhamma-anatta']['preferred_translation']}`",
        "  This line is a controlled override of the headword-level preference to leave `dhamma` untranslated.",
        f"- `{terms['sabbe-sankhata-anicca']['term']}` -> `{terms['sabbe-sankhata-anicca']['preferred_translation']}`",
        "  Keep the conditioned / impermanent relation explicit.",
        f"- `{terms['yam-aniccam-tam-dukkham-yam-dukkham-tad-anatta']['term']}` -> "
        f"`{terms['yam-aniccam-tam-dukkham-yam-dukkham-tad-anatta']['preferred_translation']}`",
        "  This is the cluster's compact progression line and should stay coordinated across all three marks.",
    ]
    return "\n".join(lines)


def render_translator_brief(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Three Marks Translator Brief",
        "",
        "## Core Defaults",
        "",
        f"- `{terms['anicca']['term']}` -> `{terms['anicca']['preferred_translation']}`",
        f"- `{terms['dukkha']['term']}` -> `{terms['dukkha']['preferred_translation']}`",
        f"- `{terms['anatta']['term']}` -> `{terms['anatta']['preferred_translation']}`",
        "",
        "## Drift Guards",
        "",
        "- Do not let `dukkha` drift back to uncontrolled suffering-language in the three-marks family.",
        "- Do not flatten `anattā` into nihilistic `no-self` slogans.",
        "- Keep `saṅkhārā` on its result-side reading in the Dhp 277-278 formulae.",
        "- Let `sabbe dhammā anattā` use `phenomena` without forcing that override back onto every `dhamma` context.",
        "- Keep the progression from impermanent to dissatisfaction to not-self readable across the family.",
    ]
    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "three-marks-cluster-glossary.md": render_glossary(terms),
        OUTPUT_DIR / "three-marks-contemplation-sheet.md": render_contemplation_sheet(terms),
        OUTPUT_DIR / "three-marks-formula-sheet.md": render_formula_sheet(terms),
        OUTPUT_DIR / "three-marks-translator-brief.md": render_translator_brief(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + ("" if content.endswith("\n") else "\n"), encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    summary = report["summary"]
    errors = report["errors"]
    warnings = report["warnings"]

    print("Three Marks Cluster Report")
    print(f"- Headwords: {summary['headwords_present']} / {summary['headwords_expected']}")
    print(f"- Supporting terms: {summary['supporting_terms_present']} / {summary['supporting_terms_expected']}")
    print(f"- Practice terms: {summary['practice_terms_present']} / {summary['practice_terms_expected']}")
    print(f"- Formula terms: {summary['formula_terms_present']} / {summary['formula_terms_expected']}")
    print()

    print("Errors")
    for key, items in errors.items():
        if items:
            print(f"- {safe_text(key)}: {', '.join(safe_text(item) for item in items)}")
        else:
            print(f"- {safe_text(key)}: none")
    print()

    print("Warnings")
    for key, items in warnings.items():
        if items:
            print(f"- {safe_text(key)}: {', '.join(safe_text(item) for item in items)}")
        else:
            print(f"- {safe_text(key)}: none")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--strict", action="store_true", help="Fail on report errors.")
    parser.add_argument("--write-docs", action="store_true", help="Generate Markdown outputs in docs/generated.")
    args = parser.parse_args()

    if not TERMS_DIR.exists():
        print(f"ERROR: Terms directory not found: {TERMS_DIR}")
        return 1

    terms = load_terms()
    report = build_report(terms)

    if args.write_docs:
        write_outputs(terms)

    if args.format == "json":
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print_text_report(report)

    if args.strict and any(report["errors"].values()):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

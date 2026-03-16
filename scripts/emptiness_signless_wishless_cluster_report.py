#!/usr/bin/env python3
"""Audit and generate outputs for the emptiness / signless / wishless interface cluster."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from scripts.text_utils import safe_text
    from scripts.term_store import iter_term_files
except ModuleNotFoundError:
    from text_utils import safe_text
    from term_store import iter_term_files


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
OUTPUT_DIR = REPO_ROOT / "docs" / "generated"

HEADWORD_TERMS = [
    "sunnata",
    "animitta",
    "appanihita",
]

SUPPORTING_TERMS = [
    "sunnata-samadhi",
    "sunnata-cetosamadhi",
    "sunnata-vimokkha",
    "animitta-samadhi",
    "animitta-cetosamadhi",
    "animitta-vimokkha",
    "appanihita-samadhi",
    "appanihita-cetosamadhi",
    "appanihita-vimokkha",
    "vimokkhamukha",
]


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


def render_mismatch_warnings(terms: dict[str, dict[str, object]]) -> list[str]:
    warnings: list[str] = []
    expected = {
        "sunnata": "emptiness",
        "animitta": "signless",
        "appanihita": "wishless",
        "sunnata-vimokkha": "emptiness release",
        "animitta-vimokkha": "signless release",
        "appanihita-vimokkha": "wishless release",
    }
    for stem, expected_rendering in expected.items():
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        if data.get("preferred_translation") != expected_rendering:
            warnings.append(stem)
    return warnings


def headword_status_gaps(terms: dict[str, dict[str, object]]) -> list[str]:
    gaps: list[str] = []
    for stem in HEADWORD_TERMS:
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        if data.get("entry_type") != "major" or data.get("status") != "stable":
            gaps.append(stem)
    return gaps


def build_report(terms: dict[str, dict[str, object]]) -> dict[str, object]:
    return {
        "summary": {
            "headwords_present": len(HEADWORD_TERMS) - len(missing_terms(terms, HEADWORD_TERMS)),
            "headwords_expected": len(HEADWORD_TERMS),
            "supporting_terms_present": len(SUPPORTING_TERMS) - len(missing_terms(terms, SUPPORTING_TERMS)),
            "supporting_terms_expected": len(SUPPORTING_TERMS),
            "formula_records_present": 0,
            "formula_records_expected": 0,
        },
        "errors": {
            "missing_headwords": missing_terms(terms, HEADWORD_TERMS),
            "missing_supporting_terms": missing_terms(terms, SUPPORTING_TERMS),
            "unstable_or_non_major_headwords": headword_status_gaps(terms),
        },
        "warnings": {
            "headwords_with_thin_authority_basis": weak_authority_terms(terms, HEADWORD_TERMS),
            "preferred_rendering_mismatches": render_mismatch_warnings(terms),
        },
    }


def render_glossary(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Emptiness / Signless / Wishless Glossary",
        "",
        "| Pali | Default | Allowed alternates | Discouraged |",
        "| --- | --- | --- | --- |",
    ]
    for stem in HEADWORD_TERMS + [
        "sunnata-samadhi",
        "animitta-samadhi",
        "appanihita-samadhi",
        "sunnata-vimokkha",
        "animitta-vimokkha",
        "appanihita-vimokkha",
    ]:
        data = terms[stem]
        alts = ", ".join(data.get("alternative_translations", []))
        discouraged = ", ".join(data.get("discouraged_translations", []))
        lines.append(
            f"| {data.get('term')} | {data.get('preferred_translation')} | {alts or '-'} | {discouraged or '-'} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_contrast_sheet(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Emptiness / Signless / Wishless Contrast Sheet",
        "",
        f"- `{terms['sunnata']['term']}`: `{terms['sunnata']['preferred_translation']}`",
        f"- `{terms['animitta']['term']}`: `{terms['animitta']['preferred_translation']}`",
        f"- `{terms['appanihita']['term']}`: `{terms['appanihita']['preferred_translation']}`",
        "",
        "## Keep Distinct",
        "",
        "- `suññatā` is emptiness-side language, especially empty of self and what belongs to self.",
        "- `anattā` remains not-self language and should not replace `suññatā` by habit.",
        "- `animitta` is signless language, not formlessness or blankness.",
        "- `appaṇihita` is wishless language, not passivity or no-goals ideology.",
        "- `nibbāna` remains the consummation-side headword, not a synonym for the triad.",
        "- `vimutti` remains release-language, while `vimokkhamukha` names the family as gateways to release.",
    ]
    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "emptiness-signless-wishless-glossary.md": render_glossary(terms),
        OUTPUT_DIR / "emptiness-signless-wishless-contrast-sheet.md": render_contrast_sheet(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + "\n", encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    summary = report["summary"]
    errors = report["errors"]
    warnings = report["warnings"]

    print("Emptiness / Signless / Wishless Interface Cluster Report")
    print(f"- Headwords: {summary['headwords_present']} / {summary['headwords_expected']}")
    print(f"- Supporting terms: {summary['supporting_terms_present']} / {summary['supporting_terms_expected']}")
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

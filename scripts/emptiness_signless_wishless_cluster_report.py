#!/usr/bin/env python3
"""Audit and generate outputs for the emptiness / signless / wishless interface cluster."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from scripts import cluster_report_common as common
    from scripts.cluster_report_common import load_terms, missing_terms, weak_authority_terms
except ModuleNotFoundError:
    import cluster_report_common as common
    from cluster_report_common import load_terms, missing_terms, weak_authority_terms


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
    for stem in HEADWORD_TERMS + SUPPORTING_TERMS:
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
    common.print_text_report("Emptiness / Signless / Wishless Interface Cluster Report", report)


def main() -> int:
    return common.run_cli(sys.modules[__name__])


if __name__ == "__main__":
    sys.exit(main())

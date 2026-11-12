#!/usr/bin/env python3
"""Audit and generate translator-facing outputs for the crossing / escape / release interface cluster."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from scripts import cluster_report_common as common
    from scripts.cluster_report_common import load_terms, missing_terms, example_source_gaps, weak_authority_terms
except ModuleNotFoundError:
    import cluster_report_common as common
    from cluster_report_common import load_terms, missing_terms, example_source_gaps, weak_authority_terms


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
OUTPUT_DIR = REPO_ROOT / "docs" / "generated"

HEADWORD_TERMS = [
    "nissarana",
    "vimutti",
    "mutti",
    "tarati",
    "tinna",
]

SUPPORTING_TERMS = [
    "nissarana-dhatu",
    "cetovimutti",
    "pannavimutti",
    "vimutti-nanadassana",
    "yogakkhema",
]

FORMULA_TERMS = [
    "imesam-pancannam-upadanakkhandhanam-assadanca-adinavanca-nissarananca",
    "ogham-atari",
    "tinno-parangato",
]


def render_mismatch_warnings(terms: dict[str, dict[str, object]]) -> list[str]:
    warnings: list[str] = []
    expected = {
        "nissarana": "escape",
        "vimutti": "release",
        "mutti": "freedom",
        "tarati": "crosses over",
        "tinna": "crossed over",
        "yogakkhema": "security from the yoke",
        "nissarana-dhatu": "element of escape",
        "ogham-atari": "crossed over the flood",
        "tinno-parangato": "crossed over, gone to the far shore",
    }
    for stem, expected_rendering in expected.items():
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        if data.get("preferred_translation") != expected_rendering:
            warnings.append(stem)
    return warnings


def build_report(terms: dict[str, dict[str, object]]) -> dict[str, object]:
    all_priority = HEADWORD_TERMS + SUPPORTING_TERMS + FORMULA_TERMS
    return {
        "summary": {
            "headwords_present": len(HEADWORD_TERMS) - len(missing_terms(terms, HEADWORD_TERMS)),
            "headwords_expected": len(HEADWORD_TERMS),
            "supporting_terms_present": len(SUPPORTING_TERMS) - len(missing_terms(terms, SUPPORTING_TERMS)),
            "supporting_terms_expected": len(SUPPORTING_TERMS),
            "formula_records_present": len(FORMULA_TERMS) - len(missing_terms(terms, FORMULA_TERMS)),
            "formula_records_expected": len(FORMULA_TERMS),
        },
        "errors": {
            "missing_headwords": missing_terms(terms, HEADWORD_TERMS),
            "missing_supporting_terms": missing_terms(terms, SUPPORTING_TERMS),
            "missing_formula_records": missing_terms(terms, FORMULA_TERMS),
            "cluster_example_source_gaps": example_source_gaps(terms, all_priority),
        },
        "warnings": {
            "headwords_with_thin_authority_basis": weak_authority_terms(terms, HEADWORD_TERMS),
            "preferred_rendering_mismatches": render_mismatch_warnings(terms),
        },
    }


def render_glossary(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Crossing / Escape / Release Interface Glossary",
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
        "# Crossing / Escape / Release Interface Contrast Sheet",
        "",
        f"- `{terms['nissarana']['term']}`: `{terms['nissarana']['preferred_translation']}`",
        f"- `{terms['vimutti']['term']}`: `{terms['vimutti']['preferred_translation']}`",
        f"- `{terms['mutti']['term']}`: `{terms['mutti']['preferred_translation']}`",
        f"- `{terms['tarati']['term']}`: `{terms['tarati']['preferred_translation']}`",
        f"- `{terms['tinna']['term']}`: `{terms['tinna']['preferred_translation']}`",
        f"- `{terms['yogakkhema']['term']}`: `{terms['yogakkhema']['preferred_translation']}`",
        "",
        "## Keep Distinct",
        "",
        "- `nissaraṇa` is escape or way-out language, not the generic release-family headword.",
        "- `vimutti` is the governed release-family headword, not the same thing as `nissaraṇa`, `mutti`, or crossing language.",
        "- `mutti` is the shorter result-noun and defaults to `freedom`, not an uncontrolled synonym switch for `vimutti`.",
        "- `tarati` is crossing as action or process, not generic escape or liberation language.",
        "- `tiṇṇa` is accomplished crossing, not just another way to say `vimutta`.",
        "- `yogakkhema` is security from the yoke, not generic peace or safety.",
        "- `ogha` remains the flood family that is crossed over.",
        "- `yoga` remains the yoke family from which security is gained.",
    ]
    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "crossing-release-interface-glossary.md": render_glossary(terms),
        OUTPUT_DIR / "crossing-release-interface-contrast-sheet.md": render_contrast_sheet(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + "\n", encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    common.print_text_report("Crossing / Escape / Release Interface Cluster Report", report)


def main() -> int:
    return common.run_cli(sys.modules[__name__])


if __name__ == "__main__":
    sys.exit(main())

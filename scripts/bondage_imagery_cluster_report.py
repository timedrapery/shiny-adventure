#!/usr/bin/env python3
"""Audit and generate translator-facing outputs for the bondage-imagery cluster."""

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
    "ogha",
    "yoga",
    "gantha",
]

SUPPORTING_TERMS = [
    "kamogha",
    "bhavogha",
    "ditthogha",
    "avijjogha",
    "kamayoga",
    "bhavayoga",
    "ditthiyoga",
    "avijjayoga",
    "kayagantha",
    "abhijjha-kayagantha",
    "byapada-kayagantha",
    "silabbata-paramasa-kayagantha",
    "idamsacca-abhinivesa-kayagantha",
    "yogakkhema",
]

FORMULA_TERMS = [
    "cattarome-bhikkhave-ogha",
    "cattarome-bhikkhave-yoga",
    "cattarome-bhikkhave-gantha",
]


def render_mismatch_warnings(terms: dict[str, dict[str, object]]) -> list[str]:
    warnings: list[str] = []
    expected = {
        "ogha": "flood",
        "yoga": "yoke",
        "gantha": "knot",
        "kamogha": "sensual flood",
        "kamayoga": "sensual yoke",
        "kayagantha": "bodily knot",
        "yogakkhema": "security from the yoke",
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
        "# Bondage-Imagery Cluster Glossary",
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
        "# Bondage-Imagery Contrast Sheet",
        "",
        f"- `{terms['ogha']['term']}`: `{terms['ogha']['preferred_translation']}`",
        f"- `{terms['yoga']['term']}`: `{terms['yoga']['preferred_translation']}`",
        f"- `{terms['gantha']['term']}`: `{terms['gantha']['preferred_translation']}`",
        f"- `{terms['kayagantha']['term']}`: `{terms['kayagantha']['preferred_translation']}`",
        "",
        "## Keep Distinct",
        "",
        "- `ogha` is flood imagery: it overwhelms and is crossed over.",
        "- `yoga` is yoke imagery: it harnesses or keeps one under a binding burden.",
        "- `gantha` is knot imagery: it ties up and fastens.",
        "- `kāyagantha` keeps that knot image explicit in the fourfold member set.",
        "- `saṃyojana` remains the fetter family, not a synonym for the imagery terms.",
        "- `āsava` remains the outflow family, not a flood, yoke, or knot.",
        "- `anusaya` remains the latent-underlying family, not an imagery substitute.",
    ]
    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "bondage-imagery-cluster-glossary.md": render_glossary(terms),
        OUTPUT_DIR / "bondage-imagery-contrast-sheet.md": render_contrast_sheet(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + "\n", encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    common.print_text_report("Bondage-Imagery Cluster Report", report)


def main() -> int:
    return common.run_cli(sys.modules[__name__])


if __name__ == "__main__":
    sys.exit(main())

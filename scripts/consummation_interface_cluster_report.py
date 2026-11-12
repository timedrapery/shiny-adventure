#!/usr/bin/env python3
"""Audit and generate translator-facing outputs for the consummation / unconditioned interface cluster."""

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
    "nibbana",
    "amata",
    "asankhata",
    "santi",
    "nibbuta",
    "parinibbana",
]

SUPPORTING_TERMS = [
    "amatapada",
    "asankhata-dhatu",
    "nibbana-dhatu",
    "saupadisesa-nibbana-dhatu",
    "anupadisesa-nibbana-dhatu",
    "parinibbana-dhatu",
    "upasama",
    "upasamanussati",
    "vimutti",
    "yogakkhema",
]

FORMULA_TERMS = [
    "ditthadhammanibbana",
]


def render_mismatch_warnings(terms: dict[str, dict[str, object]]) -> list[str]:
    warnings: list[str] = []
    expected = {
        "nibbana": "nibbāna",
        "amata": "deathless",
        "asankhata": "unconditioned",
        "santi": "peace",
        "nibbuta": "cooled",
        "parinibbana": "final nibbāna",
        "amatapada": "path to the deathless",
        "asankhata-dhatu": "unconditioned element",
        "nibbana-dhatu": "nibbāna element",
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
        "# Consummation / Unconditioned Interface Glossary",
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
        "# Consummation / Unconditioned Interface Contrast Sheet",
        "",
        f"- `{terms['nibbana']['term']}`: `{terms['nibbana']['preferred_translation']}`",
        f"- `{terms['amata']['term']}`: `{terms['amata']['preferred_translation']}`",
        f"- `{terms['asankhata']['term']}`: `{terms['asankhata']['preferred_translation']}`",
        f"- `{terms['santi']['term']}`: `{terms['santi']['preferred_translation']}`",
        f"- `{terms['nibbuta']['term']}`: `{terms['nibbuta']['preferred_translation']}`",
        f"- `{terms['parinibbana']['term']}`: `{terms['parinibbana']['preferred_translation']}`",
        "",
        "## Keep Distinct",
        "",
        "- `nibbāna` remains the governing consummation-side headword and is left untranslated by default.",
        "- `amata` is deathless language, not immortality-language and not just another casual synonym for `nibbāna`.",
        "- `asaṅkhata` is unconditioned language, not vague metaphysics and not a free replacement for `nibbāna`.",
        "- `santi` is peace-language, not mood-level calm and not `passaddhi`.",
        "- `nibbuta` is adjectival cooling-language, not the noun `nibbāna`.",
        "- `parinibbāna` is final nibbāna, not generic death-language.",
        "- `vimutti` remains release-language, not the same layer as the consummation designations.",
        "- `yogakkhema` remains security from the yoke, not a generic substitute for consummation terms.",
    ]
    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "consummation-interface-glossary.md": render_glossary(terms),
        OUTPUT_DIR / "consummation-interface-contrast-sheet.md": render_contrast_sheet(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + "\n", encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    common.print_text_report("Consummation / Unconditioned Interface Cluster Report", report)


def main() -> int:
    return common.run_cli(sys.modules[__name__])


if __name__ == "__main__":
    sys.exit(main())

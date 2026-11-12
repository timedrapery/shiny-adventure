#!/usr/bin/env python3
"""Audit and generate translator-facing outputs for the bondage / residue cluster."""

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
    "asava",
    "anusaya",
    "samyojana",
    "nivarana",
    "kilesa",
]

SUPPORTING_TERMS = [
    "upakkilesa",
    "pahana",
    "vossagga",
    "panca-nivarana",
    "avijjasava",
    "kamasava",
    # `ditthasava` is not listed: the suttas name three outflows, and the
    # outflow of views belongs to later lists. Its only citation (DN 33) was
    # false and was removed in the Wave 12 audit, so it has no sutta example.
    "bhavasava",
    "avijja-anusaya",
    "kamaraga-anusaya",
    "bhavaraga-anusaya",
    "patigha-anusaya",
    "mana-anusaya",
    "ditthi-anusaya",
    "vicikiccha-anusaya",
    "orambhagiya-samyojana",
    "uddhambhagiya-samyojana",
]

FORMULA_TERMS = [
    "asavanam-khaya",
]


def render_mismatch_warnings(terms: dict[str, dict[str, object]]) -> list[str]:
    warnings: list[str] = []
    expected = {
        "asava": "outflow",
        "anusaya": "underlying tendency",
        "samyojana": "fetter",
        "nivarana": "hindrance",
        "kilesa": "defilement",
        "upakkilesa": "corruption",
        "pahana": "abandoning",
        "vossagga": "relinquishment",
        "panca-nivarana": "five hindrances",
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
        "# Bondage / Residue Cluster Glossary",
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
        "# Bondage / Residue Contrast Sheet",
        "",
        f"- `{terms['kilesa']['term']}`: `{terms['kilesa']['preferred_translation']}`",
        f"- `{terms['upakkilesa']['term']}`: `{terms['upakkilesa']['preferred_translation']}`",
        f"- `{terms['nivarana']['term']}`: `{terms['nivarana']['preferred_translation']}`",
        f"- `{terms['anusaya']['term']}`: `{terms['anusaya']['preferred_translation']}`",
        f"- `{terms['samyojana']['term']}`: `{terms['samyojana']['preferred_translation']}`",
        f"- `{terms['asava']['term']}`: `{terms['asava']['preferred_translation']}`",
        "",
        "## Keep Distinct",
        "",
        "- `kilesa` is the broad defilement-family; it is not the only label for every narrower bondage term.",
        "- `nīvaraṇa` is an active hindrance in practice, not a latent residue by default.",
        "- `anusaya` is latent persistence lying underneath, not merely a surface obstruction.",
        "- `saṃyojana` is binding fetter-language tied to continued becoming and awakening-stage analysis.",
        "- `āsava` is deep outflow-language and should stay stable in liberation formulas such as `āsavānaṃ khayā`.",
    ]
    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "bondage-residue-cluster-glossary.md": render_glossary(terms),
        OUTPUT_DIR / "bondage-residue-contrast-sheet.md": render_contrast_sheet(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + "\n", encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    common.print_text_report("Bondage / Residue Cluster Report", report)


def main() -> int:
    return common.run_cli(sys.modules[__name__])


if __name__ == "__main__":
    sys.exit(main())

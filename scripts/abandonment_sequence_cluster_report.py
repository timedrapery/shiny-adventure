#!/usr/bin/env python3
"""Audit and generate translator-facing outputs for the abandonment / quenching / exhaustion cluster."""

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
    "pariyutthana",
    "pahana",
    "viraga",
    "vossagga",
    "nirodha",
    "khaya",
]

SUPPORTING_TERMS = [
    "pahana-sanna",
    "vossaggaparinami",
    "asavanam-khaya",
    "asavakkhaya",
    "khaye-nana",
]

FORMULA_TERMS = [
    "asesa-viraga-nirodha",
    "imassa-nirodha-idam-nirujjhati",
]


def render_mismatch_warnings(terms: dict[str, dict[str, object]]) -> list[str]:
    warnings: list[str] = []
    expected = {
        "pariyutthana": "manifestation",
        "pahana": "abandoning",
        "viraga": "fading",
        "vossagga": "relinquishment",
        "nirodha": "quenching",
        "khaya": "wearing away",
        "asavanam-khaya": "through the wearing away of the outflows",
        "asavakkhaya": "the wearing away of the outflows",
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
        "# Abandonment / Quenching / Exhaustion Glossary",
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
        "# Abandonment / Quenching / Exhaustion Contrast Sheet",
        "",
        f"- `{terms['pariyutthana']['term']}`: `{terms['pariyutthana']['preferred_translation']}`",
        f"- `{terms['pahana']['term']}`: `{terms['pahana']['preferred_translation']}`",
        f"- `{terms['viraga']['term']}`: `{terms['viraga']['preferred_translation']}`",
        f"- `{terms['vossagga']['term']}`: `{terms['vossagga']['preferred_translation']}`",
        f"- `{terms['nirodha']['term']}`: `{terms['nirodha']['preferred_translation']}`",
        f"- `{terms['khaya']['term']}`: `{terms['khaya']['preferred_translation']}`",
        "",
        "## Keep Distinct",
        "",
        "- `pariyuṭṭhāna` is manifestation language, not latent residue language.",
        "- `pahāna` is task-language: putting away, not yet quenching or exhaustion.",
        "- `virāga` is fading or cooling, not just another word for abandoning.",
        "- `vossagga` is relinquishment, not a slogan and not identical with quenching.",
        "- `nirodha` remains `quenching`, not generic cessation by default.",
        "- `khaya` is wearing away or exhaustion, not just another way to say `nirodha`.",
    ]
    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "abandonment-sequence-glossary.md": render_glossary(terms),
        OUTPUT_DIR / "abandonment-sequence-contrast-sheet.md": render_contrast_sheet(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + "\n", encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    common.print_text_report("Abandonment / Quenching / Exhaustion Cluster Report", report)


def main() -> int:
    return common.run_cli(sys.modules[__name__])


if __name__ == "__main__":
    sys.exit(main())

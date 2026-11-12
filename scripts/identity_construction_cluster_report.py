#!/usr/bin/env python3
"""Audit and generate translator-facing outputs for the identity-construction cluster."""

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
    "sakkaya",
    "ditthi",
    "ditthupadana",
    "attavadupadana",
    "mana",
    "asmimana",
    "upadana",
]

SUPPORTING_TERMS = [
    "sakkaya-ditthi",
    "pancupadanakkhandha",
    "upadanakkhandha",
]

FORMULA_TERMS = [
    "katamo-ca-bhikkhave-sakkayo",
    "sakkayassa-samudayo",
    "sakkayassa-nirodho",
]


def render_mismatch_warnings(terms: dict[str, dict[str, object]]) -> list[str]:
    warnings: list[str] = []
    expected = {
        "sakkaya": "identity",
        "ditthi": "view",
        "ditthupadana": "taking views personally",
        "attavadupadana": "taking self-doctrine personally",
        "mana": "conceit",
        "asmimana": "conceit 'I am'",
        "upadana": "taking personally",
        "pancupadanakkhandha": "five clung-to heaps",
        "upadanakkhandha": "clung-to heap",
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
        "# Identity-Construction Cluster Glossary",
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
        "# Identity-Construction Contrast Sheet",
        "",
        f"- `{terms['ditthi']['term']}`: `{terms['ditthi']['preferred_translation']}`",
        f"- `{terms['ditthupadana']['term']}`: `{terms['ditthupadana']['preferred_translation']}`",
        f"- `{terms['attavadupadana']['term']}`: `{terms['attavadupadana']['preferred_translation']}`",
        f"- `{terms['sakkaya']['term']}`: `{terms['sakkaya']['preferred_translation']}`",
        f"- `{terms['sakkaya-ditthi']['term']}`: `{terms['sakkaya-ditthi']['preferred_translation']}`",
        f"- `{terms['mana']['term']}`: `{terms['mana']['preferred_translation']}`",
        f"- `{terms['asmimana']['term']}`: `{terms['asmimana']['preferred_translation']}`",
        "",
        "## Keep Distinct",
        "",
        "- `diṭṭhi` is view; `diṭṭhupādāna` is appropriating views.",
        "- `attavādupādāna` is narrower than `diṭṭhupādāna`: the content is specifically self-doctrine.",
        "- `sakkāya-diṭṭhi` is a view; `asmimāna` is residual conceit, not a view.",
        "- `māna` is the broader measuring family; `asmimāna` is one specific residue within it.",
    ]
    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "identity-construction-cluster-glossary.md": render_glossary(terms),
        OUTPUT_DIR / "identity-construction-contrast-sheet.md": render_contrast_sheet(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + "\n", encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    common.print_text_report("Identity-Construction Cluster Report", report)


def main() -> int:
    return common.run_cli(sys.modules[__name__])


if __name__ == "__main__":
    sys.exit(main())

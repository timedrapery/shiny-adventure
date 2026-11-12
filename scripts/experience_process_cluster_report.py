#!/usr/bin/env python3
"""Audit and generate translator-facing outputs for the experience / process cluster."""

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
    "phassa",
    "vedana",
    "sanna",
    "cetana",
    "vinnana",
]

SUPPORTING_TERMS = [
    "phassapaccaya-vedana",
    "vedanakkhandha",
    "sannakkhandha",
    "vinnanakkhandha",
    "manosancetana-ahara",
]

FORMULA_TERMS: list[str] = []


def render_mismatch_warnings(terms: dict[str, dict[str, object]]) -> list[str]:
    warnings: list[str] = []
    expected = {
        "phassa": "contact",
        "vedana": "felt experience",
        "sanna": "recognition",
        "cetana": "intention",
        "vinnana": "knowing",
        "phassapaccaya-vedana": "with contact as condition, felt experience",
        "vedanakkhandha": "felt-experience heap",
        "sannakkhandha": "recognition heap",
        "vinnanakkhandha": "knowing heap",
        "manosancetana-ahara": "mental-intention nutriment",
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
        "# Experience / Process Cluster Glossary",
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
        "# Experience / Process Contrast Sheet",
        "",
        f"- `{terms['phassa']['term']}`: `{terms['phassa']['preferred_translation']}`",
        f"- `{terms['vedana']['term']}`: `{terms['vedana']['preferred_translation']}`",
        f"- `{terms['sanna']['term']}`: `{terms['sanna']['preferred_translation']}`",
        f"- `{terms['cetana']['term']}`: `{terms['cetana']['preferred_translation']}`",
        f"- `{terms['vinnana']['term']}`: `{terms['vinnana']['preferred_translation']}`",
        "",
        "## Keep Distinct",
        "",
        "- `phassa` is the contact event, not the feeling that follows and not mere physical touch.",
        "- `vedanā` is felt experience, not emotion or mood.",
        "- `saññā` is recognition, not discursive thought, concept, or memory.",
        "- `cetanā` is intention, not desire, willpower, or metaphysical free will.",
        "- `viññāṇa` is conditioned knowing, not self, soul, sentience, or pure awareness.",
        "",
        "## Formula Guardrail",
        "",
        f"- `{terms['phassapaccaya-vedana']['term']}` -> `{terms['phassapaccaya-vedana']['preferred_translation']}`",
    ]
    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "experience-process-cluster-glossary.md": render_glossary(terms),
        OUTPUT_DIR / "experience-process-contrast-sheet.md": render_contrast_sheet(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + "\n", encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    common.print_text_report("Experience / Process Cluster Report", report)


def main() -> int:
    return common.run_cli(sys.modules[__name__])


if __name__ == "__main__":
    sys.exit(main())

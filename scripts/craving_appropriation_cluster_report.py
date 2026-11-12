#!/usr/bin/env python3
"""Audit and generate translator-facing outputs for the craving / appropriation cluster."""

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
    "upadana",
    "tanha",
    "chanda",
    "raga",
    "nandi",
]

SUPPORTING_TERMS = [
    "kamacchanda",
    "kama-tanha",
    "kama-raga",
    "chandaraga",
    "chanda-iddhipada",
    "upadanakkhandha",
    "pancupadanakkhandha",
]

FORMULA_TERMS = [
    "vedanapaccaya-tanha",
    "tanhapaccaya-upadana",
    "ya-tanha-ponobbhavika",
    "nandiraga-sahagata",
]


def render_mismatch_warnings(terms: dict[str, dict[str, object]]) -> list[str]:
    warnings: list[str] = []
    expected = {
        "upadana": "taking personally",
        "tanha": "ignorant wanting",
        "chanda": "desire",
        "raga": "passion",
        "nandi": "relishing",
        "kamacchanda": "sensual desire",
        "kama-tanha": "ignorant wanting for sensuality",
        "kama-raga": "passion for sensuality",
        "upadanakkhandha": "clung-to heap",
        "pancupadanakkhandha": "five clung-to heaps",
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
        "# Craving / Appropriation Cluster Glossary",
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
        "# Craving / Appropriation Contrast Sheet",
        "",
        f"- `{terms['chanda']['term']}`: `{terms['chanda']['preferred_translation']}`",
        f"- `{terms['tanha']['term']}`: `{terms['tanha']['preferred_translation']}`",
        f"- `{terms['raga']['term']}`: `{terms['raga']['preferred_translation']}`",
        f"- `{terms['nandi']['term']}`: `{terms['nandi']['preferred_translation']}`",
        f"- `{terms['upadana']['term']}`: `{terms['upadana']['preferred_translation']}`",
        "",
        "## Keep Distinct",
        "",
        "- `chanda` is broader desire or directed interest and can be wholesome.",
        "- `taṇhā` is thirsty ignorant wanting and should not default to generic desire-language.",
        "- `rāga` is passion or affective coloring, not merely wanting.",
        "- `nandī` is relishing or delighting, not generic happiness, pleasure, or wholesome joy.",
        "- `upādāna` is appropriation or taking personally, not a vague emotional attachment label.",
        "",
        "## Formula Guardrails",
        "",
        f"- `{terms['vedanapaccaya-tanha']['term']}` -> `{terms['vedanapaccaya-tanha']['preferred_translation']}`",
        f"- `{terms['tanhapaccaya-upadana']['term']}` -> `{terms['tanhapaccaya-upadana']['preferred_translation']}`",
        f"- `{terms['nandiraga-sahagata']['term']}` -> `{terms['nandiraga-sahagata']['preferred_translation']}`",
        f"- `{terms['ya-tanha-ponobbhavika']['term']}` -> `{terms['ya-tanha-ponobbhavika']['preferred_translation']}`",
        "",
        "## Fixed Override Reminder",
        "",
        f"- `{terms['upadana']['term']}` stays `{terms['upadana']['preferred_translation']}` as a headword, but `{terms['upadanakkhandha']['term']}` and `{terms['pancupadanakkhandha']['term']}` remain fixed overrides.",
    ]
    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "craving-appropriation-cluster-glossary.md": render_glossary(terms),
        OUTPUT_DIR / "craving-appropriation-contrast-sheet.md": render_contrast_sheet(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + "\n", encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    common.print_text_report("Craving / Appropriation Cluster Report", report)


def main() -> int:
    return common.run_cli(sys.modules[__name__])


if __name__ == "__main__":
    sys.exit(main())

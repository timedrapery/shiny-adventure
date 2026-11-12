#!/usr/bin/env python3
"""Audit and generate translator-facing outputs for the knowledge / seeing / understanding cluster."""

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
    "nana",
    "vijja",
    "panna",
    "dassana",
    "abhinna",
    "parinna",
]

SUPPORTING_TERMS = [
    "avijja",
    "ditthi",
    "samma-ditthi",
    "sampajanna",
    "nanadassana",
    "vimutti-nanadassana",
    "yathabhuta-nanadassana",
    "pannavimutti",
    "amoha",
]

FORMULA_TERMS: list[str] = []


def render_mismatch_warnings(terms: dict[str, dict[str, object]]) -> list[str]:
    warnings: list[str] = []
    expected = {
        "nana": "knowledge",
        "vijja": "clear knowledge",
        "panna": "discernment",
        "dassana": "seeing",
        "abhinna": "higher knowing",
        "parinna": "full understanding",
        "sampajanna": "clear knowing",
        "nanadassana": "knowing and seeing",
        "vimutti-nanadassana": "knowing and seeing of release",
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
        "# Knowledge / Seeing / Understanding Glossary",
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
        "# Knowledge / Seeing / Understanding Contrast Sheet",
        "",
        f"- `{terms['nana']['term']}`: `{terms['nana']['preferred_translation']}`",
        f"- `{terms['vijja']['term']}`: `{terms['vijja']['preferred_translation']}`",
        f"- `{terms['panna']['term']}`: `{terms['panna']['preferred_translation']}`",
        f"- `{terms['dassana']['term']}`: `{terms['dassana']['preferred_translation']}`",
        f"- `{terms['abhinna']['term']}`: `{terms['abhinna']['preferred_translation']}`",
        f"- `{terms['parinna']['term']}`: `{terms['parinna']['preferred_translation']}`",
        "",
        "## Keep Distinct",
        "",
        "- `ñāṇa` is broader knowing-language and can be result-facing or formula-facing.",
        "- `vijjā` is clearer liberating knowledge in contrast to `avijjā`.",
        "- `paññā` is discernment as a cultivated capacity, not generic wisdom-talk.",
        "- `dassana` is the seeing side, not mystical vision and not just another word for `ñāṇa`.",
        "- `abhiññā` is higher knowing, not occult spectacle and not just `insight`.",
        "- `pariññā` is full understanding, not ordinary understanding.",
        "- `diṭṭhi` remains view, not knowledge.",
        "- `sati` remains remembering, and `sampajañña` remains practice-side clear knowing.",
        "",
        "## Source-Facing Guardrails",
        "",
        "- Preserve OSF and Dhammarato anti-mystification pressure: keep the cluster practical and release-facing.",
        "- Preserve Punnaji's practical help where useful without letting introspective explanation replace the governed defaults.",
        "- Preserve Hillside / Ñāṇamoli help where useful: context, restraint, and whole-situation awareness can sharpen explanatory notes without turning the family into imported technical jargon.",
        "",
        "## Formula Guardrails",
        "",
        f"- `{terms['nanadassana']['term']}` -> `{terms['nanadassana']['preferred_translation']}`",
        f"- `{terms['yathabhuta-nanadassana']['term']}` -> `{terms['yathabhuta-nanadassana']['preferred_translation']}`",
        f"- `{terms['vimutti-nanadassana']['term']}` -> `{terms['vimutti-nanadassana']['preferred_translation']}`",
    ]
    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "knowledge-cluster-glossary.md": render_glossary(terms),
        OUTPUT_DIR / "knowledge-cluster-contrast-sheet.md": render_contrast_sheet(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + "\n", encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    common.print_text_report("Knowledge / Seeing / Understanding Cluster Report", report)


def main() -> int:
    return common.run_cli(sys.modules[__name__])


if __name__ == "__main__":
    sys.exit(main())

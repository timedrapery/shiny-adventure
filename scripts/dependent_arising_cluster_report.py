#!/usr/bin/env python3
"""Audit and generate translator-facing outputs for the dependent-arising cluster."""

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
    "avijja",
    "sankhara",
    "vinnana",
    "namarupa",
    "salayatana",
    "phassa",
    "vedana",
    "tanha",
    "upadana",
    "bhava",
    "jati",
    "jaramarana",
    "paccaya",
    "nirodha",
    "paticcasamuppada",
    "idappaccayata",
]

CONDITIONALITY_FORMULAS = [
    "imasmim-sati-idam-hoti",
    "imassuppada-idam-uppajjati",
    "imasmim-asati-idam-na-hoti",
    "imassa-nirodha-idam-nirujjhati",
]

CHAIN_FORMULAS = [
    "avijjapaccaya-sankhara",
    "sankharapaccaya-vinnana",
    "vinnanapaccaya-namarupa",
    "namarupapaccaya-salayatanam",
    "salayatanapaccaya-phasso",
    "phassapaccaya-vedana",
    "vedanapaccaya-tanha",
    "tanhapaccaya-upadana",
    "upadanapaccaya-bhavo",
    "bhavapaccaya-jati",
    "jatipaccaya-jaramaranam",
]

FORWARD_LINK_COMPOUNDS = [
    "avijja-paccaya",
    "sankhara-paccaya",
    "vinnana-paccaya",
    "namarupa-paccaya",
    "salayatana-paccaya",
    "phassa-paccaya",
    "vedana-paccaya",
    "tanha-paccaya",
    "upadana-paccaya",
    "bhava-paccaya",
    "jati-paccaya",
]

REVERSE_LINK_COMPOUNDS = [
    "avijja-nirodha",
    "sankhara-nirodha",
    "vinnana-nirodha",
    "namarupa-nirodha",
    "salayatana-nirodha",
    "phassa-nirodha",
    "vedana-nirodha",
    "tanha-nirodha",
    "upadana-nirodha",
    "bhava-nirodha",
    "jati-nirodha",
]


def thin_link_compounds(terms: dict[str, dict[str, object]], stems: list[str]) -> list[str]:
    thin: list[str] = []
    for stem in stems:
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        examples = data.get("example_phrases")
        policy = data.get("translation_policy")
        related = data.get("related_terms")
        if not isinstance(examples, list) or not examples or not isinstance(policy, dict) or not isinstance(related, list):
            thin.append(stem)
    return thin


def build_report(terms: dict[str, dict[str, object]]) -> dict[str, object]:
    formula_terms = CONDITIONALITY_FORMULAS + CHAIN_FORMULAS
    return {
        "summary": {
            "headwords_present": len(HEADWORD_TERMS) - len(missing_terms(terms, HEADWORD_TERMS)),
            "headwords_expected": len(HEADWORD_TERMS),
            "formula_records_present": len(formula_terms) - len(missing_terms(terms, formula_terms)),
            "formula_records_expected": len(formula_terms),
        },
        "errors": {
            "missing_headwords": missing_terms(terms, HEADWORD_TERMS),
            "missing_formula_records": missing_terms(terms, formula_terms),
            "headword_example_source_gaps": example_source_gaps(terms, HEADWORD_TERMS),
            "formula_example_source_gaps": example_source_gaps(terms, formula_terms),
        },
        "warnings": {
            "headwords_with_thin_authority_basis": weak_authority_terms(terms, HEADWORD_TERMS),
            "forward_link_compounds_still_thin": thin_link_compounds(terms, FORWARD_LINK_COMPOUNDS),
            "reverse_link_compounds_still_thin": thin_link_compounds(terms, REVERSE_LINK_COMPOUNDS),
        },
    }


def render_glossary(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Dependent Arising Cluster Glossary",
        "",
        "| Pāli | Default | Allowed alternates | Discouraged |",
        "| --- | --- | --- | --- |",
    ]
    for stem in HEADWORD_TERMS:
        data = terms[stem]
        alts = ", ".join(data.get("alternative_translations", []))
        discouraged = ", ".join(data.get("discouraged_translations", []))
        lines.append(
            f"| {data.get('term')} | {data.get('preferred_translation')} | {alts or '-'} | {discouraged or '-'} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_formula_sheet(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Dependent Arising Formula Sheet",
        "",
        "## Conditionality Lines",
        "",
    ]
    for stem in CONDITIONALITY_FORMULAS:
        data = terms[stem]
        lines.append(f"- `{data.get('term')}` -> {data.get('preferred_translation')}")
    lines.extend(["", "## Forward Chain", ""])
    for stem in CHAIN_FORMULAS:
        data = terms[stem]
        lines.append(f"- `{data.get('term')}` -> {data.get('preferred_translation')}")
    lines.extend(
        [
            "",
            "## Reverse Quenching Guide",
            "",
            "- Use `imassa nirodhā idaṃ nirujjhati` as the governing whole-line model for the quenching side.",
            "- Keep `nirodha` as `quenching` by default across the linked `-nirodha` family unless a controlled local alternate is already governing the passage.",
        ]
    )
    return "\n".join(lines)


def render_translator_brief(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Dependent Arising Translator Brief",
        "",
        "## Cluster Defaults",
        "",
        f"- Keep `{terms['paticcasamuppada']['term']}` as `{terms['paticcasamuppada']['preferred_translation']}`.",
        f"- Keep `{terms['paccaya']['term']}` as `{terms['paccaya']['preferred_translation']}` and preserve the standard frame `with X as condition, Y`.",
        f"- Keep `{terms['nirodha']['term']}` as `{terms['nirodha']['preferred_translation']}` by default in the conditionality family.",
        f"- Keep `{terms['jati']['term']}` as `{terms['jati']['preferred_translation']}` by default in the chain; use `rebirth` only when the local frame clearly requires it.",
        "",
        "## Practical Pivots",
        "",
        f"- `{terms['phassa']['term']}` -> `{terms['phassa']['preferred_translation']}` should stay distinct from `{terms['vedana']['term']}` -> `{terms['vedana']['preferred_translation']}`.",
        f"- `{terms['vedana']['term']}` -> `{terms['vedana']['preferred_translation']}` and `{terms['tanha']['term']}` -> `{terms['tanha']['preferred_translation']}` form a key practical pivot; do not psychologize or soften it.",
        f"- `{terms['upadana']['term']}` -> `{terms['upadana']['preferred_translation']}` should preserve appropriation rather than generic attachment language.",
        "",
        "## Formula Discipline",
        "",
        "- Prefer the dedicated formula records for the four conditionality lines and the eleven forward-link lines.",
        "- Do not rotate among `cause`, `condition`, `quenching`, `cessation`, `birth`, and `rebirth` without a recorded local reason.",
    ]
    return "\n".join(lines)


def render_consistency_report(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Dependent Arising Consistency Report",
        "",
        "## Headword Defaults",
        "",
    ]
    for stem in HEADWORD_TERMS:
        data = terms[stem]
        lines.append(
            f"- `{data.get('term')}`: default `{data.get('preferred_translation')}`; alternates `{', '.join(data.get('alternative_translations', []))}`; discouraged `{', '.join(data.get('discouraged_translations', []))}`"
        )
    lines.extend(["", "## Formula Overrides", ""])
    for stem in CHAIN_FORMULAS + CONDITIONALITY_FORMULAS:
        data = terms[stem]
        lines.append(f"- `{data.get('term')}`: `{data.get('preferred_translation')}`")
    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "dependent-arising-cluster-glossary.md": render_glossary(terms),
        OUTPUT_DIR / "dependent-arising-formula-sheet.md": render_formula_sheet(terms),
        OUTPUT_DIR / "dependent-arising-translator-brief.md": render_translator_brief(terms),
        OUTPUT_DIR / "dependent-arising-consistency-report.md": render_consistency_report(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + "\n", encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    common.print_text_report("Dependent Arising Cluster Report", report)


def main() -> int:
    return common.run_cli(sys.modules[__name__])


if __name__ == "__main__":
    sys.exit(main())

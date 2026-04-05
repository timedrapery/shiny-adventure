#!/usr/bin/env python3
"""Audit and generate translator-facing outputs for the dependent-arising cluster."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from scripts.text_utils import safe_text
    from scripts.term_store import iter_term_files
except ModuleNotFoundError:
    from text_utils import safe_text
    from term_store import iter_term_files


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


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_terms(terms_dir: Path = TERMS_DIR) -> dict[str, dict[str, object]]:
    terms: dict[str, dict[str, object]] = {}
    for path in iter_term_files(terms_dir):
        data = load_json(path)
        if isinstance(data, dict):
            terms[path.stem] = data
    return terms


def missing_terms(terms: dict[str, dict[str, object]], stems: list[str]) -> list[str]:
    return [stem for stem in stems if stem not in terms]


def example_source_gaps(terms: dict[str, dict[str, object]], stems: list[str]) -> list[str]:
    gaps: list[str] = []
    for stem in stems:
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        examples = data.get("example_phrases")
        if not isinstance(examples, list) or not examples:
            gaps.append(stem)
            continue
        if any(not isinstance(item, dict) or not item.get("source") for item in examples):
            gaps.append(stem)
    return gaps


def weak_authority_terms(terms: dict[str, dict[str, object]], stems: list[str]) -> list[str]:
    weak: list[str] = []
    for stem in stems:
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        authority = data.get("authority_basis")
        if not isinstance(authority, list) or len(authority) < 2:
            weak.append(stem)
    return weak


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
    summary = report["summary"]
    errors = report["errors"]
    warnings = report["warnings"]

    print("Dependent Arising Cluster Report")
    print(
        f"- Headwords: {summary['headwords_present']} / {summary['headwords_expected']}"
    )
    print(
        f"- Formula records: {summary['formula_records_present']} / {summary['formula_records_expected']}"
    )
    print()

    print("Errors")
    for key, items in errors.items():
        if items:
            print(f"- {safe_text(key)}: {', '.join(safe_text(item) for item in items)}")
        else:
            print(f"- {safe_text(key)}: none")
    print()

    print("Warnings")
    for key, items in warnings.items():
        if items:
            print(f"- {safe_text(key)}: {', '.join(safe_text(item) for item in items)}")
        else:
            print(f"- {safe_text(key)}: none")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--strict", action="store_true", help="Fail if the report has errors.")
    parser.add_argument("--write-docs", action="store_true", help="Write generated docs to docs/generated.")
    args = parser.parse_args()

    if not TERMS_DIR.exists():
        print(f"ERROR: Terms directory not found: {TERMS_DIR}")
        return 1

    terms = load_terms()
    report = build_report(terms)

    if args.write_docs:
        write_outputs(terms)

    if args.format == "json":
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print_text_report(report)

    if args.strict and any(report["errors"].values()):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

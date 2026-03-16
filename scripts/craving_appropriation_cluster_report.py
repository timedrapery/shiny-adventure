#!/usr/bin/env python3
"""Audit and generate translator-facing outputs for the craving / appropriation cluster."""

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


def render_mismatch_warnings(terms: dict[str, dict[str, object]]) -> list[str]:
    warnings: list[str] = []
    expected = {
        "upadana": "taking personally",
        "tanha": "ignorant wanting",
        "chanda": "desire",
        "raga": "passion",
        "nandi": "relishing",
        "kamacchanda": "sensual distraction",
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
    for stem in HEADWORD_TERMS + ["kamacchanda", "kama-tanha", "kama-raga", "upadanakkhandha", "pancupadanakkhandha"]:
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
    summary = report["summary"]
    errors = report["errors"]
    warnings = report["warnings"]

    print("Craving / Appropriation Cluster Report")
    print(f"- Headwords: {summary['headwords_present']} / {summary['headwords_expected']}")
    print(f"- Supporting terms: {summary['supporting_terms_present']} / {summary['supporting_terms_expected']}")
    print(f"- Formula records: {summary['formula_records_present']} / {summary['formula_records_expected']}")
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
    parser.add_argument("--strict", action="store_true", help="Fail on report errors.")
    parser.add_argument("--write-docs", action="store_true", help="Generate Markdown outputs in docs/generated.")
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

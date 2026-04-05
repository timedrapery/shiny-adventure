#!/usr/bin/env python3
"""Audit and generate translator-facing outputs for the five-heaps cluster."""

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
    "khandha",
    "rupa",
    "vedana",
    "sanna",
    "sankhara",
    "vinnana",
    "upadana",
    "sakkaya",
    "sakkaya-ditthi",
    "atta",
    "anatta",
]

COLLECTIVE_TERMS = [
    "pancakkhandha",
    "pancupadanakkhandha",
    "rupakkhandha",
    "vedanakkhandha",
    "sannakkhandha",
    "sankharakkhandha",
    "vinnanakkhandha",
]

FORMULA_TERMS = [
    "pancime-bhikkhave-khandha",
    "pancime-bhikkhave-upadanakkhandha",
    "yam-kinci-rupam-vedana-sanna-sankhara-vinnanam",
    "katamo-ca-bhikkhave-sakkayo",
    "bharo-have-pancakkhandha",
    "pancupadanakkhandhesu-assado-adinavo-nissaranam",
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


def thin_collective_terms(terms: dict[str, dict[str, object]]) -> list[str]:
    thin: list[str] = []
    for stem in COLLECTIVE_TERMS:
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        examples = data.get("example_phrases")
        policy = data.get("translation_policy")
        related = data.get("related_terms")
        if not isinstance(examples, list) or not examples or not isinstance(policy, dict) or not isinstance(related, list):
            thin.append(stem)
    return thin


def inconsistent_clung_to_heap_terms(terms: dict[str, dict[str, object]]) -> list[str]:
    flagged: list[str] = []
    expected = {
        "pancupadanakkhandha": "five clung-to heaps",
        "pancime-bhikkhave-upadanakkhandha": "and what, bhikkhus, are the five clung-to heaps",
        "katamo-ca-bhikkhave-sakkayo": "and what, bhikkhus, is identity, the five clung-to heaps",
        "pancupadanakkhandhesu-assado-adinavo-nissaranam": "the gratification, danger, and escape in the five clung-to heaps",
    }
    for stem, expected_rendering in expected.items():
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        preferred = data.get("preferred_translation")
        if preferred != expected_rendering:
            flagged.append(stem)
    return flagged


def build_report(terms: dict[str, dict[str, object]]) -> dict[str, object]:
    all_priority = HEADWORD_TERMS + COLLECTIVE_TERMS + FORMULA_TERMS
    return {
        "summary": {
            "headwords_present": len(HEADWORD_TERMS) - len(missing_terms(terms, HEADWORD_TERMS)),
            "headwords_expected": len(HEADWORD_TERMS),
            "collective_terms_present": len(COLLECTIVE_TERMS) - len(missing_terms(terms, COLLECTIVE_TERMS)),
            "collective_terms_expected": len(COLLECTIVE_TERMS),
            "formula_records_present": len(FORMULA_TERMS) - len(missing_terms(terms, FORMULA_TERMS)),
            "formula_records_expected": len(FORMULA_TERMS),
        },
        "errors": {
            "missing_headwords": missing_terms(terms, HEADWORD_TERMS),
            "missing_collective_terms": missing_terms(terms, COLLECTIVE_TERMS),
            "missing_formula_records": missing_terms(terms, FORMULA_TERMS),
            "cluster_example_source_gaps": example_source_gaps(terms, all_priority),
        },
        "warnings": {
            "headwords_with_thin_authority_basis": weak_authority_terms(terms, HEADWORD_TERMS),
            "collective_terms_still_thin": thin_collective_terms(terms),
            "inconsistent_clung_to_heap_renderings": inconsistent_clung_to_heap_terms(terms),
        },
    }


def render_glossary(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Five Heaps Cluster Glossary",
        "",
        "| Pali | Default | Allowed alternates | Discouraged |",
        "| --- | --- | --- | --- |",
    ]
    for stem in HEADWORD_TERMS + ["pancakkhandha", "pancupadanakkhandha"]:
        data = terms[stem]
        alts = ", ".join(data.get("alternative_translations", []))
        discouraged = ", ".join(data.get("discouraged_translations", []))
        lines.append(
            f"| {data.get('term')} | {data.get('preferred_translation')} | {alts or '-'} | {discouraged or '-'} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_consistency_sheet(terms: dict[str, dict[str, object]]) -> str:
    members = [
        "rupa",
        "vedana",
        "sanna",
        "sankhara",
        "vinnana",
        "rupakkhandha",
        "vedanakkhandha",
        "sannakkhandha",
        "sankharakkhandha",
        "vinnanakkhandha",
    ]
    lines = [
        "# Five Heaps Consistency Sheet",
        "",
        "## Headwords",
        "",
    ]
    for stem in members[:5]:
        data = terms[stem]
        lines.append(f"- `{data.get('term')}`: `{data.get('preferred_translation')}`")
    lines.extend(["", "## Constituent Heap Compounds", ""])
    for stem in members[5:]:
        data = terms[stem]
        lines.append(f"- `{data.get('term')}`: `{data.get('preferred_translation')}`")
    return "\n".join(lines)


def render_formula_sheet(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Five Heaps Formula Sheet",
        "",
    ]
    for stem in FORMULA_TERMS:
        data = terms[stem]
        lines.append(f"- `{data.get('term')}` -> {data.get('preferred_translation')}")
    return "\n".join(lines)


def render_translator_brief(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Heaps vs. Clung-To Heaps Brief",
        "",
        "## Defaults",
        "",
        f"- Keep `{terms['khandha']['term']}` as `{terms['khandha']['preferred_translation']}`.",
        f"- Keep `{terms['pancakkhandha']['term']}` as `{terms['pancakkhandha']['preferred_translation']}`.",
        f"- Keep `{terms['pancupadanakkhandha']['term']}` as `{terms['pancupadanakkhandha']['preferred_translation']}`.",
        f"- Keep `{terms['sakkaya']['term']}` as `{terms['sakkaya']['preferred_translation']}` and read it through the five clung-to heaps.",
        "",
        "## Practical Distinctions",
        "",
        "- Do not flatten `pañcakkhandhā` and `pañcupādānakkhandhā` into the same English.",
        "- In heap context, keep `saṅkhārā` as `putting-together activities` rather than importing the dependent-arising link or `volitional formations` by habit.",
        "- In heap context, keep `viññāṇa` as `knowing` unless comparative prose clearly calls for `consciousness`.",
        "- Use the dedicated phrase records for the standard headings, the `yaṃ kiñci ...` pattern, the burden line, and the `sakkāya` equation.",
    ]
    return "\n".join(lines)


def render_cross_cluster_note(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Five Heaps Cross-Cluster Note",
        "",
        f"- `{terms['upadana']['term']}` stays `{terms['upadana']['preferred_translation']}` as a headword, but `{terms['pancupadanakkhandha']['term']}` is governed as `{terms['pancupadanakkhandha']['preferred_translation']}` as a fixed whole expression.",
        f"- `{terms['sankhara']['term']}` keeps a heap-context override as `{terms['sankharakkhandha']['preferred_translation']}` while preserving its dependent-arising policy elsewhere.",
        f"- `{terms['vinnana']['term']}` stays `{terms['vinnana']['preferred_translation']}` across both heap and dependent-arising contexts; use the formula records to keep the voice stable.",
        f"- `{terms['anatta']['term']}` and `{terms['atta']['term']}` are tied to the heap family through the standard not-self and self-view formulas rather than through abstract metaphysical claims.",
    ]
    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "five-heaps-cluster-glossary.md": render_glossary(terms),
        OUTPUT_DIR / "five-heaps-consistency-sheet.md": render_consistency_sheet(terms),
        OUTPUT_DIR / "five-heaps-formula-sheet.md": render_formula_sheet(terms),
        OUTPUT_DIR / "heaps-vs-clung-to-heaps-brief.md": render_translator_brief(terms),
        OUTPUT_DIR / "five-heaps-cross-cluster-note.md": render_cross_cluster_note(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + "\n", encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    summary = report["summary"]
    errors = report["errors"]
    warnings = report["warnings"]

    print("Five Heaps Cluster Report")
    print(f"- Headwords: {summary['headwords_present']} / {summary['headwords_expected']}")
    print(f"- Collective terms: {summary['collective_terms_present']} / {summary['collective_terms_expected']}")
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

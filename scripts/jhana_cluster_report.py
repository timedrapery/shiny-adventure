#!/usr/bin/env python3
"""Audit and generate translator-facing outputs for the jhana core cluster."""

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
    "jhana",
    "jhayati",
    "samadhi",
    "samma-samadhi",
    "vitakka",
    "vicara",
    "ekaggata",
    "piti",
    "sukha",
    "nivarana",
    "bhavana",
]

SEQUENCE_TERMS = [
    "pathama-jhana",
    "dutiya-jhana",
    "tatiya-jhana",
    "catuttha-jhana",
]

FORMULA_TERMS = [
    "vivekaja-piti-sukha",
    "avitakka-avicara",
    "cetaso-ekodibhava",
    "ajjhatta-sampasadana",
    "samadhija-piti-sukha",
    "upekkha-sukha",
    "upekkha-satiparisuddha",
    "upekkha-satiparisuddhi",
]

EXPECTED_PREFERRED_TRANSLATIONS = {
    "jhana": "mental theme",
    "jhayati": "think like this",
    "ekaggata": "directness",
    "samadhi": "mental composure",
    "samma-samadhi": "right mental composure",
    "pathama-jhana": "first mental theme",
    "dutiya-jhana": "second mental theme",
    "tatiya-jhana": "third mental theme",
    "catuttha-jhana": "fourth mental theme",
}


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


def thin_terms(terms: dict[str, dict[str, object]], stems: list[str]) -> list[str]:
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


def preferred_rendering_mismatches(terms: dict[str, dict[str, object]]) -> list[str]:
    mismatches: list[str] = []
    for stem, expected in EXPECTED_PREFERRED_TRANSLATIONS.items():
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        actual = data.get("preferred_translation")
        if actual != expected:
            mismatches.append(f"{stem}: expected '{expected}', found '{actual}'")
    return mismatches


def samma_samadhi_identity_missing(terms: dict[str, dict[str, object]]) -> list[str]:
    data = terms.get("samma-samadhi")
    if not isinstance(data, dict):
        return []
    blob = json.dumps(data, ensure_ascii=False).casefold()
    if ("jhāna" not in blob and "jhana" not in blob) or any(
        token not in blob for token in ("first", "second", "third", "fourth")
    ):
        return ["samma-samadhi"]
    return []


def build_report(terms: dict[str, dict[str, object]]) -> dict[str, object]:
    all_priority = HEADWORD_TERMS + SEQUENCE_TERMS + FORMULA_TERMS
    return {
        "summary": {
            "headwords_present": len(HEADWORD_TERMS) - len(missing_terms(terms, HEADWORD_TERMS)),
            "headwords_expected": len(HEADWORD_TERMS),
            "sequence_terms_present": len(SEQUENCE_TERMS) - len(missing_terms(terms, SEQUENCE_TERMS)),
            "sequence_terms_expected": len(SEQUENCE_TERMS),
            "formula_terms_present": len(FORMULA_TERMS) - len(missing_terms(terms, FORMULA_TERMS)),
            "formula_terms_expected": len(FORMULA_TERMS),
        },
        "errors": {
            "missing_headwords": missing_terms(terms, HEADWORD_TERMS),
            "missing_sequence_terms": missing_terms(terms, SEQUENCE_TERMS),
            "missing_formula_terms": missing_terms(terms, FORMULA_TERMS),
            "cluster_example_source_gaps": example_source_gaps(terms, all_priority),
        },
        "warnings": {
            "headwords_with_thin_authority_basis": weak_authority_terms(terms, HEADWORD_TERMS),
            "sequence_terms_still_thin": thin_terms(terms, SEQUENCE_TERMS),
            "formula_terms_still_thin": thin_terms(terms, FORMULA_TERMS),
            "preferred_rendering_mismatches": preferred_rendering_mismatches(terms),
            "samma_samadhi_identity_missing": samma_samadhi_identity_missing(terms),
        },
    }


def render_glossary(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Jhana Cluster Glossary",
        "",
        "| Pali | Default | Allowed alternates | Discouraged |",
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


def render_sequence_sheet(terms: dict[str, dict[str, object]]) -> str:
    linked_formulas = {
        "pathama-jhana": ["vivekaja-piti-sukha"],
        "dutiya-jhana": ["avitakka-avicara", "ajjhatta-sampasadana", "cetaso-ekodibhava", "samadhija-piti-sukha"],
        "tatiya-jhana": ["upekkha-sukha"],
        "catuttha-jhana": ["upekkha-satiparisuddha", "upekkha-satiparisuddhi"],
    }
    lines = [
        "# Jhana Sequence Sheet",
        "",
        f"- `{terms['samma-samadhi']['term']}` is governed in this repository as the first, second, third, and fourth `{terms['jhana']['term']}`.",
        f"- Keep `{terms['jhana']['term']}` as `{terms['jhana']['preferred_translation']}` across the fourfold sequence unless a controlled technical reason requires the Pali.",
        "",
    ]
    for stem in SEQUENCE_TERMS:
        data = terms[stem]
        lines.append(f"## {data.get('term')}")
        lines.append("")
        lines.append(f"- Default: `{data.get('preferred_translation')}`")
        lines.append(f"- Notes: {data.get('definition')}")
        formulas = linked_formulas.get(stem, [])
        if formulas:
            formula_text = ", ".join(
                f"`{terms[item].get('term')}` -> {terms[item].get('preferred_translation')}"
                for item in formulas
            )
            lines.append(f"- Linked formulas: {formula_text}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_path_brief(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Jhana Path Brief",
        "",
        "## Path Rule",
        "",
        f"- `{terms['samma-samadhi']['term']}` is the first, second, third, and fourth `{terms['jhana']['term']}`.",
        f"- Keep `{terms['samma-samadhi']['preferred_translation']}` as the default rendering for the path factor while making that fourfold identity explicit in notes and explanations.",
        "",
        "## Core Defaults",
        "",
        f"- `{terms['jhana']['term']}` -> `{terms['jhana']['preferred_translation']}`",
        f"- `{terms['jhayati']['term']}` -> `{terms['jhayati']['preferred_translation']}`",
        f"- `{terms['ekaggata']['term']}` -> `{terms['ekaggata']['preferred_translation']}`",
        f"- `{terms['samadhi']['term']}` -> `{terms['samadhi']['preferred_translation']}`",
        f"- `{terms['vitakka']['term']}` and `{terms['vicara']['term']}` stay coordinated as the practical pair in the first mental theme.",
        "- The first mental theme is not treated as separate from ānāpānasati; the same training clears distractions, brings up wholesome dhammas, and keeps the line of practice direct.",
        "",
        "## Drift Guards",
        "",
        "- Do not widen ariya samma samadhi into a vague concentration category.",
        "- Do not let jhana drift into trance, absorption, or ecstasy language.",
        "- Keep the hindrance-clearing and practical-development frame visible across the cluster.",
        "- Keep the fourfold sequence stable unless a controlled technical reason requires untranslated Pali.",
    ]
    return "\n".join(lines)


def render_formula_sheet(terms: dict[str, dict[str, object]]) -> str:
    by_stage = {
        "First mental theme": ["vivekaja-piti-sukha"],
        "Second mental theme": [
            "avitakka-avicara",
            "ajjhatta-sampasadana",
            "cetaso-ekodibhava",
            "samadhija-piti-sukha",
        ],
        "Third mental theme": ["upekkha-sukha"],
        "Fourth mental theme": ["upekkha-satiparisuddha", "upekkha-satiparisuddhi"],
    }
    lines = [
        "# Jhana Formula Sheet",
        "",
    ]
    for title, stems in by_stage.items():
        lines.append(f"## {title}")
        lines.append("")
        for stem in stems:
            data = terms[stem]
            lines.append(f"- `{data.get('term')}` -> {data.get('preferred_translation')}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "jhana-cluster-glossary.md": render_glossary(terms),
        OUTPUT_DIR / "jhana-sequence-sheet.md": render_sequence_sheet(terms),
        OUTPUT_DIR / "jhana-path-brief.md": render_path_brief(terms),
        OUTPUT_DIR / "jhana-formula-sheet.md": render_formula_sheet(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + ("" if content.endswith("\n") else "\n"), encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    summary = report["summary"]
    errors = report["errors"]
    warnings = report["warnings"]

    print("Jhana Cluster Report")
    print(f"- Headwords: {summary['headwords_present']} / {summary['headwords_expected']}")
    print(f"- Sequence terms: {summary['sequence_terms_present']} / {summary['sequence_terms_expected']}")
    print(f"- Formula terms: {summary['formula_terms_present']} / {summary['formula_terms_expected']}")
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

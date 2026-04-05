#!/usr/bin/env python3
"""Audit and generate translator-facing outputs for the verbal knowing cluster."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from scripts.term_store import iter_term_files
    from scripts.text_utils import safe_text
except ModuleNotFoundError:
    from term_store import iter_term_files
    from text_utils import safe_text


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
OUTPUT_DIR = REPO_ROOT / "docs" / "generated"

HEADWORD_TERMS = ["janati", "abhijanati", "pajanati", "sanjanati", "mannati", "anna"]
SUPPORTING_TERMS = [
    "nana",
    "vijja",
    "panna",
    "parinna",
    "sanna",
    "sampajanna",
    "sati",
    "avijja",
    "ditthi",
    "abhinna",
    "asmimana",
    "upadana",
    "vitakka",
    "papanca",
    "yathabhuta-nanadassana",
    "vimutti-nanadassana",
]
FORMULA_TERMS = [
    "yathabhutam-pajanati",
    "naparam-itthattayati-pajanati",
    "yam-vedeti-tam-sanjanati",
    "yam-sanjanati-tam-vitakketi",
    "yam-vitakketi-tam-papanceti",
    "yam-papanceti-tato-nidanam-purisam-papanca-sanna-sankha-samudacaranti",
    "pathavim-pathavito-sannatva-pathavim-mannati",
    "pathavim-pathavito-abhinnaya-pathavim-ma-manni",
    "pathavim-pathavito-abhinnaya-pathavim-na-mannati",
    "nandi-dukkhassa-mulan",
    "bhava-jati-bhutassa-jaramaranam",
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
        "janati": "knows",
        "abhijanati": "directly knows",
        "pajanati": "discerns",
        "sanjanati": "recognizes",
        "mannati": "takes to be",
        "anna": "final knowledge",
        "yathabhutam-pajanati": "discerns it as it has come to be",
        "naparam-itthattayati-pajanati": "one discerns: there is no more of this state of being",
        "yam-vedeti-tam-sanjanati": "what one feels, one recognizes",
        "yam-sanjanati-tam-vitakketi": "what one recognizes, one thinks about",
        "yam-vitakketi-tam-papanceti": "what one thinks about, one proliferates about",
        "yam-papanceti-tato-nidanam-purisam-papanca-sanna-sankha-samudacaranti": (
            "from what one proliferates about as the source, the recognitions and notions of proliferation sweep over a person"
        ),
        "pathavim-pathavito-sannatva-pathavim-mannati": (
            "having recognized earth as earth, one takes oneself to be earth"
        ),
        "pathavim-pathavito-abhinnaya-pathavim-ma-manni": (
            "having directly known earth as earth, one should not take oneself to be earth"
        ),
        "pathavim-pathavito-abhinnaya-pathavim-na-mannati": (
            "having directly known earth as earth, one does not take oneself to be earth"
        ),
        "nandi-dukkhassa-mulan": "delight is the root of dissatisfaction",
        "bhava-jati-bhutassa-jaramaranam": (
            "with becoming there is birth, and for whatever has come to be there are aging and death"
        ),
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
        "# Verbal Knowing / Recognition / Selfing Glossary",
        "",
        "| Pali | Default | Allowed alternates | Discouraged |",
        "| --- | --- | --- | --- |",
    ]
    for stem in HEADWORD_TERMS + ["nana", "abhinna", "panna", "sanna", "vitakka", "papanca", "asmimana", "upadana"]:
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
        "# Verbal Knowing / Recognition / Selfing Contrast Sheet",
        "",
        f"- `{terms['janati']['term']}`: `{terms['janati']['preferred_translation']}`",
        f"- `{terms['abhijanati']['term']}`: `{terms['abhijanati']['preferred_translation']}`",
        f"- `{terms['pajanati']['term']}`: `{terms['pajanati']['preferred_translation']}`",
        f"- `{terms['sanjanati']['term']}`: `{terms['sanjanati']['preferred_translation']}`",
        f"- `{terms['mannati']['term']}`: `{terms['mannati']['preferred_translation']}`",
        f"- `{terms['anna']['term']}`: `{terms['anna']['preferred_translation']}`",
        "",
        "## Keep Distinct",
        "",
        "- `janati` is plain knowing-language, not discernment, direct-knowing, or accomplishment-talk.",
        "- `abhijanati` is strengthened direct-knowing language, not mere recognition or generic realization-talk.",
        "- `pajanati` is a sharper discerning verb, but not completed `parinna`.",
        "- `sanjanati` is recognition-language in the `sanna` family, not generic knowledge or liberating insight.",
        "- `mannati` is selfing and taking-as language, not bland thought-language.",
        "- `anna` is accomplishment-side final knowledge, not just another way of saying `nana` or vague realization.",
        "- `sati` remains remembering, and `sampajanna` remains practice-side clear knowing.",
        "",
        "## Verb / Noun Guardrails",
        "",
        "- `janati` <-> `nana`: keep the broad knowing family coherent without inflating the verb.",
        "- `abhijanati` <-> `abhinna`: keep direct-knowing language and higher-knowledge language related without flattening them together.",
        "- `pajanati` <-> `panna` / `parinna`: keep the verb sharper than plain knowing but short of completed full understanding.",
        "- `sanjanati` -> `mannati`: preserve the MN 1 movement from recognition into selfing.",
        "- `mannati` <-> `asmimana` / `upadana` / `papanca`: keep the selfing verb tied to I-making, appropriation, and proliferation.",
        "- `anna` <-> `vijja`: keep accomplishment-side knowledge distinct from broader clear knowledge.",
        "",
        "## Formula Guardrails",
        "",
        f"- `{terms['yathabhutam-pajanati']['term']}` -> `{terms['yathabhutam-pajanati']['preferred_translation']}`",
        (
            f"- `{terms['naparam-itthattayati-pajanati']['term']}` -> "
            f"`{terms['naparam-itthattayati-pajanati']['preferred_translation']}`"
        ),
        f"- `{terms['yam-vedeti-tam-sanjanati']['term']}` -> `{terms['yam-vedeti-tam-sanjanati']['preferred_translation']}`",
        (
            f"- `{terms['yam-sanjanati-tam-vitakketi']['term']}` -> "
            f"`{terms['yam-sanjanati-tam-vitakketi']['preferred_translation']}`"
        ),
        (
            f"- `{terms['yam-vitakketi-tam-papanceti']['term']}` -> "
            f"`{terms['yam-vitakketi-tam-papanceti']['preferred_translation']}`"
        ),
        (
            f"- `{terms['yam-papanceti-tato-nidanam-purisam-papanca-sanna-sankha-samudacaranti']['term']}` -> "
            f"`{terms['yam-papanceti-tato-nidanam-purisam-papanca-sanna-sankha-samudacaranti']['preferred_translation']}`"
        ),
        (
            f"- `{terms['pathavim-pathavito-sannatva-pathavim-mannati']['term']}` -> "
            f"`{terms['pathavim-pathavito-sannatva-pathavim-mannati']['preferred_translation']}`"
        ),
        (
            f"- `{terms['pathavim-pathavito-abhinnaya-pathavim-ma-manni']['term']}` -> "
            f"`{terms['pathavim-pathavito-abhinnaya-pathavim-ma-manni']['preferred_translation']}`"
        ),
        (
            f"- `{terms['pathavim-pathavito-abhinnaya-pathavim-na-mannati']['term']}` -> "
            f"`{terms['pathavim-pathavito-abhinnaya-pathavim-na-mannati']['preferred_translation']}`"
        ),
        f"- `{terms['nandi-dukkhassa-mulan']['term']}` -> `{terms['nandi-dukkhassa-mulan']['preferred_translation']}`",
        (
            f"- `{terms['bhava-jati-bhutassa-jaramaranam']['term']}` -> "
            f"`{terms['bhava-jati-bhutassa-jaramaranam']['preferred_translation']}`"
        ),
        "",
        "## Source-Facing Guardrails",
        "",
        "- Preserve the practical anti-mystification pressure in the knowing verbs: do not inflate them into imported realization-language.",
        "- Preserve the MN 1 sequence from recognition into selfing, and from direct knowing into non-selfing.",
        "- Preserve the MN 18 sequence from feeling into recognition, from recognition into thinking, and from thinking into proliferation.",
        "- Preserve the closing pressure in MN 1: delight feeds dissatisfaction, and becoming keeps the birth-and-death sequence live.",
        "- Preserve MN 18 compatibility: what is recognized can become the footing for thought and proliferation if the family is flattened.",
    ]
    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "verbal-knowing-cluster-glossary.md": render_glossary(terms),
        OUTPUT_DIR / "verbal-knowing-cluster-contrast-sheet.md": render_contrast_sheet(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + "\n", encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    summary = report["summary"]
    errors = report["errors"]
    warnings = report["warnings"]
    print("Verbal Knowing / Recognition / Selfing Cluster Report")
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

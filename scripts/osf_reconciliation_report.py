#!/usr/bin/env python3
"""Report the current OSF reconciliation status for reviewed high-impact terms."""

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

REVIEWED_TERMS = {
    "sunnata": {
        "classification": "ALIGN",
        "expected_default": "emptiness",
        "osf_usage": "OSF-facing materials support emptiness, while Buddhadasa-line prose also uses voidness and void-mind language.",
        "governance": "Keep emptiness as the default, tolerate voidness as a controlled alternate, refuse nihilist and mystical drift.",
    },
    "animitta": {
        "classification": "TOLERATE ALTERNATE",
        "expected_default": "signless",
        "osf_usage": "OSF-facing materials do not strongly displace the default, while practical explanation can unpack the term as without sign or not taking up signs.",
        "governance": "Keep signless as the default, tolerate explanatory without-sign language, refuse formlessness and mystical-vagueness drift.",
    },
    "appanihita": {
        "classification": "TOLERATE ALTERNATE",
        "expected_default": "wishless",
        "osf_usage": "Practical explanation can unpack the term as without placing desire or as narrower desireless language, but the family needs a sharper default.",
        "governance": "Keep wishless as the default, tolerate controlled explanatory alternates, refuse passivity, apathy, and no-goals drift.",
    },
    "nibbana": {
        "classification": "TOLERATE ALTERNATE",
        "expected_default": "nibbāna",
        "osf_usage": "OSF and Buddhadasa-facing materials strongly use cooling, coolness, and cooling down in explanation.",
        "governance": "Keep nibbāna untranslated by default, tolerate cooling-language as explanatory OSF-facing gloss, refuse mystical and absolutized drift.",
    },
    "nirodha": {
        "classification": "TOLERATE ALTERNATE",
        "expected_default": "quenching",
        "osf_usage": "OSF and Dhammarato materials often use stopping, ending, or cessation in practical explanation.",
        "governance": "Keep quenching as the default, tolerate ending or cessation in controlled OSF-facing frames, refuse loose generic cessation drift.",
    },
    "sati": {
        "classification": "ALIGN",
        "expected_default": "remembering",
        "osf_usage": "Dhammarato and OSF path-language strongly support remembering, while some rough glossary or coaching prose uses awareness-language.",
        "governance": "Keep remembering as the default, tolerate awareness only as a controlled explanatory alternate, refuse mindfulness and bare-attention drift.",
    },
    "vimutti": {
        "classification": "TOLERATE ALTERNATE",
        "expected_default": "release",
        "osf_usage": "OSF-facing prose can use liberation, but the repository default is sharper as release.",
        "governance": "Keep release as the default, tolerate liberation as a controlled OSF-facing alternate, refuse generic spiritual-freedom rhetoric.",
    },
    "anapanasati": {
        "classification": "TOLERATE ALTERNATE",
        "expected_default": "ānāpānasati",
        "osf_usage": "OSF glossary explains it as remembering to look at in-and-out breathing.",
        "governance": "Keep the untranslated default, tolerate the OSF explanatory gloss, refuse collapse into generic breath-meditation language.",
    },
    "samadhi": {
        "classification": "ALIGN",
        "expected_default": "unification of mind",
        "osf_usage": "Dhammarato and OSF materials strongly reject concentration and reinforce unification of mind.",
        "governance": "Keep the current default and continue refusing concentration drift.",
    },
    "citta": {
        "classification": "TOLERATE ALTERNATE",
        "expected_default": "feeling mind",
        "osf_usage": "OSF explanatory material can use mind, heart-mind, or center of consciousness, especially in practice prose.",
        "governance": "Keep feeling mind as the default, tolerate OSF-facing explanatory alternates, refuse collapse into cognition or consciousness.",
    },
    "passaddhi": {
        "classification": "REFUSE DRIFT",
        "expected_default": "relaxation",
        "osf_usage": "Rough peace- or calm-language could easily flatten passaddhi into santi or generic tranquility.",
        "governance": "Keep relaxation as the default and refuse drift into undifferentiated peace-language.",
    },
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


def build_report(terms: dict[str, dict[str, object]]) -> dict[str, object]:
    missing = [stem for stem in REVIEWED_TERMS if stem not in terms]
    mismatches = [
        stem
        for stem, metadata in REVIEWED_TERMS.items()
        if stem in terms and terms[stem].get("preferred_translation") != metadata["expected_default"]
    ]
    return {
        "summary": {
            "reviewed_terms_present": len(REVIEWED_TERMS) - len(missing),
            "reviewed_terms_expected": len(REVIEWED_TERMS),
        },
        "errors": {
            "missing_reviewed_terms": missing,
        },
        "warnings": {
            "preferred_rendering_mismatches": mismatches,
        },
    }


def render_sheet(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# OSF Reconciliation Sheet",
        "",
        "| Term | Repo default | OSF-facing usage | Classification | Governance decision |",
        "| --- | --- | --- | --- | --- |",
    ]
    for stem, metadata in REVIEWED_TERMS.items():
        data = terms[stem]
        lines.append(
            f"| {data.get('term')} | {data.get('preferred_translation')} | {metadata['osf_usage']} | {metadata['classification']} | {metadata['governance']} |"
        )
    lines.append("")
    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / "osf-reconciliation-sheet.md"
    path.write_text(render_sheet(terms) + "\n", encoding="utf-8")
    return [path]


def print_text_report(report: dict[str, object]) -> None:
    summary = report["summary"]
    errors = report["errors"]
    warnings = report["warnings"]

    print("OSF Reconciliation Report")
    print(f"- Reviewed terms: {summary['reviewed_terms_present']} / {summary['reviewed_terms_expected']}")
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
    parser.add_argument("--write-docs", action="store_true", help="Generate the reconciliation sheet in docs/generated.")
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

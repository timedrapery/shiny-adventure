#!/usr/bin/env python3
"""Audit and generate outputs for the MN 10 / MN 118 practice-text surface."""

from __future__ import annotations

import argparse
import json
import re
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

HEADWORD_TERMS = [
    "satipatthana",
    "anapanasati",
    "sati",
    "sampajanna",
]

SUPPORTING_TERMS = [
    "kaya-sankhara",
    "vedananupassana",
]

CONTROL_RECORDS = [
    "mn10-direct-path-opening",
    "mn10-satipatthana-qualifier",
    "mn10-kayanupassi-internal-external",
    "mn10-kayo-anchor-nonappropriation",
    "mn118-breathing-remembrance-line",
    "mn118-whole-body-training",
    "mn118-body-conditioner-training",
]

TRANSLATION_SURFACE_REQUIREMENTS: tuple[dict[str, object], ...] = (
    {
        "label": "MN 10",
        "relpath": "docs/translations/mn10-satipatthana-sutta.md",
        "required_terms": (
            "mn10-direct-path-opening",
            "mn10-satipatthana-qualifier",
            "mn118-breathing-remembrance-line",
            "mn118-whole-body-training",
            "mn118-body-conditioner-training",
            "mn10-kayanupassi-internal-external",
            "mn10-kayo-anchor-nonappropriation",
        ),
    },
    {
        "label": "MN 118",
        "relpath": "docs/translations/mn118-anapanasati-sutta.md",
        "required_terms": (
            "mn118-breathing-remembrance-line",
            "mn118-whole-body-training",
            "mn118-body-conditioner-training",
            "mn10-satipatthana-qualifier",
        ),
    },
)

EXPECTED_PREFERRED_TRANSLATIONS = {
    "satipatthana": "establishment of sati",
    "anapanasati": "ānāpānasati",
    "sati": "remembering",
    "sampajanna": "clear knowing",
    "kaya-sankhara": "body conditioner",
    "vedananupassana": "contemplation of felt experience",
    "mn10-direct-path-opening": "Bhikkhus, this is the direct path for the purification of beings, for going beyond sorrow and lamentation, for ending pain and distress, for reaching the right way, for directly realizing nibbāna: namely, the four establishments of sati",
    "mn10-satipatthana-qualifier": "ardent, with clear knowing, with remembering, having removed coveting and distress regarding the world",
    "mn10-kayanupassi-internal-external": "one remains observing the body as internal, observing the body as external, and observing the body as both internal and external",
    "mn10-kayo-anchor-nonappropriation": "or remembering is simply present: 'There is body,' just enough for knowing and for remembering. One stays without depending on anything and does not take anything in the world personally",
    "mn118-breathing-remembrance-line": "one breathes in remembering the Dhamma; one breathes out remembering the Dhamma",
    "mn118-whole-body-training": "one trains: 'Breathing in, I will experience the whole body.' One trains: 'Breathing out, I will experience the whole body.'",
    "mn118-body-conditioner-training": "one trains: 'Breathing in, I will calm the body conditioner.' One trains: 'Breathing out, I will calm the body conditioner.'",
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


def supporting_terms_still_thin(terms: dict[str, dict[str, object]], stems: list[str]) -> list[str]:
    thin: list[str] = []
    for stem in stems:
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        notes = data.get("notes")
        related_terms = data.get("related_terms")
        examples = data.get("example_phrases")
        translation_policy = data.get("translation_policy")
        if not isinstance(notes, str) or len(notes.strip()) < 40:
            thin.append(stem)
            continue
        if not isinstance(related_terms, list) or not related_terms:
            thin.append(stem)
            continue
        if not isinstance(examples, list) or not examples:
            thin.append(stem)
            continue
        if not isinstance(translation_policy, dict) or not translation_policy:
            thin.append(stem)
    return thin


def render_mismatch_warnings(terms: dict[str, dict[str, object]]) -> list[str]:
    warnings: list[str] = []
    for stem, expected_rendering in EXPECTED_PREFERRED_TRANSLATIONS.items():
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        actual = data.get("preferred_translation")
        if actual != expected_rendering:
            warnings.append(f"{stem}: expected `{expected_rendering}` but found `{actual}`")
    return warnings


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


def translation_surface_failures(
    terms: dict[str, dict[str, object]],
    repo_root: Path,
    surface_requirements: tuple[dict[str, object], ...],
) -> tuple[list[str], list[str]]:
    missing_surfaces: list[str] = []
    line_gaps: list[str] = []

    for surface in surface_requirements:
        label = str(surface["label"])
        relpath = str(surface["relpath"])
        path = repo_root / relpath
        if not path.exists():
            missing_surfaces.append(relpath)
            continue

        normalized_doc = normalize_text(path.read_text(encoding="utf-8"))
        for stem in surface["required_terms"]:
            data = terms.get(str(stem))
            if not isinstance(data, dict):
                continue
            preferred = data.get("preferred_translation")
            if not isinstance(preferred, str):
                continue
            if normalize_text(preferred) not in normalized_doc:
                line_gaps.append(
                    f"{label}: missing governed control line from `{stem}` in {relpath}"
                )

    return missing_surfaces, line_gaps


def build_report(
    terms: dict[str, dict[str, object]],
    repo_root: Path = REPO_ROOT,
    surface_requirements: tuple[dict[str, object], ...] = TRANSLATION_SURFACE_REQUIREMENTS,
) -> dict[str, object]:
    all_priority = HEADWORD_TERMS + SUPPORTING_TERMS + CONTROL_RECORDS
    missing_surfaces, line_gaps = translation_surface_failures(
        terms,
        repo_root=repo_root,
        surface_requirements=surface_requirements,
    )
    return {
        "summary": {
            "headwords_present": len(HEADWORD_TERMS) - len(missing_terms(terms, HEADWORD_TERMS)),
            "headwords_expected": len(HEADWORD_TERMS),
            "supporting_terms_present": len(SUPPORTING_TERMS) - len(missing_terms(terms, SUPPORTING_TERMS)),
            "supporting_terms_expected": len(SUPPORTING_TERMS),
            "control_records_present": len(CONTROL_RECORDS) - len(missing_terms(terms, CONTROL_RECORDS)),
            "control_records_expected": len(CONTROL_RECORDS),
            "translation_surfaces_present": len(surface_requirements) - len(missing_surfaces),
            "translation_surfaces_expected": len(surface_requirements),
        },
        "errors": {
            "missing_headwords": missing_terms(terms, HEADWORD_TERMS),
            "missing_supporting_terms": missing_terms(terms, SUPPORTING_TERMS),
            "missing_control_records": missing_terms(terms, CONTROL_RECORDS),
            "control_example_source_gaps": example_source_gaps(terms, CONTROL_RECORDS),
            "missing_translation_surfaces": missing_surfaces,
            "translation_control_line_gaps": line_gaps,
        },
        "warnings": {
            "headwords_with_thin_authority_basis": weak_authority_terms(terms, HEADWORD_TERMS),
            "supporting_terms_still_thin": supporting_terms_still_thin(terms, SUPPORTING_TERMS),
            "preferred_rendering_mismatches": render_mismatch_warnings(terms),
        },
    }


def render_support_line(terms: dict[str, dict[str, object]], stem: str) -> str:
    data = terms.get(stem)
    if not isinstance(data, dict):
        return f"- `{stem}`: missing record"
    preferred = data.get("preferred_translation", "(missing preferred translation)")
    return f"- `{stem}`: `{preferred}`"


def render_control_sheet(terms: dict[str, dict[str, object]]) -> str:
    usage: dict[str, list[str]] = {stem: [] for stem in CONTROL_RECORDS}
    for surface in TRANSLATION_SURFACE_REQUIREMENTS:
        label = str(surface["label"])
        for stem in surface["required_terms"]:
            usage.setdefault(str(stem), []).append(label)

    lines = [
        "# Practice-Text Control Sheet",
        "",
        "## Shared Purpose",
        "",
        "This sheet summarizes the current governed control lines for the shared MN 10 / MN 118 practice-text surface.",
        "",
        "## Control Records",
        "",
        "| Record | Controlled English | Used in |",
        "| --- | --- | --- |",
    ]
    for stem in CONTROL_RECORDS:
        data = terms.get(stem)
        preferred = "(missing record)"
        if isinstance(data, dict):
            preferred = str(data.get("preferred_translation", "(missing preferred translation)"))
        lines.append(
            f"| `{stem}` | {preferred} | {', '.join(usage.get(stem, [])) or '-'} |"
        )

    lines.extend(
        [
            "",
            "## Supporting Terms",
            "",
        ]
    )
    for stem in HEADWORD_TERMS + SUPPORTING_TERMS:
        lines.append(render_support_line(terms, stem))

    lines.extend(
        [
            "",
            "## Operating Rule",
            "",
            "- Keep the shared breathing-side lines aligned across MN 10 and MN 118 through the governed phrase records above.",
            "- If another translation begins reusing this same formula family, add it to the audited surface instead of re-solving the wording locally.",
        ]
    )
    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "practice-text-control-sheet.md": render_control_sheet(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + "\n", encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    summary = report["summary"]
    errors = report["errors"]
    warnings = report["warnings"]

    print("Practice-Text Surface Report")
    print(f"- Headwords: {summary['headwords_present']} / {summary['headwords_expected']}")
    print(f"- Supporting terms: {summary['supporting_terms_present']} / {summary['supporting_terms_expected']}")
    print(f"- Control records: {summary['control_records_present']} / {summary['control_records_expected']}")
    print(f"- Translation surfaces: {summary['translation_surfaces_present']} / {summary['translation_surfaces_expected']}")
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

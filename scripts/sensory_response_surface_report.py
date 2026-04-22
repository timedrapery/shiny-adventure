#!/usr/bin/env python3
"""Audit and generate outputs for the MN 137 / MN 148 / SN 36.6 sensory-response surface."""

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
    "ayatana",
    "phassa",
    "vedana",
    "tanha",
    "anusaya",
    "upekkha",
]

SUPPORTING_TERMS = [
    "somanassa",
    "domanassa",
    "manopavicara",
    "sukha-vedana",
    "dukkha-vedana",
    "adukkhamasukha-vedana",
]

CONTROL_RECORDS = [
    "gehasita-somanassa",
    "nekkhammasita-somanassa",
    "gehasita-domanassa",
    "nekkhammasita-domanassa",
    "gehasita-upekkha",
    "nekkhammasita-upekkha",
    "mn137-supported-by-this-give-up-that",
    "mn137-three-establishments-of-sati",
    "sukhaya-vedanaya-phuttho-samano-abhinandati-abhivadati-ajjhosaya-titthati",
    "mn148-pleasant-feeling-trained-response",
    "mn148-painful-feeling-untrained-response",
    "mn148-painful-feeling-trained-response",
    "mn148-mixed-feeling-undiscerned-response",
    "vedanaya-samudayanca-atthangamanca-assadanca-adinavanca-nissarananca-yathabhutam-pajanati",
    "sn36-6-two-feelings-painful-feeling",
    "sn36-6-one-feeling-painful-feeling",
    "sn36-6-feelings-undiscerned-response",
    "sn36-6-feelings-discerned-response",
]

TRANSLATION_SURFACE_REQUIREMENTS: tuple[dict[str, object], ...] = (
    {
        "label": "MN 137",
        "relpath": "docs/translations/mn137-salayatanavibhanga-sutta.md",
        "required_terms": (
            "gehasita-somanassa",
            "nekkhammasita-somanassa",
            "gehasita-domanassa",
            "nekkhammasita-domanassa",
            "gehasita-upekkha",
            "nekkhammasita-upekkha",
            "mn137-supported-by-this-give-up-that",
            "mn137-three-establishments-of-sati",
        ),
    },
    {
        "label": "MN 148",
        "relpath": "docs/translations/mn148-chachakka-sutta.md",
        "required_terms": (
            "sukhaya-vedanaya-phuttho-samano-abhinandati-abhivadati-ajjhosaya-titthati",
            "mn148-pleasant-feeling-trained-response",
            "mn148-painful-feeling-untrained-response",
            "mn148-painful-feeling-trained-response",
            "mn148-mixed-feeling-undiscerned-response",
            "vedanaya-samudayanca-atthangamanca-assadanca-adinavanca-nissarananca-yathabhutam-pajanati",
        ),
    },
    {
        "label": "SN 36.6",
        "relpath": "docs/translations/sn36-6-salla-sutta.md",
        "required_terms": (
            "mn148-painful-feeling-untrained-response",
            "mn148-painful-feeling-trained-response",
            "sn36-6-two-feelings-painful-feeling",
            "sn36-6-one-feeling-painful-feeling",
            "sn36-6-feelings-undiscerned-response",
            "sn36-6-feelings-discerned-response",
        ),
    },
)

EXPECTED_PREFERRED_TRANSLATIONS = {
    "ayatana": "field",
    "phassa": "contact",
    "vedana": "felt experience",
    "tanha": "ignorant wanting",
    "anusaya": "underlying tendency",
    "upekkha": "dynamic balance",
    "somanassa": "gladness",
    "domanassa": "distress",
    "manopavicara": "mental exploration",
    "sukha-vedana": "pleasant feeling",
    "dukkha-vedana": "painful feeling",
    "adukkhamasukha-vedana": "mixed feeling",
    "gehasita-somanassa": "gladness tied to the household life",
    "nekkhammasita-somanassa": "gladness tied to renunciation",
    "gehasita-domanassa": "distress tied to the household life",
    "nekkhammasita-domanassa": "distress tied to renunciation",
    "gehasita-upekkha": "dynamic balance tied to the household life",
    "nekkhammasita-upekkha": "dynamic balance tied to renunciation",
    "mn137-supported-by-this-give-up-that": "here, supported by this, give up that",
    "mn137-three-establishments-of-sati": "three establishments of sati",
    "sukhaya-vedanaya-phuttho-samano-abhinandati-abhivadati-ajjhosaya-titthati": "when one is touched by pleasant feeling, one delights in it, affirms it, and keeps taking it personally",
    "mn148-pleasant-feeling-trained-response": "when one is touched by pleasant feeling, one does not delight in it, does not affirm it, and does not keep taking it personally",
    "mn148-painful-feeling-untrained-response": "when one is touched by painful feeling, one sorrows, grows worn down, laments, beats one's chest and cries, and falls into confusion",
    "mn148-painful-feeling-trained-response": "when one is touched by painful feeling, one does not sorrow, does not grow worn down, does not lament, does not beat one's chest and cry, and does not fall into confusion",
    "mn148-mixed-feeling-undiscerned-response": "when one is touched by mixed feeling, one does not discern that feeling's arising and vanishing, gratification, danger, and escape as they have come to be",
    "vedanaya-samudayanca-atthangamanca-assadanca-adinavanca-nissarananca-yathabhutam-pajanati": "one discerns that feeling's arising and vanishing, gratification, danger, and escape as they have come to be",
    "sn36-6-two-feelings-painful-feeling": "one feels two feelings: bodily and mental",
    "sn36-6-one-feeling-painful-feeling": "one feels one feeling: bodily, not mental",
    "sn36-6-feelings-undiscerned-response": "one does not discern those feelings' arising and vanishing, gratification, danger, and escape as they have come to be",
    "sn36-6-feelings-discerned-response": "one discerns those feelings' arising and vanishing, gratification, danger, and escape as they have come to be",
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
        if not isinstance(authority, list) or len(authority) < 1:
            weak.append(stem)
    return weak


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
        "# Sensory-Response Control Sheet",
        "",
        "## Shared Purpose",
        "",
        "This sheet summarizes the current governed control lines for the linked MN 137 / MN 148 / SN 36.6 sensory-response surface.",
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

    lines.extend(["", "## Supporting Terms", ""])
    for stem in HEADWORD_TERMS + SUPPORTING_TERMS:
        lines.append(render_support_line(terms, stem))

    lines.extend(
        [
            "",
            "## Operating Rule",
            "",
            "- Keep the household / renunciation labels and the trained / untrained response formulas aligned through the governed records above.",
            "- If another feeling-domain translation begins reusing these same families, add it to the audited surface instead of re-solving the wording locally.",
        ]
    )
    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "sensory-response-control-sheet.md": render_control_sheet(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + "\n", encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    summary = report["summary"]
    errors = report["errors"]
    warnings = report["warnings"]

    print("Sensory-Response Surface Report")
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

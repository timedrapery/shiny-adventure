#!/usr/bin/env python3
"""Audit and generate translator-facing outputs for the path-factor core cluster."""

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

HEADWORD_TERMS = [
    "samma-ditthi",
    "samma-sankappa",
    "samma-vaca",
    "samma-kammanta",
    "samma-ajiva",
    "samma-vayama",
    "samma-sati",
    "samma-samadhi",
]

SUPPORTING_TERMS = [
    "magga",
    "ariya",
    "patipada",
    "lokiya",
    "lokuttara",
]

COMPLETION_TERMS = [
    "samma-nana",
    "samma-vimutti",
]

COLLECTIVE_TERMS = [
    "ariya-atthangika-magga",
]

EXPECTED_PREFERRED_TRANSLATIONS = {
    "samma-ditthi": "right view",
    "samma-sankappa": "right attitude",
    "samma-vaca": "right speech",
    "samma-kammanta": "right action",
    "samma-ajiva": "right livelihood",
    "samma-vayama": "right effort",
    "samma-sati": "right remembering",
    "samma-samadhi": "right mental composure",
    "magga": "path",
    "ariya": "noble",
    "patipada": "path of practice",
    "lokiya": "worldly",
    "lokuttara": "beyond-the-world",
    "samma-nana": "right knowledge",
    "samma-vimutti": "right release",
    "ariya-atthangika-magga": "noble eightfold path",
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


def thin_collective_terms(terms: dict[str, dict[str, object]], stems: list[str]) -> list[str]:
    thin: list[str] = []
    for stem in stems:
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        notes = data.get("notes")
        related = data.get("related_terms")
        examples = data.get("example_phrases")
        if (
            not isinstance(notes, str)
            or not notes.strip()
            or not isinstance(related, list)
            or not related
            or not isinstance(examples, list)
            or not examples
        ):
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


def contains_all(blob: str, tokens: list[str]) -> bool:
    return all(token in blob for token in tokens)


def core_loop_identity_missing(terms: dict[str, dict[str, object]]) -> list[str]:
    missing: list[str] = []
    expectations = {
        "samma-ditthi": ["right remembering", "right effort"],
        "samma-sati": ["right view", "right effort", "circle"],
        "samma-vayama": ["right view", "right remembering"],
        "magga": ["right view", "right remembering", "right effort", "circle"],
    }
    for stem, tokens in expectations.items():
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        blob = json.dumps(data, ensure_ascii=False).casefold()
        if not contains_all(blob, tokens):
            missing.append(stem)
    return missing


def tenfold_completion_identity_missing(terms: dict[str, dict[str, object]]) -> list[str]:
    missing: list[str] = []

    samma_samadhi = terms.get("samma-samadhi")
    if isinstance(samma_samadhi, dict):
        blob = json.dumps(samma_samadhi, ensure_ascii=False).casefold()
        if (
            not any(token in blob for token in ("jhana", "jhāna"))
            or not contains_all(blob, ["first", "second", "third", "fourth", "right knowledge", "right release"])
        ):
            missing.append("samma-samadhi")

    completion_expectations = {
        "samma-nana": ["right mental composure", "right release"],
        "samma-vimutti": ["right knowledge"],
    }
    for stem, tokens in completion_expectations.items():
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        blob = json.dumps(data, ensure_ascii=False).casefold()
        if not contains_all(blob, tokens):
            missing.append(stem)
    return missing


def build_report(terms: dict[str, dict[str, object]]) -> dict[str, object]:
    all_priority = HEADWORD_TERMS + SUPPORTING_TERMS + COMPLETION_TERMS + COLLECTIVE_TERMS
    return {
        "summary": {
            "headwords_present": len(HEADWORD_TERMS) - len(missing_terms(terms, HEADWORD_TERMS)),
            "headwords_expected": len(HEADWORD_TERMS),
            "supporting_terms_present": len(SUPPORTING_TERMS) - len(missing_terms(terms, SUPPORTING_TERMS)),
            "supporting_terms_expected": len(SUPPORTING_TERMS),
            "completion_terms_present": len(COMPLETION_TERMS) - len(missing_terms(terms, COMPLETION_TERMS)),
            "completion_terms_expected": len(COMPLETION_TERMS),
            "collective_terms_present": len(COLLECTIVE_TERMS) - len(missing_terms(terms, COLLECTIVE_TERMS)),
            "collective_terms_expected": len(COLLECTIVE_TERMS),
        },
        "errors": {
            "missing_headwords": missing_terms(terms, HEADWORD_TERMS),
            "missing_supporting_terms": missing_terms(terms, SUPPORTING_TERMS),
            "missing_completion_terms": missing_terms(terms, COMPLETION_TERMS),
            "missing_collective_terms": missing_terms(terms, COLLECTIVE_TERMS),
            "cluster_example_source_gaps": example_source_gaps(terms, all_priority),
        },
        "warnings": {
            "headwords_with_thin_authority_basis": weak_authority_terms(terms, HEADWORD_TERMS),
            "collective_terms_still_thin": thin_collective_terms(terms, COLLECTIVE_TERMS),
            "preferred_rendering_mismatches": preferred_rendering_mismatches(terms),
            "core_loop_identity_missing": core_loop_identity_missing(terms),
            "tenfold_completion_identity_missing": tenfold_completion_identity_missing(terms),
        },
    }


def render_glossary(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Path-Factor Cluster Glossary",
        "",
        "| Role | Pali | Default | Allowed alternates | Discouraged |",
        "| --- | --- | --- | --- | --- |",
    ]
    grouped_terms = (
        [("Core factor", stem) for stem in HEADWORD_TERMS]
        + [("Path support", stem) for stem in SUPPORTING_TERMS]
        + [("Completion side", stem) for stem in COMPLETION_TERMS]
        + [("Collective", stem) for stem in COLLECTIVE_TERMS]
    )
    for role, stem in grouped_terms:
        data = terms[stem]
        alts = ", ".join(data.get("alternative_translations", []))
        discouraged = ", ".join(data.get("discouraged_translations", []))
        lines.append(
            f"| {role} | {data.get('term')} | {data.get('preferred_translation')} | {alts or '-'} | {discouraged or '-'} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_core_loop_brief(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Path-Factor Core Loop Brief",
        "",
        "## Core Loop",
        "",
        f"- `{terms['samma-ditthi']['term']}` -> `{terms['samma-ditthi']['preferred_translation']}`",
        f"- `{terms['samma-sati']['term']}` -> `{terms['samma-sati']['preferred_translation']}`",
        f"- `{terms['samma-vayama']['term']}` -> `{terms['samma-vayama']['preferred_translation']}`",
        f"- `{terms['magga']['term']}` keeps those three as recurring live path functions rather than isolated checklist items.",
        "",
        "## Drift Guards",
        "",
        f"- `{terms['samma-samadhi']['term']}` is not treated as a standalone meditation box. It is furnished with seven supporting path factors.",
        f"- `{terms['ariya-atthangika-magga']['term']}` remains the collective record for the full eightfold path and points back to the governed factor entries rather than replacing them.",
        f"- `{terms['lokiya']['term']}` and `{terms['lokuttara']['term']}` stay coordinated as the worldly / beyond-the-world distinction inside the same family.",
        "- Keep the loop practical without collapsing the factors into one another.",
        "- Keep the family doctrinal without turning it into static list-language.",
    ]
    return "\n".join(lines)


def render_tenfold_sequence_sheet(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Path-Factor Tenfold Sequence Sheet",
        "",
        "## Training Factors",
        "",
    ]
    for stem in HEADWORD_TERMS:
        data = terms[stem]
        lines.append(f"- `{data.get('term')}` -> `{data.get('preferred_translation')}`")
    lines.extend(
        [
            "",
            "## Completion Sequence",
            "",
            f"- `{terms['samma-samadhi']['term']}` stays the eighth path factor and the governed opening into the completion-side close.",
            f"- `{terms['samma-nana']['term']}` -> `{terms['samma-nana']['preferred_translation']}`",
            f"- `{terms['samma-vimutti']['term']}` -> `{terms['samma-vimutti']['preferred_translation']}`",
            "- Keep explicit that the trainee is eight-factored while the one beyond training closes the sequence with right knowledge and right release.",
            "",
            "## Family Contrasts",
            "",
            f"- `{terms['lokiya']['term']}` -> `{terms['lokiya']['preferred_translation']}`",
            f"- `{terms['lokuttara']['term']}` -> `{terms['lokuttara']['preferred_translation']}`",
            f"- `{terms['patipada']['term']}` keeps the practical course language available without replacing `{terms['magga']['term']}`.",
        ]
    )
    return "\n".join(lines)


def render_supporting_terms_map(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Path-Factor Support Map",
        "",
        f"- `{terms['magga']['term']}` names the whole path rather than one factor inside it.",
        f"- `{terms['ariya']['term']}` keeps the family anchored as the noble path, not just a useful lifestyle list.",
        f"- `{terms['patipada']['term']}` keeps the practical course-of-training surface available in explanatory prose.",
        f"- `{terms['lokiya']['term']}` marks wholesome but still conditioned training-side factors.",
        f"- `{terms['lokuttara']['term']}` marks the beyond-the-world side of the same path family.",
        f"- `{terms['samma-nana']['term']}` and `{terms['samma-vimutti']['term']}` preserve the tenfold completion close of MN 117.",
        f"- `{terms['ariya-atthangika-magga']['term']}` remains the collective label for the eightfold whole and should point readers back to the governed factor records.",
    ]
    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "path-factor-cluster-glossary.md": render_glossary(terms),
        OUTPUT_DIR / "path-factor-core-loop-brief.md": render_core_loop_brief(terms),
        OUTPUT_DIR / "path-factor-tenfold-sequence-sheet.md": render_tenfold_sequence_sheet(terms),
        OUTPUT_DIR / "path-factor-supporting-terms-map.md": render_supporting_terms_map(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + ("" if content.endswith("\n") else "\n"), encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    summary = report["summary"]
    errors = report["errors"]
    warnings = report["warnings"]

    print("Path-Factor Cluster Report")
    print(f"- Headwords: {summary['headwords_present']} / {summary['headwords_expected']}")
    print(f"- Supporting terms: {summary['supporting_terms_present']} / {summary['supporting_terms_expected']}")
    print(f"- Completion terms: {summary['completion_terms_present']} / {summary['completion_terms_expected']}")
    print(f"- Collective terms: {summary['collective_terms_present']} / {summary['collective_terms_expected']}")
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

#!/usr/bin/env python3
"""Audit and generate translator-facing outputs for the four noble truths cluster."""

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
    "ariyasacca",
    "dukkha",
    "samudaya",
    "nirodha",
    "magga",
]

SUPPORTING_TERMS = [
    "sati",
    "patipada",
]

TRUTH_RECORDS = [
    "dukkha-ariyasacca",
    "samudaya-ariyasacca",
    "nirodha-ariyasacca",
    "magga-ariyasacca",
]

EXPECTED_PREFERRED_TRANSLATIONS = {
    "ariyasacca": "noble truth",
    "dukkha": "dissatisfaction",
    "samudaya": "origin",
    "nirodha": "quenching",
    "magga": "path",
    "sati": "remembering",
    "patipada": "path of practice",
    "dukkha-ariyasacca": "noble truth of dissatisfaction",
    "samudaya-ariyasacca": "noble truth of origin",
    "nirodha-ariyasacca": "noble truth of quenching",
    "magga-ariyasacca": "noble truth of the path",
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


def thin_truth_records(terms: dict[str, dict[str, object]]) -> list[str]:
    thin: list[str] = []
    for stem in TRUTH_RECORDS:
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


def practical_cycle_mapping_missing(terms: dict[str, dict[str, object]]) -> list[str]:
    missing: list[str] = []
    expectations = {
        "ariyasacca": ["correct noble practice", "wake up", "wholesome change", "quenching"],
        "dukkha": ["waking up", "what is here"],
        "samudaya": ["where it is heading"],
        "nirodha": ["congratulating oneself"],
        "magga": ["making a wholesome change"],
        "sati": ["again as often as one can remember"],
    }
    for stem, tokens in expectations.items():
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        blob = json.dumps(data, ensure_ascii=False).casefold()
        if not contains_all(blob, tokens):
            missing.append(stem)
    return missing


def dukkha_nirodha_scope_missing(terms: dict[str, dict[str, object]]) -> list[str]:
    missing: list[str] = []
    expectations = {
        "ariyasacca": ["sn 22.86", "dukkha / dukkha-nirodha scope"],
        "dukkha": ["sn 22.86", "only dissatisfaction and the ending of dissatisfaction"],
        "nirodha": ["sn 22.86"],
    }
    for stem, tokens in expectations.items():
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        blob = json.dumps(data, ensure_ascii=False).casefold()
        if not contains_all(blob, tokens):
            missing.append(stem)
    return missing


def build_report(terms: dict[str, dict[str, object]]) -> dict[str, object]:
    all_priority = HEADWORD_TERMS + SUPPORTING_TERMS + TRUTH_RECORDS
    return {
        "summary": {
            "headwords_present": len(HEADWORD_TERMS) - len(missing_terms(terms, HEADWORD_TERMS)),
            "headwords_expected": len(HEADWORD_TERMS),
            "supporting_terms_present": len(SUPPORTING_TERMS) - len(missing_terms(terms, SUPPORTING_TERMS)),
            "supporting_terms_expected": len(SUPPORTING_TERMS),
            "truth_records_present": len(TRUTH_RECORDS) - len(missing_terms(terms, TRUTH_RECORDS)),
            "truth_records_expected": len(TRUTH_RECORDS),
        },
        "errors": {
            "missing_headwords": missing_terms(terms, HEADWORD_TERMS),
            "missing_supporting_terms": missing_terms(terms, SUPPORTING_TERMS),
            "missing_truth_records": missing_terms(terms, TRUTH_RECORDS),
            "cluster_example_source_gaps": example_source_gaps(terms, all_priority),
        },
        "warnings": {
            "headwords_with_thin_authority_basis": weak_authority_terms(terms, HEADWORD_TERMS),
            "truth_records_still_thin": thin_truth_records(terms),
            "preferred_rendering_mismatches": preferred_rendering_mismatches(terms),
            "practical_cycle_mapping_missing": practical_cycle_mapping_missing(terms),
            "dukkha_nirodha_scope_missing": dukkha_nirodha_scope_missing(terms),
        },
    }


def render_glossary(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Four Noble Truths Cluster Glossary",
        "",
        "| Role | Pali | Default | Allowed alternates | Discouraged |",
        "| --- | --- | --- | --- | --- |",
    ]
    grouped_terms = (
        [("Headword", stem) for stem in HEADWORD_TERMS]
        + [("Support", stem) for stem in SUPPORTING_TERMS]
        + [("Truth record", stem) for stem in TRUTH_RECORDS]
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


def render_truth_task_sheet(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Four Noble Truths Truth-Task Sheet",
        "",
        f"- `{terms['dukkha-ariyasacca']['term']}` -> `{terms['dukkha-ariyasacca']['preferred_translation']}`",
        "  Task surface: wake up and look at what is here.",
        f"- `{terms['samudaya-ariyasacca']['term']}` -> `{terms['samudaya-ariyasacca']['preferred_translation']}`",
        "  Task surface: see where the present pattern is heading.",
        f"- `{terms['nirodha-ariyasacca']['term']}` -> `{terms['nirodha-ariyasacca']['preferred_translation']}`",
        "  Task surface: notice and appreciate the quenching of dukkha.",
        f"- `{terms['magga-ariyasacca']['term']}` -> `{terms['magga-ariyasacca']['preferred_translation']}`",
        "  Task surface: make a wholesome change.",
        f"- `{terms['sati']['term']}` remains `{terms['sati']['preferred_translation']}` as the return-point that lets the cycle happen again.",
    ]
    return "\n".join(lines)


def render_correct_noble_practice_brief(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Correct Noble Practice Brief",
        "",
        "## Governing Cycle",
        "",
        "- Wake up and look at what is here.",
        "- See where it is heading.",
        "- Make a wholesome change.",
        "- Notice and appreciate the quenching of dukkha.",
        "- Do it again when remembered.",
        "",
        "## Guardrails",
        "",
        f"- `{terms['ariyasacca']['term']}` stays `{terms['ariyasacca']['preferred_translation']}` rather than turning the truths into slogan-language.",
        f"- `{terms['dukkha']['term']}` stays `{terms['dukkha']['preferred_translation']}` rather than drifting back to uncontrolled suffering-language.",
        f"- `{terms['nirodha']['term']}` stays `{terms['nirodha']['preferred_translation']}` rather than flattening it into vague positivity or generic cessation-shorthand.",
        f"- `{terms['magga']['term']}` stays `{terms['magga']['preferred_translation']}` while allowing the immediate practice-side gloss of making a wholesome change.",
        f"- `{terms['patipada']['term']}` remains available when the line needs course-of-practice language without replacing `{terms['magga']['term']}`.",
    ]
    return "\n".join(lines)


def render_scope_sheet(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Dukkha-Nirodha Scope Sheet",
        "",
        f"- `{terms['ariyasacca']['term']}` keeps the four truths ordered by the repository's `dukkha / dukkha-nirodha` scope rule.",
        f"- `{terms['dukkha']['term']}` remains the first governing side of that scope as `{terms['dukkha']['preferred_translation']}`.",
        f"- `{terms['nirodha']['term']}` remains the ending side of that scope as `{terms['nirodha']['preferred_translation']}`.",
        f"- `{terms['magga']['term']}` and `{terms['patipada']['term']}` stay readable inside that scope rather than drifting into generic self-improvement language.",
        f"- `{terms['samudaya']['term']}` stays the origin-side explanatory truth and should remain readable as what the present pattern is heading into, not as abstract creation-talk.",
    ]
    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "four-noble-truths-cluster-glossary.md": render_glossary(terms),
        OUTPUT_DIR / "four-noble-truths-truth-task-sheet.md": render_truth_task_sheet(terms),
        OUTPUT_DIR / "four-noble-truths-correct-noble-practice-brief.md": render_correct_noble_practice_brief(terms),
        OUTPUT_DIR / "dukkha-nirodha-scope-sheet.md": render_scope_sheet(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + ("" if content.endswith("\n") else "\n"), encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    summary = report["summary"]
    errors = report["errors"]
    warnings = report["warnings"]

    print("Four Noble Truths Cluster Report")
    print(f"- Headwords: {summary['headwords_present']} / {summary['headwords_expected']}")
    print(f"- Supporting terms: {summary['supporting_terms_present']} / {summary['supporting_terms_expected']}")
    print(f"- Truth records: {summary['truth_records_present']} / {summary['truth_records_expected']}")
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

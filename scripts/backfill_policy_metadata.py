#!/usr/bin/env python3
"""Backfill structured authority and policy metadata for major terms."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from scripts.term_store import iter_term_files
except ModuleNotFoundError:
    from term_store import iter_term_files


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
GENERIC_AUTHORITY_SOURCE = "Repository editorial record"

SOURCE_RULES = (
    ("What Is And Is Not The Path", "what is and is not the path", "osf-house"),
    ("OSF glossary", "osf glossary", "osf-house"),
    ("Dhammarato", "dhammarato", "dhammarato"),
    ("Buddhadasa", "buddhadasa", "buddhadasa"),
    ("Idappaccayatā practical talk profile", "idappaccayatā practical talk profile", "buddhadasa-support"),
    ("Punnaji", "punnaji", "external"),
    ("Hillside / Ñāṇamoli", "hillside", "external"),
    ("Hillside / Ñāṇamoli", "nyanamoli", "external"),
    ("Hillside / Ñāṇamoli", "ñāṇamoli", "external"),
    ("Hillside / Ñāṇamoli", "path press", "external"),
)


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict[str, object]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def infer_authority_basis(data: dict[str, object]) -> list[dict[str, str]]:
    notes = str(data.get("notes", ""))
    lower_notes = notes.lower()
    results: list[dict[str, str]] = []

    for source, needle, priority in SOURCE_RULES:
        if needle in lower_notes:
            results.append(
                {
                    "source": source,
                    "priority": priority,
                    "kind": "rationale",
                    "scope": f"Named in notes as support for the current {data.get('term', data.get('normalized_term', 'term'))} policy.",
                }
            )

    if results:
        return results

    return [
        {
            "source": GENERIC_AUTHORITY_SOURCE,
            "priority": "osf-house",
            "kind": "rationale",
            "scope": "Current house policy is preserved from the existing rule-bearing entry; source-specific provenance still needs refinement.",
        }
    ]


def infer_compound_inheritance(data: dict[str, object]) -> str:
    notes = str(data.get("notes", "")).lower()
    rules = data.get("context_rules", [])
    if "compound" in notes:
        return "inherit"
    if isinstance(rules, list):
        for rule in rules:
            if isinstance(rule, dict) and "compound" in str(rule.get("context", "")).lower():
                return "inherit"
    return "case-by-case"


def infer_drift_risk(data: dict[str, object]) -> str:
    discouraged = data.get("discouraged_translations", [])
    if isinstance(discouraged, list) and discouraged:
        first = discouraged[0]
        if isinstance(first, str):
            return f"Prevents drift back toward '{first}' or other unrecorded alternates."
    return "Prevents unrecorded synonym drift away from the preferred rendering."


def infer_translation_policy(data: dict[str, object]) -> dict[str, str]:
    preferred = str(data.get("preferred_translation", data.get("normalized_term", "the term")))
    untranslated = data.get("untranslated_preferred") is True
    policy = {
        "default_scope": f"Use '{preferred}' as the default rendering in the entry's governed translation contexts unless a recorded context rule overrides it.",
        "when_not_to_apply": "Yield to recorded context_rules, source-facing technical use, or other explicitly documented local reasons rather than rotating among alternates ad hoc.",
        "compound_inheritance": infer_compound_inheritance(data),
        "drift_risk": infer_drift_risk(data),
    }
    if untranslated:
        policy["leave_untranslated_when"] = (
            "Leave the term untranslated when source-facing doctrinal range or local explanation would be narrowed too quickly by an English equivalent."
        )
        policy["when_not_to_apply"] = (
            "Do not force an English substitute when the local passage needs the Pali term; use a gloss only when the entry or passage explicitly calls for one."
        )
    return policy


def backfill_term(data: dict[str, object]) -> tuple[dict[str, object], bool]:
    changed = False
    if data.get("entry_type") != "major":
        return data, changed

    if not data.get("authority_basis"):
        data["authority_basis"] = infer_authority_basis(data)
        changed = True
    if not data.get("translation_policy"):
        data["translation_policy"] = infer_translation_policy(data)
        changed = True
    return data, changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Report how many files would change without writing them.",
    )
    args = parser.parse_args()

    if not TERMS_DIR.exists():
        print(f"ERROR: Terms directory not found: {TERMS_DIR}")
        return 1

    changed_paths: list[Path] = []
    for path in iter_term_files(TERMS_DIR):
        data = load_json(path)
        if not isinstance(data, dict):
            continue
        updated, changed = backfill_term(data)
        if changed:
            changed_paths.append(path)
            if not args.check_only:
                write_json(path, updated)

    if args.check_only:
        print(f"Would update {len(changed_paths)} file(s).")
    else:
        print(f"Updated {len(changed_paths)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

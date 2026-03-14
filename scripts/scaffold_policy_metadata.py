#!/usr/bin/env python3
"""Scaffold authority_basis and translation_policy blocks for major terms."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict[str, object]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def build_authority_basis_placeholder(term_name: str) -> list[dict[str, str]]:
    return [
        {
            "source": "TODO authority source",
            "priority": "osf-house",
            "kind": "rationale",
            "scope": f"TODO explain which policy for {term_name} this source supports.",
        }
    ]


def build_translation_policy_placeholder(data: dict[str, object]) -> dict[str, str]:
    preferred = data.get("preferred_translation", "TODO preferred translation")
    policy = {
        "default_scope": f"TODO describe where '{preferred}' is the default rendering.",
        "when_not_to_apply": "TODO describe where the default should yield to context or remain in Pali.",
        "compound_inheritance": "case-by-case",
        "drift_risk": "TODO describe the main translation drift or doctrinal confusion this policy prevents.",
    }
    if data.get("untranslated_preferred") is True:
        policy["leave_untranslated_when"] = (
            "TODO describe when leaving the term untranslated is preferred."
        )
    return policy


def select_targets(
    *,
    include_all_missing: bool,
    requested_terms: list[str],
) -> list[Path]:
    requested = {term.strip() for term in requested_terms if term.strip()}
    targets: list[Path] = []
    for path in sorted(TERMS_DIR.glob("*.json")):
        data = load_json(path)
        if not isinstance(data, dict) or data.get("entry_type") != "major":
            continue
        if requested and path.stem not in requested:
            continue
        if include_all_missing:
            if data.get("authority_basis") and data.get("translation_policy"):
                continue
        targets.append(path)
    return targets


def scaffold_file(path: Path) -> bool:
    data = load_json(path)
    if not isinstance(data, dict):
        raise ValueError(f"{path.name}: expected a JSON object")
    if data.get("entry_type") != "major":
        raise ValueError(f"{path.name}: only major entries can be scaffolded")

    changed = False
    if not data.get("authority_basis"):
        data["authority_basis"] = build_authority_basis_placeholder(str(data.get("term", path.stem)))
        changed = True
    if not data.get("translation_policy"):
        data["translation_policy"] = build_translation_policy_placeholder(data)
        changed = True

    if changed:
        write_json(path, data)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--all-missing",
        action="store_true",
        help="Scaffold every major term missing authority_basis or translation_policy.",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Show which files would be scaffolded without modifying them.",
    )
    parser.add_argument(
        "terms",
        nargs="*",
        help="Optional normalized terms to scaffold.",
    )
    args = parser.parse_args()

    if not TERMS_DIR.exists():
        print(f"ERROR: Terms directory not found: {TERMS_DIR}")
        return 1

    if not args.all_missing and not args.terms:
        print("ERROR: Provide one or more terms or use --all-missing.")
        return 1

    targets = select_targets(
        include_all_missing=args.all_missing,
        requested_terms=args.terms,
    )

    if not targets:
        print("No target terms selected.")
        return 0

    if args.check_only:
        for path in targets:
            print(path.name)
        print(f"Would scaffold {len(targets)} file(s).")
        return 0

    changed = 0
    for path in targets:
        if scaffold_file(path):
            changed += 1
            print(f"Scaffolded {path.name}")
        else:
            print(f"Skipped {path.name}: already complete")

    print(f"Updated {changed} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

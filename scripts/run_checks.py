#!/usr/bin/env python3
"""Run the repo verification suite with one command."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

try:
    from scripts.cluster_registry import build_cluster_checks
except ModuleNotFoundError:
    from cluster_registry import build_cluster_checks


REPO_ROOT = Path(__file__).resolve().parent.parent

PRE_CLUSTER_CHECKS: tuple[tuple[str, list[str]], ...] = (
    ("Regression tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests"]),
    ("Documentation integrity", [sys.executable, "scripts/check_docs_integrity.py"]),
    ("Translation surface registry", [sys.executable, "scripts/translation_surface_index.py", "--check"]),
    ("Generated docs freshness", [sys.executable, "scripts/check_generated_docs.py"]),
    ("Translation formula consistency", [sys.executable, "scripts/check_translation_formula_consistency.py"]),
    ("Voice consistency audit", [sys.executable, "scripts/voice_consistency_audit.py"]),
    ("Schema validation", [sys.executable, "scripts/validate_terms.py", "--strict"]),
    # Strict lint keeps structural warnings release-blocking in the combined flow.
    ("Editorial lint", [sys.executable, "scripts/lint_terms.py", "--strict"]),
    ("Term directory navigation", [sys.executable, "scripts/term_directory_navigation.py", "--check"]),
    ("Translation drift", [sys.executable, "scripts/check_translation_drift.py", "--strict"]),
    ("Cluster surface coverage", [sys.executable, "scripts/check_cluster_surfaces.py"]),
)

POST_CLUSTER_CHECKS: tuple[tuple[str, list[str]], ...] = (
    ("Coverage audit", [sys.executable, "scripts/audit_term_coverage.py"]),
    ("Repository health", [sys.executable, "scripts/repo_health.py", "--top", "10"]),
)


CHECKS: tuple[tuple[str, list[str]], ...] = (
    PRE_CLUSTER_CHECKS + build_cluster_checks(sys.executable) + POST_CLUSTER_CHECKS
)


def format_command(command: list[str]) -> str:
    return " ".join(command)


def repair_hint(label: str, command: list[str]) -> str | None:
    if label in {
        "Schema validation",
        "Editorial lint",
        "Translation drift",
        "Cluster surface coverage",
    }:
        return (
            "Repair hint: rerun the failing command directly. The script now prints "
            "the rule violated, why it matters, the minimal safe fix, and repo-native examples."
        )

    label_lower = label.casefold()
    if "cluster" in label_lower or "surface" in label_lower or label == "OSF reconciliation layer":
        return (
            "Repair hint: treat this as a family-level failure. Review the authority doc, "
            "repair the family terms or collective records in one pass, and rerun the family report directly."
        )

    return None


def main() -> int:
    for label, command in CHECKS:
        print(f"==> {label}")
        result = subprocess.run(command, cwd=REPO_ROOT)
        if result.returncode != 0:
            print(
                f"{label} failed with exit code {result.returncode}. "
                f"Command: {format_command(command)}"
            )
            hint = repair_hint(label, command)
            if hint is not None:
                print(hint)
            return result.returncode
        print()
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

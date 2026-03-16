#!/usr/bin/env python3
"""Run the repo verification suite with one command."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

CHECKS: tuple[tuple[str, list[str]], ...] = (
    ("Regression tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests"]),
    ("Documentation integrity", [sys.executable, "scripts/check_docs_integrity.py"]),
    ("Schema validation", [sys.executable, "scripts/validate_terms.py"]),
    # Strict lint keeps structural warnings release-blocking in the combined flow.
    ("Editorial lint", [sys.executable, "scripts/lint_terms.py", "--strict"]),
    ("Translation drift", [sys.executable, "scripts/check_translation_drift.py", "--strict"]),
    ("Dependent arising cluster", [sys.executable, "scripts/dependent_arising_cluster_report.py", "--strict"]),
    ("Five heaps cluster", [sys.executable, "scripts/five_heaps_cluster_report.py", "--strict"]),
    ("Identity-construction cluster", [sys.executable, "scripts/identity_construction_cluster_report.py", "--strict"]),
    ("Bondage / residue cluster", [sys.executable, "scripts/bondage_residue_cluster_report.py", "--strict"]),
    ("Bondage-imagery cluster", [sys.executable, "scripts/bondage_imagery_cluster_report.py", "--strict"]),
    ("Abandonment-sequence cluster", [sys.executable, "scripts/abandonment_sequence_cluster_report.py", "--strict"]),
    ("Craving / appropriation cluster", [sys.executable, "scripts/craving_appropriation_cluster_report.py", "--strict"]),
    ("Coverage audit", [sys.executable, "scripts/audit_term_coverage.py"]),
    ("Repository health", [sys.executable, "scripts/repo_health.py", "--top", "10"]),
)


def main() -> int:
    for label, command in CHECKS:
        print(f"==> {label}")
        result = subprocess.run(command, cwd=REPO_ROOT)
        if result.returncode != 0:
            print(f"{label} failed with exit code {result.returncode}.")
            return result.returncode
        print()
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

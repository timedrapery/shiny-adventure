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
    ("Term directory navigation", [sys.executable, "scripts/term_directory_navigation.py", "--check"]),
    ("Translation drift", [sys.executable, "scripts/check_translation_drift.py", "--strict"]),
    ("Dependent arising cluster", [sys.executable, "scripts/dependent_arising_cluster_report.py", "--strict"]),
    ("Jhana cluster", [sys.executable, "scripts/jhana_cluster_report.py", "--strict"]),
    ("Path-factor cluster", [sys.executable, "scripts/path_factor_cluster_report.py", "--strict"]),
    ("Four noble truths cluster", [sys.executable, "scripts/four_noble_truths_cluster_report.py", "--strict"]),
    ("Sense-fields cluster", [sys.executable, "scripts/sense_fields_cluster_report.py", "--strict"]),
    ("Five heaps cluster", [sys.executable, "scripts/five_heaps_cluster_report.py", "--strict"]),
    ("Identity-construction cluster", [sys.executable, "scripts/identity_construction_cluster_report.py", "--strict"]),
    ("Bondage / residue cluster", [sys.executable, "scripts/bondage_residue_cluster_report.py", "--strict"]),
    ("Bondage-imagery cluster", [sys.executable, "scripts/bondage_imagery_cluster_report.py", "--strict"]),
    ("Abandonment-sequence cluster", [sys.executable, "scripts/abandonment_sequence_cluster_report.py", "--strict"]),
    ("Crossing / release interface cluster", [sys.executable, "scripts/crossing_release_interface_cluster_report.py", "--strict"]),
    ("Consummation / unconditioned interface cluster", [sys.executable, "scripts/consummation_interface_cluster_report.py", "--strict"]),
    ("Emptiness / signless / wishless interface cluster", [sys.executable, "scripts/emptiness_signless_wishless_cluster_report.py", "--strict"]),
    ("OSF reconciliation layer", [sys.executable, "scripts/osf_reconciliation_report.py", "--strict"]),
    ("Knowledge / seeing / understanding cluster", [sys.executable, "scripts/knowledge_cluster_report.py", "--strict"]),
    ("Verbal knowing / recognition cluster", [sys.executable, "scripts/verbal_knowing_cluster_report.py", "--strict"]),
    ("Craving / appropriation cluster", [sys.executable, "scripts/craving_appropriation_cluster_report.py", "--strict"]),
    ("Kama cluster", [sys.executable, "scripts/kama_cluster_report.py", "--strict"]),
    ("Experience / process cluster", [sys.executable, "scripts/experience_process_cluster_report.py", "--strict"]),
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

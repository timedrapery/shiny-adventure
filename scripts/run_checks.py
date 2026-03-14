#!/usr/bin/env python3
"""Run the repo verification suite with one command."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

CHECKS: tuple[tuple[str, list[str]], ...] = (
    ("Regression tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests"]),
    ("Schema validation", [sys.executable, "scripts/validate_terms.py"]),
    ("Editorial lint", [sys.executable, "scripts/lint_terms.py", "--strict"]),
    ("Coverage audit", [sys.executable, "scripts/audit_term_coverage.py"]),
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

# Development Guide

This guide covers local setup, daily workflows, and safe contribution patterns.

## Environment Setup

```bash
python -m venv .venv
python -m pip install -r requirements-dev.txt
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## Daily Workflow

1. Create a branch focused on one coherent change set.
2. Edit terms, scripts, or docs.
3. Run targeted checks while iterating.
4. Run full checks before opening a pull request.

## Commands

Run all checks:

```bash
python scripts/run_checks.py
```

Run targeted checks:

```bash
python -m unittest discover -s tests
python scripts/validate_terms.py
python scripts/lint_terms.py
python scripts/check_translation_drift.py
python scripts/audit_term_coverage.py
python scripts/repo_health.py --top 10
```

## Working Safely With Editorial Data

- Keep changes small and traceable.
- For major term edits, inspect compounds and related terms in the same family.
- Document rationale in notes and authority fields where policy changes.
- Avoid introducing style drift through synonym rotation.

## Pull Request Expectations

A good pull request includes:

- clear summary of what changed
- explanation of editorial effect
- references used for authority-sensitive decisions
- confirmation that local checks passed

Use the repository templates in .github/ when filing issues or pull requests.

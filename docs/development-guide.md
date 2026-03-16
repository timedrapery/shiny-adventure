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

Use script help when you are unsure about flags or output format:

```bash
python scripts/check_docs_integrity.py --help
python scripts/repo_health.py --help
python scripts/scaffold_policy_metadata.py --help
```

Run targeted tests while working on one script or workflow:

```bash
python -m unittest tests.test_validate_terms -v
python -m unittest tests.test_lint_terms -v
python -m unittest tests.test_run_checks -v
```

For a broader index of CLI tools, see [../scripts/README.md](../scripts/README.md).

## Change-Type Guidance

- Term record change: validate JSON, run editorial lint, and check translation drift before moving on.
- Script change: run the most relevant tests first, then full checks before opening a pull request.
- Documentation change: update any affected cross-links and command examples in the same pass.

For documentation and repository-surface changes, run:

```bash
python scripts/check_docs_integrity.py
```

## Working Safely With Editorial Data

- Keep changes small and traceable.
- For major term edits, inspect compounds and related terms in the same family.
- Document rationale in notes and authority fields where policy changes.
- Avoid introducing style drift through synonym rotation.

## Windows Notes

- Use PowerShell activation with `.venv\Scripts\Activate.ps1`.
- Keep command examples repo-relative so they work across shells.
- If you need a JSON artifact for inspection, prefer redirecting script output rather than editing data by hand.

## Pull Request Expectations

A good pull request includes:

- clear summary of what changed
- explanation of editorial effect
- references used for authority-sensitive decisions
- confirmation that local checks passed

Use the repository templates in .github/ when filing issues or pull requests.

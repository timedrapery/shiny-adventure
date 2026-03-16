# Open Sangha Foundation Pali Translation Lexicon

[![Checks](https://github.com/timedrapery/shiny-adventure/actions/workflows/checks.yml/badge.svg)](https://github.com/timedrapery/shiny-adventure/actions/workflows/checks.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Structured Pali-to-English translation infrastructure for Early Buddhist work.
This repository stores translation policy as versioned data so term decisions stay explicit, reviewable, machine-checkable, and stable across texts.

## What This Repository Does

- encodes term decisions in schema-validated JSON records
- distinguishes major rule-bearing entries from lighter minor entries
- records preferred renderings, governed exceptions, rationale, and provenance
- runs lint, drift, coverage, and health checks in local workflows and CI
- supports candidate intake and review before promotion into the live lexicon

## What This Repository Is Not

- a generic dictionary
- a neutral all-traditions glossary
- an automatic translator
- a place for undocumented synonym rotation

Major entries are policy-bearing records. They exist to preserve translation discipline across doctrinal families, compounds, formulas, and recurring editorial situations.

## Start Here

- New to the project: [docs/project-overview.md](docs/project-overview.md)
- Need the documentation map: [docs/DOCUMENTATION_GUIDE.md](docs/DOCUMENTATION_GUIDE.md)
- Contributing term or workflow changes: [CONTRIBUTING.md](CONTRIBUTING.md)
- Working on scripts or tests: [docs/development-guide.md](docs/development-guide.md)
- Looking for command examples: [docs/usage.md](docs/usage.md)
- Want the script index: [scripts/README.md](scripts/README.md)

## Quick Start

### Prerequisites

- Python 3.11 or 3.12

### Setup

```bash
python -m venv .venv
python -m pip install -r requirements-dev.txt
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Full Verification

```bash
python scripts/run_checks.py
```

That command runs regression tests, schema validation, editorial lint, drift checks, coverage audit, and repository health reporting.

## Common Workflows

Validate a focused term change:

```bash
python scripts/validate_terms.py
python scripts/lint_terms.py
python scripts/check_translation_drift.py
```

Inspect repository-level health:

```bash
python scripts/repo_health.py --top 10
python scripts/audit_term_coverage.py --top 15
```

Run candidate intake:

```bash
python scripts/extract_candidate_terms.py path/to/source.txt
python scripts/generate_candidate_report.py
python scripts/scaffold_candidate_terms.py --priority create_now
```

Backfill policy metadata deliberately:

```bash
python scripts/policy_backfill_queue.py
python scripts/scaffold_policy_metadata.py --check-only --all-missing
python scripts/backfill_policy_metadata.py --check-only
```

For task-based command guidance, see [docs/usage.md](docs/usage.md).

## Repository Structure

```text
shiny-adventure/
|- terms/                  # Live lexicon records, split into major/ and minor/
|- schema/                 # JSON schema for term records
|- scripts/                # Validation, reporting, scaffolding, and helper tools
|- tests/                  # Regression tests for scripts and workflow behavior
|- candidates/             # Review-first intake area for proposed terms
|- docs/                   # Editorial standards, workflow docs, and planning notes
`- .github/                # CI workflow plus issue and PR templates
```

See [docs/architecture.md](docs/architecture.md) for the operating model and [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) for field-level definitions.

## Validation Stack

- schema validation keeps records structurally correct
- editorial lint checks policy completeness and internal consistency
- drift checks catch unstable renderings across related terms
- coverage audit flags missing doctrinal families
- repository health reports summarize machine-checkable maturity signals
- GitHub Actions runs the full suite on pushes and pull requests for Python 3.11 and 3.12

## Governance And House Style

- translation principles: [TERMINOLOGY_PRINCIPLES.md](TERMINOLOGY_PRINCIPLES.md)
- translation voice and house preferences: [STYLE_GUIDE.md](STYLE_GUIDE.md)
- authority order: [docs/OSF_EDITORIAL_AUTHORITY.md](docs/OSF_EDITORIAL_AUTHORITY.md)
- term entry requirements: [docs/TERM_ENTRY_STANDARD.md](docs/TERM_ENTRY_STANDARD.md)
- tags and status vocabulary: [docs/TAG_STATUS_VOCABULARY.md](docs/TAG_STATUS_VOCABULARY.md)

## Current Priorities

Current improvement work is focused on keeping the repository coherent as it grows: sharper onboarding, clearer workflow indexing, disciplined review of draft major entries, and continued maintenance of translation-policy quality.

Current review-queue and workflow surface tools include:

- `python scripts/draft_major_review_queue.py`
- `python scripts/check_docs_integrity.py`

Planning notes live in [docs/TRANSLATION_WORKFLOW_PLAN.md](docs/TRANSLATION_WORKFLOW_PLAN.md) and the latest review snapshot is in [docs/REPOSITORY_REVIEW_2026-03.md](docs/REPOSITORY_REVIEW_2026-03.md).

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Explain editorial effect clearly, especially when changing preferred translations, context rules, doctrinal families, or workflow checks.

## License

Licensed under the MIT License. See [LICENSE](LICENSE).

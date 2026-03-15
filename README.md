# Open Sangha Foundation Pali Translation Lexicon

[![Checks](https://github.com/timedrapery/shiny-adventure/actions/workflows/checks.yml/badge.svg)](https://github.com/timedrapery/shiny-adventure/actions/workflows/checks.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Structured Pali-to-English lexicon for Early Buddhist translation work.
This repository stores translation policy as data so term decisions stay explicit, reviewable, and stable across texts.

## Overview

This project combines:

- machine-validated term records
- editorial policy for doctrinally sensitive vocabulary
- lint and drift checks that protect consistency over time

It is not a generic dictionary. Major entries are policy-bearing records that define default renderings, context exceptions, and provenance.

## Why This Project Exists

Pali translation drift often appears gradually through inconsistent wording, undocumented exceptions, and untracked source influence. This repository exists to prevent that drift by treating terminology decisions as versioned, testable artifacts.

## Features

- JSON-schema-backed term records
- explicit major/minor entry model
- strict linting and drift checks for editorial quality
- repository health reporting for policy coverage gaps
- candidate intake workflow for review-first term expansion
- contributor documentation for style, authority, and term construction

## Repository Structure

```text
shiny-adventure/
|- terms/                  # Lexicon entries (major/ and minor/)
|- schema/                 # JSON schema for term records
|- scripts/                # Validation, linting, reporting, scaffolding utilities
|- tests/                  # Unit tests for scripts and workflows
|- candidates/             # Candidate term intake and review outputs
|- docs/                   # Editorial standards and workflow documentation
`- .github/                # CI workflow and issue/PR templates
```

See [docs/project-overview.md](docs/project-overview.md) for a guided map.

## Getting Started

### Prerequisites

- Python 3.11 or 3.12

### Setup

```bash
python -m venv .venv
python -m pip install -r requirements-dev.txt
```

### Validate the Repository

```bash
python scripts/run_checks.py
```

## Usage

Run targeted tooling during editorial work:

```bash
python scripts/validate_terms.py
python scripts/lint_terms.py
python scripts/check_translation_drift.py
python scripts/repo_health.py --top 10
```

Generate and review candidate terms:

```bash
python scripts/extract_candidate_terms.py path/to/source.txt
python scripts/generate_candidate_report.py
python scripts/scaffold_candidate_terms.py --priority create_now
```

See [docs/usage.md](docs/usage.md) for practical command recipes.

## Development

- contributor workflow: [CONTRIBUTING.md](CONTRIBUTING.md)
- development guide: [docs/development-guide.md](docs/development-guide.md)
- documentation index: [docs/DOCUMENTATION_GUIDE.md](docs/DOCUMENTATION_GUIDE.md)

## Roadmap

Current priorities focus on:

- reducing unresolved drift-risk clusters
- improving policy completeness on major terms
- tightening source provenance quality in examples

Planning details are tracked in [docs/TRANSLATION_WORKFLOW_PLAN.md](docs/TRANSLATION_WORKFLOW_PLAN.md) and [docs/REPOSITORY_REVIEW_2026-03.md](docs/REPOSITORY_REVIEW_2026-03.md).

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Run local checks and describe editorial impact clearly, especially for preferred translation or context rule changes.

## License

Licensed under the MIT License. See [LICENSE](LICENSE).

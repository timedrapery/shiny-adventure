# Open Sangha Foundation Pali Translation Lexicon

[![CI](https://github.com/timedrapery/shiny-adventure/actions/workflows/ci.yml/badge.svg)](https://github.com/timedrapery/shiny-adventure/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Structured Pali-to-English translation infrastructure for early Buddhist translation work.
This repository stores translation policy as versioned data so term decisions stay explicit, reviewable, machine-checkable, and stable across texts.

New here:

1. Read [docs/project-overview.md](docs/project-overview.md) for the operating model.
2. Use [docs/documentation-guide.md](docs/documentation-guide.md) as the main map of the docs set.
3. Read [docs/development-guide.md](docs/development-guide.md) and [CONTRIBUTING.md](CONTRIBUTING.md) before editing live data.
4. If you are working from raw source text rather than refining existing entries, start with [candidates/README.md](candidates/README.md) instead of writing directly into `terms/`.

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

## Source of Truth

The repository uses a clear source-of-truth stack:

- `terms/major/` and `terms/minor/` hold the live governed lexicon
- top-level governance docs and normative docs in `docs/` explain how those records should be written and reviewed
- `candidates/` holds intake evidence that has not yet become live policy
- `docs/generated/` holds derived reference material for browsing, review, and translation support

If a generated sheet or report looks wrong, fix the live term data or the generating script first. Do not settle policy in generated docs.

## How Live Policy Enters the Repo

The repository uses a review-first path:

1. Raw source vocabulary is first handled in [`candidates/`](candidates/README.md), not in the live lexicon.
2. Confirmed editorial decisions are encoded in `terms/major/` or `terms/minor/`.
3. Scripts and tests validate structure, drift resistance, provenance, and workflow behavior.
4. Generated docs in [`docs/generated/`](docs/generated/generated-docs-guide.md) provide reference surfaces, but they do not replace the live policy records.

Typical candidate outputs include:

- `candidates/candidate_terms.json`
- `candidates/candidate_terms.md`
- `candidates/scaffolds/*.review.json`

Those files are review material. They do not become governed lexicon content until an editor makes an explicit live-entry decision.

## Start Here

- New to the project: [docs/project-overview.md](docs/project-overview.md)
- Need the documentation map: [docs/documentation-guide.md](docs/documentation-guide.md)
- Contributing term or workflow changes: [CONTRIBUTING.md](CONTRIBUTING.md)
- Working on scripts or tests: [docs/development-guide.md](docs/development-guide.md)
- Looking for command examples: [docs/usage.md](docs/usage.md)
- Want the script index: [scripts/README.md](scripts/README.md)
- Need term-directory navigation: [terms/README.md](terms/README.md)
- Working from extracted candidates: [candidates/README.md](candidates/README.md)
- Need generated reference-material guidance: [docs/generated/generated-docs-guide.md](docs/generated/generated-docs-guide.md)

## First Contribution Paths

- Revising existing live policy: start in [terms/README.md](terms/README.md), then use [docs/term-entry-standard.md](docs/term-entry-standard.md) and [docs/data-dictionary.md](docs/data-dictionary.md).
- Working from raw source text: start in [candidates/README.md](candidates/README.md) and [docs/candidate-term-workflow.md](docs/candidate-term-workflow.md).
- Changing workflow code or checks: start in [docs/development-guide.md](docs/development-guide.md) and [scripts/README.md](scripts/README.md).
- Checking project-level rules before any edit: read [TERMINOLOGY_PRINCIPLES.md](TERMINOLOGY_PRINCIPLES.md), [STYLE_GUIDE.md](STYLE_GUIDE.md), [docs/MODERN_ENGLISH_POLICY.md](docs/MODERN_ENGLISH_POLICY.md), and [docs/VOICE_STANDARD.md](docs/VOICE_STANDARD.md).

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

## Repository Map

| Path | Role | Start here |
| --- | --- | --- |
| `terms/` | Live lexicon and translation policy records | [terms/README.md](terms/README.md) |
| `schema/` | Structural contract for term records | [docs/data-dictionary.md](docs/data-dictionary.md) |
| `scripts/` | Validation, drift checks, reports, scaffolding, and helper tooling | [scripts/README.md](scripts/README.md) |
| `tests/` | Regression coverage for scripts and repository workflows | [docs/development-guide.md](docs/development-guide.md) |
| `candidates/` | Review-first intake area for source extraction output | [candidates/README.md](candidates/README.md) |
| `docs/` | Normative policy docs, workflow guides, planning notes, and reference material | [docs/documentation-guide.md](docs/documentation-guide.md) |
| `docs/generated/` | Generated reference outputs derived from live policy and audit scripts | [docs/generated/generated-docs-guide.md](docs/generated/generated-docs-guide.md) |

See [docs/architecture.md](docs/architecture.md) for the operating model and [docs/data-dictionary.md](docs/data-dictionary.md) for field-level definitions.

The live `terms/major/` and `terms/minor/` directories stay flat on disk; use
[terms/README.md](terms/README.md) and the generated term indexes for human
navigation rather than adding subfolders.

## Validation Stack

- schema validation keeps records structurally correct
- editorial lint checks policy completeness and internal consistency
- drift checks catch unstable renderings across related terms
- coverage audit flags missing doctrinal families
- repository health reports summarize machine-checkable maturity signals
- GitHub Actions runs the full suite on pushes and pull requests for Python 3.11 and 3.12

## Governance and Style

- translation principles: [TERMINOLOGY_PRINCIPLES.md](TERMINOLOGY_PRINCIPLES.md)
- translation voice and house preferences: [STYLE_GUIDE.md](STYLE_GUIDE.md)
- modern-English register policy: [docs/MODERN_ENGLISH_POLICY.md](docs/MODERN_ENGLISH_POLICY.md)
- voice-standard sentence patterns: [docs/VOICE_STANDARD.md](docs/VOICE_STANDARD.md)
- authority order: [docs/osf-editorial-authority.md](docs/osf-editorial-authority.md)
- term entry requirements: [docs/term-entry-standard.md](docs/term-entry-standard.md)
- tags and status vocabulary: [docs/tag-status-vocabulary.md](docs/tag-status-vocabulary.md)
- generated-reference guidance: [docs/generated/generated-docs-guide.md](docs/generated/generated-docs-guide.md)

## Current Priorities

The live lexicon no longer has a draft major or minor queue. Current work is focused on expanding translation-facing text surfaces around already-governed clusters, refining supporting entries when live translation exposes pressure, and keeping generated and documentation surfaces synchronized with the live dataset.

Current maintenance and workflow surface tools include:

- `python scripts/check_docs_integrity.py`
- `python scripts/check_generated_docs.py`
- `python scripts/translation_surface_index.py --check`
- `python scripts/run_checks.py`

Planning notes live in [docs/translation-workflow-plan.md](docs/translation-workflow-plan.md) and the latest review snapshot is in [docs/repository-review-2026-03.md](docs/repository-review-2026-03.md).

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Explain editorial effect clearly, especially when changing preferred translations, context rules, doctrinal families, or workflow checks.

## License

Licensed under the MIT License. See [LICENSE](LICENSE).

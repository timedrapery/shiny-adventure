# Contributing

Contributions should improve clarity, consistency, and reusability across the lexicon. This repository treats term records as editorial policy objects, so even small wording changes can affect downstream translation behavior.

For a concise reference on translation voice and house preferences, read [STYLE_GUIDE.md](STYLE_GUIDE.md) before making any entry changes.

By participating in this project, you agree to follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Before You Start

Read these documents in order:

1. [README.md](README.md)
2. [docs/project-overview.md](docs/project-overview.md)
3. [docs/development-guide.md](docs/development-guide.md)
4. [TERMINOLOGY_PRINCIPLES.md](TERMINOLOGY_PRINCIPLES.md)
5. [STYLE_GUIDE.md](STYLE_GUIDE.md)
6. [docs/osf-editorial-authority.md](docs/osf-editorial-authority.md)
7. [docs/data-dictionary.md](docs/data-dictionary.md)
8. [docs/term-entry-standard.md](docs/term-entry-standard.md)
9. [docs/tag-status-vocabulary.md](docs/tag-status-vocabulary.md)

If you are editing compounds or recurring formulas, also read [docs/headword-compound-formula-policy.md](docs/headword-compound-formula-policy.md).
If you are changing review status on a major entry, also read [docs/review-status-model.md](docs/review-status-model.md).

## Choose The Right Contribution Path

- Term record change: read the editorial documents above, inspect related headwords and compounds, and run validation plus linting before opening a pull request.
- Script or validation change: read [docs/development-guide.md](docs/development-guide.md), keep behavior deterministic, and add or update tests in `tests/`.
- Documentation change: keep wording explicit and repository-native, and update cross-links when changing workflow guidance.

## Contribution Types

Typical contributions include:

- adding or revising term entries in `terms/`
- improving schema-backed validation or linting in `scripts/`
- clarifying style and contributor documentation
- strengthening drift protection for doctrinally sensitive term families

## Editorial Expectations

- Preserve existing doctrinal decisions unless a change is explicitly justified within the repository's authority order.
- Do not replace a preferred translation simply because another English gloss is common elsewhere.
- Use `notes`, `context_rules`, and `translation_policy` to make important decisions explicit.
- When editing a major term, review linked compounds, formulas, and related terms in the same family.
- Keep filenames ASCII-safe and aligned with `normalized_term`.
- Use lowercase-kebab-case for Markdown files in `docs/`.
- Use UTF-8 encoding and preserve full Pali diacritics in `term`, examples, and documentation.

## Workflow

1. Create a focused branch.
2. Make the smallest coherent change set.
3. Run the smallest useful local checks while iterating.
4. Open a pull request that explains the editorial effect of the change.

Example setup:

```bash
git clone https://github.com/timedrapery/shiny-adventure.git
cd shiny-adventure
git checkout -b improve-term-policy
python -m venv .venv
python -m pip install -r requirements-dev.txt
python scripts/run_checks.py
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Working Loop

For most term edits, this is the practical minimum:

```bash
python scripts/validate_terms.py
python scripts/lint_terms.py
python scripts/check_translation_drift.py
```

Before opening a pull request, run the full suite:

```bash
python scripts/run_checks.py
```

If you are changing workflow code, use targeted tests while iterating:

```bash
python -m unittest tests.test_validate_terms -v
python -m unittest tests.test_lint_terms -v
```

Every CLI script in `scripts/` supports `--help`. See [scripts/README.md](scripts/README.md) for a repository-level index.

When reviewing status work on major entries, inspect the current queue with:

```bash
python scripts/draft_major_review_queue.py
```

## Working With Term Records

Contributor shorthand maps to live schema fields as follows:

- preferred rendering -> `preferred_translation`
- translation rule -> `context_rules`
- usage notes -> `notes`
- examples -> `example_phrases`
- provenance -> `authority_basis`
- drift-control summary -> `translation_policy`

For major entries, the repository expects those fields to function together rather than independently.

## Validation Checklist

Before opening a pull request, confirm:

- the JSON is valid
- the entry matches [schema/PALI_TERM_SCHEMA.json](schema/PALI_TERM_SCHEMA.json)
- the wording matches [STYLE_GUIDE.md](STYLE_GUIDE.md)
- authority-sensitive changes respect [docs/osf-editorial-authority.md](docs/osf-editorial-authority.md)
- tags and status values match [docs/tag-status-vocabulary.md](docs/tag-status-vocabulary.md)
- major-entry edits include enough rationale to prevent drift later

Recommended commands:

```bash
python -m unittest discover -s tests
python scripts/validate_terms.py
python scripts/lint_terms.py
python scripts/check_translation_drift.py
python scripts/repo_health.py
python scripts/run_checks.py
```

If your change affects candidate intake, metadata backfill, or repo reporting, also review the task-based commands in [docs/usage.md](docs/usage.md).
If your change touches Markdown or repository metadata, run `python scripts/check_docs_integrity.py` as part of the local check loop.

## Pull Requests

Pull requests should state:

- what changed
- why the change was necessary
- whether any preferred translation, context rule, or doctrinal family was affected
- whether validation was run locally
- what references or authority basis support the change, if applicable

Use the repository templates when opening issues or pull requests.

## Security

For vulnerability reporting, follow [SECURITY.md](SECURITY.md). Do not disclose suspected security issues in public issues.

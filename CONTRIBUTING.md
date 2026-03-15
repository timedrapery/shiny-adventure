# Contributing to shiny-adventure

Contributions should improve clarity, consistency, and reusability across the lexicon. This repository treats term records as editorial policy objects, so even small wording changes can affect downstream translation behavior.

## Before You Start

Read these documents in order:

1. [README.md](README.md)
2. [TERMINOLOGY_PRINCIPLES.md](TERMINOLOGY_PRINCIPLES.md)
3. [STYLE_GUIDE.md](STYLE_GUIDE.md)
4. [docs/OSF_EDITORIAL_AUTHORITY.md](docs/OSF_EDITORIAL_AUTHORITY.md)
5. [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md)
6. [docs/TERM_ENTRY_STANDARD.md](docs/TERM_ENTRY_STANDARD.md)
7. [docs/TAG_STATUS_VOCABULARY.md](docs/TAG_STATUS_VOCABULARY.md)

If you are editing compounds or recurring formulas, also read [docs/HEADWORD_COMPOUND_FORMULA_POLICY.md](docs/HEADWORD_COMPOUND_FORMULA_POLICY.md).

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
- Use UTF-8 encoding and preserve full Pali diacritics in `term`, examples, and documentation.

## Workflow

1. Create a focused branch.
2. Make the smallest coherent change set.
3. Run validation locally.
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
- authority-sensitive changes respect [docs/OSF_EDITORIAL_AUTHORITY.md](docs/OSF_EDITORIAL_AUTHORITY.md)
- tags and status values match [docs/TAG_STATUS_VOCABULARY.md](docs/TAG_STATUS_VOCABULARY.md)
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

## Pull Requests

Pull requests should state:

- what changed
- why the change was necessary
- whether any preferred translation, context rule, or doctrinal family was affected
- whether validation was run locally
- what references or authority basis support the change, if applicable

Use the repository templates when opening issues or pull requests.

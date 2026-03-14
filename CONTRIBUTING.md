# Contributing to Shiny Adventure

Thanks for contributing. The most helpful contributions are the ones that make
the dataset clearer, more consistent, and easier to extend.

## What This Repo Contains

Shiny Adventure is a structured Pali translation dataset. Most contributions
will involve one or more of these areas:

- editing term files in [terms/](terms)
- refining the schema in [schema/PALI_TERM_SCHEMA.json](schema/PALI_TERM_SCHEMA.json)
- improving the style guide in [STYLE_GUIDE.md](STYLE_GUIDE.md)
- clarifying editorial documentation in [docs/](docs)

In the current schema, contributor shorthand maps to the live JSON fields like
this:

- preferred rendering -> `preferred_translation`
- translation rule -> `context_rules`
- usage notes -> `notes`
- examples -> `example_phrases`

## First-Time Contributor Path

If this is your first change, a good starting flow is:

1. Read [STYLE_GUIDE.md](STYLE_GUIDE.md).
2. Read [docs/OSF_EDITORIAL_AUTHORITY.md](docs/OSF_EDITORIAL_AUTHORITY.md).
3. Use [docs/DOCUMENTATION_GUIDE.md](docs/DOCUMENTATION_GUIDE.md) for the recommended documentation path.
4. Read [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md).
5. Read [docs/TAG_STATUS_VOCABULARY.md](docs/TAG_STATUS_VOCABULARY.md).
6. Review one or two existing entries in [terms/](terms).
7. Make a small change such as improving notes, adding tags, or drafting one new term.

## Contribution Workflow

1. Fork the repository.
2. Clone your fork locally.
3. Create a branch for your change.
4. Make your edits.
5. Run the full checks.
6. Open a pull request with a clear summary of what changed and why.

Example commands:

```bash
git clone https://github.com/timedrapery/shiny-adventure.git
cd shiny-adventure
git checkout -b improve-term-entry
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/run_checks.py
```

On Windows PowerShell, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Editing Expectations

- Keep filenames ASCII-safe and aligned with `normalized_term`.
- Preserve current OSF house preferences unless you are intentionally proposing a change under [docs/OSF_EDITORIAL_AUTHORITY.md](docs/OSF_EDITORIAL_AUTHORITY.md).
- Use notes and context rules to explain important editorial choices.
- For major entries, avoid definition-only edits that leave the rendering policy implicit.
- If you edit a doctrinal anchor term, also review its core compounds, formula examples, and linked doctrinal neighbors so the family does not drift.
- Prefer small, focused pull requests over large mixed edits.
- When editing or generating files on Windows, use a UTF-8-aware editor or a script that writes UTF-8 explicitly.
- For bulk entry creation, prefer `python scripts/write_term_batch.py path/to/batch.json` over shell redirection or terminal paste.
- Install dependencies from `requirements-dev.txt` so local checks match CI.
- Be aware that `python scripts/run_checks.py` runs editorial lint in strict mode, so warnings such as non-reciprocal `related_terms` links must be fixed before the full suite will pass.

## Before Opening a Pull Request

Please check the following:

- The JSON is valid.
- The entry matches the schema.
- The wording is consistent with [STYLE_GUIDE.md](STYLE_GUIDE.md).
- The wording follows [docs/OSF_EDITORIAL_AUTHORITY.md](docs/OSF_EDITORIAL_AUTHORITY.md) when source priorities matter.
- The tags and status values follow [docs/TAG_STATUS_VOCABULARY.md](docs/TAG_STATUS_VOCABULARY.md).
- New major entries include notes, context rules, related terms, and example phrases.
- Doctrinal anchor entries state when the default rendering applies, when it does not, and what nearby compounds or formulas inherit the rule.
- The pull request description explains any non-obvious translation decision.

## Validation Commands

Use these commands when you want more targeted feedback than the full suite:

```bash
python -m unittest discover -s tests
python scripts/validate_terms.py
python scripts/lint_terms.py
python scripts/audit_term_coverage.py
```

Use `python scripts/run_checks.py` when you want the same combined workflow the
repository uses in CI.

## Review Notes

Reviews will focus on:

- schema correctness
- consistency with the style guide
- consistency with the OSF authority hierarchy
- clarity of definitions and notes
- whether translation decisions are explicit enough to be reusable

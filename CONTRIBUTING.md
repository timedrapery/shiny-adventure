# Contributing to Shiny Adventure

Thanks for contributing. This project is still early, so the most helpful
contributions are the ones that make the dataset clearer, more consistent, and
easier to extend.

## What This Repo Contains

Shiny Adventure is a structured Pali translation dataset. Most contributions
will involve one or more of these areas:

- editing term files in [`terms/`](terms)
- refining the schema in [`schema/PALI_TERM_SCHEMA.json`](schema/PALI_TERM_SCHEMA.json)
- improving the style guide in [`STYLE_GUIDE.md`](STYLE_GUIDE.md)
- clarifying editorial documentation in [`docs/`](docs)

## First-Time Contributor Path

If this is your first change, a good starting flow is:

1. Read [`STYLE_GUIDE.md`](STYLE_GUIDE.md).
2. Read [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md).
3. Read [`docs/TAG_STATUS_VOCABULARY.md`](docs/TAG_STATUS_VOCABULARY.md) before adding tags or setting an entry status.
4. Review one or two existing entries in [`terms/`](terms).
5. Make a small change such as improving notes, adding tags, or drafting one new term.

## Contribution Workflow

1. Fork the repository.
2. Clone your fork locally.
3. Create a branch for your change.
4. Make your edits.
5. Validate the term files against the schema.
6. Open a pull request with a clear summary of what changed and why.

Example commands:

```bash
git clone https://github.com/timedrapery/shiny-adventure.git
cd shiny-adventure
git checkout -b improve-term-entry
python -m pip install jsonschema
python scripts/validate_terms.py
```

## Editing Expectations

- Keep filenames ASCII-safe and aligned with `normalized_term`.
- Preserve project translation preferences unless you are intentionally proposing a change.
- Use notes and context rules to explain important editorial choices.
- Prefer small, focused pull requests over large mixed edits.

## Before Opening a Pull Request

Please check the following:

- The JSON is valid.
- The entry matches the schema.
- The wording is consistent with [`STYLE_GUIDE.md`](STYLE_GUIDE.md).
- The tags and status values follow [`docs/TAG_STATUS_VOCABULARY.md`](docs/TAG_STATUS_VOCABULARY.md).
- New major entries include notes, context rules, related terms, and example phrases.
- The pull request description explains any non-obvious translation decision.

## Review Notes

Reviews will focus on:

- schema correctness
- consistency with the style guide
- clarity of definitions and notes
- whether translation decisions are explicit enough to be reusable

## Questions and Discussion

If you are unsure about a translation choice, schema change, or editorial rule,
opening an issue or a draft pull request is completely fine. Early discussion is
often the fastest way to improve the dataset.

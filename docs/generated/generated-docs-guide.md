# Generated Docs Guide

## Purpose

This directory contains generated reference material produced from live term
records and audit scripts.

These files help translators and reviewers, but they do not set house policy.

## Source of Truth

The source of truth remains:

- live term records in `terms/`
- normative policy docs in `docs/`
- schema and validation logic in `schema/` and `scripts/`

Generated files summarize that policy. They do not replace it.

## When to Use These Files

Use generated docs when you need:

- human navigation over the flat `terms/` directories
- translator-facing cluster summaries
- consistency sheets or review briefs derived from governed term data
- quick reference material for active translation work

Do not use generated docs as the primary place to settle policy disputes or
record new translation rules.

## What Lives Here

Typical generated outputs include:

- major and minor term indexes
- cluster glossaries
- formula sheets
- contrast sheets
- translator briefs
- reconciliation and consistency reports

## How These Files Are Produced

Most files here are written by commands under `scripts/`, including:

- `python scripts/term_directory_navigation.py --write-docs`
- `python scripts/*_cluster_report.py --write-docs`
- `python scripts/check_generated_docs.py`

Use [../documentation-guide.md](../documentation-guide.md) and
[../../scripts/README.md](../../scripts/README.md) to find the right generator
for a given output.

## Editing Generated Docs

Do not use these files as the main place to change policy.

When a generated file looks wrong:

1. fix the live term data or the generating script
2. regenerate the file
3. rerun checks

The repository now checks generated-doc freshness directly with:

```bash
python scripts/check_generated_docs.py
```

If you make a deliberate manual touch-up to a generated file, also fix the
upstream generator or live data in the same pass so the output does not drift
back on the next regeneration.

## Common Uses

Use generated docs when you need:

- a browsing surface over flat term directories
- a translator-facing summary of a governed family surface
- a practice-text control sheet for shared translation formulas
- a quick consistency sheet for review

Use the normative docs and live term entries when you need to decide what the
policy actually is.

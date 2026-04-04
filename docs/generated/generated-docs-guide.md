# Generated Docs Guide

## Purpose

This directory contains generated reference material produced from live term
records and audit scripts.

These files are useful for translators and reviewers, but they are not the
normative source of house policy.

## Source Of Truth

The source of truth remains:

- live term records in `terms/`
- normative policy docs in `docs/`
- schema and validation logic in `schema/` and `scripts/`

Generated files summarize that policy. They do not replace it.

## When To Use These Files

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

Use [../documentation-guide.md](../documentation-guide.md) and
[../../scripts/README.md](../../scripts/README.md) to find the right generator
for a given output.

## Editing Rule

Do not treat these files as the primary place to make policy changes.

When a generated file looks wrong:

1. fix the live term data or the generating script
2. regenerate the file
3. rerun checks

If you make a deliberate manual touch-up to a generated file, also fix the
upstream generator or live data in the same pass so the output does not drift
back on the next regeneration.

## Practical Use

Use generated docs when you need:

- a browsing surface over flat term directories
- a translator-facing summary of a doctrinal cluster
- a quick consistency sheet for review

Use the normative docs and live term entries when you need to decide what the
policy actually is.

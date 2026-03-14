# Documentation Guide

This folder contains the editorial and structural reference material for
**shiny-adventure**.

If you are new to the project, this is the recommended reading order:

1. [`../README.md`](../README.md)
   Start here for the project overview and repository layout.
2. [`../STYLE_GUIDE.md`](../STYLE_GUIDE.md)
   Read this to understand the project's translation voice and core preferences.
3. [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md)
   Use this as the field-by-field reference for term records.
4. [`TERM_ENTRY_STANDARD.md`](TERM_ENTRY_STANDARD.md)
   Use this when creating or revising a term entry.
5. [`TAG_STATUS_VOCABULARY.md`](TAG_STATUS_VOCABULARY.md)
   Check this before choosing tags or assigning an editorial status.

## What Each Document Does

- [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md)
  Defines the dataset fields and how they should be used.
- [`TERM_ENTRY_STANDARD.md`](TERM_ENTRY_STANDARD.md)
  Explains how to build a good entry and what major entries should contain.
- [`TAG_STATUS_VOCABULARY.md`](TAG_STATUS_VOCABULARY.md)
  Standardizes tag choices and status values.
- [`PUNNAJI_USAGE_PROFILE.md`](PUNNAJI_USAGE_PROFILE.md)
  Records a source-backed translation profile from Ven. Dr. M. Punnaji for
  use in notes and context rules.
- [`OSF_GLOSSARY_PROFILE.md`](OSF_GLOSSARY_PROFILE.md)
  Records a source-backed glossary profile from the local OSF glossary for
  use in notes, alternates, and new-term intake.
- [`BUDDHADASA_USAGE_PROFILE.md`](BUDDHADASA_USAGE_PROFILE.md)
  Records a source-backed term profile from selected Buddhadasa Bhikkhu works
  for use in notes, context rules, and new-term intake.
- [`../STYLE_GUIDE.md`](../STYLE_GUIDE.md)
  Captures the project's translation style and recurring rendering preferences.

## Practical Workflow

When editing or adding a term:

1. Check the style guidance first.
2. Confirm the field meanings in the data dictionary.
3. Follow the term entry standard while drafting.
4. Choose tags and status from the standard vocabulary.
5. Run `python scripts/run_checks.py` before committing.

## External Source Profiles

When a local source or author strongly influences a rendering decision:

1. Add the rendering first as an alternate or source-specific context rule.
2. Mention the source influence explicitly in `notes`.
3. Prefer a small number of named source profiles over silent drift in house
   terminology.
4. Only replace the current `preferred_translation` when the project has made
   a deliberate editorial decision to do so.

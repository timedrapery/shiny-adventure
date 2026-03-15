# Documentation Guide

This folder contains the editorial and structural reference material for
**shiny-adventure**.

If you are new to the project, this is the recommended reading order:

1. [`../README.md`](../README.md)
   Start here for the project overview and repository layout.
2. [`project-overview.md`](project-overview.md)
  Read this for a concise explanation of scope, entry model, and design
  intent.
3. [`architecture.md`](architecture.md)
  Read this to understand how data, scripts, tests, and review layers fit
  together.
4. [`development-guide.md`](development-guide.md)
  Use this for environment setup, workflow expectations, and command usage.
5. [`usage.md`](usage.md)
  Use this as a command reference while working.
6. [`../TERMINOLOGY_PRINCIPLES.md`](../TERMINOLOGY_PRINCIPLES.md)
   Read this for the repository's baseline rules for preferred renderings, exceptions, and drift prevention.
7. [`../STYLE_GUIDE.md`](../STYLE_GUIDE.md)
   Read this to understand the project's translation voice and core preferences.
8. [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md)
   Use this as the field-by-field reference for term records.
9. [`TERM_ENTRY_STANDARD.md`](TERM_ENTRY_STANDARD.md)
   Use this when creating or revising a term entry.
10. [`TAG_STATUS_VOCABULARY.md`](TAG_STATUS_VOCABULARY.md)
   Check this before choosing tags or assigning an editorial status.
11. [`HEADWORD_COMPOUND_FORMULA_POLICY.md`](HEADWORD_COMPOUND_FORMULA_POLICY.md)
   Read this when a term decision needs to propagate into compounds or formula
   usage.
12. [`EDITORIAL_REVIEW_CHECKLIST.md`](EDITORIAL_REVIEW_CHECKLIST.md)
   Use this before merging a PR or promoting a major entry to a mature review
   state.
13. [`BULK_EDITING_PLAYBOOK.md`](BULK_EDITING_PLAYBOOK.md)
   Use this when adding or revising many terms in one pass.
14. [`DRIFT_RISK_TERMS.md`](DRIFT_RISK_TERMS.md)
    Review this before changing high-instability doctrinal terms.
15. [`TRANSLATION_WORKFLOW_PLAN.md`](TRANSLATION_WORKFLOW_PLAN.md)
   Read this for the current repo-shaping roadmap and next editorial phase.
16. [`REPOSITORY_REVIEW_2026-03.md`](REPOSITORY_REVIEW_2026-03.md)
   Read this for the latest high-confidence structural review notes and open
   cleanup priorities.

## What Each Document Does

- [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md)
  Defines the dataset fields and how they should be used.
- [`project-overview.md`](project-overview.md)
  Explains project scope, intended usage, and entry model for new
  contributors.
- [`architecture.md`](architecture.md)
  Describes how term data, schema, scripts, tests, and checks work together.
- [`development-guide.md`](development-guide.md)
  Defines setup, workflow, and safe contribution practices for maintainers.
- [`usage.md`](usage.md)
  Provides practical command recipes for validation, linting, and reporting.
- [`TERM_ENTRY_STANDARD.md`](TERM_ENTRY_STANDARD.md)
  Explains how to build a good entry and what major entries should contain.
- [`DRIFT_RISK_TERMS.md`](DRIFT_RISK_TERMS.md)
  Identifies the doctrinal terms most likely to cause translation instability.
- [`HEADWORD_COMPOUND_FORMULA_POLICY.md`](HEADWORD_COMPOUND_FORMULA_POLICY.md)
  Defines how translation policy should be divided between headwords,
  compounds, and formulas.
- [`EDITORIAL_REVIEW_CHECKLIST.md`](EDITORIAL_REVIEW_CHECKLIST.md)
  Defines the review gate for structural quality, provenance, and family-level
  drift control.
- [`DECISION_RECORD_TEMPLATE.md`](DECISION_RECORD_TEMPLATE.md)
  Provides a lightweight pattern for recording major editorial decisions that
  should not live only in commit history.
- [`BULK_EDITING_PLAYBOOK.md`](BULK_EDITING_PLAYBOOK.md)
  Defines a safe operating pattern for 50+ term changes without family drift.
- [`TRANSLATION_WORKFLOW_PLAN.md`](TRANSLATION_WORKFLOW_PLAN.md)
  Defines the current roadmap for making the repo translation-ready by
  doctrinal cluster.
- [`REPOSITORY_REVIEW_2026-03.md`](REPOSITORY_REVIEW_2026-03.md)
  Records the March 2026 structural review findings, especially where
  translation drift risk should be handled by maintainers rather than patched
  mechanically.
- [`TAG_STATUS_VOCABULARY.md`](TAG_STATUS_VOCABULARY.md)
  Standardizes tag choices and status values.
- [`PUNNAJI_USAGE_PROFILE.md`](PUNNAJI_USAGE_PROFILE.md)
  Records a source-backed translation profile from Ven. Dr. M. Punnaji for
  use in notes and context rules.
- [`OSF_GLOSSARY_PROFILE.md`](OSF_GLOSSARY_PROFILE.md)
  Records glossary guidance from the local OSF glossary as an internal OSF
  house-material source for notes, alternates, defaults, and new-term intake.
- [`BUDDHADASA_USAGE_PROFILE.md`](BUDDHADASA_USAGE_PROFILE.md)
  Records a source-backed term profile from selected Buddhadasa Bhikkhu works
  for use in notes, context rules, and new-term intake.
- [`DHAMMARATO_CHANTING_PROFILE.md`](DHAMMARATO_CHANTING_PROFILE.md)
  Records a source-backed liturgical term profile from Dhammarato's chanting
  manual for use in notes, context rules, and chant-term intake.
- [`DHAMMARATO_QUOTES_PROFILE.md`](DHAMMARATO_QUOTES_PROFILE.md)
  Records the Dhammarato quotes book as an internal OSF publication profile at
  the same house-material level as the OSF glossary and *What Is And Is Not
  The Path*, and may justify direct changes to preferred renderings.
- [`WHAT_IS_AND_IS_NOT_THE_PATH_PROFILE.md`](WHAT_IS_AND_IS_NOT_THE_PATH_PROFILE.md)
  Records term guidance from the OSF publication *What Is And Is Not The Path*
  as an internal OSF house-material source while preserving repo spellings and
  normalized headwords.
- [`OSF_EDITORIAL_AUTHORITY.md`](OSF_EDITORIAL_AUTHORITY.md)
  Defines the authority order for OSF translation decisions and how source
  conflicts should be resolved.
- [`../STYLE_GUIDE.md`](../STYLE_GUIDE.md)
  Captures the project's translation style and recurring rendering preferences.

## Practical Workflow

When editing or adding a term:

1. Check the style guidance first.
2. Confirm the field meanings in the data dictionary.
3. Follow the term entry standard while drafting.
4. Choose tags and status from the standard vocabulary.
5. Run `python scripts/run_checks.py` before committing.

Note that `run_checks.py` currently runs editorial lint in strict mode, so
structural warnings such as non-reciprocal `related_terms` links will block the
full check suite until resolved.

For more targeted local checking, you can also run:

- `python -m unittest discover -s tests`
- `python scripts/validate_terms.py`
- `python scripts/lint_terms.py`
- `python scripts/audit_term_coverage.py`
- `python scripts/repo_health.py`
- `python scripts/policy_backfill_queue.py`
- `python scripts/backfill_policy_metadata.py --check-only`

## Outside-Source Profiles

When an outside source or author strongly influences a rendering decision:

1. Add the rendering first as an alternate or source-specific context rule.
2. Mention the source influence explicitly in `notes`.
3. Prefer a small number of named source profiles over silent drift in house
   terminology.
4. Only replace the current `preferred_translation` when the project has made
   a deliberate editorial decision to do so.

The OSF glossary and named OSF books are not outside-source profiles. They sit
inside OSF house authority and should be treated accordingly.

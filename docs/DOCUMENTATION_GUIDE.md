# Documentation Guide

This folder holds the repository's editorial, structural, and workflow reference material. Use this page as the main index rather than reading files in arbitrary order.

## Start Here

If you are new to the project, read these first:

1. [`../README.md`](../README.md)
2. [`project-overview.md`](project-overview.md)
3. [`architecture.md`](architecture.md)
4. [`development-guide.md`](development-guide.md)
5. [`usage.md`](usage.md)

Then move into the editorial rules that govern live term data:

6. [`../TERMINOLOGY_PRINCIPLES.md`](../TERMINOLOGY_PRINCIPLES.md)
7. [`../STYLE_GUIDE.md`](../STYLE_GUIDE.md)
8. [`OSF_EDITORIAL_AUTHORITY.md`](OSF_EDITORIAL_AUTHORITY.md)
9. [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md)
10. [`TERM_ENTRY_STANDARD.md`](TERM_ENTRY_STANDARD.md)
11. [`TAG_STATUS_VOCABULARY.md`](TAG_STATUS_VOCABULARY.md)

## By Task

### Understand The Repository

- [`project-overview.md`](project-overview.md): scope, entry model, and design intent
- [`architecture.md`](architecture.md): how terms, schema, scripts, tests, and review layers fit together
- [`../README.md`](../README.md): public-facing overview and quick-start path

### Set Up And Run Checks

- [`development-guide.md`](development-guide.md): local setup, edit loop, and targeted test runs
- [`usage.md`](usage.md): task-based command recipes
- [`../scripts/README.md`](../scripts/README.md): script-by-script CLI index

### Edit Term Records Safely

- [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md): field meanings
- [`TERM_ENTRY_STANDARD.md`](TERM_ENTRY_STANDARD.md): what good major and minor entries should contain
- [`TAG_STATUS_VOCABULARY.md`](TAG_STATUS_VOCABULARY.md): permitted tag and status language
- [`HEADWORD_COMPOUND_FORMULA_POLICY.md`](HEADWORD_COMPOUND_FORMULA_POLICY.md): when policy belongs on a headword versus a compound or formula
- [`DRIFT_RISK_TERMS.md`](DRIFT_RISK_TERMS.md): doctrinal terms most likely to destabilize translation choices

### Review Editorial Decisions

- [`EDITORIAL_REVIEW_CHECKLIST.md`](EDITORIAL_REVIEW_CHECKLIST.md): merge and promotion gate
- [`REVIEW_STATUS_MODEL.md`](REVIEW_STATUS_MODEL.md): how major entries move from draft to reviewed to stable
- [`DECISION_RECORD_TEMPLATE.md`](DECISION_RECORD_TEMPLATE.md): lightweight structure for major decisions that should not live only in commit history
- [`OSF_EDITORIAL_AUTHORITY.md`](OSF_EDITORIAL_AUTHORITY.md): authority order for source conflicts and house decisions

### Work In Bulk Or Expand Coverage

- [`BULK_EDITING_PLAYBOOK.md`](BULK_EDITING_PLAYBOOK.md): safe operating pattern for large edit batches
- [`CANDIDATE_TERM_WORKFLOW.md`](CANDIDATE_TERM_WORKFLOW.md): intake and review flow for proposed terms
- [`TRANSLATION_WORKFLOW_PLAN.md`](TRANSLATION_WORKFLOW_PLAN.md): current editorial sequencing and roadmap
- [`EXPANSION_BATCH_001.md`](EXPANSION_BATCH_001.md): concrete expansion batch reference
- [`LEXICON_EXPANSION_PLAN_500.md`](LEXICON_EXPANSION_PLAN_500.md): larger-scale planning note

### Consult Named Source Profiles

- [`OSF_GLOSSARY_PROFILE.md`](OSF_GLOSSARY_PROFILE.md)
- [`WHAT_IS_AND_IS_NOT_THE_PATH_PROFILE.md`](WHAT_IS_AND_IS_NOT_THE_PATH_PROFILE.md)
- [`DHAMMARATO_QUOTES_PROFILE.md`](DHAMMARATO_QUOTES_PROFILE.md)
- [`DHAMMARATO_CHANTING_PROFILE.md`](DHAMMARATO_CHANTING_PROFILE.md)
- [`BUDDHADASA_USAGE_PROFILE.md`](BUDDHADASA_USAGE_PROFILE.md)
- [`PUNNAJI_USAGE_PROFILE.md`](PUNNAJI_USAGE_PROFILE.md)

These profiles support notes, context rules, alternates, and authority reasoning. They do not override house policy on their own unless the repository has made that decision explicitly.

### Review Current State

- [`REPOSITORY_REVIEW_2026-03.md`](REPOSITORY_REVIEW_2026-03.md): current structural review snapshot

## Practical Workflow

When editing or adding a term:

1. Confirm the project-level translation rule in [`../TERMINOLOGY_PRINCIPLES.md`](../TERMINOLOGY_PRINCIPLES.md).
2. Check wording expectations in [`../STYLE_GUIDE.md`](../STYLE_GUIDE.md).
3. Confirm field semantics in [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md).
4. Draft against [`TERM_ENTRY_STANDARD.md`](TERM_ENTRY_STANDARD.md).
5. Validate and lint before committing.

The normal full-suite command is:

```bash
python scripts/run_checks.py
```

For targeted local checking, see [`usage.md`](usage.md).

## Outside-Source Profiles

When an outside source or author strongly influences a rendering decision:

1. Add the rendering first as an alternate or source-specific context rule.
2. Mention the source influence explicitly in `notes` or `authority_basis`.
3. Prefer a small number of named source profiles over silent drift.
4. Only replace `preferred_translation` when the repository has made a deliberate editorial decision to do so.

The OSF glossary and named OSF books are internal house sources, not outside-source profiles.

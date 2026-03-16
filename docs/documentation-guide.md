# Documentation Guide

This folder holds the repository's editorial, structural, and workflow reference material. Use this page as the main index rather than reading files in arbitrary order.

## Naming Convention

Docs in `docs/` use lowercase-kebab-case filenames.

Examples:

- `documentation-guide.md`
- `osf-editorial-authority.md`
- `knowledge-seeing-understanding-cluster-map.md`

This keeps links predictable across platforms and makes repository-surface
automation simpler.

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
8. [`osf-editorial-authority.md`](osf-editorial-authority.md)
9. [`data-dictionary.md`](data-dictionary.md)
10. [`term-entry-standard.md`](term-entry-standard.md)
11. [`tag-status-vocabulary.md`](tag-status-vocabulary.md)

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

- [`data-dictionary.md`](data-dictionary.md): field meanings
- [`term-entry-standard.md`](term-entry-standard.md): what good major and minor entries should contain
- [`tag-status-vocabulary.md`](tag-status-vocabulary.md): permitted tag and status language
- [`headword-compound-formula-policy.md`](headword-compound-formula-policy.md): when policy belongs on a headword versus a compound or formula
- [`drift-risk-terms.md`](drift-risk-terms.md): doctrinal terms most likely to destabilize translation choices

### Review Editorial Decisions

- [`editorial-review-checklist.md`](editorial-review-checklist.md): merge and promotion gate
- [`review-status-model.md`](review-status-model.md): how major entries move from draft to reviewed to stable
- [`decision-record-template.md`](decision-record-template.md): lightweight structure for major decisions that should not live only in commit history
- [`osf-editorial-authority.md`](osf-editorial-authority.md): authority order for source conflicts and house decisions

### Work In Bulk Or Expand Coverage

- [`bulk-editing-playbook.md`](bulk-editing-playbook.md): safe operating pattern for large edit batches
- [`candidate-term-workflow.md`](candidate-term-workflow.md): intake and review flow for proposed terms
- [`translation-workflow-plan.md`](translation-workflow-plan.md): current editorial sequencing and roadmap
- [`expansion-batch-001.md`](expansion-batch-001.md): concrete expansion batch reference
- [`lexicon-expansion-plan-500.md`](lexicon-expansion-plan-500.md): larger-scale planning note

### Consult Named Source Profiles

- [`osf-glossary-profile.md`](osf-glossary-profile.md)
- [`what-is-and-is-not-the-path-profile.md`](what-is-and-is-not-the-path-profile.md)
- [`dhammarato-quotes-profile.md`](dhammarato-quotes-profile.md)
- [`dhammarato-chanting-profile.md`](dhammarato-chanting-profile.md)
- [`buddhadasa-usage-profile.md`](buddhadasa-usage-profile.md)
- [`punnaji-usage-profile.md`](punnaji-usage-profile.md)
- [`hillside-nyanamoli-usage-profile.md`](hillside-nyanamoli-usage-profile.md)

These profiles support notes, context rules, alternates, and authority reasoning. They do not override house policy on their own unless the repository has made that decision explicitly.

### Review Current State

- [`repository-review-2026-03.md`](repository-review-2026-03.md): current structural review snapshot

## Practical Workflow

When editing or adding a term:

1. Confirm the project-level translation rule in [`../TERMINOLOGY_PRINCIPLES.md`](../TERMINOLOGY_PRINCIPLES.md).
2. Check wording expectations in [`../STYLE_GUIDE.md`](../STYLE_GUIDE.md).
3. Confirm field semantics in [`data-dictionary.md`](data-dictionary.md).
4. Draft against [`term-entry-standard.md`](term-entry-standard.md).
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

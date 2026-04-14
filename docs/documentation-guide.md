# Documentation Guide

This folder holds the repository's editorial, structural, and workflow
reference material. Use this page as the main index instead of opening files
at random.

## What This Guide Covers

Use this page to answer three questions quickly:

- where live policy actually lives
- which document governs the task in front of you
- which files are reference-only outputs rather than source material

## File Naming

Docs in `docs/` use lowercase-kebab-case filenames.

Examples:

- `documentation-guide.md`
- `osf-editorial-authority.md`
- `knowledge-seeing-understanding-cluster-map.md`

This keeps links predictable across platforms and simplifies repository
automation.

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
8. [`MODERN_ENGLISH_POLICY.md`](MODERN_ENGLISH_POLICY.md)
9. [`VOICE_STANDARD.md`](VOICE_STANDARD.md)
10. [`osf-editorial-authority.md`](osf-editorial-authority.md)
11. [`data-dictionary.md`](data-dictionary.md)
12. [`term-entry-standard.md`](term-entry-standard.md)
13. [`tag-status-vocabulary.md`](tag-status-vocabulary.md)

If you are starting from raw source text rather than revising existing live
entries, also read:

14. [`candidate-term-workflow.md`](candidate-term-workflow.md)
15. [`../candidates/README.md`](../candidates/README.md)

## Quick Paths

- New contributor: [`../README.md`](../README.md) -> [`project-overview.md`](project-overview.md) -> [`development-guide.md`](development-guide.md) -> [`../CONTRIBUTING.md`](../CONTRIBUTING.md)
- Editing a live term entry: [`../terms/README.md`](../terms/README.md) -> [`data-dictionary.md`](data-dictionary.md) -> [`term-entry-standard.md`](term-entry-standard.md) -> [`../STYLE_GUIDE.md`](../STYLE_GUIDE.md)
- Working from raw source text: [`candidate-term-workflow.md`](candidate-term-workflow.md) -> [`../candidates/README.md`](../candidates/README.md)
- Reviewing generated reference material: [`generated/generated-docs-guide.md`](generated/generated-docs-guide.md)
- Changing tooling or tests: [`development-guide.md`](development-guide.md) -> [`../scripts/README.md`](../scripts/README.md)

## Source of Truth vs. Reference Output

Use these layers deliberately:

- live policy: `terms/major/` and `terms/minor/`
- normative guidance: top-level governance docs and rule docs in `docs/`
- intake evidence: `candidates/`
- generated reference material: `docs/generated/`

Generated docs help translators and reviewers navigate the repository, but they
do not override live term records or normative policy docs.

## By Task

### Understand the Repository

- [`project-overview.md`](project-overview.md): scope, entry model, and design intent
- [`architecture.md`](architecture.md): how terms, schema, scripts, tests, and review layers fit together
- [`../README.md`](../README.md): public-facing overview and quick-start path
- [`../terms/README.md`](../terms/README.md): how the live lexicon is laid out on disk
- [`../candidates/README.md`](../candidates/README.md): what belongs in intake versus the live lexicon

### Set Up and Run Checks

- [`development-guide.md`](development-guide.md): local setup, edit loop, and targeted test runs
- [`usage.md`](usage.md): task-based command recipes
- [`../scripts/README.md`](../scripts/README.md): script-by-script CLI index

### Work With Translation Surfaces

- [`translations/translation-documents.md`](translations/translation-documents.md): index of shareable translation pairs
- [`next-sutta-translation-roadmap.md`](next-sutta-translation-roadmap.md): ranked working order for the next outward-facing sutta translation passes
- [`mn1-mn18-mn148-linked-surface-brief.md`](mn1-mn18-mn148-linked-surface-brief.md): linked control brief for recognition, proliferation, selfing, taking personally, identity, and de-appropriation across MN 1, MN 18, and MN 148
- [`practice-text-surface-map.md`](practice-text-surface-map.md): shared MN 10 / MN 118 practice control lines
- [`sensory-response-surface-map.md`](sensory-response-surface-map.md): shared MN 137 / MN 148 feeling-domain control lines

### Edit Term Records Safely

- [`data-dictionary.md`](data-dictionary.md): field meanings
- [`term-entry-standard.md`](term-entry-standard.md): what good major and minor entries should contain
- [`tag-status-vocabulary.md`](tag-status-vocabulary.md): permitted tag and status language
- [`MODERN_ENGLISH_POLICY.md`](MODERN_ENGLISH_POLICY.md): modern-English register rules and anti-translationese guidance
- [`VOICE_STANDARD.md`](VOICE_STANDARD.md): default sentence patterns for notes, context rules, examples, and contributor docs
- [`headword-compound-formula-policy.md`](headword-compound-formula-policy.md): when policy belongs on a headword versus a compound or formula
- [`drift-risk-terms.md`](drift-risk-terms.md): doctrinal terms most likely to destabilize translation choices

### Review Editorial Decisions

- [`editorial-review-checklist.md`](editorial-review-checklist.md): merge and promotion gate
- [`review-status-model.md`](review-status-model.md): how major entries move from draft to reviewed to stable
- [`decision-record-template.md`](decision-record-template.md): lightweight structure for major decisions that should not live only in commit history
- [`osf-editorial-authority.md`](osf-editorial-authority.md): authority order for source conflicts and house decisions

### Work in Bulk or Expand Coverage

- [`bulk-editing-playbook.md`](bulk-editing-playbook.md): safe operating pattern for large edit batches
- [`candidate-term-workflow.md`](candidate-term-workflow.md): intake and review flow for proposed terms
- [`translation-workflow-plan.md`](translation-workflow-plan.md): current editorial sequencing and roadmap
- [`next-sutta-translation-roadmap.md`](next-sutta-translation-roadmap.md): current recommended order for the next translation-document additions
- [`expansion-batch-001.md`](expansion-batch-001.md): concrete expansion batch reference
- [`lexicon-expansion-plan-500.md`](lexicon-expansion-plan-500.md): larger-scale planning note

### Source Profiles

- [`osf-glossary-profile.md`](osf-glossary-profile.md)
- [`what-is-and-is-not-the-path-profile.md`](what-is-and-is-not-the-path-profile.md)
- [`dhammarato-quotes-profile.md`](dhammarato-quotes-profile.md)
- [`dhammarato-chanting-profile.md`](dhammarato-chanting-profile.md)
- [`buddhadasa-usage-profile.md`](buddhadasa-usage-profile.md)
- [`idappaccayata-practical-talk-profile.md`](idappaccayata-practical-talk-profile.md)
- [`punnaji-usage-profile.md`](punnaji-usage-profile.md)
- [`hillside-nyanamoli-usage-profile.md`](hillside-nyanamoli-usage-profile.md)

These profiles support notes, context rules, alternates, and authority reasoning. They do not override house policy on their own unless the repository explicitly says they do.

### Current State

- [`repository-review-2026-03.md`](repository-review-2026-03.md): current structural review snapshot

### Generated Reference Material

- [`generated/generated-docs-guide.md`](generated/generated-docs-guide.md): what generated docs are for and what they are not
- [`generated/major-term-index.md`](generated/major-term-index.md): human navigation for `terms/major/`
- [`generated/minor-term-index.md`](generated/minor-term-index.md): human navigation for `terms/minor/`

## Document Types

Use the docs set in layers:

- normative policy docs: repository rules that govern live data
- workflow docs: how contributors and scripts operate on that data
- source profiles: named authority and comparison material used in notes and provenance
- planning docs: backlog, sequencing, and review notes
- generated docs: reference outputs derived from live policy

Generated docs are useful reference material, but they do not override live
term data or normative policy docs.

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

## Key Directories Outside `docs/`

Some important navigation surfaces live outside this directory:

- [`../terms/README.md`](../terms/README.md): live lexicon layout and navigation
- [`../candidates/README.md`](../candidates/README.md): review-first intake layer
- [`../scripts/README.md`](../scripts/README.md): script-by-script command index

## External Source Profiles

When an outside source or author strongly influences a rendering decision:

1. Add the rendering first as an alternate or source-specific context rule.
2. Mention the source influence explicitly in `notes` or `authority_basis`.
3. Prefer a small number of named source profiles over silent drift.
4. Only replace `preferred_translation` when the repository has made a deliberate editorial decision to do so.

The OSF glossary and named OSF books are internal house sources, not outside-source profiles.

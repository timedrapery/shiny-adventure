# TAG AND STATUS VOCABULARY

## Purpose

This document defines the preferred `tags` and `status` values used in
**shiny-adventure** term entries.

It is intentionally short. The goal is to keep tagging useful and consistent,
not to build a large taxonomy too early.

Use this document alongside:

- `docs/data-dictionary.md`
- `docs/term-entry-standard.md`
- `STYLE_GUIDE.md`
- `docs/review-status-model.md`

---

## Tag Guidelines

## General Rules

- Prefer 1 to 3 tags for most entries.
- Reuse an existing tag before inventing a new one.
- Tags should describe doctrinal role, topical grouping, or editorial behavior.
- Avoid near-duplicates such as `mental-quality` and `mental-qualities`; use one standard form.
- If a tag is only needed once, it probably belongs in `notes`, not in `tags`.

## Current Preferred Tags

### `core-doctrine`

Use for central doctrinal terms that matter across major frameworks.

Examples:

- `dukkha`
- `nirodha`
- `paṭiccasamuppāda`
- `viññāṇa`

### `core-practice`

Use for terms central to practice language or training instructions.

Examples:

- `sati`
- `samādhi`
- `bhāvanā`

### `dependent-origination`

Use for terms directly tied to paṭiccasamuppāda or its standard sequence.

Examples:

- `paṭiccasamuppāda`
- `saṅkhārā`
- `taṇhā`
- `viññāṇa`

### `four-noble-truths`

Use for terms strongly anchored in the four noble truths framework.

Examples:

- `dukkha`
- `nirodha`
- `taṇhā`

### `three-marks`

Use for terms directly associated with the three marks framework.

Examples:

- `dukkha`

### `meditative-development`

Use for terms connected to development, training, or meditative development.

Examples:

- `bhāvanā`
- `jhāna`
- `vitakka`
- `vicāra`

### `mental-qualities`

Use for traits, capacities, or qualities of mind.

Examples:

- `sati`
- `samādhi`

### `jhana-factors`

Use for terms that function specifically as jhāna factors or are closely tied
to jhāna analysis.

Examples:

- `vitakka`
- `vicāra`
- `jhāna`

### `aggregates`

Use for terms belonging to the five aggregates framework.

Examples:

- `viññāṇa`

### `sense-fields`

Use for terms in the six sense-field framework, including the fields, objects,
and linked consciousness terms.

Examples:

- `cakkhu`
- `sota`
- `salāyatana`

### `causality`

Use for terms that primarily mark causal structure, conditions, or results.

Examples:

- `hetu`
- `upanisa`
- `phala`

### `ethics`

Use for terms centered on conduct, restraint, wholesome or unwholesome action,
or explicitly ethical evaluation.

Examples:

- `sīla`
- `adinnādāna`
- `kamma`

### `liberation`

Use for terms tied directly to release, unbinding, path attainments, or
liberating formulas.

Examples:

- `vimutti`
- `nibbāna`
- `arahant`

### `persons`

Use for person-types, attained individuals, communities, or role-bearing
designations.

Examples:

- `arahant`
- `sotāpanna`
- `saṅgha`

### `embodiment`

Use for terms centered on the body, embodiment, or body-based contemplation.

Examples:

- `kāya`
- `kabaḷīkāra-āhāra`
- `sampajañña`

### `context-sensitive`

Use when the preferred rendering changes significantly depending on doctrinal or
textual context.

Examples:

- `saṅkhārā`

### `translation-sensitive`

Use when the English rendering needs extra care because common translations are
especially unstable, overloaded, or misleading.

Examples:

- `dhamma`
- `ariya`
- `saṅgha`

### `worldly-conditions`

Use for gain/loss, praise/blame, fame/disrepute, and similar worldly condition
vocabulary.

Examples:

- `lābha`
- `alābha`
- `yasa`

## When Not to Add a New Tag

Do not add a new tag just because:

- a term belongs to a very narrow subtopic once
- a nuance is already explained in `notes`
- the same distinction is already captured by `status` or `entry_type`

If a new tag starts appearing in several entries, it may be worth formalizing
later in this document.

## Current Live Tag Set

As of the current repository contents, the standardized tag set is:

- `aggregates`
- `causality`
- `context-sensitive`
- `core-doctrine`
- `core-practice`
- `dependent-origination`
- `embodiment`
- `ethics`
- `four-noble-truths`
- `jhana-factors`
- `liberation`
- `meditative-development`
- `mental-qualities`
- `persons`
- `sense-fields`
- `three-marks`
- `translation-sensitive`
- `worldly-conditions`

---

## Status Guidelines

## Allowed Status Values

### `draft`

Use when an entry is still provisional.

Typical signs:

- the preferred rendering is still being tested
- examples or notes are incomplete
- context rules need more work
- the entry reflects an active editorial debate

### `reviewed`

Use when an entry has had a real editorial pass, but is still open to revision.

Typical signs:

- the structure is complete
- the translation choice is reasonably defensible
- references and examples are present
- the project may still refine the wording later

### `stable`

Use when an entry reflects the current house standard.

Typical signs:

- the preferred rendering is intentional and documented
- notes and context rules are in good shape
- examples support the decision
- the team would currently want downstream tools to treat this as the default

## Practical Rule of Thumb

- Use `draft` for work in progress.
- Use `reviewed` for solid entries that may still evolve.
- Use `stable` only when you would be comfortable reusing the entry across the project today.

For the operational workflow behind these labels, see `docs/review-status-model.md`.

---

## Recommended Editorial Checklist

Before moving an entry to `reviewed` or `stable`, check:

- The preferred translation is clearly intentional.
- The notes explain the main editorial decision.
- The tags come from the standard vocabulary in this document.
- The examples support the actual translation choice.
- The status matches the current confidence level.

---

## Current Standardization Notes

Prefer these forms:

- `mental-qualities`
- `meditative-development`
- `jhana-factors`

Avoid older or drifting variants such as:

- `mental-quality`
- `mental-development`
- `practice`
- `mental-activity`

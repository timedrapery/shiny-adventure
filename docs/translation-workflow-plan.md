# Translation Workflow Plan

## Purpose

This document defines the next development phase for **shiny-adventure** as a
translation-working repository rather than only a term archive.

The repo already contains many term files, a schema, and validation tools. The
next task is to shape those assets into a coherent translation system that can
be used directly while translating texts.

## Immediate Goal

Build the repository around **translation-ready doctrinal clusters** rather
than around isolated headwords.

That means each important term should be usable in four layers:

1. as a headword
2. as part of compounds
3. as part of canonical formulas
4. as part of a governed doctrinal cluster

## Strategic Priorities

### 1. Stabilize the editorial model

The first requirement is a clear editorial rule for:

- headword entries
- compound entries
- formula entries
- when compounds inherit the headword default
- when a formula may override the headword default

This is the foundation for translation consistency.

### 2. Build doctrinal clusters instead of editing randomly

The repo should now prioritize coherent clusters over scattered file growth.

The first clusters to stabilize should be:

- dependent arising
- five aggregates
- six sense bases
- four noble truths
- three marks
- path factors

### 3. Treat formulas as first-class translation objects

Many translation decisions only become clear in recurring canonical phrases.

The repo should therefore support not only:

- `saṅkhāra`
- `saṅkhāra-paccaya`
- `saṅkhāra-nirodha`

but also formula lines such as:

- `avijjāpaccayā saṅkhārā`
- `aniccā sabbe saṅkhārā`
- other recurring formula segments as they become editorially important

### 4. Tighten propagation from major entries to related entries

When a major entry changes, related compounds and formula records should be
reviewed in the same pass.

The repo should stop allowing a major term to change while leaving nearby
entries with stale language.

### 5. Improve translation-facing outputs

The term files are structured enough to support translator-facing artifacts.

Future tooling should generate:

- doctrinal cluster glossaries
- formula sheets
- quick-reference term briefs
- consistency reports for related term families

## Operating Sequence

Use this order when improving the repository:

1. define policy
2. stabilize one doctrinal cluster
3. add validation rules that protect that cluster
4. generate translator-facing outputs from the structured data
5. repeat with the next cluster

## First Working Cluster

The first full pilot should be **dependent arising**.

That cluster should include:

- nidāna headwords
- `-paccaya` entries
- `-nirodha` entries
- major formula examples
- cross-links between the related terms

The target is not merely correctness per file. The target is that the whole
cluster reads in one voice and can guide an actual translation session.

## Concrete Next Tasks

### Phase 1: Policy

- Add headword / compound / formula rules to project documentation.
- Define inheritance and override behavior for related entries.
- Add a short translator workflow to the main project docs.

### Phase 2: Dependent-Arising Audit

- Review every nidāna entry as a family.
- Review all related `-paccaya` and `-nirodha` entries.
- Add or strengthen formula examples for the standard chain.
- Normalize cross-references and discouraged renderings.

### Phase 3: Tooling

- Add a validation check for stale discouraged renderings in related files.
- Add a validation check for mojibake and broken diacritics.
- Add a cluster audit report for doctrinal families.

### Phase 4: Translator Outputs

- Generate a dependent-arising cluster glossary.
- Generate a formula sheet for recurring chain lines.
- Generate concise term briefs for major entries.

## Editorial Standard Going Forward

From this point on, important terms should be revised as systems, not as
isolated files.

For major doctrinal vocabulary, a finished editorial pass should normally
cover:

- the headword
- important compounds
- formula usage
- related examples
- linked entries likely to preserve stale wording

## Definition of Success

This repo is succeeding when a translator can take a passage from a sutta,
identify the relevant doctrinal cluster, and receive:

- the default English rendering
- the allowed alternates
- the discouraged renderings
- the formula-specific overrides
- the related term family needed to keep the passage coherent

That is the next real milestone for **shiny-adventure**.

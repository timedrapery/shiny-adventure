# Project Overview

This repository is a structured Pali-to-English translation lexicon for Early Buddhist texts.

It is designed as an editorial policy system, not just a word list. The core unit is a term record that combines definition, preferred rendering, context-sensitive rules, provenance, and drift-prevention guidance.

## What This Project Is

- A machine-readable term dataset in JSON
- A schema and validation toolchain for editorial consistency
- A translation drift prevention system for doctrinally sensitive vocabulary
- A contributor workflow for safe term additions and revisions

## What This Project Is Not

- A neutral all-traditions dictionary
- An automatic translator
- A free-form glossary where synonyms rotate without policy

## Entry Model

The dataset has two entry classes:

- major: rule-bearing entries that encode translation policy
- minor: lighter entries for stable and less policy-sensitive terms

Major entries carry stronger expectations around context rules, linked terms, examples, and rationale.

## What Makes A Major Entry Policy-Bearing

A major entry is not just a fuller definition.

It is expected to work as a governed editorial record that includes:

- a default `preferred_translation`
- explicit `context_rules`
- rule-bearing `notes`
- meaningful `related_terms`
- example phrases that demonstrate the policy
- provenance in `authority_basis`
- a compact machine-readable summary in `translation_policy`

If a term can drift across doctrinal settings, compounds, or translation
surfaces, it should usually be handled as a major entry.

## What Minor Entries Are For

Minor entries are lighter records for terms that are comparatively stable,
narrow, or formula-supportive.

They still belong to the governed lexicon, but they do not carry the same full
policy burden as major entries unless the repository later promotes them.

## Where Policy Lives

The repository separates live policy, intake evidence, and reference output on
purpose.

- `terms/major/` and `terms/minor/` are the live governed lexicon
- top-level governance docs and rule docs in `docs/` explain how those records are written, reviewed, and interpreted
- `candidates/` holds extracted or staged evidence that still needs editorial judgment
- `docs/generated/` holds browsing surfaces and translator-facing summaries derived from live policy

That means candidate files are not live rules, and generated docs are not the
primary place to make policy changes.

## How New Vocabulary Enters The Repository

The repository uses a review-first path:

1. candidate vocabulary is extracted or reviewed in [`../candidates/`](../candidates/README.md)
2. editors decide whether the item belongs in the live lexicon
3. approved items are added to `terms/major/` or `terms/minor/`
4. scripts and tests validate the result before merge

That separation is deliberate. Candidate evidence is not the same thing as
live house policy.

## Key Design Principle

Term decisions should be explicit and reviewable. If a translation choice changes interpretation, that choice should be represented in the record and validated in review.

## Where To Go Next

- Field definitions: [data-dictionary.md](data-dictionary.md)
- Entry drafting: [term-entry-standard.md](term-entry-standard.md)
- Translation voice and style: [../STYLE_GUIDE.md](../STYLE_GUIDE.md)
- Authority order: [osf-editorial-authority.md](osf-editorial-authority.md)
- Contributor workflow: [development-guide.md](development-guide.md)
- Terms navigation: [../terms/README.md](../terms/README.md)
- Candidate intake: [../candidates/README.md](../candidates/README.md)
- Generated reference-material guidance: [generated/generated-docs-guide.md](generated/generated-docs-guide.md)

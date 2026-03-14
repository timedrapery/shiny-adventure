# TERM ENTRY STANDARD

## Purpose

This document defines how new term records should be created for the
**shiny-adventure** Pāli translation dataset.

The goal is not merely to store definitions, but to encode **translation
decisions** in a structured and consistent format.

The dataset functions as:

-   a translator's lexicon
-   a house style guide
-   a machine-readable translation rule system

For that reason, **major terms must be rule-bearing entries rather than
simple dictionary definitions.**

Use this document alongside:

- `docs/DOCUMENTATION_GUIDE.md`
- `docs/DATA_DICTIONARY.md`
- `docs/TAG_STATUS_VOCABULARY.md`
- `STYLE_GUIDE.md`

------------------------------------------------------------------------

# Entry Types

## Major Entries (Rule-Bearing)

Major entries encode **translation rules and decisions**.

Use these for:

-   doctrinal core vocabulary
-   context-sensitive terms
-   terms appearing in key formulas
-   terms widely mistranslated
-   terms whose rendering changes depending on context

Examples:

-   dukkha
-   sati
-   jhāna
-   saṅkhārā
-   viññāṇa
-   taṇhā
-   nirodha
-   paṭiccasamuppāda

Major entries should normally include:

-   `preferred_translation`
-   `alternative_translations`
-   `discouraged_translations`
-   `context_rules`
-   `related_terms`
-   `example_phrases`

------------------------------------------------------------------------

## Minor Entries

Minor entries may be used for terms that:

-   have stable meanings
-   rarely shift by context
-   are not doctrinally central

Minor entries may omit `context_rules` and `example_phrases`.

However, the project generally favors **major entries for important
terms**.

------------------------------------------------------------------------

# Suggested Workflow

When working on an entry:

1. Read the translation preference in `STYLE_GUIDE.md`.
2. Confirm field meaning in `docs/DATA_DICTIONARY.md`.
3. Draft or revise the entry in `terms/`.
4. Choose tags and status from `docs/TAG_STATUS_VOCABULARY.md`.
5. Validate the file before committing.

------------------------------------------------------------------------

# File Naming Convention

Files must use **ASCII filenames**.

Example file paths:

    terms/sati.json
    terms/dukkha.json
    terms/jhana.json
    terms/paticcasamuppada.json

Inside the record, the Pāli term should retain diacritics.

Example:

    "term": "paṭiccasamuppāda"

------------------------------------------------------------------------

# Entry Type Convention

Every new entry should include `entry_type`.

- Use `major` for rule-bearing entries that carry translation guidance.
- Use `minor` for narrower entries that do not need the full rule set.
- In the schema, `major` entries must include `notes`, `context_rules`, `related_terms`, and `example_phrases`.

------------------------------------------------------------------------

# Required Fields

Every entry should include:

  Field                     Description
  ------------------------- -----------------------------------------------
  `term`                    Headword in Pāli with diacritics
  `normalized_term`         ASCII version used for filenames and indexing
  `entry_type`              Major or minor entry classification
  `part_of_speech`          Grammatical category
  `preferred_translation`   Default English rendering
  `definition`              Short explanatory definition
  `status`                  Editorial status

Example:

``` json
{
  "term": "dukkha",
  "normalized_term": "dukkha",
  "entry_type": "major",
  "part_of_speech": "noun",
  "preferred_translation": "dissatisfaction",
  "definition": "The unsatisfactory and unstable character of conditioned experience.",
  "status": "stable"
}
```

------------------------------------------------------------------------

# Recommended Fields for Major Entries

Major entries should normally include:

  Field                        Purpose
  ---------------------------- ---------------------------------
  `alternative_translations`   Acceptable alternate renderings
  `discouraged_translations`   Renderings to avoid
  `context_rules`              Translation changes by context
  `related_terms`              Connected doctrinal vocabulary
  `example_phrases`            Canonical usage examples
  `notes`                      Editorial notes
  `tags`                       Thematic classification

These fields allow the dataset to function as a **translation engine**
rather than a flat glossary.

------------------------------------------------------------------------

# Source-Backed Alternates

When revising an entry from a named secondary source or talker profile:

- keep the current `preferred_translation` unless the project has explicitly
  decided to change house style
- add the source-backed rendering to `alternative_translations` when it is a
  reusable English option
- add a `context_rule` when the rendering belongs only to a specific
  pedagogical or interpretive frame
- mention the source in `notes` so the editorial reason remains auditable

This repository should not silently absorb strong interpretive systems without
recording where they came from.

For OSF authority order and cases where a source may directly change
`preferred_translation`, also read `docs/OSF_EDITORIAL_AUTHORITY.md`.

------------------------------------------------------------------------

# Context Rules

`context_rules` encode translation decisions that vary depending on
usage.

Example:

``` json
"context_rules": [
  {
    "context": "In paṭiccasamuppāda sequences",
    "rendering": "choices",
    "notes": "Project preference for saṅkhārā in dependent arising."
  },
  {
    "context": "In general doctrinal statements about compounded phenomena",
    "rendering": "constructed things"
  }
]
```

Use context rules whenever:

-   a term's rendering shifts by doctrinal setting
-   literal translation would be misleading
-   traditional translations are inconsistent

------------------------------------------------------------------------

# Alternative Translations

Example:

``` json
"alternative_translations": [
  "unease",
  "stress"
]
```

------------------------------------------------------------------------

# Discouraged Translations

Example:

``` json
"discouraged_translations": [
  "suffering"
]
```

------------------------------------------------------------------------

# Related Terms

Example:

``` json
"related_terms": [
  "taṇhā",
  "nirodha",
  "anicca"
]
```

------------------------------------------------------------------------

# Example Phrases

Example:

``` json
"example_phrases": [
  {
    "pali": "aniccā sabbasaṅkhārā",
    "translation": "all constructed things are impermanent"
  }
]
```

------------------------------------------------------------------------

# Tags

Example tags:

-   aggregates
-   causality
-   context-sensitive
-   core-doctrine
-   core-practice
-   dependent-origination
-   embodiment
-   ethics
-   four-noble-truths
-   jhana-factors
-   liberation
-   mental-qualities
-   meditative-development
-   persons
-   sense-fields
-   three-marks
-   translation-sensitive
-   worldly-conditions

For the preferred current tag set and when to use each tag, see
`docs/TAG_STATUS_VOCABULARY.md`.

------------------------------------------------------------------------

# Status Field

Allowed values:

  Status     Meaning
  ---------- ----------------------------
  draft      Entry is incomplete
  reviewed   Entry checked but evolving
  stable     Current project standard

For practical guidance on when to use each status, see
`docs/TAG_STATUS_VOCABULARY.md`.

------------------------------------------------------------------------

# Editing Principles

1.  Prefer clarity over jargon.
2.  Preserve doctrinal precision.
3.  Maintain consistency with the style guide.
4.  Encode translation decisions explicitly.
5.  Favor rule-bearing entries for important terms.

------------------------------------------------------------------------

# Long-Term Goal

The **shiny-adventure** dataset aims to support:

-   translators
-   readers
-   dictionary tools
-   glossary generators
-   translation assistants
-   AI-assisted translation systems

Entries should encode **translation knowledge**, not just dictionary
meaning.

The long-term aim is to build a **structured Pāli translation engine
dataset**.

# Term Entry Standard

## Purpose

This document defines how new term records should be created for the
**shiny-adventure** Pāli translation dataset.

The goal is not just to store definitions. It is to encode translation
decisions in a structured, consistent format.

The dataset functions as:

- a translator's lexicon
- a house style guide
- a machine-readable translation rule system

Major terms therefore need to be rule-bearing entries, not simple dictionary
definitions.

The live schema expresses those editorial ideas through these field names:

- preferred rendering -> `preferred_translation`
- translation rule -> `context_rules`
- usage notes -> `notes`
- examples -> `example_phrases`
- provenance -> `authority_basis`
- rule summary -> `translation_policy`

Do not introduce a parallel vocabulary such as `preferred_rendering` unless the
schema itself is intentionally changed first.

Use this document alongside:

- `docs/documentation-guide.md`
- `docs/data-dictionary.md`
- `docs/tag-status-vocabulary.md`
- `STYLE_GUIDE.md`
- `docs/MODERN_ENGLISH_POLICY.md`
- `docs/VOICE_STANDARD.md`

## Entry Types

### Major Entries

Major entries encode translation rules and decisions.

Use these for:

- doctrinal core vocabulary
- context-sensitive terms
- terms appearing in key formulas
- terms widely mistranslated
- terms whose rendering changes depending on context

Examples:

- `dukkha`
- `sati`
- `jhāna`
- `saṅkhārā`
- `viññāṇa`
- `taṇhā`
- `nirodha`
- `paṭiccasamuppāda`

Major entries should normally include:

- `preferred_translation`
- `alternative_translations`
- `discouraged_translations`
- `context_rules`
- `notes`
- `related_terms`
- `example_phrases`
- `sutta_references`
- `tags`

### Minor Entries

Minor entries may be used for terms that:

- have stable meanings
- rarely shift by context
- are not doctrinally central

Minor entries may omit `context_rules` and `example_phrases`.

The project still prefers major entries for important terms that need governed
translation behavior.

## Suggested Workflow

When working on an entry:

1. Read the translation preferences in `STYLE_GUIDE.md`.
2. Confirm field meaning in `docs/data-dictionary.md`.
3. Draft or revise the entry in `terms/major/` or `terms/minor/` according to `entry_type`.
4. Choose tags and status from `docs/tag-status-vocabulary.md`.
5. Validate the file before committing.

If you are still gathering evidence from source text, start in `candidates/`
rather than writing directly into the live lexicon.

## File Naming Convention

Files must use ASCII filenames.

Example file paths:

```text
terms/major/sati.json
terms/major/dukkha.json
terms/major/jhana.json
terms/major/paticcasamuppada.json
```

Inside the record, the Pāli term should retain diacritics.

Example:

```json
"term": "paṭiccasamuppāda"
```

## Entry Type Convention

Every new entry should include `entry_type`.

- Use `major` for rule-bearing entries that carry translation guidance.
- Use `minor` for narrower entries that do not need the full rule set.
- In the schema, `major` entries must include `notes`, `context_rules`,
  `related_terms`, and `example_phrases`.

## Required Fields

Every entry should include:

| Field | Description |
| --- | --- |
| `term` | Headword in Pāli with diacritics |
| `normalized_term` | ASCII version used for filenames and indexing |
| `entry_type` | Major or minor entry classification |
| `part_of_speech` | Grammatical category |
| `preferred_translation` | Default English rendering |
| `definition` | Short explanatory definition |
| `status` | Editorial status |

For major entries, these required fields are only the baseline. They do not by
themselves make an entry rule-bearing.

Example:

```json
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

## Recommended Fields For Major Entries

Major entries should normally include:

| Field | Purpose |
| --- | --- |
| `alternative_translations` | Acceptable alternate renderings |
| `discouraged_translations` | Renderings to avoid |
| `context_rules` | Translation changes by context |
| `notes` | Editorial rationale and usage notes |
| `related_terms` | Connected doctrinal vocabulary |
| `example_phrases` | Canonical usage examples |
| `sutta_references` | Canonical anchors for the rule |
| `tags` | Thematic classification |
| `authority_basis` | Structured provenance for the policy |
| `translation_policy` | Machine-readable rule summary |

These fields allow the dataset to function as a translation engine rather than
a flat glossary.

For reviewed or stable major entries, `authority_basis` should not stop at a
generic placeholder such as `Repository editorial record`. Use explicit named
authority, source profile, or repository-source support once the entry is
merge-ready.

## Source-Backed Alternates

When revising an entry from an outside-source profile or a lower-authority
named source:

- keep the current `preferred_translation` unless the project has explicitly
  decided to change house style
- add the source-backed rendering to `alternative_translations` when it is a
  reusable English option
- add a `context_rule` when the rendering belongs only to a specific
  pedagogical or interpretive frame
- mention the source in `notes` so the editorial reason remains auditable

This repository should not silently absorb strong interpretive systems without
recording where they came from.

The OSF glossary and named OSF books are not outside sources. They belong to
the internal OSF house-material layer described in
`docs/osf-editorial-authority.md`.

## Context Rules

`context_rules` encode translation decisions that vary by usage.

Example:

```json
"context_rules": [
  {
    "context": "In paṭiccasamuppāda sequences",
    "rendering": "choices",
    "notes": "Use this by default in dependent arising."
  },
  {
    "context": "In general doctrinal statements about compounded phenomena",
    "rendering": "constructed things"
  }
]
```

Use context rules whenever:

- a term's rendering shifts by doctrinal setting
- literal translation would be misleading
- traditional translations are inconsistent

For doctrinal anchor terms, the combined `notes` and `context_rules` should
also state:

- when the default rendering applies
- when it should not apply
- whether compounds or formulas inherit the rule by default
- what doctrinal confusion or translation drift the rule is preventing

Avoid thin governance surfaces for reviewed or stable major entries. As a
working house standard, those entries should normally show more than a single
default/alternate split. Give the translator at least one clear boundary or
contrast rule, or else reinforce the entry with extra examples and fuller note
detail.

Use `notes` alongside `context_rules` when the repository needs to explain why
the default rendering was kept, changed, or left untranslated.

When a term-family decision is important enough to shape multiple compounds or
formula lines, also summarize it in `translation_policy` so tools do not have
to infer inheritance only from prose.

Use the voice patterns in `docs/VOICE_STANDARD.md` when writing `notes`,
`context_rules`, and `example_phrases`. In practice that means:

- direct note openings such as `The project prefers ...`
- direct context-rule notes such as `Use this by default.`
- descriptive example notes such as `Shows the term in compound use.`
- short, direct example translations that demonstrate one point at a time

For `example_phrases`, prefer complete translation phrases and note lines that
state what the example shows. Avoid fragment-only example notes when a short
`Shows ...` sentence will do the same work more clearly.

For repeated policy moves, prefer stable house phrasing such as:

- `Use this by default.`
- `Allow this as a controlled alternate only when the context clearly supports it.`
- `Use this in explanatory prose only.`
- `Do not rotate this into the house default.`
- `Keep this distinct from ...`
- `Do not let this drift into generic ... language.`

Use those forms to keep note scaffolding recognizable across entries. Vary the
surrounding sentence only when the policy difference is real.

## Tags and Status

Use the approved values in `docs/tag-status-vocabulary.md`. Do not invent
near-duplicate tags or ad hoc status labels.

## Editing Principles

1. Prefer clarity over jargon.
2. Preserve doctrinal precision.
3. Prefer modern common English over inherited translationese unless a narrow
   technical case is documented.
4. Maintain consistency with the style guide.
5. Encode translation decisions explicitly.
6. Favor rule-bearing entries for important terms.
7. Prefer structured provenance when a named source materially supports the
   rule.

When modernizing wording, update notes, examples, and context rules as well as
the headline translation fields.

## Long-Term Goal

The **shiny-adventure** dataset aims to support:

- translators
- readers
- dictionary tools
- glossary generators
- translation assistants
- AI-assisted translation systems

Entries should encode translation knowledge, not just dictionary meaning.

The long-term aim is to build a structured Pāli translation engine dataset.

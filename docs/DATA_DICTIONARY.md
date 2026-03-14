# DATA DICTIONARY

## Purpose

This document defines the fields used in the **shiny-adventure** term dataset.

It serves as the canonical reference for:

- term record structure
- field meaning
- expected value types
- editorial usage
- downstream tooling

Use this document alongside:

- `schema/PALI_TERM_SCHEMA.json`
- `docs/TERM_ENTRY_STANDARD.md`
- `docs/TAG_STATUS_VOCABULARY.md`
- `STYLE_GUIDE.md`

---

# Core Principle

The dataset is not merely definitional.

It is designed to encode **translation decisions** in a structured, machine-readable form.

For that reason, the most important fields are not only descriptive fields such as `definition`, but also decision-bearing fields such as:

- `preferred_translation`
- `alternative_translations`
- `discouraged_translations`
- `context_rules`
- `related_terms`
- `example_phrases`

In contributor shorthand, these often correspond to:

- preferred rendering -> `preferred_translation`
- translation rule -> `context_rules`
- usage notes -> `notes`
- examples -> `example_phrases`
- provenance -> `authority_basis`
- rule summary -> `translation_policy`

---

# Field Reference

## `term`

**Type:** string  
**Required:** yes

The headword in Pāli, using proper diacritics where applicable.

Example:

```json
"term": "paṭiccasamuppāda"
```

Notes:

- This is the canonical Pāli form shown to users.
- Diacritics should be preserved in the value.
- This field may differ from the filename.

---

## `normalized_term`

**Type:** string  
**Required:** yes

An ASCII-safe normalized version of the headword used for filenames, indexing, and search.

Example:

```json
"normalized_term": "paticcasamuppada"
```

Notes:

- This should usually match the filename stem.
- Do not use diacritics here.
- Keep it lowercase unless there is a compelling reason not to.

---

## `entry_type`

**Type:** string  
**Required:** yes; allowed values are `major` or `minor`

Classifies whether the record is a rule-bearing major entry or a lighter minor entry.

Example:

```json
"entry_type": "major"
```

Notes:

- Use `major` for doctrinally important, context-sensitive, or widely reused terms.
- Use `minor` for terms with a more stable and straightforward project treatment.
- In the schema, `major` entries must include `notes`, `context_rules`, `related_terms`, and `example_phrases`.

---

## `part_of_speech`

**Type:** string  
**Required:** yes

The grammatical category of the entry.

Typical values include:

- `noun`
- `verb`
- `adjective`
- `adverb`
- `participle`
- `pronoun`
- `particle`
- `compound`
- `phrase`
- `expression`
- `other`

Example:

```json
"part_of_speech": "noun"
```

---

## `literal_meaning`

**Type:** string  
**Required:** no

A literal, etymological, or transparent gloss where useful.

Example:

```json
"literal_meaning": "dependent arising"
```

Notes:

- Include this when it helps clarify the structure or historical sense of the term.
- Omit it when it adds little value or encourages misleading literalism.

---

## `preferred_translation`

**Type:** string  
**Required:** yes

The default English rendering preferred by the project.

Example:

```json
"preferred_translation": "dissatisfaction"
```

Notes:

- This is the primary project choice.
- For major entries, this should reflect an actual translation decision rather than a loose approximation.

---

## `alternative_translations`

**Type:** array of strings  
**Required:** no

Acceptable alternate renderings that may be appropriate in some contexts.

Example:

```json
"alternative_translations": [
  "unease",
  "stress"
]
```

Notes:

- These are permitted alternatives, not the project default.
- Include only viable alternatives, not every historically attested rendering.

---

## `discouraged_translations`

**Type:** array of strings  
**Required:** no

Renderings that are common or conceivable but should generally be avoided in this project.

Example:

```json
"discouraged_translations": [
  "suffering"
]
```

Notes:

- Use this field to make project boundaries explicit.
- This is especially helpful for commonly mistranslated doctrinal terms.

---

## `untranslated_preferred`

**Type:** boolean  
**Required:** no

Indicates whether the project generally prefers leaving the term untranslated.

Example:

```json
"untranslated_preferred": true
```

Notes:

- Use this for terms such as `nibbāna` when the project prefers the Pāli form in most contexts.
- This does not forbid glossing on first occurrence.

---

## `gloss_on_first_occurrence`

**Type:** string  
**Required:** no

A suggested gloss to use the first time the term appears in a translation.

Example:

```json
"gloss_on_first_occurrence": "sati (remembering with presence of mind)"
```

Notes:

- Especially useful when `untranslated_preferred` is true.
- Keep this concise and readable.

---

## `definition`

**Type:** string  
**Required:** yes

A short explanatory definition suitable for glossary, dictionary, or UI display.

Example:

```json
"definition": "The unsatisfactory and unstable character of conditioned experience."
```

Notes:

- This should explain the term clearly in plain English.
- It is not the same thing as the preferred translation.

---

## `notes`

**Type:** string  
**Required:** no

Editorial, doctrinal, or usage notes for translators and tool builders.

Example:

```json
"notes": "Project preference is dissatisfaction rather than suffering because it better reflects the broader sense of unsatisfactoriness."
```

Notes:

- Use this for nuance, cautions, and project-specific rationale.
- This is a good place to explain why a preferred translation was chosen.
- For major doctrinal anchors, this is also the place to explain what drift,
  doctrinal confusion, or misleading alternate rendering the entry is meant to
  block.

---

## `context_rules`

**Type:** array of objects  
**Required:** no, but strongly recommended for major entries

Encodes translation decisions that vary by context.

Example:

```json
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

Each object may contain:

- `context` (string, required)
- `rendering` (string, required)
- `notes` (string, optional)

Notes:

- This is one of the most important fields in the entire dataset.
- Use it whenever a term changes sense by doctrinal setting, formulaic environment, genre, or translation register.
- Major terms should usually have this field.
- For doctrinal anchor terms, these rules should make clear when compounds and
  formula lines inherit the headword default and when they do not.

---

## `related_terms`

**Type:** array of strings  
**Required:** no

Links the entry to related doctrinal, semantic, or grammatical terms.

Example:

```json
"related_terms": [
  "taṇhā",
  "nirodha",
  "anicca"
]
```

Notes:

- These relationships help create doctrinal maps and semantic navigation.
- Prefer meaningful relationships over exhaustive ones.

---

## `example_phrases`

**Type:** array of objects  
**Required:** no, but strongly recommended for major entries

Provides examples of real usage.

Example:

```json
"example_phrases": [
  {
    "pali": "aniccā sabbasaṅkhārā",
    "translation": "all constructed things are impermanent"
  }
]
```

Each object may contain:

- `pali` (string, required)
- `translation` (string, optional)
- `notes` (string, optional)
- `source` (string, optional)

Notes:

- Use canonical examples whenever possible.
- Examples should clarify usage, not merely repeat the headword.

---

## `sutta_references`

**Type:** array of strings  
**Required:** no

Canonical references especially relevant to the term.

Example:

```json
"sutta_references": [
  "SN 12.2",
  "DN 22"
]
```

Notes:

- Use when a term is strongly tied to particular passages or frameworks.
- Keep references concise and standardized.

---

## `tags`

**Type:** array of strings  
**Required:** no

Topical or structural classification labels for grouping and filtering entries.

Example:

```json
"tags": [
  "core-doctrine",
  "dependent-origination"
]
```

Possible tags include:

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
- `mental-qualities`
- `meditative-development`
- `persons`
- `sense-fields`
- `three-marks`
- `translation-sensitive`
- `worldly-conditions`

Notes:

- Tags help with navigation and tooling.
- Use the standard vocabulary in `docs/TAG_STATUS_VOCABULARY.md` rather than inventing near-duplicates.

---

## `authority_basis`

**Type:** array of objects  
**Required:** no

Structured provenance for translation policy, especially on mature major
entries.

Example:

```json
"authority_basis": [
  {
    "source": "What Is And Is Not The Path",
    "priority": "osf-house",
    "kind": "preferred-translation",
    "scope": "Supports remembering as the default rendering for sati."
  }
]
```

Each object may contain:

- `source` (string, required)
- `scope` (string, required)
- `priority` (enum, optional)
- `kind` (enum, optional)
- `notes` (string, optional)

Notes:

- Use this when a source, authority layer, or named internal profile directly
  supports the preferred rendering, context rules, or rationale.
- This field improves machine-readability for future review, reporting, and
  conflict detection.
- Mature doctrinal anchors should prefer explicit provenance rather than
  burying source support only in `notes`.
- When source-specific provenance is not yet separated out, a provisional
  internal value such as `Repository editorial record` may be used to mark
  that the entry has structured provenance coverage but still needs refinement.

---

## `translation_policy`

**Type:** object  
**Required:** no

Structured summary of how the rule should behave beyond freeform prose.

Example:

```json
"translation_policy": {
  "default_scope": "Use in most path and practice contexts.",
  "when_not_to_apply": "Do not force this rendering into source-critical passages that need the Pali term.",
  "compound_inheritance": "inherit",
  "drift_risk": "Prevents silent drift back to mindfulness."
}
```

Possible keys include:

- `default_scope`
- `when_not_to_apply`
- `compound_inheritance`
- `leave_untranslated_when`
- `drift_risk`

Notes:

- This field is meant to make rule-bearing entries easier for tools to inspect.
- Use it when the headword governs compounds, carries a leave-untranslated
  policy, or blocks a specific recurring drift.
- `notes` still carries the full editorial explanation; `translation_policy`
  is the compact machine-readable summary.

---

## `status`

**Type:** string  
**Required:** yes

Editorial status of the entry.

Allowed values:

- `draft`
- `reviewed`
- `stable`

Example:

```json
"status": "stable"
```

Definitions:

- `draft`: incomplete or provisional
- `reviewed`: checked but still open to refinement
- `stable`: current preferred project standard

---

## `version_notes`

**Type:** string  
**Required:** no

Optional note recording significant changes to the entry over time.

Example:

```json
"version_notes": "Changed preferred translation from suffering to dissatisfaction."
```

Notes:

- This field is useful when an entry evolves in a meaningful way.
- It should summarize significant editorial shifts, not every tiny edit.

---

# Major Entry Minimum

For a **major rule-bearing entry**, the recommended minimum is:

- `term`
- `normalized_term`
- `entry_type`
- `part_of_speech`
- `preferred_translation`
- `definition`
- `notes`
- `context_rules`
- `related_terms`
- `example_phrases`
- `alternative_translations`
- `discouraged_translations`
- `sutta_references`
- `tags`
- `status`

For mature doctrinal anchors, also prefer:

- `authority_basis`
- `translation_policy`

---

# Filename Convention

The JSON filename should normally correspond to `normalized_term`.

Example:

- filename: `paticcasamuppada.json`
- value: `"normalized_term": "paticcasamuppada"`

This keeps the dataset consistent and easy to process.

---

# Editorial Guidance

When filling fields:

1. Prefer clear modern English.
2. Preserve doctrinal precision.
3. Use notes to explain translation rationale.
4. Use context rules whenever the rendering changes meaningfully.
5. Treat major entries as decision records, not just definitions.

---

# Long-Term Role

This data dictionary supports the long-term goal of making **shiny-adventure** useful for:

- translators
- lexicon readers
- glossary generators
- websites
- lookup tools
- AI-assisted translation workflows

The project is intended to become a **structured Pāli translation engine dataset**.

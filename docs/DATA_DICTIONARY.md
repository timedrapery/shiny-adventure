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

- Use this for terms such as `sati` when the project prefers the Pāli form in most contexts.
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

- `core-doctrine`
- `dependent-origination`
- `four-noble-truths`
- `mental-qualities`
- `meditative-development`
- `aggregates`
- `sense-fields`
- `context-sensitive`

Notes:

- Tags help with navigation and tooling.
- Use a limited, reusable tag vocabulary where possible.

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
- `part_of_speech`
- `preferred_translation`
- `definition`
- `notes`
- `context_rules`
- `related_terms`
- `example_phrases`
- `status`

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

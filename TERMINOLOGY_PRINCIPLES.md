# Terminology Principles

This document states the repository's baseline rules for doctrinal terminology. It sits between the project overview in [README.md](README.md) and the translation voice guidance in [STYLE_GUIDE.md](STYLE_GUIDE.md).

## What the Repository Records

The lexicon records:

- preferred project renderings
- approved alternates
- discouraged renderings
- context-sensitive exceptions
- doctrinal relationships
- examples and provenance

For major terms, these are not optional niceties. They are the mechanism by which the repository preserves consistency across texts.

## Governing Principles

### Preferred translations are defaults

The `preferred_translation` field states the repository's default English rendering. It should govern unless a documented context rule overrides it.

### Exceptions must be explicit

When a term needs a different rendering in a specific doctrinal or literary context, the shift should be recorded in `context_rules`.

### Pali may remain untranslated

The repository allows a term to remain in Pali when translation would be misleading, unstable, or reductive. If that choice is made, the entry should explain why.

### Related terms matter

Term decisions are not isolated. A change to a headword can affect compounds, formulas, neighboring concepts, and doctrinal families. Major-entry edits should therefore review `related_terms` and relevant compounds.

### Drift prevention is part of the record

Major entries should make clear what instability the rule is intended to prevent. That logic belongs in `notes`, `authority_basis`, and `translation_policy`.

## What This Repository Does Not Do

The project does not aim to:

- enforce a generic pan-Buddhist glossary
- average together all English-language traditions
- replace source interpretation with automatic dictionary substitution
- treat stylistic synonym rotation as a virtue in itself

## Working Rule for Contributors

If a translation choice would change how a doctrinally important term is normally read across the corpus, that choice should be treated as policy and documented as such.

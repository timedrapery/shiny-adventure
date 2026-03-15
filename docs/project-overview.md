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

## Key Design Principle

Term decisions should be explicit and reviewable. If a translation choice changes interpretation, that choice should be represented in the record and validated in review.

## Where To Go Next

- Field definitions: [DATA_DICTIONARY.md](DATA_DICTIONARY.md)
- Entry drafting: [TERM_ENTRY_STANDARD.md](TERM_ENTRY_STANDARD.md)
- Translation voice and style: [../STYLE_GUIDE.md](../STYLE_GUIDE.md)
- Authority order: [OSF_EDITORIAL_AUTHORITY.md](OSF_EDITORIAL_AUTHORITY.md)
- Contributor workflow: [development-guide.md](development-guide.md)

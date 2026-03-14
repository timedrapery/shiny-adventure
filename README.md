# shiny-adventure

### A Rule‑Bearing Translation Lexicon for Early Buddhist Texts

[![Status](https://img.shields.io/badge/status-active%20development-blue)]()
[![License](https://img.shields.io/badge/license-see%20repo-lightgrey)]()
[![Data
Type](https://img.shields.io/badge/data-translation%20ruleset-purple)]()
[![Language](https://img.shields.io/badge/source-Pāli-orange)]()
[![Output](https://img.shields.io/badge/target-contemporary%20English-green)]()

**shiny-adventure** is a structured terminology dataset designed to
support the translation of Early Buddhist texts from **Pāli into
contemporary English**.

The project functions simultaneously as:

-   a **translator's lexicon**
-   a **house style guide**
-   a **doctrinal terminology registry**
-   a **machine-readable translation rule system**
-   a **translation memory for canonical texts**

Unlike a conventional dictionary, this repository records **translation
rules and decisions**, allowing terminology to remain consistent across
texts, translators, and translation systems.

------------------------------------------------------------------------

# Why This Project Exists

Translations of early Buddhist texts frequently suffer from:

• inconsistent rendering of key terms\
• philosophical reinterpretation of technical vocabulary\
• translation drift across different texts\
• loss of doctrinal precision

For example, the same Pāli word may appear as several unrelated English
terms across translations.

This repository addresses that problem by defining **stable translation
rules for doctrinal vocabulary**.

Each entry documents:

-   preferred translation
-   literal meaning
-   contextual variation rules
-   doctrinal notes
-   cases where the Pāli term should remain untranslated

The dataset therefore acts as a **controlled vocabulary for canonical
translation**.

------------------------------------------------------------------------

# Core Design Principles

## Clarity

Translations should be understandable to a modern reader.

## Doctrinal Precision

Technical terms preserve their functional meaning within the teachings.

## Consistency

Terms should be rendered the same way across texts unless context
requires otherwise.

## Transparency

When a Pāli term remains untranslated, the reason is documented.

## Rule-Based Terminology

Major entries encode **translation rules**, not simple dictionary
definitions.

------------------------------------------------------------------------

# Entry Types

The lexicon contains two types of entries.

## Major Entries (Rule-Bearing)

Major entries encode translation policy.

They are used for:

-   doctrinal core vocabulary
-   context-sensitive terminology
-   canonical formulas
-   historically mistranslated terms

Examples:

-   dukkha
-   saṅkhārā
-   sati
-   bhāvanā
-   jhāna
-   paṭiccasamuppāda

These entries define **how the term should be translated across the
entire corpus**.

------------------------------------------------------------------------

## Minor Entries (Reference)

Minor entries behave more like conventional dictionary records.

They are used for:

-   lower frequency vocabulary
-   straightforward nouns or verbs
-   grammatical forms
-   supporting terminology

Minor entries typically do not contain rule systems.

------------------------------------------------------------------------

# Repository Structure

    /terms
        Rule-bearing doctrinal term entries

    /schema
        JSON schema defining entry structure

    /docs
        Style guides and project documentation

    /scripts
        Utilities for generating or validating entries

Each doctrinal term exists as a **separate file**, allowing:

-   independent version control
-   machine readability
-   integration with translation tooling
-   incremental expansion of the dataset

------------------------------------------------------------------------

# Example Term Record

Simplified structure:

``` yaml
term: bhāvanā
part_of_speech: noun

literal_meaning:
  bringing into being

preferred_translation:
  development

notes:
  Avoid translating as "meditation".
  The term refers to cultivation or development of qualities.
```

Actual records may include additional rule fields and metadata defined
in the schema.

------------------------------------------------------------------------

# Translation Orientation

The project aims to produce **clear contemporary English translations**
while preserving doctrinal function.

Examples of house renderings:

  Pāli       Preferred Rendering
  ---------- ---------------------
  bhāvanā    development
  jhāna      theme
  dukkha     dissatisfaction
  saṅkhārā   constructings

Some terms intentionally remain untranslated, such as:

-   ānāpānasati

In these cases explanation is preferred over forced translation.

------------------------------------------------------------------------

# Intended Applications

The dataset can support:

-   human translators of Pāli texts
-   AI translation systems
-   digital humanities research
-   canonical terminology standardization
-   machine-assisted lexicons
-   translation memory systems

Because entries encode **translation rules**, the repository can be
integrated directly into translation pipelines.

------------------------------------------------------------------------

# AI Translation Integration

This dataset is particularly suitable for AI-assisted translation
systems.

Possible uses include:

-   grounding LLM translations in consistent terminology
-   enforcing house translation rules
-   building translation validation tools
-   canonical text alignment

The structured format allows entries to be used as:

-   prompt grounding material
-   translation memory
-   rule enforcement layer

------------------------------------------------------------------------

# Contributing

Contributions should follow the **Term Entry Standard** and schema.

When proposing a new doctrinal term:

1.  Determine whether the entry is **major** or **minor**
2.  Follow the schema exactly
3.  Document translation rationale
4.  Include doctrinal context where relevant

The goal is to maintain **stable terminology across the dataset**.

------------------------------------------------------------------------

# Project Status

The repository is under active development.

The long-term objective is the creation of a **rule-bearing
lexicon for translating the Pāli Canon into contemporary English**.

------------------------------------------------------------------------

# License

See the repository license for usage terms.

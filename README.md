# shiny-adventure

## Rule-Bearing Translation Lexicon for Early Buddhist Texts

[![Status](https://img.shields.io/badge/status-active%20development-blue)]()
[![Data](https://img.shields.io/badge/data-translation%20rules-purple)]()
[![Language](https://img.shields.io/badge/source-Pāli-orange)]()
[![Target](https://img.shields.io/badge/output-contemporary%20English-green)]()
[![Format](https://img.shields.io/badge/format-structured%20lexicon-lightgrey)]()

**shiny-adventure** is a structured translation lexicon designed to
support accurate and consistent translation of Early Buddhist texts from
**Pāli into contemporary English**.

The repository encodes **translation rules rather than dictionary
definitions**.\
It functions simultaneously as:

-   a translator lexicon
-   a house style guide
-   a doctrinal terminology registry
-   a machine readable rule system
-   a translation memory for canonical texts

The project aims to provide a **stable and transparent terminology layer
for translating the Pāli Canon**.

------------------------------------------------------------------------

# Why This Repository Exists

Translations of early Buddhist texts often suffer from serious
terminological inconsistency.

Common problems include:

-   one Pāli word translated several different ways
-   philosophical reinterpretation of technical vocabulary
-   inconsistent terminology across texts
-   loss of doctrinal precision

For example a single doctrinal term may appear across translations as
several unrelated English renderings.

This repository addresses the problem by defining **explicit translation
rules for doctrinal vocabulary**.

Each entry records:

-   preferred translation
-   literal meaning
-   contextual translation rules
-   doctrinal notes
-   cases where the Pāli should remain untranslated

The dataset therefore acts as a **controlled vocabulary for canonical
translation**.

------------------------------------------------------------------------

# Core Principles

### Clarity

Translations should be understandable to modern readers.

### Doctrinal Precision

Technical terms must preserve their functional meaning within the
teachings.

### Consistency

A term should be translated the same way across texts unless context
requires otherwise.

### Transparency

When a Pāli term is left untranslated the reason is documented.

### Rule Based Terminology

Major doctrinal terms encode translation rules rather than definitions.

------------------------------------------------------------------------

# Entry Types

The dataset contains two entry classes.

## Major Entries (Rule Bearing)

Major entries encode translation policy.

These are used for:

-   core doctrinal vocabulary
-   context sensitive terminology
-   canonical formula language
-   historically mistranslated terms

Examples include:

-   dukkha
-   saṅkhārā
-   sati
-   bhāvanā
-   jhāna
-   paṭiccasamuppāda

These entries determine **how a term should be translated across the
entire corpus**.

------------------------------------------------------------------------

## Minor Entries (Reference)

Minor entries function more like dictionary records.

Used for:

-   lower frequency vocabulary
-   straightforward nouns or verbs
-   grammatical forms

Minor entries generally do not contain rule systems.

------------------------------------------------------------------------

# Repository Architecture

    shiny-adventure
    │
    ├── terms
    │   doctrinal term entries
    │
    ├── schema
    │   JSON schema defining entry structure
    │
    ├── docs
    │   translation policy and documentation
    │
    └── scripts
        utilities for generating and validating entries

Each doctrinal term exists as an independent file which allows:

-   independent version control
-   machine readable translation rules
-   incremental dataset growth
-   integration with translation tooling

------------------------------------------------------------------------

# Example Term Entry

Simplified representation:

``` yaml
term: bhāvanā
part_of_speech: noun

literal_meaning:
  bringing into being

preferred_translation:
  development

notes:
  Avoid translating as meditation.
  The term refers to cultivation or development of qualities.
```

Actual entries include additional rule fields defined in the schema.

------------------------------------------------------------------------

# Example House Terminology

  Pāli       Preferred Rendering
  ---------- ---------------------
  bhāvanā    development
  jhāna      theme
  dukkha     dissatisfaction
  saṅkhārā   constructings

Some technical terms intentionally remain untranslated such as:

-   ānāpānasati

In such cases explanation is preferred over forced translation.

```json
{
  "term": "dukkha",
  "normalized_term": "dukkha",
  "entry_type": "major",
  "part_of_speech": "noun",
  "preferred_translation": "dissatisfaction",
  "alternative_translations": [
    "unease",
    "stress"
  ],
  "discouraged_translations": [
    "suffering"
  ],
  "untranslated_preferred": false,
  "definition": "The unsatisfactory and unstable character of conditioned experience.",
  "notes": "Project preference is dissatisfaction rather than suffering because it better reflects the broader sense of unsatisfactoriness present in experience.",
  "context_rules": [
    {
      "context": "In core doctrinal exposition and the four noble truths",
      "rendering": "dissatisfaction",
      "notes": "Default project rendering."
    }
  ],
  "related_terms": [
    "anicca",
    "anatta",
    "tanha",
    "nirodha"
  ],
  "example_phrases": [
    {
      "pali": "idaṃ dukkhaṃ ariyasaccaṃ",
      "translation": "this is the noble truth of dissatisfaction",
      "source": "SN 56.11"
    }
  ],
  "tags": [
    "three-marks",
    "core-doctrine"
  ],
  "status": "stable"
}
```

------------------------------------------------------------------------

# Translation Pipeline Example

The dataset can be integrated into modern translation workflows.

Example architecture:

    Pāli Source Text
            │
            ▼
    Tokenization / morphological analysis
            │
            ▼
    Term detection
            │
            ▼
    shiny-adventure lexicon lookup
            │
            ▼
    Rule based translation enforcement
            │
            ▼
    Human or AI translation layer
            │
            ▼
    Consistent contemporary English output

This approach allows translators and AI systems to remain aligned with a
shared terminology system.

------------------------------------------------------------------------

# Applications

The repository can support:

-   translators of the Pāli Canon
-   AI assisted translation systems
-   digital humanities research
-   canonical terminology standardization
-   linguistic analysis of Buddhist texts
-   translation memory systems

Because entries encode rules the dataset can serve as a **terminology
enforcement layer** for translation tools.

------------------------------------------------------------------------

# Development Setup

For local validation and test runs:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/run_checks.py
```

On Windows PowerShell, use `.venv\Scripts\Activate.ps1` to activate the
environment.

------------------------------------------------------------------------

# Example Use With AI Translation

The lexicon can be used to guide language models by:

-   grounding prompts with translation rules
-   validating translation output
-   enforcing house terminology
-   reducing translation drift

This makes the dataset useful for **LLM assisted canonical translation
projects**.

------------------------------------------------------------------------

# Contributing

Contributions should follow the Term Entry Standard and schema.

When proposing a new doctrinal entry:

1.  Determine whether the entry is major or minor
2.  Follow the schema exactly
3.  Provide translation rationale
4.  Document doctrinal context where necessary

The primary goal is **terminological stability across the dataset**.

------------------------------------------------------------------------

# Project Roadmap

Long term objectives include:

-   coverage of doctrinal terminology
-   integration with translation tooling
-   automated validation scripts
-   expansion into a canonical translation lexicon

------------------------------------------------------------------------

# License

See repository license for usage terms.

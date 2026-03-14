# shiny-adventure

## Rule-Bearing Translation Lexicon for Early Buddhist Texts

[![Status](https://img.shields.io/badge/status-active%20development-blue)]()
[![Data](https://img.shields.io/badge/data-translation%20rules-purple)]()
[![Language](https://img.shields.io/badge/source-Pali-orange)]()
[![Target](https://img.shields.io/badge/output-contemporary%20English-green)]()
[![Format](https://img.shields.io/badge/format-structured%20lexicon-lightgrey)]()

**shiny-adventure** is a structured translation lexicon designed to support
accurate and consistent translation of Early Buddhist texts from **Pali into
contemporary English** for the Open Sangha Foundation (OSF).

The repository encodes **translation rules rather than dictionary
definitions**. It functions simultaneously as:

- a translator lexicon
- a house style guide
- a doctrinal terminology registry
- a machine-readable rule system
- a translation memory for canonical texts

The project aims to provide a **stable and transparent terminology layer for
translating the Pali Canon** in a coherent OSF voice shaped primarily by
Dhammarato and Buddhadasa Bhikkhu.

---

## Why This Repository Exists

Translations of early Buddhist texts often suffer from serious terminological
inconsistency.

Common problems include:

- one Pali word translated several different ways
- philosophical reinterpretation of technical vocabulary
- inconsistent terminology across texts
- loss of doctrinal precision

This repository addresses the problem by defining explicit translation rules for
doctrinal vocabulary.

Each entry records:

- preferred translation
- literal meaning
- contextual translation rules
- doctrinal notes
- cases where the Pali should remain untranslated

The dataset therefore acts as a controlled vocabulary for canonical
translation.

---

## Core Principles

### OSF Editorial Authority

OSF house style is not a neutral average of many Buddhist-English traditions.

The repo follows an explicit authority order documented in
[docs/OSF_EDITORIAL_AUTHORITY.md](docs/OSF_EDITORIAL_AUTHORITY.md).

In practice this means:

- Dhammarato is a primary authority for practical teaching tone, path language,
  meditation vocabulary, and contemporary phrasing.
- Buddhadasa Bhikkhu is a primary authority for dependent arising, voidness,
  not-self, conditionality, and here-now liberation framing.
- Secondary profiles such as Punnaji and the OSF glossary remain useful, but do
  not govern house defaults unless the repo explicitly adopts them.

### Clarity

Translations should be understandable to modern readers.

### Doctrinal Precision

Technical terms must preserve their functional meaning within the teachings.

### Consistency

A term should be translated the same way across texts unless context requires
otherwise.

### Transparency

When a Pali term is left untranslated the reason is documented.

### Rule-Bearing Terminology

Major doctrinal terms encode translation rules rather than definitions.

---

## Entry Types

The dataset contains two entry classes.

### Major Entries (Rule-Bearing)

Major entries encode translation policy.

These are used for:

- core doctrinal vocabulary
- context-sensitive terminology
- canonical formula language
- historically mistranslated terms

Examples include:

- dukkha
- sankhara
- sati
- bhavana
- jhana
- paticcasamuppada

### Minor Entries (Reference)

Minor entries function more like dictionary records.

Used for:

- lower-frequency vocabulary
- straightforward nouns or verbs
- grammatical forms
- liturgical and Vinaya-support terms that do not need full rule systems

---

## Repository Architecture

```text
shiny-adventure
├── terms
│   doctrinal and liturgical term entries
├── schema
│   JSON schema defining entry structure
├── docs
│   translation policy and documentation
└── scripts
    utilities for generating and validating entries
```

Each term exists as an independent file, which allows:

- independent version control
- machine-readable translation rules
- incremental dataset growth
- integration with translation tooling

---

## Example House Terminology

| Pali | Preferred Rendering |
| --- | --- |
| dukkha | dissatisfaction; unsatisfactoriness; stress |
| tanha | ignorant wanting |
| sati | remembering |
| samadhi | unification of mind |
| metta | friendliness |
| bhavana | development |

Some technical terms intentionally remain untranslated, such as:

- anapanasati
- nibbana
- dhamma
- bhikkhu / bhikkhus

In such cases, explanation is often preferred over forced translation.

---

## Development Setup

For local validation and test runs:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/run_checks.py
```

On Windows PowerShell, use `.venv\Scripts\Activate.ps1` to activate the
environment.

---

## Contributing

Contributions should follow the term entry standard, schema, style guide, and
OSF authority order. Start with:

- [STYLE_GUIDE.md](STYLE_GUIDE.md)
- [docs/OSF_EDITORIAL_AUTHORITY.md](docs/OSF_EDITORIAL_AUTHORITY.md)
- [docs/DOCUMENTATION_GUIDE.md](docs/DOCUMENTATION_GUIDE.md)

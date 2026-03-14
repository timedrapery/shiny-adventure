# shiny-adventure

## Rule-Bearing Translation Lexicon for Early Buddhist Texts

![Status](https://img.shields.io/badge/status-active%20development-blue)
![Data](https://img.shields.io/badge/data-translation%20rules-purple)
![Language](https://img.shields.io/badge/source-Pali-orange)
![Target](https://img.shields.io/badge/output-contemporary%20English-green)
![Format](https://img.shields.io/badge/format-structured%20lexicon-lightgrey)

**shiny-adventure** is a structured Pali-to-English translation lexicon for
Early Buddhist texts. It preserves OSF house terminology as machine-readable
editorial policy rather than as a loose glossary.

The repository serves three linked purposes:

- a translator's lexicon
- a house style guide
- a machine-readable translation rule system

Major entries are therefore not ordinary dictionary definitions. They are
editorial records that tell contributors and tools how a term should usually be
rendered, when it should be rendered differently, and when it should remain in
Pali.

## What A Term Entry Encodes

The live schema uses these field names for the rule-bearing parts of an entry:

- `preferred_translation` for the default preferred rendering
- `context_rules` for translation rules that shift by context
- `notes` for usage notes and editorial rationale
- `example_phrases` for supporting examples
- `authority_basis` for structured provenance
- `translation_policy` for machine-readable drift-control metadata

For major terms, those fields together form the translation policy. The project
is best understood as a translation control layer, not as a neutral dictionary.

## Why This Repository Exists

Pali translation drifts quickly when major doctrinal vocabulary is handled
case by case. Common failure modes include:

- one headword translated several different ways without explanation
- doctrinally sensitive terms normalized into vague English
- compounds drifting away from headword policy
- untranslated terms being kept in Pali without a stated reason

This repository addresses that by making translation choices explicit,
reviewable, and reusable across the corpus.

## Core Principles

### OSF Editorial Authority

OSF house style is not a neutral average of Buddhist-English traditions.

The repo follows the authority order documented in
[docs/OSF_EDITORIAL_AUTHORITY.md](docs/OSF_EDITORIAL_AUTHORITY.md).

In practice this means:

- OSF house materials such as the OSF glossary, the Dhammarato quotes book,
  and OSF books like *What Is And Is Not The Path* sit at the top of the
  internal authority stack.
- Dhammarato is the next authority for practical teaching tone, path language,
  meditation vocabulary, and contemporary phrasing.
- Buddhadasa Bhikkhu is the next authority for dependent arising, voidness,
  not-self, conditionality, and here-now liberation framing.
- Non-OSF materials such as Punnaji are outside sources and do not govern house
  defaults unless the repo explicitly adopts them.

### Clarity

Translations should be understandable to modern readers.

### Doctrinal Precision

Technical terms must preserve their functional meaning within the teachings.

### Consistency

A term should be translated the same way across texts unless context requires
otherwise.

### Transparency

When a Pali term is left untranslated, the reason should be documented.

### Rule-Bearing Terminology

Major doctrinal terms encode translation rules rather than stand-alone
definitions.

## Entry Types

The dataset has two entry classes:

- `major`
  Rule-bearing entries for doctrinally important or context-sensitive terms.
- `minor`
  Lighter reference entries for terms that do not need a full rule system.

Major entries should normally include a defined default rendering, context
rules, related terms, supporting examples, and notes explaining the editorial
decision.

For the highest-risk doctrinal anchors, the entry should also make explicit:

- when the default rendering applies
- when it should not apply
- when compounds and formulas inherit the headword
- what drift or doctrinal confusion the rule is preventing
- which authority layer or source supports the rule
- whether compounds inherit the headword by default

## Repository Layout

```text
shiny-adventure/
|- terms/    JSON term records, one file per headword
|- schema/   JSON schema for term records
|- docs/     editorial policy and contributor reference material
|- scripts/  validation, lint, and batch-authoring utilities
`- tests/    regression tests for repo tooling
```

## Example House Terminology

| Pali | Preferred Rendering |
| --- | --- |
| dukkha | dissatisfaction; unsatisfactoriness; stress |
| taṇhā | ignorant wanting |
| sati | remembering |
| samādhi | unification of mind |
| mettā | friendliness |
| bhāvanā | development |

Some technical terms intentionally remain untranslated, such as:

- ānāpānasati
- nibbāna
- dhamma
- bhikkhu

In such cases, explanation is preferred over forced equivalence.

## Validation Workflow

For local validation and test runs:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/run_checks.py
```

On Windows PowerShell, use `.venv\Scripts\Activate.ps1` to activate the
environment.

If you want to run the checks individually, use:

```bash
python -m unittest discover -s tests
python scripts/validate_terms.py
python scripts/lint_terms.py
python scripts/audit_term_coverage.py
python scripts/repo_health.py
python scripts/policy_backfill_queue.py
python scripts/backfill_policy_metadata.py --check-only
```

`python scripts/run_checks.py` runs editorial lint in strict mode, so
structural warnings such as non-reciprocal `related_terms` links currently
block the full suite.

## Contributing

Contributions should follow the schema, term entry standard, style guide, and
OSF authority order. Start with:

- [STYLE_GUIDE.md](STYLE_GUIDE.md)
- [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md)
- [docs/TERM_ENTRY_STANDARD.md](docs/TERM_ENTRY_STANDARD.md)
- [docs/OSF_EDITORIAL_AUTHORITY.md](docs/OSF_EDITORIAL_AUTHORITY.md)
- [docs/DOCUMENTATION_GUIDE.md](docs/DOCUMENTATION_GUIDE.md)
- [docs/HEADWORD_COMPOUND_FORMULA_POLICY.md](docs/HEADWORD_COMPOUND_FORMULA_POLICY.md)
- [docs/EDITORIAL_REVIEW_CHECKLIST.md](docs/EDITORIAL_REVIEW_CHECKLIST.md)
- [docs/TRANSLATION_WORKFLOW_PLAN.md](docs/TRANSLATION_WORKFLOW_PLAN.md)

For the recommended reading order across the docs folder, use
[docs/DOCUMENTATION_GUIDE.md](docs/DOCUMENTATION_GUIDE.md).

When reviewing or adding a major term, check three things before changing any
English rendering:

1. The headword's default rendering is explicit.
2. Any context-specific exceptions are encoded in `context_rules`.
3. The rationale is stated in `notes` so the choice can be audited later.

For mature major entries, contributors should also prefer:

1. `authority_basis` entries that name the source layer behind the rule.
2. `translation_policy` metadata that states scope, inheritance, and drift risk.
3. canonical `source` citations on example phrases whenever available.

If the term is a doctrinal anchor such as `dhamma`, `dukkha`, `taṇhā`,
`saṅkhārā`, `sati`, `samādhi`, `nirodha`, `paṭiccasamuppāda`, `jāti`,
`upādāna`, `vedanā`, or `viññāṇa`, also review the linked compounds and
formula examples in the same pass so the family remains coherent.

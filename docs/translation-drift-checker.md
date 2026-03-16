# TRANSLATION DRIFT CHECKER

## Purpose

Translation drift is the gradual loss of house-style consistency across the
term dataset.

In this repository, drift usually shows up as:

- the same Pali lemma receiving conflicting default English renderings
- multiple major lemmas sharing one preferred English rendering without clear
  disambiguation
- major entries losing rule-bearing metadata and collapsing back into
  definition-only records
- alternates and discouraged renderings contradicting each other
- context-sensitive entries missing the notes that explain when a rendering
  shifts

The checker exists to catch those failures before they spread into more term
families, formulas, or downstream translation tooling.

## Command

Run the checker from the repository root:

```bash
python scripts/check_translation_drift.py
```

Optional modes:

```bash
python scripts/check_translation_drift.py --json
python scripts/check_translation_drift.py --strict
```

- `--json` emits a machine-readable report.
- `--strict` returns a non-zero exit code for warnings as well as errors.

## What It Validates

The drift checker validates:

- schema failures reported by the live JSON schema
- conflicting `preferred_translation` values for the same canonical Pali lemma
- duplicate preferred English renderings across major entries when explicit
  disambiguation is missing
- missing rule-bearing fields on `major` entries
- contradictions between `preferred_translation`,
  `alternative_translations`, `discouraged_translations`, and `context_rules`
- missing `context_rules` notes on entries tagged `context-sensitive`
- headword normalization mismatches between `term` and `normalized_term`
- major entries that look definitional rather than rule-bearing

## How To Fix Findings

If the checker reports an error:

- fix contradictory metadata first
- keep the current doctrinal decision unless the change is intentional and
  documented
- update `notes`, `context_rules`, `authority_basis`, and `translation_policy`
  together so the policy remains auditable

If the checker reports a warning:

- review whether the term family needs clearer disambiguation
- confirm that the current spelling and diacritic form are intentional
- strengthen rule-bearing notes if the entry is drifting toward glossary-only
  prose

Warnings are editorial review prompts. Errors are unsafe enough to block
automated trust in the dataset.

## Scope Limits

The checker does not decide doctrinal correctness. It cannot tell whether a
translation choice is philosophically best, only whether the repository has
encoded that choice clearly and consistently enough to prevent silent drift.

## High-Risk Terms

For a list of the doctrinal terms most likely to cause translation instability,
see [`drift-risk-terms.md`](drift-risk-terms.md). These terms include `dukkha`,
`saṅkhāra`, `viññāṇa`, `nibbāna`, `sati`, `jhāna`, `samādhi`, and `saññā`,
among others. They should be reviewed with extra care before any preferred
translation or context rule is changed.

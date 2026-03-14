# Headword, Compound, and Formula Policy

## Purpose

This document defines how translation policy should be distributed across
headword entries, compound entries, and formula entries.

The goal is to make the repository behave like a translation system rather than
like a set of unrelated word notes.

## Core Rule

The repo recognizes three editorial objects:

1. **headword entries**
2. **compound entries**
3. **formula entries**

Each object has a different job and should not be collapsed into the others.

## 1. Headword Entries

Headword entries define the base translation policy for a term.

Examples:

- `sankhara`
- `dukkha`
- `sati`
- `paticcasamuppada`

Headword entries should answer:

- What is the literal sense?
- What is the default English rendering?
- What alternates are allowed?
- What renderings are discouraged?
- What context shifts are important?

For major terms, the headword is the main editorial authority for the term
family unless a compound or formula explicitly overrides it.

## 2. Compound Entries

Compound entries record terms whose meaning is partly inherited from a headword
 but not always fully determined by it.

Examples:

- `sankhara-paccaya`
- `sankhara-nirodha`
- `citta-sankhara`
- `sankharakkhandha`

### Compound Rule

A compound should inherit the headword's preferred rendering when the doctrinal
function is substantially the same.

A compound should override the headword when:

- the compound has become a specialized technical term
- a literal carryover would be awkward or misleading
- the compound belongs to a distinct doctrinal framework
- house usage has stabilized a different rendering

### Compound Documentation Rule

When a compound overrides the headword default, the entry should say so in
`notes` or through explicit translation fields.

The override should be intelligible and auditable, not silent.

## 3. Formula Entries

Formula entries capture recurring canonical phrases or fixed doctrinal lines.

Examples:

- `avijjāpaccayā saṅkhārā`
- `aniccā sabbe saṅkhārā`
- `imasmiṃ sati idaṃ hoti`

Formula entries may be represented in one of two ways:

- as strong `example_phrases` inside major entries
- as dedicated records if the formula has enough translation importance

### Formula Rule

A formula may override both the headword and the compound default when the
phrase functions as a stabilized doctrinal expression.

This matters because canonical formulas often constrain meaning more strongly
than isolated lexical analysis.

## Inheritance Order

Use this order when deciding the translation of a term in context:

1. formula-level rule, if one exists
2. compound-level rule, if one exists
3. headword-level rule
4. project style defaults

This order should govern both human editorial work and future tooling.

## When To Create A Separate Compound Entry

Create or maintain a separate compound entry when:

- the compound appears frequently
- the compound is doctrinally important
- the compound is likely to be mistranslated
- the compound's English cannot be reliably assembled from the headword alone

Do not create separate compound entries merely because a compound exists in
Pali. The compound should earn its own record by translation relevance.

## When To Create A Formula Entry

Create a dedicated formula entry when:

- the phrase recurs widely in canonical translation work
- the phrase has a stable doctrinal function
- the phrase's English depends on more than combining term defaults
- translators will repeatedly need a governed rendering for the whole line

If a dedicated formula entry is too heavy for the current stage, add at least a
strong `example_phrase` to the governing major entry.

## Editorial Workflow Rule

When revising a major headword:

1. review related compounds
2. review major formula examples
3. review directly linked doctrinal neighbors
4. update stale inherited language in the same pass when feasible

Do not treat major-term revision as complete if nearby compound or formula
entries still preserve a now-discouraged rendering.

## Validation Direction

Future tooling should check for:

- discouraged renderings preserved in related compounds
- formula examples that contradict the governing headword policy
- mojibake or broken diacritics in Pali-facing fields
- missing links between major headwords and their core compounds

## First Application

The first doctrinal family to apply this policy to should be dependent arising.

That family is the best pilot because it already contains:

- major headwords
- many compounds
- standard formula lines
- strong doctrinal interdependence between entries

## Practical Summary

Use the repo like this:

- headword for the default term policy
- compound for specialized inherited usage
- formula for fixed canonical translation decisions

That distinction should govern future cleanup and new entry work.

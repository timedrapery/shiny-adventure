# Style Guide

This document defines the repository's translation voice and default editorial behavior. It is a house style guide for a structured Pali translation lexicon, not a general guide to Buddhist-English translation.

## Scope

The style guide exists to keep the lexicon:

- readable to contemporary English readers
- doctrinally precise
- internally consistent
- explicit about exceptions

Authority order is defined separately in [docs/OSF_EDITORIAL_AUTHORITY.md](docs/OSF_EDITORIAL_AUTHORITY.md).

## Core Principles

### Use clear contemporary English

Prefer direct modern English over archaic, pseudo-sacral, or inflated phrasing.

Prefer:

- right view
- dissatisfaction
- remembering
- friendliness
- development

Avoid by default:

- ornamental spiritual diction
- pseudo-biblical phrasing
- unnecessary technical jargon when plain English will do

### Preserve doctrinal precision

Do not flatten technical terms into vague spiritual language. When an established English gloss obscures doctrinal function, prefer a more exact rendering or leave the term in Pali.

### Keep consistency as the default

Preferred translations are defaults, not casual suggestions. Contributors should not rotate among near-synonyms unless the entry documents a real contextual reason.

### Let context govern controlled exceptions

Context matters, but exceptions should be recorded. If a term changes rendering across doctrinal, practical, or literary contexts, the entry should encode that shift in `context_rules`.

### Document untranslated choices

Leaving a term in Pali is acceptable when translation would distort the term, collapse a doctrinal distinction, or prematurely narrow the practice frame. When this happens, the reason should be explicit in the entry.

## Translation Priorities

When choosing a rendering, prioritize in this order:

1. fidelity to function in context
2. doctrinal precision
3. readability in contemporary English
4. consistency across related usage
5. literal transparency

## House Preferences

Current repository tendencies include:

- `dukkha` -> `dissatisfaction` by default, with approved alternates where documented
- `taṇhā` -> `ignorant wanting`
- `sati` -> `remembering`
- `samādhi` -> `unification of mind`
- `sammā-sati` -> `right remembering`
- `sammā-samādhi` -> `right unification of mind`
- `mettā` -> `friendliness`
- `bhāvanā` -> `development`
- `bodhi` -> `awakening`

Current repository tendencies also include:

- prefer `bhikkhu` or `bhikkhus` over `monk` or `monks` where the house style calls for the Pali
- prefer `awakening` over `enlightenment`
- prefer governed doctrinal consistency over stylistic synonym variety

## Terms Commonly Left Untranslated

Some terms often remain in Pali when English would mislead or over-narrow the meaning. Common examples include:

- `ānāpānasati`
- `dhamma`
- `nibbāna`
- `bhikkhu`
- `kāyagatā sati`

This is not automatic. The entry should still state when the untranslated form is preferred and when a gloss is acceptable.

## First Occurrence

For terms left untranslated, a first-occurrence gloss is often useful.

Example:

- `nibbāna (quenching)`

After that, the untranslated Pali may stand on its own if the entry supports that handling.

## Tone

English in this repository should be:

- calm
- exact
- readable
- contemporary
- restrained

It should not feel:

- grandiose
- mystical by default
- artificially academic
- inconsistent from one entry to the next

## Editorial Practice

When revising a core doctrinal term:

- review related compounds
- review recurring formulas
- review near-neighbor terms that could drift with it

When revising a minor term:

- keep the entry lean
- avoid inventing doctrinal nuance the corpus does not need
- align with the headword family where applicable

## Revision Rule

If house preferences change, update the relevant term records, examples, and supporting documentation in the same pass so the repository remains internally coherent.

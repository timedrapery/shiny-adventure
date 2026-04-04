# Voice Consistency Audit

## Purpose

This audit records the repository's remaining voice drift after the
modern-English and archaic-diction cleanup passes.

The main problem was no longer old-fashioned wording by itself. The remaining
problem was mixed editorial voice:

- some notes sounded like direct house policy
- some context rules used generic label fragments
- some example notes described what the example showed
- some example notes only said that the example was `useful` or `simple`
- contributor docs were mostly aligned, but they did not yet define one
  explicit sentence pattern for rule-bearing prose

The goal of this pass is to make the repository read like one careful modern
translator wrote the whole system.

## Current Inconsistencies Before Cleanup

The main inconsistencies were:

- tone drift between direct house-policy prose and placeholder-like fragments
- mixed sentence structure in `context_rules`
- mixed sentence structure in `example_phrases`
- mixed explanatory-note openers in major entries
- contributor guidance that described the desired style but did not yet define
  one operating pattern for it

This drift showed up mostly in repeated stock phrases rather than in doctrinal
disagreement.

## Voice Problem Categories

### Stock Context-Rule Labels

These were structurally correct but too generic:

- `Default project rendering.`
- `Default rendering.`
- `Acceptable alternate.`
- `Use sparingly.`

They did not tell the reader what to do in one stable direct voice.

### Fragmentary Example Notes

Example notes drifted between full descriptive sentences and short evaluative
fragments such as:

- `Simple development-oriented usage.`
- `Useful compact analytical usage.`
- `Useful paired example with nirodha.`

These were readable, but they did not form one stable house pattern.

### Mixed Explanatory Openers

Most entries already used direct openings such as `The project prefers ...` or
`The project keeps ...`, but a smaller set still used the older template
`Project preference is ...`.

That difference was minor in meaning but noticeable in voice.

### Mixed Instructional Style In Contributor Docs

Contributor-facing docs largely used direct prose, but they did not yet define
one explicit standard for:

- rule statements
- context-rule notes
- example-note wording
- direct imperative versus descriptive guidance

## Before-Change Examples

Representative mismatches before this pass included:

- [terms/major/karuna.json](../terms/major/karuna.json)
  used `Default project rendering.` in one context rule and
  `Simple development-oriented usage.` in an example note.
- [terms/major/asekha.json](../terms/major/asekha.json)
  used `Acceptable alternate.` in one context rule and
  `Useful for the completion side of the training contrast.` in an example
  note.
- [terms/major/anukampa.json](../terms/major/anukampa.json)
  opened with `Project preference is ...` while neighboring entries used
  `The project prefers ...`.
- [data-dictionary.md](data-dictionary.md)
  showed the older note style in a schema example even after the live entries
  had moved toward more direct wording.

## Target Unified Voice

The repository now targets one operational voice:

- modern and direct
- technically precise
- calm and restrained
- instructional when needed
- descriptive when showing examples
- readable in one pass

In practice, that means:

- use direct declarative notes for policy
- use `Use this ...` for context-rule instructions
- use `Shows ...` for example-note descriptions
- avoid fragment-only note labels when a short full sentence works better
- avoid filler framing such as `it should be understood that`

## Standard Patterns Adopted

### Explanatory Notes

Use short direct prose such as:

- `The project prefers ... because ...`
- `The project keeps ... because ...`
- `The project leaves ... untranslated because ...`

### Context Rules

Use instruction-first notes such as:

- `Use this by default.`
- `Use this as a controlled alternate when ...`
- `Use this when ...`
- `Do not use this for ...`

### Example Notes

Use descriptive notes such as:

- `Shows the practical contrast.`
- `Shows a compact doctrinal formula.`
- `Shows how the headword works in compounds.`

## Most Affected Areas

The heaviest voice drift was concentrated in:

1. `context_rules` notes in major term entries
2. `example_phrases` notes in major term entries
3. schema and contributor docs that still showed older wording templates
4. the script surface, which did not yet include a dedicated voice audit

## Result Of This Pass

After cleanup:

- stock rule-note fragments were rewritten into direct instructions
- example-note fragments were rewritten into one descriptive pattern
- older explanatory-note openers were aligned with the dominant house voice
- contributor docs now point to an explicit voice standard
- a lightweight audit script now catches the main template-drift patterns

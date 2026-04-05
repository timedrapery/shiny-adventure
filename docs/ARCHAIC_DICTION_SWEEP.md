# Archaic Diction Sweep

## Purpose

This report records the repo-wide sweep against lingering archaic, elevated,
or inherited Buddhist-translator diction.

It complements [MODERN_ENGLISH_AUDIT.md](MODERN_ENGLISH_AUDIT.md) by keeping a
practical inventory of what was targeted and why.

## Working Criteria

Language was flagged when it:

- sounded archaic, pseudo-scriptural, or ceremonious without adding precision
- relied on clause shapes like `one who ...` or `one dwells ...` when normal
  current English would be clearer
- used abstract noun piles where direct verb phrasing would do the same job
- preserved old prestige wording because it was familiar, not because it was
  technically needed
- left notes, examples, or translation surfaces more old-fashioned than the
  controlled headword policy

## Inventory of Flagged Language

### Archaic Connectives

- `thus`
- `there arises`
- `with regard to`
- `therein`
- `thereof`
- `whereby`
- `whilst`
- `amongst`

### Bookish Or Formulaic Verbs

- `one dwells ...`
- `dwells having entered ...`
- `comprehends fully`

### Pseudo-Scriptural Constructions

- `one who has entered the stream`
- `one who returns once`
- `one who does not return`
- repeated formula lines introduced with `thus:`

### Abstract Noun Stacks

- `cultivation`
- `abandonment`

### Legacy Buddhist Translator Jargon

- `meritorious`
- `unmeritorious`

### Britishisms Or High-Literary Residue

- `whilst`
- `amongst`
- high-formality connective fillers in running prose

## Replace / Retain / Discourage

### Replace

Replace the older wording when modern English keeps the same doctrinal job.

Examples:

- `one dwells having entered emptiness` -> `one enters and remains in emptiness`
- `one who has entered the stream` -> `someone who has entered the stream`
- `development or cultivation of mind` -> `development of mind`

### Retain

Retain older-looking wording only when an entry explicitly governs it as a
narrow technical choice.

Examples:

- `cessation` as a controlled alternate in the `nirodha` family
- `Thus-Gone One` as a limited gloss under `tathāgata`
- `cultivation of tranquility` where a source-backed note specifically calls
  for it

### Discourage

Demote the old wording when it still has recognition value but should not lead
the repo surface anymore.

Examples:

- `meritorious`
- `comprehends fully`
- `one who ...` as the default explanatory clause
- generic `cultivation` in notes and examples

## Worst Surviving Examples Before Cleanup

- `one dwells contemplating ...`
- `one dwells having entered ...`
- `one who has entered the stream`
- `meritorious action`
- `unmeritorious constructing`
- repeated `thus` and `there arises` cadence in translation documents

## Repo Areas Most Affected

- `terms/`: examples, notes, and nearby compound records
- `docs/translations/`: stock-formula cadence and lingering scriptural syntax
- contributor-facing docs: policy statements already preferred modern English,
  but that preference needed to be made more operational

## Practical Outcome

After the sweep, the repo should read in one deliberate register:

- modern
- common
- precise
- stable
- rule-bearing

The sweep does not ban every older-looking word. It separates real technical
exceptions from stale inherited style.

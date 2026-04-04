# Modern English Audit

## Purpose

This audit records a focused repository sweep against lingering elevated,
archaic, bookish, or inherited Buddhist-translator diction.

The repository already states a preference for contemporary English. The
problem is that older register still survives unevenly in:

- example phrases
- notes and rationale blocks
- context-rule prose
- translation surfaces
- generated glossaries and contrast sheets
- contributor-facing documentation

That drift makes the lexicon less readable, less internally consistent, and
less reliable as a house style system.

The target is not casual English. The target is modern, common, precise,
rule-bearing English.

## Working Criteria

Language was flagged when it did one or more of the following:

- sounded archaic, ceremonial, or pseudo-scriptural without adding precision
- sounded more British-literary or translator-inherited than broadly current
  English
- used abstract noun stacks where direct verb phrasing would work better
- used clause shapes such as `one who ...` or `one dwells ...` where a cleaner
  modern sentence would be clearer
- preserved inherited Buddhist-English prestige wording rather than a chosen
  house rule
- reintroduced stiffness in notes, examples, or generated docs even when the
  headword itself was already modernized

The audit did not treat all uncommon words as problems. A term or phrase could
be kept if it was:

- technically necessary
- already well-governed as a narrow alternate
- part of a source-facing fixed expression where modernizing it would distort
  the repository's rule-bearing surface

## Main Drift Patterns

### 1. Contemplative Formula Register

This was the clearest live pocket of inherited translationese.

Typical patterns:

- `one dwells contemplating ...`
- `one dwells having entered ...`
- `with the feeling mind thus well-composed`

These are common in practice entries and translation surfaces because the repo
often kept older source-facing cadence in examples even after modernizing the
headword.

### 2. Clause-Style Person Labels

The repository still had many alternates and explanations built around:

- `one who has entered the stream`
- `one who does not return`
- `one who returns once`

These are understandable, but they sound stiffer and more inherited than the
repo's preferred modern register.

### 3. Abstract Training Noun Piles

The repo still carried too much of the following vocabulary in definitions,
notes, and generated docs:

- `cultivation`
- `abandonment`
- `cessation`

Not all of these are wrong. The problem is overuse. In many places they were
surviving as inherited translator habits when:

- `development`
- `giving up`
- `ending`
- `quenching`
- `putting away`

would read more directly without loss.

### 4. Archaic Connective Residue

This category was smaller but still visible.

Examples:

- `thus`
- `there arises`
- `with regard to`

Many of these appeared in translation surfaces or generated docs rather than in
major preferred translations.

### 5. Legacy Prestige Terms

Some wording remained too close to older Buddhist-English prestige diction.

Examples:

- `meritorious action`
- `unmeritorious constructing`
- `one obtains`
- `comprehends fully`

These were not always preferred headword defaults, but they still survived in
minor entries, alternates, or generated outputs and therefore kept leaking old
register into the repo surface.

## Ranked Worst Patterns Before Cleanup

1. `one dwells ...` in examples and translation surfaces
2. `one who ...` alternates in person-category entries
3. `cultivation` surviving as unexamined explanatory prose
4. `meritorious / unmeritorious` surviving in nearby minor entries after the
   `puñña` headword had already moved to `benefit`
5. repeated `thus` and `there arises` cadence in translation documents

## Most Affected Areas

The style scan showed the following broad concentration pattern:

- `docs/`: highest concentration of clause-style person labels and archaic
  connective residue, especially translation surfaces and generated docs
- `terms/`: most of the abstract noun drift and old formula cadence in
  examples, notes, and context rules
- `scripts/` and `tests/`: relatively light style drift, mostly from
  documentation strings and stable cluster naming
- `schema/`: structurally important, but not a meaningful source of style drift

The most affected doctrinal clusters were:

- contemplative formula and satipaṭṭhāna-facing examples
- emptiness / signless / wishless interface examples
- person-stage labels
- development / training vocabulary around `bhāvanā`
- the `puñña` family where the headword and minors had drifted apart in
  register

## Keep / Revise / Avoid

### Keep

Use these when they are the clearest modern controlled option:

- `development`
- `giving up`
- `putting away`
- `ending` when it does not erase a needed distinction
- `quenching` where the repo has already stabilized it
- `someone who ...` when an explanatory clause is genuinely needed
- direct imperatives or direct present-tense sentences instead of ceremonial
  prose

### Revise

These are often salvageable, but too stiff in their current repo usage:

- `cultivation`
- `abandonment`
- `one who ...`
- `one dwells ...`
- `thus` in running English prose
- `there arises`
- `comprehends fully`
- `meritorious`

### Avoid

These should generally not appear as preferred modern-English defaults unless a
narrow technical note justifies them:

- faux-scriptural connective language
- prestige diction kept only because older translators used it
- high-British explanatory phrasing when simpler current English is available
- ceremonial sentence frames that make the repo sound translated rather than
  actually written

## Replace / Retain / Discourage Framework

### Replace

Replace older wording when modern English keeps the same doctrinal job.

Examples:

- `one dwells having entered emptiness` -> `one enters and remains in
  emptiness`
- `one who has entered the stream` -> `someone who has entered the stream`
- `development or cultivation of mind` -> `development of mind`

### Retain

Retain older-looking wording only when it is:

- a controlled alternate with explicit notes
- part of a fixed technical contrast the repo already depends on
- a source-facing line whose modernization would blur policy-bearing meaning

Examples likely to remain as controlled technical language:

- `cessation` as a documented alternate around `nirodha`
- `not-self` as a stable doctrinal label
- `suchness / thusness` where a narrow note explicitly justifies it

### Discourage

Demote old wording when it still has historical recognition but should not lead
the repo surface anymore.

Examples:

- `meritorious`
- `comprehends fully`
- `one who ...` clause labels as the default alternate
- `cultivation` as unmarked explanatory prose

## Modernization Policy For Contributors

- Prefer the most common English that keeps the doctrinal distinction intact.
- Modernize notes and examples, not just `preferred_translation`.
- Do not preserve older wording merely because it sounds familiar from older
  translators.
- If an older wording is retained, say why.
- If a headword has been modernized, check its compounds, formula records, and
  generated outputs in the same pass.
- Treat register drift as a consistency bug, not as optional style polishing.

## Preserved Technical Exceptions After Cleanup

The sweep did not flatten every older-looking term.

These remain deliberate exceptions:

- `cessation` can still appear as a controlled alternate in the `nirodha`
  family where the entry explicitly records it.
- `not-self` remains the stable doctrinal label for `anattā`.
- `Thus-Gone One` remains a narrow gloss under `tathāgata`, but the title
  itself still stays untranslated by default.
- `discerns` remains a governed technical verb in the `pajānāti` family
  because the repo still needs a sharper knowing-verb than plain `knows` or
  `understands`.
- `cultivation` remains available as a controlled alternate in the `bhāvanā`
  family and a few source-backed notes, but it is no longer treated as generic
  default prose.

## QA Support

The repo now includes a lightweight review script:

- `python scripts/modern_english_audit.py`

This script is a review aid, not a blind replacement engine. It flags likely
drift patterns such as `one dwells`, `one who`, `cultivation`, `meritorious`,
and archaic connective language so contributors can review them deliberately.

## Practical Result Expected From This Sweep

After cleanup, the repo should read less like inherited Buddhist-English prose
and more like one deliberate modern system:

- fewer ceremonial sentence frames
- fewer translator-tic connectives
- more direct verbs
- fewer abstract noun stacks
- clearer separation between true technical exceptions and stale old wording

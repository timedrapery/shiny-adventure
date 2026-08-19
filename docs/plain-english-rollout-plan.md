# Plain English Rollout Plan

## Purpose

This is the working plan for bringing every translation surface up to
[PLAIN_ENGLISH_STANDARD.md](PLAIN_ENGLISH_STANDARD.md).

It exists so the work can be picked up cold, on either machine, without
rereading the commit history. The standard says what good English looks like.
This document says what is done, what is left, what was deliberately left
alone, and how to do the next piece safely.

Last updated 2026-08-19.

## Current State

- 20 of 37 translation surfaces are clean.
- 17 surfaces carry 66 remaining register signals.
- 1 reader page carries 8, mirroring its surface.
- Corpus total has gone 680 to 74.

Check the live number at any time:

```bash
python scripts/plain_english_audit.py
```

Completed surfaces: MN 1, SN 36.6, DN 2, DN 15, MN 7, MN 22, MN 10, MN 117,
MN 137, MN 38, MN 118, MN 18, MN 26 (partial, see below).

## The Thing That Keeps Biting

Twice now a surface rewrite has failed the check suite because the **governed
term record was itself written in the translationese**. The lexicon was
enforcing the generic `one` rather than preventing it.

This is the single most important thing to know before continuing. When a
rewrite breaks `run_checks.py`:

1. Do not work around it in the surface.
2. Find the control-line record and read its `preferred_translation`.
3. If the record carries the artifact, revise the record, its
   `alternative_translations`, and its `context_rules[].rendering` together.
4. Revise the whole family in one pass. Half a family is worse than none,
   because it leaves one surface with plain lines and translationese siblings.
5. Expect the change to cascade into a hardcoded control map in the cluster
   report script, the generated sheet, and a regression test that pins the old
   string. Update the test rather than deleting it; the policy changed by
   decision, so the guard moves with it and keeps guarding.

Records already cleared: the ten sensory-response control lines, and nineteen
more covering MN 1, MN 10, MN 18, MN 118, and the `mannati` family.

## Working Procedure

For each surface:

```bash
python scripts/plain_english_audit.py --path docs/translations/<file>.md
```

1. Read the flagged lines **in context** before changing anything. Several
   signals have legitimate exceptions and the audit is advisory on purpose.
2. Identify the real subject. It is usually named a sentence or two earlier
   (`a bhikkhu`, `an unlearned ordinary person`) and then dropped into the
   generic `one`. Carry the named subject through with `they`.
3. Check for pronoun collisions before choosing `they`. In MN 137,
   `they see ... as they have come to be` would have collided the person with
   the forms, so that surface uses `someone` as the subject instead.
4. Do not introduce `you` where the Pali is impersonal. It adds a direct
   address the source does not have. DN 15 was written with `someone` / `they`
   for this reason.
5. Rewrite paragraph-aware, not with a flat string replace. Surfaces are
   hard-wrapped at 79 columns, so a naive replace misses occurrences that span
   a line break and leaves ragged lines behind.
6. Verify no vocabulary was lost. Diff word frequencies against `HEAD`. The
   only counts that should move are third-person verb agreement
   (`abandons` down, `abandon` up). Anything else is drift.
7. Run the full suite, not just the audit.

```bash
python scripts/run_checks.py
```

8. If the surface has a reader page in `reader-src/suttas/`, resync it. There
   is no check binding the two yet (see Open Items).

## Remaining Surfaces

Ordered by signal count. None of these has a dominant offender any more, so
batching by cluster is as reasonable as batching by count.

| Surface | Signals |
| --- | --- |
| AN 3.65 Kesamutta | 8 |
| MN 26 Pasarasi | 8 |
| MN 44 Culavedalla | 8 |
| MN 2 Sabbasava | 6 |
| MN 64 Mahamalukya | 5 |
| AN 10.60 Girimananda (both filename variants) | 4 each |
| SN 12.15 Kaccanagotta | 4 |
| SN 12.23 Upanisa | 4 |
| SN 22.89 Khemaka | 4 |
| MN 141 Saccavibhanga | 3 |
| MN 148 Chachakka | 2 |
| MN 99 Subha | 2 |
| MN 118, MN 19, MN 38, MN 39 | 1 each |

Note that AN 10.60 exists as two files, an ASCII-named one and a
Unicode-named one that is allowlisted in
`scripts/check_docs_integrity.py`. Both need the same edit.

AN 3.65 also has a reader page carrying the same 8 signals.

## Deliberately Deferred

These are real findings that were left alone on purpose. Each is a lexical or
formula decision, and settling one as a side effect of a register pass would
be exactly the kind of incidental drift this repository exists to prevent.

### The anapanasati breathing formula

MN 10 and MN 118 render it `I breathe in long`. AN 10.60 renders it
`I am breathing in long`. No term record governs it.

`I breathe in long` is awkward English and probably fails the spoken test, but
choosing between them affects three surfaces and should be a deliberate
formula decision with its own record.

### `assutava` and `sutava`

Ungoverned. Five surfaces use `unlearned ordinary person`; a sixth briefly used
`untrained` during this work and was reverted, both because `unlearned` is the
corpus norm and because `untrained` is already in use for `avinita` in MN 1
(`untrained and undisciplined in their Dhamma`). Needs a record before anyone
changes it again.

### `vinnata` and `the cognized`

`the cognized` is on the standard's own suspicious list, but the obvious
replacement collides with governed `vinnana` (`knowing`). Needs its own review.

### `sugata`

Governed as `Sugata`, but MN 64 renders it `Fortunate One` and AN 3.65 renders
it `Well-Departed One`. Three renderings for one governed term. Recorded in
`terms/major/bhagava.json` notes because `the Fortunate One` is also
`bhagava`'s literal alternate, so the collision is live.

### `he is the one who speaks and knows`

MN 38, Sati's wrong view. Ordinary English naming a referent, not the
generic-person artifact. Stays flagged by the advisory audit on purpose.

### The seven remaining nominalizations

All `recognition of unattractiveness`, a nominalized inflection of governed
`asubha` (`unattractive`), recorded in the AN 10.60 notes. The
`is_compositional` check does not currently do inflection matching, and making
it do so risks over-suppression.

## Open Items Beyond This Rollout

- **Reader sync check.** `reader-src/suttas/` duplicates its surface body with
  nothing enforcing agreement. Content is currently identical across all five
  pages, so nothing has drifted, but it has been resynced by hand several
  times. Wants a `--check` plus `--write`, tolerant of presentation
  differences: MN 63's reader page italicizes the colophon and adds a rule.
- **Wave 6 translations.** Queue is drafted in
  [next-suttas-roadmap.md](next-suttas-roadmap.md), starting with SN 12.11.
  New surfaces should be written to the plain English standard from the start;
  anything translated in the old register becomes future rollout work.
- **`HIGH_LOAD_MINOR_LINT_THRESHOLD`.** Currently 9 in
  `scripts/lint_terms.py`. The queue it guards is empty, so dropping it to 7
  would make the standard enforced rather than advisory. It would bind future
  entries too, so it is a deliberate call.

## Definition of Done

The rollout is finished when:

- `python scripts/plain_english_audit.py` reports only signals that are
  documented exceptions in this file
- no governed rendering in `terms/` carries the generic person, excluding
  epithet nouns such as `worthy one` and `Thus-Gone One`, where `one` is a
  noun meaning `person` rather than a pronoun stand-in
- every reader page matches its governed surface
- `python scripts/run_checks.py` passes

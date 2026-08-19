# Plain English Rollout Plan

## Purpose

This is the working plan for bringing every translation surface up to
[PLAIN_ENGLISH_STANDARD.md](PLAIN_ENGLISH_STANDARD.md).

It exists so the work can be picked up cold, on either machine, without
rereading the commit history. The standard says what good English looks like.
This document says what was done, what was deliberately left alone, and how
to do the same kind of work safely next time.

Last updated 2026-08-19. The rollout is complete; what remains here is the
working method, the traps, and the decisions that were deliberately deferred.
Read it before touching a translation surface or extending the audit.

## Current State

The rollout is complete across all 41 translation surfaces and all 5 reader
pages.

- 41 of 41 surfaces carry no undocumented register signals.
- 41 of 41 reader pages are generated from their governed surfaces, enforced
  by `scripts/generate_reader.py --check` inside `run_checks.py`. The audit
  scans the canonical surfaces only; auditing the generated copies as well
  would double-count every finding.
- The audit reports 8 signals, and all 8 are the documented exceptions listed
  under Deliberately Deferred below.

```bash
python scripts/plain_english_audit.py
```

Expect 8. Higher means a regression or a new surface; lower means one of the
deferred decisions has been settled and this document needs updating.

The 8 are: six occurrences of `recognition of unattractiveness` across the two
AN 10.60 files, one `one who` in MN 38 naming a referent, and one `duality of
existence` in SN 12.15. None is a defect.

### This Document Has Claimed Completion Once Before, Wrongly

On 2026-08-19 this section said the rollout was complete at 8 signals. That
number was an artifact of the detector, not a fact about the corpus.

The audit found the generic person with an explicit **list of verbs**, and the
list covered roughly half the real cases. It caught `one recognizes` but not
`one discerns`, `one cultivates`, `one fades`, `one reaches`, or `one should`.
Rerunning with a structural rule found **111 further instances across twelve
surfaces** that a "complete" rollout had never touched.

The rule is now structural: `one` is flagged when it stands as grammatical
subject, meaning it is followed by a third-person-singular verb or an
auxiliary, with a stoplist for the legitimate numeral and noun uses. That does
not depend on anyone having anticipated the verb.

Three separate times a miss turned out to be in the detector rather than the
corpus. The first two were patched by adding verbs to the list. Do not do that
again; if something is missed, ask whether the rule is the wrong shape.

**The general lesson, which applies beyond this rollout: a clean report proves
the detector found nothing, not that nothing is there.** Before trusting a zero,
check what the detector is actually looking for.

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

8. If the surface has a reader page in `reader-src/suttas/`, resync it:

```bash
python scripts/generate_reader.py --write
```

   `scripts/generate_reader.py --check` runs as part of `run_checks.py`, so a
   forgotten resync now fails the build rather than drifting silently. The
   comparison ignores presentation-only differences such as heading level,
   emphasis, and horizontal rules.

## Surfaces Completed

All 41. The five Wave 6 surfaces (SN 12.11, SN 55.5, AN 6.63, SN 12.61, MN 11)
were written to the standard from the start and needed no retrofit, which is
the intended pattern for everything new.

Note that AN 10.60 exists as two files, an ASCII-named one and a Unicode-named
one that is allowlisted in `scripts/check_docs_integrity.py`. Both need the
same edit. Any future surface work has to remember this.

## Two Traps In The Tooling

Both were found the hard way and both damaged committed work.

**The paragraph rewriter merges adjacent list items.** The helper used for
these passes treats a block between blank lines as one paragraph and re-wraps
it. Where a bulleted list has no blank line between items, it flattens the
list into running prose. This silently destroyed MN 118's breath-training
bullets in commit `7819ad5` and was not noticed until three commits later,
because **no check looks at list structure**. When rewriting a file with
lists, convert line by line instead, and check afterwards:

```bash
grep -rn "[a-z.,'] - [A-Z]" docs/translations/
```

**Line-wrapped occurrences hide from line-by-line passes.** Surfaces are
hard-wrapped at 79 columns, so `one` can sit at the end of one line with its
verb at the start of the next. A line-by-line substitution misses those
entirely. Handle them with a pattern that allows a newline and indent between
the two words, and preserve that whitespace so the wrap survives.

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

### `recognition of unattractiveness`

Six occurrences, three in each of the two AN 10.60 files. A nominalized
inflection of governed `asubha` (`unattractive`), and the rendering is recorded
in the AN 10.60 notes. The `is_compositional` check in the audit suppresses an
`X of Y` phrase when both halves are governed renderings, but it does not do
inflection matching, and making it do so risks over-suppression.

### `duality of existence`

SN 12.15, once. This surface is the governed middle-way control text and the
phrase belongs to the `atthita` / `natthita` framing, so it is doctrinal
vocabulary rather than stray noun-stacking. Changing it would be a doctrinal
decision about the middle-way formula, not a register fix.

## Open Items Beyond This Rollout

- **The four `upadana` compounds are not consistent with each other.** Two
  render the head as `taking ... personally`, matching the headword; two use
  `clinging`, which the headword records only as an alternate. The
  `ditthupadana` notes show the family revision was started and left half
  finished. Completing it touches two records, three surfaces (DN 15, MN 9,
  SN 12.2), their notes, and the generated cluster sheets. This is the largest
  open lexical question and it is well evidenced; see
  [translations/mn11-culasihanada-sutta-notes.md](translations/mn11-culasihanada-sutta-notes.md).
- **The fourfold source question wants a formula record.** SN 12.11 and MN 11
  now use identical wording for `kim nidana kim samudaya kim jatika kim
  pabhava`. A third surface should not re-solve it.
- **No check looks at list structure.** See the trap above. A small check that
  flags a bullet marker appearing mid-line would have caught the MN 118
  damage.
- **11 `partial` and 147 `inflected` citations** remain from
  `verify_example_sources.py`. Neither is reliably an error, but the `partial`
  set is worth a pass; those are usually the right sutta quoted with slightly
  wrong wording.
- **Wave 7 is undrafted.** Worth re-running the audit method now that the
  citation data is trustworthy: four of Wave 6's leverage signals turned out
  wrong when checked against sources, all traceable to citations that have
  since been repaired.
- **`HIGH_LOAD_MINOR_LINT_THRESHOLD`** is still 9 in `scripts/lint_terms.py`.
  The queue it guards is empty, so dropping it to 7 would make the standard
  enforced rather than advisory.

## Definition of Done

All four conditions are currently met:

- `python scripts/plain_english_audit.py` reports only signals that are
  documented exceptions in this file — currently 8
- no governed rendering in `terms/` carries the generic person, excluding
  epithet nouns such as `worthy one` and `Thus-Gone One`, where `one` is a
  noun meaning `person` rather than a pronoun stand-in
- every reader page matches its governed surface, enforced by
  `generate_reader.py --check`
- `python scripts/run_checks.py` passes

Keeping them met is the ongoing job. Anything newly translated should be
written to the standard from the start, which costs nothing extra and is what
the five Wave 6 surfaces did.

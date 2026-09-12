# Review Lifecycle Hardening Plan

Scope for the phase that ends with the three-text newcomer pilot running with
real participants. Recorded before implementation so the intended behaviour is
reviewable separately from the code.

The goal this serves: readers, not green checks. Automated agreement between
records prevents accidental drift; it does not establish that a rendering is
accurate or that a newcomer understood it. Every item below either protects
real human evidence or keeps a gate honest about what it actually proves.

## 1. Allow a legitimate review after the translation changes

**Current behaviour** (reproduced against `collect_failures` on `129136b`): a
participant label must be unique across a surface's whole history, and that
check runs before evidence for superseded bodies is filtered out. An earlier
review by `R1` plus a review of the revised body by the same `R1` reports
`duplicate participant R1`. The protocol tells contributors to keep the old
record and repeat the affected review, so the documented workflow is blocked.

**Intended behaviour.**

- Uniqueness is per body version: one record per participant per
  `body_sha256`. A second record for the same participant and the same body is
  still a duplicate.
- Evidence for an older body never counts toward the current body's threshold.
  It stays in the ledger as history.
- A participant who reviewed an earlier body and returns for the revised one
  records `follow_up: true`. The review counts as one of the required
  participants but never toward the independent-pass count: someone who has
  already read the text cannot supply a first unprompted reading of it.
- `follow_up: true` with no earlier record by that participant is rejected, and
  so is `independent: true` on a follow-up. The checker names the remedy.

## 2. Bind source-fidelity sign-off to what was reviewed

Read-aloud and newcomer evidence carry the `body_sha256` they were gathered
against. Source fidelity still records only a date and an evidence file, so a
sign-off stays `complete` across later edits to the translation.

**Intended behaviour.** A completed source-fidelity review records the
`body_sha256` it reviewed, exactly as the other two gates do, and stops
counting when the body changes.

**Migration, without fabricating anything.** For each of the twelve existing
sign-offs, ask git when the translation body last changed, and compare that
with the recorded completion date.

- Five surfaces (AN 3.65, SN 56.11, SN 36.6, MN 63, SN 22.59) last changed
  *before* their sign-off date. The sign-off was therefore made against the
  text published today, and binding the hash records a fact from the history.
- The other seven were edited on the same day they were signed off. Git dates
  are day-granular and the sign-off records no time, so whether the review came
  before or after that day's edit cannot be established from the repository.
  Those gates reopen as `pending`, with the original date, evidence file, and
  the reason preserved in a `superseded_signoff` block.

A first pass at this comparison used `git rev-list --until`, whose timezone
handling silently excluded same-day commits and made MN 19 look like the only
changed body. The day-granularity limit above is the real constraint, and it
cuts the other way: fewer sign-offs can be bound, not more. No approval,
reviewer, date, or source check is invented, and no sign-off is carried forward
on the strength of wanting it to hold.

## 3. Separate baseline cleanup from accepting new debt

`--update-baseline` rewrites `reviews/formula-baseline.json` from every current
disagreement, and the contributor documentation presents it as the normal step
after repairs. The same keystroke that drops resolved groups can silently
accept a newly introduced one.

**Intended behaviour.** Cleanup and acknowledgement become two operations:

- `--prune-baseline` removes resolved entries only. It refuses to run while
  regressions are present and says which groups are blocking.
- `--accept-new-debt` is the deliberate act, and requires a recorded rationale.

The existing protections stay: the ordinary check still fails on a new or
changed disagreement, exceptions still name exact records and approved
renderings, a changed approved rendering still voids its exception, and
`--json` still emits one parseable document.

## 4. Make source verification worth gating on

Before wiring `scripts/verify_example_sources.py` into CI, establish what it
actually proves. Known gaps, to be confirmed in code and then fixed:

- `--strict` fails only on `absent` and `partial`. `unfetched`, `unsupported`,
  and `inconclusive` exit zero, so an unreachable source reads as success.
- Matching is plain substring containment, so a short quotation can be
  "verified" by a longer unrelated word that happens to contain it.
- `BILARA_ROOT` tracks the upstream `main` branch and the cache is untracked,
  so two runs are not guaranteed to check the same text.

Deliver a bounded, reproducible check over the supported collections with
verified, failed, and unresolved reported separately, regression cases for the
reported `dhammatā` and `sati` matches, and a precise statement of what remains
uncovered. A gate is added only if its result is trustworthy and repeatable.

## 5. Prepare the three-text pilot for real participants

AN 2.9, SN 36.6, and AN 3.65 are named in
[the review workboard](../reviews/README.md) with a protocol but no
ready-to-use session material. Supply the facilitator script, the participant
instructions, the comprehension questions, the read-aloud procedure, and worked
examples of recording evidence — reusing the existing ledger, inventing no
participants, and promoting nothing to `validated` without real evidence.

## Editorial boundary

The remaining thirty formula groups are editorial debt, not a lint queue. The
next batch is chosen for meaning-sensitive differences — sense fields,
intention and action, the remaining `sati`/`satipaṭṭhāna` variation — over
articles and punctuation. Each proposal carries the Pali, the source context,
the competing renderings, the lexicon rule in play, and a recommendation.
Decisions that policy does not already settle stay proposals.

## Out of scope for this phase

Full-corpus source verification, the glossary keyed to term identifiers, the
`mkdocs-material` end-of-life migration, and the remaining formula groups
beyond the named batch.

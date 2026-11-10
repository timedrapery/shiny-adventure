# Repository Audit: Handoff Notes

Written 2026-11-10. The session ran out of budget part-way through
implementation, so this file separates what was verified, what was changed,
what was approved but not done, and what still needs the owner.

Read [plain-readability-handoff.md](plain-readability-handoff.md) as well; it
covers the translation pass that came before this audit.

## Baseline

At `main` commit `6a10c76` all four verification commands passed locally:
744 unit tests, `python scripts/run_checks.py`, `mkdocs build --strict`, and
104 browser tests (`pnpm test:a11y`).

## Verified findings

### 1. Human validation is almost empty, and honestly recorded

Supported risk, not a defect. The ledger
(`reviews/newcomer-review-ledger.json`) shows, against the bodies now
published:

- newcomer sessions: 0 of 60
- read-aloud reviews complete and bound: 2 of 12 (AN 2.9, SN 36.6)
- source-fidelity sign-offs complete and bound: 2 of 12 (SN 36.6, SN 22.59)
- all 80 surfaces are `provisional`; none is `validated`

The checks that pass on every commit establish structural validity and
internal consistency. They do not establish that a translation is accurate
or that a newcomer understands it.

### 2. The public "last editorial review" line was wrong on 55 of 80 pages

Confirmed defect, fixed. Each reader page printed
`Last editorial review: <date> · body version <hash>`, and on 55 pages the
body was newer than the date. Fifty-one of those came from the 2026-11-09
sentence pass, which re-hashed the bodies and left the dates behind.

Root cause: the hash and the date lived in two hand-edited tables in
`scripts/surface_registry.py`. The stale-hash check printed the new hash to
paste in, and nothing asked about the date.

### 3. Notes files contradict the review ledger on 7 pilot texts

Confirmed defect, **approved for repair but not done**. The ledger is the
documented authority. The `## Readability Review` sections of these notes
files disagree with it:

| Surface | Notes say | Ledger says |
| --- | --- | --- |
| AN 2.9 | source fidelity complete; read-aloud pending | fidelity pending; read-aloud complete |
| SN 36.6 | read-aloud pending | read-aloud complete |
| SN 45.2, SN 56.17, AN 8.6, AN 11.12, SN 12.44 | source fidelity complete | fidelity pending (sign-off superseded) |

Outside the pilot cohort, 14 more notes files say source-fidelity review is
complete with no ledger record at all, so that claim is bound to no body.

### 4. Release integrity

Supported risk; needs the owner. `main` is unprotected, pull requests 33 to
44 have no submitted reviews, and pull requests 43 and 44 were merged 8 and
5 seconds after they were opened, before their CI runs finished. CI did pass
afterwards on both, and the deploy workflow reruns the full suite before
publishing, so nothing broken reached the site. The gap is that nothing
prevents it.

### 5. Editorial debt

- 29 formula disagreements are real and acknowledged in
  `reviews/formula-baseline.json`. About half are articles only
  (`the first mental theme` / `first mental theme`). The rest are different
  words for the same Pali and need an editorial ruling, for example:
  `coveting` / `covetousness`; `the internal fields` / `the internal sense
  fields`; `nibbāna is the highest ease` / `the highest satisfaction`;
  `all constructed things` / `all that has been put together`;
  `establishment of remembering` / `establishment of sati`;
  `knowing and seeing of release` / `knowledge and vision of release`;
  `guarding the faculties` / `sense restraint`;
  `without remainder` / `without fuel remaining`.
- Unlisted declared renderings were 2. One was a stale MN 10 notes line left
  by the 2026-11-09 pass, now fixed. The other is AN 8.39's notes declaring
  `samaṇa` as `ascetics and brahmins` against the record's `recluse`; that is
  an editorial question.

### 6. Maintenance complexity

Confirmed, fixed. Changing one translation meant hand-editing a hash table
and running about thirty generator commands in order. See the new command
below.

### 7. Source verification

`python scripts/verify_example_sources.py --strict` reported 601 verified,
168 qualified, 0 failed, and 79 unresolved (52 elided passages, 27 that could
not be fetched from this environment). It checks that quoted Pali appears in
the cited sutta. It is not a review of whether the English is right.

### Not finished

A security read of `feedback_service/` was started and did not complete
before the session ended. Nothing about it is concluded here.

## What changed in this session

- `reviews/body-versions.json` (new): one record per surface holding the body
  hash and the date that body was last revised. It replaces the two tables in
  `scripts/surface_registry.py`. Dates were set from git history to the day
  each current body first appeared.
- `scripts/refresh_derived.py` (new), with `tests/test_refresh_derived.py`:

  ```bash
  python scripts/refresh_derived.py            # report stale body versions
  python scripts/refresh_derived.py --write    # record versions, regenerate all
  python scripts/run_checks.py
  ```

  It records a changed body's hash and date together, then runs every
  generator in order. It never edits the review ledger. If a changed body has
  human evidence bound to its old hash, it names the surface and stops short
  of deciding anything.
- The reader line now reads `Text last revised: <date> · body version <hash>`.
  The registry field is `revised_on`, documented as a version date and not a
  review claim.
- The stale-hash failure message now points at the refresh command.
- Three notes passages that still quoted pre-pass wording were corrected
  (MN 10, MN 38, MN 39).

## Owner decisions and actions still needed

1. **Protect `main`.** Require the CI check to pass before merge. This is a
   GitHub setting and was not changed.
2. **Rule on the substantive formula disagreements** listed above, then make
   the record copies agree.
3. **Rule on `samaṇa`** in AN 8.39's notes.
4. **Do the human reviews.** The read-aloud gate needs one reviewer and about
   an hour for the First 12.

## Next actions, in order

1. Align the 7 notes files with the ledger (already approved), and add a
   check to `scripts/check_newcomer_reviews.py` that fails when a pilot
   text's notes and the ledger disagree. Done when the check passes and a
   test shows it failing on a planted disagreement.
2. Make the ledger tests independent of live data. Several tests in
   `tests/test_check_newcomer_reviews.py` call
   `next(... status == "complete")` on the real ledger, so they fail if the
   last sign-off is ever reopened for a good reason. Done when the tests pass
   against a ledger copy with no completed gate.
3. Finish the `feedback_service/` security read.
4. Check the hand-written tallies in `reviews/README.md` against the ledger
   in the same check as item 1.
5. `scripts/text_utils.safe_text` escapes every Pali diacritic in reports
   (`abhijjhā`) even on a UTF-8 terminal. Escape only what the output
   stream cannot encode.

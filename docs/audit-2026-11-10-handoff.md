# Repository Audit: Handoff Notes

Written 2026-11-10. This file separates what was verified, what was changed,
and what still needs the owner.

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

### 3. Notes files contradicted the review ledger on 7 pilot texts

Confirmed defect, fixed with the owner's approval. The ledger is the
documented authority. The `## Readability Review` sections of these notes
files disagreed with it:

| Surface | Notes said | Ledger says |
| --- | --- | --- |
| AN 2.9 | source fidelity complete; read-aloud pending | fidelity pending; read-aloud complete |
| SN 36.6 | read-aloud pending | read-aloud complete |
| SN 45.2, SN 56.17, AN 8.6, AN 11.12, SN 12.44 | source fidelity complete | fidelity pending (sign-off superseded) |

Only the status lines in those seven notes files were changed. No ledger
evidence was touched.

**Still open:** outside the pilot cohort, 14 more notes files say
source-fidelity review is complete with no ledger record at all, so that
claim is bound to no body. They were not changed; see the owner decisions.

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

### 8. Feedback service

`feedback_service/` and the browser client were read in full by a delegated
review, which reproduced each defect below with a script. The first six were
then reproduced again as failing tests in this session and fixed.

Fixed:

- **One unreadable sheet row ended the import.** A lone surrogate, an
  oversized integer, or a cell over 128 KiB raised out of
  `python -m feedback_service ingest`, and every valid response after that
  row was never stored. The form is public, so anyone could cause it. Each
  row is now handled on its own and reported by line number.
- The same values returned HTTP 500 from the live endpoint. A surrogate is
  now kept as a replacement mark; an out-of-range `question_version` is a
  validation error.
- `Content-Length: -1` slipped past the size limit and read the whole body.
- With `FEEDBACK_TRUST_PROXY=1` the rate limit used the leftmost
  `X-Forwarded-For` entry, which the client controls. It uses the last entry
  now, the one the proxy appends.
- A static request for `//other.host/..` was answered with a redirect to that
  host (`--site-dir` only). An embedded NUL returned 500.
- The browser client attached a session code to feedback on every page. On
  any text but the session's own it was refused as the wrong text, and on the
  Google Form path the reader was told it was sent. The code is now attached
  only on the text the session link was opened on.

Reproduced by the delegated review, **not re-verified here and not fixed**:

- Import timestamps: `03/04/2026` always parses month-first, sheet-local
  time is stamped as UTC, and an unrecognised format silently becomes the
  import time. This date becomes a ledger `reviewed_on`.
- Import accepts a formal response for a session that is already closed; the
  live endpoint refuses it.
- An edited "Send again" reuses the same submission id, so the first version
  wins.
- A non-ASCII CSRF value returns 500 (authenticated only). The admin form
  accepts session keys and labels the validator later rejects.
- Staging (`scripts/stage_feedback_evidence.py`) never marks a surface
  validated, but it copies the body hash a client asserted, matches a
  returning reader by label only, and will stage a back-dated record as
  history. `docs/reader-feedback-plan.md` says such records are refused.

Operations, from the documentation: nothing is hosted. The public site posts
to a Google Form and a maintainer imports the sheet by hand. Receipt was last
tested by hand on 2026-09-13, rejected rows are only printed, and the queue
and dispositions live in a git-ignored local database with manual backup.

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
- `scripts/check_newcomer_reviews.py` now fails when a pilot text's notes, or
  the tallies in `reviews/README.md`, disagree with the ledger.
- Ledger and readability tests build their own fixtures. Before, four tests
  required the live ledger to hold a completed sign-off (and the notes to say
  particular things), so reopening the last real sign-off for a good reason
  broke the suite. Verified by emptying a scratch copy of the ledger.
- The feedback-service fixes listed under finding 8, each with a regression
  test that failed before the fix.

## Owner decisions and actions still needed

1. **Protect `main`.** Require the CI check to pass before merge. This is a
   GitHub setting and was not changed.
2. **Rule on the substantive formula disagreements** listed above, then make
   the record copies agree.
3. **Rule on `samaṇa`** in AN 8.39's notes.
4. **Decide what the 14 unbound "source-fidelity review: complete" notes
   lines should say.** They sit outside the pilot cohort, so no ledger record
   backs them.
5. **Do the human reviews.** The read-aloud gate needs one reviewer and about
   an hour for the First 12.

## Next actions, in order

1. Fix import timestamps in `feedback_service/ingest.py`: record the sheet's
   time zone and date order explicitly, and keep a note when a timestamp
   could not be parsed. Done when a `dd/mm` sheet and an unparseable stamp
   each have a test.
2. Decide how import should treat a response for a closed session, then make
   import and the live endpoint agree. Done when one test covers both paths.
3. Make `docs/reader-feedback-plan.md` and `stage_feedback_evidence.py` agree
   on records for a body the reader did not see, and match a returning reader
   on session as well as label.
4. `scripts/text_utils.safe_text` escapes every Pali diacritic in reports
   (`abhijjh\u0101`) even on a UTF-8 terminal. Escape only what the output
   stream cannot encode.
5. CI runs the unit tests and five checks twice, once as separate steps and
   once inside `run_checks.py`. Harmless, and a few minutes per run.

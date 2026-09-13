# Facilitator Guide for Newcomer Sessions

How to run a real session with someone new to these texts, using the reader
feedback system alongside the
[newcomer comprehension protocol](../docs/newcomer-review-protocol.md). The
protocol decides what counts as evidence; this guide is the practical
procedure. The [printable session sheet](pilot-session-sheet.md) still works
for note-taking.

Do not invent, backfill, or summarise from memory. If a session did not
happen, nothing is recorded.

## Before the session

1. In the maintainer area of the feedback service, create a session for the
   text (for the pilot, `sn36_6`). Give it an internal title; put no
   participant details in it.
2. Add one anonymous label per participant (`R1`, `R2`, ...). Mark a
   participant `returning` only if they read an earlier version of this
   text in an earlier session, and record that session and label. Everyone
   else is `fresh`.
3. Copy each participant's link from the session page. It is the public
   reader page with `?session=<code>&participant=<label>` added. The page
   looks the same; only the responses are tagged.
4. Confirm the participant is new to early Buddhist suttas (or record that
   they are not). Do not collect a name, email address, or demographics.
5. Withhold the translation notes and the glossary page.

## During the session

**Let them read first.** Give the participant the link and let them read at
their own pace. Do not define a term, explain the teaching, or comment on
their reactions while they read. If they ask what a word means, say that is
exactly what you want to learn and ask them to note it in the feedback
control after the passage.

**Encourage feedback as they go, not after.** The "Give feedback" control
after each passage is for the moment they stumble. Ask them to use it when a
word, a sentence, or missing background stops them, and to write what they
thought it meant.

**Ask neutral questions.** When they finish, ask them to complete the review
at the end of the page. Read the questions aloud only if asked, and read them
exactly as written:

- "In your own words, what was this passage saying?"
- the passage-specific question shown on the page;
- "Which wording, if any, made you stop and reread?"

Do not prompt, hint, or correct. Small vocabulary differences are not
failures; house terminology is not required. If you must clarify a question,
repeat it; do not rephrase it.

**Record where wording or explanations failed.** Note, outside the
repository, which passages they reread, which glossary explanation they
opened, and anything they said aloud that did not make it into the form. If
they used the words-used panel, ask them to rate the explanation there.

**Record independence.** After the session, on the session page, record
whether the answers were given without prompting. This is required before a
response can be exported as evidence.

## After the session

1. Assess each comprehension response against the question set's assessment
   guidance in `includes/feedback/comprehension/<surface>.json`: `pass`,
   `fail`, or `unclear`. Accept reasonable paraphrases. Write a short
   assessment note.
2. Read the passage feedback in the queue. Record a disposition on each:
   what the problem was and where a fix would belong. Group repeated
   problems by term in the by-term view before proposing a change.
3. Export the session and stage it:

   ```bash
   python -m feedback_service export-session --code <code> --out session.json
   python scripts/stage_feedback_evidence.py --export session.json
   python scripts/stage_feedback_evidence.py --export session.json --write
   python scripts/check_newcomer_reviews.py
   ```

   The dry run says which records will count against the current body and
   which are history. Update the surface's ledger `status` by hand if a gate
   changes. Nothing in this path marks a text validated.

## Evaluating a revision

A wording change that materially affects a reviewed passage invalidates the
earlier evidence for that passage. To judge the revision:

- Run a new session on the new body version with **fresh** newcomers. Their
  results are the primary evidence.
- Invite **returning** readers from the earlier session as well, marked as
  returning. Their results show whether the change helped someone who
  already knew the text; they are reported separately and do not replace the
  fresh readers.
- Keep the earlier session's evidence attached to the version it reviewed.
  The ledger keeps it as history, the service keeps it under its body hash,
  and the queue can filter by version. Never edit an old record's hash.

A revision has helped only when fresh readers on the new version stumble
less than fresh readers on the old one, on the same passage, with the same
questions. Until that has been observed with real readers, say so.

## What stays out of the repository

Names, contact details, demographics, recruiting notes, and anything a
participant said that identifies them. The repository holds the anonymous
ledger record and, if wanted, a dated note in the surface's notes file about
what was learned.

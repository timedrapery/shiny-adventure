# Reader Feedback System

How readers tell the editors where a translation is hard to follow, how that
evidence is tied to the exact passage and governed term it concerns, and how
an editor turns it into a revision and checks the revision with readers.

The design decisions are recorded in
[reader-feedback-plan.md](reader-feedback-plan.md). This page is the working
guide. The service's own operator notes are in
[`feedback_service/README.md`](../feedback_service/README.md).

## What it is for

The plain-English standard and the automated audits catch register problems.
They cannot tell whether a contemporary reader understood a passage. The
feedback system collects that evidence in three forms:

- **Passage feedback** on any paragraph of an enabled translation: which kind
  of difficulty ("I don't understand a word or phrase", "I understand the
  words, but not the sentence", "I'm missing some background", "The wording
  feels awkward", "Something else") and, optionally, what the reader thought
  it meant or where they got stuck.
- **Glossary feedback** on each explanation in the words-used panel: did it
  help (yes, partly, no), with an optional comment.
- **An optional comprehension review** at the end of the page: a paraphrase in
  the reader's own words, one passage-specific question, and which wording
  made them stop and reread, plus an optional familiarity question.

No account, no Pali, no contact details, and no proposed rewording are
required. Feedback never changes a translation, a glossary entry, a term
record, or a readability status. An editor reads it, decides, and records why.

## Where things live

| Path | Role |
| --- | --- |
| `includes/feedback/config.json` | which surfaces are enabled, the service endpoint, the reader-facing note |
| `includes/feedback/paragraph-ids/<surface>.json` | stable passage identifiers, maintained by `scripts/paragraph_ids.py` |
| `includes/feedback/term-maps/<surface>.json` | editor-written passage-to-term mappings |
| `includes/feedback/comprehension/<surface>.json` | versioned comprehension question sets with assessment guidance |
| `scripts/reader_feedback.py` | validates those inputs and builds the page manifest |
| `scripts/generate_reader.py` | embeds the manifest and the hidden feedback section on enabled pages |
| `reader-src/javascripts/reader-feedback.js` | the reader-side controls |
| `feedback_service/` | the separately deployable submission service and maintainer queue |
| `scripts/stage_feedback_evidence.py` | the checked path from a reviewed session export into the newcomer ledger |
| `reviews/facilitator-guide.md` | how to run a real newcomer session |

Both new checks run inside `scripts/run_checks.py`: "Passage identifiers"
and "Reader feedback inputs".

## The pilot

Feedback is enabled on the three pilot texts: **SN 36.6**, **AN 2.9**, and
**AN 3.65**. SN 36.6 went first (the reasons are in the plan: Essential Five,
on a newcomer pathway, the most governed terminology, one-session length)
and is the only one with an editor-written term map; on the other two,
term mappings come from the words-used panel until an editor writes their
maps. Enabling a further text is one line in `enabled_surfaces` plus
`python scripts/paragraph_ids.py --write --surface <key>`.

Everything in `includes/feedback/comprehension/` is marked
`"editorial_status": "draft"`. Nothing has been through source review. To
approve a set, an editor records the review in a repository file, then sets
`approved_on` and `approval_evidence` to that file; the input check refuses an
approved set without both. Readers are shown draft questions on the pilot
page, and every response records the question version, its content hash, and
the editorial status at the time.

## What a submission carries

Captured automatically from the page manifest, never typed by the reader:

- the surface key and label, and the page path;
- the stable passage id, its text fingerprint, its section, and the exact
  wording shown, taken from the rendered paragraph;
- the translation body hash (`READABILITY_BODY_SHA256`), the same version
  the evidence ledger binds to;
- governed term ids with their basis (`explicit` from the term map,
  `glossary` from the words-used panel), or an explicit `unmapped` state;
- the version of each relevant glossary explanation (a hash of its text) and
  the version of the introduction (a hash of the guide record or intro file);
- the target: translation, glossary, introduction, or comprehension;
- for a comprehension review, the question set version, content hash, and
  editorial status;
- the receipt time, recorded by the service.

Feedback is never deleted or rewritten when a translation changes. A later
revision is compared against it by version: the queue filters by body hash,
and the passage map keeps the previous fingerprint of an edited passage.

## Stable passage identifiers

`scripts/paragraph_ids.py` owns `includes/feedback/paragraph-ids/`. A passage
is a blank-line-separated block inside the `## Translation` section that is
not a heading. Ids (`p001`, `p002`, ...) are allocated once per surface and
never reused. After editing an enabled translation:

```bash
python scripts/paragraph_ids.py --write
python scripts/generate_reader.py --write
```

The alignment rules, in order of precedence:

1. An unchanged passage keeps its id wherever it moved.
2. An edited passage between the same neighbours keeps its id; its previous
   fingerprint is kept in `previous_fingerprints`.
3. One passage that became several: the first part keeps the id, the rest get
   new ids with `split_from`.
4. Several passages that became one: the survivor keeps the first id, the
   others are retired with `merged_into`.
5. A new passage gets a new id; a removed one is retired with the body hash
   that removed it.

`--check` fails when a map is stale, so an edited translation cannot be
regenerated with wrong ids.

## Term mappings

Feedback carries a governed term id only from two explicit sources:

- the editor-written term map, marked `explicit`, written from the surface's
  governing decisions in its notes file;
- the words-used panel, marked `glossary`, where a glossary rendering occurs
  in the passage as a whole phrase and equals a governed record's preferred
  rendering. This is the same mechanism the panel itself uses, not a looser
  substring match.

Anything else is `unmapped`. The queue shows the basis with every term, and
the disposition form has a field for confirmed or corrected term ids. The
bounded mapping work for the pilot is `term-maps/sn36_6.json`; the verses
are deliberately left unmapped. To map another surface, write its map from
its notes file; the input check rejects unknown term ids and passage ids.

## Editorial workflow

Lifecycle: **received → examined → proposed change → revised → checked with
readers**. For each submission the maintainer queue records:

- the observed readability problem;
- where the fix belongs: translation, glossary, introduction, shared lexicon,
  or no change;
- the editorial rationale;
- a reference to the resulting change (commit, pull request, or notes file);
- follow-up evidence, only if actually collected (a session code, an export,
  or later submission ids);
- confirmed or corrected term ids.

Every disposition is appended to a history; nothing is overwritten and the
original response stays visible. The by-term view groups submissions across
suttas so repeated confusion about one rendering can be raised as a lexicon
question through the normal term-record process rather than patched locally.

The service has no AI assistance. If any is added later it must be advisory
only, must never hide or summarise away the original response, and must never
take a lifecycle step or an assessment by itself.

## Public feedback and formal evidence

Two channels, never mixed:

- **Public**: anything submitted without a session link. Read for insight;
  never counted toward the newcomer threshold; never exported as evidence.
  Anonymous submissions cannot establish unique participants.
- **Formal**: submitted through a facilitator's link carrying a session code
  and an anonymous participant label. Counted once per participant per body
  version; a repeat is stored but marked as not counting. Participants can be
  marked `returning` with the earlier session and label, so a revision can be
  judged with fresh newcomers and returning readers separately.

The reviewed export of a session includes only assessed, counted responses
whose independence the facilitator recorded, and lists everything else as
excluded with the reason. A returning participant is never independent: the
service refuses to record it, the export says `follow_up: true`, and
`scripts/stage_feedback_evidence.py` stages them under their earlier ledger
label with `independent: false`, which the ledger checker counts as a
participant and never as an independent pass. Responses to a draft question
set stay exploratory: the staging script leaves them out unless an editor
runs it with `--accept-draft-questions`, and that acceptance, the question
version, and the question set hash are written on the staged record. The
script appends only when `check_newcomer_reviews.py` still passes. Promotion to `validated` remains
the two-key operation in the protocol; nothing in this path performs it.

## Running the whole workflow locally

```bash
python scripts/run_checks.py                      # includes the new checks
mkdocs build --strict
python -m feedback_service hash-password          # choose a maintainer password
export FEEDBACK_MAINTAINER_USER=editor
export FEEDBACK_MAINTAINER_PASSWORD_HASH='pbkdf2_sha256$...'
export FEEDBACK_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
python -m feedback_service serve --site-dir site
```

Then:

1. Open `http://127.0.0.1:8765/suttas/sn36-6-salla-sutta/`. The service
   serves the built site, so the page's health probe succeeds on the same
   origin and the controls appear.
2. Use "Give feedback" after a passage, rate an explanation in the words-used
   panel, and complete the review at the end of the page.
3. Open `http://127.0.0.1:8765/admin/`, filter the queue, open a submission,
   and record a disposition.
4. For a formal session: create a session and participants under Sessions,
   open the page with `?session=<code>&participant=R1`, submit the review,
   assess it, record independence, export the session, and run
   `python scripts/stage_feedback_evidence.py --export session.json`.

The rendered tests do the same in Chromium:
`pnpm test:a11y` runs the accessibility suite and
`tests/browser/reader-feedback.spec.js` against a throwaway database.

## Operator notes

Storage, access, retention, backup, and deletion are described in
[`feedback_service/README.md`](../feedback_service/README.md). In short:
SQLite with numbered migrations; HTTP Basic maintainer access from
environment variables with no defaults; no contact details unless
`FEEDBACK_ALLOW_CONTACT=1`, and then only with consent in a separate table;
`backup`, `purge --older-than`, and `delete` commands; request logs without
bodies.

## The Google Form transport

The public site uses a transport instead of a hosted service:
`includes/feedback/config.json` names a Google Form the editors own
(`transport.form_action` and `transport.payload_field`). The page posts each
submission as one JSON string into the form's single long-answer question.
Readers see the same controls. The browser cannot read the form's reply, so
the page says "sent", not "received", keeps the reader's text, and offers
"Send again"; the client submission id stays the same, so a repeat is
dropped on import. Receipt was verified end to end on 2026-09-13: two test
submissions from the public SN 36.6 page reached the responses sheet and
imported into the queue with the expected passage ids, fingerprints, body
hash, and term mappings. Repeat that check after any change to the form.

To read feedback: open the form's **Responses** tab, open the linked
spreadsheet, download it as CSV, then

```bash
python -m feedback_service ingest --csv responses.csv
python -m feedback_service serve
```

`ingest` applies the same validation as the live endpoint, resolves formal
session codes against the local sessions, and skips rows already stored.
The queue, dispositions, sessions, exports, and evidence staging then work
exactly as described above, on the maintainer's machine. Delete rows from
the sheet once they are in the queue if you want the form to hold nothing.

## Deployment status

No hosted service is deployed and none is required: the public site posts
to the Google Form transport above, and the maintainer queue runs on the
editor's machine over the ingested responses. Hosting the service instead
(so the queue is reachable from anywhere and submissions are stored
directly) remains an option; the steps are under "Deploying" in the
service README, and switching is a config change from `transport` to
`endpoint`.

## Keeping the page readable

On devices with a mouse or trackpad, the passage controls are transparent
until the passage is hovered, the control is focused, or its form is open;
they remain in the document at full size, so keyboard and screen-reader
users find them in the normal order. Touch screens have no hover, so there
the controls are always shown. This is a presentation choice in
`reader.css`, not a change to what is collected.

## Limitations of the first version

- No feedback without JavaScript. The GitHub issue link in the source-and-
  status panel remains the no-script route.
- No text-selection feedback; the passage control is the unit.
- No feedback on the standalone glossary page; explanations are rated from
  the per-page words-used panel.
- The by-term grouping depends on explicit or glossary-backed mappings; an
  unmapped passage appears only under its sutta and passage until an editor
  confirms a term.
- The service is single-instance SQLite. That is appropriate for the volume
  a pilot text will see; it is not a design for many concurrent writers.
- Comprehension questions are drafts pending editorial review.
- Actual improvement in comprehension has not been demonstrated. That needs
  real readers, real sessions, and a revision judged against them.

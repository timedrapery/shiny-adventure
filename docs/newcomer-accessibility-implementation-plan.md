# Newcomer Accessibility Implementation Plan

## Goal

Make the Pali suttas usable by contemporary English speakers who have never
studied Pali or encountered Buddha-Dhamma before. A newcomer should be able to
begin with a short text, understand what happened and why it matters, meet
technical vocabulary without getting stranded, and know what to read next.

The governed translation remains authoritative. Orientation, definitions,
navigation, and optional reading aids must help the reader without silently
adding doctrine to the translated text.

## Current baseline

- 61 governed translations are published with reading times, source
  disclosures, navigation, and page-specific words-used panels.
- The corpus passes the automated plain-English register audit.
- Five texts have structured newcomer guides and twelve more have dedicated
  reader introductions.
- The review ledger records zero of thirty-five required newcomer sessions and
  zero of seven required read-aloud reviews. Automated checks are not a
  substitute for these human gates.

## Recommended First 12

These texts form the deliberately small, testable front door to the larger
collection. The order starts with short, recognizable teachings and introduces
foundational material only after the reader has some footing.

1. AN 2.9, *What Keeps the World Human*
2. SN 45.2, *Good Friendship Is the Whole Path*
3. SN 56.17, *What Ignorance Means*
4. SN 36.6, *One Arrow, Not Two*
5. AN 8.6, *When Life Goes Up and Down*
6. AN 11.12, *Six Things to Remember Anywhere*
7. AN 3.65, *How to Test a Teaching*
8. MN 63, *The Man Struck by a Poisoned Arrow*
9. SN 56.11, *The First Teaching*
10. SN 22.59, *What Is Fit to Call Self?*
11. MN 19, *Two Kinds of Thinking*
12. SN 12.44, *How the World Arises—and Ends*

## Implementation order

### 1. Run a three-text human pilot

Pilot AN 2.9, SN 36.6, and AN 3.65. They represent a very short teaching, a
concrete practical teaching, and a longer foundational dialogue.

For each newcomer, record only the anonymous evidence required by the existing
review protocol:

- what happened or was discussed;
- the practical point;
- any word or sentence that caused a stop or reread;
- whether both paraphrases were independently accurate.

Also complete a full read-aloud review of each text. Do not invent, infer, or
backfill human evidence. A useful product-level target is that at least four of
five newcomers can explain both the situation and practical point, no recurring
unexplained term blocks comprehension, and no sentence repeatedly causes a
reread.

### 2. Revise recurring problems from the pilot

Change wording only when the evidence identifies a recurring problem or when a
read-aloud pass exposes a clear spoken-English failure. Re-run source-fidelity,
terminology, plain-English, reader-generation, and accessibility checks after
each affected batch. Repeat affected human reviews when a material change
invalidates their evidence.

### 3. Establish the First 12 as a governed reader collection

Represent the First 12 in the shared surface registry rather than duplicating
the list across templates. Add automated checks for membership, order, unique
entries, valid public pages, reading metadata, and navigation.

### 4. Give every First 12 text a structured newcomer guide

Extend the existing evidence-checked guide format beyond the Essential Five.
Each guide must include:

- what happens;
- the central question;
- the main practical point;
- a reading cue;
- what the text is not saying;
- three to six key words already supported by the reader glossary;
- one or more governed translation sections that support the guide.

After the First 12 are complete, extend the same coverage to all texts in Sets
1 and 2 of the newcomer reading order.

### 5. Introduce a first-encounter terminology rule

A newcomer should not need prior Pali study, a separate glossary visit, or a
hover interaction to understand the current passage. On first meaningful use,
an unavoidable Pali term or distinctive house rendering should have an
immediate short explanation available in the reading flow.

Implement this as reader annotation or orientation, not as an unmarked addition
to the governed translation. Keep the full words-used panel for deeper help.
Prioritize terms such as *bhikkhu*, *arahant*, *nibbāna*, Dhamma/dhamma,
Saṅgha, heart, thinking mind, composure, and remembering.

### 6. Simplify the public front door

Give the homepage one dominant low-commitment action: read a teaching that
takes about two minutes. Beneath it, offer three short pathways:

- I am curious but skeptical.
- I am dealing with stress or pain.
- I want something practical to try.

Each pathway should contain three to five texts, show its approximate total
reading time, and end with a clear next choice. Preserve the complete 61-text
reading order and advanced filters for readers who want them.

### 7. Complete human validation of the First 12

Use the existing newcomer-review ledger and machine gate. A surface becomes
`validated` only after source fidelity, newcomer comprehension, and full
read-aloud review all pass. Publish an honest progress summary; provisional
texts must remain visibly provisional.

### 8. Improve the presentation of long and repetitive texts

Do not delete repetition from the authoritative translation. Instead, add
optional presentation aids:

- label the repeated pattern;
- show what changes from one cycle to the next;
- add section progress cues;
- allow repeated blocks to collapse in a guided-reading view while keeping the
  complete text available;
- keep explanatory transitions outside the governed translation.

Start with MN 10, MN 118, MN 22, DN 2, and the longer dependent-arising texts.

### 9. Add listening after wording is stable

Add reviewed narration or carefully checked text-to-speech to the validated
First 12 before considering corpus-wide audio. Audio must follow the complete
translation, expose useful section navigation, and meet the same read-aloud
standard as the page.

### 10. Balance future translation selection

Keep lexicon leverage as an editorial concern, but score future public-reading
priorities separately for newcomer value:

- standalone clarity;
- a recognizable human problem;
- reading time under ten minutes;
- memorable narrative, image, or dialogue;
- an observable or practicable point;
- the amount of prior Buddhist vocabulary assumed.

Translation-roadmap priority and reader-order priority may differ. Record both
instead of forcing one ranking to serve both purposes.

## Delivery milestones

### Milestone A — Pilot-ready

- This plan is published.
- The First 12 are represented in project data.
- AN 2.9, SN 36.6, and AN 3.65 have complete guide and review materials.
- A reviewer can perform and record the three-text pilot without editing JSON
  by guesswork.

### Milestone B — First 12 reader experience

- All twelve structured guides pass evidence and glossary validation.
- The homepage offers a two-minute start and three newcomer pathways.
- First-encounter terminology help works without hover and without changing the
  governed translation.
- Reader, EPUB, link, and accessibility checks pass.

### Milestone C — Human validated

- All required newcomer and read-aloud evidence is recorded.
- Recurring comprehension failures have been repaired and re-reviewed.
- Passing First 12 surfaces are marked `validated` by the existing machine
  gate.

### Milestone D — Deeper access

- Guided repetition controls are available on selected long texts.
- Reviewed audio is available for the stable First 12.
- New translations are prioritized with both editorial-leverage and
  newcomer-value scores.

## Immediate next action

Prepare the three-text pilot and the First 12 infrastructure, then ask real
newcomers to read AN 2.9, SN 36.6, and AN 3.65. The human evidence is the next
decisive input; implementation may prepare and improve the experience, but it
must not claim that unperformed reviews have passed.

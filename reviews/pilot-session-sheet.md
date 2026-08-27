# Newcomer Pilot Session Sheet

Use one copy per participant and per text. This worksheet is for taking notes
during a session; only the anonymous fields required by the ledger belong in
Git. Do not write a participant's name, contact details, demographics, or
private remarks here or in the repository.

## Before the session

- Text: AN 2.9 / SN 36.6 / AN 3.65
- Anonymous participant label: R__
- Date: YYYY-MM-DD
- Confirmed new to early Buddhist suttas: yes / no
- Translation notes and glossary page withheld: yes / no

Give the participant only the public reader page. Do not define a term or
explain the teaching while they read.

## Ask without prompting

### 1. What happened?

“In your own words, what happened or what was being discussed?”

Notes:

### 2. What is the practical point?

“What do you think the practical point is?”

Notes:

### 3. Where did the reading catch?

“Which word or sentence made you stop or reread?”

Exact words or sentences:

### 4. Is the next step clear?

“If you wanted to continue, would you know what to read next?”

Notes for navigation improvements (do not enter these in the governed ledger
unless they identify a concrete page problem):

## Reviewer decision

- Both paraphrases were materially accurate without prompting: yes / no
- Independent session: yes / no
- Recurring problem already seen in another session: yes / no
- If yes, issue to investigate:

## Ledger-ready record

Copy this object into the correct surface's `newcomer_reviews` list only after
replacing every placeholder with the participant's actual, unprompted evidence.

```json
{
  "participant": "R__",
  "reviewed_on": "YYYY-MM-DD",
  "independent": true,
  "what_happened": "Participant's unprompted paraphrase.",
  "practical_point": "Participant's unprompted paraphrase.",
  "confusing_words": [],
  "pass": true
}
```

## Separate full read-aloud review

- Anonymous reviewer label: A__
- Date: YYYY-MM-DD
- Complete translation read aloud from beginning to end: yes / no
- Sentences that were hard to say or understand on first hearing:
- Result: pending / complete

Do not mark the ledger's read-aloud gate complete unless the whole translation
was read aloud and a dated reviewer observation was recorded.

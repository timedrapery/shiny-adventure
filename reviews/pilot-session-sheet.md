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
- Has this person read an earlier version of this text? yes / no
  (if yes, this is a follow-up: see *Returning readers* below)
- Translation notes and glossary page withheld: yes / no
- Body hash of the text they are about to read:

Get that last one before the session, and paste the same value into the record
afterwards. It is what ties the evidence to the words this person actually read:

```bash
python - <<'EOF'
from pathlib import Path
from scripts.check_readability_reviews import translation_body_sha256
print(translation_body_sha256(Path("docs/translations/an2-9-cariya-sutta.md")))
EOF
```

The three pilot texts are `docs/translations/an2-9-cariya-sutta.md`,
`docs/translations/sn36-6-salla-sutta.md`, and
`docs/translations/an3-65-kesamutta-sutta.md`.

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
  "pass": true,
  "body_sha256": "the hash recorded before the session",
  "follow_up": false
}
```

Then run `python scripts/check_newcomer_reviews.py`. It will tell you if
anything is missing or inconsistent; it cannot tell whether the evidence is
real, which is the part that rests on you.

### Returning readers

If this person read an earlier version of the same text, set `follow_up` to
`true` and `independent` to `false`, and leave their earlier record exactly as
it is. A follow-up counts as one of the five participants for this version of
the text but never toward the four independent passes: someone who has already
read an earlier draft cannot give a first unprompted account of it.

A follow-up is still worth running. It is the only way to learn whether a
revision fixed the thing that confused that particular reader.

## Separate full read-aloud review

- Anonymous reviewer label: A__
- Date: YYYY-MM-DD
- Complete translation read aloud from beginning to end: yes / no
- Sentences that were hard to say or understand on first hearing:
- Body hash of the text that was read aloud:
- Result: pending / complete

The read-aloud gate records its `body_sha256` too, in the
`human_read_aloud` object beside the reviewer labels.

Do not mark the ledger's read-aloud gate complete unless the whole translation
was read aloud and a dated reviewer observation was recorded.

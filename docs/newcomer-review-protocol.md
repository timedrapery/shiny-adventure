# Newcomer Comprehension Review Protocol

This is the human gate between a technically checked translation and a reader-
validated one. Automated checks cannot substitute for it.

Use the [newcomer review workboard](../reviews/README.md) for public links and
current progress. The JSON ledger remains authoritative.

## Cohort and threshold

The current cohort is the newcomer First 12 defined in
`scripts/surface_registry.py`. Each text needs five people who are new to early
Buddhist suttas. At least four must be able to explain both what happened and
the practical point without being fed the answer.

Begin with the three-text pilot: AN 2.9, SN 36.6, and AN 3.65. Do not wait for
the other nine texts before acting on a recurring problem found across these
three different lengths and forms. A wording change that materially affects a
reviewed passage invalidates the affected evidence and must be reviewed again.

Record only anonymous participant labels such as `R1`. Do not record names,
email addresses, demographic data, or private contact details in the repo.

## Session

1. Give the participant the public reader page without the translation notes.
2. Ask them to read it at their own pace. Do not explain specialist terms.
3. Ask: “In your own words, what happened or what was being discussed?”
4. Ask: “What do you think the practical point is?”
5. Ask which sentence or term made them stop or reread.
6. Ask: “If you wanted to continue, would you know what to read next?” Record
   the answer outside the repository unless it identifies a concrete page
   problem; the governed ledger deliberately stores only comprehension
   evidence.
7. Separately, have a reviewer read the complete translation aloud and record
   any sentence that is hard to speak or understand on first hearing.

A comprehension pass means both paraphrases are materially accurate and were
given without prompting. Small vocabulary differences are not failures.

## Ledger fields

Add a record to `reviews/newcomer-review-ledger.json`:

```json
{
  "participant": "R1",
  "reviewed_on": "2026-08-24",
  "independent": true,
  "what_happened": "The participant's unprompted paraphrase.",
  "practical_point": "The participant's unprompted paraphrase.",
  "confusing_words": ["word or sentence, if any"],
  "pass": true,
  "body_sha256": "the hash of the body this reader actually read",
  "follow_up": false
}
```

`body_sha256` is the hash of the translation body the participant was given.
Get it for the current body with:

```bash
python - <<'EOF'
from pathlib import Path
from scripts.check_readability_reviews import translation_body_sha256
print(translation_body_sha256(Path("docs/translations/an2-9-cariya-sutta.md")))
EOF
```

Recording it is required; matching today's body is what makes the review count
toward the threshold. When wording changes, the earlier records stay in the
ledger as history and stop counting, and the gate needs fresh sessions. Do not
edit an old record's hash to make it current — that claims a reader saw text
they never saw.

## Returning readers

A participant may review more than one version of the same text, and the
earlier record stays. What must be unique is the pair of participant and body:
one record per person per version.

A later session by someone who already read an earlier version is a follow-up,
and records `follow_up: true` with `independent: false`. It counts as one of
the five participants for that version — they did read it — but never toward
the four independent passes. Someone who has read an earlier draft cannot give
a first unprompted account of the text, and counting them as a fresh newcomer
would inflate the only number the gate really rests on.

Prefer new participants when you can get them. A follow-up is worth recording
for a different reason: it shows whether a revision fixed the thing that
confused that reader the first time, which a new reader cannot tell you.

## Source fidelity

The source-fidelity gate records the `body_sha256` it reviewed, exactly as the
other two gates do: the sign-off says *this English renders this Pali*, so it
is about a translation, not about a filename. When the body changes, the
sign-off stops counting and the changed passages need a real reassessment.

A sign-off that cannot be tied to the body now published is not deleted and not
left standing. It moves to a `superseded_signoff` block — original date,
evidence file, and the reason it does not carry forward — and the gate returns
to `pending`.

For a read-aloud review, add an anonymous reviewer label and dated observation
under `human_read_aloud.reviewers`, record the `body_sha256` that was read
aloud, then set that gate to `complete` only when the full text has been read
aloud.

Run `python scripts/check_newcomer_reviews.py`. The check rejects duplicate
participants, incomplete evidence, evidence without the body it was gathered
against, a false promotion to `validated`, or a missing companion document. It
reads the promotion requirement from `scripts/surface_registry.py`, so a
surface marked `validated` there must have a complete ledger record even if it
is not listed in the cohort. Once all three gates pass, change the surface's
readability status to `validated` in `READABILITY_STATUS` and update its body
hash if wording changed.

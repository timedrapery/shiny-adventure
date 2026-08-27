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
  "pass": true
}
```

For a read-aloud review, add an anonymous reviewer label and dated observation
under `human_read_aloud.reviewers`, then set that gate to `complete` only when
the full text has been read aloud.

Run `python scripts/check_newcomer_reviews.py`. The check rejects duplicate
participants, incomplete evidence, a false promotion to `validated`, or a
missing companion document. Once all three gates pass, change the surface's
readability status to `validated` and update its body hash if wording changed.

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
   any sentence that is hard to speak or understand on first hearing. That is
   its own gate with its own procedure; see [Read-aloud review](#read-aloud-review).
   It does not depend on this session and should not wait for one.

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

## Read-aloud review

This gate is separate from the newcomer sessions and much cheaper to run. It
needs one reviewer and a voice, not five recruited strangers, and the whole
three-text pilot is about twenty minutes of reading. Nothing about it waits on
recruitment, so it should not be queued behind it.

Generate the session kit first:

```bash
python scripts/read_aloud_kit.py --surface sn36_6
```

The kit carries the current `body_sha256`, computed rather than copied, and the
translation split into numbered sentences. Add `--facilitator` for the measured
watch points from the spoken register profile, and withhold that section until
after the read: a reviewer who has been told where the awkward sentences are is
no longer giving a first hearing.

Run it like this:

1. Read the whole translation aloud at a speaking pace, to the end. Silent
   review does not satisfy this gate, and a section skipped is a section
   unreviewed.
2. Do not stop to fix anything. Mark the sentence number and carry on.
3. Mark a sentence when you have to restart it, run out of breath, breathe
   where the punctuation offered nowhere to, say a word you would not say out
   loud, or finish unsure of who was speaking.
4. A listener is optional and useful. What they could not follow on first
   hearing is the thing silent review cannot reach; record it separately.

### What to record

Record the location, not a verdict. A gate that stores one boolean per surface
throws away the only part that tells an editor what to change.

```json
{
  "status": "complete",
  "body_sha256": "the hash of the body that was read aloud",
  "reviewers": [
    {
      "label": "A1",
      "reviewed_on": "2026-09-17",
      "read_complete": true,
      "observations": [
        {
          "sentence": 14,
          "line": 62,
          "problem": "What caught, in the reviewer's words."
        }
      ]
    }
  ]
}
```

Sentence numbers come from the kit and are stable for as long as the body is.
If the body changes the hash changes with it, so a number can never quietly
come to point at different words.

An empty `observations` list is a real result. A reviewer who read the whole
text and stumbled nowhere has told you something; an invented stumble has not.

`read_complete: false` with the observations gathered so far is the honest
record of a session that stopped early. Leave `status` at `pending` in that
case: a partial read is worth keeping and is not the gate.

Run `python scripts/check_newcomer_reviews.py`. The check rejects duplicate
participants, incomplete evidence, evidence without the body it was gathered
against, a false promotion to `validated`, or a missing companion document. It
reads the promotion requirement from `scripts/surface_registry.py`, so a
surface marked `validated` there must have a complete ledger record even if it
is not listed in the cohort. Once all three gates pass, change the surface's
readability status to `validated` in `READABILITY_STATUS` and update its body
hash if wording changed.

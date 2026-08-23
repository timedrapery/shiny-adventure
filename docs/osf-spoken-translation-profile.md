# OSF Spoken-Translation Profile

## Status

- Profile version: `osf-spoken-v1-pilot`
- Rollout scope: every translation surface registered in
  [`scripts/surface_registry.py`](../scripts/surface_registry.py), as of
  2026-08-22
- Original calibration surface: `SN 36.6`
- Review status: `pilot`
- Human approval gates: editor read-aloud and newcomer-comprehension review
  are still pending
- Governing standard:
  [PLAIN_ENGLISH_STANDARD.md](PLAIN_ENGLISH_STANDARD.md)
- Evidence manifest:
  [osf-spoken-translation-sources.json](../candidates/source-manifests/osf-spoken-translation-sources.json)

This profile governs sentence-level spoken English in OSF translation
surfaces. It does not override the Pali, a term record, a phrase record, or a
documented ambiguity. Corpus-wide coverage records which bodies received this
pass; it does not mean that Dhammarato, Alexander H, or newcomer readers have
approved them.

## Source Hierarchy

Use these controls in order:

1. The Pali and its segmentation control meaning, speakers, sequence, and
   repetition.
2. Governed records in `terms/` control lexical and formula choices.
3. Repository authority profiles control practical teaching posture.
4. Dhammarato transcript evidence calibrates reusable spoken techniques.
5. Authorized OSF editor samples calibrate final cadence and warmth.
6. Read-aloud and newcomer review show whether the result works in practice.

If a more natural sentence requires changing a governed rendering, stop the
surface pass. Make the term- or phrase-family decision openly and move every
linked control together.

## Core Voice

### Start with what is happening

Name the person, action, feeling, question, or consequence. Do not begin with
an abstract explanation when the source gives a scene.

### Use one spoken move at a time

A spoken move is a question, answer, reason, example, contrast, consequence,
or instruction. Prefer a clean sequence of these moves over one sentence that
nests several of them.

### Ask real questions

Questions should sound like something one speaker could ask another. Preserve
the source's answer and its timing; do not add rhetorical questions merely to
make the translation lively.

### Prefer concrete verbs

Let people feel, ask, listen, resist, look, know, and let go. Keep governed
technical nouns when they are doing real work, but rebuild the grammar around
them when that makes the action easier to hear.

### Make contrasts easy to hear

When the source contrasts two people, choices, causes, or outcomes, keep the
same terms on both sides and let the changed element stand out. Do not vary
synonyms for style inside a controlled contrast.

### Keep oral repetition

Repetition is part of the text's structure. First make the repeated unit a
good spoken sentence. Then repeat it without decorative synonym changes.

### Sound contemporary, not trendy

Neutral contractions are welcome. Slang, internet idiom, fashionable therapy
language, and imported inspirational language are not. Warmth should come
from clear syntax, honest questions, and human-scale pacing.

## Dhammarato Calibration

The full public index at <https://dhammarato.com/blog/> is eligible reference
evidence. Profile version `osf-spoken-v1-pilot` uses representative pages in
the evidence manifest to cover beginner teaching, question-and-answer
exchanges, practical reframing, sutta retelling, and the one-arrow/two-arrows
teaching.

The archive calibrates voice; it does not replace the canonical source. Before
a passage supports a stable profile claim, an editor must identify
Dhammarato's own turns on the multi-speaker page and check automatic captions
against the recording. Transcript summaries, other speakers, false starts,
filler, one-off jokes, provocative rhetoric, and signature catchphrases do not
become house style.

## Alexander H Calibration

The editor supplied the public YouTube playlist recorded in source `OSF-AV-1`
for this purpose. Speaker-labelled transcript evidence from `OSF-AV-6` and
`OSF-AV-7` supports these provisional traits:

- invite shared investigation: ask the listener to look and see
- name the familiar habit or difficulty before offering a reframe
- move from the old pattern to the available choice now
- use ordinary situations and visible consequences
- repeat one short central point so the listener can carry it away
- keep the relationship warm and collaborative

Raw speech also contains filler, long rolling clauses, personal examples, and
direct second-person address. Those are not copied automatically. Canonical
translation keeps the directness and question pattern while shortening the
syntax; it uses `you` only when the Pali addresses the listener.

## Evidence And Rights Rule

The repository stores source URLs, speaker scope, review state, rights state,
and derived observations only. It does not commit transcript bodies. Public
availability and permission to use a source for calibration do not by
themselves grant permission to redistribute a transcript.

Automatic captions are discovery aids until checked against the recording,
especially where Pali vocabulary is involved. A multi-speaker source may not
support a speaker-specific claim until the relevant turns are identified.

## Surface Workflow

1. **Semantic lock:** list the source segments, governed terms, recurring
   formulas, speakers, repetitions, and deliberate ambiguities.
2. **Voice draft:** revise sentence realization, cadence, dialogue, and
   paragraphing without silently changing lexical policy.
3. **Read-aloud review:** mark any line the designated editor would not
   naturally say.
4. **Fidelity review:** map every changed proposition back to the source and
   record meaning-sensitive calls in the companion notes.
5. **Governance review:** run term, formula, drift, and family checks.
6. **Newcomer review:** show the rendered translation without notes to at least
   five readers new to Buddha-Dhamma.
7. **Publish:** regenerate the reader from the canonical surface and run the
   full verification suite.

## Approval Standard

`approved` means all of the following are recorded:

- the designated editor completed the read-aloud pass
- fidelity review found no unsupported addition, omission, speaker change,
  sequence change, or resolved ambiguity
- governed renderings and formulas pass their checks
- at least four of five newcomers can state what happened and the practical
  point in their own words
- the canonical translation-body hash still matches the reviewed body

Until then the honest status is `pilot`, even when the draft and automated
checks are complete.

## Attribution Boundary

This is an OSF house profile informed by public source material. It does not
claim that Dhammarato, Alexander H, or another source speaker translated,
reviewed, approved, or endorsed a particular translation unless that action is
separately recorded.

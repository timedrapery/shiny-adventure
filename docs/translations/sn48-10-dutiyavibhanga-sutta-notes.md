# SN 48.10 Translation Notes

This document is the companion rationale for
[SN 48.10: Dutiyavibhaṅga Sutta](sn48-10-dutiyavibhanga-sutta.md). The main
translation is the primary study surface; this file records debated
translation choices, source-audit calls, and edition notes that govern it.

## Source Base

- Primary source: the Pali text of SN 48.10 as segmented in SuttaCentral's
  Bilara data.
- Control surface: the repository's current term policy, especially `indriya`,
  `saddhā`, `vīriya`, `sati`, `samādhi`, `paññā`, `jhāna`, `pīti`, `sukha`,
  `ekaggatā`, `upekkhā`, `vossagga`, `citta`, and `chanda`.
- The discourse is 297 Pali words across 40 body segments. It is short because
  four of its five definitions are stock passages stated in full elsewhere.

## Governing Decisions

- **The definitions are quoted from the corpus, not re-solved.** Four of the
  five faculties are defined here by passages that governed surfaces already
  carry: the four right efforts (SN 51.13), the four establishments of
  remembering (MN 10), the four mental themes (the governed jhāna formula),
  and the epithets of the Buddha (MN 38). Their wording is reused verbatim.
  Re-translating them locally would have produced five subtly different
  Englishes for text the corpus states identically, which is the drift the
  formula records exist to prevent.
- **`pīti` and `sukha` are rendered `rejoicing` and `satisfaction`, not
  `delight` and `ease`.** This is the governed policy and it is worth stating
  plainly because the corpus does not currently follow it — see the re-audit
  call below. The `pīti` record carries an explicit context rule, *"when
  contrasted directly with sukha in jhāna formulas"*, and its rendering is
  `rejoicing`.
- `indriya` keeps `faculty`. The alternate reading, `spiritual faculty`, adds
  a word the Pali does not have and imports a register the discourse avoids:
  every definition here is behavioural.
- `saddhā` keeps `confidence` rather than `faith`. The discourse defines it as
  something placed in a specific object for a stated reason — the awakening of
  the Tathāgata, followed by the epithets that say what that awakening
  consists of. `Faith` would make the placement unnecessary.
- `saddahati tathāgatassa bodhiṁ` is rendered `place confidence in the
  awakening of the Tathāgata`, keeping the verb cognate with the noun so the
  faculty and its exercise read as the same word in English as in Pali.
- `bhagavā` inside the epithet string follows the house pattern: the leading
  `itipi so bhagavā` is `So indeed is the Buddha`, and the closing `bhagavā`
  is the adjective `blessed`, as in DN 2 and MN 38. `The Blessed One` is a
  register signal the audit flags and was corrected before commit.
- `vossaggārammaṇaṁ karitvā` is rendered `having made relinquishment the
  object`. `Ārammaṇa` is the object of attention rather than a cause, so
  `taking relinquishment as the basis` was rejected as importing a
  causal claim.
- `satinepakkena samannāgato` is rendered `possess the highest carefulness in
  remembering`. `Nepakka` is ungoverned; see below.
- `dhammā` is rendered `qualities` in the right-effort formula and `dhammas`
  in the establishments-of-remembering formula. This is not inconsistency: the
  first means wholesome and unwholesome states of mind, the second is the
  fourth establishment's technical object. Both follow the surfaces the
  passages are quoted from.
- The subject is `they`, carrying the `noble disciple` named at the head of
  each definition, per the register standard's warning against generic `one`.

## Peyyala Handling

The Pali abbreviates three passages. The opening list gives the first and last
faculties and elides the middle three (`saddhindriyaṁ …pe… paññindriyaṁ`), and
the establishments-of-remembering formula gives the first and fourth and
elides the middle two.

This edition marks the elisions where the source marks them. The list is a
special case worth noting: the three elided faculties are each defined in full
immediately afterwards, so nothing is lost by not expanding the header — the
discourse expands it itself.

The peyyala matters for citation. Any phrase quoted from inside an elision
verifies as `inconclusive` rather than `ok`, so all citations added from this
surface quote text the source writes out in full.

## Re-audit Calls

- **The jhāna formula has drifted from its own governed policy across five
  surfaces. Found 2026-08-22, not fixed here.** `pīti` is governed as
  `rejoicing` and `sukha` as `satisfaction`, with an explicit `pīti` context
  rule for jhāna formulas. The corpus renders the formula `delight and ease`
  in DN 2, MN 19, MN 44, MN 99, and MN 141, and `rejoicing and satisfaction`
  in MN 26, MN 38, MN 39, and MN 43. Seven instances against four. This
  edition follows the policy.

  The reason nothing caught it is structural: `check_translation_drift.py`
  detects drift *across term entries*, and no check compares translation prose
  against the renderings the term records govern. That gap is worth a check of
  its own; repairing the five surfaces is a separate editorial pass, not
  something to fold into a new translation.
- **`indriya` and `saddhā` were orphan majors and are anchored by this
  surface.** Both already cited SN 48.10 with phrases the sutta really
  contains — `pañcindriyāni` and `saddhindriya` — and were orphaned only
  because no governed surface carried them. Translating the text was the
  repair; the citations needed no edit.
- **The five faculty minors had no citations at all.** `saddhindriya`,
  `viriyaindriya`, `satindriya`, `samādhindriya`, `paññindriya`, and
  `panca-indriya` each carried a preferred translation and no
  `sutta_references` or `example_phrases`. All six now cite this discourse,
  which defines each of them by name.
- `nepakka` is ungoverned. It occurs in the remembering faculty's definition
  and recurs wherever that faculty is defined, so it is a candidate. Flagged
  rather than governed here, matching house practice for terms exposed by a
  translation.
- `udayatthagāminī paññā` and `nibbedhika` as an adjective are likewise
  ungoverned. `Nibbedhika` has a surface already — AN 6.63, titled *The
  Penetrating Exposition* — so `penetrating` is used here for continuity.
- `vīriyaindriya`'s slug spells the sandhi out where its four siblings collapse
  it (`saddhindriya`, `satindriya`, `samādhindriya`, `paññindriya`). Its `term`
  field is the correct `viriyindriya`, so this is a slug respelling rather than
  a headword mismatch, and the `repo_health.py` queue correctly passes it. Left
  alone; noted so it is not mistaken for a defect later.

## Practice Clarifications

- The five faculties are not five capacities a person has or lacks. Every
  definition here is a description of activity: placing confidence, arousing
  energy, remembering, composing the mind, discerning. The noun form is a
  convenience.
- The faculty of remembering is defined twice over — first as ordinary recall
  of what was said and done long ago, then as the four establishments. The
  discourse puts these side by side without comment, and the translation keeps
  them adjacent rather than subordinating one to the other.
- The faculty of discernment is defined by the four noble truths, which places
  the whole list inside the path rather than beside it. Nothing here is
  preliminary.

## Editorial Presentation

- Section headings are editorial and do not correspond to divisions in the
  Pali.
- Prose is hard-wrapped at 79 columns, per the register standard.

## Edition Status

- This is the first stable study edition of the SN 48.10 surface.
- SN 48.10 is the first Wave 8 translation surface. Wave 8 opened as a
  citation-repair wave rather than a translation wave, and this text was the
  best-ranked candidate left standing once the repair work was done: two
  orphan majors in 297 words, the best ratio in the audit.

## Readability Review

- Standard: `plain-english-v1`
- Status: `provisional`
- Review result: each faculty is introduced by the same direct question and
  then shown through action; the governed right-effort, remembering, mental-
  theme, and truth formulas remain stable.
- Automated governance review: complete; the full repository verification
  suite passed on 2026-08-22.
- Human read-aloud usability review: pending.
- Newcomer comprehension review: pending.

This surface remains provisional until the human reviews are recorded.

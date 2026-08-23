# SN 12.11 Translation Notes

This document is the companion rationale for
[SN 12.11: Āhāra Sutta](sn12-11-ahara-sutta.md). The main translation is the
primary study surface; this file records debated translation choices,
source-audit calls, and edition notes that govern it.

## Source Base

- Primary source: the Pali text of SN 12.11 as segmented in SuttaCentral's
  Bilara data (32 segments).
- Control surface: the repository's current term policy, especially `āhāra`
  and its four compounds, `taṇhā`, `vedanā`, `phassa`, `saḷāyatana`,
  `nāmarūpa`, `viññāṇa`, `saṅkhārā`, `avijjā`, `nidāna`, `samudaya`, and
  `nirodha`, together with the governed dependent-arising chain in SN 12.2.
- Working method: the discourse was governed as one argument that runs the
  four nutriments back to ignorant wanting and then back along the whole chain
  to ignorance, rather than as a list of four items with a chain appended.

## Why This Surface Was Needed

The audit that produced the Wave 6 queue found `āhāra` and its four compounds
among the largest group of orphan major entries in the lexicon: governed
records whose only citation anchor was an untranslated text.

The gap was easy to miss because
[SN 46.51](sn46-51-ahara-sutta.md) is also titled Āhāra Sutta and was already
translated. That discourse is about what feeds and starves the distractions and
the awakening factors, and it deliberately renders `āhāra` with a local
feeding-and-starving idiom rather than the headword default. The consequence
was that `nutriment`, the `āhāra` headword's own default rendering, appeared in
no translation surface anywhere in the repository. This surface is where it
finally governs running text.

## Governing Decisions

- `āhāra` is rendered `nutriment`, the headword default. The four members keep
  their governed compound renderings: `kabaḷīkāro āhāro` is
  `edible-food nutriment`, `phassa` is `contact nutriment`, `manosañcetanā` is
  `mental-intention nutriment`, and `viññāṇaṁ` is `knowing nutriment`.
- `oḷāriko vā sukhumo vā` is rendered `whether coarse or fine`. Neither term is
  governed; the pair describes the grade of edible food, not a doctrinal
  distinction.
- `bhūtānaṁ vā sattānaṁ ṭhitiyā sambhavesīnaṁ vā anuggahāya` is rendered
  `that keep beings going once they have come to be, and that support those
  looking to come to be`. `Ṭhiti`, `sambhavesī`, and `anuggaha` are all
  ungoverned. The line is deliberately kept as two plain verb phrases rather
  than the noun-heavy `for the maintenance of ... and the support of ...`,
  under rule 6 of the plain-English standard.
- `kiṁnidāna kiṁsamudaya kiṁjātika kiṁpabhava` is rendered as four questions:
  `what is their source? what is their origin? what are they born from? what
  produces them?`, with the answer repeating all four. `Nidāna` takes its
  recorded context rule for source-emphasis prose rather than the `link`
  default, which would read oddly here.
- The fourfold quartet is preserved in full at every one of its eight
  occurrences. The Pali repeats it each time. Reference translations often
  abridge the answer to a single word; this edition follows the repository's
  practice of preserving repetition for study readability.
- The chain is reused verbatim from the governed SN 12.2 surface, including
  `taking personally` for `upādāna` and `this whole heap of dissatisfaction`
  for `dukkhakkhandha`.

## Editorial Presentation

- The source abridges the opening with `…` and the dependent-arising chain with
  `…pe…` at both the arising and the quenching end. This edition expands both
  ends from the governed SN 12.2 chain. Expanding rather than reproducing the
  ellipsis follows the same call already recorded in the MN 64 notes.
- The translation is divided into four sections: `The Setting`,
  `The Four Nutriments`, `Where They Come From`, and `The Chain`.
- The title carries the parenthetical `(The Four Nutriments)` to keep it
  distinguishable from SN 46.51 in directory listings and the generated index.

## Re-audit Calls

- `dukkhakkhandha` is not governed by a term record, and the corpus is not
  consistent about it. SN 12.2 has `this whole heap of dissatisfaction ...
  quenches`, which follows the governed `khandha` (`heap`) and `nirodha`
  (`quenching`). SN 12.15 has `this entire mass of dissatisfaction ceases`.
  This surface follows SN 12.2 because that wording matches the governed
  headwords. The SN 12.15 wording should be re-examined, and the compound
  probably deserves a record of its own.
- The fourfold source question is likely to recur — it appears in this pattern
  elsewhere in the Nidāna collection — so it is a candidate for a formula
  record. This surface establishes the wording; a record should follow if a
  second surface needs it. **Resolved 2026-08-21.** Promoted to
  `kim-nidana-kim-samudaya-kim-jatika-kim-pabhava-formula`, which records this
  surface's wording as the governing one. The pass found a third surface as
  well: MN 38 carries the same passage in identical Pali and had re-solved it
  locally. It now follows this surface. DN 21 carries the question form alone
  and is not yet translated.
- `sambhavesī` is left ungoverned. It carries a real distinction against
  `bhūta` that this discourse depends on, and if another surface needs it, it
  should get a minor entry rather than a second local solution.
- `ṭhiti` is ungoverned here, but the lexicon already has `viññāṇa-ṭhiti`
  (`station of knowing`). If `ṭhiti` is ever governed on its own, this line
  should be rechecked for consistency with that compound.

## Practice Clarifications

- The discourse does not treat the four nutriments as four kinds of food in a
  loose sense. Each is something that sustains an ongoing process, which is why
  the argument can run them back to ignorant wanting rather than to appetite.
- The reason the chain is appended is that the question `what produces the
  nutriments?` has already been answered once the answer reaches ignorance.
  The four nutriments are not a separate teaching bolted onto dependent
  arising; they are an entry point into it.

## Spoken-Voice Review

- Profile: `osf-spoken-v1-pilot`
- Status: `pilot`
- Sources: `GOV-PLAIN-1`, `DH-CORPUS-1`, `DH-TEACH-1`, `OSF-AV-1`,
  `OSF-AV-6`, `OSF-AV-7`
- Review result: the direct source questions and repeated answers make the
  nutriment sequence hearable; the governed dependent-arising chain remains
  unchanged.
- Automated governance review: pending the integration run.
- Alexander H read-aloud review: pending.
- Newcomer comprehension review: pending.

This surface remains a pilot until the human reviews are recorded.

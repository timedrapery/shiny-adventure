# SN 51.13 Translation Notes

This document is the companion rationale for
[SN 51.13: Chandasamādhi Sutta](sn51-13-chandasamadhi-sutta.md). The main
translation is the primary study surface; this file records debated
translation choices, source-audit calls, and edition notes that govern it.

## Source Base

- Primary source: the Pali text of SN 51.13 as segmented in SuttaCentral's
  Bilara data.
- Control surface: the repository's current term policy, especially `chanda`,
  `iddhipāda`, `vīmaṁsā`, `vīriya`, `citta`, `samādhi`, `ekaggatā`, `padhāna`,
  `sammappadhāna`, `kusala`, `akusala`, `pāpaka`, `bhāvanā`, and
  `sammā-vāyāma`.
- The discourse is 242 Pali words and consists of a single formula stated four
  times. Almost every decision here is about the formula rather than about
  local phrasing.

## Governing Decisions

- **`chanda` keeps `desire`.** This was the open question the surface was
  chosen to settle. The headword default survives contact with a text where
  `chanda` heads a wholesome path factor, and no context rule was needed. The
  word is not the problem in Pali or in English: what makes `kāmacchanda` a
  distraction is the sensuality, not the desiring. Rendering `chanda` as
  `enthusiasm` or `zeal` here to avoid an awkward-sounding wholesome desire
  would have hidden exactly the continuity the four bases of power depend on.
- `iddhipāda` keeps `basis of power`. The compound names the footing that
  power stands on, not the power itself.
- `vīmaṁsā` keeps `investigation`. The alternate reading, `inquiry`, is
  available but `investigation` matches the headword and keeps the factor
  active rather than merely questioning.
- `citta` keeps `feeling mind` throughout, including as the third base of
  power. This produces `composure through the feeling mind`, which is heavier
  than the other three but consistent. Substituting a bare `mind` for the
  third member only would have made it read as a different kind of item than
  its siblings.
- `padhāna` is governed as `exertion`, so `padhānasaṅkhārā` is rendered
  `exertion conditioners`. This keeps the compound inside the governed
  conditioner family alongside `kāyasaṅkhāra`, `vacīsaṅkhāra`,
  `cittasaṅkhāra`, and `āyusaṅkhāra`, rather than introducing
  `volitional formations` or `efforts of striving`.
- `padhāna` and `sammā-vāyāma` are kept distinct: `exertion` and `effort`
  respectively. Both appear in the formula here -- `vāyamati` is the verb of
  effort, `padahati` the verb of exertion -- so collapsing them would have
  made one clause repeat another.
- The four-clause effort formula is rendered `they generate desire ...; they
  make an effort, arouse energy, take hold of the feeling mind, and exert
  themselves`. `cittaṁ paggaṇhāti` is `take hold of the feeling mind` rather
  than `uplift` or `exert`, keeping `exert` for `padahati`.
- `dhammā` in the effort formula is rendered `qualities`, not `dhammas`. The
  Pali here means wholesome and unwholesome states of mind, and the governed
  `dhamma` headword default would import the teaching-sense into a place the
  text does not use it. This matches the existing `sammā-vāyāma` example
  phrase.
- `pāpakānaṁ akusalānaṁ` is rendered `harmful, unwholesome`, keeping both
  adjectives rather than compressing to `bad`.
- The subject is `they`, carrying the `bhikkhu` named in the opening clause of
  each section. The register standard's warning against the generic `one`
  applies, and the named subject is available a few words earlier.

## Peyyala Handling

The Pali writes the first round in full and abbreviates the other three with
`…pe…`, each at a different point: the second section elides from the first
clause, the third from partway into the first clause, and the fourth after the
first clause is complete.

This edition marks the elisions with `...` at the points the source marks them
rather than silently expanding all four rounds to full length. The alternative
would produce a document four times longer than the discourse, in which the
one thing the text does structurally -- state a formula once and then vary a
single term -- becomes invisible.

The peyyala does affect citation verification, but less than expected. The
workflow plan records that a peyyala-bearing root text downgrades unmatched
phrases to `inconclusive`; it does not downgrade phrases that do match. All
five citations added to the `padhāna` family from this discourse verify `ok`,
because each quotes a phrase from a part the source writes out in full. The
hazard is real for phrases that fall inside an elision, not for the text as a
whole.

## Re-audit Calls

- **`padhānasaṅkhāra` was ungoverned and is the load-bearing compound here.
  Resolved 2026-08-20.** It is named four times, and the whole discourse exists
  to define the bases of power as the combination of a factor, the composure
  gained through it, and these conditioners. A minor entry now records
  `exertion conditioner`, tied to `padhāna` and kept inside the governed
  conditioner family, with `volitional formation` explicitly discouraged so the
  aggregate sense of `saṅkhāra` cannot leak in.
- **`padhāna`, `sammappadhāna`, and `cattāro sammappadhānā` had records but no
  `sutta_references`. Resolved 2026-08-20.** All three now cite this discourse.
  Note the care taken: SN 51.13 states the four-exertion formula in full four
  times but never uses the collective name `sammappadhāna`, so those two
  records quote what the discourse actually says rather than the term it does
  not use. That follows the `anāgāmī` precedent recorded in the workflow plan
  -- quote the sutta, do not move the citation to one that merely contains the
  word.
- `cattaro-sammappadhana.json` had `cattaro-sammappadhana` in its `term` field
  where the standard expects the Pali headword with diacritics. Corrected to
  `cattāro sammappadhānā` in the same pass.
- **`iddhipāda` was not linked to its four factors. Resolved 2026-08-20.** The
  headword now links to `chanda`, `vīriya`, `citta`, `vīmaṁsā`, `samādhi`, and
  `padhānasaṅkhāra`, so the family is visible as a set rather than as four
  unrelated records that happen to appear together.
- `cittassa ekaggatā` is rendered `directness of feeling mind` from the
  `ekaggatā` headword. The full phrase is a stock expression and may deserve a
  formula record; it recurs wherever `samādhi` is defined.
- `paggaṇhāti` is ungoverned. It appears in the effort formula, which recurs
  widely, so it is a candidate alongside `vāyamati` and `padahati`.

## Practice Clarifications

- The four bases of power are not four different techniques. They are four
  things a person can lean on to arrive at the same composure, and the rest of
  the formula is identical in each case.
- The desire in question is desire for a result that has not happened yet:
  that unarisen unwholesome qualities stay unarisen, that arisen ones be
  abandoned, that unarisen wholesome ones arise, and that arisen ones continue
  and fill out. It is not desire for an object.
- `iddhi` is often read as psychic power. This discourse says nothing about
  that. It defines the footing, and the footing is ordinary: something to lean
  on, composure, and sustained exertion.

## Editorial Presentation

- Section headings are editorial and do not correspond to divisions in the
  Pali.
- Prose is hard-wrapped at 79 columns, per the register standard.

## Edition Status

- This is the first stable study edition of the SN 51.13 surface.
- SN 51.13 is the second Wave 7 surface. It was chosen for carrying three
  orphan major entries -- `chanda`, `iddhipāda`, and `vīmaṁsā` -- the highest
  count of any substantive text in the audit, in 242 Pali words.

## Readability Review

- Standard: `plain-english-v1`
- Status: `provisional`
- Review result: each basis of power follows the same audible sequence, so the
  changed support stands out while the exertion refrain stays stable.
- Automated governance review: complete; the full repository verification
  suite passed on 2026-08-22.
- Human read-aloud usability review: pending.
- Newcomer comprehension review: pending.

This surface remains provisional until the human reviews are recorded.

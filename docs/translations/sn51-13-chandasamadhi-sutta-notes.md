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

Note that this makes the surface a poor citation target for
`verify_example_sources.py`, which reports any phrase in a peyyala-bearing
text as `inconclusive`. That limitation is recorded in the workflow plan and
applies to the source text, not to this rendering.

## Re-audit Calls

- **`padhānasaṅkhāra` is ungoverned and is the load-bearing compound here.**
  It is named four times, and the whole discourse exists to define the bases
  of power as the combination of a factor, the composure gained through it,
  and these conditioners. It was rendered to match the conditioner family, but
  that is a local decision a record should confirm. A minor entry tied to
  `padhāna` and the `saṅkhāra` family is the natural next step.
- `cattāro-sammappadhāna`, `sammappadhāna`, and `padhāna` all have records but
  none carries `sutta_references`. This discourse states the four-exertion
  formula in full and is a clean citation for all three.
- `cattaro-sammappadhana.json` has `cattaro-sammappadhana` in its `term`
  field, where the standard expects the Pali headword with diacritics. That is
  a record defect rather than a translation question, but it was noticed here.
- `iddhipāda` has a record but this is the first surface to exercise it. The
  three sibling factors `vīriya`, `citta`, and `vīmaṁsā` are governed
  separately and are not currently linked to `iddhipāda` as a set. The four
  bases are a family and would benefit from being recorded as one.
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

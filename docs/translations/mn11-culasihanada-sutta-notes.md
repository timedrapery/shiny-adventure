# MN 11 Translation Notes

This document is the companion rationale for
[MN 11: Cūḷasīhanāda Sutta](mn11-culasihanada-sutta.md). The main translation
is the primary study surface; this file records debated translation choices,
source-audit calls, and edition notes that govern it.

## Source Base

- Primary source: the Pali text of MN 11 as segmented in SuttaCentral's Bilara
  data (132 segments).
- Control surface: the repository's current term policy, especially `upādāna`
  and its four compounds, `samaṇa`, `paribbājaka`, `papañca`, `pariññā`,
  `pasāda`, `rāga`, `dosa`, `moha`, `taṇhā`, `vijjā`, and `avijjā`, together
  with the fourfold source question established in SN 12.11.
- Working method: the discourse was governed as one argument that starts from a
  claim about who counts as a recluse and ends by grounding that claim in the
  full understanding of taking personally, rather than as a polemic with a
  doctrinal appendix.

## Governing Decisions

- The fourfold source question reuses the wording established in SN 12.11:
  `what is their source? what is their origin? what are they born from? what
  produces them?`, with the answer repeating all four. This is the second
  surface to need it, which settles the question the SN 12.11 notes left open:
  it should become a formula record.
- `pasāda` takes its recorded alternate `confidence` rather than the `clarity`
  default. The passage is about confidence in a teacher and a teaching, and
  `clarity about the Teacher` does not say that.
- `samaṇa` is `recluse` and `paribbājaka` is `wanderer`, both governed, which
  keeps the two groups distinct throughout the exchange.
- `niṭṭhā` is rendered `goal`. Ungoverned. The question the discourse turns on
  is whether there is one goal or many, and `culmination` or `consummation`
  would obscure a plain question.
- `anuruddhappaṭiviruddha` is rendered `favours and opposes`, reusing the
  wording already used in MN 38 and MN 26 for the same pair.
- `paritassati` is rendered `is agitated`. Ungoverned.
- The closing formula reuses the governed `there is no more of this state of
  being`.

## Re-audit Calls

- **The four `upādāna` compounds were not consistent with each other, and this
  is the surface where that showed. Resolved.** The discourse enumerates all
  four in one list, which used to produce:

  > sensual clinging, taking views personally, clinging to rules and
  > observances, and taking self-doctrine personally

  Two members used `taking ... personally`, matching the `upādāna` headword;
  two used `clinging`, which the headword records only as an alternate. That
  was a half-finished family revision rather than a considered split. The
  `diṭṭhupādāna` notes said the project *now* keeps `taking views personally`
  "because it aligns the compound more tightly with the upādāna headword",
  which is the same argument that applies to `kāmupādāna` and
  `sīlabbatupādāna`. The headword's own compound context rule already directed
  all four members to carry its appropriative force, so the two `clinging`
  defaults were out of compliance with a rule the family already recorded.

  The family was harmonised in one pass. The list now reads:

  > taking sensuality personally, taking views personally, taking habits and
  > observances personally, and taking self-doctrine personally

  Each revised compound keeps its `clinging` rendering as a controlled
  continuity alternate rather than losing it, so source-facing prose can still
  use the familiar wording.

  In the same pass the `sīlabbata` stem moved from `rules and observances` to
  `habits and observances` across every record that carries it, so
  `sīlabbatupādāna`, `sīlabbata-parāmāsa`, and the `kāyagantha` knot entry stay
  aligned. That reached MN 2 and MN 64 as well, which carry the fetter
  wording.

- The fourfold source question now has two surfaces (SN 12.11 and this one)
  using identical wording. It should be promoted to a formula record so a third
  surface does not re-solve it. **Resolved 2026-08-21.** The record is
  `kim-nidana-kim-samudaya-kim-jatika-kim-pabhava-formula`. The third surface
  already existed: MN 38 carries the same Pali and had solved it a third way,
  and was brought onto the governed wording in the same pass.
- `niṭṭhā`, `paritassati`, `sīhanāda`, `sahadhammika`, `bhavadiṭṭhi`, and
  `vibhavadiṭṭhi` are ungoverned. The two views in particular carry real weight
  here and in SN 12.15, and are candidates for a paired minor entry.
- The `kāmupādāna` record's example cites `catasso upādānā` from this
  discourse. The text reads `cattārimāni upādānāni`. This was flagged as
  `partial` by `verify_example_sources.py` and is corrected in the same pass as
  this surface.

## Practice Clarifications

- The lion's roar is not a claim that other traditions have nothing. The
  argument that follows grounds it in one specific thing: whether a teaching
  can give a full account of all four kinds of taking personally, including the
  taking of self-doctrine personally. A teaching that stops short of that last
  one is described as leaving its followers' confidence pointed somewhere that
  does not lead out.
- The two views, becoming and non-becoming, are presented as a trap that works
  by opposition: holding either one puts a person in conflict with the other,
  and the way out is not to pick the better one but to see how both arise and
  cease.
- The final passage is the point of the whole discourse. What ends the taking
  personally is not effort against each of the four in turn but the giving up
  of ignorance, after which none of the four is taken up.

## Spoken-Voice Review

- Profile: `osf-spoken-v1-pilot`
- Status: `pilot`
- Sources: `GOV-PLAIN-1`, `DH-CORPUS-1`, `DH-TEACH-1`, `OSF-AV-1`,
  `OSF-AV-6`, `OSF-AV-7`
- Review result: the setting, the other wanderers' possible objections, and
  the two causal answers now move in shorter spoken units; the goal contrasts,
  four kinds of taking personally, and repeated source questions remain
  intact.
- Governed wording left unchanged: the fourfold `source / origin / born from /
  produces` question and the four `taking ... personally` compounds must stay
  synchronized with their controlling records.
- Automated governance review: pending the integration run.
- Alexander H read-aloud review: pending.
- Newcomer comprehension review: pending.

This surface remains a pilot until the human reviews are recorded.

# AN 3.136 Translation Notes

This document is the companion rationale for
[AN 3.136: Uppāda Sutta](an3-136-uppada-sutta.md). The main translation is the
primary study surface; this file records debated translation choices,
source-audit calls, and edition notes that govern it.

## Source Base

- Primary source: the Pali text of AN 3.136 as segmented in SuttaCentral's
  Bilara data (`an3.136:1.1` to `an3.136:1.16`), fetched from the upstream
  Bilara root and matching its hash in `reviews/source-pins.json`.
- Control surfaces: SN 12.20 for the frame (`uppādā vā ... tathāgatānaṁ
  anuppādā vā tathāgatānaṁ, ṭhitāva sā dhātu dhammaṭṭhitatā dhammaniyāmatā`
  and the seven verbs of teaching), and the formula records `aniccā
  sabbasaṅkhārā`, `dukkhā sabbasaṅkhārā`, and `sabbe dhammā anattā` for the
  three lines.
- Working method: the discourse says the same thing three times, once for
  each characteristic. The study edition keeps all three statements whole.
  The repetition is the teaching, not padding.

## Governing Decisions

- `sabbe saṅkhārā aniccā` is `all that has been put together is impermanent`,
  `sabbe saṅkhārā dukkhā` is `all that has been put together is
  unsatisfactory`, and `sabbe dhammā anattā` is `all phenomena are not-self`,
  each from its formula record. `saṅkhārā` takes its result-side reading here:
  things that have been put together, not the activity of putting together.
- `dukkhā` is `unsatisfactory`, the formula record's controlled adjective. The
  repository's headword default for `dukkha` is `dissatisfaction`; the record
  allows the adjective inside this fixed line only.
- `dhammā` is `phenomena`, the formula record's controlled override. The
  headword default leaves `dhamma` untranslated. The shift from `saṅkhārā` in
  the first two lines to `dhammā` in the third is in the Pali and is kept: the
  third line covers more than what has been put together.
- `ṭhitāva sā dhātu dhammaṭṭhitatā dhammaniyāmatā` is `that element still
  stands: the stability of the pattern, the regularity of the pattern`, copied
  from SN 12.20. SN 12.20 adds `idappaccayatā`, `conditionality`; this text
  does not, and the translation does not add it.
- `abhisambujjhati abhisameti` is `awakens to this and breaks through to it`,
  and `ācikkhati deseti paññāpeti paṭṭhapeti vivarati vibhajati uttānīkaroti`
  is `tells it, teaches it, makes it known, sets it out, reveals it, breaks it
  down, and makes it plain`, both copied from SN 12.20.

## Re-audit Calls

- The setting is absent in the source: the discourse opens with
  `bhikkhave`. The translation does not supply one.
- `Catutthaṁ` is rendered `The fourth discourse is finished.` AN 3.136 is the
  fourth discourse of its vagga.

## Practice Clarifications

- The discourse does not say the Buddha made these things true. It says they
  hold whether or not anyone awakens to them, and that a Tathāgata's work is
  to see them and make them plain.
- The three lines are things to see in experience, not beliefs to hold. The
  rest of the corpus gives the method: SN 22.59 for not-self, SN 22.26 for
  seeing the gratification and the danger, MN 122 for watching the heaps rise
  and pass.

## Readability Review

- Standard: `plain-english-v1`
- Status: `provisional`
- Source check: drafted against the pinned segmented Pali; every segment from
  `an3.136:1.1` to `an3.136:1.16` is rendered.
- Automated governance review: complete; the full repository suite passed on
  2026-11-09.
- Human read-aloud usability review: optional, not recorded.
- Newcomer comprehension review: optional, not recorded.

## Wave 12 Role

AN 3.136 is the first Wave 12 queue item. It anchors the three formula lines
with a source the verifier can check, and it gives SN 12.20's frame a second
surface.

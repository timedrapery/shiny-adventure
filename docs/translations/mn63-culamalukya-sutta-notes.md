# MN 63 Translation Notes

This document is the companion rationale for
[MN 63: Cūḷamālukya Sutta](mn63-culamalukya-sutta.md). The main translation is
the primary study surface; this file records debated translation choices,
source-audit calls, and edition notes that govern it.

## Source Base

- Primary source: the Pali text of MN 63 as segmented in SuttaCentral's Bilara
  data.
- Control surface: the repository's current term policy, especially
  `brahmacariya`, `loka`, `tathāgata`, `dukkha`, `jāti`, `jarāmaraṇa`, `soka`,
  `parideva`, `domanassa`, `upāyāsa`, `nibbidā`, `virāga`, `nirodha`,
  `upasama`, `abhiññā`, `sambodha`, and `nibbāna`.
- Working method: the discourse was governed as the repository's control
  surface for the ten undeclared points (`avyākata`), the poisoned-arrow
  simile against demanding metaphysical answers before practicing, and the
  "understand as declared what I have declared" formula that closes the
  discourse.
- Companion surface: MN 64 (Mahāmālukya Sutta) already governs the same
  disciple, Mālukyaputta, in a later-life episode about the five lower
  fetters. This edition reuses MN 64's established spelling `Mālukyaputta`
  (without the anusvāra on the second syllable) and its title convention
  (`Cūḷamālukya` / `Mahāmālukya`) for cross-surface consistency between the
  two discourses addressed to the same person.

## Governing Decisions

- `brahmacariya` is rendered `spiritual life` (existing minor entry). The
  recurring line `brahmacariyaṁ carissāmi` / `na brahmacariyaṁ careyyaṁ` is
  rendered "I will continue to live the spiritual life" / "I will renounce
  the training."
- `loka` is rendered `world` (major lexicon entry). `Sassato loko` / `asassato
  loko` = "the world is eternal" / "the world is not eternal." `Antavā loko` /
  `anantavā loko` = "the world is finite" / "the world is infinite."
- `tathāgata` remains untranslated as `Tathāgata` (major lexicon entry,
  `untranslated_preferred: true`). The four Tathāgata-after-death
  propositions keep the title in place rather than substituting "the Buddha"
  or "the enlightened one," consistent with the entry's doctrinal-weight
  rationale.
- `dukkha` is rendered `dissatisfaction` in the closing four-fold declared
  formula (`idaṁ dukkhan`ti... ), matching the house default for four-truths
  context established in SN 56.11 and reused in MN 141, MN 9, MN 2, MN 39, and
  SN 12.15. This sutta's version of the formula does not use the compound
  `ariyasacca` explicitly, so the translation follows the source and does not
  insert "noble truth" where the Pali does not have it.
- The recurring consequence clause `atthi, mālukyaputta, jāti, atthi
  jarāmaraṇaṁ, atthi soka-parideva-dukkha-domanassupāyāsā, yesāhaṁ
  diṭṭheva dhamme nirodhaṁ paññapemi` is rendered "there is still birth,
  ageing and death, sorrow, lamentation, pain, distress, and despair — and it
  is the ending of these, here and now, that I declare." This reuses the
  exact five-term rendering of `soka-parideva-dukkha-domanassa-upāyāsa`
  ("sorrow, lamentation, pain, distress, and despair") already governed in
  MN 141, MN 9, MN 38, and SN 12.15, and the "birth... ageing and death"
  pairing already governed in MN 38 and SN 12.15.
- The seven-term formula `na etaṁ atthasaṁhitaṁ, na etaṁ ādibrahmacariyakaṁ,
  na nibbidāya na virāgāya na nirodhāya na upasamāya na abhiññāya na
  sambodhāya na nibbānāya saṁvattati` is rendered "it is not beneficial, it is
  not relevant to the fundamentals of the spiritual life, and it does not
  lead to disenchantment, fading, cessation, calming, higher knowing,
  awakening, or nibbāna." The six-term tail (`nibbidā, virāga, nirodha,
  upasama, abhiññā, sambodha, nibbāna` — the same seven-item chain, counting
  `nibbāna` as the seventh) reuses the exact rendering already governed in
  MN 26 ("disenchantment, fading, cessation, calming, higher knowing,
  awakening, or nibbāna"), so this discourse inherits that chain rather than
  re-solving it locally. The positive mirror in the declared-truths section
  swaps only the final connective ("and" for "or") to match the source's
  affirmative framing.
- `Bhagavā` is rendered `Blessed One`, matching the current default used in
  the most recently governed surfaces (MN 22, SN 12.15, AN 3.65) rather than
  "the Buddha," which the earlier MN 64 surface uses for the same speaker and
  the same disciple. See Re-audit Calls below.

## Re-audit Calls

- Resolved: `avyākata` (undeclared / unrecorded) now has a minor entry,
  `terms/minor/avyakata.json`.
- Resolved: the ten undeclared points themselves (`dasa avyākatavatthūni`)
  now have a formula record, `terms/minor/dasa-avyakatavatthuni.json`.
  Note for the roadmap: the source text of MN 63 lists ten propositions (two
  each on the eternity and finitude of the world, two on the identity of soul
  and body, and four on the Tathāgata's status after death), not fourteen.
  [next-suttas-roadmap.md](../next-suttas-roadmap.md) has already been
  corrected to say "ten"; [next-sutta-translation-roadmap.md](../next-sutta-translation-roadmap.md)
  never contained the erroneous count.
- Resolved: `jīva` (soul) and `sarīra` (body, in the specific sense of the
  physical frame paired with `jīva` in this question) now have cross-linked
  minor entries, `terms/minor/jiva.json` and `terms/minor/sarira.json`.
  `Sarīra` is kept distinct from the repository's existing body-language
  around `kāya`.
- Resolved: `salla` (arrow, dart) now has a minor entry,
  `terms/minor/salla.json`, which explicitly keeps this sutta's poisoned-arrow
  image distinct from SN 36.6's two-arrows contrast rather than collapsing
  them into one cross-reference.
- The bow, bowstring, shaft, fletching, and binding-sinew details in the
  poisoned-arrow simile are rendered with generalized, legible modern English
  (e.g., "vulture, heron, hawk, peacock, or some other bird" for the
  feather-fletching list) rather than with maximally precise botanical or
  material terms, several of which do not have a single settled modern
  English equivalent. If a future revision wants maximal source-fidelity on
  this list, that should be a deliberate, separately reviewed editorial
  decision rather than an incidental effect of this pass.
- Resolved: `Bhagavā` in MN 64 has been harmonized to `Blessed One`, matching
  this surface and the current house default. See MN 64's notes, Edition
  Status, for the revision log.

## Editorial Presentation

- The main translation is divided into seven sections: `The Setting`,
  `Mālukyaputta's Reflection`, `Mālukyaputta's Challenge`, `Not Promised, Not
  Agreed`, `The Poisoned Arrow`, `Not Dependent On These Views`, and
  `Undeclared And Declared`.
- The ten-point list appears in full at each of its three occurrences
  (Mālukyaputta's private reflection, his restatement to the Blessed One, and
  the Blessed One's final declared/undeclared summary), consistent with the
  repository's policy of preserving repetition for study readability rather
  than collapsing it to "and so on" outside of the one clearly bracketed
  editorial abridgment in `Mālukyaputta's Challenge` (marked in square
  brackets because the Bilara segmentation itself abbreviates that one
  restatement with `pe`).
- The `Not Dependent On These Views` section groups the ten points into their
  four natural pairs/quadruple (world-eternal, world-finite, soul-body,
  Tathāgata-after-death) rather than writing out ten nearly identical
  paragraphs, since the source itself treats these as one repeating
  structural unit per group. This keeps the section readable while still
  stating every one of the ten views explicitly.

## Edition Status

- This companion supports the first stable study edition of the repository's
  MN 63 translation surface.
- All items flagged in the original Re-audit Calls above were resolved in a
  later lexicon-backlog pass: the `avyākata`, `jīva`, `sarīra`, and `salla`
  minor entries; the ten-undeclared-points formula record; the roadmap
  wording correction; and the `Bhagavā` harmonization against MN 64.

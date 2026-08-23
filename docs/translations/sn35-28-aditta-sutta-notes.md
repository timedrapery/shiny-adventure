# SN 35.28 Translation Notes

This document is the companion rationale for
[SN 35.28: Āditta Sutta](sn35-28-aditta-sutta.md). The main translation is
the primary study surface; this file records debated translation choices,
source-audit calls, and edition notes that govern it.

## Source Base

- Primary source: the Pali text of SN 35.28 as segmented in SuttaCentral's
  Bilara data.
- Control surface: the repository's current term policy, especially `āditta`,
  `rāga`, `dosa`, `moha`, `mano`, `citta`, `vedanā`, `nibbindati`, `virāga`,
  `vimutti`, and `āsava`.
- Working method: the discourse was governed as the repository's control
  surface for the burning-fire formula across all six sense fields, the
  threefold fire of passion, aversion, and delusion, and the
  disenchantment-fading-release arc.

## Governing Decisions

- `āditta` is rendered `burning`. The Pali `āditta` (from `ā + dīpita`,
  blazing, set ablaze) is the structuring metaphor of the entire discourse —
  every element of experience is stated to be `burning`. `Burning` is direct,
  concrete, and preserves the fire imagery that runs through the sutta and
  into its title (Āditta Sutta, the Fire Sermon).
- `mano` is rendered `thinking mind` in its role as the sixth sense base.
  `Mano` names the cognitive, discursive aspect of mind — the organ that
  processes ideas (`dhamma`) as the eye processes sights. It is distinguished
  from `citta` (`feeling mind`), which names the experiential, feeling aspect
  of mind. Both terms appear in SN 35.28: `mano` as the sixth internal sense
  base, `citta` in the final verse describing the bhikkhus' release.
- `dhamma` is rendered `ideas` in its role as the objects of `mano` (the sixth
  sense base). In the sense-field context, `dhamma` names the domain of
  mental objects — thoughts, concepts, mental images — that `mano` processes
  in the same way the eye processes sights. `Ideas` is used as the most
  natural English term for this class of mental objects, without importing the
  doctrinal weight of `dhamma` as Teaching.
- `rāga` is rendered `passion` (house default).
- `dosa` is rendered `aversion` (house default).
- `moha` is rendered `delusion` (house default).
- `vedanā` is rendered `felt experience` (house default).
- `nibbindati` is rendered `grows disenchanted` (house default).
- `virāga` is rendered `fading` (house default).
- `vimutti` is rendered `release` (house default).
- `āsava` is rendered `outflow` (house default).
- `citta` is rendered `feeling mind` in the final verse: `the feeling minds of
  those thousand bhikkhus were released from outflows without clinging`.
- `anupādāya` is rendered `without clinging`. The term names non-appropriation
  — not grasping at anything as the basis for continued becoming.
- The burning formula adds `jātiyā jarāmaraṇena sokaparidevadukkhadomanassupāyāsehi`
  — rendered `burning with birth, ageing, death, sorrow, lamentation, pain,
  distress, and despair`. These eight terms round out the full weight of
  suffering implied by the fires of passion, aversion, and delusion.

## Existing Control Records Reused

All governing terms for SN 35.28 are already covered by existing lexicon
records:

- `rāga` → `passion` (major)
- `dosa` → `aversion` (major)
- `moha` → `delusion` (major)
- `vedanā` → `felt experience` (major)
- `nibbidā` / `nibbindati` → `disenchantment` / `grows disenchanted` (major)
- `virāga` → `fading` (major)
- `vimutti` → `release` (major)
- `āsava` → `outflow` (major)
- `citta` → `feeling mind` (major)

## Re-audit Calls

- Resolved: `āditta` now has a minor entry, `terms/minor/aditta.json`. It
  remains an adjective used as the sutta's structuring metaphor rather than a
  heavier doctrinal term. `Burning` is used throughout without further
  qualification, which is the correct approach: the fire metaphor is
  self-evident and needs no gloss.
- `mano` as `thinking mind` (sixth sense base) versus `citta` as `feeling
  mind` (experiential mind) is a distinction the translation preserves
  consistently. The two terms appear in different syntactic roles within the
  same discourse: `mano` in the burning formula (`the thinking mind is
  burning`), `citta` in the release formula (`the feeling minds of those
  thousand bhikkhus`). Keeping the distinction prevents flattening a
  meaningful Pali contrast.
- The sense-contact objects are rendered with natural English sensory nouns
  rather than technical Pali-derived terms: `rūpa` → `sights` (not `form`,
  which would invoke the heap sense), `sadda` → `sounds`, `gandha` → `smells`,
  `rasa` → `tastes`, `phoṭṭhabba` → `touches`, `dhamma` → `ideas`. These
  are the six doors' objects in their phenomenological sense.
- The abbreviated disenchantment section (after the full burning formula)
  contracts the repetition into grouped statements rather than expanding each
  sense field identically. This mirrors the Pali's own condensation pattern
  in this passage: the full per-field formula is given for the eye in the
  disenchantment section, then the remaining five fields are stated in
  compressed form. The main translation follows this structure.
- `Chaṭṭhaṁ.` is rendered `The sixth discourse is finished.` This matches the
  discourse-closing formula used in other surfaces in this repository.

## Editorial Presentation

- The main translation is divided into two sections: `All Is Burning` and
  `Disenchantment and Release`.
- The burning formula for each of the six sense fields repeats the full
  structure: sense base is burning → its object is burning → its knowing is
  burning → its contact is burning → whatever felt experience arises from
  that contact is burning. The repetition is preserved in full for the first
  section, consistent with the repository's policy of preserving the Pali
  repetition structure for study readability.
- The disenchantment section uses the Pali's own abbreviated structure: the
  eye field is given in full, then the remaining five are stated compactly.

## Edition Status

- This companion supports the first stable study edition of the repo's
  SN 35.28 translation surface.
- The `āditta` minor entry was added in a later lexicon-backlog pass; see
  Re-audit Calls above. Future revisions should focus on `mano` / `citta` if
  the feeling-mind / thinking-mind distinction develops a more fully governed
  policy across the six-sense-field family.

## Spoken-Voice Review

- Profile: `osf-spoken-v1-pilot`
- Status: `pilot`
- Sources: `GOV-PLAIN-1`, `DH-CORPUS-1`, `DH-TEACH-1`, `OSF-AV-1`,
  `OSF-AV-6`, `OSF-AV-7`
- Review result: the repeated `is burning` unit stays short and forceful while
  the changed sense field remains obvious; the release sequence and governed
  sense vocabulary are preserved.
- Automated governance review: pending the integration run.
- Alexander H read-aloud review: pending.
- Newcomer comprehension review: pending.

This surface remains a pilot until the human reviews are recorded.

# MN 39 Translation Notes

This document is the companion rationale for
[MN 39: Mahā-Assapura Sutta](mn39-maha-assapura-sutta.md). The main
translation is the primary study surface; this file records debated
translation choices, source-audit calls, and edition notes that govern it.

## Source Base

- Primary source: the Pali text of MN 39 as segmented in SuttaCentral's
  Bilara data.
- Control surface: the repository's current term policy, especially `hiri-
  ottappa`, `indriya`, `nivarana`, `sati`, `sampajanna`, `jhana`, `jhayati`,
  `piti`, `upekkha`, `asava`, `citta`, `vedana`, `panna`, and `samadhi`.
- Working method: the discourse was governed as the next strategic surface
  per `docs/next-sutta-translation-roadmap.md`, extending the jhāna
  progression and distraction-clearing surfaces from DN 2 and SN 46.51 into
  a full ascending-practice arc with the five similes and three higher
  knowledges.

## Governing Decisions

- `hirī-ottappa` is rendered `conscience and concern`. The house record for
  `hiri-ottappa` (minor, reviewed) gives this as the default pair.
- `sati` is rendered `remembering` and `sampajañña` is rendered `clear
  knowing` throughout. The formula `satisampajaññena samannāgatā` is rendered
  `possessed of remembering and clear knowing`. In the wakefulness section,
  `sato sampajāno` is rendered `with remembering and clear knowing`.
- `indriya` is rendered `faculty`. The phrase `indriyesu guttadvārā` (guarded
  at the faculty doors) is rendered `guarded at the faculty doors`, with the
  individual faculty restraint instructions using `eye-faculty`, `ear-faculty`,
  and so on.
- The five `nīvaraṇa` members follow their governed distraction-family
  renderings: `sensual distraction`, `aversive distraction`, `dull
  distraction`, `agitated distraction`, and `uncertain distraction`. In the
  hindrance-clearing sequence (section 13), the abandonment formula names
  each individually rather than using collective `nīvaraṇa` language; this
  keeps the clearing action concrete.
- `jhāna` is rendered `mental theme` (major, reviewed). The four formulas are
  rendered `first mental theme` through `fourth mental theme`.
- `pīti` is rendered `rejoicing` (major, updated house default). In the jhāna
  formulas: `vivekajaṁ pītisukhena` is rendered `rejoicing and satisfaction
  born of seclusion`; `samādhijaṁ pītisukhena` is rendered `rejoicing and
  satisfaction born of composure`; `nippītikena sukhena` is rendered
  `satisfaction free of rejoicing`. `Sukha` is rendered `satisfaction`
  following the preferred house default; the earlier rendering `happiness` was
  the discouraged form and has been corrected throughout this surface.
- `upekkhā` in the third and fourth mental themes is rendered `dynamic
  balance` (major, house default). `Upekkhāsatipārisuddhiṁ` in the fourth
  mental theme is rendered `pure dynamic balance and remembering`.
- `citta` is rendered `heart` throughout. In the body-permeation
  formulas for the fourth mental theme, `parisuddhena cetasā pariyodātena`
  is rendered `pure, bright heart`.
- `āsava` is rendered `outflow` (major). The three outflows — `kāmāsava`,
  `bhavāsava`, `avijjāsava` — are rendered `outflow of sensual desire`,
  `outflow of becoming`, and `outflow of ignorance`.
- `dukkha` in the Four Truths passage is rendered `dissatisfaction`, following
  the house default.

## Existing Control Records Reused

MN 39 does not need new live phrase records. The governing terms already have
sufficient lexicon coverage:

- `hirī-ottappa` → `conscience and concern` (minor, reviewed)
- `indriya` → `faculty` (major)
- `nīvaraṇa` members → governed distraction-family renderings (major)
- `sati` → `remembering` (major)
- `sampajañña` → `clear knowing` (major)
- `jhāna` → `mental theme` (major, reviewed)
- `pīti` → `rejoicing` (major)
- `upekkhā` → `dynamic balance` (major)
- `āsava` → `outflow` (major)
- `citta` → `heart` (major)
- `paññā` → `discernment` (major)
- `samādhi` → `composure` (major)
- `vedanā` → `felt experience` (major) — in the eating section

## Re-audit Calls

- Resolved: `samaṇa` is now a major lexicon entry, `terms/major/samana.json`
  (promoted from a thinner minor entry that had recorded an unused
  "contemplative" default; the major entry corrects this to `recluse`,
  matching actual usage). `Recluse` is the clearest modern English that
  preserves the withdrawn, quieted sense without importing asceticism or
  harshness, and MN 39 makes it the central term of address, closing with its
  folk etymology (`samita` = calmed). It is used consistently across all
  seven-title instances.
- `brāhmaṇo` is rendered `brahmin` as a title alongside `recluse` throughout,
  with `brahmin` as the established English form.
- The seven closing epithets (`samaṇa`, `brāhmaṇa`, `nhātaka`, `vedagū`,
  `sottiyo`, `ariya`, `arahaṁ`) are rendered `recluse`, `brahmin`, `bathed
  one`, `knowledge-master`, `one cleansed`, `noble one`, and `perfected one`.
  The folk etymologies in sections 23–29 are translated to show the wordplay:
  `samita` (calmed) for `samaṇa`; `bāhita` (expelled) for `brāhmaṇa`;
  `nhāta` (bathed away) for `nhātaka`; `vidita` (fully known) for `vedagū`;
  `nissuta` (scoured off) for `sottiyo`; `ārakā` (far away) for `ariya`;
  and `ārakā` again (impeccably far away) for `arahaṁ`.
- `kāyasamācāra / vacīsamācāra / manosamācāra` are rendered `bodily conduct`,
  `verbal conduct`, and `mental conduct`. `Ācāra` (conduct, behavior) is
  straightforward; `samā` prefix is absorbed into the simplicity of `pure
  conduct`.
- `nimittaggāhī nānubyañjanaggāhī` is rendered `will not grasp at the overall
  sign or at its details`. `Nimitta` (the overall feature or sign of the
  object) and `anuvyañjana` (secondary details) are kept visible as two
  distinct grasping tendencies.
- `bhojane mattaññū` is rendered `knowing measure in eating`. `Mattaññū`
  (one who knows the measure/amount) is rendered as `knowing measure`, a
  plain functional description.
- `abhijjhādomanassa` is rendered `covetousness and displeasure`. `Abhijjhā`
  (covetousness, wanting what belongs to the world) and `domanassa`
  (displeasure) name the two bad qualities that flood in through unguarded
  faculties.
- Resolved: `abhisandeti parisandeti paripūreti parippharati` now has a
  formula record,
  `terms/minor/abhisandeti-parisandeti-paripureti-parippharati.json`. It is
  rendered `drenches, saturates, fills, and spreads`, describing the
  permeation of the body by the quality generated in each mental theme. The
  progression from drench to saturate to fill to spread shows thorough
  permeation without overflow.
- `āneñjappatta` in the three-higher-knowledge opener is rendered
  `imperturbable`. The compound means "having reached non-movement" —
  `imperturbable` keeps this literal without importing later doctrinal
  language.
- `brahmacariya` in the liberation formula is rendered `spiritual life`.
  `Brahmacariya` (the holy life, the practice of the path) is rendered as
  `spiritual life` in the familiar liberation formula: `khīṇā jāti, vusitaṁ
  brahmacariyaṁ, kataṁ karaṇīyaṁ, nāparaṁ itthattāyā`ti`.
- The `…pe…` abbreviation marks in the Bilara for sense-faculty members
  2–5 and the middle three Truths passages are expanded in full throughout
  the translation, consistent with the repository's policy of preserving
  repetition for study readability.
- The five similes (debt, illness, prison, slavery, desert) are written out
  fully for each case. The Pali gives each simile in full before drawing the
  comparison; the translation preserves this structure rather than summarizing.

## Editorial Presentation

- The main translation is divided into seven sections: `The Setting`, `What
  Makes a True Recluse`, `Settling Into Seclusion`, `Abandoning the Five
  Distractions`, `Five Similes for the Distractions`, `The Four Mental
  Themes`, `Three Higher Knowledges`, and `Seven Titles Explained`.
- The "still more to do" refrain (`'mā vo sāmaññatthikānaṁ sataṁ sāmaññattho
  parihāyi, sati uttariṁ karaṇīye'`) is rendered consistently as: `I declare
  to you, bhikkhus, I announce to you: 'You who seek the recluse's goal — do
  not let the recluse's goal decline while there is still more to do.'` In
  the middle steps, this is abbreviated to `I declare to you: do not let the
  recluse's goal decline while there is still more to do.` — following the
  pattern set in the Pali's own abbreviation of the middle iterations.
- Repetition is preserved throughout: body-permeation formulas, simile
  structure, three-higher-knowledge opener, and seven-title closing are all
  written out in full.

## Edition Status

- This companion supports the first stable study edition of the repo's MN 39
  translation surface.
- The `samaṇa` major-entry promotion and the body-permeation verb cluster
  formula record were added in a later lexicon-backlog pass; see Re-audit
  Calls above. Future revisions should focus on the `brahmacariya` rendering
  if the house develops a narrower policy for the liberation formula.

## Readability Review

- Standard: `plain-english-v1`
- Status: `provisional`
- Review: made the opening definition and uncertainty passage easier to hear;
  preserved the ascending `still more to do` refrain, five similes,
  body-permeation formulas, higher knowledges, and seven-title wordplay.
- Automated governance review: complete; the full repository verification
  suite passed on 2026-08-22.
- Human read-aloud usability review: pending.
- Newcomer comprehension review: pending.
- Governed wording retained: `knowing measure in eating` and the seven title
  epithets remain unchanged because the notes govern their functional and
  wordplay renderings.

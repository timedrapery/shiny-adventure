# SN 12.15 Translation Notes

This document is the companion rationale for
[SN 12.15: Kaccānagotta Sutta](sn12-15-kaccanagotta-sutta.md). The main
translation is the primary study surface; this file records debated translation
choices, source-audit calls, and edition notes that govern it.

## Source Base

- Primary source: the Pali text of SN 12.15 as segmented in SuttaCentral's
  Bilara data.
- Control surface: the repository's current term policy, especially `diṭṭhi`,
  `upādāna`, `anusaya`, `avijjā`, `saṅkhārā`, `viññāṇa`, `vedanā`, `taṇhā`,
  `paññā`, and the standard dependent-arising chain.
- Working method: the discourse was governed as the repository's control
  surface for the middle-way definition of right view. The sutta is the
  shortest high-leverage text in the current queue — one page, but foundational
  for every surface that touches the two extremes of eternalism and
  annihilationism.

## Governing Decisions

- `atthitā` is rendered `the view of existence` and `natthitā` is rendered
  `the view of non-existence`. These are abstract nouns formed from the verbs
  `atthi` (exists) and `natthi` (does not exist). They name the two
  metaphysical poles the world is caught between: the view that things simply
  exist (eternalism, `sassatavāda`) and the view that things simply do not
  exist (annihilationism, `ucchedavāda`). The rendering "view of existence /
  view of non-existence" preserves the abstract noun form and makes clear that
  these are epistemological positions, not bare descriptions of reality.
- `lokasamudaya` is rendered `arising of the world` and `lokanirodha` is
  rendered `cessation of the world`. These terms use `loka` (world) in the
  sense of the world of experience — the dependent-arising process of
  suffering — not a cosmological claim. Seeing the arising of the world means
  seeing how suffering originates; seeing its cessation means seeing how it
  ends. The seeing (with right discernment) dissolves the metaphysical poles:
  if you see things arising dependently, you cannot hold "nothing exists";
  if you see things ceasing dependently, you cannot hold "everything exists
  permanently."
- `upayupādānābhinivesavinibandha` (mn22:15:2.4) is rendered "bound by
  approach, taking personally, and insistence." The compound parses as:
  `upaya` (going toward, approach) + `upādāna` (taking personally) +
  `abhinivesa` (insisting, leaning in hard) + `vinibandha` (bond, binding).
  These are three progressive layers of attachment: the initial movement
  toward experience, the grasping of it as personal, and the refusal to
  release it. Together they name the mechanism by which the world becomes
  entangling.
- `cetaso adhiṭṭhāna` is rendered `fixation of the feeling mind`. `Adhiṭṭhāna`
  = standing upon, firm resolve, fixation. In the context of sn12.15:2.5, it
  names the mental act of planting the feeling mind on something as a fixed
  point — the psychological gesture that solidifies approach and grasping into
  a standing commitment.
- `abhinivesa` is rendered `insistence` (no lexicon entry; local rendering).
  `Abhinivesa` = leaning into, insisting on, the strong grasping at a position.
  Distinct from `upādāna` (taking personally) in that `abhinivesa` is the
  holding-hard gesture that follows grasping.
- `aparapaccayā ñāṇamevassa ettha hoti` is rendered "their knowledge of this
  is independent of others." `Apara` = other, `paccayā` = dependent upon,
  `ñāṇa` = knowledge. The phrase names the mark of genuine direct insight:
  the knowing does not depend on the testimony of others — it is firsthand.
  This is distinct from mere learning or inference.
- `sammādiṭṭhi` is rendered `right view` throughout (no lexicon entry; natural
  English rendering). The sutta opens with Kaccānagotta's question about the
  scope of right view (`kittāvatā sammādiṭṭhi hoti`), and the entire discourse
  is the answer. Future surfaces should use the same rendering.
- `kittāvatā` in the opening question is rendered "how far does right view
  extend?" (`kittāvatā` = how much, to what extent). This preserves the
  sense of scope — Kaccānagotta is asking not just for a definition but for the
  full reach of what right view covers.
- The two-extremes formula: `'Sabbamatthī'ti kho, kaccāna, ayameko anto.
  'Sabbaṁ natthī'ti ayaṁ dutiyo anto.` = "'All exists' — this is one extreme.
  'All does not exist' — this is the second extreme." The Tathāgata teaches by
  the middle, without approaching either extreme. This formula is the
  foundational statement of the middle way as an epistemological position —
  prior to any specific ethical or meditative teaching.

## Existing Control Records Reused

- `avijjā` → `ignorance` (major)
- `saṅkhārā` → `putting things together` (major)
- `viññāṇa` → `knowing` (major)
- `nāmarūpa` → `name-and-form` (major)
- `saḷāyatana` → `six sense fields` (major)
- `phassa` → `contact` (major)
- `vedanā` → `felt experience` (major)
- `taṇhā` → `ignorant wanting` (major)
- `upādāna` → `taking personally` (major)
- `bhava` → `becoming` (major)
- `jāti` → `birth` (major)
- `paññā` → `discernment` (major)
- `anusaya` → `underlying tendency` (major)

## Re-audit Calls

- Resolved: `atthitā` and `natthitā` now have paired minor entries,
  `terms/minor/atthita.json` and `terms/minor/natthita.json`.
- Resolved: `abhinivesa` now has a minor entry,
  `terms/minor/abhinivesa.json`, distinguishing it from `upādāna` and
  `anusaya` as planned.
- `sammādiṭṭhi` still has no standalone lexicon entry, and this remains a
  deliberate deferral rather than an oversight: `terms/major/ditthi.json`
  already governs the compound via `compound_inheritance: inherit`, and this
  sutta's "right view" rendering already follows from that. A standalone
  entry is still appropriate when the path-factor cluster adds the
  natural English equivalent and is used consistently across the repository.
  A minor entry would be appropriate when the path-factor cluster adds the
  eight-factor path as individual entries.
- The DA chain in sn12.15:3.4-3.9 is abbreviated in the Bilara with `…pe…`
  for the middle links of both the arising and cessation chains. Both chains
  are expanded in full in the translation, consistent with the repository's
  policy of preserving repetition for study readability.

## Editorial Presentation

- The main translation is divided into three sections: `The Setting`, `Right
  View`, and `The Two Extremes and the Middle`.
- The teaching falls into two halves: (1) the positive definition of right
  view as the seeing that dissolves both the view of existence and the view
  of non-existence — by releasing the "my self" fixation; and (2) the
  positive content of the middle: dependent arising, stated in full in both
  the arising and cessation directions.
- The closing `Pañcamaṁ` = "the fifth" — SN 12.15 is the fifth sutta in the
  Āhāravagga (SN 12.11–12.20). "The fifth discourse is finished."

## Edition Status

- This companion supports the first stable study edition of the repo's
  SN 12.15 translation surface.
- The `atthitā` / `natthitā` and `abhinivesa` minor entries were added in a
  later lexicon-backlog pass; see Re-audit Calls above. `sammādiṭṭhi` remains
  intentionally deferred.
- This sutta should be cited as the governing authority for the two-extremes
  / middle formulation in any future surface that touches eternalism or
  annihilationism.

## Readability Review

- Standard: `plain-english-v1`
- Status: `provisional`
- Review result: Kaccānagotta's question and the two-extremes contrast remain
  the audible spine; the middle-way and dependent-arising control language is
  preserved rather than paraphrased away.
- Automated governance review: complete; the full repository verification
  suite passed on 2026-08-22.
- Human read-aloud usability review: pending.
- Newcomer comprehension review: pending.

This surface remains provisional until the human reviews are recorded.

# Next Suttas Roadmap

## Purpose

This roadmap ranks the next untranslated suttas that would strengthen the live
lexicon most efficiently.

The point is not to choose the most famous discourses in the abstract. The
point is to choose texts that:

- reuse already-governed doctrinal clusters
- sharpen near-neighbor distinctions that still carry drift risk
- stabilize repeated formulas that should not be re-solved locally
- expose the next useful headword, compound, or formula refinements

## Audit Basis

This ranking reflects the repository at 36 translation surfaces. All fifteen
entries in the original ranked roadmap are complete, along with eleven
additional surfaces (AN 4.113, AN 11.9, SN 12.23, SN 35.28, MN 38, MN 26,
MN 22, SN 12.15, AN 3.65, MN 63, and the pre-existing surfaces). Wave 5 is now
complete. The next gains come from doctrinal families that are now
well-governed in the lexicon but thin in outward-facing translation
documents.

Wave 6 was audited on 2026-08-19 against this same 36-surface state. Its
ranking applies the four factors below but corrects for a flaw they have on
their own — see the method note under Ranked Roadmap (Wave 6).

The ranking weights four factors:

1. live `sutta_references` density across the current lexicon
2. direct pressure on policy-bearing major entries
3. formula and sequence density that can stabilize translator-facing control
   language
4. ability to reduce future drift across clusters already under governance

## Ranked Roadmap (Wave 6)

Audited 2026-08-19 against the 36-surface, 1145-term state.

### Method Note: Raw Citation Count Is Not Leverage

The four factors above rank `DN 22` first on raw citation weight, at fifteen
citing entries. That ranking is wrong, and the reason matters for every future
audit.

`DN 22` is the expanded Mahāsatipaṭṭhāna, and `MN 10` already has a surface.
Of the fifteen entries citing `DN 22`, twelve are already anchored by `MN 10`,
so translating it would re-govern vocabulary that running text already
demonstrates. Its genuinely new contribution is three major entries.

The sharper measure is how many citing entries are **orphans**: records whose
sutta anchors are *all* untranslated, so no existing surface shows their policy
in running text. Across the lexicon there are 189 such orphan entries. A
further 543 entries carry no sutta citation at all, which is expected for many
minor compounds but is worth watching as a separate coverage question.

Wave 6 therefore ranks by ungoverned major families rather than by citation
volume.

### 1. SN 12.11: Āhāra Sutta

- Leverage signal: six orphan entries, all major -- `ahara`, `cetana`,
  `kabalinkara-ahara`, `manosancetana-ahara`, `phassa-ahara`, and
  `vinnana-ahara`. No other candidate anchors this many major entries that
  currently have no surface at all.
- Beware the name collision: `SN 46.51` is also titled Āhāra Sutta and is
  already translated, but it is a different text about what feeds the
  distractions and awakening factors. More importantly, that surface
  deliberately overrides `ahara` into a local feeding-and-starving idiom
  rather than the headword default `nutriment`. The result is that the
  `ahara` headword's own default rendering has no translation surface
  demonstrating it anywhere in the repository.
- Strengthens: the four-nutriments family as a governed set, and the
  nutriment-to-craving link that sits directly beside dependent arising.
- Likely lexicon pressure: confirm whether `nutriment` survives as the
  headword default once it governs a text where the four nutriments are the
  subject rather than a simile; and record the relationship between the
  headword default and the `SN 46.51` local override explicitly.
- Status: translated. See [SN 12.11](translations/sn12-11-ahara-sutta.md) and
  its [translation notes](translations/sn12-11-ahara-sutta-notes.md).
  `nutriment` did survive as the headword default. The notes flag that
  `dukkhakkhandha` is ungoverned and rendered inconsistently between SN 12.2
  and SN 12.15, and that the fourfold source question is a candidate for a
  formula record.

### 2. SN 55.5

- Leverage signal: five orphan major entries -- `sotapanna`, `sakadagami`,
  `anagami`, `sotapatti`, and `phala`. The entire attainment ladder is
  governed in the lexicon but appears in no translation surface.
- Strengthens: path-fruit vocabulary and the factors of stream-entry, which
  are cited across the path-factor and liberation clusters without any running
  text to anchor them.
- Likely lexicon pressure: fix the boundary between `phala` as fruit of the
  path and `phala` in ordinary result-language; and settle whether the four
  attainment terms stay in Pali or take English renderings, since they are
  currently governed as a family but never exercised.

### 3. AN 6.63: Nibbedhika Sutta

- Leverage signal: `kamma` is a major policy-bearing headword whose only
  citation anchor is this untranslated text. For an early-Buddhist lexicon,
  `kamma` having no translation surface is the single most conspicuous gap the
  audit found.
- Strengthens: the intention-and-action family -- `kamma`, `cetana`, `papa`,
  and `phala` -- including the definition that identifies intention as what is
  meant by kamma.
- Likely lexicon pressure: keep `kamma` from drifting into generic
  consequence-language; and confirm how `cetana` reads when it is defining
  kamma rather than sitting in the dependent-arising chain.

### 4. SN 12.61

- Leverage signal: the highest formula density in the queue. Four formula
  records -- `imasmim-sati-idam-hoti`, `imasmim-asati-idam-na-hoti`,
  `imassuppada-idam-uppajjati`, and `imassa-nirodha-idam-nirujjhati` -- plus
  the `idappaccayata` and `paccaya` majors.
- Strengthens: the general conditionality formula that underlies every
  dependent-arising surface already in the repository. This is reusable
  control language rather than a single text's vocabulary.
- Likely lexicon pressure: stabilize the four-line formula as one governed
  block so it is not re-solved locally in each surface that quotes it.

### 5. MN 11: Cūḷasīhanāda Sutta

- Leverage signal: the highest major-entry pressure among texts whose entries
  are not orphans -- six majors, including all four `upadana` types
  (`kamupadana`, `ditthupadana`, `silabbatupadana`, `attavadupadana`) plus
  `atta` and `ditthi`.
- Strengthens: the appropriation family at the point where it is enumerated
  rather than assumed, which is the weakest link in the dependent-arising
  chain as currently surfaced.
- Likely lexicon pressure: confirm the four-fold `upadana` enumeration as a
  formula record.

### Also Considered

- `SN 22.105` -- short, and anchors the `sakkaya` pair whose
  `translation_policy` was written on 2026-08-19. Good per-word return if a
  quick surface is wanted.
- `SN 51.13` -- the `iddhipada` family, four orphan entries.
- `SN 45.174` -- the `gantha` knots family, seven orphan entries but only one
  major.
- `MN 77` -- ten orphan entries, but all are `kasina` minors with narrow
  doctrinal reach. High count, low leverage; a good example of why raw orphan
  count is also not sufficient on its own.

## Suggested Order (Wave 6)

1. `SN 12.11` -- most ungoverned major entries, and closes the `ahara`
   headword-default gap
2. `SN 55.5` -- the entire attainment ladder, currently unexercised
3. `AN 6.63` -- gives `kamma` a translation surface
4. `SN 12.61` -- reusable conditionality control language
5. `MN 11` -- the four-fold appropriation enumeration

## Ranked Roadmap (Wave 5)

### 1. MN 22: Alagaddūpama Sutta

- Leverage signal: the raft simile (`kullūpama dhamma`) was referenced in
  MN 38 without a source surface — MN 22 is that source.
- Strengthens: the not-self and not-grasping-the-teaching families; the "not
  mine, not I, not my self" refrain; the `anattā` formula across the five
  heaps; and the snake / grass simile for wrong grasp of the teaching.
- Likely lexicon pressure: govern the "not mine, not I, not my self" refrain
  as a formula record; confirm the `n'etaṁ mama` / `n'esohamasmi` /
  `na m'eso attā` triple; and keep the not-grasping-the-teaching prose from
  drifting into generic freedom language.

### 2. SN 12.15: Kaccānagotta Sutta

- Leverage signal: extremely high per-length leverage — one page, directly
  defines right view as the middle between eternalism and annihilationism.
- Strengthens: the `diṭṭhi` family (eternalism / annihilationism), the
  `sammādiṭṭhi` record, and the DA-as-middle-way teaching that anchors MN 38,
  SN 12.2, and MN 9.
- Likely lexicon pressure: govern `sassatavāda` (eternalism) and `ucchedavāda`
  (annihilationism) as a paired minor entry; confirm how the repo renders the
  `atthitā / natthitā` (existence / non-existence) poles in the middle-way
  formula.

### 3. AN 3.65: Kālāma Sutta

- Leverage signal: the most broadly referenced AN sutta not yet covered; the
  AN cluster has only three surfaces (AN 4.113, AN 10.60, AN 11.9).
- Strengthens: the epistemological foundation — confidence grounded in direct
  experience rather than tradition, report, or reasoning alone; connects to
  MN 38's "known, seen, realized for yourselves" passage and MN 26's "not
  speaking out of reverence for the teacher" passage.
- Likely lexicon pressure: govern the ten-criterion list (don't rely on oral
  tradition, lineage, hearsay, scripture, reasoning, inference, analogy,
  agreement with one's views, the seeming competence of the speaker, or
  reverence for the teacher); keep the empirical-confidence family distinct
  from both pure faith language and pure rationalist language.

### 4. MN 63: Cūḷamālukya Sutta

- Leverage signal: the poisoned arrow simile; the undeclared-questions
  (`avyākata`) family; connects directly to MN 38's not-running-to-past/future
  passage and MN 26's conditional-knowing teaching.
- Strengthens: the undeclared (`avyākata`) doctrinal family; the "poisoned
  arrow" simile for not letting metaphysical speculation block practice; the
  boundary between what the teaching covers and what it leaves aside.
- Likely lexicon pressure: govern `avyākata` (undeclared / unrecorded) as a
  minor entry; confirm the ten undeclared points (`dasa avyākatavatthūni`)
  as a formula record; and keep the simile from being read as
  anti-intellectual rather than practice-orienting.
- Status: translated. See
  [MN 63](translations/mn63-culamalukya-sutta.md) and its
  [translation notes](translations/mn63-culamalukya-sutta-notes.md). The
  notes flag that the source text lists ten propositions, not fourteen, and
  that `avyākata`, `jīva`, and `sarīra` still need formal minor entries.

### 5. SN 12.15: Kaccānagotta Sutta

(Already ranked at 2 — included here for completeness in the sequencing
notes below.)

## Suggested Translation Order

### Wave 5: Source-Closing and Gap-Filling (complete)

1. `MN 22` Alagaddūpama — closes the raft-simile source gap, governs the
   not-self refrain as a formula record
2. `SN 12.15` Kaccānagotta — highest per-length doctrinal leverage in the
   remaining queue
3. `AN 3.65` Kālāma — expands the AN cluster, governs empirical-confidence
   epistemology
4. `MN 63` Cūḷamālukya — governs the undeclared family and the poisoned
   arrow simile

All four surfaces are now translated; see
[next-sutta-translation-roadmap.md](next-sutta-translation-roadmap.md) for the
completed-surfaces list and the next wave.

## Why This Order

- `MN 22` lands first because the raft simile was referenced in MN 38 without
  a source surface. The sutta also carries the most reusable not-self formula
  in the corpus — the threefold "not mine, not I, not my self" refrain across
  all five heaps — which is cited but not yet governed in an outward-facing
  translation document.
- `SN 12.15` lands second because it is the shortest high-leverage text in the
  remaining queue. One page, but it directly defines the middle-way framing
  that underlies MN 38, MN 9, and SN 12.2. No other text gives this much
  return per word.
- `AN 3.65` lands third because the AN cluster is thin relative to the MN and
  SN clusters, and this sutta is the most broadly referenced AN text in the
  broader tradition.
- `MN 63` lands fourth because the undeclared-questions family is currently
  ungoverned and is beginning to appear as an implicit background in multiple
  surfaces.

## What To Update In The Lexicon After Each Sutta

After each translation pass:

1. review the governing major entries, compounds, and formula records together
2. update headword notes only when the sutta exposes a reusable family-level
   boundary
3. add formula records when a stock line is likely to recur across multiple
   translation surfaces
4. refresh any linked brief, map, or generated cluster sheet that now has a
   stronger control passage
5. regenerate translation indexes and rerun the full verification suite

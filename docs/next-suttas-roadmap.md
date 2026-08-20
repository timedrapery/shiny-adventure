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

This ranking was made when the repository had 36 translation surfaces; it now has 41, and the historical figure is kept because the ranking below was computed against that state. All fifteen
entries in the original ranked roadmap are complete, along with eleven
additional surfaces (AN 4.113, AN 11.9, SN 12.23, SN 35.28, MN 38, MN 26,
MN 22, SN 12.15, AN 3.65, MN 63, and the pre-existing surfaces). Wave 5 is now
complete. The next gains come from doctrinal families that are now
well-governed in the lexicon but thin in outward-facing translation
documents.

Wave 6 was audited on 2026-08-19 against this same 36-surface state. Its
ranking applies the four factors below but corrects for a flaw they have on
their own — see the method note under Ranked Roadmap (Wave 6).

Wave 7 was audited on 2026-08-20 against the current 42-surface, 1147-term
state, and is the first audit that is reproducible rather than hand-computed:
run `python scripts/audit_surface_leverage.py`. It carries two further
corrections to the method, both recorded under Ranked Roadmap (Wave 7).

The ranking weights four factors:

1. live `sutta_references` density across the current lexicon
2. direct pressure on policy-bearing major entries
3. formula and sequence density that can stabilize translator-facing control
   language
4. ability to reduce future drift across clusters already under governance

## Ranked Roadmap (Wave 7)

Audited 2026-08-20 against the 42-surface, 1147-term state.

This audit is reproducible. Run it rather than recomputing by hand:

```bash
python scripts/audit_surface_leverage.py
```

Current state: 614 of 1147 records are cited, 429 anchored, **185 orphaned**,
533 uncited. Wave 6 recorded 189 orphans against 1145 terms, so three waves of
translation have barely moved the orphan count. That is expected -- those waves
added surfaces for vocabulary that was largely already anchored -- but it means
orphan reduction has not been what the waves were buying.

### Method Note: Orphan Count Is Not Leverage Either

Wave 6 established that raw citation count is not leverage. That still holds:
`DN 22` again tops raw citations at fifteen citing entries while contributing
only three orphan majors, for the same reason as before.

The orphan measure has now developed the same disease one level over. Ranked
mechanically by orphan count, the top of the field is:

| Sutta | Orphan entries | Pali words |
| --- | --- | --- |
| `SN 45.174` | 7 | 34 |
| `SN 45.171` | 6 | 35 |
| `AN 7.11` | 6 | 18 |
| `SN 45.172` | 5 | 30 |

These are bare enumerations. `AN 7.11` in full is a title, "there are seven
underlying tendencies", the list, and a restatement of the count. `SN 45.171`
carries a peyyala and an explicit expansion instruction. They score well per
word because they *are* the vocabulary, with no context around it. A surface
built from one would demonstrate nothing that a cluster sheet could not state
more usefully.

`MN 77` shows the same distortion from the other direction: ten orphan
entries, all of them `kasina` compounds, one mechanical list inside a long
discourse. Wave 6's Also Considered list already flagged that case; the
correction here is to make it measurable rather than a judgement call.

So the audit now separates candidates by whether the anchoring text is
substantive, using a Pali body-word count from `.bilara-cache`. Texts at or
below 80 words are reported as enumeration stubs on a separate track. Texts
that are not cached are reported as unverified rather than guessed at.

### Method Note: Orphan Percentage Understates Cluster Darkness

Factor 4 asks which governed clusters would gain most. Measuring that by
orphan share alone is misleading, because an *uncited* term is not an orphan
-- it has no anchors to be untranslated -- yet it is equally invisible in
running text.

The audit therefore reports **dark** terms: orphaned plus uncited, meaning no
running-text demonstration anywhere. The difference is not cosmetic. The
emptiness / signless / wishless cluster has only 3 orphans out of 13 terms,
which reads as healthy. It is in fact 13 of 13 dark: the three headwords are
orphaned and all ten supporting terms are uncited. Not one of its governed
terms appears in any translated surface.

| Cluster | Dark | Principal untranslated anchor |
| --- | --- | --- |
| Emptiness / signless / wishless | 13/13 (100%) | `MN 43` |
| Bondage-imagery | 15/17 (88%) | `SN 45.171` / `.172` / `.174` |
| Consummation / unconditioned | 11/16 (69%) | `Iti 44` |
| Bondage / residue | 10/22 (45%) | `AN 7.11` |
| Crossing / release interface | 4/10 (40%) | `MN 70` |

Five clusters are fully shown in running text: dependent arising, experience /
process, five heaps, four noble truths, and sense-fields.

### 1. MN 43: Mahāvedalla Sutta

- Leverage signal: the emptiness / signless / wishless cluster is the only
  governed cluster that is 100% dark, and `MN 43` is its principal anchor,
  carrying both `animitta` and `appanihita`.
- Note what it does not finish: `sunnata` cites `SN 35.85` and `MN 121`, not
  `MN 43`. One surface brings the cluster from 0/13 shown to 2/13. The ten
  supporting compounds are uncited and need citations written, not a further
  translation.
- Strengthens: a cluster with full policy machinery -- report script, contrast
  sheet, governed alternates -- and no running text behind any of it.
- Likely lexicon pressure: confirm whether the three headwords survive contact
  with a text where they are the subject, and write `sutta_references` for the
  ten supporting compounds.
- Status: translated 2026-08-20. See
  [MN 43](translations/mn43-mahavedalla-sutta.md) and its
  [translation notes](translations/mn43-mahavedalla-sutta-notes.md). The
  cluster moved from 13/13 dark to 11/13: `animitta` and `appanihita` are now
  anchored, and `sunnata` still is not, exactly as predicted. The remaining
  eleven dark terms are the single `sunnata` orphan plus the ten uncited
  supporting compounds, which need citations written rather than another
  translation.

  The pass also turned up a split in the threefold `sankhara` triad --
  `vacisankhara` defaulted to `verbal process` while its two siblings used
  `conditioner` -- and harmonised it before drafting, so the split was not
  propagated to a second surface.

### 2. SN 51.13: Chandasamādhi Sutta

- Leverage signal: three orphan majors -- `chanda`, `iddhipada`, `vimamsa` --
  the highest count of any substantive text, in 242 Pali words.
- The `iddhipada` family has no governed cluster of its own, so this opens
  territory rather than completing it. `chanda` carries drift risk against
  `kamacchanda` and `tanha`, and the kama cluster already governs that
  boundary from the other side.
- Likely lexicon pressure: whether `chanda` holds `desire` once it heads a
  wholesome path factor rather than sitting beside the sensuality family.
- Status: translated 2026-08-20. See
  [SN 51.13](translations/sn51-13-chandasamadhi-sutta.md) and its
  [translation notes](translations/sn51-13-chandasamadhi-sutta-notes.md).
  `chanda` held `desire` without needing a context rule: what makes
  `kamacchanda` a distraction is the sensuality, not the desiring, so the
  headword survives contact with a wholesome path factor unchanged. All three
  orphan majors are now anchored, taking the repository from 43 orphan majors
  to 40. The notes flag `padhanasankhara` as the load-bearing ungoverned
  compound, and record that `padhana`, `sammappadhana`, and
  `cattaro-sammappadhana` all lack `sutta_references` that this discourse
  could supply.

### 3. MN 70: Kīṭāgiri Sutta

- Leverage signal: two orphan majors, `cetovimutti` and `pannavimutti`, and
  the crossing / release interface cluster is 40% dark.
- Touches three governed clusters at once -- crossing / release, knowledge /
  seeing / understanding, and abandonment-sequence -- which is unusual.
- Likely lexicon pressure: the relationship between the two liberations, which
  the repository currently governs as separate records with no surface showing
  them contrasted.

### 4. Iti 44: Nibbānadhātu Sutta

- Leverage signal: 135 Pali words, four orphans, and the consummation /
  unconditioned cluster is 69% dark.
- Anchors `nibbana-dhatu`, `saupadisesa-nibbana-dhatu`,
  `anupadisesa-nibbana-dhatu`, and `parinibbana-dhatu` -- the last of which had
  its citation repaired to `Iti 44` on 2026-08-19, so this would be the first
  surface to exercise that repair.
- Caveat: it is short and carries verse, and the collection has no `Iti`
  surface yet, so it would set precedent for how the reader handles them.

### 5. SN 12.43: Dukkha Sutta

- Leverage signal: 183 Pali words and six orphans, all six of them the
  `-samudaya` formula family (`phassa`, `vedana`, `namarupa`, `upadana`,
  `bhava`, `jati`). Completes a formula family inside a cluster that is
  already fully shown.
- Only one orphan major, so it ranks low on factor 2 while being among the
  best per-word returns in the corpus.

### Also Considered

- `DN 22` -- three orphan majors and fifteen citing entries, but the Wave 6
  reasoning is unchanged: `MN 10` already anchors most of it.
- `MN 119` -- `kaya` and `kayagata-sati`, 1902 words, overlapping `MN 10`.
- `AN 3.86` -- `anagami` and `sakadagami`, 274 words, though `SN 55.5` already
  anchors the attainment ladder and this record's citation was repaired on
  2026-08-19.
- `AN 2.9` -- two orphan majors, `hiri` and `ottappa`. Length still
  unverified; see the note on range files below.
- `MN 77` -- verified at 4338 Pali words for ten `kasina` minors. The length
  is now measured rather than assumed, and it confirms the deprioritisation.

**Family-completion candidates.** These carry no orphan majors, so they rank
low on factor 2, but each closes a coherent governed family in one pass:

- `AN 8.6` (433 words) -- the eight worldly conditions, six orphans in three
  pairs: `labha` / `alabha`, `yasa` / `ayasa`, `ninda` / `pasamsa`.
- `MN 41` (1280 words) -- the threefold conduct family, six orphans:
  `kaya` / `vaci` / `mano` crossed with `sucarita` / `duccarita`.
- `SN 45.2` (166 words) -- `kalyanamitta`, `kalyanamittata`, `papamittata`.
  Very short, and the friendship family currently has no surface at all.

### Resolved: The Enumeration-Stub Track

Settled 2026-08-20, and not by translation.

Investigating the bondage-imagery cluster turned up a different defect than the
one being looked for. The cluster declares seventeen terms and validates that
all seventeen records exist, but `render_glossary` iterated a hardcoded subset:
`HEADWORD_TERMS` plus one representative member per family. Ten governed terms
-- three of the four floods, three of the four yokes, and all four bodily knots
-- existed as JSON and appeared in no generated output anywhere. A translator
consulting the repository's own sheets would never have seen them.

Nine other cluster reports had the same shape. All ten now render their full
declared member sets, and `tests/test_cluster_glossary_coverage.py` fails if
any declared term stops appearing.

That is the right remedy for these terms, and a translation surface is not.
Rendering `kāmogho, bhavogho, diṭṭhogho, avijjogho` into English produces
exactly what a glossary row produces, with more ceremony: the reader gains a
three-line page and the translator gains nothing. The audit now confirms the
point numerically. Of the bondage-imagery cluster's fifteen dark terms, **zero
are reachable by a substantive text** -- every one is anchored only to
enumeration stubs.

So `SN 45.171`, `SN 45.172`, `SN 45.174`, `AN 7.11`, and `SN 50.1` stay off the
translation queue permanently. The audit now reports enumeration-only terms
separately from dark terms that a real text could still rescue, which keeps the
ranking pointed at work translation can actually do.

One thing this does **not** change. `dark` still means "never shown at work in
a sentence", not "unpublished". Redefining it to exclude anything now visible
in a glossary was considered and rejected: it would zero the metric for all
twenty-one clusters and erase the Wave 7 ranking signal, MN 43's case with it.
Policy visibility and running-text demonstration are different goods, and the
metric tracks the second.

### Background: The Original Enumeration-Stub Reasoning


The bondage-imagery cluster is 88% dark, and all fifteen dark terms are
anchored by three SN 45 repetition suttas totalling about 100 Pali words:
`SN 45.171` (the floods), `SN 45.172` (the yokes), and `SN 45.174` (the
knots). `AN 7.11` covers six `anusaya` orphans in eighteen words.

`SN 50.1` belongs here too. It was listed as unverified until 2026-08-20;
fetching it showed a five-item `bala` enumeration with a Ganges simile, so its
two orphan majors (`bala`, `saddha`) sit behind a stub rather than a text.

This is the cheapest coverage in the repository, and it is invisible to the
roadmap because the roadmap ranks translation candidates and these should not
become translation surfaces. Handle the enumerations as formula records or
cluster-sheet entries instead. Note that `silabbata-paramasa-kayagantha` sits
in this set: it was revised on 2026-08-20 during the `silabbata` stem pass and
still has no running text behind it.

### Finding: Range-Bundled Suttas Could Not Be Verified (fixed)

`SN 50.1` has no root-text file of its own. SuttaCentral bundles the
Gangapeyyalavagga repetitions into `sn50.1-12_root-pli-ms.json`, and
`source_url` in `scripts/verify_example_sources.py` builds only the
per-sutta path, so the request 404s.

The consequence is quiet. A citation to a range-bundled sutta is recorded as
`unfetched`, which is neither `absent` nor `ok`, so it neither fails nor
passes. This is the same shape of blind spot as the peyyala case already
recorded in the workflow plan: a verdict that looks like an absence of
evidence and reads like a pass. Do not treat `unfetched` as `fine` either.

Fixed on 2026-08-20. `resolve_source` now falls back to the range bundle,
finding it by listing the vagga directory once and caching the listing. The
sweep went from 10 `unfetched` to 0, and `absent` stayed at 0 -- so the blind
spot was hiding ten citations and none of them was wrong. They resolve as four
`ok`, two `inflected`, and four `inconclusive`, the last because range
bundles are dense with peyyala.

The affected citations were `AN 2.9` (4), `SN 50.1` (3), `SN 43.14`,
`SN 35.191`, and `AN 1.49`.

`Dhp 21` and `Ud 8.3` remain unverifiable for a different reason: their
collections are in the `UNSUPPORTED` set, so no URL is attempted at all. That
is a separate gap and still open.

### Finding: MN 61 Anchors No Governed Vocabulary

`MN 61` is the only translation surface that no term record cites. It was
translated by direct request rather than drawn from a wave audit, so no
lexicon follow-through was written. It shows no policy in running text and
contributes nothing to any cluster. Either write citations for the vocabulary
it governs, or accept it as a reader-facing text with no lexicon role and
record that choice. `tests/test_audit_surface_leverage.py` pins the current
state so the list cannot grow unnoticed.

## Suggested Order (Wave 7)

1. `MN 43` -- the only 100% dark governed cluster
2. `SN 51.13` -- most orphan majors among substantive texts, and short
3. `MN 70` -- three governed clusters at once
4. `Iti 44` -- 69% dark cluster, 135 words
5. `SN 12.43` -- completes the `-samudaya` formula family

Lengths were resolved on 2026-08-20 by caching the missing root texts, which
moved `SN 50.1` to the stub track and confirmed `MN 77`. Three citations
remain unverifiable for structural reasons recorded below.

The enumeration-stub track was settled on 2026-08-20 and removed from the
queue; see Resolved below.

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
- Status: translated. See
  [SN 55.5](translations/sn55-5-dutiyasariputta-sutta.md) and its
  [translation notes](translations/sn55-5-dutiyasariputta-sutta-notes.md).
  Correction to the leverage signal above: SN 55.5 anchors two majors, not
  five. `sakadagami`, `anagami`, and `phala` cite this sutta for Pali that is
  not in it. The discourse covers only the four stream-entry factors, the
  stream as the eightfold path, and the stream-enterer.

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
- Status: translated. See
  [AN 6.63](translations/an6-63-nibbedhika-sutta.md) and its
  [translation notes](translations/an6-63-nibbedhika-sutta-notes.md).
  Correction to the leverage signal above: this discourse does not anchor
  `phala` or `papa`. It uses `vipaka` throughout and never `phala`, and
  contains no `pap` at all. That claim came from a mis-sourced citation, since
  repaired. It genuinely anchors `kamma` and `cetana`.

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
- Status: translated. See
  [SN 12.61](translations/sn12-61-assutava-sutta.md) and its
  [translation notes](translations/sn12-61-assutava-sutta-notes.md).
  Correction to the leverage signal above: `idappaccayata` does not occur in
  SN 12.61 at all. The four formula records do, and that is what this surface
  anchors.

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
- Status: translated. See
  [MN 11](translations/mn11-culasihanada-sutta.md) and its
  [translation notes](translations/mn11-culasihanada-sutta-notes.md). The
  enumeration exposed that the four `upadana` compounds are not consistent with
  each other: two render the head as `taking ... personally` and two as
  `clinging`. That is recorded as the main open lexical question coming out of
  Wave 6.

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

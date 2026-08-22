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

### 3. MN 70: Kīṭāgiri Sutta (withdrawn)

- **Withdrawn 2026-08-20.** Its two orphan majors, `cetovimutti` and
  `pannavimutti`, were orphaned by missing citations rather than by absent
  vocabulary: `MN 43` already demonstrates both. Citing it from those records
  anchored them, and `MN 70` left the ranked candidate list. See Finding:
  Citation Debt Outranks Translation.
- Original leverage signal: two orphan majors, and the crossing / release
  interface cluster is 40% dark.
- Touches three governed clusters at once -- crossing / release, knowledge /
  seeing / understanding, and abandonment-sequence -- which is unusual.
- Likely lexicon pressure: the relationship between the two liberations, which
  the repository currently governs as separate records with no surface showing
  them contrasted.

### 4. Iti 44: Nibbānadhātu Sutta (complete)

- **Translated 2026-08-21.** Anchors all four `nibbana-dhatu` records, taking
  orphans from 140 to 136. Also the repository's first Itivuttaka surface, so
  it settles the collection's framing formulas. The hand-check its
  `UNSUPPORTED` status forced turned up a wrong citation in
  `saupadisesa-nibbana-dhatu`; see the workflow plan.

- Leverage signal: 135 Pali words, four orphans, and the consummation /
  unconditioned cluster is 69% dark.
- Anchors `nibbana-dhatu`, `saupadisesa-nibbana-dhatu`,
  `anupadisesa-nibbana-dhatu`, and `parinibbana-dhatu` -- the last of which had
  its citation repaired to `Iti 44` on 2026-08-19, so this would be the first
  surface to exercise that repair.
- Caveat: it is short and carries verse, and the collection has no `Iti`
  surface yet, so it would set precedent for how the reader handles them.

### 5. SN 12.43: Dukkha Sutta (withdrawn)

- **Withdrawn 2026-08-20.** All six of its orphans were the `-samudaya`
  family, and `MN 9` already states the chain in full. Citing MN 9 from those
  six records anchored them without a translation. Second candidate withdrawn
  for citation debt, after `MN 70`.
- Original leverage signal: 183 Pali words and six orphans, all six of them
  the `-samudaya` formula family (`phassa`, `vedana`, `namarupa`, `upadana`,
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

### Finding: Citation Debt Outranks Translation

Found 2026-08-20 while preparing MN 70, and it changed the queue.

`MN 70` was ranked third on the strength of two orphan majors, `cetovimutti`
and `paññāvimutti`. Both records cited `MN 70` and nothing else. But `MN 43`,
translated earlier the same day, uses `cetovimutti` throughout its final third
-- qualifying it four ways as measureless, through nothingness, through
emptiness, and signless -- and states `paññāvimutti` at 14.1. The vocabulary
was already demonstrated in running text. The records simply did not cite the
surface that demonstrated it.

Adding three verified citations to `cetovimutti`, `paññāvimutti`, and
`suññatā` moved more than translating a 1,945-word discourse would have:

- orphan majors 40 to 37, orphans 178 to 175
- `MN 70` left the ranked candidate list entirely
- the emptiness / signless / wishless cluster reached **zero orphans**, with
  its three headwords all anchored; its remaining ten dark terms are uncited
  supporting compounds, which no translation addresses

**An orphan is a claim about citations, not about coverage.** The audit
measures whether a record's anchors are translated, and a record with a
missing citation is indistinguishable from a record whose vocabulary has never
been shown. The first costs a verified example phrase to fix. The second costs
a translation.

### How Much Debt Is There

A crude sweep -- matching each orphan record's Pali stem against the cached
root texts of the 40 translated suttas that have one -- returns 77 candidates,
26 of them major entries. That number is an upper bound and should not be
quoted as a finding. Short stems produce false positives: `santi` matches the
ordinary verb "there are", and `dhamma` matches nearly everything. Each
candidate needs the term checked in context before a citation is written.

The high-confidence ones visible in that sweep include `sunnata` in `MN 44`
and `MN 64`, `phassa-samudaya` in `SN 12.11`, `MN 9` and `MN 11`, `sakadagami`
in `MN 118`, `sampajanna` in `DN 2` and `MN 39`, and `parinibbana` in `DN 15`
and `MN 118`.

**Run this pass before drafting any further Wave 7 surface.** Every citation it
writes is cheaper than the translation it might otherwise justify, and each
one that lands changes the ranking. Any candidate that survives the pass is a
genuine translation target rather than a bookkeeping gap.

Standing rule: after translating a surface, check which orphan records that
surface now demonstrates and cite it from them. The lexicon pass already
covers terms the surface exposed as missing; this is the reverse direction, and
it was not being done.

### The Citation-Debt Pass, First Round

Run 2026-08-20. Nineteen verified citations, no translation.

| | Before the pass | After |
| --- | --- | --- |
| Orphan majors | 37 | **27** |
| Orphan records | 175 | **156** |
| Anchored records | 450 | 469 |

For scale: the day opened at 45 orphan majors and 185 orphans, across 42
surfaces. Two translations and this pass together account for the difference,
and the pass did more of it than either translation.

**What was cited.** The whole `-samudaya` family -- `phassa`, `vedanā`,
`upādāna`, `bhava`, `jāti`, `nāmarūpa` -- from `MN 9`, which states the chain
in full and has been a governed surface since Wave 3. Then thirteen more:
`saṅkhata`, `tathāgata`, `saṁsāra`, `macchariya` from `DN 15`;
`pāṭimokkha` from `DN 2`; `sakadāgāmī` from `MN 118`; `asaṅkhata` from
`MN 44`; `nibbuta` from `MN 26`; `anāgāmī` and `upādānakkhandha` from `MN 10`;
and the three `āsava` compounds from `MN 2`. Every one verifies `ok` against
the Bilara root text.

**`SN 12.43` is withdrawn as a consequence.** It was ranked fifth for six
orphans, all of them the `-samudaya` family. `MN 9` already demonstrates every
one. This is the second Wave 7 candidate to be withdrawn for the same reason,
after `MN 70`.

### How To Run The Rest Of It

The matcher lives in scratch, not in `scripts/`, because it is not yet good
enough to ship. Two rounds of it were wrong in instructive ways:

- Matching a **truncated stem** produces false positives across compound
  boundaries. `jūtappamādaṭṭhāna`, a compound about gambling, contains the
  letters of `appamāda` and was reported as evidence that `DN 2` demonstrates
  heedfulness. It does not.
- Matching the **term minus its final character with a loose suffix** is
  better but still wrong. It matched `bhavantaṁ`, a respectful address, for
  `bhāvanā`; `dhammataṇhā` for `dhammatā`; `bhikkhuno` for `bhikkhunī`; and
  `sāraṇīya` for `saraṇa`.

What worked was requiring the match to start at a word boundary and then
**reading the matching segment before writing anything**. Every citation in
this round was eyeballed in context first. That is the step that cannot be
automated away, and it is why the remaining candidates are listed rather than
applied.

Roughly thirty candidates remain from the word-boundary sweep, mostly minor
entries: the conduct family (`kāyasucarita` and its five siblings) in `DN 2`
and `MN 117`, the precepts (`pāṇātipāta`, `adinnādāna`, `musāvāda`) in `DN 2`
and `MN 141`, `brahmacariya`, `dhammavinaya`, `sappurisadhamma`,
`chandarāga`, `upasampadā`, `sikkhāpada`, `santuṭṭhi`. Each needs the same
treatment: read the segment, write a phrase, verify.

### The Citation-Debt Pass, Second Round

Run 2026-08-20, immediately after the first. Sixteen more verified citations,
again with no translation.

| | Session start | After round one | After round two |
| --- | --- | --- | --- |
| Orphan majors | 45 | 27 | **27** |
| Orphan records | 185 | 156 | **140** |
| Anchored records | 429 | 469 | **485** |

Round two was entirely minor entries, which is why the major count did not
move. The conduct family -- `kayasucarita`, `vacisucarita`, `manosucarita` and
their three misconduct counterparts -- all came from one segment of `DN 2`,
the divine-eye passage, which states both halves of the set together. The
precepts `panatipata`, `adinnadana` and `musavada` came from the conduct
section of the same discourse, along with `sikkhapada`, `santutthi` and
`dhammavinaya`. Then `chandaraga` from `DN 15`, `sappurisadhamma` from `MN 1`,
`upasampada` from `MN 117`, and `brahmacariya` from `AN 6.63`.

All sixteen verify `ok`. The repository-wide sweep now reports 455 `ok`,
still zero `absent` and zero `unfetched`.

**Three candidates were rejected on inspection**, and they are the useful part
of the record because they show what the matcher cannot decide:

- `bhikkhunī` matched `bhikkhuno`, which is the genitive of `bhikkhu`, a
  different word entirely.
- `dhammatā` matched `dhammataṇhā`, which is `dhamma` plus `taṇhā`.
- `pārisuddhi` matched `parisuddhaṁ`, the adjective `parisuddha`. Related, but
  not the noun the record governs.

Each of these would have produced a citation that passes `verify_example_sources.py`,
because the quoted phrase really is in the cited sutta. The verifier checks
that a phrase occurs; it cannot check that the phrase contains the term the
record is about. That gap is the reason this pass is done by reading rather
than by script.

### What Remains

The word-boundary sweep is now exhausted for terms of eight characters or
more. Shorter terms were excluded because they collide too often to be worth
reviewing one by one, so a residue of genuine debt certainly remains among
them.

The 140 remaining orphans are not all debt. Many are genuine coverage gaps
whose anchors are untranslated, which is what the ranked candidate list is
for. Anything still ranked there has now survived two rounds of this pass.

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
3. ~~the citation-debt pass~~ -- **done, two rounds.** Thirty-five verified
   citations took orphan majors from 45 to 27 and orphans from 185 to 140,
   without a translation
4. ~~`Iti 44`~~ -- **done 2026-08-21.** 69% dark cluster, 135 words, and the
   last translation in the wave. `Iti` is in the verifier's `UNSUPPORTED` set,
   so every citation it added was checked by hand instead -- which is how a
   wrong one already in the lexicon was found

**Wave 7 is complete.** Two of the five original entries have been withdrawn. `MN 70` and
`SN 12.43` were both ranked on orphans that already-translated surfaces
demonstrate; see their entries above. Wave 7 as translation work is now
`MN 43` and `SN 51.13`, both done, plus `Iti 44`. The rest of the value in
the wave turned out to be citation work.

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

## Wave 8 (audited 2026-08-21)

**Wave 8 is not a translation wave.** The audit ranked `DN 22` first, and
checking that signal against the source disqualified it. What the ranking was
actually measuring was citation debt, and the same check found the debt is far
larger than the `partial` bucket the 2026-08-21 sweep cleared.

Run the audit yourself rather than trusting this summary:

```bash
python scripts/audit_surface_leverage.py
```

### 1. Sweep the `inflected` and `inconclusive` citations

296 citations sit in these two buckets — 149 `inflected`, 147 `inconclusive` —
and `verify_example_sources.py` prints `Every verifiable citation checks out`
while they do. Both buckets demonstrably contain wrong citations.

The plan already warned not to read `inconclusive` as `fine`, because a
peyyala anywhere in a root text downgrades every unmatched phrase in it. What
was not recorded is that `inflected` hides the same failure. `inflected` means
a word stem matched, not that the cited phrase is present, so a citation can
quote a different word from the same root and still pass.

Four confirmed by hand, each checked against the cached root text:

| Record | Cites | Quoting | Reality |
| --- | --- | --- | --- |
| `bhagava` | MN 1 | an opening formula sited at Sāvatthī | MN 1 opens at Ukkaṭṭhā, in the Subhaga grove |
| `adhicitta` | MN 44 | `adhicittasikkhā` | MN 44 contains no `adhicitta` at all |
| `anicca` | SN 22.59 | `yadaniccaṁ taṁ dukkhaṁ` | SN 22.59 does not use that form |
| `arahant` | MN 2 | `arahā hoti` | MN 2 contains no `arahā` |

A crude screen — flagging any citation with a whole word stem absent from the
cited sutta — puts 103 of the 296 under suspicion. **That is an upper bound,
not a count of errors.** The screen over-flags compounds and sandhi, where a
word genuinely present appears only inside a longer form. Every one has to be
checked by hand before it is called wrong. Four out of four hand-checked
suspects were real, but they were chosen for being plausible, so that rate
will not hold across the whole set.

Method, the same one that worked on the `partial` bucket: check whether a
whole word stem is missing from the cited sutta, not whether the phrase failed
to match.

**The screen under-flags as well as over-flags.** `triage_citation_stems.py`
calls a word missing when its first five characters are absent from the cited
sutta. A wrong word that happens to share those five characters with a word
the sutta does contain is therefore invisible to it. Both of the DN 22 errors
in section 2 were: `dhammānudhammapaṭipanna` in a text full of `dhamma`, and
`sati-sampajañña` in a text full of `sampajāno`. Neither ever appeared in the
98, and neither appears in the 59 that remain.

Screening instead on how much of each word the sutta can account for as a
contiguous run — the `cover` figure the script already computes — raises the
suspect list from 59 to 110. That is not obviously the better screen: it
trades one false-positive mode for another, since it flags every compound
whose parts the text spells separately (`nibbida` citing `nibbindati`, which
is fine). It is recorded here as a known limit of the current sweep rather
than applied, because changing the screen mid-sweep reclassifies every band.
Whatever the count says, a citation is only wrong once someone has read the
segment.

**Band B cleared (2026-08-21).** 25 citations repaired, band B 27 -> 2.
Suspects 59 -> 33, `ok` 511 -> 540, `inconclusive` 106 -> 84, orphan majors
24 -> 23.

Band B did not have the shape the previous round recorded for it. That round
called band B "mostly compound-forms the text does not spell as one word,"
with the sutta right and the fix a re-quote. Across the remaining 27 the
dominant failure was heavier than that: **eleven cited a sutta containing no
form of the headword at all.** `viraga` cited an MN 149 with no virāga,
`patigha` an SN 35.232 with no paṭigha, `sotapanna` an SN 55.1 with no
sotāpanna, `parinna` an MN 9 with no pariññā, `panna` and `adhipanna` an
SN 12.23 with no paññā, `arahant` an MN 2 with no arahant in either of its
two citations. Those are not re-quotes; each needed a different sutta, and
in nine cases a governed surface was available and took it.

**Four wrong citations were holding up claims in `notes` and
`authority_basis`, which is the part worth remembering.** A citation is not
inert: the editorial prose cites it back. `samma-samadhi` stated that
"MN 117 ... defines the factor through the four jhānas" -- MN 117 contains no
jhāna in any form and defines the factor by its supports and equipment. The
repository's doctrinal position is right and the attribution was wrong: MN 141
does define sammā samādhi through the fourfold sequence, and is a governed
surface, so the claim moved there and MN 117's actual framing is now stated as
its own thing. `nivarana`, `pahana`, `mana` and `raga` needed the same kind of
correction on a smaller scale. **After repairing a citation, grep the record's
own `notes` for the phrase you just removed.** `lint_terms.py` catches this
only when the `authority_basis` source name changes, not when the claim
quietly stops being true.

Two are flagged rather than forced, and both need a decision this pass cannot
make:

- `vipassana-nana` <- SN 12.23. `vipassanāñāṇa` appears in no governed
  surface's body text. Its one occurrence anywhere in the cache is a DN 2
  section heading, which is editorial apparatus rather than running text.
  Citing a heading would be worse than leaving it uncited.
- `pancime-bhikkhave-khandha` <- SN 22.48. The record's **headword itself** is
  unattested: SN 22.48 reads `ime vuccanti, bhikkhave, pañcakkhandhā`, and the
  nearest real `pañcime` phrase is SN 22.89's `pañcime, āvuso,
  upādānakkhandhā`. No correct citation exists for the phrase as recorded, so
  this is a record rename -- identity fields, filename, and the reciprocal
  links in `khandha` and `pancakkhandha` -- not a citation fix.

### The sweep is finished (2026-08-22)

Bands A and C worked in one pass. **Suspects 33 -> 5, band A 1 -> 0, band C
31 -> 3.** `ok` 540 -> 568, `inconclusive` 84 -> 60, orphan majors 23 -> 22.
Across the whole sweep, from the day it opened: **suspects 98 -> 5, `ok`
470 -> 568, `inconclusive` 147 -> 60.**

Band C was supposed to be the false-positive band -- "likely compound," the
screen's own label. It was not. Of its 31 rows, 26 were genuinely wrong, and
the same wrong-sutta failure that dominated band B ran straight through it:
`ekaggata` cited a DN 2 with no `ekaggatā`, `samadhi` an MN 44 with no
`samāhita`, `papa` an AN 6.63 with no `pāpa`, `asekha` an MN 53 -- the *Sekha*
Sutta -- with no `asekha` at all, twice. **The `cover` figure sorts rows by
how much of the missing word the sutta explains, and that turns out to
correlate with nothing.** A wrong citation whose word happens to share letters
with something present scores exactly like a right one. Band C should not be
trusted as a triage tier in future sweeps; it only ever measured spelling
overlap.

Band A's one outstanding row is resolved. `nissarana-dhatu`'s note asked
whoever came next to "fetch that sutta and repair this properly" -- DN 33 was
already in the cache, listing `cha nissaraṇiyā dhātuyo`.

**Three records traded a wrong citation on a governed surface for a correct
one on an ungoverned surface** -- `kama-dhatu` and `nissarana-dhatu` to DN 33,
`uddhambhagiya-samyojana` to AN 10.13. They became orphans by doing so, which
is why orphan minors rose while orphan majors fell. That is the right trade:
the audit measures whether a governed surface demonstrates a term, and a
citation that points at a sutta not containing the word never demonstrated
anything. `papa` went the other way, to a governed AN 3.65.

Five rows remain, and none of them is a repairable citation:

- `bhava-nirodha` and `jati-nirodha` <- SN 12.2 are **correct**. SN 12.2
  spells its arising chain in full and elides the cessation chain
  (`saṅkhāranirodhā viññāṇanirodho …pe…`), so both quoted lines belong to a
  passage the root text abbreviates. This is precisely the case `inconclusive`
  exists for, and they should stay.
- `vipassana-nana` cannot be cited from anywhere. The compound occurs in no
  governed surface's body text and its only occurrence in the cache is a DN 2
  section heading. Documented in the record itself rather than moved.
- `pancime-bhikkhave-khandha` and
  `pancupadanakkhandhesu-assado-adinavo-nissaranam` both have **unattested
  headwords** -- coined formula records naming a phrase no sutta uses. Each is
  a record rename, not a citation fix, and each is flagged in its own record.

**What the sweep was actually worth.** It began as a check on 296 soft
verdicts and ended having found that roughly one in three was wrong, that the
wrongness clustered in citations pointing at the wrong sutta entirely, that
four wrong citations were propping up false claims in editorial `notes`, and
that two records are named after phrases that do not exist. None of that was
visible from `Every verifiable citation checks out`, which the verifier
printed the whole time.

### 2. Repair DN 22 rather than translating it

`DN 22` topped the ranking on three orphan majors — `dhamma`, `kaya`,
`sampajanna`. It should not be translated. Of the five citations behind those
three records:

- **three are already demonstrated by `MN 10`**, a governed surface:
  `kāye kāyānupassī viharati`, `dhammesu dhammānupassī viharati`, and
  `sampajānakārī hoti` all occur in both texts. DN 22 is MN 10 plus the
  expanded truths section, so translating it would re-govern vocabulary the
  corpus already shows in running text.
- **two are wrong.** `dhammānudhammapaṭipanna` and `sati-sampajañña` do not
  occur in DN 22. The first is recorded `inconclusive`, the second
  `inflected`, which is how both survived the sweep.

Moving the three good citations to MN 10 and repairing the two wrong ones
anchors all three majors with no translation at all. This is the third time
this pattern has decided a queue: `MN 70` and `SN 12.43` were both withdrawn
from Wave 7 for it.

**Done (2026-08-21).** All five citations were checked against the cached root
text segment before being rewritten, not against the verifier's verdict:

| Record | Was | Now |
| --- | --- | --- |
| `kaya` | `kāye kāyānupassī viharati` ← DN 22 | same phrase ← MN 10 |
| `dhamma` | `dhammesu dhammānupassī viharati` ← DN 22 | same phrase ← MN 10 |
| `sampajanna` | `sampajānakārī hoti` ← DN 22 | same phrase ← MN 10 |
| `dhamma` | `dhammānudhammapaṭipanna` ← DN 22 | `dhammānudhammappaṭipatti` ← SN 55.5 |
| `sampajanna` | `sati-sampajañña` ← DN 22 | `ātāpī sampajāno satimā` ← MN 10 |

The two repairs both landed on a governed surface rather than needing one.
`dhammānudhammappaṭipatti` is the fourth factor of stream-entry and is spelled
out in `SN 55.5`; the compound `sati-sampajañña` occurs in neither DN 22 nor
MN 10, and the place the two words actually stand side by side is the
satipaṭṭhāna refrain, `ātāpī sampajāno satimā`.

One more citation in the same records was repaired on the way past: `kaya`
cited MN 119 for `kāyagatā sati` split into two words, where MN 119 spells
`kāyagatāsati` solid all thirty times.

`sutta_references` is the field the audit reads for orphan status, not
`example_phrases[].source` — both have to move, or the metric does not.
Result: orphan majors 27 → 24, orphans 134 → 131, `ok` 508 → 511. DN 22 is off
the ranked list entirely, and `MN 119` drops from two orphan majors to one,
exactly as predicted below.

### 3. Then translate, in this order

All three signals below were verified against the cached root text before
being written down, per the Wave 6 method correction.

1. `SN 48.10` — 303 Pali words, `indriya` 14 times and `saddha` 3 times.
   The best ratio in the audit: two orphan majors in a text short enough to
   govern in one sitting.
2. `MN 119` Kāyagatāsati Sutta — 1,906 words, `kāyagatā` 30 times. The
   dedicated anchor for `kayagata-sati`. Note that its other claimed orphan
   major, `kaya`, stops being one as soon as the DN 22 citations move to
   MN 10, so this text is worth one record rather than two.
3. `AN 2.9` — **weaker than the audit implies.** It was ranked while
   uncached; now cached, it is 843 Pali words rather than the short text the
   ranking assumed, and `hiri` occurs exactly once. Its `hiri` citation is
   also among the suspects above. Verify before committing to it.

`SN 50.1`, `SN 45.171`, `SN 45.172`, `SN 45.174`, and `AN 7.11` remain
permanently off the queue as peyyala vaggas and enumeration stubs; the Wave 7
audit settled that and nothing here reopens it.

### What This Wave Says About The Audit Script

`audit_surface_leverage.py` ranks by orphan count, and an orphan is a record
whose citations all point at untranslated suttas. It cannot tell the
difference between a record that needs a translation and a record that needs
its citation corrected. DN 22 ranked first on three records that a governed
surface already demonstrates.

That is not a defect in the script so much as a limit worth stating: the
ranking is a list of records with no running text behind them *as currently
cited*. Check the citations before reading the ranking as a translation queue.

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

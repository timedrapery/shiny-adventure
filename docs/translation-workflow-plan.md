# Translation Workflow Plan

## Purpose

This document defines the current working phase for **shiny-adventure** now
that the repository already functions as a translation-working system rather
than only a term archive.

The repo now has governed major-entry coverage, cluster audits, generated
translator-facing outputs, and verified translation surfaces. The active task
is to extend those assets deliberately while keeping them synchronized.

## Start Here

If you are picking this repository up cold, read this section, then the two
documents it names, then run the checks.

The repository is the editorial and governance layer. The public reading
edition at `reader-src/` is generated from it. Neither is a copy of the other:
the governed translations in `docs/translations/` are authoritative, and the
reader is produced from them.

1. **[reader-architecture.md](reader-architecture.md)** — how the reader is
   generated, which files are authoritative, and how to add a translation or a
   reader introduction.
2. **[plain-english-rollout-plan.md](plain-english-rollout-plan.md)** — the
   register standard's working method, the traps in the tooling, and the
   lexical decisions deliberately deferred. Read before touching a translation
   surface.
3. **[next-sutta-translation-roadmap.md](next-sutta-translation-roadmap.md)** —
   the completed-surface list and the translation queue.

Then confirm the working copy is healthy:

```bash
python scripts/run_checks.py
```

```bash
mkdocs build --strict
```

First-time setup on a new machine:

```bash
python -m venv .venv
```

```bash
python -m pip install -r requirements-dev.txt
```

## Update As Of 2026-08-25

- 62 governed translation surfaces and 62 generated reader pages. SN 48.10
  and MN 119 complete the two strong translation items from the verified Wave
  8 queue; MN 131, SN 22.86, SN 45.2, and AN 8.6 were added by direct request
  or reader-value review outside the wave sequence. AN 2.9 closes the older
  queue and anchors `hiri` and `ottappa` in a compact running text. SN 45.8,
  SN 12.44, AN 3.88, and Iti 49 complete Wave 9. AN 11.12 opens Wave 10
  with six source-verified recollection anchors and a portable daily-life
  practice.
- SN 56.17 was added by direct request as a 53-word definition of ignorance
  through the four truths. It follows SN 56.11 in the reader and makes the
  source's abbreviated four-part practice instruction explicit.
- MN 131 is the control surface for the Bhaddekaratta verse and for its
  explanation through relishing past and future versions of the fivefold
  experiential field and identifying present experience as self.
- SN 22.86 is the control surface for trying to identify the Tathāgata with,
  in, apart from, as the total of, or outside the five heaps before applying
  any of the four post-death positions.
- 1,155 term records, including reusable `bhaddekaratta` and `saccato thetato`
  records and an exact governed example for the SN 22.86 dukkha-nirodha close.
- All 62 surfaces report no automated plain-English register signals. The
  first seven-sutta newcomer review cohort is tracked in
  `reviews/newcomer-review-ledger.json`; human read-aloud and comprehension
  passes remain the final validation gate, so none is mislabeled as validated.
- The reader now includes topic, form, stage, difficulty, and length filters;
  per-sutta source and review disclosures; rendered Playwright/axe checks; and
  EPUB structure validation in the deployment gate.

## State As Of 2026-08-21

- 45 governed translation surfaces. Waves 1 through 7 complete, plus MN 61,
  which was requested directly rather than drawn from a wave audit. Wave 7 was
  MN 43, SN 51.13, and Iti 44.
- 46 reader pages, one per surface, all generated. Every one carries a
  hand-written reader introduction; none is left on the generated default. The
  reader also publishes a downloadable EPUB.
- 1,153 term records. `repo_health.py` reports two open backlog queues: the
  slug/headword mismatch queue, which lists three records whose slug names a
  different Pali phrase from the headword they document, and the governed
  rendering drift queue, which lists 21 declarations — three documents that
  declare two renderings for one headword, and eighteen that declare a
  rendering their term record neither prefers, lists as an alternate, nor
  governs through a context rule.
- Register audit: 10 signals across 46 files — one clause person label, five
  generic `one` as subject, four nominalization chains — concentrated in
  MN 137 (5) and AN 10.60 (3). The rollout plan still says 8; that figure
  counted notes files, which the audit no longer scans.
- The four `upadana` compounds are harmonised on the headword default, and the
  `silabbata` stem renders as `habits and observances` throughout.
- The threefold `sankhara` triad is harmonised on `conditioner`.
- Citation sweep: 470 ok, 0 absent, 0 unfetched, 0 partial.
- 133 orphan records, 26 of them major, down from 185 and 45. Two rounds of
  the citation-debt pass account for most of that; Iti 44 anchored four more,
  and the partial-citation sweep anchored the rest.
- Every governed term a cluster declares now appears in its generated
  glossary.
- The reader deploys automatically from `main` behind the full check suite.

## Open Work

Ordered by value, not urgency.

### 1. Sweep the `inflected` and `inconclusive` citations

Wave 8 was audited on 2026-08-21 and turned out not to be a translation wave.
The ranking put `DN 22` first; checking that signal against the source
disqualified it, and the same check found that the citation debt the `partial`
sweep cleared was the small part of the problem.

296 citations sit in the `inflected` and `inconclusive` buckets, and
`verify_example_sources.py` prints `Every verifiable citation checks out`
while both hide wrong citations. `bhagava` cites MN 1 for an opening formula
sited at Sāvatthī when MN 1 opens at Ukkaṭṭhā; `adhicitta` cites MN 44, which
contains no `adhicitta`; `anicca` cites SN 22.59 for a form it does not use;
`arahant` cites MN 2, which has no `arahā`. A crude screen puts 103 of the 296
under suspicion, but that is an upper bound and every one needs a hand check.

`DN 22` belongs in the same pass rather than in a translation queue: three of
its five cited phrases are already demonstrated by `MN 10`, and two are wrong.

Full reasoning, the verified translation order behind the sweep, and a note on
what the ranking script can and cannot see are in
[next-suttas-roadmap.md](next-suttas-roadmap.md).

```bash
python scripts/audit_surface_leverage.py
```

The sweep itself is reproducible rather than hand-listed:

```bash
python scripts/triage_citation_stems.py --band A
```

It narrows the two buckets to citations with a whole word whose stem is absent
from the cited sutta -- the test that worked on the `partial` bucket. Read its
output as a review list, not an error list: it over-flags compounds and sandhi,
where a word that is present appears only inside a longer form. Band A is
sorted to the front because the sutta explains least of the missing word there.

**Band A is clear as of 2026-08-21.** 25 repaired, 98 suspects down to 74,
`ok` from 470 to 495. One row remains in band A and is flagged rather than
fixed; see below.

Roughly half were the `anagami` pattern -- the cited sutta was right and the
fix was to quote what it actually says. `kamma` is the good example: it cited
AN 6.63 for `kammassa phalaṁ`, a sutta with no `phala` in any form, and now
quotes the line the surface was governed for, `Cetanāhaṁ, bhikkhave, kammaṁ
vadāmi`. The other half were wrong suttas and had to move: `adhisila` and
`adhicitta` cited an MN 44 with no `sikkhā` in it at all, `puthujjana` cited an
MN 9 with no `puthujjana`, and `punna` cited AN 7.52, which is the
Dānamahapphala Sutta and says `mahapphala` throughout rather than `puñña`.

Five examples were removed rather than repaired, because the cited sutta had no
line to move them to and inventing one is worse than carrying one example
fewer: `domanassa`, `puthujjana`, `lokiya`, and both of `punna`'s.

`lokiya` is worth remembering. Neither of its citations survived, and no
governed surface uses the word: MN 117 draws exactly the mundane /
supramundane distinction the record exists for, but calls it `sāsavā
puññabhāgiyā`. The record now quotes that, and the word `lokiya` is marked as
a commentarial convenience for a distinction the suttas draw in other words.

`nissarana-dhatu` is the one band A row left. MN 137 contains no `nissaraṇa`,
so the citation is wrong, but no cached sutta carries the compound
`nissaraṇa-dhātu`. It is flagged in the record rather than moved to a sutta
using the bare `nissaraṇa`, which would trade a wrong citation for a
misleading one. Fetch the six `nissaraṇīyā dhātuyo` sutta and repair it there.

Band B is about half done: 42 down to 27. Band C (31) is untouched and is
mostly the screen's false-positive mode, so it should be expected to come back
largely clean.

Band B turned out to have its own shape. Where band A was mostly wrong suttas,
band B is mostly **compound-forms the text does not spell as one word** --
`vigatalobha` cited to an MN 9 that says `Lobho akusalamūlaṁ`, `rasārammaṇa`
cited to an MN 148 that says `rasāyatanaṁ`, `amohamūla` to an MN 9 that says
`amoho kusalamūlaṁ`. Those are still wrong citations, but the sutta is right
and the fix is a re-quote.

Two results from band B are worth keeping:

- **Two repo-native records for a governed surface carried a garbled Pali
  word.** `mn148-painful-feeling-trained-response` and its untrained twin
  quoted `uraṁtadati`, which is not a Pali word. MN 148 reads `urattāḷiṁ
  kandati`, beating the breast and wailing. This was a transcription error in
  the repository's own phrase records, not an inherited citation.
- **MN 43 does not contain `appaṇihita`.** Its four liberations of mind are
  `appamāṇā`, `ākiñcaññā`, `suññatā`, and `animittā`. The Wave 7 audit ranked
  MN 43 first partly on its carrying both `animitta` and `appanihita`; it
  carries the first and not the second. The translation was still worth doing
  on the rest of the signal, but the ranking repeated on its own top candidate
  exactly the error Wave 6 was corrected for.

### 2. Smaller items

- Consider dropping `HIGH_LOAD_MINOR_LINT_THRESHOLD` from 9 to 7 in
  `scripts/lint_terms.py`, now that the queue it guards is empty.
- Several terms recur across surfaces while still ungoverned: `assutava` and
  `sutava` (seven surfaces), `vemattata`, `kamaguna`, `attabhava`, `samisa`,
  `niramisa`, `nittha`, `dukkhakkhandha`, and the `bhavaditthi` /
  `vibhavaditthi` pair.
- Five dependabot pull requests are open against workflow actions and dev
  dependencies. They were reviewed during the reader phase and deliberately
  left alone; see the reader architecture document.

## Resolved Finding: The Fourfold Source Question

Resolved 2026-08-21. `kiṁnidānaṁ kiṁsamudayaṁ kiṁjātikaṁ kiṁpabhavaṁ` is now
governed by `kim-nidana-kim-samudaya-kim-jatika-kim-pabhava-formula`, a minor
formula record covering both the question and its answering form:

> what is its source? What is its origin? What is it born from? What produces
> it?

> Ignorant wanting is its source, ignorant wanting is its origin; it is born
> from ignorant wanting, and ignorant wanting produces it.

The question and the answer are one unit, not two. The Pali answers by
declining the same four members against the conditioning item, so the English
has to reuse the same four words in the same order or the answer stops sounding
like an answer.

The premise recorded for this task was that two surfaces shared the wording and
a third should not re-solve it. The third surface already existed. **MN 38
carries the same passage, in Pali word-for-word identical to SN 12.11, and had
solved it a third way**: the question became `what is the origin, arising,
birth, and source of`, the answer became `have ignorant wanting as their
source`, and the remaining seven links were compressed into a prose chain
(`And felt experience — from contact. And contact — from the six sense
fields.`). MN 38 now reads as SN 12.11 reads.

Three further things fell out of the same block, all of them compliance with
records that already existed rather than new judgment:

- MN 38 rendered `āhāra` as `nutrients` twice, against its own recorded
  `nutriment`.
- Three of the four nutriment members were off their own major entries:
  `material nutriment` for `kabalinkara-ahara` (`edible-food nutriment`),
  `mental volition` for `manosancetana-ahara` (`mental-intention nutriment`),
  and a bare `contact` for `phassa-ahara` (`contact nutriment`). Each of those
  records carries an explicit `In the four-nutriments framework` rule.
- The compression contradicted MN 38's own recorded policy of preserving
  repetition for study readability. That policy exists to expand `…pe…`, but
  the Pali at mn38:16 carries no peyyala at all — the translation was
  abbreviating a passage the source already writes out in full.

`saḷāyatana` was deliberately left as `six sense fields` in MN 38 rather than
moved to the headword default `six fields of experience`. That is a recorded
controlled alternate this surface carries consistently, so it is not drift.

Two wordings in the same block stay divergent because nothing governs them:
`oḷāriko vā sukhumo vā` (`coarse or subtle` here, `coarse or fine` in
SN 12.11) and the `bhūtānaṁ vā sattānaṁ ṭhitiyā sambhavesīnaṁ vā anuggahāya`
clause. `oḷārika`, `sukhuma`, and `sambhavesī` are all ungoverned; SN 12.11's
notes had already flagged `sambhavesī` as a candidate minor entry. Settle the
records first, then the wording.

### Enforcement

Three patterns were added to `check_translation_formula_consistency.py` so a
fourth surface cannot re-solve this quietly: the recombined question, the
question collapsed to its origin member alone, and the recombined answer. All
three match across `\s+` rather than a literal space, because the wrapped
prose puts a line break inside the formula — the same trap that hid two MN 11
paragraphs during the `upadana` pass.

Both control surfaces had predicted this. SN 12.11's notes asked for a record
if a second surface needed the wording, and MN 11's notes said a third surface
should not re-solve it. Both calls are now marked resolved in place. Neither
noticed that the third surface was already in the repository, which is the
lesson worth keeping: a re-audit call that names a future risk should be
checked against the corpus that already exists, not only against the corpus to
come.

## Resolved Finding: The Split `upadana` Family

Resolved 2026-08-20. The four `upadana` compounds are now harmonised on the
headword default, so the fourfold enumeration reads:

> taking sensuality personally, taking views personally, taking habits and
> observances personally, and taking self-doctrine personally

Two of the four previously rendered the head as `clinging`, which the headword
records only as an alternate. The decisive evidence was already in the
repository: `upadana`'s own compound context rule directs all four members to
carry the headword's appropriative force, so the two `clinging` defaults were
out of compliance with a rule the family had already recorded. The revision was
not a new editorial judgment so much as finishing one.

`silabbatupadana` was the only genuinely new wording. Its recorded alternates
were `appropriating rules and observances` and `rule-and-observance clinging`,
neither of which matches the family pattern.

The same pass then moved the `silabbata` stem from `rules and observances` to
`habits and observances` everywhere it occurs. Changing only the `upadana`
compound would have left one Pali stem rendered two ways across neighbouring
records, which is the same failure this finding exists to close, one level
down. So `silabbata-paramasa` is now `grasping at habits and observances`, the
`kayagantha` knot entry follows it, and MN 2 and MN 64 were brought along
because they carry the fetter wording.

Every revised compound keeps its `clinging` rendering as a controlled
continuity alternate, so source-facing prose can still use the familiar
wording. `silabbatupadana` keeps `clinging to habits and observances`
specifically for continuity with the fetter entry `silabbata-paramasa`.

The pass touched four term records, the headword's family note, six surfaces
(DN 15, MN 2, MN 9, MN 11, MN 64, SN 12.2), five note files, the kama cluster
map and its report script, one policy test, and the generated cluster sheets,
term indexes, and reader pages.

Two scope lessons, both worth repeating:

- The scope recorded before the pass said three surfaces. MN 11 also carried
  the wording and was missed in that count -- the surface whose own notes
  raised the finding.
- Prose surfaces wrap at about 76 characters, so a governed phrase can straddle
  a line break and evade a plain `grep`. Two MN 11 paragraphs were missed on
  the first sweep for exactly that reason. Audit renderings with a
  whitespace-insensitive search (`\s+` between words), not a literal one.

Full rationale is in
[translations/mn11-culasihanada-sutta-notes.md](translations/mn11-culasihanada-sutta-notes.md).

## Resolved Finding: The `partial` Verdict Was Not Benign

Resolved 2026-08-21. The eleven `partial` citations are repaired and the sweep
now reports zero. `ok` went from 455 to 466.

The reason this sat untouched is recorded above: both roadmap documents
described `partial` as *the right sutta quoted with slightly wrong wording* and
filed it under smaller items. **One of the eleven was that.** The other ten
were wrong citations, and four of them were the record's only citation, so
those four records were resting on nothing at all -- the same shape as the
`phala` case from the 2026-08-19 pass.

Three of the ten point back at suttas that pass had already convicted. `AN
3.32` was found not to contain `appaṇihito vimokkho`; `animitta` still cited it
for `animitto vimokkho`, which is not there either. `AN 3.134` was found to be
the three-assemblies sutta with no `dhātu` in it; `hetu` still cited it for
`hetuṁ paṭicca`, and it has no `hetu` either. The earlier pass fixed the
citations it was looking at rather than the suttas it had just disproved.

| Record | Was | Now |
| --- | --- | --- |
| `animitta` | AN 3.32 `animitto vimokkho` | SN 43.4 `animitto samādhi` |
| `cetovimutti` | MN 70 | AN 3.32 `yañca cetovimuttiṁ paññāvimuttiṁ upasampajja viharato` |
| `pannavimutti` | MN 70 | MN 70 `Ayaṁ vuccati, bhikkhave, puggalo paññāvimutto` |
| `hetu` | AN 3.134 | DN 2 `natthi, mahārāja, hetu natthi paccayo sattānaṁ saṅkilesāya` |
| `kilesa` | AN 3.33 | AN 4.5 `Yo ve kilesāni pahāya pañca` |
| `nibbana` | SN 38.1 `taṇhakkhayo nibbānaṁ` | SN 38.1 `rāgakkhayo dosakkhayo mohakkhayo` |
| `nidana` | SN 12.1 | SN 12.11 `kiṁnidānā kiṁsamudayā kiṁjātikā kiṁpabhavā` |
| `sankhata` | SN 43.1 `saṅkhata dhamma` | SN 12.20 `aniccaṁ saṅkhataṁ paṭiccasamuppannaṁ` |
| `sankhata` | SN 43.1 `sabbe saṅkhatā aniccā` | DN 16 `jātaṁ bhūtaṁ saṅkhataṁ palokadhammaṁ` |
| `khaye-nana` | MN 70 `khaye ñāṇaṁ` | SN 12.23 `vimuttūpanisaṁ khaye ñāṇan` |

Three cases are worth remembering:

- `nibbana` was the only genuine wording slip. SN 38.1 really does define
  nibbāna, but by `rāgakkhayo dosakkhayo mohakkhayo`, not by `taṇhakkhayo`.
- `pannavimutti` was the `anagami` precedent again. MN 70 was the right sutta;
  it simply does not carry the long stock phrase the record quoted. The fix was
  to quote what MN 70 says, not to move the citation. Its partner record
  `cetovimutti` had to move, because MN 70 never uses that word at all -- one
  quoted phrase, two records, and only one of them was in the right place.
- `khaye-nana` and `nidana` both moved onto governed surfaces they should have
  been citing all along, SN 12.23 and SN 12.11.

### One Case Left Open

`sabbe-sankhata-anicca` is not a citation repair. Its notes claimed `SN 43.1
anchors the line itself`; SN 43.1 defines the *un*conditioned and contains
neither `sabbe` nor `aniccā`. The phrase `sabbe saṅkhatā aniccā` does not
appear anywhere this repository can reach. The canonical line is `sabbe
saṅkhārā aniccā` (AN 3.136), and the sibling record `anicca-sabbe-sankhara`
already governs it.

So the record governs an English line built by substituting `saṅkhata` into a
formula the texts state with `saṅkhāra`. The false claim is removed and the
record now cites AN 3.136 with an explicit note that the Pali reads `saṅkhārā`.
Whether to merge it into `anicca-sabbe-sankhara` or relabel it as a repository
coinage is an editorial call, not a citation repair, so it is left standing and
flagged in the record itself.

### Method Note

Read a `partial` by checking whether whole word stems are missing, not whether
the phrase failed to match. `normalize()` already folds `ṁ` and `ṃ` together,
so an orthographic mismatch does not produce `partial` -- which was the first
hypothesis here, and it was wrong. If a stem is absent, the citation is wrong,
not merely differently worded.

## Resolved Finding: Unverified Example Citations

Found 2026-08-19 while translating SN 55.5, and resolved the same day. Recorded
because the failure mode is worth recognising again.

Several `example_phrases` cited a `source` sutta that did not contain the Pali
they quoted. `lint_terms.py` checks that a reviewed or stable major entry *has*
example sources; nothing checked that a cited source actually contains the
cited text, so the errors were invisible.

Twelve citations across nine records were wrong. Every one was a genuinely
wrong citation rather than a numbering artefact: the off-by-N hypothesis was
tested by probing plus or minus six around each cited number and found the
phrase nowhere. The cited suttas were about other things -- AN 5.229 is five
dangers in a black snake, AN 3.134 is three kinds of assembly, and AN 4.173
contains no `dhatu` at all.

Every replacement was verified against the Bilara root text before being
written:

| Record | Was | Now |
| --- | --- | --- |
| `anagami` | AN 3.86 `anāgāmī` | AN 3.86 `opapātiko hoti tattha parinibbāyī` |
| `appanihita` | AN 3.32 `appaṇihito vimokkho` | SN 43.4 `appaṇihito samādhi` |
| `issa` | AN 5.229 | DN 21 `issāmacchariya` |
| `macchariya` | AN 5.229 | DN 21 `piyāppiye sati issāmacchariyaṁ hoti` |
| `tathata` | AN 3.134 | SN 12.20 `tathatā avitathatā anaññathatā` |
| `vijja` | AN 10.1 | AN 10.61 `vijjāvimutti` |
| `parinibbana-dhatu` | AN 4.173 | Iti 44 `anupādisesā nibbānadhātu` |
| `sakadagami` | SN 55.5 `sakadāgāmimagga` | AN 3.86 `rāgadosamohānaṁ tanuttā sakadāgāmī hoti` |
| `sotapatti` | SN 55.5 `sotāpattiphala` | SN 55.5 `sappurisasaṁsevo hi` |
| `sotapanna` | SN 55.5 `sotāpannassa` | SN 55.5 `sotāpanno` |
| `phala` | SN 55.5 and AN 6.63 | DN 2 `sāmaññaphalaṁ`, `sandiṭṭhikaṁ sāmaññaphalaṁ` |

`sutta_references` were updated to match, so no record still points at a sutta
none of its examples uses.

Two cases are worth remembering:

- `anagami` was the instructive one. AN 3.86 was the right sutta all along; it
  simply never uses the word `anāgāmī`, naming the non-returner by destiny
  instead. The fix was to quote what the sutta says, not to move the citation.
- `phala` had no valid citation at all. SN 55.5 has no `phal` in any form, and
  AN 6.63 uses `vipāka` throughout. It now cites DN 2, which is already a
  governed surface.

### What This Cost The Audit

The Wave 6 ranking was built partly on this citation data, so some of its
leverage estimates were wrong. SN 55.5 was ranked for five orphan majors and
actually anchors two. Both roadmap documents carry the correction.

### Standing Guidance

Run `python scripts/verify_example_sources.py` after any pass that adds or
edits `example_phrases`. It is opt-in rather than part of `run_checks.py`
because it needs network access.

The 2026-08-25 sweep reports zero `absent`, zero `unfetched`, zero
`unsupported`, and zero `partial` across 804 examples. It reports 135
`inflected`, which is ordinary lemma citation and not an automatic error.

**The `partial` verdict was misread until 2026-08-21.** This section used to
say `partial` is usually the right sutta quoted with slightly wrong wording,
and dismissed the 11 of them as `worth a pass eventually; not defects`. When
the pass was finally run, exactly one of the eleven fit that description. The
other ten were wrong citations of the same kind the 2026-08-19 sweep found:
whole word stems absent from the cited sutta. See the resolved finding below.

One known blind spot: a root text that uses peyyala anywhere makes every
unmatched phrase in it `inconclusive`, even when the elision has nothing to do
with the phrase. That is what initially hid three of the SN 55.5 errors, which
were caught by hand instead. Do not read `inconclusive` as `fine`.

A second blind spot of the same shape was closed on 2026-08-20. SuttaCentral
bundles peyyala vaggas into range files such as `sn50.1-12`, so a per-sutta
URL 404s and the citation was recorded as `unfetched` -- a verdict that
neither fails nor passes. Ten citations across five suttas sat there
unverified. `resolve_source` now falls back to the range bundle, and all ten
resolved without turning up a single wrong citation.

The Khuddaka resolver gap is closed for `Dhp`, `Ud`, `Iti`, `Snp`, `Thag`, and
`Thig`; only a bare `KN` label is intrinsically unresolvable because it does
not identify a collection. On 2026-08-25 the verifier was also changed to list
`partial` matches and make strict mode fail on them. All eight live partials
were repaired. The resulting audit covers 804 examples with zero partial,
absent, unfetched, or unsupported matches.

## Concrete Next Tasks

### Phase 1: Translation Surface Expansion

- Extend `docs/translations/` where the existing cluster policy can already support clean governed text work.
- Use the [Wave 10 execution plan](wave-10-execution-plan.md) as the current source of truth, [next-sutta-translation-roadmap.md](next-sutta-translation-roadmap.md) as the short active-queue view, and [next-suttas-roadmap.md](next-suttas-roadmap.md) for historical audit reasoning.
- Use [first-wave-sutta-translation-prep.md](first-wave-sutta-translation-prep.md) as the completed first-wave operational packet, and use [asava-method-sequence-sheet.md](asava-method-sequence-sheet.md) when revising the completed `MN 2` outflow surface.
- Waves 1 through 8 and the direct-request additions were complete at 55
  surfaces. All four items from the 2026-08-25 Wave 9 audit—SN 45.8,
  SN 12.44, AN 3.88, and Iti 49—are published. AN 11.12 is the first Wave 10
  packet; SN 12.20 is next, followed by AN 8.39 and SN 46.1, subject to the
  source checks recorded in the execution plan.
- Add or refine note surfaces when a translation document exposes missing control language.

### Phase 2: Maintenance And Freshness

- Keep `README.md`, `docs/repository-review-2026-03.md`, and generated indexes aligned with the actual repository state.
- Regenerate derived docs whenever upstream term data changes.

### Phase 3: Controlled Expansion

- Keep using `docs/lexicon-expansion-plan-500.md` as the intake plan for the next family batches.
- Prefer additions that strengthen a live doctrinal cluster or translation surface.

### Phase 4: Targeted Supporting-Term Refinement

- Revise reviewed minor entries when live translation or note work reveals ambiguity that the current note surface does not control well enough.
- Prefer updating a full local family or surface together rather than reopening scattered entries one by one.

## Editorial Standard Going Forward

From this point on, important terms should be revised as systems, not as
isolated files.

For major doctrinal vocabulary, a finished editorial pass should normally
cover:

- the headword
- important compounds
- formula usage
- related examples
- linked entries likely to preserve stale wording

## Definition of Success

This repo is succeeding when a translator can take a passage from a sutta,
identify the relevant doctrinal cluster, and receive:

- the default English rendering
- the allowed alternates
- the discouraged renderings
- the formula-specific overrides
- the related term family needed to keep the passage coherent

That is the working standard for **shiny-adventure** now.

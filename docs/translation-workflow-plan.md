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

## State As Of 2026-08-21

- 45 governed translation surfaces. Waves 1 through 7 complete, plus MN 61,
  which was requested directly rather than drawn from a wave audit. Wave 7 was
  MN 43, SN 51.13, and Iti 44.
- 45 reader pages, one per surface, all generated. Every one carries a
  hand-written reader introduction; none is left on the generated default. The
  reader also publishes a downloadable EPUB.
- 1,155 term records. `repo_health.py` reports no open backlog in any section.
- Register audit: 5 signals, all documented exceptions in the rollout plan.
  Both new surfaces report zero signals. The rollout plan still says 8; that
  figure counted notes files, which the audit no longer scans. Same three
  exceptions either way.
- The four `upadana` compounds are harmonised on the headword default, and the
  `silabbata` stem renders as `habits and observances` throughout.
- The threefold `sankhara` triad is harmonised on `conditioner`.
- Citation sweep: 466 ok, 0 absent, 0 unfetched, 0 partial.
- 136 orphan records, 27 of them major, down from 185 and 45. Two rounds of
  the citation-debt pass account for most of that; Iti 44 anchored the last
  four.
- Every governed term a cluster declares now appears in its generated
  glossary.
- The reader deploys automatically from `main` behind the full check suite.

## Open Work

Ordered by value, not urgency.

### 1. Audit and name Wave 8

Wave 7 finished on 2026-08-21 with `Iti 44`. Its three translation surfaces
were `MN 43`, `SN 51.13`, and `Iti 44`; `MN 70` and `SN 12.43` were both
withdrawn once the citation-debt pass anchored the orphans that justified
them. The queue is now empty, so the next translation needs a fresh audit
rather than a pick from a standing list.

The audit is reproducible rather than hand-computed:

```bash
python scripts/audit_surface_leverage.py
```

Run against the 45-surface state it currently ranks `DN 22` first (three
orphan majors: `dhamma`, `kaya`, `sampajanna`), then `MN 119` (`kaya`,
`kayagata-sati`) and `SN 48.10` (`indriya`, `saddha`, 297 words). Confirm each
leverage signal against the source before committing to a queue position; that
is the method correction Wave 6 paid for.

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

The sweep currently reports zero `absent`, zero `unfetched`, and zero
`partial`. It reports 149 `inflected`, which is ordinary lemma citation and not
an error.

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

One gap is still open: `Dhp`, `Ud`, `Iti`, `Snp`, `Thag`, `Thig`, and `KN`
are in the `UNSUPPORTED` set, so 27 citations are never checked at all. If a
verse citation is wrong, nothing in the repository would notice.

**That gap has now produced a real defect.** Translating `Iti 44` on
2026-08-21 meant hand-checking the four `nibbana-dhatu` records against the
cached root text, and one of them cited `sa-upādisesā nibbānadhātu` -- a
hyphenated form the text does not contain. It had sat there unnoticed because
no script can read `Iti`. The fix was trivial; finding it was not, and nothing
except translating the sutta would have surfaced it. The other three verified
clean. Treat the remaining 27 unsupported citations as unverified rather than
as passing, and hand-check any of them that a new surface touches.

## Concrete Next Tasks

### Phase 1: Translation Surface Expansion

- Extend `docs/translations/` where the existing cluster policy can already support clean governed text work.
- Use [next-suttas-roadmap.md](next-suttas-roadmap.md) as the source-of-truth ranked roadmap for the next outward-facing sutta additions, and use [next-sutta-translation-roadmap.md](next-sutta-translation-roadmap.md) as the short active-queue view extracted from it.
- Use [first-wave-sutta-translation-prep.md](first-wave-sutta-translation-prep.md) as the completed first-wave operational packet, and use [asava-method-sequence-sheet.md](asava-method-sequence-sheet.md) when revising the completed `MN 2` outflow surface.
- Waves 1 through 6 are complete at 41 surfaces, plus MN 61 added outside the wave sequence for 42 total. Wave 7 has not been drafted; running the audit method in [next-suttas-roadmap.md](next-suttas-roadmap.md) against the current state is the prerequisite for naming the next queue. See Open Work above for why that audit is more trustworthy now than it was.
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

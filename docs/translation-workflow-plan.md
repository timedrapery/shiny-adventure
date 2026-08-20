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

## State As Of 2026-08-20

- 42 governed translation surfaces. Waves 1 through 6 complete, plus MN 61,
  which was requested directly rather than drawn from a wave audit.
- 42 reader pages, one per surface, all generated. 11 carry hand-written
  reader introductions. The reader also publishes a downloadable EPUB.
- 1,148 term records. `repo_health.py` reports no open backlog in any section.
- Register audit: 8 signals, all documented exceptions in the rollout plan.
- The four `upadana` compounds are harmonised on the headword default.
- Citation sweep: 400 ok, 0 absent.
- The reader deploys automatically from `main` behind the full check suite.

## Open Work

Ordered by value, not urgency.

### 1. Translate Wave 7

Drafted 2026-08-20. The ranking is `MN 43`, `SN 51.13`, `MN 70`, `Iti 44`,
`SN 12.43`; the reasoning and two method corrections are in
[next-suttas-roadmap.md](next-suttas-roadmap.md).

The audit is now reproducible rather than hand-computed:

```bash
python scripts/audit_surface_leverage.py
```

`MN 43` leads because the emptiness / signless / wishless cluster is the only
governed cluster with no running text behind a single one of its thirteen
terms. Two items to settle first: five candidates have uncached root texts, so
their lengths are unverified; and the enumeration-stub track is cheaper than
anything in the ranking but belongs in formula records, not surfaces.

### 2. Promote the fourfold source question to a formula record

`kim nidana kim samudaya kim jatika kim pabhava` now has identical wording in
SN 12.11 and MN 11. A third surface should not re-solve it.

### 3. Smaller items

- Write reader introductions for the texts that still use the generated
  default. The next ones in newcomer order are the Stage 2 and Stage 3 texts
  without one: SN 55.5, MN 2, MN 118, MN 10, DN 2.
- Work through the 11 `partial` citations from `verify_example_sources.py`.
  Those are usually the right sutta quoted with slightly wrong wording.
- Consider dropping `HIGH_LOAD_MINOR_LINT_THRESHOLD` from 9 to 7 in
  `scripts/lint_terms.py`, now that the queue it guards is empty.
- Several terms recur across surfaces while still ungoverned: `assutava` and
  `sutava` (seven surfaces), `vemattata`, `kamaguna`, `attabhava`, `samisa`,
  `niramisa`, `nittha`, `dukkhakkhandha`, and the `bhavaditthi` /
  `vibhavaditthi` pair.
- Five dependabot pull requests are open against workflow actions and dev
  dependencies. They were reviewed during the reader phase and deliberately
  left alone; see the reader architecture document.

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

The sweep currently reports zero `absent` and zero `unfetched`. It also
reports 11 `partial` and 149 `inflected`, and neither is reliably an error:
`partial` is usually the right sutta quoted with slightly wrong wording, and
`inflected` is ordinary lemma citation. Worth a pass eventually; not defects.

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

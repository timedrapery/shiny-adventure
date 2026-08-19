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

## State As Of 2026-08-19

- 41 governed translation surfaces, Waves 1 through 6 complete.
- 41 reader pages, one per surface, all generated. 10 carry hand-written
  reader introductions.
- 1,148 term records. `repo_health.py` reports no open backlog in any section.
- Register audit: 8 signals, all documented exceptions in the rollout plan.
- Citation sweep: 400 ok, 0 absent.
- The reader deploys automatically from `main` behind the full check suite.

## Open Work

Ordered by value, not urgency.

### 1. Harmonise the four `upadana` compounds

The largest open lexical question, and well evidenced. Two of the four render
the head as `taking ... personally`, matching the `upadana` headword; two use
`clinging`, which the headword records only as an alternate. The
`ditthupadana` notes show the revision was started and left half finished.

Completing it touches two term records, three surfaces (DN 15, MN 9, SN 12.2),
their notes, and the generated cluster sheets. Full evidence is in
[translations/mn11-culasihanada-sutta-notes.md](translations/mn11-culasihanada-sutta-notes.md).

Revise the family in one pass. Half a family is worse than none.

### 2. Draft Wave 7

Undrafted, and the next major translation project. Re-run the audit method in
[next-suttas-roadmap.md](next-suttas-roadmap.md), which is more trustworthy
than it was: four of Wave 6's leverage signals turned out wrong when checked
against sources, all traceable to citations that have since been repaired.

### 3. Promote the fourfold source question to a formula record

`kim nidana kim samudaya kim jatika kim pabhava` now has identical wording in
SN 12.11 and MN 11. A third surface should not re-solve it.

### 4. Smaller items

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

The sweep currently reports zero `absent`. It also reports 11 `partial` and
147 `inflected`, and neither is reliably an error: `partial` is usually the
right sutta quoted with slightly wrong wording, and `inflected` is ordinary
lemma citation. Worth a pass eventually; not defects.

One known blind spot: a root text that uses peyyala anywhere makes every
unmatched phrase in it `inconclusive`, even when the elision has nothing to do
with the phrase. That is what initially hid three of the SN 55.5 errors, which
were caught by hand instead. Do not read `inconclusive` as `fine`.

## Concrete Next Tasks

### Phase 1: Translation Surface Expansion

- Extend `docs/translations/` where the existing cluster policy can already support clean governed text work.
- Use [next-suttas-roadmap.md](next-suttas-roadmap.md) as the source-of-truth ranked roadmap for the next outward-facing sutta additions, and use [next-sutta-translation-roadmap.md](next-sutta-translation-roadmap.md) as the short active-queue view extracted from it.
- Use [first-wave-sutta-translation-prep.md](first-wave-sutta-translation-prep.md) as the completed first-wave operational packet, and use [asava-method-sequence-sheet.md](asava-method-sequence-sheet.md) when revising the completed `MN 2` outflow surface.
- Waves 1 through 6 are complete at 41 surfaces. Wave 7 has not been drafted; running the audit method in [next-suttas-roadmap.md](next-suttas-roadmap.md) against the current state is the prerequisite for naming the next queue. See Open Work above for why that audit is more trustworthy now than it was.
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

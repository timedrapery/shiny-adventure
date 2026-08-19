# Translation Workflow Plan

## Purpose

This document defines the current working phase for **shiny-adventure** now
that the repository already functions as a translation-working system rather
than only a term archive.

The repo now has governed major-entry coverage, cluster audits, generated
translator-facing outputs, and verified translation surfaces. The active task
is to extend those assets deliberately while keeping them synchronized.

## Immediate Goal

Move from foundational cluster buildout to **translation-surface expansion and
maintenance**.

That means each covered doctrinal area should stay usable in four layers:

1. as a headword
2. as part of compounds and supporting entries
3. as part of canonical formulas or control lines
4. as part of live translation documents and generated reference outputs

## Strategic Priorities

### 1. Expand translation-facing text surfaces

The repository already has enough policy to support more governed translation
work directly.

The next gains should come from:

- extending `docs/translations/` where cluster policy is already in place
- treating note files and control lines as first-class editorial surfaces
- using translation work to reveal where supporting entries still need refinement

### 2. Keep generated outputs and navigation current

The generated browsing and translator-facing layers are now part of the normal
working surface.

That means:

- refresh generated docs and translation indexes whenever upstream term data changes
- prefer fixing live data or generators rather than hand-editing derived outputs
- keep navigation and reference layers trustworthy for contributors and translators

### 3. Continue controlled lexicon expansion

Expansion is still useful, but it should now follow the system already in
place.

The next additions should:

- come in coherent 20 to 40 term family batches
- prioritize terms that unlock real translation work
- strengthen live doctrinal clusters instead of isolated dictionary growth

### 4. Keep planning docs honest

Planning and review docs should now track actual repository state rather than
stale expected work.

That means:

- refresh README priorities when major queues empty or focus changes
- update review snapshots when counts or structure change materially
- treat stale roadmap language as a maintenance issue, not harmless drift

### 5. Maintain the reviewed supporting surface

The draft-clearance phase is complete, but supporting entries still need
editorial attention when live translation work exposes pressure.

That means:

- refine reviewed minor records when a translation surface shows ambiguity or drift risk
- revise families together rather than making isolated synonym swaps
- let real text work, not abstract completeness goals, decide when a minor entry needs more rule surface

## Operating Sequence

Use this order when improving the repository:

1. choose a family or translation surface with active pressure
2. review the governing major entries plus affected supporting entries together
3. update translation docs or generated outputs affected by the change
4. run targeted checks and then full verification
5. refresh planning or review docs if the repository state materially changed

## Current Working Surface

The foundational cluster-buildout milestone is largely complete.

The live lexicon currently has no draft major or minor entries.

As of 2026-08-19 every backlog section in `python scripts/repo_health.py`
reports none, including the high-load minor `translation_policy` queue. There
is no remaining machine-detectable gap in the dataset, so the next work has to
be chosen editorially rather than read off a report.

Current governed surfaces already include:

- dependent arising
- five heaps
- six sense fields
- four noble truths
- three marks
- path factors
- practice-text control surfaces
- sensory-response control surfaces

## Active Work

The current active piece of work is the plain-English rollout: bringing the
running text of every translation surface up to
[PLAIN_ENGLISH_STANDARD.md](PLAIN_ENGLISH_STANDARD.md).

[plain-english-rollout-plan.md](plain-english-rollout-plan.md) is the
pick-up-here document for that work. It holds the current counts, the ordered
list of remaining surfaces, the working procedure, and the list of lexical
questions that were deliberately deferred rather than settled as a side effect
of a register pass.

Read it before touching a translation surface. In particular it records the
failure mode that has already bitten twice: governed term records that
themselves carry the translationese, so that fixing a surface breaks the check
suite until the record is fixed too.

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
- Waves 1 through 5 are complete at 36 surfaces. Wave 6 has not been drafted; running the audit method in [next-suttas-roadmap.md](next-suttas-roadmap.md) against the current 36-surface state is the prerequisite for naming the next queue.
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

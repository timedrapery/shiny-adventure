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

## Open Finding: Unverified Example Citations

Found 2026-08-19 while translating SN 55.5. This is the most serious data
issue currently known, and it is not detectable by any check in the suite.

Several `example_phrases` cite a `source` sutta that does not contain the Pali
they quote. Verified against the Bilara source text:

| Record | Cited source | Cited Pali | Present? |
| --- | --- | --- | --- |
| `sakadagami` | SN 55.5 | `sakadāgāmimagga` | no |
| `anagami` | SN 55.5 | `anāgāmimagga` | no |
| `phala` | SN 55.5 | `sotāpattiphala` | no |
| `phala` | AN 6.63 | `kammassa phalaṁ` | no |
| `sotapatti` | SN 55.5 | `sotāpattiphala` | no |
| `sotapatti` | SN 55.5 | `sotāpattiyaṅgāni` | no, text has the singular |
| `sotapanna` | SN 55.5 | `sotāpannassa` | no, text has `sotāpanno` |

SN 55.5 contains no `sakadāgām`, no `anāgām`, and no `phal` in any form.
AN 6.63 uses `vipāka` throughout and never `phala`. `phala` therefore has no
verified citation at all, and `anagami` has none either, since its other
citation is AN 3.86, which also contains no `anāgām`.

The two inflection mismatches have been corrected, because the right form was
verifiable from the source. The rest are left in place and flagged, because
picking a replacement source is an editorial decision and guessing one would
repeat the original mistake.

Why it matters beyond these records:

- The Wave 6 ranking was built partly on this citation data, so its leverage
  estimates were wrong. SN 55.5 was ranked for five orphan majors and actually
  anchors two.
- `lint_terms.py` checks that reviewed and stable major entries *have* example
  sources. Nothing checks that a cited source contains the cited Pali.

### The Tooling Now Exists

`python scripts/verify_example_sources.py` fetches the Bilara root text for
each cited sutta and reports whether the quoted Pali is there. It is opt-in
rather than part of `run_checks.py`, because it needs network access and a
check that fails when GitHub is unreachable would be worse than no check.

Sweep of all 738 examples, 2026-08-19:

| Verdict | Count | Meaning |
| --- | --- | --- |
| ok | 387 | found |
| inflected | 147 | stem present, different ending; normal lemma citation |
| inconclusive | 148 | root text uses peyyala, so absence proves nothing |
| partial | 11 | right sutta, wrong quoted wording |
| absent | 9 | no word of the phrase in the cited sutta |
| unfetched | 10 | retrieval failed |
| unsupported | 26 | Dhp / Iti / Ud, chunked by verse range in Bilara |

Only `absent` is reliably an error, and even there one caveat applies: AN
numbering is not stable across editions. All nine remaining `absent` verdicts
are AN citations, and SuttaCentral's AN 3.134 is Parisāsutta where other
schemes number that discourse differently. Before treating one as wrong, check
the fetched sutta's title.

The nine are: `anagami` (AN 3.86), `appanihita` (AN 3.32), `issa` and
`macchariya` (AN 5.229, two each), `parinibbana-dhatu` (AN 4.173), `tathata`
(AN 3.134), and `vijja` (AN 10.1). `anagami` is confirmed wrong by hand: AN
3.86 is the right *kind* of sutta and contains `sakadāgāmī` and `sotāpanno`,
but no `anāgām` in any form. The other eight need the numbering check before
anyone edits them.

Building the tool took four corrections, all found by testing it against
records verified by hand first, and all worth knowing if it is ever extended:
case-sensitive stem probes missed segment-initial capitals; diacritic
conventions differ between the records (`paṭhavi`) and Bilara MS (`pathavi`);
root texts abridge with peyyala so absence often proves nothing; and a stem
that keeps the final vowel misses ordinary case inflection.

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

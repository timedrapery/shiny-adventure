# Wave 9 Execution Plan

This is the durable handoff document for the next translation wave. A
contributor should be able to clone the repository on another machine, confirm
the baseline, and continue without relying on chat history.

## Baseline

Snapshot date: 2026-08-25.

- 58 governed translation surfaces and 58 generated sutta pages
- 1,155 governed term records
- 633 cited term records: 525 anchored by a translated surface and 108 orphaned
- 10 orphan major terms
- 804 cited example phrases checked: zero partial, absent, unfetched, or
  unsupported matches
- all generated sutta pages included in the rendered axe accessibility suite

Reproduce the planning audit with:

```bash
python scripts/audit_surface_leverage.py --top 20
python scripts/verify_example_sources.py --strict --top 30
```

Do not select a text solely because it has many citations. Confirm that its
root text contains the governed term in meaningful running prose. Bare lists,
peyyāla stubs, and collection headings belong in formula or cluster work, not
in the reader as standalone translations.

## Committed Queue

Work in this order unless a direct reader request takes priority.

1. **SN 45.8, Vibhaṅga Sutta** — **complete 2026-08-25.** 300 Pali words.
   Anchors the orphan major
   `ariya` inside a complete explanation of the noble eightfold path. This is
   the strongest combination of reader value, manageable length, and
   path-cluster pressure.
2. **SN 12.44, Loka Sutta** — **complete 2026-08-25.** 182 Pali words.
   Anchors `loka` through the arising and ending of the world in lived sensory
   experience, with direct value for the reader's dependent-arising and
   sense-contact pathways.
3. **AN 3.88, Tatiyasikkhā Sutta** — **complete 2026-08-25.** 230 Pali
   words. Anchors `adhicitta` in the threefold training. AN 4.41 was removed as
   a false leverage anchor because it contains only a related mind-development
   phrase, not `adhicitta`.
4. **Iti 49, Diṭṭhigata Sutta** — 173 Pali words. Anchors `pariyuṭṭhāna` in
   its active sense of being taken over by views and strengthens the
   abandonment-sequence cluster.

SN 35.82 was the fallback for SN 12.44 but was not needed: the published
edition makes the abbreviated repetition readable by naming all six sense
doors and consolidating their shared causal tail. DN 21 and DN 1 remain useful
but are deferred because their length is disproportionate to one orphan-major
anchor. Short Dhammapada verses remain eligible as poetry, but the current
length heuristic reports them with enumeration stubs, so inspect them by hand
before promoting one.

## Packet Required for Every Sutta

Each queue item is complete only when one pull request or commit series adds
all of the following:

1. Cached Bilara root Pali and a checked source boundary.
2. A term-family inventory, including collisions and context-specific
   renderings.
3. A plain contemporary English translation in `docs/translations/`.
4. Companion notes documenting source decisions, uncertainties, readability
   status, and review evidence.
5. A hand-written `Before you read` introduction and reader metadata in
   `scripts/surface_registry.py`.
6. Regenerated reader pages, indexes, navigation, glossary, and EPUB inputs.
7. Updated roadmap, changelog, and any term records the translation changed.
8. Clean validation results from the gates below.

Never mark a surface `validated` without recorded human evidence. Source
fidelity, read-aloud usability, and newcomer comprehension are separate gates.

## Validation Gates

Run these from the repository root before publishing:

```bash
python scripts/verify_example_sources.py --strict --top 30
python scripts/run_checks.py
python -m mkdocs build --strict
pnpm exec playwright test
```

Then build or validate the EPUB through the normal reader generation workflow.
The rendered accessibility suite discovers every directory under
`site/suttas/`; a new page is therefore covered automatically after the site
build.

## Human Review Workstream

The initial seven-sutta review cohort stays independent of Wave 9 drafting.
Use [the newcomer review workboard](../reviews/README.md) to recruit five new
readers per text and record one full read-aloud review. Do not delay a
source-faithful draft for unavailable participants, but keep it provisional
until the ledger satisfies the review threshold.

The next human-review cohort should be created only after the initial cohort
has usable results. The likely second cohort is AN 2.9, AN 3.69, AN 4.5, and
SN 1.1, followed by the Wave 9 surfaces.

## Restart and Handoff Procedure

On any machine:

```bash
git fetch origin
git switch main
git pull --ff-only
git status --short
python scripts/repo_health.py
```

Read this plan, the short
[active roadmap](next-sutta-translation-roadmap.md), and the
[translation workflow](translation-workflow-plan.md). Choose the first
unfinished queue item, create a `codex/` or contributor branch, and keep the
entire translation packet together. Before stopping, record completed work,
open questions, exact validation results, and the next action in the surface
notes or this plan—not only in a local terminal or chat.

After merging or pushing to `main`, confirm both GitHub Actions workflows are
green and open the public reader page. Check the title, introduction,
translation, source disclosure, previous/next navigation, and narrow-screen
reflow.

## Definition of Wave Completion

Wave 9 is complete when all four queue items are published, their source
examples pass the strict verifier, the full repository checks and rendered
accessibility suite pass, the live pages are reachable, and this plan has been
replaced by a fresh audit rather than merely relabeled.

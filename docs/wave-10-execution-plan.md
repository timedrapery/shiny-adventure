# Wave 10 Execution Plan

This is the durable handoff document for the active translation wave. A
contributor should be able to clone the repository on another machine,
confirm the baseline, and continue without relying on chat history.

## Baseline

Snapshot date: 2026-08-25.

- 61 governed translation surfaces and 61 generated sutta pages
- 1,155 governed term records
- 633 cited term records: 532 anchored by a translated surface and 101 orphaned
- 9 orphan major terms
- 806 cited example phrases checked: zero partial, absent, unfetched, or
  unsupported matches
- all generated sutta pages included in the rendered axe accessibility suite

Reproduce the planning audit with:

```bash
python scripts/audit_surface_leverage.py --top 20
python scripts/verify_example_sources.py --strict --top 30
```

Do not select a text solely because it has many citations. Confirm that its
root text contains each governed term in meaningful running prose. Bare lists,
peyyāla stubs, collection headings, and related-but-different compounds belong
in formula or cluster work, not automatically in the reader queue.

## Source-Audit Findings

- SN 55.30 is a real dialogue, but it does not contain `ariyapuggala`. Its
  relevant running-text term is `ariyasāvaka`, and its Saṅgha formula is
  abbreviated. The false direct citation was removed.
- AN 11.12 contains six recollections, not seven. It does not contain
  `upasamānussati`; that false citation was replaced by the exact list source
  at AN 1.296-305.
- SN 50.1 remains an enumeration or peyyāla-family signal, despite appearing
  at the top of the raw major-term ranking. Do not promote it without first
  establishing a substantive source boundary.

## Committed Queue

Work in this order unless a direct reader request takes priority.

1. **AN 11.12, Dutiyamahānāma Sutta** — **complete 2026-08-25.** 367 Pali
   words. Anchors six verified recollection compounds in a portable practice
   for walking, standing, sitting, lying down, working, and family life.
2. **SN 12.20, Paccaya Sutta** — 355 Pali words. Five verified orphan signals
   in a substantive dependent-arising text. Before drafting, inspect every
   credited compound and decide how to present its compressed formula without
   losing the source boundary.
3. **AN 8.39, Abhisanda Sutta** — 268 Pali words. Two orphan signals in a
   manageable ethics-and-consequence teaching. Confirm both terms in the root
   before translation.
4. **SN 46.1, Himavanta Sutta** — 125 Pali words. One orphan awakening-factor
   anchor and a compact practice comparison. Use after the two higher-leverage
   texts, or as a safe fallback if either source audit fails.

DN 21 and DN 1 each carry one orphan major but are deferred at roughly 3,142
and 7,693 Pali words. Their reader value may justify later full packets, but
not as efficient one-term anchors.

## Packet Required for Every Sutta

Each queue item is complete only when one commit series adds all of the
following:

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
`site/suttas/`; a new page is covered automatically after the site build.

## Human Review Workstream

The initial seven-sutta review cohort stays independent of Wave 10 drafting.
Use [the newcomer review workboard](../reviews/README.md) to recruit five new
readers per text and record one full read-aloud review. Do not delay a
source-faithful draft for unavailable participants, but keep it provisional
until the ledger satisfies the review threshold.

The likely second cohort is AN 2.9, AN 3.69, AN 4.5, and SN 1.1, followed by
the Wave 9 and Wave 10 surfaces.

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

Wave 10 is complete when all four queue items are published, their source
examples pass the strict verifier, the full repository checks and rendered
accessibility suite pass, the live pages are reachable, and this plan has been
replaced by a fresh audit rather than merely relabeled.

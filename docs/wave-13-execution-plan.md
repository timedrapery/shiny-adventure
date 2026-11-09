# Wave 13 Execution Plan

This is the durable handoff document for the active translation wave. A
contributor should be able to clone the repository on another machine, confirm
the baseline, and continue without relying on chat history.

It replaces the [Wave 12 execution plan](wave-12-execution-plan.md), which is
complete. This plan is written from a fresh audit run on 2026-11-09, not by
extending Wave 12's ranking.

## Baseline

Snapshot date: 2026-11-09, after the audit and its repairs.

- 75 governed translation surfaces and 75 generated sutta pages
- 1,161 governed term records
- 648 cited term records: 575 anchored by a translated surface and 73 orphaned
- 7 orphan major terms
- 843 cited example phrases checked: zero partial and zero absent matches

Do not copy these numbers forward. Regenerate them:

```bash
python scripts/audit_surface_leverage.py --top 20
python scripts/next_sutta_priority_report.py
python scripts/verify_example_sources.py --strict --top 30
```

## What This Audit Changed

As in Wave 12, every orphan record's headword was checked against the root
text of each discourse it cites, not only its quoted examples.

- **`paritta`** cited Sn 1.8 (Karaṇīyamettā) and Khp 6 (Ratana). Both are
  recited as protection texts, but neither contains the word. It now cites
  AN 4.67, where the verse `Katā me rakkhā katā me parittā` (`I have made my
  safeguard, I have made my protection`) verifies `exact`.
- **The three unification records are one family again.** Wave 12 recorded
  that `animitta-samādhi` and `appaṇihita-samādhi` still preferred `signless
  samadhi` and `wishless samadhi`, from before the samādhi ruling, while
  `suññata-samādhi` read `unification that comes forth from emptiness`. They
  now prefer `emptiness unification`, `signless unification`, and `wishless
  unification`, the compact form the samādhi record allows in compounds, with
  the old renderings kept as alternates. No translation surface used them.

## Source-Audit Findings

- **The orphan-major ranking is still spent for short prose.** Its leaders
  are DN 1 and DN 21 (long), Dhp 202 and Dhp 368 (`santi` as compound member
  and adjective), and the same enumeration stubs as Wave 12.
- **This queue is ranked on reader value plus a verified anchor.** Four of
  the five items anchor an orphan record; the fifth, Snp 1.8, anchors nothing
  new but is one of the most recited texts in the canon and opens the Sutta
  Nipāta.
- **`bodhisattva` cites MN 123 for the Sanskrit spelling.** MN 123 has
  `bodhisatta`. The record is a spelling-pointer, like `śūnyatā` was; leave it
  for a later decision on Sanskrit records rather than repairing it here.

## Committed Queue

Every signal below was checked against the root text before the item was
given a position.

1. **Dhp 179–196, the Buddhavagga** — **complete 2026-11-09**. 210 Pali words in eighteen verses, one
   upstream file (`dhp179-196`). The Buddha chapter, with verses 183 to 185:
   `not doing any evil, taking up the wholesome, purifying the mind`.
   Anchors `khanti` (`khantī paramaṁ tapo`, verse 184). Follows the Dhp 21–32
   framing.
2. **Snp 1.8, the Karaṇīyamettā Sutta** — **complete 2026-11-09**. 134 Pali words in ten verses. What
   should be done by someone skilled in the good: friendliness for all
   beings, `as a mother would her only child`. The repository's first Sutta
   Nipāta surface; its notes settle the collection's framing.
3. **AN 8.41, Saṅkhittūposatha Sutta** — **complete 2026-11-09**. 337 Pali words. The eight factors of
   the observance day, each modeled on the arahants. Anchors `uposatha`.
4. **AN 8.54, Dīghajāṇu Sutta** — **complete 2026-11-09**. 626 Pali words. Four things for welfare
   here and now and four for welfare in the future, taught to a householder.
   Anchors `pāpamitta`. The most practical lay text in the queue.
5. **MN 113, Sappurisa Sutta** — **complete 2026-11-09**. 1,448 Pali words. The good person and the
   bad person: pride in family, fame, gains, learning, ascetic practice, or
   even meditative attainment marks the bad person; the good person puts the
   practice, and non-identification, first. Anchors `asappurisadhamma`.
   **Replaces AN 1.49–52.** That surface would span two upstream bundle files
   (`an1.41-50`, `an1.51-60`) and two vaggas, and its SuttaCentral source link
   could not be verified from the working environment. It stays a good
   candidate once a cross-file surface is designed.

## Off The Queue, And Why

- **SN 50.1** — no discrete source boundary. Permanently off.
- **SN 43.4, SN 45.171, SN 45.172, SN 45.174, AN 7.11, AN 7.17, AN 7.18,
  AN 8.59, AN 10.13, SN 22.15, SN 22.105** — enumeration stubs.
- **MN 77** — kasiṇa formula sheet, not a translation.
- **DN 1, DN 14, DN 16, DN 21, DN 33** — real anchors, deferred on length.
- **Dhp 202, Dhp 368** — `santi` is not a clean noun anchor in either.
- **MN 113 (1,448 words), AN 8.51 (881), MN 123 (1,177)** — verified anchors
  for `asappurisadhamma`, `bhikkhunī`, and `bodhisatta`; good candidates for
  the next wave.
- **Khp 1, AN 5.36, AN 1.296–305, SN 4.3, AN 7.16** — verified but very short
  or low reader value; batch them later if at all.

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

## Validation Gates

```bash
python scripts/verify_example_sources.py --strict --top 30
python scripts/run_checks.py
python -m mkdocs build --strict
pnpm exec playwright test
```

## Restart and Handoff Procedure

```bash
git fetch origin
git switch main
git pull --ff-only
git status --short
python scripts/repo_health.py
```

Read this plan, the short [active roadmap](next-sutta-translation-roadmap.md),
and the [translation workflow](translation-workflow-plan.md). The first
queue is finished: Dhp 179–196, Snp 1.8, AN 8.41, AN 8.54, and MN 113 are all
published. The next step is a fresh audit for the next wave.

## Definition of Wave Completion

Wave 13 is complete when all five queue items are published, their source
examples pass the strict verifier, the full repository checks and rendered
accessibility suite pass, and the live pages are reachable. After the last
item, run a fresh audit and write a new plan from it.

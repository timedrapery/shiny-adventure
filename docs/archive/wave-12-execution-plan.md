# Wave 12 Execution Plan

**Complete 2026-11-09. Superseded by the
[Wave 13 execution plan](wave-13-execution-plan.md).** Kept for its source
findings. The unification-record follow-up below was done in the Wave 13 audit.

This is the working plan for the active translation wave. A
contributor should be able to clone the repository on another machine, confirm
the baseline, and continue without relying on chat history.

It replaces the [Wave 11 execution plan](wave-11-execution-plan.md), which is
complete. This plan is written from a fresh audit run on 2026-11-09, not by
extending Wave 11's ranking.

## Baseline

Snapshot date: 2026-11-09, after the audit and its citation repairs.

- 70 governed translation surfaces and 70 generated sutta pages
- 1,161 governed term records
- 638 cited term records: 563 anchored by a translated surface and 75 orphaned
- 8 orphan major terms
- 830 cited example phrases checked: zero partial and zero absent matches
- all generated sutta pages included in the rendered axe accessibility suite

Do not copy these numbers forward. Regenerate them:

```bash
python scripts/audit_surface_leverage.py --top 20
python scripts/next_sutta_priority_report.py
python scripts/verify_example_sources.py --strict --top 30
```

## What This Audit Changed

The example verifier only checks quoted phrases. Most orphan records cite a
sutta with no quoted phrase at all, so this round also checked every orphan
record's headword against the root text of each discourse it cites, part by
part for hyphenated headwords. That found five citations to texts that do not
contain the word. All five are repaired:

- **`adhiṭṭhāna`** cited AN 10.176, the Cunda Sutta, which has no form of the
  word. DN 33 lists `cattāri adhiṭṭhānāni`, but those are the four foundations
  (discernment, truth, generosity, calming), not the record's `resolution`
  sense, so it was not substituted. The record is now uncited.
- **`āloka-kasiṇa`** cited MN 77, whose ten kasiṇa bases end with space and
  consciousness and include no light kasiṇa. AN 10.25 gives the same ten. The
  record is now uncited.
- **`asappurisadhamma`** cited MN 110, which speaks of the bad person and their
  qualities but never uses the compound. It now cites MN 113, which opens with
  it, and gains a verified example.
- **`diṭṭhāsava`** cited and quoted DN 33, which lists three outflows
  (`kāmāsavo`, `bhavāsavo`, `avijjāsavo`) and no outflow of views. The
  verifier had returned `inconclusive` on it, because DN 33 uses peyyāla, so
  it was never caught. Citation and example are removed, and the bondage /
  residue cluster no longer requires a sutta example for it.
- **`bala`**, an orphan major, cited SN 50.1, which Wave 11 established has no
  discrete source boundary. It now cites AN 5.14, which names the five
  strengths and defines each one. Both of its examples verify `exact` there.

Two formula records gained a second, checkable source. `dukkhā
sabbasaṅkhārā` and `sabbe dhammā anattā` cited only Dhp 278 and Dhp 279,
which the verifier cannot address. Both now also cite AN 3.136, as
`aniccā sabbasaṅkhārā` already did, and verify `exact` there.

One finding is recorded and left alone: `ariya-puggala`'s AN 8.59 example
quotes the eight `puggalā` correctly, but the discourse never uses `ariya`.
The record already says so.

The priority report had a defect this round exposed: its closing footer
looked for a queue position named `next`, which no item uses, so it announced
"there is no next item" while Wave 11 still had one. It now checks whether
any item is unpublished.

## Source-Audit Findings

- **The orphan-major ranking is spent for short prose.** The eight orphan
  majors sit behind the same walls Wave 11 named: enumeration stubs
  (`gantha`, `ogha`, `appaṇihita`, `ariya-puggala`), single verses (`santi`
  at Dhp 202 and Dhp 368), the SN 50.1 repetition series (now repaired for
  `bala`), and long discourses (`issa` at DN 21, `asañña` at DN 1). Only
  `bala` is reachable by a short, clean text, and it leads this queue's
  anchors.
- **This queue is ranked on verified anchors plus reader value.** Each item
  below anchors at least one record and is a text a newcomer would want: the
  three characteristics as a law, the five strengths defined, the
  Dhammapada's Path chapter, recollection of death, and the companion to MN
  122.
- **The emptiness / signless / wishless cluster is still a citation
  problem.** Ten of its thirteen terms have no `sutta_references`. MN 122 is
  now translated and MN 121 is queued, so a citation pass on that cluster is
  worth doing first: it decides which records MN 121 can anchor.

## Committed Queue

Every signal below was checked against the root text before the item was
given a position. Work in this order unless a direct reader request takes
priority.

1. **AN 3.136, Uppāda Sutta** — **complete 2026-11-09**. 94 Pali words, no peyyāla, clean boundary
   (`an3.136:1.1` to `1.15`). Whether Tathāgatas arise or not, the element
   stands: all that has been put together is impermanent, all that has been
   put together is unsatisfactory, all phenomena are not-self; a Tathāgata
   awakens to it and makes it known. Anchors `aniccā sabbasaṅkhārā`,
   `dukkhā sabbasaṅkhārā`, and `sabbe dhammā anattā`, and gives SN 12.20's
   `ṭhitāva sā dhātu dhammaṭṭhitatā dhammaniyāmatā` a second surface.
2. **AN 5.14, Vitthata Sutta** — **complete 2026-11-09**. 181 Pali words; its four mental themes are
   written out in the source. Names and defines the five strengths and
   anchors the orphan major `bala`. The faith definition is the Tathāgata's
   epithets (DN 2), and the strengths follow SN 48.10's faculties.
3. **Dhp 273–289, the Maggavagga** — **complete 2026-11-09**. 209 Pali words in seventeen verses, one
   upstream file (`dhp273-289`). The Path chapter: the eightfold path as best
   of paths, verses 277 to 279 on impermanence, unsatisfactoriness, and
   not-self, and the call to make the effort yourself. Verse handling is
   settled in the Dhp 21–32 notes. Anchors the same three formula lines in
   their verse form.
4. **AN 6.19, Maraṇassati Sutta** — **complete 2026-11-09**. 487 Pali words. Bhikkhus say how they
   recollect death; the Buddha says which of them practice it heedfully.
   Anchors `maraṇassati`, and connects to `appamāda` in Dhp 21–32.
5. **MN 121, Cūḷasuññata Sutta** — **complete 2026-11-09**. 995 Pali words. The gradual entry into
   emptiness, step by step, and the companion to MN 122. Take it last, after
   a citation pass on the emptiness / signless / wishless cluster, and expect
   a full packet.

## Emptiness-Cluster Citation Pass

Done with MN 121, as item 5 required:

- `animitta-cetosamādhi` now cites MN 43 (`sabbanimittānaṁ amanasikārā
  animittaṁ cetosamādhiṁ upasampajja viharati`) and MN 121, both `exact`.
  MN 43 was already translated, so the record is anchored.
- `suññata-samādhi`, `animitta-samādhi`, and `appaṇihita-samādhi` now cite
  SN 43.4 and DN 33 (`suññato samādhi, animitto samādhi, appaṇihito
  samādhi`), `exact` at SN 43.4. Neither text is translated, so they move
  from uncited to orphaned.
- The three `vimokkha` records, the two remaining `cetosamādhi` records, and
  `vimokkhamukha` stay uncited. Their terms belong to the Paṭisambhidāmagga
  and later literature; no sutta source was found.
- Follow-up for the next audit: `animitta-samādhi` and `appaṇihita-samādhi`
  still prefer `signless samadhi` and `wishless samadhi`, which predate the
  samādhi ruling (`unification of mind`), while `suññata-samādhi` reads
  `unification that comes forth from emptiness`. Bring the three into one
  form before they are used on a surface.

## Off The Queue, And Why

Record these so the next audit does not re-propose them.

- **SN 50.1** — no discrete source boundary upstream. Permanently off; `bala`
  now cites AN 5.14 instead.
- **SN 43.4, SN 45.171, SN 45.172, SN 45.174, AN 7.11, AN 8.59, AN 10.13,
  SN 22.15, SN 22.105, AN 7.18** — enumeration stubs. Formula or
  cluster-sheet work, not reader translations.
- **MN 77** — its kasiṇa orphans are a formula sheet, and the discourse is
  long. Do the sheet, not the translation.
- **DN 1 (7,693 words), DN 21 (3,142), DN 33 (8,338), DN 14 (8,437), DN 16
  (14,721)** — real anchors, deferred on length.
- **Dhp 202 and Dhp 368** — `santi` occurs only as a compound member and as an
  adjective. Neither is a clean anchor for the noun.
- **Khp 1, AN 5.36, AN 1.296–305, AN 1.49–52** — verified, but each is a few
  lines and anchors one minor record. Candidates for a later short-text
  packet, not a wave position.
- **AN 10.176** — ranked only on the false `adhiṭṭhāna` citation, repaired
  away this round.

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

Run these from the repository root before publishing:

```bash
python scripts/verify_example_sources.py --strict --top 30
python scripts/run_checks.py
python -m mkdocs build --strict
pnpm exec playwright test
```

## Human Review Workstream

Human review is optional and does not gate publishing. Use
[the newcomer review workboard](../../reviews/README.md) when readers are
available.

## Restart Procedure

On any machine:

```bash
git fetch origin
git switch main
git pull --ff-only
git status --short
python scripts/repo_health.py
```

Read this plan, the short [active roadmap](../next-sutta-translation-roadmap.md),
and the [translation workflow](../translation-workflow-plan.md). The first
queue is finished: AN 3.136, AN 5.14, Dhp 273–289, AN 6.19, and MN 121 are
all published, and the emptiness-cluster citation pass went in with MN 121.
The next step is a fresh audit for the next wave. Keep each translation packet together
on one branch, and record completed work, open questions, and the next action
in the surface notes or this plan.

After merging to `main`, confirm the GitHub Actions workflows are green and
open the public reader page.

## Definition of Wave Completion

Wave 12 is complete when all five queue items are published, their source
examples pass the strict verifier, the full repository checks and rendered
accessibility suite pass, and the live pages are reachable.

After the last item, run a fresh audit and write a new plan from it. Do not
extend this ranking.

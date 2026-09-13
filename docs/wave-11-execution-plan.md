# Wave 11 Execution Plan

This is the durable handoff document for the active translation wave. A
contributor should be able to clone the repository on another machine, confirm
the baseline, and continue without relying on chat history.

It replaces the [Wave 10 execution plan](wave-10-execution-plan.md), which is
complete. This plan is written from a fresh audit run on 2026-09-13, not by
extending Wave 10's ranking.

## Baseline

Snapshot date: 2026-09-13, after the audit and its citation repairs.

- 65 governed translation surfaces and 65 generated sutta pages
- 1,157 governed term records
- 637 cited term records: 552 anchored by a translated surface and 85 orphaned
- 9 orphan major terms
- 821 cited example phrases checked: zero partial and zero absent matches
- all generated sutta pages included in the rendered axe accessibility suite

Do not copy these numbers forward. Regenerate them:

```bash
python scripts/audit_surface_leverage.py --top 20
python scripts/next_sutta_priority_report.py
python scripts/verify_example_sources.py --strict --top 30
```

`verify_example_sources.py` reaches bundled root texts — Dhp verse ranges,
`an2.1-10`, `sn50.1-12` — by listing the upstream directory through the GitHub
contents API. Where that API is unreachable, those citations come back
`unfetched` rather than verified and `--strict` fails on them. That is a
network result, not a citation problem.

## What This Audit Changed

The audit's first job is checking its own inputs, and this round found eight
citation problems in the records it was ranking. All eight are repaired.

Four of them closed an orphan with no translation at all, because the term was
already demonstrated in a text the repository has translated:

- **`cāga`** cited AN 7.49, which is the Dutiyasaññā Sutta and contains no
  form of `cāga`. It now cites `attano cāgaṁ anussareyyāsi` in AN 11.12.
- **`samatha`** and **`vipassanā`** both cited SN 35.204, an
  Ajjhattātītayadanicca repetition sutta in the Saṭṭhipeyyāla vagga, which
  contains neither word. Both now cite MN 43's five supports of right view.
- **`vinaya`** cited MN 108, the Gopakamoggallāna Sutta, which is about the
  Saṅgha after the Buddha's death but contains no form of `vinaya`. It now
  cites `dhammavinaye` in MN 11.

Three were repaired to a true source that is not yet translated, so the record
stays orphaned — the honest outcome, as with `dhammatā` in Wave 10:

- **`appicchatā`** cited AN 4.27. That discourse is titled Santuṭṭhi but
  speaks of being content with what is trifling and easy to get, and has no
  form of `appicchatā`. It now cites the ten topics of talk in MN 122.
- **`diṭṭhadhammanibbāna`** cited MN 13, which contains no form of `nibbāna`
  at all. It now cites DN 1's five here-and-now-nibbāna doctrines.
- **`bhāro have pañcakkhandhā`** quoted a singular that is not in the verse.
  SN 22.22 reads `Bhārā have pañcakkhandhā`, nominative plural agreeing with
  `pañcakkhandhā`.

One was removed rather than repaired:

- **`śūnyatā`** is a record for the Sanskrit spelling. It cited MN 121, which
  contains `suññatā` and no form of `śūnyatā`. A Sanskrit form has no Pali
  running-text anchor, so the citation is gone and the record now points at
  the governed Pali headword `suññatā`, which carries the policy and the
  sources.

Two of these — `diṭṭhadhammanibbāna` at MN 13 and, in Wave 10,
`bojjhaṅgabhāvanā` at SN 46.1 — were invisible to `--strict` because both
discourses use peyyāla, so the verifier returns `inconclusive` and proves
nothing either way. Open `inconclusive` verdicts by hand as well as
`inflected` ones.

The audit script itself had a defect this round exposed. Once the Dhammapada
bundles were cached, `Dhp 21` was filed as an enumeration stub for being
twelve words long. Verse is the densest substantive text there is, not a count
followed by a list, so `audit_surface_leverage.py` no longer ranks any verse
collection by length.

## Source-Audit Findings

- **SN 50.1 is settled, permanently.** Three plans have carried a note saying
  not to promote it without first establishing a substantive source boundary.
  There is none to establish: upstream has no `sn50.1` file. The text lives in
  `sn50.1-12`, the Balādisutta of the Gaṅgāpeyyālavagga, which covers twelve
  discourses in one Ganges-repetition series. Its content is real — the five
  strengths, the Ganges slanting east, the same four-part tail as SN 46.1 —
  but there is no discrete discourse to give a boundary to. The orphan major
  `bala` and the record `saddhā` therefore cannot be anchored by translating
  SN 50.1, and no translated surface states the five strengths. That is a
  genuine gap, and closing it needs a different text, not this one.
- **The orphan-major track is exhausted for short substantive prose.** All
  nine remaining orphan majors sit behind one of four walls: verse (`appamāda`
  at Dhp 21, `santi` at Dhp 202 and Dhp 368), a peyyāla series with no
  boundary (`bala`), an enumeration stub (`appaṇihita` at SN 43.4, `gantha` at
  SN 45.174, `ogha` at SN 45.171, `ariyapuggala` at AN 8.59), or a very long
  discourse (`issa` at DN 21 at 3,142 words, `asañña` at DN 1 at 7,693 words).
  Ranking the next wave purely by orphan majors would therefore produce either
  a verse decision or a multi-thousand-word packet. This plan does the first.
- **The emptiness / signless / wishless cluster is a citation problem, not a
  translation problem.** It reports 11 of 13 terms dark, but ten of those are
  *uncited* rather than orphaned: they have no `sutta_references` at all, so
  no translation can anchor them until someone gives them verified sources. A
  citation pass on that cluster would move it further than any single text.

## Committed Queue

Every signal below was checked against the cached root text before the item
was given a position. Work in this order unless a direct reader request takes
priority.

1. **Dhp 21–32, the Appamādavagga** — 124 Pali words in twelve verses, one
   upstream file (`dhp21-32`), clean boundary. Anchors the orphan major
   `appamāda` (`Appamādo amatapadaṁ, pamādo maccuno padaṁ`) and the record
   `amatapada`. **Precondition: settle verse before drafting.** This would be
   the repository's first Dhammapada surface and its first verse surface, and
   the packet must decide, in the notes, how verse lines are set, whether the
   commentarial `vatthu` headings are excluded (they are not canonical verse
   and should be), and how a vagga is titled and numbered as a reader page.
   Iti 44 is the precedent for adding a collection: settle the framing in the
   notes, once, for everything that follows.
2. **Ud 8.3, Tatiyanibbānapaṭisaṁyutta** — 84 Pali words, no peyyāla. Anchors
   `asankhata-dhatu` with an exact quotation, and it is the `atthi, bhikkhave,
   ajātaṁ abhūtaṁ akataṁ asaṅkhataṁ` passage, which carries its own argument:
   without the unborn there would be no escape from the born. The repository
   already has Itivuttaka surfaces, so a second Khuddaka collection is a small
   step. The shortest high-value item on the list.
3. **SN 22.22, Bhāra Sutta** — 108 Pali words. Anchors the burden formula. The
   burden is the five clung-to heaps, the carrier is the person, taking it up
   is ignorant wanting, putting it down is its fading. Note before drafting
   that `puggalo tissa vacanīyaṁ` is a long-standing interpretive crux and the
   translation must not settle it; the notes are where that belongs.
4. **SN 22.26, Assāda Sutta** — 223 Pali words, one peyyāla. Anchors the
   `imesaṁ pañcannaṁ upādānakkhandhānaṁ … assādañca … ādīnavañca …
   nissaraṇañca` formula with an exact quotation. A first-person account of
   the Buddha's pre-awakening investigation, and a natural companion to SN
   22.48 and SN 22.59.
5. **MN 122, Mahāsuññata Sutta** — 1,547 Pali words. Anchors `appicchatā` and
   `asaṁsagga`, the only remaining two-orphan text that is neither an
   enumeration stub nor a deferral on length. Take it only after the four
   short items, and expect a full packet rather than a quick one.

## Off The Queue, And Why

Record these so the next audit does not re-propose them.

- **SN 50.1** — no discrete source boundary upstream; see the findings above.
  Permanently off.
- **SN 43.4, SN 45.171, SN 45.172, SN 45.174, AN 7.11, AN 7.17, AN 7.18, AN
  8.59, AN 10.13, SN 22.15, SN 22.105** — enumeration stubs. Formula or
  cluster-sheet work, not reader translations. Already settled in Wave 7.
- **SN 35.204, AN 4.27, AN 7.49, MN 13, MN 108** — ranked only by citations
  that turned out to be false. Repaired away this round; they carry no
  leverage.
- **MN 77** — ten orphans, all of them kasiṇa records. That is a formula
  sheet, and the discourse is long. Do the sheet, not the translation.
- **DN 1 (7,693 words), DN 21 (3,142), DN 33 (8,338), DN 16 (14,721)** — real
  anchors, deferred on length. Their reader value may justify later packets;
  none is an efficient one-term anchor.
- **Dhp 202 and Dhp 368** — both cite the orphan major `santi`. Dhp 202 has it
  as a compound member (`santiparaṁ`); Dhp 368 has `santaṁ`, an adjective, not
  the noun. Neither is a clean anchor, and both are single verses outside the
  Appamādavagga. Revisit only after item 1 has settled how verse is handled.

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

Human newcomer review runs in parallel with drafting and does not gate it.
Publishing a surface requires the automated and editorial gates above; reader
evidence is what moves an already-published surface from `provisional` to
`validated`, and it accumulates whenever real readers are available.

So: never delay a source-faithful draft because participants are unavailable,
and never mark a surface `validated` without recorded evidence for the body
now published. Both halves of that hold at once.

Use [the newcomer review workboard](../reviews/README.md) for the cohort, the
public links, and the current tally.

## Restart and Handoff Procedure

On any machine:

```bash
git fetch origin
git switch main
git pull --ff-only
git status --short
python scripts/repo_health.py
```

Read this plan, the short [active roadmap](next-sutta-translation-roadmap.md),
and the [translation workflow](translation-workflow-plan.md). The first
unfinished queue item is **Dhp 21–32**, and it has a precondition; if you do
not want to settle verse now, take **Ud 8.3** and leave item 1 in place.
Create a `codex/` or contributor branch and keep the entire translation packet
together. Before stopping, record completed work, open questions, exact
validation results, and the next action in the surface notes or this plan —
not only in a local terminal or chat.

After merging or pushing to `main`, confirm both GitHub Actions workflows are
green and open the public reader page. Check the title, introduction,
translation, source disclosure, previous/next navigation, and narrow-screen
reflow.

## Definition of Wave Completion

Wave 11 is complete when all five queue items are published, their source
examples pass the strict verifier, the full repository checks and rendered
accessibility suite pass, and the live pages are reachable.

Recorded reader evidence is not part of that definition. It is a separate,
open-ended workstream, and waiting for it would stop the wave indefinitely.

After the last item, run a fresh audit and write a new plan from it. Do not
extend this ranking. Every wave so far has found leverage signals that were
wrong until they were checked against the source — eight of them this round.

# Wave 10 Execution Plan

This is the durable handoff document for the active translation wave. A
contributor should be able to clone the repository on another machine,
confirm the baseline, and continue without relying on chat history.

## Baseline

Snapshot date: 2026-09-13, after AN 8.39.

- 64 governed translation surfaces and 64 generated sutta pages
- 1,157 governed term records
- 635 cited term records: 544 anchored by a translated surface and 91 orphaned
- 9 orphan major terms
- 813 cited example phrases checked: zero partial and zero absent matches
- all generated sutta pages included in the rendered axe accessibility suite

Do not copy these numbers forward. They are a snapshot, and the two commands
below regenerate them in under a minute:

```bash
python scripts/audit_surface_leverage.py --top 20
python scripts/verify_example_sources.py --strict --top 30
```

Two things the counts do not show on their own. SN 12.20 anchored four of its
five orphan signals rather than five: the fifth, `dhammatā`, was a false
citation, and its repaired source (DN 14) is not a translated surface, so that
record stays orphaned. Closing a citation honestly can leave the orphan count
higher than the queue predicted. And `verify_example_sources.py` reaches
bundled root texts — Dhp verse ranges, `an2.1-10`, `sn50.1-12` — by listing
the upstream directory through the GitHub contents API. Where that API is
unreachable, those citations come back `unfetched` rather than verified, and
`--strict` fails on them. That is a network result, not a citation problem;
check whether `https://api.github.com` is reachable before treating it as one.

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
- `dhammatā` does not occur in SN 12.20. The discourse has `dhammaṭṭhitatā`
  and `dhammaniyāmatā` and never the bare word, so the citation was moved to
  DN 14, where `Ayamettha dhammatā` occurs in running text. The strict
  verifier had scored it `inflected` rather than `absent`, because the stem
  sits inside those two longer words.
- `dhammatthiti` cited `dhammatthitā` to SN 12.20, which is neither the
  headword nor the source form and passed only as a prefix of the real word.
  It now cites `ṭhitāva sā dhātu dhammaṭṭhitatā`.
- `kāmesu micchācārā veramaṇī` is not in AN 8.39. The discourse has
  `kāmesumicchācāraṁ pahāya kāmesumicchācārā paṭivirato hoti` and no form of
  `veramaṇī` anywhere. The citation now quotes the running text.
- All of these have the same shape as the earlier `ariyapuggala` and
  `upasamānussati` findings. An `inflected` verdict on a short headword or on
  a precept formula is worth opening by hand; the verifier proves a string
  occurs, not that the governed term does.

## Committed Queue

Work in this order unless a direct reader request takes priority.

1. **AN 11.12, Dutiyamahānāma Sutta** — **complete 2026-08-25.** 367 Pali
   words. Anchors six verified recollection compounds in a portable practice
   for walking, standing, sitting, lying down, working, and family life.
2. **SN 12.20, Paccaya Sutta** — **complete 2026-08-27.** 355 Pali words.
   Anchors the natural-law support layer around conditionality in running
   text. The compressed formula is presented by keeping both of the source's
   full frame statements and naming each elided link once between them; the
   source boundary excludes the vagga closing and mnemonic verse from
   `sn12.20:5.10` onward. The source audit found two bad citations, recorded
   below.
3. **AN 8.39, Abhisanda Sutta** — **complete 2026-09-13.** 268 Pali words.
   Both ranked orphan signals confirmed in the root and anchored:
   `kāmesu-micchācāra` and `surāmeraya-majjapamādaṭṭhāna`. `dāna`, `saraṇa`,
   and `saṅgha` were closed at the same time, each against an exact
   running-text phrase. The source boundary excludes `an8.39:8.2`
   (`Navamaṁ`); the source audit found one bad citation, recorded below.
4. **SN 46.1, Himavanta Sutta** — **not started. This is the next
   translation.** 125 Pali words. One orphan awakening-factor anchor
   (`bojjhaṅga-bhāvanā`) and a compact practice comparison. Verify that
   signal against the root before drafting, as with every other item here.

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

Human newcomer review runs in parallel with drafting and does not gate it.
Publishing a surface requires the automated and editorial gates above; reader
evidence is what moves an already-published surface from `provisional` to
`validated`, and it accumulates whenever real readers are available.

So: never delay a source-faithful draft because participants are unavailable,
and never mark a surface `validated` without recorded evidence for the body
now published. Both halves of that hold at once.

Use [the newcomer review workboard](../reviews/README.md) for the cohort, the
public links, and the current tally. The cohort is the First 12, and its
threshold is five readers and one full read-aloud review per text.

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
[translation workflow](translation-workflow-plan.md). The first unfinished
queue item is **SN 46.1**. Create a `codex/` or contributor branch and keep
the entire translation packet together. Before stopping, record completed work,
open questions, exact validation results, and the next action in the surface
notes or this plan—not only in a local terminal or chat.

After merging or pushing to `main`, confirm both GitHub Actions workflows are
green and open the public reader page. Check the title, introduction,
translation, source disclosure, previous/next navigation, and narrow-screen
reflow.

## Definition of Wave Completion

Three of the four queue items are published. Wave 10 is complete when SN 46.1
joins them, its source examples pass the strict verifier, the full repository
checks and rendered accessibility suite pass, and the live pages are
reachable.

Recorded reader evidence is not part of that definition. It is a separate,
open-ended workstream, and waiting for it would stop the wave indefinitely.

After SN 46.1, run a fresh audit. Do not extend this ranking: it was built
against a 61-surface corpus, three of its four items are done, and every wave
so far has found leverage signals that were wrong until checked against the
source. Replace this plan with the new audit rather than relabeling it.

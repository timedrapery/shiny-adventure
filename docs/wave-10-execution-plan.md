# Wave 10 Execution Plan

**Wave 10 is complete as of 2026-09-13, and this plan is superseded.** The
active handoff document is the
[Wave 11 execution plan](wave-11-execution-plan.md), written from a fresh audit
run the same day.

This page stays as the durable record of Wave 10: its baseline, its source
findings, and the audit procedure that produced its successor. Every number
below is a snapshot and no longer describes the corpus.

## Baseline

Snapshot date: 2026-09-13, at the close of the wave.

- 65 governed translation surfaces and 65 generated sutta pages
- 1,157 governed term records
- 638 cited term records: 548 anchored by a translated surface and 90 orphaned
- 9 orphan major terms
- 816 cited example phrases checked: zero partial and zero absent matches
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
- `bojjhaṅgabhāvanā` is not in SN 46.1. The discourse contains no form of
  `bhāvanā` at all; its running text is `satta bojjhaṅge bhāvento satta
  bojjhaṅge bahulīkaronto`. Two records quoted the compound to it, including
  the orphan record that ranked the text. Both now quote running text.
- All of these have the same shape as the earlier `ariyapuggala` and
  `upasamānussati` findings. An `inflected` verdict on a short headword or on
  a precept formula is worth opening by hand; the verifier proves a string
  occurs, not that the governed term does.
- **The SN 46.1 case extends that rule to `inconclusive`.** A discourse that
  uses peyyāla makes the verifier return `inconclusive` for anything it cannot
  find, which proves nothing either way — so a false citation can sit behind
  that verdict indefinitely. On a short discourse the elision is usually
  readable: check what the peyyāla actually stands for, and the question is
  decidable by hand.

## Committed Queue

All four items are published. This section is now history; it is kept because
the source decisions recorded in it are still the precedents the next wave
works from.

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
4. **SN 46.1, Himavanta Sutta** — **complete 2026-09-13.** 125 Pali words.
   Conduct as the ground the seven awakening factors grow on, in one simile.
   The source boundary excludes `sn46.1:1.14` (`Paṭhamaṁ`); the five elided
   factors are written out because the peyyāla stands for nothing but a tail
   the source prints twice. Its one ranked orphan signal,
   `bojjhaṅga-bhāvanā`, turned out to quote a compound the discourse does not
   contain; the record is anchored here by repair, and the finding is recorded
   below.

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
[translation workflow](translation-workflow-plan.md). There is no unfinished
queue item; run the audit described under
[Running the next audit](#running-the-next-audit) first. Then create a
`codex/` or contributor branch and keep the entire translation packet
together. Before stopping, record completed work,
open questions, exact validation results, and the next action in the surface
notes or this plan—not only in a local terminal or chat.

After merging or pushing to `main`, confirm both GitHub Actions workflows are
green and open the public reader page. Check the title, introduction,
translation, source disclosure, previous/next navigation, and narrow-screen
reflow.

## Wave Completion

All four queue items are published, their source examples pass the strict
verifier, the full repository checks and the rendered accessibility suite
pass, and the live pages are reachable. Wave 10 is complete.

Recorded reader evidence was not part of that definition and is not a gap in
it. It is a separate, open-ended workstream; waiting for it would have stopped
the wave indefinitely. All four surfaces are published as `provisional` and
stay that way until their evidence is recorded.

## Running the Next Audit

Do not pick the next text from the queue above. That ranking was computed
against a 61-surface corpus, every item in it is done, and each of the four
waves so far has found at least one leverage signal that was wrong until it
was checked against the source.

Start here instead:

```bash
python scripts/audit_surface_leverage.py --top 20
python scripts/next_sutta_priority_report.py
```

Then, for each candidate the audit ranks:

1. Fetch the root text and confirm the governed term is in meaningful running
   prose, not a bare list, a peyyāla stub, a collection heading, or a
   related-but-different compound.
2. Read the segment the citation quotes. Both `inflected` and `inconclusive`
   verdicts hide false citations, and six have been found this way so far.
3. Only then commit to a queue position, and write the new plan from the audit
   rather than relabeling this one.

The **Packet Required for Every Sutta** and **Validation Gates** sections above
carry forward unchanged, whatever the next audit selects.

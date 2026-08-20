# Next Sutta Translation Roadmap

This shorter note now tracks the near-term queue extracted from
[next-suttas-roadmap.md](next-suttas-roadmap.md).

Use that full roadmap as the source of truth for:

- the ranked order
- the live citation audit
- the doctrinal-cluster rationale for each choice
- the post-translation lexicon update rules

## Completed Surfaces (42 total)

### Wave 1: Dense Existing Support
- `SN 12.2` Paṭiccasamuppāda-vibhaṅga Sutta
- `SN 56.11` Dhammacakkappavattana Sutta
- `DN 2` Sāmaññaphala Sutta
- `MN 2` Sabbāsava Sutta
- `MN 9` Sammādiṭṭhi Sutta

### Wave 2: Distinction-Forcing Surfaces
- `MN 44` Cūḷavedalla Sutta
- `MN 64` Mahāmālukya Sutta
- `DN 15` Mahānidāna Sutta
- `SN 22.89` Khemaka Sutta
- `SN 22.48` Khandha Sutta

### Wave 3: Strategic Expansion
- `MN 7` Vattha Sutta
- `SN 36.6` Salla Sutta
- `SN 46.51` Āhāra Sutta
- `MN 39` Mahā-Assapura Sutta
- `AN 10.60` Girimānanda Sutta

### Wave 4: Beyond the Original Roadmap
- `AN 4.113` Patodasutta
- `AN 11.9` Saddhāsutta
- `SN 12.23` Upanisā Sutta
- `SN 35.28` Āditta Sutta
- `MN 38` Mahātaṇhāsaṅkhaya Sutta
- `MN 26` Pāsarāsi Sutta

### Wave 5: Source-Closing and Gap-Filling
- `MN 22` Alagaddūpama Sutta
- `SN 12.15` Kaccānagotta Sutta
- `AN 3.65` Kesamutta Sutta (Kālāma Sutta)
- `MN 63` Cūḷamālukya Sutta

### Wave 6: Ungoverned Major Families
- `SN 12.11` Āhāra Sutta (The Four Nutriments)
- `SN 55.5` Dutiyasāriputta Sutta (The Stream and the Stream-Enterer)
- `AN 6.63` Nibbedhika Sutta (The Penetrating Exposition)
- `SN 12.61` Assutavā Sutta (The Body and the Mind)
- `MN 11` Cūḷasīhanāda Sutta (The Shorter Lion's Roar)

### Outside the Wave Sequence
- `MN 61` Ambalaṭṭhikarāhulovāda Sutta (Advice to Rāhula on Lying) —
  requested directly rather than drawn from a wave audit. Control surface for
  the threefold before/during/after reflection formula on bodily, verbal, and
  mental action, and for the water-vessel and war-elephant similes. Reader
  placement is set 3.

### Pre-existing Surfaces (governed before the roadmap was active)
- `MN 1` Mūlapariyāya Sutta
- `MN 10` Satipaṭṭhāna Sutta
- `MN 18` Madhupindika Sutta
- `MN 19` Dvedhāvitakka Sutta
- `MN 99` Subha Sutta
- `MN 117` Mahācattārīsaka Sutta
- `MN 118` Ānāpānasati Sutta
- `MN 137` Saḷāyatanavibhaṅga Sutta
- `MN 141` Saccavibhaṅga Sutta
- `MN 148` Chachakka Sutta
- `SN 12.2` (see Wave 1)
- `SN 22.59` Anattalakkhaṇa Sutta

## Current Active Queue

**Wave 7 is drafted.** Audited 2026-08-20; the full ranking and its two
method corrections are in
[next-suttas-roadmap.md](next-suttas-roadmap.md). Rerun it with
`python scripts/audit_surface_leverage.py` rather than recomputing by hand.

Order:

1. `MN 43` -- the emptiness / signless / wishless cluster is the only governed
   cluster with no running text behind any of its thirteen terms
2. `SN 51.13` -- three orphan majors (`chanda`, `iddhipada`, `vimamsa`) in
   242 Pali words
3. `MN 70` -- `cetovimutti` and `pannavimutti`; touches three governed
   clusters
4. `Iti 44` -- the two nibbana elements; consummation cluster is 69% dark
5. `SN 12.43` -- completes the `-samudaya` formula family in 183 words

Two things to settle before drafting. Five candidates have uncached root texts
so their lengths are unverified. And the enumeration-stub track --
`SN 45.171` / `.172` / `.174` and `AN 7.11`, about 120 Pali words covering
21 dark terms -- is cheaper than anything in the list above but should become
formula records rather than translation surfaces.

### Wave 6: Ungoverned Major Families (complete)

Audited 2026-08-19 against the 36-surface, 1145-term state. See
[next-suttas-roadmap.md](next-suttas-roadmap.md) for the full rationale, the
per-text leverage signals, and the method note on why raw citation count was
rejected as the ranking basis.

1. ~~`SN 12.11` Āhāra Sutta~~ — **complete**. Six orphan major entries, the
   four-nutriments family; also closed the gap where the `ahara` headword
   default had no surface because `SN 46.51` overrides it locally. See
   [SN 12.11](translations/sn12-11-ahara-sutta.md) and its
   [notes](translations/sn12-11-ahara-sutta-notes.md).
2. ~~`SN 55.5`~~ — **complete**. Anchors `sotapanna` and `sotapatti`. The
   audit's claim of five orphan majors turned out to rest on bad citation
   data; see the surface notes and the citation-integrity finding in
   [translation-workflow-plan.md](translation-workflow-plan.md).
3. ~~`AN 6.63` Nibbedhika Sutta~~ — **complete**. Gives `kamma` its first
   translation surface, including the line that defines action as intention.
4. ~~`SN 12.61`~~ — **complete**. Anchors the four conditionality formula
   records. Note it does not contain `idappaccayata`, contrary to the
   original leverage signal.
5. ~~`MN 11` Cūḷasīhanāda Sutta~~ — **complete**. Anchors the four-fold
   `upadana` enumeration, and surfaced that the four compounds are not
   consistent with each other. See the surface notes.

**Wave 6 is complete.** All five surfaces are translated.

### What Wave 6 Says About Running The Next Audit

Four of the five leverage signals in the Wave 6 ranking turned out to be wrong
when checked against the source texts:

- SN 55.5 was ranked for five orphan majors and anchors two. `sakadagami`,
  `anagami`, and `phala` cited it for Pali that is not in it.
- AN 6.63 was said to anchor `phala` and `papa`. It uses `vipaka` throughout
  and contains no `pap` at all.
- SN 12.61 was said to anchor `idappaccayata`. The word does not occur in it.

All three traced to `example_phrases` citing suttas that did not contain the
quoted Pali. Those citations have since been repaired and
`scripts/verify_example_sources.py` now reports zero `absent`, so an audit run
today rests on better data than Wave 6's did.

Two method points worth carrying forward:

- Rank by **orphan count**, not citation volume. Raw citation weight ranked
  DN 22 first, but twelve of its fifteen citing entries are already anchored
  by MN 10, so it would mostly re-govern vocabulary already demonstrated.
- **Verify the leverage signal against the source before committing to a
  queue position.** Every one of the errors above would have been caught by
  fetching the sutta and grepping for the term.

The organizing idea for this wave is different from Wave 5. Wave 5 closed
source gaps for material already cited in existing surfaces. Wave 6 targets
**orphan** entries: governed records whose sutta anchors are all untranslated,
so nothing in the outward-facing corpus demonstrates their policy in running
text.

## Operating Note

For each of these texts:

1. review the governing headwords, compounds, and formula records together
2. draft the main translation and the companion note file in one pass
3. add new phrase records only where repetition or drift risk justifies them
4. refresh any affected surface brief or map
5. run the full verification suite before treating the translation as stable

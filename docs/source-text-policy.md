# Source Text Policy

Decided by the owner on 2026-11-10.

## The rule

This project does not use SuttaCentral content, except where its use is
authorized.

That means:

- no fetching, caching, or reading of SuttaCentral's Pali root texts or its
  translations, by any script or by hand during drafting;
- no comparison against SuttaCentral translations (Sujato's or anyone else's);
- no links to suttacentral.net from the reader.

"Authorized" means one of two things, and either must be recorded in this file
before the use begins:

1. written permission from SuttaCentral for the specific use, or
2. a SuttaCentral publication whose own license statement carries no request
   against the use in question.

## Why

SuttaCentral's texts are dedicated to the public domain through CC0, so this
is not a legal restriction. It is a request, and the project honours it.

The publication records in SuttaCentral's data repository
(`bilara-data/_publication.json`) carry this sentence on 45 of their 143
publications, including the Mahāsaṅgīti Pali root text (`scpub38`) and all of
Bhikkhu Sujato's English translations:

> The translator respectfully requests that any use be in accordance with the
> values and principles of the Buddhist community. In particular, please do
> not use this work in AI training datasets, for the development of any AI
> model or algorithm, or in any AI-derived technologies.

This project is drafted with AI assistance, so that request applies to it.

## What the project uses instead

The source checks read the **Chaṭṭha Saṅgāyana Tipiṭaka** of the Vipassana
Research Institute, from its published XML at
<https://github.com/VipassanaTech/tipitaka-xml>. Its terms, from that
repository's README:

> These files are made freely available for non-commercial use. Please
> attribute Vipassana Research Institute when incorporating these files into
> your projects.

How the project meets them:

- **Non-commercial.** The project is free and has no commercial use.
- **Attribution.** Every reader page names the edition and the book its text
  comes from, and links to <https://tipitaka.org/romn/>.
- **Not redistributed.** The VRI files are never committed. Scripts read them
  from a gitignored cache (`.vri-cache/`) or from a local clone named by
  `$VRI_TIPITAKA_DIR`.

The VRI README asks nothing about AI use. No other VRI terms page could be
checked from the session that made this change, because tipitaka.org was not
reachable from it. Check <https://tipitaka.org/> before relying on that.

The Mahāsaṅgīti was itself built on the Chaṭṭha Saṅgāyana, so readings agree
closely. Spelling differs in places (VRI writes `ṃ` where the Mahāsaṅgīti
writes `ṁ`); the checks fold those differences.

## Where the edition is read

- `scripts/vri_source.py` locates a cited discourse in the VRI books and maps
  the familiar citation numbers onto VRI's divisions, recording each place
  where VRI numbers differently.
- `scripts/verify_example_sources.py` checks every term record's quoted Pali
  against it. Digests of the passages read are pinned in
  `reviews/source-pins.json`.
- `scripts/audit_surface_leverage.py` and `scripts/triage_citation_stems.py`
  take word counts and text from it, without downloading anything.

Citation numbering (`MN 10`, `SN 12.61`, `AN 3.65`) is kept. It is a scholarly
reference convention used across editions and translations, not SuttaCentral
content.

## The record before this decision

The 80 translations published before 2026-11-10 were drafted against the
Mahāsaṅgīti, and their editorial notes and review records say so. That history
is left as written, because it is what happened. From 2026-11-10 source checks
run against the VRI edition. When the 2026-11-10 switch was made, the citation
check gave 593 exact matches, 183 qualified, 0 failed, and 72 inconclusive
because VRI abridges those passages, against 601, 168, 0, and 79 on the old
source (27 of which could not be fetched at all).

A human source-fidelity sign-off recorded in
`reviews/newcomer-review-ledger.json` was given against the text named in its
evidence. Re-checking a translation against the VRI edition is new review
work, not a transfer of the old sign-off.

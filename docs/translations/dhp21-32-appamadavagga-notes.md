# Dhp 21-32 Translation Notes

This document is the companion rationale for
[Dhp 21-32: Appamādavagga](dhp21-32-appamadavagga.md). The main translation is
the primary study surface; this file records debated translation choices,
source-audit calls, and edition notes that govern it.

## Source Base

- Primary source: the Pali text of Dhp 21-32 as segmented in SuttaCentral's
  Bilara data (`dhp21:0.1` to `dhp32:5`), fetched from the upstream Bilara
  root.
- Control surfaces: the `appamāda`, `amatapada`, `amata`, `jhāna`,
  `jhāyati`, `yogakkhema`, and `nibbāna` records; SN 1.1 and SN 36.6 for
  existing verse register.
- Working method: twelve four-line or six-line verses, each translated as one
  stanza and kept line for line where English allows.

## Dhammapada Framing

This is the repository's first Dhammapada surface and its first surface that is
verse from start to finish. These decisions hold for later Dhammapada chapters
unless a chapter's notes record a reason to differ.

- **One surface per chapter (`vagga`).** The surface is titled with the verse
  range and the Pali chapter name, `Dhp 21-32: Appamādavagga`, and the reader
  page uses a plain English title. The range uses a plain hyphen because it is
  also the SuttaCentral identifier (`dhp21-32`).
- **Verse numbers are kept.** Dhammapada verses are cited by number, so each
  stanza opens with its number in bold (`**21**`). The reader shows the number
  in the margin.
- **Lines are kept.** Each Pali line is one English line where the syntax
  allows; the English may reorder lines within a stanza when the Pali order
  would make a broken English sentence, as in verses 26 and 31.
- **Commentary story titles are excluded.** The root text carries a story
  title (`vatthu`) above nine of the twelve verses, such as `Sāmāvatīvatthu`
  and `Kumbaghosakaseṭṭhivatthu`. They come from the later commentary, which
  tells the occasion for each verse, and are not part of the verses. They are
  not translated or shown.
- **The chapter close is kept.** `Appamādavaggo dutiyo` is rendered `The
  second chapter, on heedfulness, is finished.`, matching the closing lines of
  the other surfaces.

### How verse is displayed

Verse in this repository is written one stanza per paragraph and one line per
verse line, under a heading that starts with `Verse` or `Verses`. Plain
Markdown joins those lines into a single paragraph, so the reader generator
marks each multi-line paragraph in such a section as verse and the stylesheet
keeps its line breaks. The same rule now applies to the closing verses of SN
36.6, SN 22.22, Iti 44, and Iti 49, which had been displaying as run-on
prose.

## Governing Decisions

- `appamāda` remains `heedfulness`, `pamāda` `heedlessness`, `appamatta`
  `heedful`, and `pamatta` `heedless`.
- `Appamādo amatapadaṁ, pamādo maccuno padaṁ` is `Heedfulness is the path to
  the deathless; heedlessness is the path to death.`, following the
  `amatapada` record. The `appamāda` record's two examples, which read `the
  deathless path` and `the path of death`, now match, and the formula
  agreement baseline entry for this line is removed.
- `jhāyin` (verse 23) and `jhāyanto` (verse 27) are `those who practice the
  mental themes` and `practices the mental themes`. The `jhāyati` record
  discourages `meditate`, and its default `think like this` needs an object
  that these verses do not supply; tying the word to `jhāna` as `mental
  theme` keeps it inside the governed family. This is a document-local
  rendering.
- `yogakkhemaṁ anuttaraṁ` is `the unsurpassed security from the yoke`,
  following the `yogakkhema` record.
- `yasa` keeps its governed `fame` (verse 24).
- `sukha` keeps `satisfaction` (verse 27), and `paññā` keeps `discernment` in
  `the tower of discernment` (verse 28).
- `saṁyojana` keeps `fetter` (verse 31).
- `bhayadassī` is `who sees fear`, keeping `bhaya` as governed `fear`.
- `Maghavā` (verse 30) is kept as a name. It is a name of Sakka, chief of the
  devas; the reader intro says so, and the verse does not.
- `medhāvī` is `the intelligent` and `sumedhasa` `the person of good
  understanding`. `dhīra` is `the steadfast`. These are document-local; no
  record governs them.

## Practice Clarifications

- Heedfulness here is not anxiety or vigilance for its own sake. The chapter
  presents it as the one quality that keeps practice going: effort, care,
  restraint, and returning again and again.
- Verse 21's `the heedless are as if already dead` is a figure, not a claim
  about rebirth. The heedful `do not die` in the sense that they are on the
  path to the deathless.

## Readability Review

- Standard: `plain-english-v1`
- Status: `provisional`
- Source check: drafted against the segmented Pali; every verse line from
  `dhp21:1` to `dhp32:4` is rendered, and the chapter close `dhp32:5`.
- Automated governance review: complete; the full repository suite passed on
  2026-11-09.
- Human read-aloud usability review: optional, not recorded.
- Newcomer comprehension review: optional, not recorded.

## Wave 11 Role

Dhp 21-32 is the first Wave 11 queue item. Its precondition, settling how verse
is set, titled, and numbered, is settled above by explicit editorial decision
on 2026-11-09. It anchors the orphan major `appamāda` and the record
`amatapada`.

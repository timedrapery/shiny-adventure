# SN 55.5 Translation Notes

This document is the companion rationale for
[SN 55.5: Dutiyasāriputta Sutta](sn55-5-dutiyasariputta-sutta.md). The main
translation is the primary study surface; this file records debated translation
choices, source-audit calls, and edition notes that govern it.

## Source Base

- Primary source: the Pali text of SN 55.5 as segmented in SuttaCentral's
  Bilara data (22 segments).
- Control surface: the repository's current term policy, especially
  `sotāpatti`, `sotāpanna`, `sappurisa`, `yoniso manasikāra`, and the eight
  path factors, together with the `…ti vuccati` frame governed in SN 12.15.
- Working method: the discourse was governed as three linked definitions —
  what leads to stream-entry, what the stream is, and who counts as having
  entered it — rather than as three separate question-and-answer exchanges.

## Governing Decisions

- The `…ti vuccati` frame is rendered `they speak of 'X, X.'`, reusing the
  wording already governed in SN 12.15 rather than re-solving it. The doubled
  term is kept, because the doubling is what marks the phrase as a quoted
  expression being examined.
- `sappurisasaṁseva` is rendered `keeping company with good persons`.
  `Sappurisa` is governed as `good person`; the `saṁseva` half is ungoverned
  and is given a plain verb phrase rather than the noun-heavy `association
  with`, under rule 6 of the plain-English standard.
- `saddhammassavana` is rendered `hearing the true Dhamma`. Neither half is
  governed.
- `dhammānudhammappaṭipatti` is rendered `practicing in line with the Dhamma`.
  Ungoverned, and deliberately plain: the phrase means practising the teaching
  in a way that accords with it, and the longer literal renderings do not say
  that any more precisely in English.
- `samannāgato` is rendered `anyone who has`, not `endowed with`. The point is
  possession of the path, and `endowed with` adds a formality the Pali does not
  carry.
- `svāyaṁ āyasmā evaṁnāmo evaṅgotto` is rendered `this venerable one, with such
  a name, from such a family`. The idiom is a placeholder for naming an actual
  person, and the translation keeps it as a placeholder rather than resolving
  it.

## Re-audit Calls

- **The lexicon cites this sutta for material it does not contain.** Five major
  records carry `example_phrases` sourced to SN 55.5, and the source text
  supports only two of them. SN 55.5 contains `sotāpanno`,
  `sotāpattiyaṅgaṁ` / `sotāpattiyaṅgan`, and `maggo` / `maggena`. It contains
  no `sakadāgām`, no `anāgām`, and no `phal` in any form.
  - `sakadagami` cites `sakadāgāmimagga` here. Not present.
  - `anagami` cites `anāgāmimagga` here. Not present.
  - `phala` cites `sotāpattiphala` here. Not present.
  - `sotapatti` cites `sotāpattiphala` here. Not present. Its second example
    cites `sotāpattiyaṅgāni`; the text has the singular `sotāpattiyaṅgaṁ`.
  - `sotapanna` cites `sotāpannassa`; the text has `sotāpanno`.

  The two inflection mismatches are corrected in this pass because the correct
  form is verifiable from the source. The three phrases that are absent
  entirely are left in place and flagged rather than deleted, because choosing
  a replacement source is an editorial decision and inventing one would repeat
  the original error.
- The same audit found that `phala`'s other citation is also wrong: it cites
  `kammassa phalaṁ` from AN 6.63, and AN 6.63 uses `vipāka` throughout, never
  `phala`. `phala` therefore currently has no verified citation at all.
- This class of error is not detectable by any current check. The repository
  verifies that `example_phrases` *have* a source, but nothing verifies that
  the cited source actually contains the cited Pali. That gap is worth closing
  with tooling rather than by hand.
- The lexicon governs `sota` as `ear`. The `soto` of this discourse is an
  unrelated homonym meaning `stream`. If `sota` in the stream sense ever needs
  a record, it must be a separate entry rather than a context rule on the
  hearing faculty.
- `sotāpattiyaṅga` itself has no record, despite being the subject of the first
  third of this discourse. It is a candidate for a minor entry.

## Practice Clarifications

- The discourse defines the stream as the path itself, not as a state reached
  by the path. That is why the third answer can define a stream-enterer purely
  as someone who has the eightfold path, with no reference to attainment
  levels or to what has been abandoned.
- The four factors are ordered as a sequence that can actually be followed:
  find good company, hear the teaching, attend to it wisely, then practise in
  line with it. Nothing in the list is inward-only, and the first item is
  social.

## Readability Review

- Standard: `plain-english-v1`
- Status: `provisional`
- Review result: the Buddha and Sāriputta exchange short, real questions and
  answers; the repeated definitions are preserved so the practical sequence
  can be heard and remembered.
- Automated governance review: complete; the full repository verification
  suite passed on 2026-08-22.
- Human read-aloud usability review: pending.
- Newcomer comprehension review: pending.

This surface remains provisional until the human reviews are recorded.

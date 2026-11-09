# AN 5.14 Translation Notes

This document is the companion rationale for
[AN 5.14: Vitthata Sutta](an5-14-vitthata-sutta.md). The main translation is
the primary study surface; this file records debated translation choices,
source-audit calls, and edition notes that govern it.

## Source Base

- Primary source: the Pali text of AN 5.14 as segmented in SuttaCentral's
  Bilara data (`an5.14:1.1` to `an5.14:6.5`), fetched from the upstream
  Bilara root and matching its hash in `reviews/source-pins.json`.
- Control surface: SN 48.10, which defines the five faculties in the same
  words. Every definition here is copied from it, including the Tathāgata's
  epithets and the four mental themes, so that the faculties and the
  strengths read as the same qualities under two names.
- Working method: the discourse names the five strengths, then defines each
  one in a fixed frame: `And what is ...? A noble disciple ... This is
  called ...`. The frame is kept for all five.

## Governing Decisions

- `bala` is `strength`, its governed default; `power` is the record's
  alternate and is not used. `pañca balāni` is `five strengths`.
- The five names follow their records: `saddhābala` `confidence strength`,
  `vīriyabala` `energy strength`, `satibala` `remembering strength`,
  `samādhibala` `unification strength`, and `paññābala` `discernment
  strength`. `samādhibala`'s default is `strength of unification`; the surface
  uses the record's listed alternate `unification strength` so the five names
  stay parallel.
- `saddahati tathāgatassa bodhiṁ` is `place confidence in the awakening of the
  Tathāgata`, and the epithets follow SN 48.10. DN 2 and MN 122 use a slightly
  different epithet wording (`holy`, `fit for training`); the sister text
  governs here.
- The energy definition (`āraddhavīriyo viharati ... anikkhittadhuro
  kusalesu dhammesu`) is SN 48.10's first sentence for the faculty of energy.
  SN 48.10 goes on to the four right efforts; AN 5.14 does not, and the
  translation does not add them.
- The remembering definition (`satimā hoti paramena satinepakkena
  samannāgato, cirakatampi cirabhāsitampi saritā anussaritā`) is SN 48.10's
  first sentence for the faculty of remembering. AN 5.14 does not add the
  four foundations.
- The four mental themes follow SN 48.10, with `sukha` as `satisfaction`
  throughout. MN 19 and MN 122 use `ease` in the third and fourth themes; the
  sister text governs here.
- SN 48.10 introduces the unification faculty with `vossaggārammaṇaṁ karitvā
  labhati samādhiṁ`. AN 5.14 goes straight to the mental themes, and the
  translation does too.
- The discernment definition (`udayatthagāminiyā paññāya samannāgato ariyāya
  nibbedhikāya sammā dukkhakkhayagāminiyā`) is SN 48.10's first sentence.
  AN 5.14 does not add the four truths.

## Re-audit Calls

- The source has no setting; the discourse opens with `bhikkhave`.
- `Catutthaṁ` is rendered `The fourth discourse is finished.`
- The source writes out the four mental themes in full. There is no peyyāla.

## Practice Clarifications

- The strengths are not five new things. SN 48.10 defines the five faculties
  in the same words. The traditional explanation, which the discourse itself
  does not state, is that the strengths are the faculties once their
  opposites can no longer shake them.
- Each strength has a practical test. Confidence is confidence in an
  awakening that actually happened; energy is not putting down the burden;
  remembering is recalling what was done and said long ago; unification is
  the mental themes; discernment leads to arising and passing away and to the
  wearing away of dissatisfaction.

## Readability Review

- Standard: `plain-english-v1`
- Status: `provisional`
- Source check: drafted against the pinned segmented Pali; every segment from
  `an5.14:1.1` to `an5.14:6.5` is rendered.
- Automated governance review: complete; the full repository suite passed on
  2026-11-09.
- Human read-aloud usability review: optional, not recorded.
- Newcomer comprehension review: optional, not recorded.

## Wave 12 Role

AN 5.14 is the second Wave 12 queue item. It anchors the orphan major `bala`,
which Wave 11 could not reach through SN 50.1, and gives the five strength
records and `pañca bala` their first verified source.

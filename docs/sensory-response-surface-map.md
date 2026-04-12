# Sensory-Response Surface Map

## Purpose

This document defines the current governed surface for the linked MN 137 /
MN 148 sensory-response family.

The goal is to keep the household / renunciation feeling categories and the
trained / untrained feeling-response formulas under live repository policy
rather than leaving them to translation-note memory.

## Current Scope

The current governed surface includes:

- the MN 137 household-tied and renunciation-tied gladness labels
- the MN 137 household-tied and renunciation-tied distress labels
- the MN 137 household-tied and renunciation-tied dynamic-balance labels
- the MN 137 staged replacement line
- the MN 137 closing three-establishments-of-sati line
- the MN 148 pleasant-feeling untrained and trained response lines
- the MN 148 painful-feeling untrained and trained response lines
- the MN 148 mixed-feeling undiscerned and discerned response lines

These lines and category labels are controlled through live records in
`terms/` and audited together by
`python scripts/sensory_response_surface_report.py`.

## Operating Rule

When a feeling-domain line is now functioning as a repeated control surface
across multiple translation documents:

1. encode it in `terms/` as a governed live record
2. align the translation documents with that record
3. audit the shared surface directly

Do not keep a repeated feeling-response formula aligned only through
translation notes.

## Current Control Records

- `gehasita-somanassa`
- `nekkhammasita-somanassa`
- `gehasita-domanassa`
- `nekkhammasita-domanassa`
- `gehasita-upekkha`
- `nekkhammasita-upekkha`
- `mn137-supported-by-this-give-up-that`
- `mn137-three-establishments-of-sati`
- `sukhaya-vedanaya-phuttho-samano-abhinandati-abhivadati-ajjhosaya-titthati`
- `mn148-pleasant-feeling-trained-response`
- `mn148-painful-feeling-untrained-response`
- `mn148-painful-feeling-trained-response`
- `mn148-mixed-feeling-undiscerned-response`
- `vedanaya-samudayanca-atthangamanca-assadanca-adinavanca-nissarananca-yathabhutam-pajanati`

## Translation-Surface Rule

MN 137 and MN 148 should stay aligned on the household / renunciation and
trained / untrained response families unless a recorded local reason explicitly
governs a divergence.

If a future feeling-domain translation begins reusing more of these same
families, add it to the audit surface rather than re-solving the phrasing
locally.

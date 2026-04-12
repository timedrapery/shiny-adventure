# Practice-Text Surface Map

## Purpose

This document defines the current governed surface for the shared MN 10 / MN 118
practice-text family.

The goal is to keep repeated high-impact practice lines under live repository
policy rather than leaving them to translator memory or note-file prose.

## Current Scope

The current governed surface includes:

- the MN 10 direct-path opening
- the satipaṭṭhāna practical qualifier line
- the body-branch internal / external refrain line
- the body-branch anchor / non-appropriation closing line
- the shared breathing-side remembrance line in MN 10 and MN 118
- the shared whole-body training line in MN 10 and MN 118
- the shared body-conditioner training line in MN 10 and MN 118

These lines are controlled through live records in `terms/` and audited
together by `python scripts/practice_text_surface_report.py`.

## Operating Rule

When a practice line is now functioning as a shared control surface across more
than one translation document:

1. encode it in `terms/` as a governed live record
2. align the translation documents with that record
3. audit the shared surface directly

Do not keep a repeated practice formula aligned only through translation notes.

## Current Control Records

- `mn10-direct-path-opening`
- `mn10-satipatthana-qualifier`
- `mn10-kayanupassi-internal-external`
- `mn10-kayo-anchor-nonappropriation`
- `mn118-breathing-remembrance-line`
- `mn118-whole-body-training`
- `mn118-body-conditioner-training`

## Translation-Surface Rule

MN 10 and MN 118 should stay aligned on the shared breathing-side control lines
unless a recorded local reason explicitly governs a divergence.

If a future practice text begins reusing more of these same lines, add it to
the audit surface rather than re-solving the phrase locally.

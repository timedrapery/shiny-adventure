# OSF Editorial Authority

## Purpose

This document defines the editorial authority order for the Open Sangha
Foundation translation dataset.

The point is to make translation decisions auditable and internally coherent.
This repository should not behave like a pile of interesting source notes. It
should behave like a governed editorial system.

## Authority Order

When sources disagree, use this order:

1. OSF house style as explicitly recorded in this repository
2. Dhammarato and Buddhadasa Bhikkhu together, where they clearly align
3. Dhammarato, when he is the clearest guide for practical instruction,
   meditation language, contemporary tone, and OSF teaching vocabulary
4. Buddhadasa Bhikkhu, when he is the clearest guide for dependent arising,
   voidness, not-self, natural-law framing, and here-now liberation language
5. Named OSF publications adopted into the repository house style, including
   *What Is And Is Not The Path*, when they clarify usage without overriding
   canonical repo spellings
6. Existing repository defaults that do not conflict with the above
7. Secondary source profiles such as Punnaji, the OSF glossary, and other
   local materials

## Primary Authorities

### Dhammarato

Dhammarato is a primary OSF authority for:

- practical teaching tone
- path language in contemporary English
- meditation and mind-training vocabulary
- here-now practice framing
- anti-scholastic and anti-mystification language

### Buddhadasa Bhikkhu

Buddhadasa Bhikkhu is a primary OSF authority for:

- dependent arising and conditionality
- `idappaccayata`
- `sunnata` and void-mind language
- practical readings of `jati`, `bhava`, and `upadana`
- `nibbana` as coolness and immediate relevance
- ordinary versus supramundane teaching distinctions

## Secondary Authorities

Secondary profiles can inform alternates, notes, and source-specific context
rules, but they do not override OSF defaults unless the repository makes an
explicit editorial decision.

Examples:

- Punnaji
- OSF glossary
- Dhammarato chanting manual when the issue is broader doctrine rather than
  liturgical vocabulary

## Rule For Preferred Translation Changes

Change `preferred_translation` when:

1. Dhammarato and Buddhadasa clearly align, or
2. one of them is plainly primary for that domain and there is no stronger
   conflict from the other, and
3. the rendering is reusable across OSF translation and teaching contexts,
   not just a one-off slogan or heading

Otherwise:

- keep the current default
- record the source-backed rendering in `alternative_translations`,
  `context_rules`, or `notes`

## Rule For Notes

When a term is materially shaped by Dhammarato or Buddhadasa:

- say so directly in `notes`
- treat that source as primary guidance, not just background influence
- remove stale wording that suggests older house defaults are still primary
  when they no longer are

## Current OSF Direction

At the current stage of the project:

- Dhammarato is setting the main practical house language
- Buddhadasa is setting much of the doctrinal and dependent-arising frame
- OSF publications such as *What Is And Is Not The Path* can refine term
  definitions and usage while the repo keeps its own normalized spellings
- the repository should increasingly read like a coherent Dhammarato /
  Buddhadasa-line editorial system rather than a neutral aggregator of many
  Buddhist English vocabularies

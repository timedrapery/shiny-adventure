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
2. OSF house materials at the publication level, including the OSF glossary and
   named OSF books such as *What Is And Is Not The Path* and the Dhammarato
   quotes book
3. Dhammarato, as the primary living OSF lineage voice for practical
   instruction, meditation language, contemporary tone, and OSF teaching
   vocabulary
4. Buddhadasa Bhikkhu, as the foundational lineage authority for dependent
   arising, voidness, not-self, natural-law framing, and here-now liberation
   language
5. Existing repository defaults that do not conflict with the above
6. First named external practical checkpoints such as Punnaji and the
   Hillside / Ñāṇamoli / Path Press stream
7. Other outside-source materials when needed

## Primary OSF Authorities

### OSF House Materials

The following sit at the same editorial level inside OSF house authority:

- the OSF glossary
- named OSF publications, including *What Is And Is Not The Path* and the
  Dhammarato quotes book
- explicit house-style decisions already recorded in this repository

These are internal OSF sources, not outside-source profiles.

### Dhammarato

Dhammarato is a primary OSF authority immediately under OSF house materials
and is especially authoritative for:

- practical teaching tone
- path language in contemporary English
- meditation and mind-training vocabulary
- here-now practice framing
- anti-scholastic and anti-mystification language

### Buddhadasa Bhikkhu

Buddhadasa Bhikkhu is a primary OSF authority immediately under Dhammarato and
is especially authoritative for:

- dependent arising and conditionality
- `idappaccayata`
- `sunnata` and void-mind language
- practical readings of `jati`, `bhava`, and `upadana`
- `nibbana` as coolness and immediate relevance
- ordinary versus supramundane teaching distinctions

## Outside Sources

Outside-source profiles can inform alternates, notes, and source-specific
context rules, but they do not override OSF defaults unless the repository
makes an explicit editorial decision.

Examples:

- Punnaji
- Hillside / Ñāṇamoli / Path Press
- other outside-source profiles when a term needs them

## Rule For Preferred Translation Changes

Change `preferred_translation` when:

1. an OSF house material clearly supports the rendering, or
2. Dhammarato is plainly primary for that domain and there is no stronger
   conflict from OSF house material, or
3. Buddhadasa is plainly primary for that domain and there is no stronger
   conflict from OSF house material or Dhammarato, and
4. the rendering is reusable across OSF translation and teaching contexts,
   not just a one-off slogan or heading

Otherwise:

- keep the current default
- record the source-backed rendering in `alternative_translations`,
  `context_rules`, or `notes`

## Rule For Notes

When a term is materially shaped by OSF house material, Dhammarato, or
Buddhadasa:

- say so directly in `notes`
- treat that source as primary guidance, not just background influence
- remove stale wording that suggests older house defaults are still primary
  when they no longer are

## Current OSF Direction

At the current stage of the project:

- OSF house materials such as the OSF glossary and OSF books sit at the top of
  the internal authority stack
- Dhammarato is the next practical lineage authority
- Buddhadasa is the next doctrinal lineage authority
- the repository should increasingly read like a coherent Dhammarato /
  Buddhadasa-line editorial system rather than a neutral aggregator of many
  Buddhist English vocabularies

# Next Suttas Roadmap

## Purpose

This roadmap ranks the next untranslated suttas that would strengthen the live
lexicon most efficiently.

The point is not to choose the most famous discourses in the abstract. The
point is to choose texts that:

- reuse already-governed doctrinal clusters
- sharpen near-neighbor distinctions that still carry drift risk
- stabilize repeated formulas that should not be re-solved locally
- expose the next useful headword, compound, or formula refinements

## Audit Basis

This ranking is based on the current repository state:

- `python scripts/repo_health.py --top 10` reports no draft queue, no weak
  major entries, no major metadata gaps, and no translation collisions.
- `python scripts/audit_term_coverage.py --top 15` reports no missing
  families and no partial-family backlog.
- the repo already has stable translation surfaces for DN 2, MN 1, MN 2, MN 9,
  MN 10, MN 18, MN 19, MN 44, MN 64, MN 99, MN 117, MN 118, MN 137, MN 141,
  MN 148, SN 12.2, SN 22.59, and SN 56.11
- the next gains therefore come from leverage inside mature clusters rather
  than from emergency term backfill

The ranking weights four factors:

1. live `sutta_references` density across the current lexicon
2. direct pressure on policy-bearing major entries
3. formula and sequence density that can stabilize translator-facing control
   language
4. ability to reduce future drift across clusters already under governance

No new blocking major-entry scaffolds were needed for this roadmap. The live
policy surface is already strong enough to support the next translation wave.

## Ranked Roadmap

### 1. SN 12.2: Paṭiccasamuppāda-vibhaṅga Sutta

- Leverage signal: `59` live citations, `24` from major entries.
- Strengthens: dependent arising, `paccaya`, `nirodha`, `vedanā -> taṇhā ->
  upādāna`, `nāmarūpa`, `viññāṇa`, and the eleven forward-link formulas.
- Likely lexicon pressure: keep `condition` from drifting into `cause`, keep
  `birth` distinct from `rebirth`, and confirm that link-level formula records
  inherit the headword policy cleanly.

### 2. DN 2: Sāmaññaphala Sutta

- Leverage signal: `35` live citations, `21` from major entries.
- Strengthens: `nīvaraṇa`, `jhāna`, training-sequence prose, practical
  abandoning formulas, and release-side stock declarations.
- Likely lexicon pressure: keep the hindrance-clearing sequence stable, hold
  `samādhi`, `jhāna`, `ekaggatā`, and first-jhāna pair language together, and
  prevent long-practice prose from splitting into mixed English registers.

### 3. SN 56.11: Dhammacakkappavattana Sutta

- Leverage signal: `31` live citations, `23` from major entries.
- Strengthens: four noble truths, the `taṇhā` definition formula,
  `pañcupādānakkhandhā`, and the truth-task family.
- Likely lexicon pressure: keep the first truth practical rather than
  slogan-like, confirm the governed `five clung-to heaps` expression, and keep
  truth-family formulas aligned with MN 141 rather than drifting into
  prestige-diction.

### 4. MN 2: Sabbāsava Sutta

- Leverage signal: `11` live citations, `7` from major entries.
- Strengthens: `āsava`, `āsavakkhaya`, `yoniso manasikāra`,
  `ayoniso manasikāra`, and the method-sequence for dealing with trouble.
- Likely lexicon pressure: sharpen the outflow family beyond headline glosses,
  stabilize the method verbs across `seeing`, `restraint`, `use`, `enduring`,
  `avoiding`, `removing`, and `developing`, and keep `outflow` distinct from
  broader defilement language.

### 5. MN 9: Sammādiṭṭhi Sutta

- Leverage signal: `28` live citations, `22` from major entries.
- Strengthens: wholesome and unwholesome roots, `diṭṭhi`, `ariyasāvaka`,
  dependent arising, nutriment-related analysis, and appropriation-family
  distinctions.
- Likely lexicon pressure: keep the root family aligned, keep broad analytical
  list prose from rotating among near-neighbor glosses, and confirm how the
  dependent-arising family reads inside a longer Sariputta-style exposition.

### 6. MN 44: Cūḷavedalla Sutta

- Leverage signal: `10` live citations, `9` from major entries.
- Strengthens: `vedanā`, `saññā`, `viññāṇa`, `samādhi`, and the
  `adhisīla` / `adhicitta` / `adhipaññā` triad.
- Likely lexicon pressure: keep feeling, recognition, and knowing sharply
  distinct, confirm when comparative `consciousness` language is allowed but
  not default, and stabilize compact analytic dialogue prose.

### 7. MN 64: Mahāmālukya Sutta

- Leverage signal: `11` live citations, `8` from major entries.
- Strengthens: `anusaya`, `saṃyojana`, lower and higher fetters,
  sensual-passion residue, and awakening-stage analysis.
- Likely lexicon pressure: tighten the boundary between active hindrance,
  latent tendency, and binding fetter, and promote any lower-fetter /
  higher-fetter list handling that still lives only in prose.

### 8. DN 15: Mahānidāna Sutta

- Leverage signal: `8` live citations, `3` from major entries.
- Strengthens: `viññāṇa`, `nāmarūpa`, the contact-to-feeling sequence, and
  dependent-arising anti-metaphysical guardrails.
- Likely lexicon pressure: keep `knowing` tied to conditioned process rather
  than witness-like metaphysics, and confirm how the repo handles reciprocal
  `viññāṇa` / `nāmarūpa` lines without losing readability.

### 9. SN 22.89: Khemaka Sutta

- Leverage signal: `7` live citations, `6` from major entries.
- Strengthens: `asmimāna`, `anusaya`, `saṃyojana`, identity residue, and the
  five-heaps selfing family after SN 22.59.
- Likely lexicon pressure: keep self-view, taking personally, and the residual
  conceit `I am` distinct, and decide whether the identity-construction brief
  now needs an explicit five-heaps companion surface.

### 10. SN 22.48: Khandha Sutta

- Leverage signal: `11` live citations, `2` from major entries.
- Strengthens: `pañcakkhandhā`, `pañcupādānakkhandhā`, and the constituent
  heap compounds that carry the family in formulaic form.
- Likely lexicon pressure: confirm collective `five heaps` versus
  `five clung-to heaps`, keep the constituent compounds aligned with the
  stabilized SN 22.59 translation voice, and prevent minor-entry compound drift
  from accumulating invisibly.

### 11. MN 7: Vattha Sutta

- Leverage signal: `6` live citations, `6` from major entries.
- Strengthens: `kilesa`, `upakkilesa`, cleansing imagery, and the relation
  between broad defilement-family language and narrower corruption-language.
- Likely lexicon pressure: keep `defilement` from swallowing the narrower
  residue families, and decide whether the `upakkilesa` side now needs a
  stronger translator-facing note surface.

### 12. SN 36.6: Salla Sutta

- Leverage signal: `1` live citation, `1` from a major entry.
- Strengthens: feeling-side reaction language, bodily pain versus mental
  distress, and the practical line between first pain and added reactive pain.
- Likely lexicon pressure: add sharper note-level language for reactive
  doubling, align it with the MN 137 / MN 148 sensory-response surface, and
  decide whether the repo now needs a reusable feeling-escalation formula
  record.

### 13. SN 46.51: Āhāra Sutta

- Leverage signal: `6` live citations, `6` from major entries.
- Strengthens: `nīvaraṇa`, awakening factors, and the feeding / starving side
  of conditional-practice prose.
- Likely lexicon pressure: keep nourishment-side formulas distinct from generic
  causal language, and decide whether the repo now needs a compact
  translator-facing feed / unfeed brief for hindrance and awakening-factor
  work.

### 14. MN 39: Mahā-Assapura Sutta

- Leverage signal: `9` live citations, `8` from major entries.
- Strengthens: hindrance abandoning, jhāna sequence, release, and
  `vimutti-ñāṇadassana` style closing formulas.
- Likely lexicon pressure: stabilize long practice-progression English outside
  DN 2, and keep the release-and-knowledge close coordinated with the existing
  liberation family rather than recasting it as inspirational prose.

### 15. AN 10.60: Girimānanda Sutta

- Leverage signal: `6` live citations, `2` from major entries.
- Strengthens: perception practice, three-marks contemplative compounds, and
  abandoning-oriented saññā formulas.
- Likely lexicon pressure: decide whether the practice-perception family now
  needs a dedicated translator-facing note surface around `anicca-saññā`,
  `dukkha-saññā`, `anatta-saññā`, and `pahāna-saññā`.

## Suggested Translation Order

Use the ranked list as the source of truth, but work in three waves:

### Wave 1: Dense Existing Support

- Completed: `SN 12.2`, `SN 56.11`, `DN 2`, `MN 2`, `MN 9`

### Wave 2: Distinction-Forcing Surfaces

- Completed: `MN 44`, `MN 64`
- `DN 15`
- `SN 22.89`
- `SN 22.48`

### Wave 3: Strategic Expansion

- `MN 7`
- `SN 36.6`
- `SN 46.51`
- `MN 39`
- `AN 10.60`

## Why This Order

- Wave 1 should land first because those texts already carry the heaviest live
  policy surface. The completed `SN 12.2`, `SN 56.11`, and `DN 2` surfaces now
  provide controls for dependent arising, four-truths language, hindrance
  clearing, and jhāna prose.
- Wave 1 is now complete. Wave 2 now continues with `DN 15`, using the
  completed first-wave surfaces and the completed `MN 44` and `MN 64` surfaces
  as controls for right-view, dependent-arising, four-truths, outflow,
  training-sequence, identity, felt-experience, mental-composure, fetter, and
  underlying-tendency language.
- Wave 2 comes next because those texts sharpen distinctions the repo already
  records but has not yet forced through enough outward-facing translation
  documents: fetter versus tendency, identity residue versus view, and
  conditioned knowing versus metaphysical consciousness drift.
- Wave 3 is still high value, but it is better treated after the denser
  clusters are confirmed in translation-facing prose. Those texts are more
  likely to extend surface coverage than to settle the biggest remaining
  default-versus-default tensions.

## What To Update In The Lexicon After Each Sutta

After each translation pass:

1. review the governing major entries, compounds, and formula records together
2. update headword notes only when the sutta exposes a reusable family-level
   boundary
3. add formula records when a stock line is likely to recur across multiple
   translation surfaces
4. refresh any linked brief, map, or generated cluster sheet that now has a
   stronger control passage
5. regenerate translation indexes and rerun the full verification suite

## Not First-Wave

These texts are still useful, but they are not the best immediate leverage
plays relative to the current lexicon surface:

- `SN 35.28` Ādittapariyāya Sutta: strong and famous, but the current live
  citation footprint is thinner than the ranked set above, so it would force
  more net-new fire and fuel governance before returning value.
- `MN 38` Mahātaṇhāsaṅkhaya Sutta: important for `viññāṇa` and `taṇhā`, but
  DN 15 and the completed MN 44 surface are cleaner first stabilizers for the
  current knowing-process surface.
- `MN 26` Ariyapariyesanā Sutta: already useful for knowledge and liberation
  language, but it is less direct as a next-step drift reducer than the
  denser formula and contrast texts above.
- `SN 12.23` Upanisa Sutta: strong reserve candidate once the core
  dependent-arising translation surfaces are in place and the repo is ready to
  widen the positive-sequence side.

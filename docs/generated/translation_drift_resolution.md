# Translation Drift Resolution

Generated: 2026-04-20

## Terms Updated

- `pabbajita` (`terms/minor/pabbajita.json`)
- `gahaṭṭha` (`terms/minor/gahattha.json`)
- `mettācetovimutti` (`terms/minor/metta-cetovimutti.json`)
- `karuṇācetovimutti` (`terms/minor/karuna-cetovimutti.json`)
- `muditācetovimutti` (`terms/minor/mudita-cetovimutti.json`)
- `upekkhācetovimutti` (`terms/minor/upekkha-cetovimutti.json`)

## Changes Made

### Term Entries

- `pabbajita`: added `discouraged_translations`, `context_rules`, `example_phrases`, and `sutta_references`; standardized the default around `renunciant`.
- `gahaṭṭha`: added the same rule-bearing support surface; stabilized the household / gone-forth contrast as `householder` versus `renunciant`.
- `mettācetovimutti`: added rule fields; stabilized the full rendering `liberation of mind through friendliness`.
- `karuṇācetovimutti`: added rule fields; stabilized the full rendering `liberation of mind through kindness towards others`.
- `muditācetovimutti`: added rule fields; stabilized the full rendering `liberation of mind through gladness`.
- `upekkhācetovimutti`: added rule fields; stabilized the full rendering `liberation of mind through dynamic balance`.

### Translation And Policy Surfaces

- `pabbajita`: `renunciate` -> `renunciant` in `docs/translations/mn99-subha-sutta.md` and `docs/translations/mn99-subha-sutta-notes.md`.
- `pātimokkha`: `pātimokkha` -> `pāṭimokkha` in `docs/translations/dn2-samannaphala-sutta.md`.
- Brahmavihāra release compounds: `liberation of mind through ...` -> full four-compound renderings in `docs/translations/mn99-subha-sutta-notes.md`.
- `vitakka`: source-profile line `vitakka as applying` -> `applying-language used to explain vitakka` in `docs/dhammarato-quotes-profile.md`.
- `vicāra`: source-profile line `vicara as sustaining` -> `sustaining-language used to explain vicara` in `docs/dhammarato-quotes-profile.md`.
- `savitakkaṁ savicāraṁ`: `vitakka and vicāra as thinking and pondering` -> `savitakkaṁ savicāraṁ as with thinking and pondering` in `docs/first-jhana-entry-sheet.md`.
- `sammāsaṅkappa`: `samma-sankappa as attitude` -> `samma-sankappa as right attitude` in `docs/what-is-and-is-not-the-path-profile.md`.
- `nirodha`: source-profile line `nirodha as cessation` -> `cessation-language used to explain nirodha` in `docs/dhammarato-quotes-profile.md`.

## Conflicts Resolved

- Removed all assertive unregistered rendering statements from the live docs scanned by the audit pattern, excluding the original audit snapshot itself.
- Preserved registered context alternates where they are already governed by term entries, such as heap-context `saṅkhārā` -> `putting-together activities`.
- Preserved guardrail statements that explicitly say not to use a rendering by default, such as `taṇhā` not as generic `desire` and `jhāna` not as `absorption`.
- Kept cross-entry collisions that are intentional doctrinal contrasts rather than defects. Examples include `desire` across `chanda` / `taṇhā`, `release` across `vimutti` / `nissaraṇa` / `khaya`, and `nibbāna` across consummation-side designations.

## Any Ambiguities That Require Human Review

- The audit listed 841 remaining minor entries with one or more missing audit-requested fields. The live schema does not require those fields for minor entries. Mechanical backfill would introduce weak or artificial discouraged translations, so those should be handled in future family batches when a real translation surface exposes pressure.
- The 69 cross-entry collisions in the audit are mostly intentional contrast points. They should become an explicit allowlist with rationale, owner terms, and family notes rather than being removed by global synonym edits.
- Guardrail-only findings are not translation drift in use. They should be excluded or separately classified by any future automated audit.
- The generated audit report itself is a historical snapshot and still names issues resolved in this pass. Use this resolution report plus current checks as the checkpoint state.

## Verification

- `python scripts/validate_terms.py --strict`
- `python scripts/check_translation_drift.py --strict`
- `python scripts/check_generated_docs.py`
- `python scripts/check_translation_formula_consistency.py --format json`
- `python -m unittest tests.test_craving_appropriation_policy tests.test_validate_terms tests.test_check_translation_drift`
- `python -m unittest tests.test_validate_terms tests.test_check_translation_drift`

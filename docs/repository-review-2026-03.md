# Repository Review Notes

## Scope

This note records the high-confidence structural conclusions after the March
2026 professional-surface cleanup pass.

It focuses on file naming, directory structure, contributor navigation, and
other repository-maintenance concerns rather than doctrinal judgment.

## Current Surface

- Term files: 1117
- Major terms: 236
- Minor terms: 881
- Docs files in `docs/`: 67
- Verification stack: passing

## Findings

### Naming

- `docs/` now uses one filename convention: lowercase-kebab-case.
- This is enforced by `python scripts/check_docs_integrity.py`.
- Edge-case filename drift in the path-factor family was reduced by normalizing
  `sammasankappa.json` to `samma-sankappa.json`.

### Directory Structure

- `terms/major/` and `terms/minor/` remain flat on disk by design.
- The repo is now large enough that flat directories are weak for human
  browsing but still strong for tooling, file destinations, and editorial
  predictability.
- The chosen solution is not to introduce nested term subdirectories.
- Instead, the repo now uses a generated navigation layer for human browsing.

### Navigation

- `terms/README.md` now states the flat-directory decision explicitly.
- Generated indexes in `docs/generated/major-term-index.md` and
  `docs/generated/minor-term-index.md` provide human navigation.
- `python scripts/term_directory_navigation.py --check` is now part of the
  standard verification flow.

### Documentation Freshness

- The previous review snapshot was stale and materially undercounted the live
  term surface.
- This file now reflects the current repository scale and decisions as of the
  first-wave translation-surface refresh.
- Refresh this snapshot when the live term counts or the top-level docs surface
  change materially.

## Immediate Maintenance Rule

1. Keep `terms/` flat unless tooling needs change strongly enough to justify a
   deliberate migration.
2. Treat generated navigation as the human-browsing layer.
3. Keep `docs/` filename style uniform and machine-checked.
4. Normalize future edge-case filenames when they break obvious family patterns.

# Repository Review Notes

## Scope

This note records the high-confidence structural issues found during the
March 2026 cleanup pass. It is intended to help maintainers separate safe
editorial maintenance from decisions that require doctrinal judgment.

## Findings

### Schema and Entry Baseline

- All 984 current term files include the schema's globally required fields.
- All current `major` entries include `notes`, `context_rules`,
  `related_terms`, and `example_phrases`.
- The March 2026 documentation cleanup resolved the main contributor-language
  mismatch around live schema fields such as `preferred_translation`,
  `context_rules`, `notes`, and `example_phrases`.

### Translation-Drift Risks

- The strict validation stack currently passes, so reciprocal `related_terms`
  warnings are not the active blocker they were during the earlier cleanup
  pass.
- Current health reporting shows no missing `authority_basis`, no missing
  `translation_policy`, no example-source gaps, and no unresolved preferred
  translation collisions in major entries.
- Current coverage reporting shows no missing doctrinal families from the
  repository's tracked coverage set.
- The main remaining risk is now surface-level rather than structural: the
  repository is strong internally, but new contributors still depend too much
  on knowing where to look for the right workflow, command, or review document.

### Documentation Drift

- Core contributor docs now align with the live schema and the current
  repository structure.
- The remaining documentation gap is operational rather than definitional:
  command discovery, workflow entry points, and GitHub-native navigation need
  to be more obvious at first glance.

### Maturity Signals

- CI already runs the full verification suite on pull requests and pushes for
  Python 3.11 and 3.12.
- Community-health files are present and coherent.
- A small set of major entries still remains in `draft`, which is reasonable,
  but that queue should stay explicit so editorial review status remains easy
  to interpret.

## Immediate Priorities

1. Keep the public repository surface as disciplined as the underlying data by
  tightening README navigation, command discovery, and contributor entry
  points.
2. Maintain explicit review discipline around the remaining `draft` major
  entries so status vocabulary continues to mean something.
3. Keep workflow docs aligned with the live script surface as new reporting,
  scaffolding, or backfill utilities are added.

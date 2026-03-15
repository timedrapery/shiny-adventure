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
  warnings are not the active release blocker they were during the earlier
  cleanup pass.
- The main quality gap has shifted from structural correctness to provenance
  depth: many major entries still rely on generic `authority_basis`, and more
  than 100 major entries still have at least one example phrase without a
  canonical `source` citation.
- The highest-yield next work is cluster-based provenance hardening,
  especially in dependent arising, core practice, and mental-quality families,
  where house policy is already present but still needs stronger source-backed
  support.

### Documentation Drift

- Core contributor docs now align with the live schema and the current
  repository structure.
- The remaining documentation gap is operational rather than definitional:
  cluster-by-cluster editorial progress is still tracked mostly in narrative
  planning documents rather than in compact milestone-style execution notes.

## Immediate Priorities

1. Replace generic `authority_basis` entries in the highest-leverage doctrinal
  clusters, starting with dependent arising.
2. Fill missing `example_phrases[].source` citations where canonical references
  are already known or can be verified from related term families.
3. Continue reviewing major entries for rule quality, especially where notes
  describe translation philosophy but context rules remain thinner than the
  surrounding editorial claims.

# Repository Review Notes

## Scope

This note records the high-confidence structural issues found during the
March 2026 cleanup pass. It is intended to help maintainers separate safe
editorial maintenance from decisions that require doctrinal judgment.

## Findings

### Schema and Entry Baseline

- All 965 current term files include the schema's globally required fields.
- All current `major` entries include `notes`, `context_rules`,
  `related_terms`, and `example_phrases`.
- The main alignment issue is not missing keys. It is that contributor-facing
  documentation sometimes uses conceptual language like "preferred rendering"
  and "translation rule" without clearly mapping that language to the live
  schema fields.

### Translation-Drift Risks

- `related_terms` reciprocity is incomplete across a live cluster of doctrinal
  entries. The lint suite currently reports these as warnings, but
  `scripts/run_checks.py` treats them as release-blocking by running
  `lint_terms.py --strict`.
- The current warning cluster is concentrated in entries that affect dependent
  arising, grasping, becoming, fetters, hindrances, and insight vocabulary.
- Because many of the affected term files are already modified in the worktree,
  those doctrinal link repairs should be reviewed by a human editor rather than
  patched mechanically.

### Documentation Drift

- Earlier docs implied that `entry_type` was only a project convention even
  though the current schema requires it.
- Earlier docs did not state clearly that `preferred_translation`,
  `context_rules`, `notes`, and `example_phrases` are the live structural
  equivalents of preferred rendering, translation rule, usage notes, and
  examples.

## Immediate Priorities

1. Resolve the current reciprocal `related_terms` warnings in the doctrinal
   clusters already under active revision.
2. Decide whether reciprocal links should remain warnings or become an explicit
   policy requirement for reviewed and stable entries.
3. Continue reviewing major entries for rule quality, especially where notes
   describe translation philosophy but context rules remain thin.

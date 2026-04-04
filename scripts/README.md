# Script Index

This directory contains the repository's validation, reporting, scaffolding, and helper tooling.

All CLI scripts support `--help`.

Use [../docs/usage.md](../docs/usage.md) for task-based command recipes and
[../docs/generated/generated-docs-guide.md](../docs/generated/generated-docs-guide.md)
if you are working with scripts that write under `docs/generated/`.

When a script produces generated reference material, treat that output as a
derived surface. Fix the live term data or the generating script first when the
output looks wrong.

## Core Verification Commands

- `python scripts/run_checks.py`
  Runs the full verification suite in the same order used by CI.
- `python scripts/check_docs_integrity.py`
  Validates internal Markdown links and required repository-surface metadata files.
- `python scripts/check_translation_formula_consistency.py`
  Detects discouraged stock-phrase variants and formula-level drift in the shareable translation surfaces under `docs/translations/`.
- `python scripts/validate_terms.py`
  Validates term JSON files against the project schema.
- `python scripts/lint_terms.py`
  Runs editorial lint checks against live term data.
- `python scripts/check_translation_drift.py`
  Detects translation drift across related terms and policy-bearing records.
- `python scripts/term_directory_navigation.py --check`
  Verifies that the generated major/minor term navigation indexes are present and current.
- `python scripts/dependent_arising_cluster_report.py`
  Audits the dependent-arising cluster and can generate translator-facing outputs.
- `python scripts/jhana_cluster_report.py`
  Audits the jhana core cluster and can generate translator-facing outputs.
- `python scripts/path_factor_cluster_report.py`
  Audits the path-factor core cluster and can generate translator-facing outputs.
- `python scripts/four_noble_truths_cluster_report.py`
  Audits the four noble truths cluster and can generate translator-facing outputs.
- `python scripts/sense_fields_cluster_report.py`
  Audits the sense-fields cluster and can generate translator-facing outputs.
- `python scripts/three_marks_cluster_report.py`
  Audits the three-marks cluster and can generate translator-facing outputs.

## Reporting And Planning Commands

- `python scripts/repo_health.py --top 10`
  Reports repository health signals for editorial scalability and automation.
- `python scripts/audit_term_coverage.py --top 15`
  Reports doctrinal coverage gaps in the term dataset.
- `python scripts/modern_english_audit.py`
  Reports likely elevated or archaic diction in the live repo surface and helps reviewers catch register drift before merge.
- `python scripts/voice_consistency_audit.py`
  Reports mixed note templates, fragmentary example-note phrasing, and other voice-pattern drift in the live repo surface.
- `python scripts/dependent_arising_cluster_report.py --write-docs`
  Checks the dependent-arising cluster surface and writes glossary, formula-sheet, brief, and consistency outputs into `docs/generated/`.
- `python scripts/jhana_cluster_report.py --write-docs`
  Checks the jhana core cluster surface and writes glossary, sequence, path-brief, and formula-sheet outputs into `docs/generated/`.
- `python scripts/path_factor_cluster_report.py --write-docs`
  Checks the path-factor core cluster surface and writes glossary, core-loop, tenfold-sequence, and supporting-terms outputs into `docs/generated/`.
- `python scripts/four_noble_truths_cluster_report.py --write-docs`
  Checks the four noble truths cluster surface and writes glossary, truth-task, correct-noble-practice, and scope outputs into `docs/generated/`.
- `python scripts/sense_fields_cluster_report.py --write-docs`
  Checks the sense-fields cluster surface and writes glossary, twelve-field-map, contact-interface, and translator-brief outputs into `docs/generated/`.
- `python scripts/three_marks_cluster_report.py --write-docs`
  Checks the three-marks cluster surface and writes glossary, contemplation-sheet, formula-sheet, and translator-brief outputs into `docs/generated/`.
- `python scripts/term_directory_navigation.py --write-docs`
  Generates navigation indexes for the flat `terms/major/` and `terms/minor/` directories.
- `python scripts/draft_major_review_queue.py`
  Reports the current queue of draft major entries still awaiting an editorial pass.
- `python scripts/five_heaps_cluster_report.py`
  Audits the five-heaps / clung-to-heaps cluster and can generate translator-facing sheets in `docs/generated/`.
- `python scripts/identity_construction_cluster_report.py`
  Audits the identity-construction cluster and can generate a glossary plus contrast sheet in `docs/generated/`.
- `python scripts/bondage_residue_cluster_report.py`
  Audits the bondage / residue cluster and can generate a glossary plus contrast sheet in `docs/generated/`.
- `python scripts/bondage_imagery_cluster_report.py`
  Audits the bondage-imagery cluster and can generate a glossary plus contrast sheet in `docs/generated/`.
- `python scripts/abandonment_sequence_cluster_report.py`
  Audits the abandonment / quenching / exhaustion cluster and can generate a glossary plus contrast sheet in `docs/generated/`.
- `python scripts/crossing_release_interface_cluster_report.py`
  Audits the crossing / escape / release interface cluster and can generate a glossary plus contrast sheet in `docs/generated/`.
- `python scripts/consummation_interface_cluster_report.py`
  Audits the consummation / unconditioned interface cluster and can generate a glossary plus contrast sheet in `docs/generated/`.
- `python scripts/emptiness_signless_wishless_cluster_report.py`
  Audits the emptiness / signless / wishless interface cluster and can generate a glossary plus contrast sheet in `docs/generated/`.
- `python scripts/osf_reconciliation_report.py`
  Audits the current OSF reconciliation surface and can generate a term-by-term reconciliation sheet in `docs/generated/`.
- `python scripts/knowledge_cluster_report.py`
  Audits the knowledge / seeing / understanding cluster and can generate a glossary plus contrast sheet in `docs/generated/`.
- `python scripts/verbal_knowing_cluster_report.py`
  Audits the verbal knowing / recognition cluster and can generate a glossary plus contrast sheet in `docs/generated/`.
- `python scripts/craving_appropriation_cluster_report.py`
  Audits the craving / appropriation / affective-attachment cluster and can generate a glossary plus contrast sheet in `docs/generated/`.
- `python scripts/kama_cluster_report.py`
  Audits the kāma / sensuality cluster and can generate a glossary plus contrast sheet in `docs/generated/`.
- `python scripts/experience_process_cluster_report.py`
  Audits the phassa / vedanā / saññā / cetanā / viññāṇa cluster and can generate a glossary plus contrast sheet in `docs/generated/`.
- `python scripts/policy_backfill_queue.py`
  Ranks major terms that should be prioritized for metadata backfill.

## Candidate Intake Commands

- `python scripts/extract_candidate_terms.py path/to/source.txt`
  Extracts review candidates from Pali source texts without creating live entries.
- `python scripts/generate_candidate_report.py`
  Renders a Markdown review report from candidate extraction JSON.
- `python scripts/scaffold_candidate_terms.py --priority create_now`
  Scaffolds review packets for extracted candidates without writing to `terms/`.

## Metadata Backfill Commands

- `python scripts/scaffold_policy_metadata.py --check-only --all-missing`
  Shows which major entries would receive placeholder `authority_basis` or `translation_policy` blocks.
- `python scripts/scaffold_policy_metadata.py --all-missing`
  Writes placeholder metadata blocks for missing major-entry policy fields.
- `python scripts/backfill_policy_metadata.py --check-only`
  Applies machine-safe metadata backfill logic without writing files.

Use these conservatively. Placeholder output still requires editorial completion before review or merge.

## Batch Writing Commands

- `python scripts/write_term_batch.py --help`
  Writes term entry batches to `terms/` using explicit UTF-8 output.

## Internal Helper Modules

- `scripts/term_store.py`
  Shared helpers for locating and writing term files.
- `scripts/text_utils.py`
  Shared text normalization and ASCII-safe display helpers.

These modules are support code, not standalone workflow entry points.

## Practical Starting Points

- Editing term data: run `validate_terms.py`, `lint_terms.py`, and `check_translation_drift.py`.
- Checking repository surface quality: run `check_docs_integrity.py`.
- Checking overall repository maturity: run `repo_health.py` and `audit_term_coverage.py`.
- Reviewing open major-entry status work: run `draft_major_review_queue.py`.
- Preparing a merge-ready pass: run `run_checks.py`.
- Intake from new source material: use the candidate workflow commands first, then promote only after review.

# Usage

This page provides task-based command patterns for maintainers and contributors. For a script-by-script index, see [../scripts/README.md](../scripts/README.md).

If you are not sure where the underlying policy lives, read
[documentation-guide.md](documentation-guide.md) first. If you are working with
derived materials under `docs/generated/`, also read
[generated/generated-docs-guide.md](generated/generated-docs-guide.md).

## Validate A Term Change

After editing live records in `terms/`, run:

```bash
python scripts/validate_terms.py
python scripts/lint_terms.py
python scripts/check_translation_drift.py
```

Use strict mode when you want warnings to become release-blocking:

```bash
python scripts/lint_terms.py --strict
python scripts/check_translation_drift.py --strict
```

Use this path for preferred translation changes, context rule edits, tag changes, and family-level policy work.

For the jhana family specifically, add the dedicated audit:

```bash
python scripts/jhana_cluster_report.py --strict
```

For the path-factor family specifically, add the dedicated audit:

```bash
python scripts/path_factor_cluster_report.py --strict
```

For the four noble truths family specifically, add the dedicated audit:

```bash
python scripts/four_noble_truths_cluster_report.py --strict
```

For the sense-fields family specifically, add the dedicated audit:

```bash
python scripts/sense_fields_cluster_report.py --strict
```

For the three-marks family specifically, add the dedicated audit:

```bash
python scripts/three_marks_cluster_report.py --strict
```

## Run The Full Verification Suite

```bash
python scripts/run_checks.py
```

This runs tests, schema validation, editorial lint in strict mode, drift checks, coverage audit, and repository health reporting in sequence.

It also runs the dedicated cluster audits, including the jhana, path-factor, four-noble-truths, sense-fields, and three-marks checks.

## Check Documentation And Repository Surface

```bash
python scripts/check_docs_integrity.py
```

Use this after editing Markdown, issue templates, or repository-surface metadata such as `CITATION.cff`.

## Audit Modern English Register

```bash
python scripts/modern_english_audit.py
```

Use this after broad wording changes in `terms/`, translation docs, or policy
docs when you want a quick report of likely archaic or elevated diction that
should be reviewed before merge.

## Audit Voice Consistency

```bash
python scripts/voice_consistency_audit.py
```

Use this after changing `notes`, `context_rules`, `example_phrases`, or
contributor docs when you want a quick report of mixed note templates,
fragmentary example notes, or other voice-pattern drift.

## Inspect Repository Health

Generate the default human-readable report:

```bash
python scripts/repo_health.py --top 10
```

Export JSON for automation or archival:

```bash
python scripts/repo_health.py --format json > repo-health.json
```

Use this when you want a compact summary of policy coverage, status counts, untranslated terms, and other maturity signals.

## Audit Doctrinal Coverage

```bash
python scripts/audit_term_coverage.py --top 15
```

Use this when planning expansion work or confirming that a doctrinal family is already represented.

## Review Draft Major Entries

```bash
python scripts/draft_major_review_queue.py
```

Export JSON when you want to archive or compare the queue:

```bash
python scripts/draft_major_review_queue.py --format json
```

Use this when deciding which policy-bearing entries still need an editorial pass before promotion from `draft`.

## Work On Metadata Backfill

Rank the highest-priority terms first:

```bash
python scripts/policy_backfill_queue.py
```

Preview placeholder scaffolding without editing files:

```bash
python scripts/scaffold_policy_metadata.py --check-only --all-missing
```

Apply machine-safe backfills where repository policy allows:

```bash
python scripts/backfill_policy_metadata.py --check-only
```

Use this workflow conservatively. Placeholder scaffolding is only a drafting aid and still requires editorial completion.
If the output leaves `Repository editorial record` in place, refine that
provenance before treating the entry as review-ready.

## Candidate Intake Workflow

Extract candidate terms from source text:

```bash
python scripts/extract_candidate_terms.py path/to/source.txt
```

Generate a review report from the extracted data:

```bash
python scripts/generate_candidate_report.py
```

Scaffold review packets for high-priority candidates:

```bash
python scripts/scaffold_candidate_terms.py --priority create_now
```

Candidate outputs belong in review flow first. Do not promote them into `terms/` until their editorial status, authority basis, and family impact have been checked.

Directory-level guidance for those outputs lives in
[../candidates/README.md](../candidates/README.md).

## Regenerate Reference Material

Regenerate the flat term indexes:

```bash
python scripts/term_directory_navigation.py --write-docs
```

Regenerate a translator-facing cluster surface after cluster-level policy work:

```bash
python scripts/path_factor_cluster_report.py --write-docs
python scripts/four_noble_truths_cluster_report.py --write-docs
```

Use the relevant cluster script for the family you changed. Generated files are
reference outputs, not the source of truth.

## Run Targeted Tests

Use focused test commands when iterating on one script:

```bash
python -m unittest tests.test_validate_terms -v
python -m unittest tests.test_repo_health -v
python -m unittest tests.test_run_checks -v
```

Use broad discovery before merging workflow changes:

```bash
python -m unittest discover -s tests
```

## Discover Flags And Options

Every CLI script supports `--help`.

```bash
python scripts/check_docs_integrity.py --help
python scripts/check_translation_drift.py --help
python scripts/scaffold_candidate_terms.py --help
python scripts/repo_health.py --help
```

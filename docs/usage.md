# Usage

This page provides task-based command patterns for maintainers and contributors. For a script-by-script index, see [../scripts/README.md](../scripts/README.md).

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

## Run The Full Verification Suite

```bash
python scripts/run_checks.py
```

This runs tests, schema validation, editorial lint in strict mode, drift checks, coverage audit, and repository health reporting in sequence.

It also runs the dedicated cluster audits, including the jhana and path-factor core-cluster checks.

## Check Documentation And Repository Surface

```bash
python scripts/check_docs_integrity.py
```

Use this after editing Markdown, issue templates, or repository-surface metadata such as `CITATION.cff`.

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

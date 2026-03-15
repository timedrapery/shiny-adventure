# Usage

This page provides practical command patterns for maintainers and contributors.

## Validate All Terms

```bash
python scripts/validate_terms.py
```

Use this after editing term records to catch schema violations and filename-to-normalized-term mismatches.

## Run Editorial Lint

```bash
python scripts/lint_terms.py
```

Use strict mode to block unresolved structural warnings:

```bash
python scripts/lint_terms.py --strict
```

## Check Translation Drift

```bash
python scripts/check_translation_drift.py
```

Use strict mode when preparing merge-ready changes:

```bash
python scripts/check_translation_drift.py --strict
```

## Generate Repository Health Report

```bash
python scripts/repo_health.py --top 10
```

Export JSON for automation or archival:

```bash
python scripts/repo_health.py --format json > repo-health.json
```

## Run Full Verification Suite

```bash
python scripts/run_checks.py
```

This command runs tests, schema validation, linting, drift checks, coverage audit, and repository health reporting in sequence.

## Candidate Intake Workflow

Extract candidate terms from source text:

```bash
python scripts/extract_candidate_terms.py path/to/source.txt
```

Generate a report:

```bash
python scripts/generate_candidate_report.py
```

Scaffold high-priority candidate files:

```bash
python scripts/scaffold_candidate_terms.py --priority create_now
```

Candidate outputs should be reviewed before promotion into terms/.

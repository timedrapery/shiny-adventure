# Architecture

This document describes how repository components work together.

## High-Level Layout

- `terms/`: authoritative live term records, split into `major/` and `minor/`
- `schema/`: JSON schema defining record structure and required policy fields
- `scripts/`: validation, linting, drift checks, reporting, scaffolding, and generation tooling
- `tests/`: regression tests for scripts and repository workflows
- `docs/`: normative policy docs, workflow guides, and planning material
- `docs/generated/`: generated reference outputs derived from live policy and reporting scripts
- `candidates/`: intake area for proposed terms before editorial promotion

## Data Flow

### Live Policy Flow

1. A contributor edits or creates JSON term records in `terms/`.
2. Scripts validate structure and policy behavior against schema rules.
3. Lint and drift checks surface inconsistency risks and policy gaps.
4. Tests guard script behavior and repository-level automation.

### Candidate Intake Flow

1. A contributor extracts or reviews vocabulary under `candidates/`.
2. Review artifacts stay separate from the live lexicon.
3. An editor decides whether a candidate belongs in `terms/major/` or `terms/minor/`.
4. The promoted live entry then goes through the normal validation path.

### Generated Reference Flow

1. Scripts summarize live policy into indexes, glossaries, briefs, and reports under `docs/generated/`.
2. Reviewers and translators use those outputs for navigation and comparison.
3. If a generated file is wrong, the fix belongs in live term data or the generating script.

## Validation Layers

- Schema validation: field-level structural correctness
- Editorial lint: policy consistency and quality checks
- Drift checker: highlights translation instability risk
- Coverage and health reports: visibility into backlog and metadata gaps

## Extension Model

New checks should be added under scripts/ with corresponding tests under tests/.

Prefer deterministic, file-based checks that can run in CI without external services.

## Operational Rule

Keep behavior conservative: avoid bulk automated term rewrites without explicit editorial review.

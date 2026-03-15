# Architecture

This document describes how repository components work together.

## High-Level Layout

- terms/: authoritative term records, split into major/ and minor/
- schema/: JSON schema defining record structure and required policy fields
- scripts/: validation, linting, drift checks, reporting, and scaffolding tools
- tests/: regression tests for scripts and workflow behavior
- docs/: editorial standards and contributor guidance
- candidates/: intake area for proposed terms before editorial promotion

## Data Flow

1. A contributor edits or creates JSON term records in terms/.
2. Scripts validate structure and policy behavior against schema rules.
3. Lint and drift checks surface inconsistency risks and policy gaps.
4. Tests guard script behavior and repository-level automation.

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

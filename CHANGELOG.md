# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project follows Semantic Versioning where versioning is used.

## [Unreleased]

### Added

- Added project trust and governance files: security policy and code of conduct.
- Added contributor-oriented docs spine for project overview, architecture, development, and usage.
- Added [scripts/README.md](scripts/README.md) as a script index for validation, reporting, and scaffolding tools.
- Added `CITATION.cff` so the repository can be cited as a maintained translation dataset.
- Added a workflow issue template for documentation, reporting, and contributor-experience gaps.
- Added `scripts/draft_major_review_queue.py` to keep remaining draft major entries visible as an explicit review queue.
- Added `scripts/check_docs_integrity.py` to validate internal Markdown links and required repository-surface metadata files.
- Added [docs/REVIEW_STATUS_MODEL.md](docs/REVIEW_STATUS_MODEL.md) to define how major entries move from draft to reviewed to stable.

### Changed

- Reconstructed README for clearer onboarding and GitHub discoverability.
- Strengthened GitHub collaboration metadata with issue template configuration and dependency update automation.
- Reworked documentation navigation so task-based workflow entry points are easier to find.
- Expanded usage and development guidance with targeted commands, test examples, and script discovery notes.
- Updated repository review notes to reflect the current health-report state instead of earlier cleanup-era backlog claims.
- Improved `scaffold_policy_metadata.py` so placeholder scaffolding emits an explicit completion warning.
- Extended the full verification suite so documentation and repository-surface integrity are checked alongside tests and term validation.
- Promoted 8 structurally complete major entries from `draft` to `reviewed` after an explicit status pass.

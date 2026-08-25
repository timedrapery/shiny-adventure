# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project follows Semantic Versioning where versioning is used.

## [Unreleased]

### Added

- Added a governed plain-English translation of SN 12.44, Loka Sutta, with
  companion notes, newcomer guidance, a complete six-sense presentation of
  the abbreviated source pattern, and direct running-text support for `loka`.
- Added a governed plain-English translation of SN 45.8, Vibhaṅga Sutta, with
  companion notes, a newcomer introduction, complete definitions of all eight
  path factors, and direct running-text support for `ariya`.
- Added governed plain-English translations, companion notes, newcomer
  introductions, and generated reader pages for AN 3.69, AN 4.5, and SN 1.1.
- Added a durable Wave 9 execution plan and newcomer-review workboard so work
  can resume from any clone without relying on chat history.
- Added a governed plain-English translation of AN 2.9, Cariya Sutta, with
  companion source notes, newcomer guidance, reader placement as "What Keeps
  the World Human," and running-text anchors for `hiri` and `ottappa` as
  `conscience` and `moral caution`.
- Added plain contemporary English translations, companion source notes,
  reader introductions, and generated reader pages for SN 45.2, AN 8.6, and
  MN 119.
- Added a newcomer-review protocol and machine-checked seven-sutta cohort
  ledger. Source-fidelity evidence is recorded separately from the still-
  pending human read-aloud and newcomer-comprehension gates.
- Added a progressively enhanced "Find a sutta" page with topic, form,
  reading-stage, difficulty, and length filters, plus reading times throughout
  the discovery lists.
- Added visible source, license, provisional-status, review-date, and content-
  hash disclosures to every sutta page.
- Added Playwright and axe rendered-accessibility checks across every generated
  sutta page, narrow-screen and
  keyboard regressions, EPUB structure validation, and Khuddaka Nikāya source
  resolution for Dhammapada, Itivuttaka, Sutta Nipāta, Theragāthā,
  Therīgāthā, and Udāna citations.
- Added a governed, plain contemporary English translation of SN 22.86,
  Anurādha Sutta, with companion source notes, a controlled rendering of the
  Tathāgata and five-heaps questions, a hand-written newcomer introduction,
  and a generated reader page titled "Can You Pin Down the Tathāgata?"
- Added a governed, plain contemporary English translation of MN 131,
  Bhaddekaratta Sutta, with companion source notes, reusable title policy, a
  hand-written newcomer introduction, and a generated reader page titled
  "Don't Chase the Past or Long for the Future."
- Added project trust and governance files: security policy and code of conduct.
- Added contributor-oriented docs spine for project overview, architecture, development, and usage.
- Added [scripts/README.md](scripts/README.md) as a script index for validation, reporting, and scaffolding tools.
- Added `CITATION.cff` so the repository can be cited as a maintained translation dataset.
- Added a workflow issue template for documentation, reporting, and contributor-experience gaps.
- Added `scripts/draft_major_review_queue.py` to keep remaining draft major entries visible as an explicit review queue.
- Added `scripts/check_docs_integrity.py` to validate internal Markdown links and required repository-surface metadata files.
- Added [docs/review-status-model.md](docs/review-status-model.md) to define how major entries move from draft to reviewed to stable.
- Added neutral readability-review metadata and a checker that locks every
  registered translation body to its documented review state.
- Added structured, source-checked newcomer guides for the Essential Five and
  a reader-accessibility regression checker covering every generated page.
- Added a long-form reader stylesheet with system fonts, visible keyboard
  focus, larger controls, reduced-motion support, mobile reflow, and print
  rules.

### Changed

- Clarified the reader glossary's `world` entry so it covers the lived world
  built through the senses as well as wider cosmological uses.
- Made per-page glossary generation prefer the longest matching phrase,
  including phrases split by Markdown line wrapping, so a phrase such as
  `clearly knowing` no longer picks up an unrelated gloss for `knowing`.
- Repaired the example-source verifier so partial matches are visible and
  strict mode rejects them; corrected all eight partial citations in the live
  corpus.
- Added a registry-backed documentation check that rejects stale current
  translation-surface counts.
- Corrected the surface-leverage audit so it resolves discourses stored inside
  bundled Bilara cache files, counts only the requested discourse, and does not
  misclassify AN 2.9's short counterfactual argument as a bare enumeration.
- Reconstructed README for clearer onboarding and GitHub discoverability.
- Strengthened GitHub collaboration metadata with issue template configuration and dependency update automation.
- Reworked documentation navigation so task-based workflow entry points are easier to find.
- Expanded usage and development guidance with targeted commands, test examples, and script discovery notes.
- Updated repository review notes to reflect the current health-report state instead of earlier cleanup-era backlog claims.
- Improved `scaffold_policy_metadata.py` so placeholder scaffolding emits an explicit completion warning.
- Extended the full verification suite so documentation and repository-surface integrity are checked alongside tests and term validation.
- Promoted 8 structurally complete major entries from `draft` to `reviewed` after an explicit status pass.
- Extended editorial review guidance with source-fidelity, human read-aloud
  usability, newcomer-comprehension, and reader-template accessibility checks.
- Reframed the corpus-wide sentence-level pass around neutral newcomer
  readability rather than person-specific voice calibration. The completed
  translation improvements and body hashes remain intact while human reviews
  remain pending.
- Reworked all 57 reader pages around a clear `Before you read` / `Translation`
  hierarchy, computed reading times, visible term definitions, semantic reading
  navigation, and plain-English titles; replaced the wide glossary and sutta
  index tables with flowing layouts.

# EDITORIAL REVIEW CHECKLIST

Use this checklist when reviewing a pull request, batch term import, or major
policy revision.

## 1. Structural Review

- The entry validates against `schema/PALI_TERM_SCHEMA.json`.
- `normalized_term` matches the filename stem.
- Major entries include non-empty `alternative_translations`,
  `discouraged_translations`, `context_rules`, `related_terms`,
  `example_phrases`, `sutta_references`, and `tags`.
- The JSON contains only documented fields.

## 2. Rule Quality Review

- The preferred rendering is explicit.
- `notes` explain what translation drift or doctrinal confusion the entry is
  meant to prevent.
- `context_rules` say when the default applies and when it should not.
- If compounds inherit the headword by default, that is stated in
  `translation_policy.compound_inheritance` or made explicit in `notes`.
- If the term is often left in Pali, that decision is explicit and the entry
  explains when untranslated use is preferred.

## 3. Provenance Review

- If a preferred rendering or context rule depends on source authority, the
  entry includes `authority_basis`.
- The cited authority matches the order in
  `docs/OSF_EDITORIAL_AUTHORITY.md`.
- Source-backed alternates are not silently promoted to house defaults.
- Example phrases include canonical `source` citations where available.

## 4. Family Review

- Compounds, formulas, and doctrinal neighbors were checked in the same pass.
- `related_terms` links are doctrinally meaningful and reciprocal.
- Changes to anchor terms did not leave nearby compounds drifting back toward
  older English defaults.
- If a compound breaks inheritance from the headword, the override is explicit.

## 5. Release Readiness

- `python scripts/run_checks.py` passes.
- `python scripts/repo_health.py` was reviewed for new provenance or citation
  gaps introduced by the change.
- Documentation was updated if the change affects contributor workflow or
  schema interpretation.

## Summary

<!-- Briefly describe what this pull request changes and why. -->

- **What changed:**
- **Why it changed:**

## Translation Decision

<!-- Complete this section for any change that affects preferred translations,
	 context rules, or doctrinal families. Leave N/A if not applicable. -->

- **Preferred translation affected:** (or N/A)
- **Doctrinal family or compounds reviewed:** (list headwords checked)
- **Authority basis:** (OSF house, Dhammarato, Buddhadasa, or secondary source)
- **Drift-risk terms reviewed:** (confirm any high-instability terms in scope were checked against [docs/DRIFT_RISK_TERMS.md](../docs/DRIFT_RISK_TERMS.md))

## References

<!-- Sutta citations, OSF publication references, or other supporting material. -->

- (add references or leave blank)

## Validation Checklist

- [ ] `python scripts/run_checks.py` passes locally.
- [ ] All changed JSON files are schema-compliant (`python scripts/validate_terms.py`).
- [ ] Lint checks pass (`python scripts/lint_terms.py`).
- [ ] If a preferred translation or context rule changed, the rationale is documented in the entry's `notes` or `authority_basis`.
- [ ] If a major term was changed, linked compounds, formulas, and related terms were reviewed in the same pass.
- [ ] Tags and `status` values match [docs/TAG_STATUS_VOCABULARY.md](../docs/TAG_STATUS_VOCABULARY.md).

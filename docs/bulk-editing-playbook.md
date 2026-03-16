# BULK EDITING PLAYBOOK

Use this when adding or revising dozens of terms in one editorial cycle.

## 1. Choose a Controlled Scope

- Work by doctrinal family, formula cluster, or source profile.
- Do not mix unrelated policy changes in one batch.
- Decide in advance which headwords are anchors and which compounds inherit
  from them.

## 2. Scaffold First

For major entries that still need structured provenance or rule summaries, use:

```bash
python scripts/scaffold_policy_metadata.py --all-missing --check-only
python scripts/scaffold_policy_metadata.py sati samadhi vedana
```

This creates placeholder `authority_basis` and `translation_policy` blocks so
reviewers can see exactly what still needs editorial completion.

## 3. Edit in Passes

Recommended pass order:

1. preferred renderings and discouraged renderings
2. `context_rules`
3. `notes`
4. `authority_basis`
5. `translation_policy`
6. `example_phrases` and `source` citations
7. `related_terms` reciprocity

## 4. Run the Right Checks

During the batch:

```bash
python scripts/validate_terms.py
python scripts/lint_terms.py
python scripts/repo_health.py --top 20
python scripts/policy_backfill_queue.py --top 20
python scripts/backfill_policy_metadata.py --check-only
```

Before merge:

```bash
python scripts/run_checks.py
```

## 5. Review for Drift, Not Just Validity

- Check that compounds still align with their anchor terms.
- Check that synonymous English defaults have not crept back in.
- Check that new source-backed alternates did not silently become defaults.
- Check that examples include canonical citations where available.

## 6. Record Major Decisions

If the batch changes a doctrinal anchor or a family-level rule, add a decision
record using `docs/decision-record-template.md`.

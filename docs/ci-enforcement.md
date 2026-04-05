# CI Enforcement

This repository is expected to fail early when live policy, doctrinal cluster
surfaces, or regression coverage drift out of alignment.

## What CI Enforces

CI now blocks merges on:

- schema violations in live term records
- unresolved major preferred-translation collisions
- editorial lint failures, including weak major rule notes and premature
  `stable` promotion
- translation-drift failures, including conflicting lemma defaults and direct
  contradictions between allowed and discouraged renderings
- missing doctrinal cluster authority surfaces
- failed doctrinal cluster reports in strict mode
- failed regression tests
- any failure inside `python scripts/run_checks.py`

`python scripts/run_checks.py` is the single authoritative repository entrypoint.
CI also runs the highest-signal checks individually so failures surface earlier
and more clearly in pull requests.

For repair workflow and examples of the new diagnostic blocks, also read
[contributor-repair-guide.md](contributor-repair-guide.md).

## CI-Failing Commands

The workflow runs:

```bash
python scripts/validate_terms.py --strict
python scripts/lint_terms.py --strict
python scripts/check_translation_drift.py --strict
python scripts/check_cluster_surfaces.py
python -m unittest discover -s tests
python scripts/run_checks.py
```

If any command returns a non-zero exit code, CI fails.

## How To Read A Failure Block

The enforcement scripts now emit repair guidance in a consistent shape:

- `Rule violated`
- `File`
- `Code`
- `What failed`
- `Why it matters`
- `Minimal safe fix`
- `Good repo example(s)`

The goal is not to soften failures. The goal is to make the smallest safe
repair obvious without asking contributors to search the whole repository first.

The GitHub Actions workflow runs the human-readable form of these checks, so the
same repair blocks appear directly in CI logs. When machine-readable output is
useful, the main enforcement scripts also support `--json`.

## What Causes Failure

### Term-record failures

Major entries are expected to function as rule surfaces, not as thin glossary
stubs.

CI blocks:

- missing required major-entry rule fields
- major notes that are too short to function as policy
- contradictory alternates or discouraged renderings
- placeholder or mojibake text
- missing translation-policy structure on rule-bearing entries
- generic authority placeholders on reviewed or stable majors

### Drift failures

CI blocks:

- the same canonical lemma carrying multiple preferred translations
- major entries using a discouraged rendering inside a context rule
- the same rendering appearing as both allowed and discouraged
- any cluster report finding that fails in `--strict` mode

### Status failures

`reviewed` means the entry is usable.
`stable` means downstream work should currently treat it as the house default.

CI blocks a `stable` major entry if it still looks too thin to carry that
signal. The current stable-floor gate fails entries that have all of these at
once:

- short notes
- only two context rules
- only one example
- only one authority item

If an entry cannot clear that floor yet, keep it `reviewed`.

## Doctrinal Cluster Coverage

Each CI-enforced doctrinal cluster must have all of the following:

- one authority document in `docs/`
- one report script in `scripts/`
- regression coverage in `tests/`

The authoritative inventory lives in
[`scripts/cluster_registry.py`](../scripts/cluster_registry.py).
The surface verifier is
[`scripts/check_cluster_surfaces.py`](../scripts/check_cluster_surfaces.py).

When adding a new CI-enforced cluster:

1. Add the authority document in `docs/`.
2. Add the report script in `scripts/`.
3. Add the regression tests in `tests/`.
4. Register the cluster in `scripts/cluster_registry.py`.
5. Run `python scripts/check_cluster_surfaces.py`.
6. Run `python scripts/run_checks.py`.

Do not add a cluster doc and assume CI will discover it automatically.
The registry is deliberate so cluster coverage stays explicit.

## Adding or Modifying Terms

For new or changed major entries:

- keep `preferred_translation`, `context_rules`, `discouraged_translations`,
  `related_terms`, `translation_policy`, and `authority_basis` aligned
- make the note read as policy, not dictionary prose
- keep example phrases and references sourced
- use `reviewed` until the entry is strong enough to anchor downstream reuse

For minor entries:

- keep schema compliance strict
- keep compounds and formula records aligned with their governing headwords
- avoid introducing unsignaled alternate renderings

Do not change preferred translations casually.
If a preferred translation changes, review the term family, compounds, and any
cluster report that touches that family in the same pass.

## Local Safeguards

An optional local pre-commit hook config is included:

```bash
pre-commit install
```

It runs:

```bash
python scripts/validate_terms.py --strict
python scripts/lint_terms.py --strict
```

Use it to catch merge-blocking failures before pushing.

## Fixing CI Failures

- Schema failure: fix the term record structure first.
- Lint failure: strengthen the live record rather than weakening the rule.
- Drift failure: resolve the contradiction in term data or cluster policy.
- Cluster surface failure: add the missing doc, script, test, or registry entry.
- Test failure: update the implementation and the regression expectation in the
  same pass.

When a failure names multiple related terms or a doctrinal family, do a same-pass
family review rather than patching one file in isolation.

If a generated surface looks wrong, do not patch `docs/generated/` first.
Fix the live term data or generator and rerun the check.

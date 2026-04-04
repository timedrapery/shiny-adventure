# Candidate Intake

This directory is the intake layer for proposed vocabulary discovered in source
texts.

It is deliberately separate from `terms/`.

Use this directory when you are collecting evidence or staging review packets.
Use `terms/` only after the repository has made a live editorial decision.

## What Belongs Here

Use `candidates/` for:

- extracted candidate-term JSON reports
- rendered review reports
- review packets under `candidates/scaffolds/`
- other review-first artifacts that still need editorial judgment

Use `terms/` only after the repository has decided that a candidate belongs in
the governed live lexicon.

## What This Directory Is Not

This is not:

- a staging area for half-finished live term entries
- a place to invent `preferred_translation` values by frequency alone
- a shortcut around the review rules for major entries

## Normal Workflow

1. Extract candidates from source text:

```bash
python scripts/extract_candidate_terms.py path/to/source.txt
```

2. Render the review report:

```bash
python scripts/generate_candidate_report.py
```

3. Scaffold review packets when needed:

```bash
python scripts/scaffold_candidate_terms.py --priority create_now
```

4. Review the evidence before deciding whether a real term entry should be
   added to `terms/`.

## Typical Files

- `candidate_terms.json`: machine-readable extraction report
- `candidate_terms.md`: grouped human review report
- `scaffolds/*.review.json`: review packets for terms that need editorial
  treatment

These outputs are working review materials, not live policy.

## Promotion Rule

Do not promote a candidate directly into `terms/` just because it recurs.

Before promotion:

1. confirm the headword spelling and normalization
2. check whether the term is already covered under another form
3. decide whether it belongs as a `major` or `minor` entry
4. follow [docs/candidate-term-workflow.md](../docs/candidate-term-workflow.md),
   [docs/term-entry-standard.md](../docs/term-entry-standard.md), and
   [STYLE_GUIDE.md](../STYLE_GUIDE.md)

## Related Guides

- [docs/candidate-term-workflow.md](../docs/candidate-term-workflow.md): full intake workflow
- [terms/README.md](../terms/README.md): what belongs in the live lexicon
- [docs/generated/generated-docs-guide.md](../docs/generated/generated-docs-guide.md): how generated reference material differs from live policy

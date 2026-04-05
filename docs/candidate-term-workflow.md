# Candidate Term Workflow

## Purpose

This workflow exists to discover candidate Pali terms from source texts without
silently turning extraction output into house style.

The pipeline is intentionally review-first:

- extract recurring candidate terms
- compare them against the existing lexicon
- rank them for editorial attention
- keep evidence and source traces
- avoid auto-approving translations or rule-bearing entries

## Safety Rule

Candidate extraction is not translation.

The extraction scripts must not:

- invent `preferred_translation` values
- create rule-bearing `major` entries automatically
- overwrite existing term records
- treat frequency alone as doctrinal importance

## Scripts

### 1. Extract candidates

```bash
python scripts/extract_candidate_terms.py path/to/source.txt
python scripts/extract_candidate_terms.py corpus/ --output candidates/candidate_terms.json
```

This step:

- tokenizes Pali-facing text
- inspects unigrams, bigrams, and trigrams
- compares extracted items against existing term records
- marks covered, unresolved, and variant-like candidates
- assigns a review priority
- writes a JSON evidence report

The default output is `candidates/candidate_terms.json`.

### 2. Generate human review report

```bash
python scripts/generate_candidate_report.py
```

This renders a Markdown report grouped into:

- `create_now`
- `review_soon`
- `low_priority`
- `ignore`

The default output is `candidates/candidate_terms.md`.

### 3. Optional review scaffolding

```bash
python scripts/scaffold_candidate_terms.py --priority create_now
```

This does **not** write into `terms/`.

It creates review packets under `candidates/scaffolds/` so an editor can assess
the evidence before deciding whether a real term entry should exist.

The default packet filename pattern is `candidates/scaffolds/<normalized>.review.json`.

## Files Written Under `candidates/`

The intake workflow normally produces:

- `candidates/candidate_terms.json`: machine-readable extraction report
- `candidates/candidate_terms.md`: grouped human review report
- `candidates/scaffolds/*.review.json`: editorial review packets for selected items

Treat these as evidence and review aids. They are not live translation policy.

## Prioritization Rules

Candidates are ranked higher when they show one or more of these signals:

- recurrence across multiple files
- repeated multi-word formula behavior
- overlap with existing doctrinal or major-term vocabulary
- probable normalization or spelling variation of an existing headword
- likelihood of causing translation drift if left unresolved

The priorities mean:

- `create_now`: likely doctrinal, formulaic, or variant-sensitive enough to justify prompt editorial treatment
- `review_soon`: promising but not yet urgent
- `low_priority`: real vocabulary, but weak current evidence
- `ignore`: already covered, common particles, fragments, or low-value noise

## Review Expectations

When promoting a candidate into a real term entry:

1. confirm the headword spelling and normalization
2. check whether the candidate is already covered under a different spelling
3. decide whether it belongs as a `major` or `minor` entry
4. follow `STYLE_GUIDE.md`, `docs/term-entry-standard.md`, and `docs/headword-compound-formula-policy.md`
5. document any real translation decision explicitly rather than inheriting it from extraction output

Use [../candidates/README.md](../candidates/README.md) when you need the
directory-level overview of what belongs in intake versus the live lexicon.

## Suggested First Corpus

The best first corpus is a dependent-arising-focused source set or another
formula-dense doctrinal corpus. That gives the workflow a meaningful test on:

- recurrent doctrinal headwords
- compounds
- phrase-level recurrence
- normalization variants

That is a better pilot than a broad mixed corpus full of low-value narrative
names and particles.

# Contributor Repair Guide

This guide explains how to respond to CI and local enforcement failures without
guesswork.

The repository still fails strictly.
What changed is the quality of the failure output: enforcement scripts now tell
you what failed, why the repository cares, and the smallest safe repair.

## Failure Block Format

The main enforcement scripts now print the same diagnostic shape:

- `Rule violated`: the rule the repository will not relax
- `File`: the affected file when one file is clearly responsible
- `Code`: the machine-stable failure code when available
- `What failed`: the concrete local problem
- `Why it matters`: why the repo treats this as governance, not style
- `Minimal safe fix`: the smallest repair that satisfies the rule
- `Good repo example(s)`: nearby governed surfaces worth imitating structurally

Use the example paths as shape references, not as text to copy blindly.

## Repair Order

When a check fails, repair in this order:

1. Schema shape
2. Major-entry policy surface
3. Drift contradiction
4. Relationship integrity
5. Status discipline
6. Cluster-level closure

Do not start by editing generated docs or broad contributor docs.
Fix the live record or live enforcement surface first.

## Common Repair Patterns

### Schema failure

Typical message:

- a required field is missing
- a field has the wrong type
- a slug or enum value is invalid

Smallest safe repair:

- add the missing field with the minimum repo-consistent shape
- replace the invalid type or value with a schema-compliant one
- keep `normalized_term` aligned with the filename

Do not add ad hoc fields to work around the schema.

### Major-entry policy failure

Typical message:

- a major entry is missing `authority_basis`, `translation_policy`,
  `discouraged_translations`, or other rule-bearing fields
- the note is too short or too descriptive to act as policy

Smallest safe repair:

- make the entry clearly rule-bearing in the same pass
- add the missing field with a real governed value
- keep `preferred_translation`, `context_rules`, `discouraged_translations`,
  `related_terms`, `authority_basis`, and `translation_policy` aligned

Good structural models:

- `terms/major/dukkha.json`
- `terms/major/sati.json`
- `terms/major/sankhara.json`

### Drift failure

Typical message:

- the same lemma carries competing preferred translations
- a rendering appears as both allowed and discouraged
- a context rule uses a discouraged rendering

Smallest safe repair:

- do a same-pass family review
- preserve the existing stable house default unless a governed review explicitly
  changes it
- align the whole family surface, not just one field

Do not invent a new English solution unless the repository already governs it.

### Relationship failure

Typical message:

- `related_terms` points to a missing local entry
- a relationship is one-way when reciprocity is expected

Smallest safe repair:

- add the missing local entry in the same pass, or replace/remove the broken link
- add the reverse link if the relationship should propagate policy
- remove the forward-only link if the relationship is not actually governing

Good structural models:

- `terms/major/sati.json`
- `terms/major/samadhi.json`

### Status failure

Typical message:

- a `stable` major entry is still too thin
- a stabilized drift-danger term dropped below the required floor

Smallest safe repair:

- either deepen the record immediately
- or demote the status to the strongest honest value

Treat `stable` as a reuse commitment.
If you would not want other contributors to follow the entry as the current
house default, it is not stable yet.

### Cluster failure

Typical message:

- a cluster authority doc, script, or test is missing
- a cluster report detects thin collective terms or phrasing mismatches

Smallest safe repair:

- close the family at the family level
- update the authority doc, the script, and the tests together when the surface
  itself is incomplete
- repair related headwords or collective terms in one pass when the failure is
  internal to a doctrinal family

Do not patch one collective or one headword and assume the family is closed.

## Same-Pass Family Review

Do a same-pass family review when:

- the failure names multiple related terms
- the failure touches a cluster report
- the failure changes a preferred translation in a governed family
- the failure concerns compounds inheriting from a headword
- the failure concerns a collective record or stock formula

Examples:

- if a `tanha` compound drifts, review the compound and the `tanha` headword
  together
- if a cluster report fails on phrasing mismatch, review the family doc and the
  affected family terms together

## JSON Diagnostics

Several enforcement scripts also support JSON output.
Use it when you want to archive diagnostics or drive tooling, but prefer the
normal human-readable blocks while editing locally.

In CI, you will usually see the human-readable blocks first. Start there unless
you are building tooling around the diagnostics.

## Final Rule

Do not weaken a rule just because the failure is inconvenient.
The right fix is to make the live policy or live cluster surface explicit enough
that future contributors will not have to guess.

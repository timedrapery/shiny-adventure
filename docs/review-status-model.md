# Review Status Model

This document explains how major term entries move from `draft` to `reviewed` to `stable`.

It does not replace [tag-status-vocabulary.md](tag-status-vocabulary.md). It turns that vocabulary into an operational workflow so status values remain meaningful across the repository.

## Purpose

Status is an editorial confidence signal.

It should answer a practical question:

- Is this entry still being worked out?
- Has it had a real editorial pass?
- Should downstream work currently treat it as the house default?

Status should not be used as a vague marker of age, importance, or how much prose an entry contains.

## Major Entry Lifecycle

### `draft`

Use `draft` when a major entry is structurally present but still under active review.

Typical reasons include:

- the preferred rendering is still under pressure from nearby terms or compounds
- the notes explain the direction of travel but the decision is not yet settled
- examples are present but the team still wants another editorial pass
- the term sits inside an unresolved doctrinal cluster or paired framework

In practice, a draft major entry can still be well-formed and fully valid. `Draft` means review is still open, not that the record is malformed.

### `reviewed`

Use `reviewed` when a major entry has had a real editorial pass and can be relied on for ordinary project work, even if later refinement is possible.

Typical signs:

- the preferred translation is intentional
- notes and context rules align with each other
- examples support the live policy
- related terms and compounds have at least been checked for obvious drift

`Reviewed` is the normal status for solid policy-bearing entries that are still open to future refinement.

### `stable`

Use `stable` when the current entry expresses the house standard strongly enough that downstream reuse should default to it.

Typical signs:

- the preferred rendering is settled enough to anchor nearby work
- the notes explain the main drift risk clearly
- context rules are mature rather than merely present
- examples and references support the decision without obvious gaps
- the team would want related translation work to follow this entry today

`Stable` should be used deliberately. It is a commitment signal, not just a compliment.

## Promotion Rules

Before moving a major entry from `draft` to `reviewed`, check:

- the preferred translation is clearly intentional
- `notes` explains the main editorial decision
- `context_rules` expresses the live exceptions rather than placeholder logic
- examples support the actual policy being claimed
- tags and related terms fit the surrounding doctrinal family

Before moving a major entry from `reviewed` to `stable`, check:

- the entry would be safe to reuse across the current project without caveat
- related compounds or paired terms have been checked in the same pass when relevant
- the drift risk is explicit enough that later contributors can understand what the entry is protecting
- the status reflects current house confidence, not hoped-for future confidence

## Review Queue

Use the draft-major queue to keep `draft` status explicit:

```bash
python scripts/draft_major_review_queue.py
```

This report shows:

- how many major entries are still in `draft`
- which doctrinal tags dominate the queue
- which specific headwords still need a pass

Use JSON output if you want to archive or compare the queue over time:

```bash
python scripts/draft_major_review_queue.py --format json
```

## Working Rule

If a major entry is good enough to guide real translation work today but still open to refinement, prefer `reviewed`.

If the team would currently want downstream work to follow it as the house default, use `stable`.

If the repository still expects another real editorial pass, leave it at `draft`.
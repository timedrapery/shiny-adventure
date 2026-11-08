# Source-Fidelity Recheck: 2026-11-08 Rulings

Two texts had their source-fidelity sign-off superseded when the 2026-11-08
term rulings changed their wording. Only the lines below changed. Everything
else in each body is identical to the text that was signed off, so a recheck
covers these lines only.

Each Pali segment is quoted from the pinned SuttaCentral Bilara root text. Both
sources were fetched and match their hashes in
[`source-pins.json`](source-pins.json).

Background for both rulings: the
[talk transcripts profile](../docs/dhammarato-talk-transcripts-profile.md) and
the term records [`samma-samadhi`](../terms/major/samma-samadhi.json) and
[`byapada`](../terms/major/byapada.json).

## SN 56.11 — Dhammacakkappavattana Sutta

[Translation](../docs/translations/sn56-11-dhammacakkappavattana-sutta.md) ·
[Notes](../docs/translations/sn56-11-dhammacakkappavattana-sutta-notes.md)

The last factor of the eightfold path changed in both path lists.

**sn56.11:3.3**

> sammādiṭṭhi sammāsaṅkappo sammāvācā sammākammanto sammāājīvo sammāvāyāmo
> sammāsati sammāsamādhi.

- Signed-off English: `right composure`
- Current English: `right unification of mind`

**sn56.11:4.10**

> sammādiṭṭhi …pe… sammāsamādhi.

- Signed-off English: `right composure`
- Current English: `right unification of mind`

Check: does `right unification of mind` render `sammāsamādhi` in this list?
The record governs it as the mind gathered together and unified, not
one-pointed focus.

## AN 3.65 — Kesamutta Sutta

[Translation](../docs/translations/an3-65-kesamutta-sutta.md) ·
[Notes](../docs/translations/an3-65-kesamutta-sutta-notes.md)

One word changed in the noble disciple's description.

**an3.65:42.1** (opening of the segment)

> Sa kho so, kālāmā, ariyasāvako evaṁ vigatābhijjho vigatabyāpādo asammūḷho
> sampajāno patissato …

- Signed-off English: `free of coveting, free of aversive distraction,
  unconfused, clearly knowing and remembering`
- Current English: `free of coveting, free of ill will, unconfused, clearly
  knowing and remembering`

Check: does `free of ill will` render `vigatabyāpādo`? The record governs
`byāpāda` as `ill will`, which also matches `abyāpāda` (non-ill-will).

## Recording the result

If a line passes, record it in
[`newcomer-review-ledger.json`](newcomer-review-ledger.json) by replacing the
surface's `source_fidelity` block with a completed sign-off, in the same
shape the other completed sign-offs use:

| Surface | Body reviewed (`body_sha256`) |
| --- | --- |
| `sn56_11` | `eb6d3157db74759051e539229541662de48d9d91cb3460b169708b3842b445de` |
| `an3_65` | `54ad464a9de6ff0a6fceb17ff684129dda50416f5dce2f44c07bbaf6d4b0edb7` |

```json
"source_fidelity": {
  "status": "complete",
  "completed_on": "YYYY-MM-DD",
  "evidence": "reviews/source-fidelity-recheck-2026-11-08.md",
  "body_sha256": "<hash from the table above>",
  "bound_by": "recheck of the 2026-11-08 changed lines against the pinned Bilara root"
}
```

Then run `python scripts/check_newcomer_reviews.py` to confirm the gate is
bound to the published body.

If a line fails, leave the gate `pending` and open a translation issue naming
the segment, so the wording can be corrected before the gate is signed again.

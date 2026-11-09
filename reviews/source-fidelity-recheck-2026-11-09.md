# Source-Fidelity Recheck: 2026-11-09 Neutral Feeling

One cohort text, SN 36.6, had its source-fidelity sign-off and its read-aloud
review superseded on 2026-11-09, when the third feeling register changed from
`mixed feeling` to `neutral feeling`. Only the lines below changed. Everything
else in the body is identical to the text that was signed off, so a recheck
covers these lines only.

Each Pali segment is quoted from the SuttaCentral Bilara root text.

Background: the term record
[`adukkhamasukha-vedana`](../terms/minor/adukkhamasukha-vedana.json). The Pali
says `neither painful nor pleasant`. In ordinary English `mixed feelings` means
feeling two ways at once, which the Pali does not say.

## SN 36.6 — Salla Sutta

[Translation](../docs/translations/sn36-6-salla-sutta.md) ·
[Notes](../docs/translations/sn36-6-salla-sutta-notes.md)

**sn36.6:1.1**

> Assutavā, bhikkhave, puthujjano sukhampi vedanaṁ vedayati, dukkhampi vedanaṁ
> vedayati, adukkhamasukhampi vedanaṁ vedayati.

- Signed-off English: `feels pleasant, painful, and mixed feelings`
- Current English: `feels pleasant, painful, and neutral feelings`

**sn36.6:1.2**

> Sutavā, bhikkhave, ariyasāvako sukhampi vedanaṁ vedayati, dukkhampi vedanaṁ
> vedayati, adukkhamasukhampi vedanaṁ vedayati.

- Signed-off English: `feels pleasant, painful, and mixed feelings too`
- Current English: `feels pleasant, painful, and neutral feelings too`

**sn36.6:1.21** and **sn36.6:3.14**

> … yo adukkhamasukhāya vedanāya avijjānusayo, so anuseti.
>
> … yo adukkhamasukhāya vedanāya avijjānusayo, so nānuseti.

- Signed-off English: `the underlying tendency toward ignorance in mixed
  feeling`
- Current English: `the underlying tendency toward ignorance in neutral
  feeling`

**sn36.6:1.24** and **sn36.6:3.17**

> Adukkhamasukhañce vedanaṁ vedayati, saññutto naṁ vedayati.
>
> Adukkhamasukhañce vedanaṁ vedayati, visaññutto naṁ vedayati.

- Signed-off English: `If they feel a mixed feeling`
- Current English: `If they feel a neutral feeling`

Check: does `neutral feeling` render `adukkhamasukhā vedanā` in these lines?

## Recording the result

If the lines pass, record it in
[`newcomer-review-ledger.json`](newcomer-review-ledger.json) by replacing the
surface's `source_fidelity` block with a completed sign-off:

| Surface | Body reviewed (`body_sha256`) |
| --- | --- |
| `sn36_6` | `096b106691120022d95cc9e3cfdb948b3523a1a064d61c6125a2bad4cf015993` |

```json
"source_fidelity": {
  "status": "complete",
  "completed_on": "YYYY-MM-DD",
  "evidence": "reviews/source-fidelity-recheck-2026-11-09.md",
  "body_sha256": "<hash from the table above>",
  "bound_by": "recheck of the 2026-11-09 changed lines against the Bilara root"
}
```

The read-aloud gate is also open again. The 2026-09-17 review is kept in the
ledger under `superseded_reviews` and no longer counts. A new read-aloud pass
needs one reviewer and about five minutes:
`python scripts/read_aloud_kit.py --surface sn36_6`.

Then run `python scripts/check_newcomer_reviews.py` to confirm the gates are
bound to the published body.

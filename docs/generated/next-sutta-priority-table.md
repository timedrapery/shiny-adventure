# Next Sutta Priority Table

Snapshot: 2026-08-25, after completing AN 11.12 and correcting two false
source signals.

The corpus has 1,155 term records and 61 translation surfaces. Of 633 cited
records, 532 are anchored by a translated surface and 101 are orphaned; 9 of
those orphans are major terms. Use the
[Wave 10 execution plan](../wave-10-execution-plan.md) for the active queue,
validation, and handoff gates, and the
[full roadmap](../next-suttas-roadmap.md) for historical method notes.

| Queue | Sutta | Pali length | Orphan major | Reader and policy value |
| ---: | --- | ---: | --- | --- |
| complete | `SN 45.8` Vibhaṅga | 300 words | `ariya` | published 2026-08-25; path-factor cluster now has no dark governed terms |
| complete | `SN 12.44` Loka | 182 words | `loka` | published 2026-08-25; connects lived sensory experience to dependent arising |
| complete | `AN 3.88` Tatiyasikkhā | 230 words | `adhicitta` | published 2026-08-25; threefold training; replaces the false AN 4.41 leverage signal |
| complete | `Iti 49` Diṭṭhigata | 173 words | `pariyuṭṭhāna` | active takeover by views; abandonment-sequence cluster |
| complete | `AN 11.12` Dutiyamahānāma | 367 words | — | six verified recollection anchors; practice while moving, working, or at home |
| 1 | `SN 12.20` Paccaya | 355 words | — | five orphan anchors in a substantive dependent-arising text |
| 2 | `AN 8.39` Abhisanda | 268 words | — | two orphan anchors in a manageable ethics and consequence text |
| 3 | `SN 46.1` Himavanta | 125 words | — | one orphan anchor and a compact awakening-factor practice |

Direct inspection found that SN 55.30 contains `ariyasāvaka` and an
abbreviated Saṅgha formula, not `ariyapuggala`; it is not a priority anchor.
AN 11.12 contains six of its seven credited recollection terms, not
`upasamānussati`; that term belongs to the AN 1.296-305 list. SN 50.1 and
other enumeration or peyyāla stubs remain
formula or cluster-sheet work rather than reader translations. Longer
one-anchor candidates such as DN 21 and DN 1 remain deferred.

Reproduce the numbers:

```bash
python scripts/audit_surface_leverage.py --top 20
python scripts/verify_example_sources.py --strict --top 30
```

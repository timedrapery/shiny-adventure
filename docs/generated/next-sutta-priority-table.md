# Next Sutta Priority Table

Snapshot: 2026-08-25, after publishing the first Wave 9 surface.

The corpus has 1,155 term records and 56 translation surfaces. Of 633 cited
records, 523 are anchored by a translated surface and 110 are orphaned; 12 of
those orphans are major terms.
Use the [Wave 9 execution plan](../wave-9-execution-plan.md) for the committed
order and delivery gates, and the
[full roadmap](../next-suttas-roadmap.md) for historical method notes.

| Queue | Sutta | Pali length | Orphan major | Reader and policy value |
| ---: | --- | ---: | --- | --- |
| complete | `SN 45.8` Vibhaṅga | 300 words | `ariya` | published 2026-08-25; path-factor cluster now has no dark governed terms |
| 1 | `SN 12.44` Loka | 182 words | `loka` | world arising and ending through lived sensory experience |
| 2 | `AN 3.88` Tatiyasikkhā | 230 words | `adhicitta` | threefold training; replaces the false AN 4.41 leverage signal |
| 3 | `Iti 49` Diṭṭhigata | 173 words | `pariyuṭṭhāna` | active takeover by views; abandonment-sequence cluster |

Fallback: `SN 35.82` is an 85-word alternate anchor for `loka`. Longer
one-anchor candidates such as DN 21 and DN 1 are deferred. Enumeration and
peyyāla stubs remain formula or cluster-sheet work unless hand inspection
shows a genuinely substantive short text.

Reproduce the numbers:

```bash
python scripts/audit_surface_leverage.py --top 20
python scripts/verify_example_sources.py --strict --top 30
```

# Next Sutta Priority Table

Snapshot: 2026-08-25, after drafting all four Wave 9 surfaces and adding SN
56.17 by direct request.

The corpus has 1,155 term records and 60 translation surfaces. Of 633 cited
records, 526 are anchored by a translated surface and 107 are orphaned; 9 of
those orphans are major terms. Wave 9 is complete in content. Use the
[Wave 9 execution plan](../wave-9-execution-plan.md) for its remaining
validation and publication gates, and the
[full roadmap](../next-suttas-roadmap.md) for historical method notes.

| Queue | Sutta | Pali length | Orphan major | Reader and policy value |
| ---: | --- | ---: | --- | --- |
| complete | `SN 45.8` Vibhaṅga | 300 words | `ariya` | published 2026-08-25; path-factor cluster now has no dark governed terms |
| complete | `SN 12.44` Loka | 182 words | `loka` | published 2026-08-25; connects lived sensory experience to dependent arising |
| complete | `AN 3.88` Tatiyasikkhā | 230 words | `adhicitta` | published 2026-08-25; threefold training; replaces the false AN 4.41 leverage signal |
| complete | `Iti 49` Diṭṭhigata | 173 words | `pariyuṭṭhāna` | active takeover by views; abandonment-sequence cluster |

The strongest verified next-wave candidate is `AN 11.12`: 367 Pali words with
seven orphan term anchors and a practical sequence built around recollection.
Before committing that queue, inspect the unverified `SN 55.30` source boundary
because it may provide a shorter running-text anchor for the orphan major
`ariya-puggala`. Longer one-anchor candidates such as DN 21 and DN 1 remain
deferred. `SN 50.1` and other enumeration or peyyāla stubs remain formula or
cluster-sheet work rather than reader translations.

Reproduce the numbers:

```bash
python scripts/audit_surface_leverage.py --top 20
python scripts/verify_example_sources.py --strict --top 30
```

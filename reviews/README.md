# Newcomer Review Workboard

This workboard turns the
[newcomer comprehension protocol](../docs/newcomer-review-protocol.md) into a
handoff-ready queue. The JSON ledger remains authoritative; this page is the
human-readable operating view.

Current state: **0 of 35 newcomer sessions recorded** and **0 of 7 read-aloud
reviews complete**. Source-fidelity review is complete for every cohort text.

| Text | Public reader page | Read aloud | Newcomers | Passing threshold |
| --- | --- | --- | ---: | ---: |
| AN 3.65 | [How to Test a Teaching](https://timedrapery.github.io/shiny-adventure/suttas/an3-65-kesamutta-sutta/) | pending | 0/5 | 0/4 |
| SN 56.11 | [The First Teaching](https://timedrapery.github.io/shiny-adventure/suttas/sn56-11-dhammacakkappavattana-sutta/) | pending | 0/5 | 0/4 |
| SN 36.6 | [One Arrow, Not Two](https://timedrapery.github.io/shiny-adventure/suttas/sn36-6-salla-sutta/) | pending | 0/5 | 0/4 |
| MN 63 | [The Man Struck by a Poisoned Arrow](https://timedrapery.github.io/shiny-adventure/suttas/mn63-culamalukya-sutta/) | pending | 0/5 | 0/4 |
| SN 22.59 | [What Is Fit to Call Self?](https://timedrapery.github.io/shiny-adventure/suttas/sn22-59-anattalakkhana-sutta/) | pending | 0/5 | 0/4 |
| MN 131 | [Don't Chase the Past or Long for the Future](https://timedrapery.github.io/shiny-adventure/suttas/mn131-bhaddekaratta-sutta/) | pending | 0/5 | 0/4 |
| SN 22.86 | [Can You Pin Down the Tathāgata?](https://timedrapery.github.io/shiny-adventure/suttas/sn22-86-anuradha-sutta/) | pending | 0/5 | 0/4 |

## Next Action

Recruit one participant at a time and use the public page without showing the
translation notes. Record only anonymous labels and the evidence required by
the protocol. A review that happened but was not recorded is not a completed
gate.

For each text:

1. Complete one full read-aloud pass and record any sentence that is hard to
   say or understand on first hearing.
2. Run five independent newcomer sessions.
3. Enter each unprompted paraphrase and any confusing words in
   `newcomer-review-ledger.json`.
4. Run `python scripts/check_newcomer_reviews.py`.
5. Revise the translation if the evidence shows a recurring problem, update
   its body hash, and repeat affected reviews.

Do not invent, summarize from memory, or backfill participant evidence. Do not
put names, contact details, or demographic data in this repository. Change a
surface to `validated` only when the machine check confirms every required
gate.

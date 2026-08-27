# Newcomer Review Workboard

This workboard turns the
[newcomer comprehension protocol](../docs/newcomer-review-protocol.md) into a
handoff-ready queue. The JSON ledger remains authoritative; this page is the
human-readable operating view.

Current state: **0 of 60 newcomer sessions recorded** and **0 of 12 read-aloud
reviews complete**. Source-fidelity review is complete for every cohort text.

## Three-text pilot — do these first

| Text | Public reader page | Read aloud | Newcomers | Passing threshold |
| --- | --- | --- | ---: | ---: |
| AN 2.9 | [What Keeps the World Human](https://timedrapery.github.io/shiny-adventure/suttas/an2-9-cariya-sutta/) | pending | 0/5 | 0/4 |
| SN 36.6 | [One Arrow, Not Two](https://timedrapery.github.io/shiny-adventure/suttas/sn36-6-salla-sutta/) | pending | 0/5 | 0/4 |
| AN 3.65 | [How to Test a Teaching](https://timedrapery.github.io/shiny-adventure/suttas/an3-65-kesamutta-sutta/) | pending | 0/5 | 0/4 |

Use the [printable pilot session sheet](pilot-session-sheet.md). Finish and
evaluate this pilot before recruiting for the remaining nine texts.

## Remaining First 12

| Text | Public reader page | Read aloud | Newcomers | Passing threshold |
| --- | --- | --- | ---: | ---: |
| SN 45.2 | [Good Friendship Is the Whole Path](https://timedrapery.github.io/shiny-adventure/suttas/sn45-2-upaddha-sutta/) | pending | 0/5 | 0/4 |
| SN 56.17 | [What Ignorance Means](https://timedrapery.github.io/shiny-adventure/suttas/sn56-17-avijja-sutta/) | pending | 0/5 | 0/4 |
| AN 8.6 | [When Life Goes Up and Down](https://timedrapery.github.io/shiny-adventure/suttas/an8-6-dutiyalokadhamma-sutta/) | pending | 0/5 | 0/4 |
| AN 11.12 | [Six Things to Remember Anywhere](https://timedrapery.github.io/shiny-adventure/suttas/an11-12-dutiyamahanama-sutta/) | pending | 0/5 | 0/4 |
| MN 63 | [The Man Struck by a Poisoned Arrow](https://timedrapery.github.io/shiny-adventure/suttas/mn63-culamalukya-sutta/) | pending | 0/5 | 0/4 |
| SN 56.11 | [The First Teaching](https://timedrapery.github.io/shiny-adventure/suttas/sn56-11-dhammacakkappavattana-sutta/) | pending | 0/5 | 0/4 |
| SN 22.59 | [What Is Fit to Call Self?](https://timedrapery.github.io/shiny-adventure/suttas/sn22-59-anattalakkhana-sutta/) | pending | 0/5 | 0/4 |
| MN 19 | [Two Kinds of Thinking](https://timedrapery.github.io/shiny-adventure/suttas/mn19-dvedhavitakka-sutta/) | pending | 0/5 | 0/4 |
| SN 12.44 | [How the World Arises—and Ends](https://timedrapery.github.io/shiny-adventure/suttas/sn12-44-loka-sutta/) | pending | 0/5 | 0/4 |

## Recording a completed session

For each text:

1. Give the participant the public page without translation notes or coaching.
2. Ask the questions in the protocol and record the answers on the session
   sheet.
3. Enter only the anonymous evidence fields in
   `newcomer-review-ledger.json`.
4. Complete one independent, full read-aloud pass and record hard-to-say or
   hard-to-hear sentences.
5. Run `python scripts/check_newcomer_reviews.py`.
6. Revise only when evidence shows a recurring problem, update the body hash
   when translation wording changes, and repeat affected reviews.

Do not invent, summarize from memory, or backfill participant evidence. Do not
put names, contact details, demographic data, or private recruiting notes in
this repository. Change a surface to `validated` only when the machine check
confirms every required gate.

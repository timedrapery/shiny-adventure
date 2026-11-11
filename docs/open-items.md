# Open Items

The standing editorial rulings, the decisions still waiting, and the next
pieces of work, in one place. Remove an item when it is done and record the
change in `CHANGELOG.md`.

## Standing editorial rulings

- **House terms stay.** Plain-English work changes the sentences around the
  OSF glossary terms, not the terms. `ignorant wanting`, `taking personally`,
  `quenching`, `felt experience`, `unification of mind`, `putting things
  together`, `heap`, `bhikkhu`, `Bhante`, and `Tathāgata` remain in the
  translations.
- **`mixed feeling` stays** for `adukkhamasukhā vedanā`. `neutral feeling` is
  inaccurate: the third register is still something felt, not an absence of
  feeling. Do not propose `neutral` again.
- **Taṇhā for newcomers** is explained as "wanting something you can't have
  right now". That phrase opens the `ignorant wanting` definition in
  [`includes/glossary.md`](../includes/glossary.md) and is a context rule on
  [`terms/major/tanha.json`](../terms/major/tanha.json). It is not used inside
  a translated sutta, because it cannot carry the compounds or the
  dependent-arising chain.

## Decisions needed

1. **`samaṇa` in AN 8.39.** Its notes declare `ascetics and brahmins` against
   the record's `recluse`.
2. **Old GitHub records.** Pull requests #1 to #46 and the workflow runs
   before 2026-11-10 still show commit details from before that day's history
   rewrite. GitHub does not let them be edited. Recreating the repository
   under the same name and pushing the current history is the only way to
   clear them; GitHub Pages then has to be switched back on, and stars,
   watchers, and issues are lost.
3. **The dependent-arising chain.** Lines such as `with putting things
   together as condition, knowing` and the 129-word quenching chain are the
   hardest sentences left. Every link is a governed phrase record, so this
   needs a ruling, not a sentence repair. A verb version would read `When
   ignorance completely fades and quenches, putting things together
   quenches.`
4. **`abhijjhā` in MN 39.** MN 39 renders `abhijjhādomanassa` as
   `covetousness and displeasure`, while the `abhijjhā` record and MN 10 use
   `coveting` (MN 10: `coveting and distress`). Decide whether MN 39 should
   follow, which would change about five sentences.

## Human review

All 80 surfaces are `provisional`. Against the published bodies the ledger
(`reviews/newcomer-review-ledger.json`) shows 0 of 60 newcomer sessions, 4 of
12 read-aloud reviews (AN 2.9, SN 36.6, AN 8.6, SN 56.17), and 2 of 12 source-fidelity
sign-offs (SN 36.6, SN 22.59). The automated checks establish structure and
consistency, not accuracy or comprehension.

- Read the First 12 aloud: one reviewer, about an hour, with
  `python scripts/read_aloud_kit.py --surface <key>`.
- Run the three-text newcomer pilot in [`reviews/README.md`](../reviews/README.md).
- SN 22.59 and SN 36.6 still carry older sentence patterns
  (`Seeing this, bhikkhus, a learned noble disciple ...`,
  `Being disenchanted, they fade.`) because their bodies hold bound review
  evidence. Bring them into line when their sign-offs are redone, in the same
  sitting.

## Next work

### Translations and reader

1. Make the `Before you read` guides plainer, using the taṇhā definition as the
   model: the plain thing first, the house term second.
2. Write a phrase record for the four-directions friendliness formula and unify
   AN 3.65, MN 7, MN 43, and MN 99 on the AN 3.65 wording.
3. Choose the next translation queue; it needs a fresh audit before any sutta
   is given a position.

### Tooling

1. `scripts/text_utils.safe_text` escapes every Pali diacritic in reports
   (`abhijjhā`) even on a UTF-8 terminal. Escape only what the output
   stream cannot encode.

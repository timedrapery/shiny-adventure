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

1. **Protect `main`.** Require the CI check to pass before merge. Nothing
   currently stops a pull request merging before its checks finish.
2. **Formula disagreements.** 29 are acknowledged in
   `reviews/formula-baseline.json`. About half differ only in articles
   (`the first mental theme` / `first mental theme`). The rest use different
   words for the same Pali and need a ruling, for example `coveting` /
   `covetousness`; `the internal fields` / `the internal sense fields`;
   `nibbāna is the highest ease` / `the highest satisfaction`;
   `all constructed things` / `all that has been put together`;
   `establishment of remembering` / `establishment of sati`;
   `knowing and seeing of release` / `knowledge and vision of release`;
   `guarding the faculties` / `sense restraint`;
   `without remainder` / `without fuel remaining`.
3. **`samaṇa` in AN 8.39.** Its notes declare `ascetics and brahmins` against
   the record's `recluse`.
4. **Unbound source-fidelity claims.** Outside the pilot cohort, 14 notes files
   say source-fidelity review is complete with no ledger record behind them.
   Decide what those lines should say.
5. **The dependent-arising chain.** Lines such as `with putting things
   together as condition, knowing` and the 129-word quenching chain are the
   hardest sentences left. Every link is a governed phrase record, so this
   needs a ruling, not a sentence repair. A verb version would read `When
   ignorance completely fades and quenches, putting things together
   quenches.`

## Human review

All 80 surfaces are `provisional`. Against the published bodies the ledger
(`reviews/newcomer-review-ledger.json`) shows 0 of 60 newcomer sessions, 2 of
12 read-aloud reviews (AN 2.9, SN 36.6), and 2 of 12 source-fidelity
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

### Feedback service

1. **Import timestamps** in `feedback_service/ingest.py`: `03/04/2026` always
   parses month-first, sheet-local time is stamped as UTC, and an unrecognised
   format silently becomes the import time. Record the sheet's time zone and
   date order explicitly and keep a note when a stamp cannot be parsed. Done
   when a `dd/mm` sheet and an unparseable stamp each have a test.
2. **Closed sessions.** Import accepts a formal response for a closed session;
   the live endpoint refuses it. Make them agree, with one test covering both.
3. **Staging.** `scripts/stage_feedback_evidence.py` copies the body hash a
   client asserted, matches a returning reader by label only, and will stage a
   back-dated record as history, which `docs/reader-feedback-plan.md` says is
   refused. Make the two agree and match on session as well as label.
4. An edited "Send again" reuses the same submission id, so the first version
   wins.
5. A non-ASCII CSRF value returns 500 (authenticated only). The admin form
   accepts session keys and labels the validator later rejects.

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

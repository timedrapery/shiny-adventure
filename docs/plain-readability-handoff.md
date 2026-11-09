# Plain Readability Pass: Handoff Notes

Written 2026-11-09 at the end of a working session. Read this first when the
work is picked up again. It says what was decided, what was changed, what was
deliberately left alone, and what to do next.

## The decision that governs this work

The owner was asked how far plain English should override the OSF glossary in
the translated text. The answer was: **keep all house terms.**

So `ignorant wanting`, `taking personally`, `quenching`, `felt experience`,
`unification of mind`, `putting things together`, `heap`, `bhikkhu`, `Bhante`,
and `Tathāgata` all stay in the translations. The readability work is on the
sentences around those terms, and on the reader guides.

Two related rulings.

**`mixed feeling` stays.** `adukkhamasukhā vedanā` was changed to `neutral
feeling` during this pass and changed back the same day: the owner ruled that
`neutral feeling` is inaccurate. The third register is still something felt,
not a flat absence of feeling. Do not propose `neutral` again.

The second ruling: the owner asked that taṇhā be explained to newcomers as
**"wanting something you can't have right now"**. That phrase is now the first
sentence of the `ignorant wanting` definition in
[`includes/glossary.md`](../includes/glossary.md), which feeds the glossary
page, the key-words panels, and the tooltips. It is recorded as a context rule
on [`terms/major/tanha.json`](../terms/major/tanha.json). It is not used
inside a translated sutta, because it cannot carry the compounds or the
dependent-arising chain.

## What changed in this pass

1. **One error fixed.** SN 45.2 had one `right intention`; it is now the
   governed `right attitude`.
2. **Forms of address moved out of the middle of the sentence.**
   `This too, bhikkhus, is ...` became `Bhikkhus, this too is ...`, and
   `And what, friends, is birth?` became `And what is birth, friends?`. The
   spoken-register profile's mid-clause share went from 48.8% to 16.5%.
3. **The bare `Here` opener is gone.** `Here a bhikkhu ...` and
   `Here, Ānanda, a bhikkhu ...` now start with the person.
4. **`Having ...ed` clauses rewritten as ordinary sentences**, about sixty of
   them. The remembering-practice refrain now ends `and with coveting and
   distress about the world put aside`, and its record
   (`mn10-satipatthana-qualifier`) and the practice-text report were updated
   to match.
5. **The release declaration is one formula again.** MN 22, SN 35.28, and
   MN 39 had drifted to `Birth is finished ... nothing further for this`. They
   now use the governed `Birth is worn away ... there is no more of this state
   of being`.
6. **`they fade` became `their passion fades`** in MN 148, SN 12.61, SN 22.86,
   MN 22, and SN 35.28, and SN 12.61's `might well fade toward it` was
   rewritten. A person fading is not what the Pali says.
7. **Smaller repairs:** the last generic `one`; `upon`, `shall`,
   `possessed of`, `endowed with`; `ageing` spelled one way; the AN 3.65
   four-directions passage; the MN 63 arrow speech split into sentences; the
   MN 10 grain-bag and MN 121 mansion similes; the MN 137 `with reference to`
   refrain; MN 61 `is certainly not to be done`.

The full suite (`python scripts/run_checks.py`) passes.

## What was deliberately left alone

- **SN 22.59, AN 2.9, and SN 36.6 were not edited.** They hold the only human
  review evidence still bound to a published body (source-fidelity sign-offs
  for SN 22.59 and SN 36.6, read-aloud reviews for AN 2.9 and SN 36.6), and several tests expect at least
  one bound sign-off to exist. As a result SN 22.59 still says
  `Seeing this, bhikkhus, a learned noble disciple ...` and
  `Being disenchanted, they fade. Through fading, they are released.` while
  its sister texts have the new wording. Bring it into line the next time its
  sign-off is being redone anyway.
- **The dependent-arising chain was not restructured.** Lines such as
  `with putting things together as condition, knowing` and the 129-word
  quenching chain are the hardest sentences left in the corpus, but every link
  is a governed phrase record with tests and cluster reports behind it. This
  needs an owner ruling, not a sentence repair. A verb version would read
  `When ignorance completely fades and quenches, putting things together
  quenches.`
- **Contractions.** Dialogue is contracted 1.5% of the time. The standard
  says to judge this by ear, not to run a replacement, so it was not touched.
- **The four-directions friendliness formula** is still worded four different
  ways across AN 3.65, MN 7, MN 43, and MN 99. Only AN 3.65 was repaired. No
  record governs it yet.
- **Newcomer guides and reader introductions** were not rewritten, apart from
  the taṇhā definition. This was planned and not reached.

## What to do next, in order

1. Decide the dependent-arising chain (see above). It is the single largest
   readability gain available without changing a house term.
2. Read the First 12 aloud. Nine of the twelve changed in this pass; the
   read-aloud gates for AN 2.9 and SN 36.6 are complete. One reviewer, about an hour:
   `python scripts/read_aloud_kit.py --surface <key>`.
3. Bring SN 22.59 and SN 36.6 into line with the new sentence patterns and
   redo their sign-offs in the same sitting.
4. Make the `Before you read` guides plainer, using the taṇhā definition as
   the model: say the plain thing first, name the house term second.
5. Write a phrase record for the four-directions formula and unify the four
   surfaces on the AN 3.65 wording.
6. Run the three-text newcomer pilot in
   [`reviews/README.md`](../reviews/README.md). Zero newcomer sessions have
   been recorded, and that is the only test of whether any of this worked.

## How to make a corpus-wide wording change safely

Edit `docs/translations/*.md` (never `reader-src/`, which is generated), and
change any term record, script constant, or test that quotes the old wording.
Then refresh every derived file, in this order:

```bash
# 1. body hashes: update READABILITY_BODY_SHA256 in scripts/surface_registry.py
#    to match scripts/check_readability_reviews.translation_body_sha256()
python scripts/paragraph_ids.py --write
python scripts/generate_reader.py --write
for f in scripts/*_report.py scripts/term_directory_navigation.py \
         scripts/translation_surface_index.py; do
  grep -q -- '"--write-docs"' "$f" && python "$f" --write-docs
done
python scripts/health_dashboard.py --write
python scripts/next_sutta_priority_report.py --write
python scripts/run_checks.py
```

Things that will bite:

- A changed body makes any ledger evidence bound to its old hash fail the
  newcomer-review check. Reopen the gate honestly (see how `sn36_6` is
  recorded in `reviews/newcomer-review-ledger.json`); never edit an old hash.
- Translations are hard-wrapped at about 79 columns, but verse paragraphs and
  a few files (MN 1, MN 148, MN 26, MN 36) are not. Rewrap prose only.
- `scripts/practice_text_surface_report.py` and several cluster reports hold
  exact sentences as constants. A reworded formula must be changed there too,
  or the practice-text test fails with `missing governed control line`.
- Aim a pass with `python scripts/plain_english_audit.py --spoken`. Its
  shared-unit list shows which sentences are heard most often.

# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project follows Semantic Versioning where versioning is used.

## [Unreleased]

### Added

- Added a governed plain-English translation of Ud 8.3,
  Tatiyanibbānapaṭisaṁyutta Sutta, with companion notes, a reader
  introduction, reader metadata, and a generated reader page placed at the end
  of set 5 beside Iti 44. At 139 English words it is the shortest page in the
  collection, and it makes one conditional argument: there would be no
  discernible escape from what is born, become, made and conditioned unless
  there were something that is not. Wave 11 item 2, taken first because item 1
  carries a precondition. Anchors `asaṅkhata-dhātu`; corpus orphans 85 to 84.
- Added three reader glosses (conditioned, unconditioned) and generalised a
  fourth: the `escape` gloss described `nissaraṇa` only as a way out of a
  feeling, which was true on SN 36.6 and wrong on every other page that uses
  the word.

- Added the [Wave 11 execution plan](docs/wave-11-execution-plan.md), written
  from a fresh audit rather than by extending Wave 10's spent ranking. Its
  queue is Dhp 21-32, Ud 8.3, SN 22.22, SN 22.26, and MN 122; every signal was
  checked against the cached root text before the item was given a position.
  The plan also records what is permanently off the queue and why, so the next
  audit does not re-propose it.

- Added a governed plain-English translation of SN 46.1, Himavanta Sutta, with
  companion notes, a reader introduction, reader metadata, and a generated
  reader page placed at the end of stage 3, beside SN 46.51. Nāgas grow on the
  Himalaya until they are big enough to go down through the pools and rivers
  into the ocean; conduct is put in the mountain's place, as what the seven
  awakening factors get large on. **This completes Wave 10.**
- Added seven reader glosses (nāgas, conduct, seclusion, relinquishment,
  discernment of qualities, rejoicing, relaxation), which close tooltip gaps
  across the awakening-factor and jhāna surfaces, not only this page.

- Added a governed plain-English translation of AN 8.39, Abhisanda Sutta, with
  companion notes, a reader introduction, reader metadata, and a generated
  reader page placed in stage 2 after AN 2.9. The discourse counts the three
  refuges and the five abstentions as eight streams of benefit, and describes
  each abstention as a gift: someone who has given up killing, stealing,
  betrayal, lying, or drunken recklessness has given every other being freedom
  from fear, freedom from enmity, and freedom from affliction, and comes to
  share in that freedom without limit. Both of its ranked orphan signals,
  `kāmesu-micchācāra` and `surāmeraya-majjapamādaṭṭhāna`, are anchored in
  running text, and `dāna`, `saraṇa`, and `saṅgha` are closed along the way.
  Corpus orphans 96 to 91.
- Added two minor phrase records the AN 8.39 translation needed:
  `puññābhisando kusalābhisando`, which holds `benefit` and `wholesome` to
  their own governed headwords across the discourse's signature compound, and
  `abhayaṁ averaṁ abyābajjhaṁ`, which fixes one `freedom from` frame for all
  three members of the triad. `dāna` gains a context rule for the countable
  sense, since `five generosities` is not English.
- Added `scripts/next_sutta_priority_report.py`, so
  `docs/generated/next-sutta-priority-table.md` is generated from the live
  corpus instead of written by hand into `docs/generated/`, where nothing
  regenerated it. The committed file had drifted to 61 surfaces and 101
  orphans against an actual 64 and 91, and still listed a finished text as the
  next item. `check_generated_docs.py` now fails when it drifts again.

- Added a reader feedback system, enabled on the three pilot texts (SN 36.6, AN 2.9, AN 3.65). Each passage of
  an enabled translation gets a discreet, keyboard- and screen-reader-operable
  "Give feedback" control; the words-used panel asks whether each explanation
  helped; and an optional comprehension review closes the page. Submissions
  carry the surface, stable passage id, exact wording shown, translation body
  hash, governed term ids with their mapping basis, glossary and introduction
  versions, and the question set version. A standard-library submission
  service (`feedback_service/`) stores them in SQLite behind validation,
  rate limiting, and honeypot checks, and gives maintainers an authenticated
  queue with a five-step editorial lifecycle, per-term grouping, formal
  review sessions, and a reviewed export that
  `scripts/stage_feedback_evidence.py` checks into the newcomer ledger. See
  [docs/reader-feedback-system.md](docs/reader-feedback-system.md).
- Added stable passage identifiers (`scripts/paragraph_ids.py`,
  `includes/feedback/paragraph-ids/`) with documented split and merge
  behaviour, an editor-written term map for SN 36.6, and draft comprehension
  question sets with assessment guidance for AN 2.9, SN 36.6, and AN 3.65.
  The question sets are drafts awaiting editorial review.
- Added a facilitator guide for real newcomer sessions
  ([reviews/facilitator-guide.md](reviews/facilitator-guide.md)).

- Added a governed plain-English translation of MN 36, Mahāsaccaka Sutta, by
  direct request, with companion notes, a reader introduction, reader
  metadata, and a generated reader page placed in stage 3 after MN 19. Saccaka
  claims some practitioners train the body and others the mind; the Buddha
  answers with a single test, whether pleasant or painful feeling takes over
  the heart, and then with his own account of the two teachers, the
  austerities, the remembered first mental theme, and the three knowledges.
- Added a governed plain-English translation of SN 12.20, Paccaya Sutta, with
  companion notes, a reader introduction, reader metadata, and a generated
  reader page. The discourse separates dependent arising, the pattern, from
  the things that arise dependently, the changing items the pattern runs
  through, and closes with why someone who sees this stops asking what they
  were and what they will be.
- Added reader glosses for `becoming`, `dependently arisen`, `conditionality`,
  `stability of the pattern`, `regularity of the pattern`, `suchness`, and
  `right discernment`, closing tooltip gaps that affected the whole
  dependent-arising set rather than only the new page.
- Added a governed plain-English translation of AN 11.12,
  Dutiyamahānāma Sutta, with companion notes, newcomer guidance, reader
  placement as "Six Things to Remember Anywhere," and running-text support
  for six recollection terms.
- Added a durable Wave 10 execution plan with a source-verified queue and a
  restart procedure for continuing on another machine.
- Added a governed plain-English translation of Iti 49, Diṭṭhigata Sutta,
  with companion notes, newcomer guidance, reader placement as "Taken Over by
  Views," and running-text support for `pariyuṭṭhāna` as active takeover.
- Added a governed plain-English translation of SN 56.17, Avijjā Sutta, with
  companion notes, newcomer guidance, an explicit expansion of the abbreviated
  four-truths practice instruction, and reader placement as "What Ignorance
  Means."
- Added a governed plain-English translation of AN 3.88, Tatiyasikkhā Sutta,
  with companion notes, newcomer guidance, a consolidated and readable
  attainment ladder, and direct running-text support for `adhicitta` in the
  threefold training.
- Added a governed plain-English translation of SN 12.44, Loka Sutta, with
  companion notes, newcomer guidance, a complete six-sense presentation of
  the abbreviated source pattern, and direct running-text support for `loka`.
- Added a governed plain-English translation of SN 45.8, Vibhaṅga Sutta, with
  companion notes, a newcomer introduction, complete definitions of all eight
  path factors, and direct running-text support for `ariya`.
- Added governed plain-English translations, companion notes, newcomer
  introductions, and generated reader pages for AN 3.69, AN 4.5, and SN 1.1.
- Added a durable Wave 9 execution plan and newcomer-review workboard so work
  can resume from any clone without relying on chat history.
- Added a governed plain-English translation of AN 2.9, Cariya Sutta, with
  companion source notes, newcomer guidance, reader placement as "What Keeps
  the World Human," and running-text anchors for `hiri` and `ottappa` as
  `conscience` and `moral caution`.
- Added plain contemporary English translations, companion source notes,
  reader introductions, and generated reader pages for SN 45.2, AN 8.6, and
  MN 119.
- Added a newcomer-review protocol and machine-checked seven-sutta cohort
  ledger. Source-fidelity evidence is recorded separately from the still-
  pending human read-aloud and newcomer-comprehension gates.
- Added a progressively enhanced "Find a sutta" page with topic, form,
  reading-stage, difficulty, and length filters, plus reading times throughout
  the discovery lists.
- Added visible source, license, provisional-status, review-date, and content-
  hash disclosures to every sutta page.
- Added Playwright and axe rendered-accessibility checks across every generated
  sutta page, narrow-screen and
  keyboard regressions, EPUB structure validation, and Khuddaka Nikāya source
  resolution for Dhammapada, Itivuttaka, Sutta Nipāta, Theragāthā,
  Therīgāthā, and Udāna citations.
- Added a governed, plain contemporary English translation of SN 22.86,
  Anurādha Sutta, with companion source notes, a controlled rendering of the
  Tathāgata and five-heaps questions, a hand-written newcomer introduction,
  and a generated reader page titled "Can You Pin Down the Tathāgata?"
- Added a governed, plain contemporary English translation of MN 131,
  Bhaddekaratta Sutta, with companion source notes, reusable title policy, a
  hand-written newcomer introduction, and a generated reader page titled
  "Don't Chase the Past or Long for the Future."
- Added project trust and governance files: security policy and code of conduct.
- Added contributor-oriented docs spine for project overview, architecture, development, and usage.
- Added [scripts/README.md](scripts/README.md) as a script index for validation, reporting, and scaffolding tools.
- Added `CITATION.cff` so the repository can be cited as a maintained translation dataset.
- Added a workflow issue template for documentation, reporting, and contributor-experience gaps.
- Added `scripts/draft_major_review_queue.py` to keep remaining draft major entries visible as an explicit review queue.
- Added `scripts/check_docs_integrity.py` to validate internal Markdown links and required repository-surface metadata files.
- Added [docs/review-status-model.md](docs/review-status-model.md) to define how major entries move from draft to reviewed to stable.
- Added neutral readability-review metadata and a checker that locks every
  registered translation body to its documented review state.
- Added structured, source-checked newcomer guides for the Essential Five and
  a reader-accessibility regression checker covering every generated page.
- Added a long-form reader stylesheet with system fonts, visible keyboard
  focus, larger controls, reduced-motion support, mobile reflow, and print
  rules.

### Changed

- Ud 8.3 is the repository's first Udāna surface, and its notes settle the
  collection's framing formula — the occasion, the `imaṁ udānaṁ udānesi`
  line, and the closing marker — as Iti 44 did for the Itivuttaka.
- `generate_reader.py` no longer drops a surface whose collection is missing
  from the All Suttas index's hardcoded list. Adding Ud 8.3 exposed it: the
  page claims to list every translation and silently omitted one. The Udāna is
  now listed, and an unlisted collection raises an error naming it instead of
  vanishing.

- `audit_surface_leverage.py` no longer ranks verse collections by length.
  Once the Dhammapada bundles were cached, it filed Dhp 21 — twelve Pali words,
  and the only running-text anchor for the governed major `appamāda` — as an
  enumeration stub for being short. A verse is the densest substantive text
  there is, not a count followed by a list.
- `next_sutta_priority_report.py` now carries the Wave 11 queue and keeps
  Wave 10's finished rows as history. Queue rows record whether they are
  published as a fact rather than as display text, and the tests check that
  claim against the corpus in both directions.
- Pointed the documentation guide, the roadmap, the README, and the workflow
  plan at the Wave 11 plan. The documentation guide had still been calling the
  Wave 9 plan current, two waves after it was superseded.

- Replaced the auto-scaffolded `nāga` record, whose definition and preferred
  translation were both placeholder text, with a real entry: the word is kept
  in Pali because it covers great serpents and elephants alike and the sources
  usually do not say which, and picking an English animal would resolve an
  ambiguity the source leaves open.
- Marked Wave 10 complete across the plan, the roadmap, the README, and the
  generated priority table. None of them now names a next queue item; all of
  them say the next translation task is a fresh audit, and the Wave 10 plan
  gained a short procedure for running one. `next_sutta_priority_report.py`
  renders a finished queue as finished, and its tests enforce that a queue with
  no next item says so.

- Separated the two kinds of review gate across the planning documents. The
  automated and editorial gates are what a translation must clear to be
  published, as `provisional`; recorded newcomer and read-aloud evidence is an
  open-ended workstream that raises a published surface to `validated`. The
  Wave 10 plan, the newcomer accessibility plan, and the review workboard now
  say so, and none of them tells a contributor to stop translating while the
  ledger is empty. No evidence rule was relaxed: reader evidence still must be
  recorded against the body hash it was gathered against, and must never be
  inferred, simulated, or backfilled.
- Refreshed the stale counts, queue positions, and next-action language in the
  Wave 10 execution plan, the active roadmap, the newcomer accessibility plan,
  the review workboard, and the translation workflow plan. Where a document
  quoted a number that a script can regenerate, it now says which script to
  run instead of inviting the next reader to trust the snapshot.
- Recorded in the Wave 10 plan that `verify_example_sources.py --strict`
  reports `unfetched` for Dhp verse ranges and bundled AN and SN files when
  `https://api.github.com` is unreachable, because that is how the resolver
  finds a bundle. It is a network result rather than a citation problem.

- Set `site_url` in `mkdocs.yml`. Without it, the site's 404 page loaded its
  stylesheets and scripts from the domain root instead of `/shiny-adventure/`,
  so any mistyped or not-yet-deployed address showed an unstyled page with a
  full-screen logo.
- Corrected a false source signal found while auditing MN 36: the discourse
  does not contain `nāparaṃ itthattāyāti pajānāti`. Its first-person
  declaration closes with `abbhaññāsiṁ` (`abhijānāti`). The
  `naparam-itthattayati-pajanati` and `pajanati` records now cite SN 22.86
  for the exact form, `asava` now quotes MN 36's own line naming the three
  outflows, and `abhijanati` gains MN 36 as a running-text example. All three
  old citations had passed the strict verifier as `inflected`.
- Repaired eight citation problems found by the Wave 11 audit, in the records
  it was ranking. Four closed an orphan with no translation at all, because the
  term was already demonstrated in a translated surface: `cāga` cited AN 7.49,
  the Dutiyasaññā Sutta, which has no form of it, and now cites AN 11.12;
  `samatha` and `vipassanā` both cited SN 35.204, a Saṭṭhipeyyāla repetition
  sutta containing neither, and now cite MN 43; `vinaya` cited MN 108, which
  contains no form of it, and now cites MN 11. Three were repaired to a true
  but untranslated source and stay orphaned: `appicchatā` (AN 4.27 to MN 122),
  `diṭṭhadhammanibbāna` (MN 13, which contains no form of `nibbāna` at all, to
  DN 1), and the burden formula, which quoted a singular `bhāro` where SN 22.22
  reads the nominative plural `Bhārā`. The eighth, the Sanskrit `śūnyatā`, lost
  its citation rather than gaining a new one: it cited MN 121, which contains
  `suññatā` and no form of `śūnyatā`, and a Sanskrit form has no Pali
  running-text anchor. Corpus orphans 90 to 85.
- Corrected a sixth false source signal, found while auditing SN 46.1 and the
  first one hidden behind an `inconclusive` verdict rather than an `inflected`
  one. `bojjhaṅga-bhāvanā` and the `bojjhaṅga` major entry both quoted the
  compound `bojjhaṅgabhāvanā` to SN 46.1, which contains no form of `bhāvanā`
  at all. Because the discourse uses peyyāla, the strict verifier returned
  `inconclusive` and could not call it absent. Both records now quote the
  running text `satta bojjhaṅge bhāvento satta bojjhaṅge bahulīkaronto`.
- Aligned two awakening-factor compound records with their own headwords.
  `pītisambojjhaṅga` read `delight awakening factor` while `pīti` records an
  explicit rule that bojjhaṅga contexts take `rejoicing`, and
  `passaddhisambojjhaṅga` read `tranquility awakening factor` while
  `passaddhi` defaults to `relaxation`. Both translation surfaces already
  followed the headwords, so the records were the outliers; nothing caught it,
  because the drift checker compares renderings across related entries rather
  than a compound against the context rule of its own head.
- Corrected a false source signal found while auditing AN 8.39:
  `kāmesu-micchācāra` cited `kāmesu micchācārā veramaṇī` to that discourse,
  which contains no form of `veramaṇī`. It now quotes the discourse's own
  `kāmesumicchācāraṁ pahāya kāmesumicchācārā paṭivirato hoti`. The old
  citation had passed the strict verifier as `inflected`, the same shape as
  the `ariyapuggala`, `upasamānussati`, `dhammatā`, and MN 36 findings.
- Corrected two more false source signals found while auditing SN 12.20:
  `dhammatā` does not occur in that discourse and now cites DN 14, and
  `dhammatthiti` cited a form that was neither the headword nor the source
  form and now cites the exact running-text `dhammaṭṭhitatā`. Both had passed
  the strict verifier as `inflected` or as a prefix match.
- Corrected false source signals for `ariyapuggala` and `upasamānussati`:
  SN 55.30 does not contain the first compound, and AN 11.12 does not contain
  the second; the latter now cites its direct list source at AN 1.296.
- Clarified the `yoga` policy for the distinct `yogo karaṇīyo` effort idiom
  and added SN 56.17's four-truths definition to the governed `avijjā` record.
- Corrected the three-training term examples to use the governed `higher
  conduct` rather than `higher virtue`, and repaired stale AN 3.88 source
  references for `adhipaññā` and `sikkhā`.
- Clarified the reader glossary's `world` entry so it covers the lived world
  built through the senses as well as wider cosmological uses.
- Made per-page glossary generation prefer the longest matching phrase,
  including phrases split by Markdown line wrapping, so a phrase such as
  `clearly knowing` no longer picks up an unrelated gloss for `knowing`.
- Repaired the example-source verifier so partial matches are visible and
  strict mode rejects them; corrected all eight partial citations in the live
  corpus.
- Added a registry-backed documentation check that rejects stale current
  translation-surface counts.
- Corrected the surface-leverage audit so it resolves discourses stored inside
  bundled Bilara cache files, counts only the requested discourse, and does not
  misclassify AN 2.9's short counterfactual argument as a bare enumeration.
- Reconstructed README for clearer onboarding and GitHub discoverability.
- Strengthened GitHub collaboration metadata with issue template configuration and dependency update automation.
- Reworked documentation navigation so task-based workflow entry points are easier to find.
- Expanded usage and development guidance with targeted commands, test examples, and script discovery notes.
- Updated repository review notes to reflect the current health-report state instead of earlier cleanup-era backlog claims.
- Improved `scaffold_policy_metadata.py` so placeholder scaffolding emits an explicit completion warning.
- Extended the full verification suite so documentation and repository-surface integrity are checked alongside tests and term validation.
- Promoted 8 structurally complete major entries from `draft` to `reviewed` after an explicit status pass.
- Extended editorial review guidance with source-fidelity, human read-aloud
  usability, newcomer-comprehension, and reader-template accessibility checks.
- Reframed the corpus-wide sentence-level pass around neutral newcomer
  readability rather than person-specific voice calibration. The completed
  translation improvements and body hashes remain intact while human reviews
  remain pending.
- Reworked all 66 reader pages around a clear `Before you read` / `Translation`
  hierarchy, computed reading times, visible term definitions, semantic reading
  navigation, and plain-English titles; replaced the wide glossary and sutta
  index tables with flowing layouts.

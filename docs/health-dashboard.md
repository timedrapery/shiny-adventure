# Health Dashboard

This document explains the editorial health dashboard: what each number
measures, what it deliberately does not measure, and how to act on it.

The dashboard itself is generated at
[`generated/health-dashboard.md`](generated/health-dashboard.md).

## Purpose

The repository already fails loudly when a record breaks. It had no way to
answer the slower questions:

- How much of the Pali we actually quote is governed at all?
- Where do translation surfaces argue with the records that govern them?
- What has been sitting in a review queue, and since when?
- How often do the schema and lint gates actually catch something?

The dashboard answers those four and nothing else. It is a reporting surface,
not a gate. No number here blocks a merge; the gates stay in
[ci-enforcement.md](ci-enforcement.md).

## Commands

```bash
# Live report, with review-queue ages in days
python scripts/health_dashboard.py --top 20

# The same data as JSON, with full detail lists
python scripts/health_dashboard.py --format json

# Regenerate the committed Markdown
python scripts/health_dashboard.py --write

# Rebuild the weekly schema and lint failure history
python scripts/backfill_check_history.py
```

## Coverage

**What it measures.** The share of quoted Pali that some term record governs.

The corpus is built from two in-repository sources: backticked Pali spans in
`docs/translations/`, and the `example_phrases` the records themselves carry.
External source texts are not read — the repository stores metadata-only
manifests for those, so anything derived from them could not be verified by
CI.

A backticked span counts as Pali only when it contains at least one Pali
diacritic, after which every token inside it counts. That keeps
`pariyuṭṭhitena cetasā viharati` whole, including the undiacriticked
`viharati`, without letting a backticked English `heart` into the corpus. The
left side of a rendering declaration (`` `dukkha` is rendered `...` ``) is
Pali by construction, so it is collected too — but only when it carries no
diacritic, since a diacriticked headword is already a backticked span and
counting it twice inflated every occurrence figure.

Two percentages are reported because they answer different questions. Coverage
**by surface** asks how much of the vocabulary is governed. Coverage **by
occurrence** asks how much of the text a reader meets is governed, and is
always higher, because the ungoverned tail is mostly words used once.

**What it does not measure.** Whether the governing record is any good. A
one-line minor entry counts exactly as much as a mature major entry.

**How surfaces match.** Three routes, reported separately:

| Route | Meaning | Trust |
| --- | --- | --- |
| `exact` | The surface is a headword | High |
| `inflected` | It matched after a coarse case-ending fold | Good, not certain |
| `compound` | It is two governed headwords run together | Good, not certain |

The fold is a measurement device, not a morphological analyser. It removes one
whole listed ending — `-smiṃ`, `-ānaṃ`, `-assa` and the rest — then restores
the stem vowel, so `cittaṃ`, `cittassa`, `rūpasmiṃ`, and `dhamme` reach
`citta`, `rūpa`, and `dhamma`. A second round may take at most three more
characters, because past that a fold stops describing an inflection and starts
finding a different word: `veramaṇī` reaches `vera`, which governs enmity and
has nothing to do with abstaining, only by taking two bites. Wrong lemmas still
get through occasionally. Treat any single folded row as a lead to check, not a
fact.

**How to act on it.** The ranked ungoverned list is a candidate queue with
evidence attached. A surface near the top appearing across several documents
is a genuine governance gap. Feed it to `scripts/extract_candidate_terms.py`
and the normal candidate workflow — do not create a record straight from a
frequency count.

## Drift

**What it measures.** Renderings a translation document *declares* against the
record that governs the headword, in the three shapes
`repo_health.collect_governed_rendering_drift` already distinguishes:
`self_contradiction`, `discouraged`, and `unlisted`.

**What it does not measure, on purpose.** Translation prose is not scanned for
discouraged renderings. That was tried and abandoned — the reasoning is
recorded in full in `repo_health.collect_governed_rendering_drift`. The short
version: a phrase cannot be attributed to a headword without an alignment this
repository does not have, and the attempt produced 168 hits of which a sampled
majority were correct renderings of a *different* term. Do not re-attempt it
without Pali-to-English alignment.

This is why the drift number is small. It counts what can be checked, not
everything that could be wrong.

## Review queue

**What it measures.** Everything waiting on an editorial decision, in the
three shapes the repository stores review work:

- staged files under `candidates/`
- term records still marked `draft`
- translation surfaces in `reviews/newcomer-review-ledger.json` that have not
  reached `validated`, the terminal status in that ledger's vocabulary

**Where the dates come from.** There is no timestamp in the term schema, so
git is the clock: each item is dated from the commit that added it. Ledger
surfaces use their recorded source-fidelity date where they have one, since
the ledger does not record when a surface entered the queue.

This is why CI checks out full history. A shallow clone does not fail on
`git log` — it answers from its graft boundary, so anything added before that
boundary looks like it arrived on the day of the clone. The generator detects
the boundary and withholds exactly those dates, reporting `unknown` instead of
a wrong one; dates after the boundary are trustworthy and match what CI sees.

Two workflow notes follow from dating the queue out of git:

- **Commit before regenerating.** A candidate file added in the same change as
  the regenerated dashboard has no commit to date it yet, so it renders
  `unknown` locally and a real date in CI, and the freshness check calls the
  dashboard stale. Commit the queue change first, then regenerate.
- **Regenerate from a full clone.** From a shallow one, older items report
  `unknown` and the committed file will not match CI.

**Why the committed file shows dates, not day counts.** The generated Markdown
is compared byte for byte by `scripts/check_generated_docs.py`. A day count
would change every midnight and the file would be permanently stale. Run the
script directly for live ages; they are in the JSON output too.

## Schema and lint failures per week

**What it measures.** `validate_terms.py --strict` and `lint_terms.py
--strict` replayed against **every** commit in history, grouped by ISO week.

Counts are findings — individual rule violations — not failing runs. One
broken entry and forty broken entries are different weeks, and an exit code
cannot tell them apart.

A week reports its worst commit rather than the sum, so a failure that
survives several commits is counted once rather than once per commit. Weeks
with no commits are absent rather than zero-filled.

**Reading a flat zero.** At the time of writing every commit in the repository
passes both checks, so the series is all zeros. That is a real result, not a
broken measurement: the gates have never had to catch a regression on the
default branch. Until one does, treat this panel as a tripwire rather than a
trend.

**Why replay rather than CI logs.** Replay is deterministic and offline. A
run-history scrape cannot distinguish a real failure from a re-run, a
force-push, or an infrastructure error, and it cannot see the weeks before the
workflow existed.

## Maintenance

The Markdown is freshness-enforced like every other generated doc: it is
registered in `scripts/surface_registry.py`, and
`scripts/check_generated_docs.py` regenerates it and fails CI if the committed
copy differs. Regenerate with `--write` whenever terms, translations, or the
check history change.

The dashboard sits in `NON_CLUSTER_GENERATED_SURFACES` rather than
`CLUSTER_SURFACES`, because it reports on the repository instead of governing
a doctrinal family. That keeps `scripts/check_cluster_surfaces.py` from
demanding an authority document for it.

`reviews/check-history.jsonl` is rebuilt by
`scripts/backfill_check_history.py`, which rewrites the whole file each run
and is therefore idempotent. It is not run in CI: it needs full history and
takes a couple of minutes, so it is a periodic maintainer command.

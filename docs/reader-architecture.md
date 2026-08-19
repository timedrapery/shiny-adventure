# Reader Architecture

How the public reading edition is produced from the governed translation
corpus, and what to do when you want to change it.

The short version: **the reader is generated, not maintained.** The governed
translations in `docs/translations/` are authoritative. Reader pages are a
presentation layer over them, rebuilt by one script.

## What is authoritative and what is derived

| File | Status | Who owns it |
| --- | --- | --- |
| `docs/translations/*.md` | authoritative | editorial layer |
| `docs/translations/*-notes.md` | authoritative | editorial layer |
| `terms/**/*.json` | authoritative | editorial layer |
| `scripts/surface_registry.py` | authoritative | corpus + reader metadata |
| `includes/glossary.md` | authoritative | hand-written reader-voice glosses |
| `reader-src/about.md` | authoritative | hand-written reader prose |
| the `About this text` block in a sutta page | authoritative | hand-written reader prose |
| everything else under `reader-src/` | **generated** | `scripts/generate_reader.py` |
| the sutta block in `mkdocs.yml` nav | **generated** | `scripts/generate_reader.py` |
| `site/` | build output, gitignored | MkDocs |

A sutta reader page therefore contains exactly three kinds of content, and they
are kept visibly separate:

- **generated framing** — title, reference line, reading-path links, the
  per-page glossary
- **reader-authored prose** — the `About this text` block, preserved verbatim
  across every regeneration
- **canonical translation** — the body, copied from the governed surface with
  headings demoted one level, never edited in place

## The generator

```bash
python scripts/generate_reader.py --check
```

```bash
python scripts/generate_reader.py --write
```

`--check` runs inside `scripts/run_checks.py`, so a reader that has drifted
from the governed corpus fails the build. It is deterministic and idempotent:
running `--write` twice produces no second change.

It owns 45 files: the home page, Start Here, the All Suttas index, the
glossary page, 41 sutta pages, and the generated navigation block in
`mkdocs.yml`.

Everything it needs comes from two places — the governed surface named in the
registry, and the reader metadata in the registry itself.

## Reader metadata lives in the surface registry

There is one registry, not two. `scripts/surface_registry.py` holds
`TRANSLATION_SURFACES` (the corpus) and, beside it, `READER_METADATA` keyed by
the same surface key. Each entry carries:

- `pali_title` — the Pali name without the collection reference
- `reader_title` — a plain-English title, or `None` to fall back to the Pali
- `stage` and `order` — position in the newcomer reading path
- `path_note` — the one-line editorial note shown on Start Here

`STAGES` defines the five stages of the reading path and their descriptions.
`ESSENTIAL_FIVE` is the "if you only read five" set.

A test fails if any surface lacks reader metadata, if any metadata is orphaned,
or if two texts claim the same position in a stage.

## Adding a new translation surface

1. Write the translation and its notes in `docs/translations/`, to
   [PLAIN_ENGLISH_STANDARD.md](PLAIN_ENGLISH_STANDARD.md).
2. Register it in `TRANSLATION_SURFACES` in `scripts/surface_registry.py`.
3. Add a `READER_METADATA` entry for it in the same file. Give it a stage, a
   position, and a `path_note`. Leave `reader_title` as `None` unless you are
   also writing an introduction.
4. Regenerate:

```bash
python scripts/translation_surface_index.py --write-docs
```

```bash
python scripts/generate_reader.py --write
```

5. Run the suite. The new text now has a reader page, a place in the reading
   path, a row in the All Suttas index, and a navigation entry. No counts need
   updating anywhere: every public number is derived from the registry.

## Adding or improving a reader introduction

Edit the `About this text` block directly in
`reader-src/suttas/<surface>.md`. Then set `reader_title` for that surface in
`READER_METADATA`, and regenerate.

The generator reads the existing block back out of the page and writes it
straight through, so it survives regeneration. Texts without one get a short
restrained default rather than invented commentary.

Introductions should orient rather than interpret: plain contemporary English,
an intelligent general reader assumed, a reason the text matters where it sits
in the sequence, no academic throat-clearing, and no Buddhist jargon unless the
jargon is the subject. Do not adjust the translation to match an introduction.

## The glossary

`includes/glossary.md` is the hand-written source, in reader voice. It is
deliberately not the editorial `notes` field from the term records, which is
written for contributors.

Two things are generated from it:

- `reader-src/glossary.md`, the standalone glossary page, which joins each
  gloss to the governed Pali term where the rendering matches a record
- a per-page block appended to each sutta page containing **only** the terms
  that appear on that page

The per-page injection replaced a single glossary auto-appended to every page.
That older arrangement meant a term could carry only one note across the whole
site, even where the same English word does different work in different
suttas — the problem that forced `arrow` and `world` to be rewritten
generically when the prototype grew from one page to five. Definitions now
travel with the page, so a per-sutta override is a change to the generator's
lookup rather than an architectural problem.

## Testing locally

```bash
python scripts/run_checks.py
```

```bash
mkdocs build --strict
```

```bash
mkdocs serve
```

`run_checks.py` includes the reader-generation check and the Markdown
structure check. `mkdocs serve` gives a live preview on localhost.

## Deployment

`.github/workflows/deploy-reader.yml` deploys to GitHub Pages on every push to
`main` that touches the corpus, the reader, the terms, the scripts, or the
site configuration. It also accepts a manual dispatch.

The gate is the real one: the full verification suite, then an explicit
reader-freshness check, then a strict MkDocs build, all in the build job before
the deploy job runs. A drifted reader or a failing check cannot publish.

CI additionally builds the site with `--strict` on pull requests, so site
breakage is caught before it reaches `main`.

## Decisions deliberately not made here

- **Dependency and action upgrades.** Five dependabot pull requests are open
  against `actions/checkout`, `actions/setup-python`, `actions/upload-artifact`,
  `jsonschema`, and `pre-commit`. They were reviewed during this phase and left
  alone: they are unrelated to the reader, and the workflows they touch cannot
  be exercised locally, so merging them blind during a presentation-layer
  change would be the wrong risk to take. They should be handled as their own
  small task.
- **Translation wording.** Nothing in the corpus was retranslated for the sake
  of presentation. One reader-facing defect was corrected — the Start Here note
  for AN 11.9 described it as being about faith, when `Saddha` there is the
  name of the monk being addressed and the text is about how to meditate — and
  that correction is to reader metadata, not to the translation.

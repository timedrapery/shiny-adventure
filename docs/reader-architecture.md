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
| `includes/glossary.md` | authoritative | hand-written reader-facing glosses |
| `includes/newcomer-guides/*.json` | authoritative | structured First 12 orientation |
| `includes/reader-intros/*.md` | authoritative | hand-written orientation for newer non-First-12 surfaces |
| `reader-src/about.md` | authoritative | hand-written reader prose |
| `reader-src/stylesheets/` and `reader-src/javascripts/` | authoritative | progressive presentation and interaction |
| a legacy `About this text` / `Before you read` block outside the First 12 | authoritative | preserved reader prose |
| generated Markdown under `reader-src/` | **generated** | `scripts/generate_reader.py` |
| the sutta block in `mkdocs.yml` nav | **generated** | `scripts/generate_reader.py` |
| `site/` | build output, gitignored | MkDocs |

A sutta reader page therefore contains exactly three kinds of content, and they
are kept visibly separate:

- **generated framing** — plain-English title, reference, reading time, skip
  link, visible definitions, and semantic reading-order navigation
- **newcomer orientation** — an evidence-checked structured guide for the
  First 12, or a preserved legacy/default introduction for another text
- **canonical translation** — the body copied unchanged from the governed
  surface beneath a generated `Translation` heading, never edited in place

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

It owns one file per registered surface plus four collection pages and the
generated navigation block in `mkdocs.yml`: the home page, Start Here, the All
Suttas index, and the glossary page. The count follows the registry, so it is
not restated here.

Everything it needs comes from the governed surface named in the registry, the
reader metadata in the registry, the reader-facing glossary, and the structured
First 12 guides in `includes/newcomer-guides/`.

## Reader metadata lives in the surface registry

There is one registry, not two. `scripts/surface_registry.py` holds
`TRANSLATION_SURFACES` (the corpus) and, beside it, `READER_METADATA` keyed by
the same surface key. Each entry carries:

- `pali_title` — the Pali name without the collection reference
- `reader_title` — the required plain-English title
- `stage` and `order` — position in the newcomer reading path
- `path_note` — the one-line editorial note shown on Start Here

`STAGES` defines the five stages of the reading path and their descriptions.
`ESSENTIAL_FIVE` is the "if you only read five" set. `FIRST_TWELVE` is the
smaller newcomer collection shown before the complete five-stage order.
`QUICK_START` and `NEWCOMER_PATHWAYS` supply the homepage's low-commitment
starting text and three human-centered routes.

A test fails if any surface lacks reader metadata, if any metadata is orphaned,
or if two texts claim the same position in a stage.

## Adding a new translation surface

1. Write the translation and its notes in `docs/translations/`, to
   [PLAIN_ENGLISH_STANDARD.md](PLAIN_ENGLISH_STANDARD.md).
2. Register it in `TRANSLATION_SURFACES` in `scripts/surface_registry.py`.
3. Add a `READER_METADATA` entry for it in the same file. Give it a stage, a
   position, a `path_note`, and a nonempty plain-English `reader_title`.
4. Regenerate:

```bash
python scripts/translation_surface_index.py --write-docs
```

```bash
python scripts/generate_reader.py --write
```

5. Run the suite. The new text now has a reader page, a place in the reading
   path, an item in the All Suttas index, and a navigation entry. No counts need
   updating anywhere: every public number is derived from the registry.

## Adding or improving newcomer guidance

For a First 12 text, edit its authoritative JSON record in
`includes/newcomer-guides/`; never edit the guide inside the generated sutta
page. Each record supplies the scene, central question, main point, reading
cue, key terms, a guard against likely misreadings, and the governed section
headings that support the summary.

The generator validates that:

- all twelve guides exist and point to registered First 12 surfaces
- required prose fields and three to six key terms are present
- each key term exists in the reader glossary and occurs in the translation
- each evidence heading exactly matches a governed translation heading

For another text, prefer an authoritative
`includes/reader-intros/<surface-key>.md` file. Older pages with a legacy
introduction still preserve their `About this text` or `Before you read` block
across regeneration. A text without either gets a short restrained default
rather than invented commentary.

Guidance should orient rather than interpret: plain contemporary English, no
prior Buddhist knowledge assumed, no academic throat-clearing, and no Buddhist
jargon unless it is immediately explained. Do not adjust the translation to
match an introduction.

Every First 12 page also shows its position and previous/next step in that
compact route. The complete five-stage navigation remains available
independently.

## Progressive guidance for long texts

`reader-src/javascripts/reader-guidance.js` adds section progress cues to long
translations and optional collapse controls to selected repeated patterns. It
changes presentation only: the complete governed text is present and expanded
by default, remains readable without JavaScript, and is never rewritten by the
script. Add a section to its explicit allowlist only when the repetition is
structural and hiding it temporarily helps navigation without hiding what
changes from one cycle to the next.

## The glossary

`includes/glossary.md` is the hand-written reader-facing source. It is
deliberately not the editorial `notes` field from the term records, which is
written for contributors.

Two things are generated from it:

- `reader-src/glossary.md`, the standalone glossary page, which joins each
  gloss to the governed Pali term where the rendering matches a record
- a visible, keyboard-operable terms panel on each sutta page containing
  **only** terms that appear on that page
- exact-case inline abbreviation notes as a secondary convenience where a
  browser supports them; the visible panel never depends on hovering

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
structure check. It also runs `check_reader_accessibility.py`, which validates
heading hierarchy, reading metadata, skip links, visible definitions, named
navigation, guide coverage, flowing indexes, and the site accessibility asset.
`mkdocs serve` gives a live preview on localhost; `mkdocs build --strict` is the
rendered-site gate used in CI. The Playwright/axe suite discovers every built
directory under `site/suttas/`, so every registered sutta page receives a
rendered serious/critical accessibility scan rather than a sample-only check.

## The downloadable edition

`scripts/build_book.py` assembles the whole collection into a single EPUB,
published at `downloads/osf-pali-readings.epub` and linked from the home page.

It is built from `reader-src/`, not from `docs/translations/`, so it inherits
the reader titles, structured newcomer guidance, preserved legacy
introductions, reading times, and reading order. Website-only furniture is
dropped on the way in: the generated-by banner, skip link, previous/all/next
navigation, per-page visible terms panel, and inline abbreviation definitions.
The full glossary is included once as an appendix instead.

```bash
python scripts/build_book.py --check    # is pandoc available?
python scripts/build_book.py            # build into site/downloads/
```

Two things about how it is wired, both deliberate:

- **pandoc is not required for ordinary work.** The book is built only in the
  deploy workflow, after MkDocs has run. Editing a translation, running the
  checks, and building the site locally all work without it.
- **The home page links to the book with a raw `<a>` tag, not a Markdown
  link.** MkDocs validates Markdown links against its own source files, and the
  book is written straight into the built site, so a Markdown link would fail
  `mkdocs build --strict` for anyone without pandoc. Generated pages also use
  small, scoped HTML elements where native semantics matter: `details` for the
  terms disclosure, `nav` for reading order, and `dl` for definitions.

The consequence worth knowing: a locally built site has a download link that
404s unless `build_book.py` has been run into `site/` after `mkdocs build`.

## Deployment

`.github/workflows/deploy-reader.yml` deploys to GitHub Pages on every push to
`main` that touches the corpus, the reader, the terms, the scripts, or the
site configuration. It also accepts a manual dispatch.

The gate is the real one: the full verification suite, then an explicit
reader-freshness check, then a strict MkDocs build, all in the build job before
the deploy job runs. A drifted reader or a failing check cannot publish. The
downloadable edition is built after the site and before the artifact upload,
since MkDocs cleans `site/` on every build.

CI additionally builds the site with `--strict` on pull requests, so site
breakage is caught before it reaches `main`.

## Editorial boundaries

- Presentation changes do not authorize edits to the canonical translation
  body. Meaning, recurring vocabulary, and formula decisions remain governed
  by the translation and lexicon layers.
- Newcomer guidance may explain what happens, identify the central question,
  and warn against a likely misreading. It must remain traceable to governed
  section headings and must not silently settle an ambiguity.
- Passing the reader accessibility checker does not mark a translation
  `validated`. Human read-aloud usability and newcomer-comprehension reviews
  remain separate gates under `PLAIN_ENGLISH_STANDARD.md`.

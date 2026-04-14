# Style Guide

This document defines the repository's translation voice and default editorial
behavior. It is a house style guide for a structured Pāli translation lexicon,
not a general guide to Buddhist-English translation.

## Scope

The style guide exists to keep the lexicon:

- readable to contemporary English readers
- doctrinally precise
- internally consistent
- explicit about exceptions

Authority order is defined separately in
[docs/osf-editorial-authority.md](docs/osf-editorial-authority.md).

## Core Principles

### Use clear contemporary English

Prefer direct modern English over archaic, pseudo-sacral, or inflated phrasing.

Prefer:

- right view
- dissatisfaction
- remembering
- friendliness
- development

Avoid by default:

- ornamental spiritual diction
- pseudo-biblical phrasing
- unnecessary technical jargon when plain English will do

See [docs/MODERN_ENGLISH_POLICY.md](docs/MODERN_ENGLISH_POLICY.md) for the
repo's explicit anti-translationese register rules. See
[docs/VOICE_STANDARD.md](docs/VOICE_STANDARD.md) for the repository's default
sentence patterns for notes, context rules, examples, and contributor docs.

### Prefer modern common English over legacy prestige diction

Older Buddhist-English phrasing is not a virtue by itself.

Do not preserve wording just because it sounds familiar from old translations,
sermons, or academic Buddhist prose.

Prefer:

- direct verbs over abstract noun piles
- modern sentence flow over ceremonial cadence
- common English over bookish English when precision is unchanged

Review carefully before using:

- `thus`
- `one dwells ...`
- `one who ...`
- unexamined `cultivation`
- unexamined `abandonment`
- prestige terms such as `meritorious` when a better current-English option is
  already available in the family

If an older-looking term remains the best option in a narrow context, the entry
should say why.

### Preserve doctrinal precision

Do not flatten technical terms into vague spiritual language. When an
established English gloss obscures doctrinal function, prefer a more exact
rendering or leave the term in Pāli.

### Keep consistency as the default

Preferred translations are defaults, not casual suggestions. Contributors
should not rotate among near-synonyms unless the entry documents a real
contextual reason.

### Let context govern controlled exceptions

Context matters, but exceptions should be recorded. If a term changes
rendering across doctrinal, practical, or literary contexts, the entry should
encode that shift in `context_rules`.

### Document untranslated choices

Leaving a term in Pāli is acceptable when translation would distort the term,
collapse a doctrinal distinction, or prematurely narrow the practice frame.
When this happens, the reason should be explicit in the entry.

## Translation Priorities

When choosing a rendering, prioritize in this order:

1. fidelity to function in context
2. doctrinal precision
3. readability in contemporary English
4. consistency across related usage
5. literal transparency

## House Preferences

Current repository tendencies include:

- `dukkha` -> `dissatisfaction` by default, with approved alternates where documented
- `taṇhā` -> `ignorant wanting`
- `sati` -> `remembering`
- `samādhi` -> `mental composure`
- `sammā-sati` -> `right remembering`
- `sammā-samādhi` -> `right mental composure`
- `jhāna` -> `mental theme`
- `mettā` -> `friendliness`
- `bhāvanā` -> `development`
- `bodhi` -> `awakening`

Current repository tendencies also include:

- prefer `bhikkhu` or `bhikkhus` over `monk` or `monks` where the house style calls for the Pāli
- prefer `awakening` over `enlightenment`
- prefer governed doctrinal consistency over stylistic synonym variety

## Terms Commonly Left Untranslated

Some terms often remain in Pāli when English would mislead or over-narrow the
meaning. Common examples include:

- `ānāpānasati`
- `dhamma`
- `nibbāna`
- `bhikkhu`
- `kāyagatā sati`

This is not automatic. The entry should still state when the untranslated form
is preferred and when a gloss is acceptable.

## First Occurrence

For terms left untranslated, a first-occurrence gloss is often useful.

Example:

- `nibbāna (quenching)`

After that, the untranslated Pāli may stand on its own if the entry supports
that handling.

## Tone

English in this repository should be:

- calm
- exact
- readable
- contemporary
- restrained

It should not feel:

- grandiose
- mystical by default
- artificially academic
- inconsistent from one entry to the next

The repository's default note and example patterns are defined in
[docs/VOICE_STANDARD.md](docs/VOICE_STANDARD.md). Use that document when
editing `notes`, `context_rules`, `example_phrases`, or contributor guidance.

## Editorial Practice

When revising a core doctrinal term:

- review related compounds
- review recurring formulas
- review near-neighbor terms that could drift with it

When revising a minor term:

- keep the entry lean
- avoid inventing doctrinal nuance the corpus does not need
- align with the headword family where applicable

## Revision Rule

If house preferences change, update the relevant term records, examples, and
supporting documentation in the same pass so the repository remains internally
coherent.

That includes register changes. Do not modernize only `preferred_translation`
while leaving notes, examples, generated docs, or nearby compounds in older
translator diction.

## Markdown And Document Formatting

Apply consistent formatting across all Markdown files in this repository.

### Encoding

- All files use UTF-8 encoding.
- Preserve full Pāli diacritics in the `term` field, example phrases, and in
  running prose where the Pāli appears directly.
- Use ASCII-safe `normalized_term` values for filenames and JSON lookup keys.

### Heading Hierarchy

- Use a single `#` H1 per document.
- Use `##` for major sections and `###` for subsections.
- Do not skip heading levels.
- Headings should not be duplicated within a document.

### Lists

- Use `-` for unordered lists throughout.
- Use `1.` for numbered steps.
- Keep list items parallel in structure.

### Code Blocks

- Use fenced code blocks with an explicit language identifier where one applies:
  - `json` for term record examples
  - `bash` for shell commands
  - `text` for directory trees and plain text output
- Use inline code for field names, filenames, term values, and command names.

### Links

- Use relative links for all internal cross-references.
- Verify that links resolve before merging a change.
- Do not link to files that do not exist.

### Tables

- Use Markdown tables for structured comparisons where a list would be hard to
  scan.
- Keep tables narrow: prefer a few columns over a wide multi-column layout.

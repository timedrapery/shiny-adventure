# Shiny Adventure

A structured, modern approach to translating and understanding Pali terms.

Shiny Adventure is an early-stage lexicon project. It is designed to capture
translation decisions in a format that is useful for both human contributors
and future tools.

The repository currently includes:

- a JSON schema for term records
- a translation style guide
- editorial documentation for writing entries
- a starter set of structured term files in [`terms/`](terms)

The long-term goal is to support a future Pali lexicon, study tool, search
experience, or translation workflow built on clear and consistent data.

## Project Goals

- Create a standardized JSON format for Pali term records
- Develop a translation style guide that stays consistent across contributors
- Build a growing library of accurate, well-structured term entries
- Support future tooling such as search, cross-referencing, and glossary generation

## Repository Layout

- [`schema/PALI_TERM_SCHEMA.json`](schema/PALI_TERM_SCHEMA.json): canonical JSON schema
- [`terms/`](terms): structured Pali term entries
- [`docs/README.md`](docs/README.md): documentation map and reading order
- [`STYLE_GUIDE.md`](STYLE_GUIDE.md): house translation style
- [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md): field-by-field reference
- [`docs/TERM_ENTRY_STANDARD.md`](docs/TERM_ENTRY_STANDARD.md): guidance for creating entries
- [`docs/TAG_STATUS_VOCABULARY.md`](docs/TAG_STATUS_VOCABULARY.md): standard tags and status guidance
- [`CONTRIBUTING.md`](CONTRIBUTING.md): contributor workflow

## Example Term Entry

```json
{
  "term": "dukkha",
  "normalized_term": "dukkha",
  "entry_type": "major",
  "part_of_speech": "noun",
  "preferred_translation": "dissatisfaction",
  "alternative_translations": [
    "unease",
    "stress"
  ],
  "discouraged_translations": [
    "suffering"
  ],
  "untranslated_preferred": false,
  "definition": "The unsatisfactory and unstable character of conditioned experience.",
  "notes": "Project preference is dissatisfaction rather than suffering because it better reflects the broader sense of unsatisfactoriness present in experience.",
  "related_terms": [
    "anicca",
    "anatta",
    "tanha",
    "nirodha"
  ],
  "tags": [
    "three-marks",
    "core-doctrine"
  ],
  "status": "stable"
}
```

## How to Work in This Repo

If you are new to this project, start here:

1. Read [`STYLE_GUIDE.md`](STYLE_GUIDE.md) to understand the translation voice.
2. Use [`docs/README.md`](docs/README.md) for the recommended documentation path.
3. Read [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md) to learn each field.
4. Use [`docs/TERM_ENTRY_STANDARD.md`](docs/TERM_ENTRY_STANDARD.md) when adding or revising a term.
5. Check [`docs/TAG_STATUS_VOCABULARY.md`](docs/TAG_STATUS_VOCABULARY.md) before choosing tags or status values.
6. Validate term files before opening a pull request.

## Local Validation

To validate the dataset locally:

```bash
python -m pip install jsonschema
python scripts/validate_terms.py
```

This runs the same schema validation logic used by GitHub Actions.

## Contributing

Contributions are welcome, especially in these areas:

- adding new term entries
- improving existing entries
- tightening schema rules
- clarifying editorial guidance
- reviewing terminology choices for consistency

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the contribution workflow.

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE).

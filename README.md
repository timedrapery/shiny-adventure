# shiny-adventure

Structured Pali-to-English translation lexicon for Early Buddhist texts.

![Status](https://img.shields.io/badge/status-active%20development-blue)
![Language](https://img.shields.io/badge/source-Pali-orange)
![Target](https://img.shields.io/badge/output-contemporary%20English-green)
![Format](https://img.shields.io/badge/format-structured%20lexicon-lightgrey)

`shiny-adventure` is a translator's lexicon, house style guide, doctrinal terminology registry, and machine-readable translation rule system. It records how the repository expects important Pali terms to be rendered, when those defaults should shift by context, and where the Pali should remain untranslated.

This project is not a neutral dictionary. Major entries are rule-bearing editorial records intended to reduce translation drift across a corpus.

## Purpose

The repository exists to make translation decisions explicit, reviewable, and reusable.

It is designed to help contributors:

- preserve OSF house terminology in a structured form
- keep doctrinally sensitive terms stable across texts
- document context-specific exceptions rather than letting them accumulate silently
- support validation, linting, and future translation tooling

## Translation Philosophy

The project follows a practical but doctrinally precise translation philosophy:

- prefer clear contemporary English over archaic or artificially sacred diction
- preserve technical precision when a term plays a doctrinal role
- keep certain Pali terms untranslated when English would distort the function
- treat consistency as the default unless a documented context rule overrides it
- record rationale, examples, and related terms so decisions can be audited later

Authority is governed by [docs/OSF_EDITORIAL_AUTHORITY.md](docs/OSF_EDITORIAL_AUTHORITY.md). A concise statement of repository-wide terminology rules is in [TERMINOLOGY_PRINCIPLES.md](TERMINOLOGY_PRINCIPLES.md). Detailed house-style preferences are in [STYLE_GUIDE.md](STYLE_GUIDE.md).

## Rule-Bearing Entries

The repository has two entry classes:

- `major`: doctrinally important or context-sensitive records that carry translation policy
- `minor`: lighter reference records for terms with more stable treatment

For major entries, the important fields are not only definitional. They also encode default renderings, translation exceptions, doctrinal scope, and drift-prevention guidance.

Core rule-bearing fields include:

- `preferred_translation`
- `context_rules`
- `notes`
- `example_phrases`
- `authority_basis`
- `translation_policy`

Together, these fields function as the repository's consistency-enforcement layer.

## Repository Structure

```text
shiny-adventure/
|- README.md
|- CONTRIBUTING.md
|- STYLE_GUIDE.md
|- TERMINOLOGY_PRINCIPLES.md
|- schema/
|  `- PALI_TERM_SCHEMA.json
|- terms/
|  |- major/
|  `- minor/
|- docs/
|  |- DATA_DICTIONARY.md
|  |- TERM_ENTRY_STANDARD.md
|  |- HEADWORD_COMPOUND_FORMULA_POLICY.md
|  |- OSF_EDITORIAL_AUTHORITY.md
|  |- drift-risk-terms.md
|  `- ...
|- scripts/
|  |- validate_terms.py
|  |- check_translation_drift.py
|  |- lint_terms.py
|  `- ...
|- tests/
|  `- ...
`- .github/
   |- workflows/
   `- ISSUE_TEMPLATE/
```

## Schema

The live schema is defined in [schema/PALI_TERM_SCHEMA.json](schema/PALI_TERM_SCHEMA.json).

Required baseline fields are:

- `term`
- `normalized_term`
- `entry_type`
- `part_of_speech`
- `preferred_translation`
- `definition`
- `status`

Major entries must also include rule-bearing metadata such as notes, context rules, related terms, examples, alternates, discouraged translations, references, and tags.

The field-by-field reference is documented in [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md). Entry construction standards are in [docs/TERM_ENTRY_STANDARD.md](docs/TERM_ENTRY_STANDARD.md).

## Example Term Entries

Example major entry shape:

```json
{
  "term": "dukkha",
  "normalized_term": "dukkha",
  "entry_type": "major",
  "part_of_speech": "noun",
  "preferred_translation": "dissatisfaction",
  "alternative_translations": ["unsatisfactoriness", "stress"],
  "discouraged_translations": ["suffering"],
  "definition": "The unstable and unsatisfactory character of conditioned experience.",
  "notes": "Use the default rendering in core doctrinal exposition unless a narrower local context is explicit.",
  "context_rules": [
    {
      "context": "four noble truths exposition",
      "rendering": "dissatisfaction"
    }
  ],
  "example_phrases": [
    {
      "pali": "idaṃ dukkhaṃ ariyasaccaṃ",
      "translation": "this is the noble truth of dissatisfaction",
      "source": "SN 56.11"
    }
  ],
  "doctrinal_importance": "encoded through entry_type, tags, notes, and translation_policy",
  "status": "stable"
}
```

Example minor entry shape:

```json
{
  "term": "ajiva",
  "normalized_term": "ajiva",
  "entry_type": "minor",
  "part_of_speech": "noun",
  "preferred_translation": "livelihood",
  "definition": "A speech, path, or conduct term used in ethical and practical analysis.",
  "status": "reviewed"
}
```

## Contributing Terms

When contributing a term or revising an existing entry:

1. Read [CONTRIBUTING.md](CONTRIBUTING.md).
2. Confirm field usage in [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md).
3. Follow [docs/TERM_ENTRY_STANDARD.md](docs/TERM_ENTRY_STANDARD.md).
4. Check house-style expectations in [STYLE_GUIDE.md](STYLE_GUIDE.md).
5. Review authority order in [docs/OSF_EDITORIAL_AUTHORITY.md](docs/OSF_EDITORIAL_AUTHORITY.md).
6. Run validation before opening a pull request.

For doctrinal anchor terms, contributors should also review linked compounds and neighboring entries in the same family so the policy remains coherent.

## Validation and Drift Protection

Set up a local environment:

```bash
python -m venv .venv
python -m pip install -r requirements-dev.txt
```

Run the full repository checks:

```bash
python scripts/run_checks.py
```

Run targeted checks:

```bash
python -m unittest discover -s tests
python scripts/validate_terms.py
python scripts/lint_terms.py
python scripts/check_translation_drift.py
python scripts/repo_health.py
```

Translation-drift guidance for high-instability terms is tracked in [docs/drift-risk-terms.md](docs/drift-risk-terms.md).

## Candidate Workflow

The repository includes a review-first candidate intake path. Candidate extraction is for discovery and prioritization, not automatic glossary generation.

```bash
python scripts/extract_candidate_terms.py path/to/source.txt
python scripts/generate_candidate_report.py
python scripts/scaffold_candidate_terms.py --priority create_now
```

Candidate outputs remain under `candidates/` until an editor reviews them. See [docs/CANDIDATE_TERM_WORKFLOW.md](docs/CANDIDATE_TERM_WORKFLOW.md).

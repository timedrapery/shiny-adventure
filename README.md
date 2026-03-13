# 🌿 Shiny Adventure
A structured, modern approach to translating and understanding Pāli terms.

Shiny Adventure is an early-stage project focused on building a clean, consistent, and extensible system for working with Pāli vocabulary, including:

- Clear, human-readable English translations
- Multiple definition layers
- Structured metadata
- A JSON schema for standardized term records
- A translation style guide for consistency across contributors

This repository is the foundation for a future Pāli lexicon, study tool, or translation workflow, built with clarity and precision in mind.

## ✨ Project Goals

- Create a standardized JSON format for Pāli terms
- Develop a translation style guide that ensures consistency
- Build a growing library of accurate, well-sourced term entries
- Support future tooling (search, cross-referencing, visualization, etc.)

## 📁 Repository Structure

/  
├── schema/                 — JSON schema files  
│   └── pali_term.schema.json  
└── terms/                  — Individual Pāli term records  
│   └── bhavana.json  
│   └── dukkha.json  
│   └── jhana.json  
│   └── samadhi.json  
│   └── sati.json  
├── CONTRIBUTING.md         — Project overview  
├── LICENSE.md              — Project overview  
├── README.md               — Project overview  
├── STYLE_GUIDE.md          — Translation standards and conventions  

## 🧘 Example Term Entry

```json
{
  "term": "dukkha",
  "normalized_term": "dukkha",
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
    "anattā",
    "taṇhā",
    "nirodha"
  ],
  "tags": [
    "three-marks",
    "core-doctrine"
  ],
  "status": "stable"
}
```

## 🤝 How to Contribute

This project is in its early stages — contributions are welcome.

You can help by:

- Adding new Pāli term entries
- Improving the translation style guide
- Suggesting schema enhancements
- Opening issues for discussion
- Reviewing existing entries

If you're familiar with Pāli, linguistics, or structured data design, your input is especially valuable.

## 📜 License

This project is licensed under the MIT License.  

## Contributing

For more information on contributing to this project, please see the [CONTRIBUTING.md](CONTRIBUTING.md) file.  

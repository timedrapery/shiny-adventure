# STYLE GUIDE

## Purpose

This project is a living lexicon and translation dataset for rendering Pāli texts into contemporary English for a wide audience.

It serves three related purposes:

1. A translator's house style guide
2. A human-readable lexicon
3. A machine-readable dataset for translation tools

The aim is not merely literal equivalence, but consistent, intelligible, and context-sensitive English that preserves doctrinal precision while remaining readable.

---

## General Principles

### 1. Use clear contemporary English

Prefer plain modern English over archaic, overly academic, or artificially "sacred" diction.

Preferred:
- right view
- dissatisfaction
- remembering
- delight

Avoid when possible:
- suffering, if dissatisfaction is more precise
- mindfulness, when sati is better left untranslated or glossed differently
- absorption, if it distorts the sense of jhāna
- religious archaisms such as "thus have I heard" style wording unless deliberately chosen

---

### 2. Preserve doctrinal precision

Do not flatten technical terms into vague spiritual language.

When a common English rendering obscures the function of a term, prefer:
- a more precise English rendering
- or the untranslated Pāli term

---

### 3. Keep key Pāli terms untranslated when necessary

Some terms should remain in Pāli when translation would distort or prematurely narrow their meaning.

Examples may include:
- ānāpānasati
- sati
- bhikkhu / bhikkhus
- kāyagatā sati

These may be glossed on first occurrence, then left untranslated thereafter.

---

### 4. Prefer consistency across texts

A term should normally receive the same English rendering across texts unless context clearly requires otherwise.

The lexicon exists to support continuity across:
- suttas
- vinaya passages
- commentarial discussion
- contemporary paraphrases
- tool-generated glossaries
- app and API outputs

---

### 5. Context still governs meaning

Consistency does not mean rigidity.

A preferred rendering is the default, not an absolute law. If context demands a different rendering, that may be used, but the deviation should be noted where appropriate.

---

## Translation Priorities

When choosing a rendering, prioritize in this order:

1. Fidelity to function in context
2. Doctrinal precision
3. Readability in contemporary English
4. Cross-text consistency
5. Literal transparency

Literalness is valuable, but not if it obscures what the line is doing.

---

## Preferred Translation Tendencies

These reflect current house style and may evolve.

### Keep untranslated
- ānāpānasati
- sati
- bhikkhu / bhikkhus
- kāyagatā sati

### Preferred renderings
- dukkha -> dissatisfaction
- pīti -> delight
- samādhi -> composure
- sammā-samādhi -> right composure
- vitakka -> thinking
- vicāra -> pondering
- bhāvanā -> development
- kusala -> wholesome
- akusala -> unwholesome
- bodhi -> awakening
- sammā-diṭṭhi -> right view
- sammāsaṅkappa -> right attitude
- sammā-sati -> right sati
- nīvaraṇa -> distraction
- nirodha -> quenching
- khandha -> heap
- saṅkhārā -> choices (in paṭiccasamuppāda contexts, per project preference)
- saññā -> recognition
- asañña -> non-recognition
- āyatana -> cognitive realm, except where it clearly means one of the six sense fields
- salāyatana -> sense field

### Special project preferences
- Use "bhikkhus" rather than "monks"
- Use gender-neutral pronouns
- Use "awakening" rather than "enlightenment"
- Extend core term preferences into compounds when the doctrinal function stays the same
- Prefer "right sati" over "right mindfulness"
- Prefer "right composure" over "right concentration"
- Avoid using "the teaching says" in contemporary paraphrase
- Prefer "in this case" or "in this instance" over "in this teaching"

---

## Handling of First Occurrence

When a key Pāli term first appears in a text, the translator may:

1. leave it in Pāli
2. provide a short gloss
3. thereafter use the Pāli term without repeated glossing

Example:
- sati (remembering with presence of mind)

After that:
- sati

---

## Repeated Formula Passages

Repeated passages should normally be translated consistently unless:
- the context changes their force
- the repeated structure would sound unnatural in English
- variation is needed to preserve sense rather than surface form

Where repeated formulae are standardized, the project should aim to store a stable preferred rendering for reuse.

---

## Variants and Alternatives

The dataset may include:
- preferred translation
- acceptable alternatives
- discouraged renderings
- context-specific notes

This allows both human translators and software tools to distinguish:
- default rendering
- allowed variation
- translations to avoid

---

## Notes on Tone

The English should feel:
- direct
- calm
- precise
- readable
- contemporary

It should not feel:
- artificially mystical
- pseudo-biblical
- padded with jargon
- needlessly academic

---

## Punctuation and Formatting Preferences

- Minimize em dashes
- Use quotation marks only when present in the source, unless English style requires them for clarity outside translation
- Maintain simple formatting
- Prefer clean sectioning and structured entries

---

## Role of the Lexicon

The lexicon is not merely a glossary.

It is:
- a record of translation decisions
- a house style guide
- a rule base for apps and translation tools
- a continuity layer across projects

Every term entry should help answer:
- What does this term mean?
- How should it usually be rendered here?
- What should be avoided?
- When does context change the default?

---

## Revision Policy

This style guide is living and revisable.

Changes should aim toward:
- greater consistency
- greater clarity
- greater usefulness for both human translators and machine tools

When a translation preference changes, related term records should be updated so the dataset remains internally coherent.

# Support Text Standard

How to write the text a reader meets around a translation: reader
introductions, "Before you read" guides, glossary definitions, and newcomer
comprehension questions.

This standard draws on the principles of ASD-STE100 Simplified Technical
English: one meaning per word, short sentences, one idea per sentence, and
active voice. It is the project's own rule set, written for this material. It
does not copy the ASD-STE100 specification or its dictionary, and the project
does not claim ASD-STE100 compliance.

## Scope

Applies to:

- `includes/reader-intros/*.md`
- `includes/newcomer-guides/*.json`
- the definitions in `includes/glossary.md`
- newcomer comprehension questions

Does not apply to the translations themselves. In a sutta, repetition carries
meaning, verse and dialogue have their own shape, and the house terms are
fixed. Those follow [`PLAIN_ENGLISH_STANDARD.md`](PLAIN_ENGLISH_STANDARD.md).
Notes written for editors are also out of scope.

## Rules

**1. One idea per sentence.** If a sentence joins two ideas with "and",
"while", or a semicolon, consider making it two sentences.

**2. Short sentences.** At most 20 words when you ask the reader something or
tell them what to do (a question, a reading cue). At most 25 words when you
describe or explain. A quoted line from the translation does not count toward
the limit.

**3. Short paragraphs.** At most six sentences in a reader introduction
paragraph. At most three sentences in one field of a "Before you read" guide.

**4. Active voice.** Say who does what: "The Buddha teaches the monks", not
"The monks are taught". Use the passive only when the doer is unknown or does
not matter.

**5. One word, one meaning.** Use the house rendering of a term every time,
and use it only in that sense. Do not swap in a synonym for variety. The
governed lexicon is this project's list of technical names: `ignorant
wanting`, `quenching`, `heart`, and the rest are correct here even though they
are not everyday English.

**6. The plain thing first, then the house term.** Say what the reader needs
to understand in ordinary words, then name the house term. Model: the
glossary entry for `ignorant wanting` opens with "wanting something you can't
have right now".

**7. Verbs over nouns.** Prefer "when the reader sees" to "the reader's
seeing". Avoid stacked nouns such as "feedback evidence staging".

**8. No filler.** Leave out "it should be noted that", "in a sense", "quite",
"very", and similar words that add length but not meaning.

## Checking

`python scripts/support_text_audit.py` reports sentences over the limits,
likely passive voice, and long paragraphs in the in-scope files. It is
advisory: a finding is a prompt to look, not a verdict. `--strict` fails on
any finding.

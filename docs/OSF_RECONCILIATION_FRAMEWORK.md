# OSF Reconciliation Framework

This note governs how the repository reconciles its stabilized house style with
OSF-facing glossary, book, and Dhammarato/Buddhadasa materials.
It is not a general report. It exists to keep in-house materials usable
without letting rough glossary wording or living teaching rhetoric destabilize
the lexicon.

## Source Layers

This reconciliation layer uses the repository's existing authority order:

1. explicit repository house style already encoded in live term records
2. OSF house materials such as the OSF glossary and *What Is And Is Not The Path*
3. Dhammarato house-facing materials
4. Buddhadasa-line doctrinal and practical framing
5. first external practical checkpoint profiles such as Punnaji and the
   Hillside / Ñāṇamoli stream
6. other outside-source profiles when needed

The point is not to treat every OSF-facing phrase as a new default.
The point is to classify what each in-house source is actually doing.

## Reconciliation Outcomes

### ALIGN

Use `ALIGN` when OSF-facing usage strongly matches the repository's stabilized
default and can reinforce it directly.

Typical implementation:

- keep the current `preferred_translation`
- strengthen `notes`
- add or refine `authority_basis`
- add stronger anti-drift notes where the OSF material clarifies the intent

### TOLERATE ALTERNATE

Use `TOLERATE ALTERNATE` when OSF-facing wording is useful, intelligible, or
pedagogically valuable but should not replace the repository's default.

Typical implementation:

- keep the current `preferred_translation`
- encode the OSF-facing wording as a controlled alternate or explanatory note
- make the local scope explicit in `context_rules`
- stop that alternate from silently becoming the new default

### REFUSE DRIFT

Use `REFUSE DRIFT` when OSF-adjacent wording, rough glossary shorthand, or
motivational rhetoric would weaken doctrinal precision, flatten distinctions,
psychologize too loosely, or introduce mystification.

Typical implementation:

- add or strengthen `discouraged_translations`
- add explicit anti-drift language in `notes` or `translation_policy`
- distinguish pedagogical shorthand from translator-facing default policy

## Practice-Language Filter

The repository preserves a strict difference between:

- rule-bearing term policy
- explanatory teaching language
- motivational rhetoric
- rough glossary wording
- translator-facing prose

Useful OSF explanation may be preserved without becoming the lexicon default.
Useful practical external clarification may also be preserved the same way.

Examples:

- `sati` can tolerate awareness-language in rough OSF coaching prose only when
  the recollective function remains explicit.
- `animitta` can tolerate explanatory without-sign language or practical notes
  about not fastening on perceptual signs without losing `signless` as the default.
- `appaṇihita` can tolerate explanatory without-placing-desire language without
  drifting into apathy or no-goals rhetoric.
- `nibbāna` can preserve cooling or coolness as explanatory OSF/Buddhadasa
  language without losing the untranslated default.
- `nibbāna` can also tolerate narrower practical serenity-language in external
  pedagogical explanation without losing the untranslated default.
- `nirodha` can tolerate ending or cessation in named OSF explanatory frames
  without losing `quenching` as the house default.
- `vimutti` can tolerate liberation or emancipation in controlled explanatory
  frames without losing `release` as the default.
- practice notes about gladdening the mind may be preserved without collapsing
  doctrinal distinctions among `citta`, `mano`, `nīvaraṇa`, `āsava`, and other
  already-stabilized families.

## Translator Rule

When OSF-facing wording differs from the current default, ask in this order:

1. Does it strengthen the existing house rule?
2. Is it a useful explanatory alternate only?
3. Would using it as a default flatten an already-stabilized distinction?
4. Is it translator-usable policy or merely teaching rhetoric?

If the answer to 3 or 4 is unfavorable, encode the wording only as a
controlled alternate or refuse it as drift.

## Current Reconciliation Focus

The current reviewed OSF reconciliation surface covers:

- `suññatā`
- `animitta`
- `appaṇihita`
- `nibbāna`
- `nirodha`
- `sati`
- `vimutti`

with limited supporting review of nearby practice-facing and doctrinal terms
where needed for coherence.

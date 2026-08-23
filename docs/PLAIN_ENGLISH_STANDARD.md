# Plain English Standard

## Purpose

This document governs the **running English of translation surfaces**: the
text a reader actually reads in `docs/translations/` and `reader-src/`.

It is the third register document in the repository, and the three do not
overlap:

| Document | Governs |
| --- | --- |
| [MODERN_ENGLISH_POLICY.md](MODERN_ENGLISH_POLICY.md) | word choice inside term records |
| [VOICE_STANDARD.md](VOICE_STANDARD.md) | editorial prose: notes, context rules, contributor docs |
| **This document** | the translated sutta text itself |

Before this document existed, the first two were sometimes applied to
translation prose by analogy. That was a mistake in both directions. A term
record's `preferred_translation` is a lexical decision; a sentence in a sutta
is an act of English composition. They need different rules.

## The Standard

A person should be able to read or hear one of these translations and follow
what is happening without already knowing Buddhist vocabulary.

The English should sound like something a clear, intelligent person would
actually say out loud today.

That means:

- plain, direct, concrete, conversational
- ordinary vocabulary and ordinary sentence structure
- short where the Pāli is short
- easy to read aloud and easy to listen to
- faithful to what the Pāli is actually doing

It does **not** mean childish, dumbed down, cute, inspirational, poetic,
mystical, devotional, or self-help. The simplicity has to come from
understanding the text well enough to say it plainly. Simple is not vague.

## Governing Priorities

The target is neutral, contemporary English that a newcomer can follow without
knowing Buddhist terminology. No teacher, editor, transcript, or recording is a
voice model for the translation. Named sources may support lexical or doctrinal
decisions elsewhere in the repository, but sentence cadence and presentation
are governed here by reader comprehension and source fidelity.

Use these controls in order:

1. The Pali controls meaning, speakers, sequence, repetition, and ambiguity.
2. Governed term and phrase records control recurring vocabulary and formulas.
3. This standard controls sentence shape, dialogue, paragraphing, and running
   English.
4. Human usability and newcomer-comprehension review test whether the result is
   genuinely readable.

If clearer wording would change a governed rendering or resolve a real
ambiguity, stop the surface edit. Make the term- or phrase-family decision
openly and update every linked control together.

## The Read-Aloud Test

Every sentence has to pass one neutral usability question:

> Can a reader say this comfortably and understand it at ordinary reading
> speed?

Read awkward sentences aloud. If a sentence fails, make it natural without
losing meaning. If a real distinction prevents a smoother sentence, keep the
distinction and record why in the companion notes.

## Newcomer Readability Rules

- Begin with the concrete person, action, question, or problem already present
  in the source.
- Prefer one clear move at a time: question, answer, reason, example, contrast,
  consequence, or instruction.
- Use short clause-based sentences when a long sentence would hide the action.
- Make speakers and pronoun referents clear without adding information.
- Use neutral contractions where they improve flow; avoid slang and fashionable
  idiom.
- Make a contrast explicit when the source itself establishes one.
- Keep dialogue askable and answerable.
- Perfect a repeated unit before repeating it, and preserve intentional
  repetition.

These are composition rules, not permission to add teaching material. Do not
insert a modern analogy, explanatory aside, joke, emotional cue, or direct
address that the source does not provide. Added orientation belongs in the
reader introduction; interpretation belongs in the companion notes.

## Review States

Every registered translation carries a body hash and a neutral readability
review record.

- `provisional` means the current body received the documented readability pass
  and automated governance checks, but its human validation gates are not all
  complete.
- `validated` requires a recorded source-fidelity review, a human read-aloud
  usability review, and newcomer-comprehension testing in which at least four
  of five readers can state what happened and the practical point in their own
  words. The stored hash must still match the reviewed translation body.

Website-level accessibility—including semantic structure, keyboard use,
contrast, zoom and reflow, and screen-reader behavior—is tested at the reader
template level. A readable body does not by itself prove that the surrounding
website is accessible.

## Rules

### 1. Do not use `one` as a generic person

`one` as a stand-in person is the single most common source of translationese
in this corpus.

Prefer:

> When you feel something painful, you get upset about it.

or, when the text is describing a type of person rather than addressing the
listener:

> An untrained person feels something painful and gets upset about it.

Avoid:

> When one is touched by painful feeling, one sorrows and laments.

English has `you`, `they`, `a person`, `someone`, and the plural. Pāli has no
equivalent of the English generic `one`; it is an artifact of translation, not
a feature of the source.

Watch for `one's` in the same way: `beats one's chest` should be `beats their
chest` or `beats his chest` depending on who is being described.

### 2. Do not open clauses with `Having ...ed`

The Pāli absolutive is a normal, unremarkable connector. English `Having
recognized earth as earth, ...` is not normal English.

Prefer:

> He recognizes earth as earth. Then he takes himself to be earth.

or:

> Once he has recognized earth as earth, he takes himself to be earth.

Avoid:

> Having recognized earth as earth, one takes oneself to be earth.

### 3. Use `the Buddha`, not `the Blessed One`

`bhagavā` is governed by [`terms/major/bhagava.json`](../terms/major/bhagava.json).
The default rendering is `the Buddha`.

`the Blessed One` is the ceremonial register this standard exists to remove,
and it was also a live inconsistency: before this rule, sixteen surfaces used
`the Blessed One`, twenty-one used `the Buddha`, and DN 2 used both in the same
document.

Two contexts are recorded exceptions, and they are worth understanding because
they show how this standard is supposed to work. `Blessed One` is kept in
direct address, since English does not address anyone as `the Buddha` and the
repository already uses `Bhante` for `bhante`. It is also kept in the
`itipi so` recollection formula, where `bhagavā` heads a list that names
`buddha` separately, so `That Buddha is the arahant, the fully awakened Buddha`
would be redundant.

Neither exception is a loophole. Both are recorded as `context_rules` on the
term record, which is where a contextual rendering belongs. A blanket ban was
tried first and the corpus produced the counterexamples immediately.

`tathāgata` stays untranslated. It is a different word doing different work,
and collapsing it into `the Buddha` would lose a real distinction.

### 4. Keep repetition, but make it sound intentional

These are oral texts. Repetition is structural and usually load-bearing. Do
not delete it to make the page shorter.

But repetition should read like a person deliberately repeating themselves,
not like a template that failed to fill in. When a formula repeats across
twenty items, the sentence being repeated has to be a good English sentence
first, because the reader is going to hear it twenty times.

Test the repeated unit on its own before repeating it.

### 5. Dialogue should sound like dialogue

When people speak, make them sound like people speaking. Questions should
sound like questions someone would ask. Answers should sound like answers.
Commands should be direct.

Do not make ancient Indian characters sound like nineteenth-century English
gentlemen. Do not add modern slang or American idiom either. Aim for neutral,
contemporary conversational English.

### 6. Prefer verbs to abstract nouns

Prefer:

> when that stops, this stops

Avoid:

> with the cessation of that, there is the cessation of this

Nominalization is not banned. Some governed terms are nouns and must stay
nouns. But a chain of `-tion of -ment of -ness` is almost always a sentence
that has not been written yet.

### 7. Do not add doctrine

Do not improve the Buddha. Do not insert explanation into the translation. Do
not resolve an ambiguity just because a later tradition resolved it.

If something needs explaining, it goes in the companion `-notes.md` file. The
reader must always be able to tell what the text says apart from what we think
it means.

### 8. Pāli in the English

Untranslated Pāli is not automatically clearer. The primary reading has to
work for someone who does not know any Pāli.

Terms the repository deliberately keeps in Pāli (`bhikkhu`, `dhamma`,
`nibbāna`, `tathāgata`, and others recorded in
[../STYLE_GUIDE.md](../STYLE_GUIDE.md)) stay. Everything else should be in
English in the running text, with the Pāli available in the notes file, the
lexicon, and the reader edition's tooltips.

Do not drop a Pāli word into the English just because Buddhist readers would
recognize it.

## Words To Be Suspicious Of

These are not banned. The rule is never to use them *automatically* because
Buddhist translations normally do.

`thus`, `therein`, `thereof`, `whereby`, `herein`, `one who`, `that which`,
`abides`, `dwells`, `having gone`, `having seen`, `cognizes`, `perceives as`,
`formations`, `fabrications`, `phenomena`, `aggregates`, `sense bases`,
`clinging`, `craving`, `defilements`, `liberation`, `cessation`, `suchness`,
`conditioned phenomena`, `unconditioned`, `volitional formations`.

For each one, ask what the sentence is actually saying, to this listener, in
this place. Then say that.

Note that several of these are already governed away in the lexicon: the
repository renders `saṅkhāra` with putting-together language rather than
`formations`, `khandha` as `heap` rather than `aggregate`, and `vimutti` as
`release` rather than `liberation`. Where the lexicon has already decided,
follow the lexicon.

## Relationship To The Lexicon

This standard does not override governed renderings, and it is not a licence
to invent a fresh synonym every time a word appears.

Distinguish two things:

- **lexical meaning** — what a Pāli expression does consistently across the
  corpus, which the term record governs
- **English realization** — how that meaning is best said in this particular
  sentence

The schema already supports this. A term record carries
`preferred_translation`, `alternative_translations`,
`discouraged_translations`, `context_rules`, and `translation_policy`. A fixed
gloss that produces awkward running English is a signal that the record needs a
`context_rule`, not a signal to ignore the record.

If a governed rendering cannot be made to work in natural English anywhere,
that is an editorial finding about the record. Raise it and fix the record.
Do not quietly work around it in one surface.

## Checking

Run:

```bash
python scripts/plain_english_audit.py
```

The audit reports register signals in translation surfaces with guidance for
each. It is advisory by default and does not fail the build, because several
of its signals have legitimate exceptions and a crude gate would damage good
translations.

Use `--strict` to make it exit non-zero, and `--path` to scope it to one file
while revising.

A flagged line is a prompt to reread the sentence aloud. It is not proof that
the sentence must change.

## What This Standard Does Not Cover

- `-notes.md` files, generated docs, and contributor prose. Those follow
  [VOICE_STANDARD.md](VOICE_STANDARD.md).
- `preferred_translation` and other term-record fields. Those follow
  [MODERN_ENGLISH_POLICY.md](MODERN_ENGLISH_POLICY.md).
- Editorial Note blocks at the top of a translation surface. Those are
  apparatus, not translation.

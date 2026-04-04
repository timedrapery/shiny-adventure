# Modern English Policy

## Purpose

This repository prefers modern, common, precise English.

That preference is not cosmetic. It affects:

- `preferred_translation`
- `alternative_translations`
- `discouraged_translations`
- `context_rules`
- `notes`
- `example_phrases`
- translation surfaces
- generated translator-facing docs

The goal is maximum doctrinal precision with maximum present-day readability.

## Core Rule

Do not use elevated legacy Buddhist-English diction as a mark of seriousness.

Older phrasing should survive only when it is:

- technically necessary
- explicitly documented as a controlled alternate
- part of a narrow source-facing formula where a modern replacement would blur
  the governed meaning

## Preferred Style

Prefer:

- direct modern English
- common verbs over abstract noun piles
- ordinary sentence structure over ceremonial cadence
- language a careful present-day reader can understand on first contact

Examples of the direction the repo prefers:

- `development` over unexamined `cultivation`
- `giving up` or `putting away` over abstract `abandonment` when no
  distinction is lost
- `someone who ...` over `one who ...` when a clause is really needed
- direct sentence flow instead of filler `thus`
- `enters and remains in ...` over `dwells having entered ...`

## What To Avoid By Default

Avoid unmarked use of:

- archaic connective language
- pseudo-scriptural cadence
- inherited Buddhist translation prestige diction
- high-British literary phrasing that is not doing real technical work
- ceremonial noun-heavy explanation when a direct verb phrase would be clearer

Examples that should trigger review:

- `thus`
- `therein`
- `thereof`
- `whereby`
- `whilst`
- `amongst`
- `one dwells ...`
- `one who ...`
- `meritorious`
- `comprehends fully`
- unexamined `cultivation`
- unexamined `abandonment`

## Technical Exceptions

Some older-looking wording may still be correct in narrow contexts.

Keep it only when the entry or note explains why.

Examples of likely justified exceptions:

- `cessation` as a controlled alternate where the `nirodha` family explicitly
  records it
- `not-self` as the stable doctrinal label for `anattā`
- `thusness` only where the `tathatā` entry explicitly supports it

The test is not whether older translators used the wording.
The test is whether the current repository still needs it.

## Entry-Level Expectations

When editing a major or minor entry:

1. check whether the preferred translation is already modern
2. check whether notes and examples have fallen behind it
3. check whether alternates preserve legacy wording without explanation
4. check whether related compounds still carry older register

Do not modernize only the headline field while leaving old register in the
supporting prose.

## Contributor Checklist

Before merging wording changes, ask:

- Is this the most natural modern English that preserves the distinction?
- Am I keeping an older wording because it is precise, or only because it is
  familiar?
- Does the example phrase sound like live English or inherited translationese?
- If I kept an older alternate, did I explain when it is still valid?
- Did I check the related family for register mismatch?

## QA Guidance

Use the modern-English audit and any accompanying flagged-word tooling as a
review aid, not as a blind replacement engine.

Run `python scripts/modern_english_audit.py` after large term, note, or
translation-surface changes.

A flagged phrase is a prompt to review the wording.
It is not proof that the wording must always be changed.

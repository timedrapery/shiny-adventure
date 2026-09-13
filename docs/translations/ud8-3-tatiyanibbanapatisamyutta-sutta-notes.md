# Ud 8.3 Translation Notes

This document records the source and editorial decisions for [Ud 8.3:
Tatiyanibbānapaṭisaṁyutta Sutta](ud8-3-tatiyanibbanapatisamyutta-sutta.md).

## Source Base

- Primary source: SuttaCentral Bilara Mahāsaṅgīti root text, segment IDs
  `ud8.3:1.1`–`ud8.3:3.3`.
- Canonical reader source: <https://suttacentral.net/ud8.3/pli/ms>.
- Source boundary: the discourse ends at `ud8.3:3.3`. The segment after it,
  `3.4` (`Tatiyaṁ`), is collection apparatus marking the third discourse of
  the Pāṭaligāmiya vagga. The closing line `The third discourse is finished.`
  renders that marker only, as on every other surface in this repository.
- The discourse has 84 Pali words once the front matter is excluded, and uses
  no peyyāla. It is the shortest surface in the corpus.
- Control surfaces: Iti 44 for Khuddaka framing and for `asaṅkhata`, MN 43 for
  the conditional `paññāyati` shape, and AN 10.60 and MN 11 for the standard
  Sāvatthī opening.

## Udāna Framing

This is the repository's first Udāna surface, so the collection's framing is
settled here for the ones that follow. The Udāna's whole shape is a short
narrative occasion followed by the `udāna` it prompted, and the English has to
keep those two things distinguishable.

- `Evaṁ me sutaṁ—ekaṁ samayaṁ bhagavā sāvatthiyaṁ viharati jetavane
  anāthapiṇḍikassa ārāme.` — `So I heard. At one time the Buddha was staying
  near Sāvatthī, in Jeta's Grove, Anāthapiṇḍika's monastery.` Both halves
  match the wording already used across the corpus; `So I heard` is the
  majority form by twenty-six to eight.
- `Atha kho bhagavā etamatthaṁ viditvā tāyaṁ velāyaṁ imaṁ udānaṁ udānesi:` —
  `Then the Buddha, understanding what this meant, spoke this inspired saying
  at that moment:`. `udāna` is `inspired saying` rather than the cognate
  `uttered this utterance`, which is Pali sentence shape rather than English.
  `tāyaṁ velāyaṁ` is kept as `at that moment` because the collection's point
  is that the saying belongs to an occasion.
- `Tatiyaṁ.` — `The third discourse is finished.`, the closing line already
  used from SN 36.6 onward.
- The framing sits outside the headed section rather than getting a section of
  its own, as in Iti 44, so the reader meets the discourse the way the
  collection presents it.

## Governing Decisions

- **`ajāta abhūta akata asaṅkhata` is four parallel participles, and its
  positive counterpart is the same four words.** `unborn, unbecome, unmade,
  unconditioned` against `born, become, made, conditioned`. This is the whole
  discourse: it argues that the escape from the second series is discernible
  only because the first exists. Varying the wording between the two halves —
  or rendering one series as nouns and the other as adjectives — would break
  the argument in English. `asaṅkhata` and `saṅkhata` keep their governed
  `unconditioned` and `conditioned`.
- **`bhūta` takes `become` here, not its headword default `being`.** The
  headword covers the noun — a being, an existent thing — and this passage
  needs the participle in a series of four. `unbecome` is unusual English on
  its own; between `unborn` and `unmade` it is transparent, and the series is
  what carries it.
- **The four are rendered `what is unborn …`, not `an unborn …`.** The Pali is
  a bare neuter substantive. `An unborn, an unbecome, an unmade` is
  translationese, and it also reifies four separate items where the Pali has
  one thing under four descriptions. `What is …` keeps the neuter indefinite
  without supplying a noun the source does not have.
- **`nissaraṇaṁ paññāyetha` is `no escape would be discerned`.** `nissaraṇa`
  keeps its governed `escape` and `paññā` its governed `discernment`. MN 43
  already renders the identical conditional shape as `no emergence would be
  discerned`, so the two surfaces read alike.
- **`sandasseti samādapeti samuttejeti sampahaṁseti` is kept as four verbs**:
  `pointing out, urging on, rousing, and gladdening`. The pile-up is the
  source's own emphasis and is not compressed, as with the seven verbs of
  teaching in SN 12.20.
- **`aṭṭhiṁ katvā, manasi katvā, sabbaṁ cetaso samannāharitvā, ohitasotā` is
  `treating it as something that mattered, attending to it, bringing their
  whole heart to bear, listening closely`.** `ceto` keeps the governed
  `heart`. The absolutives are turned into participial modifiers rather than
  `Having made it their concern …` openers, which the plain-English standard
  rejects.
- **`nibbānapaṭisaṁyuttāya dhammiyā kathāya` is `a Dhamma talk about
  nibbāna`.** Both `dhamma` and `nibbāna` stay in Pali, as the reader glossary
  already supports on every other page that uses them.

## Practice Clarifications

- The discourse is an argument, not a description. It says nothing about what
  the unborn is like, and this edition adds nothing. What it claims is
  conditional: if there were no such thing, there would be no way out of what
  is born, become, made, and conditioned; because there is, there is.
- `Unconditioned` is a negative term in Pali and stays negative in English.
  The `asaṅkhata` record discourages `eternal`, `transcendent reality`, and
  `ultimate ground` for exactly this reason — the discourse says what the
  unborn is not, and turning that into a positive metaphysical object is an
  addition, not a translation.
- The framing is not decoration either. The bhikkhus are listening hard to a
  talk about nibbāna, and the saying is what that occasion drew out of the
  Buddha. The Udāna presents its sayings as prompted rather than freestanding.

## Readability Review

- Standard: `plain-english-v1`
- Status: `provisional`
- Source-fidelity review: complete against the cited segmented Pali.
- Automated governance review: complete; the full repository suite passed on
  2026-09-13.
- Human read-aloud usability review: pending.
- Newcomer comprehension review: pending.

This surface remains provisional until the human reviews are recorded.

## Wave 11 Role

Ud 8.3 is the second Wave 11 queue item, taken first because item 1 carries a
precondition — Dhp 21-32 would be the repository's first verse surface and its
packet has to settle verse handling before drafting.

It was ranked for one orphan signal, `asaṅkhata-dhātu`, and anchors it: the
record's quoted `ajātaṁ abhūtaṁ akataṁ asaṅkhataṁ` verified `exact` against
the root before drafting, which is not something every wave has been able to
say about its ranking. Corpus orphans go from 85 to 84.

Beyond the lexicon, this is the shortest surface in the corpus and one of the
few places where the canon argues for something rather than analysing it. It
belongs beside Iti 44, which handles the two nibbāna elements, and it gives
the reader path a page that can be read in a minute.

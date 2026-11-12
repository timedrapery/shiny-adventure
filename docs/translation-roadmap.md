# Translation Roadmap

This page says which suttas to translate next and how to choose them. It
replaces two older roadmaps. Their full audit history, wave by wave, is in
[the roadmap history](archive/translation-roadmap-history.md).

## Where we are

**Wave 13 is complete.** The next queue needs a fresh audit. Each wave since
Wave 9 has its own execution plan in [the archive](archive/), and the
[Wave 13 execution plan](archive/wave-13-execution-plan.md) is the latest.

## How we choose the next texts

We choose texts that do the most for the lexicon. A good next text:

- uses word families that the lexicon already governs
- tests distinctions between close terms that could still drift
- fixes the wording of formulas that repeat across texts
- shows the next useful headword, compound, or formula to refine

To find candidates, run:

```bash
python scripts/audit_surface_leverage.py
```

Then apply these lessons from earlier waves:

- **Count orphans, not citations.** An orphan is a governed term whose cited
  texts are all untranslated. A text cited by many records may only repeat
  words that other texts already show.
- **Skip bare lists.** A text of 80 Pali words or fewer is usually just a list.
  A cluster sheet shows a list better than a translation does.
- **Look for dark families.** A term is dark when no translation shows it in
  running text. A family can have few orphans and still be fully dark.
- **Fix missing citations first.** A record can look unshown only because it
  does not cite a text we already translated. A citation costs far less than a
  new translation.
- **Check the source before you queue a text.** In Wave 6, three of five picks
  did not contain the words they were chosen for.

## After each translation

1. Review the headwords, compounds, and formulas the text uses, together.
2. Write the translation and its notes file in one pass.
3. Add a phrase record only when a line repeats or could drift.
4. Update a headword's notes only when the text shows a boundary that applies
   to the whole family.
5. Refresh any map or generated sheet that the text now supports better.
6. Rebuild the indexes and run all the checks.

## Done so far (80 texts)

### Before the roadmap

- `MN 1` Mūlapariyāya Sutta
- `MN 10` Satipaṭṭhāna Sutta
- `MN 18` Madhupindika Sutta
- `MN 19` Dvedhāvitakka Sutta
- `MN 99` Subha Sutta
- `MN 117` Mahācattārīsaka Sutta
- `MN 118` Ānāpānasati Sutta
- `MN 137` Saḷāyatanavibhaṅga Sutta
- `MN 141` Saccavibhaṅga Sutta
- `MN 148` Chachakka Sutta
- `SN 22.59` Anattalakkhaṇa Sutta

### Wave 1: Dense existing support

- `SN 12.2` Paṭiccasamuppāda-vibhaṅga Sutta
- `SN 56.11` Dhammacakkappavattana Sutta
- `DN 2` Sāmaññaphala Sutta
- `MN 2` Sabbāsava Sutta
- `MN 9` Sammādiṭṭhi Sutta

### Wave 2: Distinction-forcing texts

- `MN 44` Cūḷavedalla Sutta
- `MN 64` Mahāmālukya Sutta
- `DN 15` Mahānidāna Sutta
- `SN 22.89` Khemaka Sutta
- `SN 22.48` Khandha Sutta

### Wave 3: Strategic expansion

- `MN 7` Vattha Sutta
- `SN 36.6` Salla Sutta
- `SN 46.51` Āhāra Sutta
- `MN 39` Mahā-Assapura Sutta
- `AN 10.60` Girimānanda Sutta

### Wave 4: Beyond the original roadmap

- `AN 4.113` Patodasutta
- `AN 11.9` Saddhāsutta
- `SN 12.23` Upanisā Sutta
- `SN 35.28` Āditta Sutta
- `MN 38` Mahātaṇhāsaṅkhaya Sutta
- `MN 26` Pāsarāsi Sutta

### Wave 5: Closing source gaps

- `MN 22` Alagaddūpama Sutta
- `SN 12.15` Kaccānagotta Sutta
- `AN 3.65` Kesamutta Sutta (Kālāma Sutta)
- `MN 63` Cūḷamālukya Sutta

### Wave 6: Ungoverned major families

- `SN 12.11` Āhāra Sutta (The Four Nutriments)
- `SN 55.5` Dutiyasāriputta Sutta (The Stream and the Stream-Enterer)
- `AN 6.63` Nibbedhika Sutta (The Penetrating Exposition)
- `SN 12.61` Assutavā Sutta (The Body and the Mind)
- `MN 11` Cūḷasīhanāda Sutta (The Shorter Lion's Roar)

### Wave 7: Dark clusters and orphan majors

- `MN 43` Mahāvedalla Sutta (The Longer Analysis)
- `SN 51.13` Chandasamādhi Sutta (The Four Bases of Power)
- `Iti 44` Nibbānadhātu Sutta (The Two Nibbāna Elements): the first
  Itivuttaka text

### Wave 8: Verified translation queue

- `SN 48.10` Dutiyavibhaṅga Sutta (The Five Faculties)

### Wave 9: Source-verified reader value

- `SN 45.8` Vibhaṅga Sutta (What the Eightfold Path Means): anchors `ariya`
- `SN 12.44` Loka Sutta (How the World Arises—and Ends): anchors `loka`
- `AN 3.88` Tatiyasikkhā Sutta (Three Trainings Cover Everything): anchors
  `adhicitta`
- `Iti 49` Diṭṭhigata Sutta (Taken Over by Views): anchors `pariyuṭṭhāna`

### Wave 10: Portable practice and verified orphans

- `AN 11.12` Dutiyamahānāma Sutta (Six Things to Remember Anywhere)
- `SN 12.20` Paccaya Sutta (Discovered, Not Invented)
- `AN 8.39` Abhisanda Sutta (Eight Streams of Benefit)
- `SN 46.1` Himavanta Sutta (Conduct Is Where Practice Grows)

### Wave 11: Verified anchors after a fresh audit

- `Ud 8.3` Tatiyanibbānapaṭisaṁyutta Sutta (Why There Is a Way Out): the first
  Udāna text; anchors `asaṅkhata-dhātu`
- `SN 22.22` Bhāra Sutta (Putting Down the Burden)
- `Dhp 21-32` Appamādavagga (Heedfulness Is the Path to the Deathless): the
  first Dhammapada and verse text
- `SN 22.26` Assāda Sutta (What the Heaps Offer, and the Way Out)
- `MN 122` Mahāsuññata Sutta (Dwelling in Emptiness)

### Wave 12

- `AN 3.136` Uppāda Sutta (True Whether or Not a Buddha Appears)
- `AN 5.14` Vitthata Sutta (The Five Strengths): anchors `bala`
- `Dhp 273-289` the Maggavagga (The Path)
- `AN 6.19` Maraṇassati Sutta (Recollecting Death, One Breath at a Time)
- `MN 121` Cūḷasuññata Sutta (Emptiness, Step by Step)

### Wave 13

- `Dhp 179-196` the Buddhavagga (The Teaching of the Buddhas)
- `Snp 1.8` Metta Sutta (May All Beings Be Happy): the first Sutta Nipāta text
- `AN 8.41` Saṅkhittūposatha Sutta (Living Like an Arahant for a Day)
- `AN 8.54` Dīghajāṇu Sutta (A Good Life Now and Later)
- `MN 113` Sappurisa Sutta (The Good Person and the Bad Person)

### Requested directly

- `SN 56.17` Avijjā Sutta (What Ignorance Means)
- `MN 61` Ambalaṭṭhikarāhulovāda Sutta (Advice to Rāhula on Lying)
- `MN 131` Bhaddekaratta Sutta (One Fine Night)
- `SN 22.86` Anurādha Sutta
- `SN 45.2` Upaḍḍha Sutta
- `AN 8.6` Dutiyalokadhamma Sutta
- `MN 119` Kāyagatāsati Sutta
- `AN 2.9` Cariya Sutta
- `AN 3.69` Akusalamūla Sutta
- `AN 4.5` Anusota Sutta
- `SN 1.1` Oghataraṇa Sutta
- `MN 36` Mahāsaccaka Sutta

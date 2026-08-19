# Lexicon Expansion Plan 500

## Purpose

This plan lays out the next controlled expansion stage for approximately 500
 additional term entries.

The goal is not dictionary completeness. The goal is better doctrinal coverage,
 better compound handling, and lower translation drift in the areas where the
 repository is most likely to be reused.

## Tier Status

Checked 2026-08-19 against the live 1145-term lexicon.

- Tier 1: complete. All 18 representative targets resolve to live entries.
- Tier 2: partial. The five `bala` compounds are live; `bojjhanga-samadhi`,
  `indriya-samatta`, `phassa-nirodha-samudaya`, `vedana-nirodha-samudaya`,
  `sekhabala`, `asekhabala`, `ariya-pariyesana`, and `anariya-pariyesana`
  are not.
- Tier 3: partial. Roughly half the representative targets resolve through
  nominal forms; `iti-vuccati`, `anupubbikatha`, `sappurisasevana`,
  `asappurisasevana`, `yoniso-upaparikkha`, and `dhammadesana` are not live.
- Tier 4: not started, and deliberately gated behind Tiers 1 to 3.

## How To Read The Representative Targets

The target names below are indicative, not filenames. Checking coverage by
literal name match understates it, because live records follow two conventions
this plan's original lists did not:

- compounds are normally written solid, so the live record for `saddha-bala`
  is `saddhabala.json`
- entries are normally nominal rather than verbal, so `ovadati` is live as
  `ovada` and `paccavekkhati` as `paccavekkhana`

Before treating a target as missing, check it hyphen-insensitively and check
the nominal form. Use the generated term indexes in `docs/generated/` rather
than guessing at a filename.

## Current Assessment

The repository already covers many core headwords well, especially:

- major doctrinal anchors such as `dukkha`, `sati`, `samadhi`, `nirodha`,
  `paticcasamuppada`, `vedana`, `vinnana`, and `upadana`
- many dependent-origination links
- much of the sense-field vocabulary
- many person terms and common doctrinal compounds

The next expansion should focus less on isolated single nouns and more on:

- doctrinal compounds that inherit or override headword policy
- framework labels that recur in formulas and lists
- person classifications that stabilize ethical and path language
- training and framing expressions that repeatedly appear in translation work

## Tier Structure

### Tier 1: 120 terms

Highest-priority rule-bearing additions. These matter because they are frequent,
 doctrinally important, and likely to drift if left implicit.

Families:

- root-analysis compounds and ethical classification terms: 20
- internal/external, noble/ordinary, and person-classification terms: 20
- path-factor and training-framework compounds: 25
- dependent-origination compounds and formula terms: 30
- aggregate and sense-process compounds with high drift risk: 25

Representative targets:

- `kusala-mula`
- `akusala-mula`
- `phassa-samudaya`
- `vinnana-tthiti`
- `anariya`
- `ariya-puggala`
- `sappurisa-dhamma`
- `indriya-bala`
- `bojjhanga-bhavana`
- `namarupa-samudaya`
- `vedana-samudaya`
- `tanha-samudaya`
- `upadana-samudaya`
- `bhava-samudaya`
- `jati-samudaya`
- `dukkha-samudaya`
- `ajjhatta`
- `bahiddha`

### Tier 2: 160 terms

Framework vocabulary that will strongly improve coverage of recurring sutta
 formulas and cluster consistency.

Families:

- awakening factors, faculties, strengths, and powers: 35
- dependent-origination side compounds and reciprocal formulas: 35
- aggregate, sense-base, and consciousness-family expansions: 30
- training language, restraint language, and meditative-development terms: 35
- liberation, path-attainment, and comparison terms: 25

Representative targets:

- `saddhabala` (live)
- `viriyabala` (live)
- `satibala` (live)
- `samadhibala` (live)
- `pannabala` (live)
- `dhammavicaya-bhavana` (family live via `dhammavicaya`; the `bhavana`
  compound is not)
- `bojjhanga-samadhi`
- `indriya-samatta`
- `phassa-nirodha-samudaya`
- `vedana-nirodha-samudaya`
- `ayoniso-patisankhana` (the positive `yoniso-patisankha` is live; the
  negative form is not)
- `ariya-pariyesana` and `anariya-pariyesana` (only the bare `pariyesana`
  headword is live, so the noble / ignoble search distinction that MN 26
  turns on is not yet governed as its own pair)
- `sekhabala` and `asekhabala` (the `sekha` and `asekha` headwords are live;
  the strength compounds are not)

### Tier 3: 140 terms

Narrative, dialog, and formula-support vocabulary that is not always doctrinally
 central by itself but appears often enough to improve translation consistency.

Families:

- repeated framing expressions and discourse-introduction terms: 35
- recurring ethical and evaluative compounds: 30
- common relational and pedagogical compounds: 30
- formula-support nouns and verbs: 25
- common person-role and conversational address terms not yet covered: 20

Representative targets:

- `yathabhuta` (live through `yathabhutam-pajanati` and
  `yathabhuta-nanadassana`)
- `ovada` (live; the plan originally listed the verb `ovadati`)
- `paccavekkhana` (live; the plan originally listed the verb `paccavekkhati`)
- `anusasana` (live; the plan originally listed `anusasani`)
- `anumodana` (live; the `katha` compound is not)
- `kalyanamitta-sevana` (family live via `kalyanamitta` and
  `kalyanamittata`; the `sevana` compound is not)
- `iti-vuccati`
- `anupubbikatha`
- `sappurisasevana`
- `asappurisasevana`
- `yoniso-upaparikkha`
- `dhammadesana`

### Tier 4: 80 terms

Lower-frequency but still useful support vocabulary. These should be added only
 after higher-risk doctrinal and formula clusters are in better shape.

Families:

- lower-frequency technical compounds that complete existing families: 30
- secondary cosmology and world-language compounds: 20
- lower-frequency person and role classifications: 15
- supporting abstract nouns and evaluative adjectives: 15

Representative targets:

- additional loka and yoni compounds
- lesser-used bhavana derivatives
- paired moral or social contrast terms
- cluster-completion compounds around existing major anchors

## Roadmap Summary

- Tier 1: 120
- Tier 2: 160
- Tier 3: 140
- Tier 4: 80

Total planned next-stage additions: 500

## What Not to Mass-Generate

Do not mass-generate:

- low-frequency particles and grammatical fragments
- proper names simply for dictionary completeness
- doctrinal compounds whose house rendering is still unclear
- late or commentarial terminology unless the repository explicitly wants it
- near-duplicate spelling variants without first deciding normalization policy

## Batch Policy

Expansion should proceed in batches of roughly 20 to 40 terms.

Each batch should be coherent by family, for example:

- wholesome/unwholesome root compounds
- internal/external contemplative vocabulary
- person-classification compounds
- dependent-origination formula compounds
- faculties/strengths/awakening-factor framework terms

That keeps review manageable and reduces doctrinal drift.

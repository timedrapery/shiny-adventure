# Translation Drift Audit

Generated: 2026-04-20

## Audit Scope And Method

This audit scans live term entries, docs, generated docs, translations/notes, scripts, tests, schema, candidates, and top-level policy files. The only repository write is this generated report.

- Term entries scanned: 1117 (236 major, 881 minor)
- Repository text files scanned: 1398
- Documentation Markdown files scanned: 156
- Generated Markdown files scanned: 60
- Translation Markdown files scanned: 29
- Baseline checks run before this report: `validate_terms.py --json` clean, `check_translation_drift.py --json` clean, `check_generated_docs.py` passed, `check_translation_formula_consistency.py --format json` returned zero findings.
- Audit posture: prefer false positives over missed inconsistencies; guardrail statements are listed separately from assertive usage.

## 1. Inconsistent Term Usage

### Generated/Docs Table Default Mismatches

- None found. Markdown `Default`/`Preferred` table rows match term-entry preferred translations where a term column could be resolved.

### Explicit Non-Preferred Rendering Statements

#### `animitta` (`animitta`)
- Preferred translation: `signless` at `terms/major/animitta.json`
- Variants found:
  - `formless`
    - unregistered; guardrail at `docs/emptiness-signless-wishless-interface-map.md:50`: - Do not translate `animitta` as `formless`, `blank`, or `imageless` by default.

#### `appaṇihita` (`appanihita`)
- Preferred translation: `wishless` at `terms/major/appanihita.json`
- Variants found:
  - `passive`
    - unregistered; guardrail at `docs/emptiness-signless-wishless-interface-map.md:51`: - Do not translate `appaṇihita` as `passive`, `apathetic`, `aimless`, or `no goals`.

#### `chanda` (`chanda`)
- Preferred translation: `desire` at `terms/major/chanda.json`
- Variants found:
  - `craving`
    - unregistered; guardrail at `docs/craving-appropriation-affective-attachment-map.md:29`: - Do not translate `chanda` as `craving` by default.

#### `ekaggatā` (`ekaggata`)
- Preferred translation: `directness` at `terms/major/ekaggata.json`
- Variants found:
  - `one-pointedness`
    - unregistered; guardrail at `docs/jhana-cluster-map.md:53`: - Do not rewrite `ekaggatā` as `one-pointedness` when `directness` is the live

#### `jhāna` (`jhana`)
- Preferred translation: `mental theme` at `terms/major/jhana.json`
- Variants found:
  - `absorption`
    - unregistered; guardrail at `docs/jhana-cluster-map.md:51`: - Do not translate `jhāna` as `absorption`, `trance`, or `ecstasy` by default.

#### `nirodha` (`nirodha`)
- Preferred translation: `quenching` at `terms/major/nirodha.json`
- Variants found:
  - `cessation`
    - registered; assertive; registered sources: alternative_translations[1], context_rules[4].rendering at `docs/dhammarato-quotes-profile.md:57`: - `nirodha` as `cessation`

#### `pabbajita` (`pabbajita`)
- Preferred translation: `renunciant` at `terms/minor/pabbajita.json`
- Variants found:
  - `renunciate`
    - unregistered; assertive at `docs/translations/mn99-subha-sutta-notes.md:23`: - `gahaṭṭha` remains `householder` and `pabbajita` remains `renunciate`.
    - unregistered; assertive at `docs/translations/mn99-subha-sutta.md:12`: `householder`; `pabbajita` is rendered `renunciate`; `nīvaraṇa` is rendered

#### `pāṭimokkha` (`patimokkha`)
- Preferred translation: `pāṭimokkha` at `terms/major/patimokkha.json`
- Variants found:
  - `pātimokkha`
    - unregistered; assertive at `docs/translations/dn2-samannaphala-sutta.md:12`: `pātimokkha` remains `pātimokkha`; `indriyasaṃvara` is rendered `guarding

#### `sammāsaṅkappa` (`samma-sankappa`)
- Preferred translation: `right attitude` at `terms/major/samma-sankappa.json`
- Variants found:
  - `attitude`
    - unregistered; assertive at `docs/what-is-and-is-not-the-path-profile.md:52`: - `samma-sankappa` as `attitude`

#### `saṅkhārā` (`sankhara`)
- Preferred translation: `putting things together` at `terms/major/sankhara.json`
- Variants found:
  - `putting-together activities`
    - registered; assertive; registered sources: alternative_translations[4], context_rules[3].rendering at `docs/translations/sn22-59-anattalakkhana-sutta-notes.md:30`: - `saṅkhārā` remains `putting-together activities` in the heap-family context.
    - registered; guardrail; registered sources: alternative_translations[4], context_rules[3].rendering at `docs/generated/heaps-vs-clung-to-heaps-brief.md:13`: - In heap context, keep `saṅkhārā` as `putting-together activities` rather than importing the dependent-arising link or `volitional formations` by habit.
    - registered; guardrail; registered sources: alternative_translations[4], context_rules[3].rendering at `scripts/five_heaps_cluster_report.py:231`: "- In heap context, keep `saṅkhārā` as `putting-together activities` rather than importing the dependent-arising link or `volitional formations` by habit.",

#### `suññatā` (`sunnata`)
- Preferred translation: `emptiness` at `terms/major/sunnata.json`
- Variants found:
  - `nothingness`
    - unregistered; guardrail at `docs/emptiness-signless-wishless-interface-map.md:48`: - Do not translate `suññatā` as `nothingness`.

#### `taṇhā` (`tanha`)
- Preferred translation: `ignorant wanting` at `terms/major/tanha.json`
- Variants found:
  - `desire`
    - unregistered; guardrail at `docs/craving-appropriation-affective-attachment-map.md:30`: - Do not translate `taṇhā` as `desire` by default.

#### `upādāna` (`upadana`)
- Preferred translation: `taking personally` at `terms/major/upadana.json`
- Variants found:
  - `attachment`
    - unregistered; guardrail at `docs/craving-appropriation-affective-attachment-map.md:31`: - Do not translate `upādāna` as `attachment` by default.

#### `upekkhācetovimutti` (`upekkha-cetovimutti`)
- Preferred translation: `liberation of mind through dynamic balance` at `terms/minor/upekkha-cetovimutti.json`
- Variants found:
  - `liberation of mind through ...`
    - unregistered; assertive at `docs/translations/mn99-subha-sutta-notes.md:34`: `upekkhā cetovimutti` are rendered as `liberation of mind through ...`

#### `vicāra` (`vicara`)
- Preferred translation: `pondering` at `terms/major/vicara.json`
- Variants found:
  - `sustaining`
    - unregistered; assertive at `docs/dhammarato-quotes-profile.md:60`: - `vicara` as `sustaining`
  - `thinking and pondering`
    - unregistered; assertive at `docs/first-jhana-entry-sheet.md:26`: - Keep `vitakka` and `vicāra` as `thinking and pondering`.

#### `vitakka` (`vitakka`)
- Preferred translation: `thinking` at `terms/major/vitakka.json`
- Variants found:
  - `applying`
    - unregistered; assertive at `docs/dhammarato-quotes-profile.md:59`: - `vitakka` as `applying`

## 2. Conflicting Rule Definitions

These are cross-entry rendering collisions: one entry allows or prefers a rendering that another entry discourages. Many are intentional doctrinal contrasts; they still need explicit family guardrails.

Total cross-entry collisions found: 69

### 1. `desire`
- Term / rule conflict: `desire` is allowed by 3 entry field(s) and discouraged by 7 entry field(s).
- Allowed/preferred side: `chanda` preferred_translation (`terms/major/chanda.json`); `chanda` context_rules[0].rendering (`terms/major/chanda.json`); `chanda` context_rules[3].rendering (`terms/major/chanda.json`)
- Discouraged side: `cetana` discouraged_translations[1] (`terms/major/cetana.json`); `kama` discouraged_translations[0] (`terms/major/kama.json`); `kamacchanda` discouraged_translations[0] (`terms/major/kamacchanda.json`); `lobha` discouraged_translations[0] (`terms/major/lobha.json`); `raga` discouraged_translations[1] (`terms/major/raga.json`); `tanha` discouraged_translations[0] (`terms/major/tanha.json`); `upadana` discouraged_translations[1] (`terms/major/upadana.json`)

### 2. `release`
- Term / rule conflict: `release` is allowed by 6 entry field(s) and discouraged by 3 entry field(s).
- Allowed/preferred side: `mutti` alternative_translations[0] (`terms/major/mutti.json`); `mutti` context_rules[1].rendering (`terms/major/mutti.json`); `vimutti` preferred_translation (`terms/major/vimutti.json`); `vimutti` context_rules[0].rendering (`terms/major/vimutti.json`); `vimutti` context_rules[3].rendering (`terms/major/vimutti.json`); `vimutti` context_rules[4].rendering (`terms/major/vimutti.json`)
- Discouraged side: `khaya` discouraged_translations[2] (`terms/major/khaya.json`); `nissarana` discouraged_translations[2] (`terms/major/nissarana.json`); `pahana` discouraged_translations[2] (`terms/major/pahana.json`)

### 3. `nibbāna`
- Term / rule conflict: `nibbāna` is allowed by 3 entry field(s) and discouraged by 5 entry field(s).
- Allowed/preferred side: `nibbana` preferred_translation (`terms/major/nibbana.json`); `nibbana` context_rules[0].rendering (`terms/major/nibbana.json`); `nibbana` context_rules[6].rendering (`terms/major/nibbana.json`)
- Discouraged side: `amata` discouraged_translations[3] (`terms/major/amata.json`); `asankhata` discouraged_translations[3] (`terms/major/asankhata.json`); `nibbuta` discouraged_translations[2] (`terms/major/nibbuta.json`); `santi` discouraged_translations[3] (`terms/major/santi.json`); `upasama` discouraged_translations[2] (`terms/minor/upasama.json`)

### 4. `fetter`
- Term / rule conflict: `fetter` is allowed by 3 entry field(s) and discouraged by 3 entry field(s).
- Allowed/preferred side: `samyojana` preferred_translation (`terms/major/samyojana.json`); `samyojana` context_rules[0].rendering (`terms/major/samyojana.json`); `samyojana` context_rules[3].rendering (`terms/major/samyojana.json`)
- Discouraged side: `gantha` discouraged_translations[2] (`terms/major/gantha.json`); `kilesa` discouraged_translations[2] (`terms/major/kilesa.json`); `yoga` discouraged_translations[2] (`terms/major/yoga.json`)

### 5. `peace`
- Term / rule conflict: `peace` is allowed by 6 entry field(s) and discouraged by 3 entry field(s).
- Allowed/preferred side: `santi` preferred_translation (`terms/major/santi.json`); `santi` context_rules[0].rendering (`terms/major/santi.json`); `santi` context_rules[2].rendering (`terms/major/santi.json`); `santi` context_rules[3].rendering (`terms/major/santi.json`); `upasama` alternative_translations[1] (`terms/minor/upasama.json`); `upasama` context_rules[2].rendering (`terms/minor/upasama.json`)
- Discouraged side: `mutti` discouraged_translations[3] (`terms/major/mutti.json`); `nibbana` discouraged_translations[1] (`terms/major/nibbana.json`); `yogakkhema` discouraged_translations[0] (`terms/minor/yogakkhema.json`)

### 6. `cause`
- Term / rule conflict: `cause` is allowed by 4 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `hetu` preferred_translation (`terms/major/hetu.json`); `hetu` context_rules[0].rendering (`terms/major/hetu.json`); `hetu` context_rules[2].rendering (`terms/major/hetu.json`); `nidana` alternative_translations[1] (`terms/major/nidana.json`)
- Discouraged side: `paccaya` discouraged_translations[0] (`terms/major/paccaya.json`)

### 7. `escape`
- Term / rule conflict: `escape` is allowed by 3 entry field(s) and discouraged by 2 entry field(s).
- Allowed/preferred side: `nissarana` preferred_translation (`terms/major/nissarana.json`); `nissarana` context_rules[0].rendering (`terms/major/nissarana.json`); `nissarana` context_rules[2].rendering (`terms/major/nissarana.json`)
- Discouraged side: `mutti` discouraged_translations[1] (`terms/major/mutti.json`); `vimutti` discouraged_translations[1] (`terms/major/vimutti.json`)

### 8. `freedom`
- Term / rule conflict: `freedom` is allowed by 3 entry field(s) and discouraged by 3 entry field(s).
- Allowed/preferred side: `mutti` preferred_translation (`terms/major/mutti.json`); `mutti` context_rules[0].rendering (`terms/major/mutti.json`); `mutti` context_rules[2].rendering (`terms/major/mutti.json`)
- Discouraged side: `nissarana` discouraged_translations[1] (`terms/major/nissarana.json`); `vimutti` discouraged_translations[2] (`terms/major/vimutti.json`); `yogakkhema` discouraged_translations[2] (`terms/minor/yogakkhema.json`)

### 9. `self`
- Term / rule conflict: `self` is allowed by 2 entry field(s) and discouraged by 3 entry field(s).
- Allowed/preferred side: `atta` preferred_translation (`terms/major/atta.json`); `atta` context_rules[0].rendering (`terms/major/atta.json`)
- Discouraged side: `sakkaya` discouraged_translations[0] (`terms/major/sakkaya.json`); `upadhi` discouraged_translations[0] (`terms/major/upadhi.json`); `vinnana` discouraged_translations[2] (`terms/major/vinnana.json`)

### 10. `condition`
- Term / rule conflict: `condition` is allowed by 3 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `paccaya` preferred_translation (`terms/major/paccaya.json`); `paccaya` context_rules[0].rendering (`terms/major/paccaya.json`); `paccaya` context_rules[1].rendering (`terms/major/paccaya.json`)
- Discouraged side: `hetu` discouraged_translations[0] (`terms/major/hetu.json`)

### 11. `defilement`
- Term / rule conflict: `defilement` is allowed by 2 entry field(s) and discouraged by 2 entry field(s).
- Allowed/preferred side: `kilesa` preferred_translation (`terms/major/kilesa.json`); `kilesa` context_rules[0].rendering (`terms/major/kilesa.json`)
- Discouraged side: `asava` discouraged_translations[0] (`terms/major/asava.json`); `ogha` discouraged_translations[2] (`terms/major/ogha.json`)

### 12. `discerns`
- Term / rule conflict: `discerns` is allowed by 2 entry field(s) and discouraged by 2 entry field(s).
- Allowed/preferred side: `pajanati` preferred_translation (`terms/major/pajanati.json`); `pajanati` context_rules[0].rendering (`terms/major/pajanati.json`)
- Discouraged side: `abhijanati` discouraged_translations[1] (`terms/major/abhijanati.json`); `janati` discouraged_translations[1] (`terms/major/janati.json`)

### 13. `identity`
- Term / rule conflict: `identity` is allowed by 3 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `sakkaya` preferred_translation (`terms/major/sakkaya.json`); `sakkaya` context_rules[0].rendering (`terms/major/sakkaya.json`); `sakkaya` context_rules[1].rendering (`terms/major/sakkaya.json`)
- Discouraged side: `asmimana` discouraged_translations[2] (`terms/major/asmimana.json`)

### 14. `insight`
- Term / rule conflict: `insight` is allowed by 1 entry field(s) and discouraged by 4 entry field(s).
- Allowed/preferred side: `vipassana` preferred_translation (`terms/minor/vipassana.json`)
- Discouraged side: `abhinna` discouraged_translations[2] (`terms/major/abhinna.json`); `dassana` discouraged_translations[0] (`terms/major/dassana.json`); `nana` discouraged_translations[0] (`terms/major/nana.json`); `panna` discouraged_translations[0] (`terms/major/panna.json`)

### 15. `wearing away`
- Term / rule conflict: `wearing away` is allowed by 3 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `khaya` preferred_translation (`terms/major/khaya.json`); `khaya` context_rules[0].rendering (`terms/major/khaya.json`); `khaya` context_rules[3].rendering (`terms/major/khaya.json`)
- Discouraged side: `nirodha` discouraged_translations[1] (`terms/major/nirodha.json`)

### 16. `body`
- Term / rule conflict: `body` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `kaya` preferred_translation (`terms/major/kaya.json`); `kaya` context_rules[0].rendering (`terms/major/kaya.json`)
- Discouraged side: `rupa` discouraged_translations[0] (`terms/major/rupa.json`)

### 17. `heart`
- Term / rule conflict: `heart` is allowed by 3 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `citta` alternative_translations[2] (`terms/major/citta.json`); `citta` context_rules[2].rendering (`terms/major/citta.json`); `hadaya` preferred_translation (`terms/minor/hadaya.json`)
- Discouraged side: `mano` discouraged_translations[1] (`terms/major/mano.json`)

### 18. `ignorance`
- Term / rule conflict: `ignorance` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `avijja` preferred_translation (`terms/major/avijja.json`); `avijja` context_rules[0].rendering (`terms/major/avijja.json`)
- Discouraged side: `moha` discouraged_translations[0] (`terms/major/moha.json`)

### 19. `knows`
- Term / rule conflict: `knows` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `janati` preferred_translation (`terms/major/janati.json`); `janati` context_rules[0].rendering (`terms/major/janati.json`)
- Discouraged side: `sanjanati` discouraged_translations[0] (`terms/major/sanjanati.json`)

### 20. `recognizes`
- Term / rule conflict: `recognizes` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `sanjanati` preferred_translation (`terms/major/sanjanati.json`); `sanjanati` context_rules[0].rendering (`terms/major/sanjanati.json`)
- Discouraged side: `abhijanati` discouraged_translations[0] (`terms/major/abhijanati.json`)

### 21. `reflection`
- Term / rule conflict: `reflection` is allowed by 3 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `vicara` alternative_translations[0] (`terms/major/vicara.json`); `vicara` context_rules[1].rendering (`terms/major/vicara.json`); `paccavekkhana` preferred_translation (`terms/minor/paccavekkhana.json`)
- Discouraged side: `yoniso-manasikara` discouraged_translations[0] (`terms/major/yoniso-manasikara.json`)

### 22. `relaxation`
- Term / rule conflict: `relaxation` is allowed by 2 entry field(s) and discouraged by 2 entry field(s).
- Allowed/preferred side: `passaddhi` preferred_translation (`terms/major/passaddhi.json`); `passaddhi` context_rules[0].rendering (`terms/major/passaddhi.json`)
- Discouraged side: `santi` discouraged_translations[2] (`terms/major/santi.json`); `upasama` discouraged_translations[1] (`terms/minor/upasama.json`)

### 23. `resentment`
- Term / rule conflict: `resentment` is allowed by 3 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `dosa` alternative_translations[1] (`terms/major/dosa.json`); `dosa` context_rules[2].rendering (`terms/major/dosa.json`); `upanaha` preferred_translation (`terms/minor/upanaha.json`)
- Discouraged side: `issa` discouraged_translations[0] (`terms/major/issa.json`)

### 24. `suppression`
- Term / rule conflict: `suppression` is allowed by 1 entry field(s) and discouraged by 7 entry field(s).
- Allowed/preferred side: `vikkhambhana` preferred_translation (`terms/minor/vikkhambhana.json`)
- Discouraged side: `pahana` discouraged_translations[0] (`terms/major/pahana.json`); `samvara` discouraged_translations[0] (`terms/major/samvara.json`); `vossagga` discouraged_translations[0] (`terms/major/vossagga.json`); `adhivasana` discouraged_translations[0] (`terms/minor/adhivasana.json`); `samatha` discouraged_translations[0] (`terms/minor/samatha.json`); `upasama` discouraged_translations[0] (`terms/minor/upasama.json`); `vinodana` discouraged_translations[0] (`terms/minor/vinodana.json`)

### 25. `taste`
- Term / rule conflict: `taste` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `rasa` preferred_translation (`terms/major/rasa.json`); `rasa` context_rules[0].rendering (`terms/major/rasa.json`)
- Discouraged side: `jivha` discouraged_translations[0] (`terms/major/jivha.json`)

### 26. `abandoning`
- Term / rule conflict: `abandoning` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `pahana` preferred_translation (`terms/major/pahana.json`); `pahana` context_rules[0].rendering (`terms/major/pahana.json`)
- Discouraged side: `vinodana` discouraged_translations[1] (`terms/minor/vinodana.json`)

### 27. `anger`
- Term / rule conflict: `anger` is allowed by 1 entry field(s) and discouraged by 2 entry field(s).
- Allowed/preferred side: `kodha` preferred_translation (`terms/minor/kodha.json`)
- Discouraged side: `byapada` discouraged_translations[0] (`terms/major/byapada.json`); `dosa` discouraged_translations[0] (`terms/major/dosa.json`)

### 28. `discipline`
- Term / rule conflict: `discipline` is allowed by 2 entry field(s) and discouraged by 2 entry field(s).
- Allowed/preferred side: `sikkha` alternative_translations[0] (`terms/minor/sikkha.json`); `vinaya` preferred_translation (`terms/minor/vinaya.json`)
- Discouraged side: `silabbata-paramasa` discouraged_translations[0] (`terms/major/silabbata-paramasa.json`); `silabbatupadana` discouraged_translations[0] (`terms/major/silabbatupadana.json`)

### 29. `heaven`
- Term / rule conflict: `heaven` is allowed by 1 entry field(s) and discouraged by 2 entry field(s).
- Allowed/preferred side: `sagga` preferred_translation (`terms/minor/sagga.json`)
- Discouraged side: `nibbana` discouraged_translations[2] (`terms/major/nibbana.json`); `parinibbana` discouraged_translations[2] (`terms/major/parinibbana.json`)

### 30. `death`
- Term / rule conflict: `death` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `maccu` preferred_translation (`terms/minor/maccu.json`); `mara` alternative_translations[1] (`terms/minor/mara.json`)
- Discouraged side: `parinibbana` discouraged_translations[0] (`terms/major/parinibbana.json`)

### 31. `effort`
- Term / rule conflict: `effort` is allowed by 1 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `vayama` preferred_translation (`terms/minor/vayama.json`)
- Discouraged side: `viriya` discouraged_translations[0] (`terms/major/viriya.json`)

### 32. `fear`
- Term / rule conflict: `fear` is allowed by 1 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `bhaya` preferred_translation (`terms/minor/bhaya.json`)
- Discouraged side: `ottappa` discouraged_translations[0] (`terms/major/ottappa.json`)

### 33. `object`
- Term / rule conflict: `object` is allowed by 1 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `arammana` preferred_translation (`terms/minor/arammana.json`)
- Discouraged side: `photthabba` discouraged_translations[0] (`terms/major/photthabba.json`)

### 34. `pleasant feeling`
- Term / rule conflict: `pleasant feeling` is allowed by 1 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `sukha-vedana` preferred_translation (`terms/minor/sukha-vedana.json`)
- Discouraged side: `kamacchanda` discouraged_translations[4] (`terms/major/kamacchanda.json`)

### 35. `unification of mind`
- Term / rule conflict: `unification of mind` is allowed by 1 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `cetaso-ekodibhava` preferred_translation (`terms/minor/cetaso-ekodibhava.json`)
- Discouraged side: `samadhi` discouraged_translations[2] (`terms/major/samadhi.json`)

### 36. `wrong view`
- Term / rule conflict: `wrong view` is allowed by 1 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `miccha-ditthi` preferred_translation (`terms/minor/miccha-ditthi.json`)
- Discouraged side: `ditthi` discouraged_translations[0] (`terms/major/ditthi.json`)

### 37. `earth element`
- Term / rule conflict: `earth element` is allowed by 1 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `pathavi-dhatu` preferred_translation (`terms/minor/pathavi-dhatu.json`)
- Discouraged side: `pathavi-kasina` discouraged_translations[0] (`terms/minor/pathavi-kasina.json`)

### 38. `fire element`
- Term / rule conflict: `fire element` is allowed by 1 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `tejo-dhatu` preferred_translation (`terms/minor/tejo-dhatu.json`)
- Discouraged side: `tejo-kasina` discouraged_translations[0] (`terms/minor/tejo-kasina.json`)

### 39. `space element`
- Term / rule conflict: `space element` is allowed by 1 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `akasa-dhatu` preferred_translation (`terms/minor/akasa-dhatu.json`)
- Discouraged side: `akasa-kasina` discouraged_translations[0] (`terms/minor/akasa-kasina.json`)

### 40. `stubbornness`
- Term / rule conflict: `stubbornness` is allowed by 1 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `thambha` preferred_translation (`terms/minor/thambha.json`)
- Discouraged side: `adhitthana` discouraged_translations[0] (`terms/minor/adhitthana.json`)

### 41. `water element`
- Term / rule conflict: `water element` is allowed by 1 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `apo-dhatu` preferred_translation (`terms/minor/apo-dhatu.json`)
- Discouraged side: `apo-kasina` discouraged_translations[0] (`terms/minor/apo-kasina.json`)

### 42. `attachment`
- Term / rule conflict: `attachment` is allowed by 2 entry field(s) and discouraged by 8 entry field(s).
- Allowed/preferred side: `raga` alternative_translations[0] (`terms/major/raga.json`); `raga` context_rules[1].rendering (`terms/major/raga.json`)
- Discouraged side: `chanda` discouraged_translations[1] (`terms/major/chanda.json`); `gantha` discouraged_translations[1] (`terms/major/gantha.json`); `ogha` discouraged_translations[1] (`terms/major/ogha.json`); `samyojana` discouraged_translations[0] (`terms/major/samyojana.json`); `tanha` discouraged_translations[1] (`terms/major/tanha.json`); `upadana` discouraged_translations[0] (`terms/major/upadana.json`); `yoga` discouraged_translations[0] (`terms/major/yoga.json`); `chandaraga` discouraged_translations[1] (`terms/minor/chandaraga.json`)

### 43. `cessation`
- Term / rule conflict: `cessation` is allowed by 2 entry field(s) and discouraged by 4 entry field(s).
- Allowed/preferred side: `nirodha` alternative_translations[1] (`terms/major/nirodha.json`); `nirodha` context_rules[4].rendering (`terms/major/nirodha.json`)
- Discouraged side: `khaya` discouraged_translations[0] (`terms/major/khaya.json`); `pahana` discouraged_translations[1] (`terms/major/pahana.json`); `viraga` discouraged_translations[2] (`terms/major/viraga.json`); `vossagga` discouraged_translations[1] (`terms/major/vossagga.json`)

### 44. `consciousness`
- Term / rule conflict: `consciousness` is allowed by 2 entry field(s) and discouraged by 3 entry field(s).
- Allowed/preferred side: `vinnana` alternative_translations[0] (`terms/major/vinnana.json`); `vinnana` context_rules[3].rendering (`terms/major/vinnana.json`)
- Discouraged side: `citta` discouraged_translations[0] (`terms/major/citta.json`); `mano` discouraged_translations[0] (`terms/major/mano.json`); `vijja` discouraged_translations[2] (`terms/major/vijja.json`)

### 45. `understands`
- Term / rule conflict: `understands` is allowed by 4 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `janati` alternative_translations[1] (`terms/major/janati.json`); `janati` context_rules[2].rendering (`terms/major/janati.json`); `pajanati` alternative_translations[1] (`terms/major/pajanati.json`); `pajanati` context_rules[2].rendering (`terms/major/pajanati.json`)
- Discouraged side: `mannati` discouraged_translations[2] (`terms/major/mannati.json`)

### 46. `cognition`
- Term / rule conflict: `cognition` is allowed by 2 entry field(s) and discouraged by 2 entry field(s).
- Allowed/preferred side: `mano` alternative_translations[0] (`terms/major/mano.json`); `mano` context_rules[2].rendering (`terms/major/mano.json`)
- Discouraged side: `citta` discouraged_translations[1] (`terms/major/citta.json`); `nana` discouraged_translations[2] (`terms/major/nana.json`)

### 47. `craving`
- Term / rule conflict: `craving` is allowed by 2 entry field(s) and discouraged by 3 entry field(s).
- Allowed/preferred side: `tanha` alternative_translations[0] (`terms/major/tanha.json`); `tanha` context_rules[1].rendering (`terms/major/tanha.json`)
- Discouraged side: `chanda` discouraged_translations[0] (`terms/major/chanda.json`); `raga` discouraged_translations[2] (`terms/major/raga.json`); `chandaraga` discouraged_translations[0] (`terms/minor/chandaraga.json`)

### 48. `hindrance`
- Term / rule conflict: `hindrance` is allowed by 2 entry field(s) and discouraged by 2 entry field(s).
- Allowed/preferred side: `nivarana` alternative_translations[0] (`terms/major/nivarana.json`); `nivarana` context_rules[1].rendering (`terms/major/nivarana.json`)
- Discouraged side: `kilesa` discouraged_translations[1] (`terms/major/kilesa.json`); `upakkilesa` discouraged_translations[1] (`terms/major/upakkilesa.json`)

### 49. `liberation`
- Term / rule conflict: `liberation` is allowed by 2 entry field(s) and discouraged by 2 entry field(s).
- Allowed/preferred side: `vimutti` alternative_translations[0] (`terms/major/vimutti.json`); `vimutti` context_rules[1].rendering (`terms/major/vimutti.json`)
- Discouraged side: `mutti` discouraged_translations[0] (`terms/major/mutti.json`); `nissarana` discouraged_translations[0] (`terms/major/nissarana.json`)

### 50. `bad`
- Term / rule conflict: `bad` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `papa` alternative_translations[0] (`terms/major/papa.json`); `papa` context_rules[1].rendering (`terms/major/papa.json`)
- Discouraged side: `akusala` discouraged_translations[0] (`terms/major/akusala.json`)

### 51. `behavior`
- Term / rule conflict: `behavior` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `kamma` alternative_translations[1] (`terms/major/kamma.json`); `kamma` context_rules[2].rendering (`terms/major/kamma.json`)
- Discouraged side: `patipada` discouraged_translations[0] (`terms/major/patipada.json`)

### 52. `belief`
- Term / rule conflict: `belief` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `ditthi` alternative_translations[2] (`terms/major/ditthi.json`); `ditthi` context_rules[4].rendering (`terms/major/ditthi.json`)
- Discouraged side: `saddha` discouraged_translations[0] (`terms/major/saddha.json`)

### 53. `doubt`
- Term / rule conflict: `doubt` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `vicikiccha` alternative_translations[0] (`terms/major/vicikiccha.json`); `vicikiccha` context_rules[1].rendering (`terms/major/vicikiccha.json`)
- Discouraged side: `vimamsa` discouraged_translations[0] (`terms/major/vimamsa.json`)

### 54. `fuel`
- Term / rule conflict: `fuel` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `upadana` alternative_translations[3] (`terms/major/upadana.json`); `upadana` context_rules[4].rendering (`terms/major/upadana.json`)
- Discouraged side: `ahara` discouraged_translations[0] (`terms/major/ahara.json`)

### 55. `interest`
- Term / rule conflict: `interest` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `chanda` alternative_translations[1] (`terms/major/chanda.json`); `chanda` context_rules[2].rendering (`terms/major/chanda.json`)
- Discouraged side: `kamacchanda` discouraged_translations[1] (`terms/major/kamacchanda.json`)

### 56. `joy`
- Term / rule conflict: `joy` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `piti` alternative_translations[0] (`terms/major/piti.json`); `piti` context_rules[1].rendering (`terms/major/piti.json`)
- Discouraged side: `nandi` discouraged_translations[2] (`terms/major/nandi.json`)

### 57. `kindness`
- Term / rule conflict: `kindness` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `adosa` alternative_translations[0] (`terms/major/adosa.json`); `adosa` context_rules[1].rendering (`terms/major/adosa.json`)
- Discouraged side: `abyapada` discouraged_translations[0] (`terms/major/abyapada.json`)

### 58. `latent tendency`
- Term / rule conflict: `latent tendency` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `anusaya` alternative_translations[0] (`terms/major/anusaya.json`); `anusaya` context_rules[1].rendering (`terms/major/anusaya.json`)
- Discouraged side: `pariyutthana` discouraged_translations[2] (`terms/major/pariyutthana.json`)

### 59. `mood`
- Term / rule conflict: `mood` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `citta` alternative_translations[3] (`terms/major/citta.json`); `citta` context_rules[3].rendering (`terms/major/citta.json`)
- Discouraged side: `vedana` discouraged_translations[1] (`terms/major/vedana.json`)

### 60. `smell`
- Term / rule conflict: `smell` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `gandha` alternative_translations[0] (`terms/major/gandha.json`); `gandha` context_rules[1].rendering (`terms/major/gandha.json`)
- Discouraged side: `ghana` discouraged_translations[0] (`terms/major/ghana.json`)

### 61. `stress`
- Term / rule conflict: `stress` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `dukkha` alternative_translations[1] (`terms/major/dukkha.json`); `dukkha` context_rules[2].rendering (`terms/major/dukkha.json`)
- Discouraged side: `upayasa` discouraged_translations[0] (`terms/major/upayasa.json`)

### 62. `understanding`
- Term / rule conflict: `understanding` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `panna` alternative_translations[0] (`terms/major/panna.json`); `panna` context_rules[1].rendering (`terms/major/panna.json`)
- Discouraged side: `parinna` discouraged_translations[0] (`terms/major/parinna.json`)

### 63. `vision`
- Term / rule conflict: `vision` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `dassana` alternative_translations[1] (`terms/major/dassana.json`); `dassana` context_rules[2].rendering (`terms/major/dassana.json`)
- Discouraged side: `cakkhu-vinnana` discouraged_translations[0] (`terms/major/cakkhu-vinnana.json`)

### 64. `conceptual proliferation`
- Term / rule conflict: `conceptual proliferation` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `papanca` alternative_translations[0] (`terms/major/papanca.json`); `papanca` context_rules[1].rendering (`terms/major/papanca.json`)
- Discouraged side: `papanca-sanna-sankha` discouraged_translations[1] (`terms/minor/papanca-sanna-sankha.json`)

### 65. `law`
- Term / rule conflict: `law` is allowed by 2 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `dhamma` alternative_translations[4] (`terms/major/dhamma.json`); `dhamma` context_rules[5].rendering (`terms/major/dhamma.json`)
- Discouraged side: `vinaya` discouraged_translations[0] (`terms/minor/vinaya.json`)

### 66. `sensation`
- Term / rule conflict: `sensation` is allowed by 1 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `vedana` alternative_translations[2] (`terms/major/vedana.json`)
- Discouraged side: `phassa` discouraged_translations[0] (`terms/major/phassa.json`)

### 67. `arrogance`
- Term / rule conflict: `arrogance` is allowed by 1 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `mada` alternative_translations[0] (`terms/minor/mada.json`)
- Discouraged side: `mana` discouraged_translations[1] (`terms/major/mana.json`)

### 68. `attraction`
- Term / rule conflict: `attraction` is allowed by 1 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `anunaya` alternative_translations[0] (`terms/minor/anunaya.json`)
- Discouraged side: `kamacchanda` discouraged_translations[2] (`terms/major/kamacchanda.json`)

### 69. `perfection`
- Term / rule conflict: `perfection` is allowed by 1 entry field(s) and discouraged by 1 entry field(s).
- Allowed/preferred side: `paramita` alternative_translations[0] (`terms/minor/paramita.json`)
- Discouraged side: `parisuddhi` discouraged_translations[0] (`terms/minor/parisuddhi.json`)

## 3. Missing Rule Fields

The live schema requires these fields for major entries and allows lighter minor entries. This audit treats the requested components as required audit surfaces for every term, so minor entries are listed when they omit them.

- Major entries missing any audited component: 0
- Minor entries missing any audited component: 847
- Total entries missing at least one audited component: 847

### Missing `discouraged_translations`, `context_rules`, `example_phrases` (535 term entries)

- `abhijjhā` (`abhijjha`; minor) ? `terms/minor/abhijjha.json`
- `abhisamaya` (`abhisamaya`; minor) ? `terms/minor/abhisamaya.json`
- `abhisaṅkhāra` (`abhisankhara`; minor) ? `terms/minor/abhisankhara.json`
- `abrahmacariya-veramani` (`abrahmacariya-veramani`; minor) ? `terms/minor/abrahmacariya-veramani.json`
- `abrahmacariya` (`abrahmacariya`; minor) ? `terms/minor/abrahmacariya.json`
- `abyāpāda-dhātu` (`abyapada-dhatu`; minor) ? `terms/minor/abyapada-dhatu.json`
- `acariya` (`acariya`; minor) ? `terms/minor/acariya.json`
- `aḍḍha` (`addha`; minor) ? `terms/minor/addha.json`
- `adhikaraṇa` (`adhikarana`; minor) ? `terms/minor/adhikarana.json`
- `adhimokkha` (`adhimokkha`; minor) ? `terms/minor/adhimokkha.json`
- `adhipati-paccaya` (`adhipati-paccaya`; minor) ? `terms/minor/adhipati-paccaya.json`
- `adhipati` (`adhipati`; minor) ? `terms/minor/adhipati.json`
- `adinava-nana` (`adinava-nana`; minor) ? `terms/minor/adinava-nana.json`
- `adinnadana-veramani` (`adinnadana-veramani`; minor) ? `terms/minor/adinnadana-veramani.json`
- `adosamūla` (`adosa-mula`; minor) ? `terms/minor/adosa-mula.json`
- `adukkhamasukhavedanā` (`adukkhamasukha-vedana`; minor) ? `terms/minor/adukkhamasukha-vedana.json`
- `āgantuka` (`agantuka`; minor) ? `terms/minor/agantuka.json`
- `agāra` (`agara`; minor) ? `terms/minor/agara.json`
- `ahara-paccaya` (`ahara-paccaya`; minor) ? `terms/minor/ahara-paccaya.json`
- `ahare-patikula-sanna` (`ahare-patikula-sanna`; minor) ? `terms/minor/ahare-patikula-sanna.json`
- `ahetuka` (`ahetuka`; minor) ? `terms/minor/ahetuka.json`
- `ahirika` (`ahirika`; minor) ? `terms/minor/ahirika.json`
- `Ajātasattu` (`ajatasattu`; minor) ? `terms/minor/ajatasattu.json`
- `ajiva` (`ajiva`; minor) ? `terms/minor/ajiva.json`
- `akasa-dhatu` (`akasa-dhatu`; minor) ? `terms/minor/akasa-dhatu.json`
- `akuppā-cetovimutti` (`akuppa-cetovimutti`; minor) ? `terms/minor/akuppa-cetovimutti.json`
- `akusala-dhamma` (`akusala-dhamma`; minor) ? `terms/minor/akusala-dhamma.json`
- `alobhamūla` (`alobha-mula`; minor) ? `terms/minor/alobha-mula.json`
- `amacca` (`amacca`; minor) ? `terms/minor/amacca.json`
- `Ambapālī` (`ambapali`; minor) ? `terms/minor/ambapali.json`
- `āmisa-pīti` (`amisa-piti`; minor) ? `terms/minor/amisa-piti.json`
- `āmisa-sukha` (`amisa-sukha`; minor) ? `terms/minor/amisa-sukha.json`
- `amohamūla` (`amoha-mula`; minor) ? `terms/minor/amoha-mula.json`
- `anagami-magga` (`anagami-magga`; minor) ? `terms/minor/anagami-magga.json`
- `anāgāmiphala` (`anagami-phala`; minor) ? `terms/minor/anagami-phala.json`
- `anagāriya` (`anagariya`; minor) ? `terms/minor/anagariya.json`
- `Ānanda` (`ananda`; minor) ? `terms/minor/ananda.json`
- `anantara-paccaya` (`anantara-paccaya`; minor) ? `terms/minor/anantara-paccaya.json`
- `anantara` (`anantara`; minor) ? `terms/minor/anantara.json`
- `Anāthapiṇḍika` (`anathapindika`; minor) ? `terms/minor/anathapindika.json`
- `aneñjābhisaṅkhāra` (`anenjabhisankhara`; minor) ? `terms/minor/anenjabhisankhara.json`
- `animitta-cetosamadhi` (`animitta-cetosamadhi`; minor) ? `terms/minor/animitta-cetosamadhi.json`
- `animitta-samadhi` (`animitta-samadhi`; minor) ? `terms/minor/animitta-samadhi.json`
- `animitta-vimokkha` (`animitta-vimokkha`; minor) ? `terms/minor/animitta-vimokkha.json`
- `anissita` (`anissita`; minor) ? `terms/minor/anissita.json`
- `annamanya-paccaya` (`annamanya-paccaya`; minor) ? `terms/minor/annamanya-paccaya.json`
- `annamanya` (`annamanya`; minor) ? `terms/minor/annamanya.json`
- `anottappa` (`anottappa`; minor) ? `terms/minor/anottappa.json`
- `anta` (`anta`; minor) ? `terms/minor/anta.json`
- `antaguna` (`antaguna`; minor) ? `terms/minor/antaguna.json`
- `antevāsika` (`antevasika`; minor) ? `terms/minor/antevasika.json`
- `antevasin` (`antevasin`; minor) ? `terms/minor/antevasin.json`
- `anubyañjana` (`anubyanjana`; minor) ? `terms/minor/anubyanjana.json`
- `anuloma-khanti` (`anuloma-khanti`; minor) ? `terms/minor/anuloma-khanti.json`
- `anuloma-nana` (`anuloma-nana`; minor) ? `terms/minor/anuloma-nana.json`
- `anuloma` (`anuloma`; minor) ? `terms/minor/anuloma.json`
- `anunaya` (`anunaya`; minor) ? `terms/minor/anunaya.json`
- `Anuruddha` (`anuruddha`; minor) ? `terms/minor/anuruddha.json`
- `anusāsanā` (`anusasana`; minor) ? `terms/minor/anusasana.json`
- `anussati` (`anussati`; minor) ? `terms/minor/anussati.json`
- `apāya` (`apaya`; minor) ? `terms/minor/apaya.json`
- `apo-dhatu` (`apo-dhatu`; minor) ? `terms/minor/apo-dhatu.json`
- `apo` (`apo`; minor) ? `terms/minor/apo.json`
- `appamana` (`appamana`; minor) ? `terms/minor/appamana.json`
- `appana-samadhi` (`appana-samadhi`; minor) ? `terms/minor/appana-samadhi.json`
- `appanihita-cetosamadhi` (`appanihita-cetosamadhi`; minor) ? `terms/minor/appanihita-cetosamadhi.json`
- `appanihita-samadhi` (`appanihita-samadhi`; minor) ? `terms/minor/appanihita-samadhi.json`
- `appanihita-vimokkha` (`appanihita-vimokkha`; minor) ? `terms/minor/appanihita-vimokkha.json`
- `apuññābhisaṅkhāra` (`apunnabhisankhara`; minor) ? `terms/minor/apunnabhisankhara.json`
- `āraddhavīriya` (`araddha-viriya`; minor) ? `terms/minor/araddha-viriya.json`
- `arahatta-magga` (`arahatta-magga`; minor) ? `terms/minor/arahatta-magga.json`
- `arahattaphala` (`arahatta-phala`; minor) ? `terms/minor/arahatta-phala.json`
- `arahatta` (`arahatta`; minor) ? `terms/minor/arahatta.json`
- `ārāma` (`arama`; minor) ? `terms/minor/arama.json`
- `arammana-paccaya` (`arammana-paccaya`; minor) ? `terms/minor/arammana-paccaya.json`
- `arammana` (`arammana`; minor) ? `terms/minor/arammana.json`
- `ariyasaṅgha` (`ariyasangha`; minor) ? `terms/minor/ariyasangha.json`
- `arūpa-dhātu` (`arupa-dhatu`; minor) ? `terms/minor/arupa-dhatu.json`
- `asappurisadhamma` (`asappurisa-dhamma`; minor) ? `terms/minor/asappurisa-dhamma.json`
- `asappurisa` (`asappurisa`; minor) ? `terms/minor/asappurisa.json`
- `asevana-paccaya` (`asevana-paccaya`; minor) ? `terms/minor/asevana-paccaya.json`
- `asevana` (`asevana`; minor) ? `terms/minor/asevana.json`
- `assu` (`assu`; minor) ? `terms/minor/assu.json`
- `asubha-sanna` (`asubha-sanna`; minor) ? `terms/minor/asubha-sanna.json`
- `asubha` (`asubha`; minor) ? `terms/minor/asubha.json`
- `asubhānupassanā` (`asubhanupassana`; minor) ? `terms/minor/asubhanupassana.json`
- `asura` (`asura`; minor) ? `terms/minor/asura.json`
- `asurakāya` (`asurakaya`; minor) ? `terms/minor/asurakaya.json`
- `asuraloka` (`asuraloka`; minor) ? `terms/minor/asuraloka.json`
- `ātāpī` (`atapi`; minor) ? `terms/minor/atapi.json`
- `ātappa` (`atappa`; minor) ? `terms/minor/atappa.json`
- `atthalokadhamma` (`atthalokadhamma`; minor) ? `terms/minor/atthalokadhamma.json`
- `atthi-paccaya` (`atthi-paccaya`; minor) ? `terms/minor/atthi-paccaya.json`
- `atthi` (`atthi`; minor) ? `terms/minor/atthi.json`
- `atthika-asubha` (`atthika-asubha`; minor) ? `terms/minor/atthika-asubha.json`
- `atthiminja` (`atthiminja`; minor) ? `terms/minor/atthiminja.json`
- `aveccappasada` (`aveccappasada`; minor) ? `terms/minor/aveccappasada.json`
- `avigata-paccaya` (`avigata-paccaya`; minor) ? `terms/minor/avigata-paccaya.json`
- `avigata` (`avigata`; minor) ? `terms/minor/avigata.json`
- `avihiṃsā-dhātu` (`avihimsa-dhatu`; minor) ? `terms/minor/avihimsa-dhatu.json`
- `ayonisomanasikara` (`ayonisomanasikara`; minor) ? `terms/minor/ayonisomanasikara.json`
- `bandhu` (`bandhu`; minor) ? `terms/minor/bandhu.json`
- `bhanga-nana` (`bhanga-nana`; minor) ? `terms/minor/bhanga-nana.json`
- `bhatta` (`bhatta`; minor) ? `terms/minor/bhatta.json`
- `bhaya-nana` (`bhaya-nana`; minor) ? `terms/minor/bhaya-nana.json`
- `bhaya` (`bhaya`; minor) ? `terms/minor/bhaya.json`
- `bhayagati` (`bhayagati`; minor) ? `terms/minor/bhayagati.json`
- `bhesajja` (`bhesajja`; minor) ? `terms/minor/bhesajja.json`
- `bhikkhu-sangha` (`bhikkhu-sangha`; minor) ? `terms/minor/bhikkhu-sangha.json`
- `bhikkhuni-sangha` (`bhikkhuni-sangha`; minor) ? `terms/minor/bhikkhuni-sangha.json`
- `bhojane-mattannuta` (`bhojane-mattannuta`; minor) ? `terms/minor/bhojane-mattannuta.json`
- `bhojanīya` (`bhojaniya`; minor) ? `terms/minor/bhojaniya.json`
- `bhūta` (`bhuta`; minor) ? `terms/minor/bhuta.json`
- `Bimbisāra` (`bimbisara`; minor) ? `terms/minor/bimbisara.json`
- `brahma-yoni` (`brahma-yoni`; minor) ? `terms/minor/brahma-yoni.json`
- `brahma` (`brahma`; minor) ? `terms/minor/brahma.json`
- `brahmaloka` (`brahmaloka`; minor) ? `terms/minor/brahmaloka.json`
- `brāhmaṇa` (`brahmana`; minor) ? `terms/minor/brahmana.json`
- `brahmavihāra` (`brahmavihara`; minor) ? `terms/minor/brahmavihara.json`
- `caga-dhana` (`caga-dhana`; minor) ? `terms/minor/caga-dhana.json`
- `cakkhu-dvara` (`cakkhu-dvara`; minor) ? `terms/minor/cakkhu-dvara.json`
- `cattaro-iddhipada` (`cattaro-iddhipada`; minor) ? `terms/minor/cattaro-iddhipada.json`
- `cattaro-sammappadhana` (`cattaro-sammappadhana`; minor) ? `terms/minor/cattaro-sammappadhana.json`
- `catu-dhatu` (`catu-dhatu`; minor) ? `terms/minor/catu-dhatu.json`
- `catudhatu-vavatthana` (`catudhatu-vavatthana`; minor) ? `terms/minor/catudhatu-vavatthana.json`
- `catuparisa` (`catuparisa`; minor) ? `terms/minor/catuparisa.json`
- `cetanā-dhātu` (`cetana-dhatu`; minor) ? `terms/minor/cetana-dhatu.json`
- `cetanasampanna` (`cetanasampanna`; minor) ? `terms/minor/cetanasampanna.json`
- `ceto-vimutti` (`ceto-vimutti`; minor) ? `terms/minor/ceto-vimutti.json`
- `ceto-viveka` (`ceto-viveka`; minor) ? `terms/minor/ceto-viveka.json`
- `cetosamadhi` (`cetosamadhi`; minor) ? `terms/minor/cetosamadhi.json`
- `cetosamatha` (`cetosamatha`; minor) ? `terms/minor/cetosamatha.json`
- `cha-dvarani` (`cha-dvarani`; minor) ? `terms/minor/cha-dvarani.json`
- `chandagati` (`chandagati`; minor) ? `terms/minor/chandagati.json`
- `cittiddhipāda` (`citta-iddhipada`; minor) ? `terms/minor/citta-iddhipada.json`
- `citta-kammannata` (`citta-kammannata`; minor) ? `terms/minor/citta-kammannata.json`
- `citta-lahuta` (`citta-lahuta`; minor) ? `terms/minor/citta-lahuta.json`
- `citta-muduta` (`citta-muduta`; minor) ? `terms/minor/citta-muduta.json`
- `citta-pagunnata` (`citta-pagunnata`; minor) ? `terms/minor/citta-pagunnata.json`
- `citta-passaddhi` (`citta-passaddhi`; minor) ? `terms/minor/citta-passaddhi.json`
- `cittasaṅkhāra` (`citta-sankhara`; minor) ? `terms/minor/citta-sankhara.json`
- `citta-ujjukata` (`citta-ujjukata`; minor) ? `terms/minor/citta-ujjukata.json`
- `cittabhāvanā` (`cittabhavana`; minor) ? `terms/minor/cittabhavana.json`
- `cīvara` (`civara`; minor) ? `terms/minor/civara.json`
- `cīvarapaccaya` (`civarapaccaya`; minor) ? `terms/minor/civarapaccaya.json`
- `Cunda` (`cunda`; minor) ? `terms/minor/cunda.json`
- `daharabhikkhu` (`daharabhikkhu`; minor) ? `terms/minor/daharabhikkhu.json`
- `dalidda` (`dalidda`; minor) ? `terms/minor/dalidda.json`
- `danta` (`danta`; minor) ? `terms/minor/danta.json`
- `dāraka` (`daraka`; minor) ? `terms/minor/daraka.json`
- `dārikā` (`darika`; minor) ? `terms/minor/darika.json`
- `desa` (`desa`; minor) ? `terms/minor/desa.json`
- `deva-yoni` (`deva-yoni`; minor) ? `terms/minor/deva-yoni.json`
- `deva` (`deva`; minor) ? `terms/minor/deva.json`
- `Devadatta` (`devadatta`; minor) ? `terms/minor/devadatta.json`
- `devaloka` (`devaloka`; minor) ? `terms/minor/devaloka.json`
- `devaputta` (`devaputta`; minor) ? `terms/minor/devaputta.json`
- `dhamma-tanha` (`dhamma-tanha`; minor) ? `terms/minor/dhamma-tanha.json`
- `dhammacakkhu` (`dhammacakkhu`; minor) ? `terms/minor/dhammacakkhu.json`
- `dhammaniyāma` (`dhammaniyama`; minor) ? `terms/minor/dhammaniyama.json`
- `dhammavicayasambojjhaṅga` (`dhammavicaya-sambojjhanga`; minor) ? `terms/minor/dhammavicaya-sambojjhanga.json`
- `dhātu` (`dhatu`; minor) ? `terms/minor/dhatu.json`
- `dhītā` (`dhita`; minor) ? `terms/minor/dhita.json`
- `ditthadhamma-sukha-vihara` (`ditthadhamma-sukha-vihara`; minor) ? `terms/minor/ditthadhamma-sukha-vihara.json`
- `dosamūla` (`dosa-mula`; minor) ? `terms/minor/dosa-mula.json`
- `dosagati` (`dosagati`; minor) ? `terms/minor/dosagati.json`
- `duccarita` (`duccarita`; minor) ? `terms/minor/duccarita.json`
- `duggati` (`duggati`; minor) ? `terms/minor/duggati.json`
- `dukkhavedanā` (`dukkha-vedana`; minor) ? `terms/minor/dukkha-vedana.json`
- `dūta` (`duta`; minor) ? `terms/minor/duta.json`
- `dvāra` (`dvara`; minor) ? `terms/minor/dvara.json`
- `gahakāraka` (`gahakaraka`; minor) ? `terms/minor/gahakaraka.json`
- `gahapati-duhitā` (`gahapati-duhita`; minor) ? `terms/minor/gahapati-duhita.json`
- `gahapati-putta` (`gahapati-putta`; minor) ? `terms/minor/gahapati-putta.json`
- `gahapati` (`gahapati`; minor) ? `terms/minor/gahapati.json`
- `gahaṭṭha` (`gahattha`; minor) ? `terms/minor/gahattha.json`
- `gāmaka` (`gamaka`; minor) ? `terms/minor/gamaka.json`
- `gandha-tanha` (`gandha-tanha`; minor) ? `terms/minor/gandha-tanha.json`
- `gandhabba` (`gandhabba`; minor) ? `terms/minor/gandhabba.json`
- `garuḷa` (`garula`; minor) ? `terms/minor/garula.json`
- `ghana-dvara` (`ghana-dvara`; minor) ? `terms/minor/ghana-dvara.json`
- `gharāvāsa` (`gharavasa`; minor) ? `terms/minor/gharavasa.json`
- `gihinī` (`gihini`; minor) ? `terms/minor/gihini.json`
- `gilānapaccaya` (`gilanapaccaya`; minor) ? `terms/minor/gilanapaccaya.json`
- `gocara` (`gocara`; minor) ? `terms/minor/gocara.json`
- `gotrabhu-nana` (`gotrabhu-nana`; minor) ? `terms/minor/gotrabhu-nana.json`
- `gotrabhū` (`gotrabhu`; minor) ? `terms/minor/gotrabhu.json`
- `hadaya` (`hadaya`; minor) ? `terms/minor/hadaya.json`
- `hatavikkhittaka` (`hatavikkhittaka`; minor) ? `terms/minor/hatavikkhittaka.json`
- `hetu-paccaya` (`hetu-paccaya`; minor) ? `terms/minor/hetu-paccaya.json`
- `hiri-dhana` (`hiri-dhana`; minor) ? `terms/minor/hiri-dhana.json`
- `hiri-ottappa` (`hiri-ottappa`; minor) ? `terms/minor/hiri-ottappa.json`
- `indriyabala` (`indriya-bala`; minor) ? `terms/minor/indriya-bala.json`
- `indriya-bhavana` (`indriya-bhavana`; minor) ? `terms/minor/indriya-bhavana.json`
- `indriya-paccaya` (`indriya-paccaya`; minor) ? `terms/minor/indriya-paccaya.json`
- `itthī` (`itthi`; minor) ? `terms/minor/itthi.json`
- `itthibhāva` (`itthibhava`; minor) ? `terms/minor/itthibhava.json`
- `jagariya` (`jagariya`; minor) ? `terms/minor/jagariya.json`
- `jana` (`jana`; minor) ? `terms/minor/jana.json`
- `janapada` (`janapada`; minor) ? `terms/minor/janapada.json`
- `jhana-paccaya` (`jhana-paccaya`; minor) ? `terms/minor/jhana-paccaya.json`
- `jhaya` (`jhaya`; minor) ? `terms/minor/jhaya.json`
- `jivha-dvara` (`jivha-dvara`; minor) ? `terms/minor/jivha-dvara.json`
- `jivitindriya` (`jivitindriya`; minor) ? `terms/minor/jivitindriya.json`
- `kālakata` (`kalakata`; minor) ? `terms/minor/kalakata.json`
- `kalyana-mitta` (`kalyana-mitta`; minor) ? `terms/minor/kalyana-mitta.json`
- `kalyāṇamittatā` (`kalyanamittata`; minor) ? `terms/minor/kalyanamittata.json`
- `kamma-paccaya` (`kamma-paccaya`; minor) ? `terms/minor/kamma-paccaya.json`
- `kammannacitta` (`kammannacitta`; minor) ? `terms/minor/kammannacitta.json`
- `kammanta` (`kammanta`; minor) ? `terms/minor/kammanta.json`
- `kammassakata` (`kammassakata`; minor) ? `terms/minor/kammassakata.json`
- `karisa` (`karisa`; minor) ? `terms/minor/karisa.json`
- `karuṇācetovimutti` (`karuna-cetovimutti`; minor) ? `terms/minor/karuna-cetovimutti.json`
- `kaya-dvara` (`kaya-dvara`; minor) ? `terms/minor/kaya-dvara.json`
- `kaya-gata` (`kaya-gata`; minor) ? `terms/minor/kaya-gata.json`
- `kaya-kamma` (`kaya-kamma`; minor) ? `terms/minor/kaya-kamma.json`
- `kaya-kammannata` (`kaya-kammannata`; minor) ? `terms/minor/kaya-kammannata.json`
- `kaya-lahuta` (`kaya-lahuta`; minor) ? `terms/minor/kaya-lahuta.json`
- `kaya-muduta` (`kaya-muduta`; minor) ? `terms/minor/kaya-muduta.json`
- `kaya-pagunnata` (`kaya-pagunnata`; minor) ? `terms/minor/kaya-pagunnata.json`
- `kaya-passaddhi` (`kaya-passaddhi`; minor) ? `terms/minor/kaya-passaddhi.json`
- `kaya-ujjukata` (`kaya-ujjukata`; minor) ? `terms/minor/kaya-ujjukata.json`
- `kaya-viveka` (`kaya-viveka`; minor) ? `terms/minor/kaya-viveka.json`
- `kesa` (`kesa`; minor) ? `terms/minor/kesa.json`
- `khādanīya` (`khadaniya`; minor) ? `terms/minor/khadaniya.json`
- `khelo` (`khelo`; minor) ? `terms/minor/khelo.json`
- `Khemā` (`khema`; minor) ? `terms/minor/khema.json`
- `khetta` (`khetta`; minor) ? `terms/minor/khetta.json`
- `kilomaka` (`kilomaka`; minor) ? `terms/minor/kilomaka.json`
- `kinnara` (`kinnara`; minor) ? `terms/minor/kinnara.json`
- `kiriyā` (`kiriya`; minor) ? `terms/minor/kiriya.json`
- `Kisāgotamī` (`kisagotami`; minor) ? `terms/minor/kisagotami.json`
- `kodha` (`kodha`; minor) ? `terms/minor/kodha.json`
- `kulaputta` (`kulaputta`; minor) ? `terms/minor/kulaputta.json`
- `kumāra` (`kumara`; minor) ? `terms/minor/kumara.json`
- `kumārī` (`kumari`; minor) ? `terms/minor/kumari.json`
- `kuṭāgāra` (`kutagara`; minor) ? `terms/minor/kutagara.json`
- `lasika` (`lasika`; minor) ? `terms/minor/lasika.json`
- `lobhamūla` (`lobha-mula`; minor) ? `terms/minor/lobha-mula.json`
- `lokadhamma` (`lokadhamma`; minor) ? `terms/minor/lokadhamma.json`
- `lokiya-samadhi` (`lokiya-samadhi`; minor) ? `terms/minor/lokiya-samadhi.json`
- `lokuttara-samadhi` (`lokuttara-samadhi`; minor) ? `terms/minor/lokuttara-samadhi.json`
- `loma` (`loma`; minor) ? `terms/minor/loma.json`
- `maccu` (`maccu`; minor) ? `terms/minor/maccu.json`
- `mada` (`mada`; minor) ? `terms/minor/mada.json`
- `magga-nana` (`magga-nana`; minor) ? `terms/minor/magga-nana.json`
- `magga-paccaya` (`magga-paccaya`; minor) ? `terms/minor/magga-paccaya.json`
- `maggaphala` (`magga-phala`; minor) ? `terms/minor/magga-phala.json`
- `mahābhūta` (`mahabhuta`; minor) ? `terms/minor/mahabhuta.json`
- `Mahākaccāna` (`mahakaccana`; minor) ? `terms/minor/mahakaccana.json`
- `Mahākassapa` (`mahakassapa`; minor) ? `terms/minor/mahakassapa.json`
- `Mahāpajāpatī` (`mahapajapati`; minor) ? `terms/minor/mahapajapati.json`
- `mahāsāla` (`mahasala`; minor) ? `terms/minor/mahasala.json`
- `makkha` (`makkha`; minor) ? `terms/minor/makkha.json`
- `mālāgandhavilepana` (`mala-gandha-vilepana`; minor) ? `terms/minor/mala-gandha-vilepana.json`
- `Mallikā` (`mallika`; minor) ? `terms/minor/mallika.json`
- `mamsa` (`mamsa`; minor) ? `terms/minor/mamsa.json`
- `mānatta` (`manatta`; minor) ? `terms/minor/manatta.json`
- `mano-dvara` (`mano-dvara`; minor) ? `terms/minor/mano-dvara.json`
- `mano-kamma` (`mano-kamma`; minor) ? `terms/minor/mano-kamma.json`
- `manussa-yoni` (`manussa-yoni`; minor) ? `terms/minor/manussa-yoni.json`
- `manussa` (`manussa`; minor) ? `terms/minor/manussa.json`
- `manussaloka` (`manussaloka`; minor) ? `terms/minor/manussaloka.json`
- `marana-sanna` (`marana-sanna`; minor) ? `terms/minor/marana-sanna.json`
- `mātā` (`mata`; minor) ? `terms/minor/mata.json`
- `matthalunga` (`matthalunga`; minor) ? `terms/minor/matthalunga.json`
- `mātugāma` (`matugama`; minor) ? `terms/minor/matugama.json`
- `medo` (`medo`; minor) ? `terms/minor/medo.json`
- `mettācetovimutti` (`metta-cetovimutti`; minor) ? `terms/minor/metta-cetovimutti.json`
- `mitta` (`mitta`; minor) ? `terms/minor/mitta.json`
- `Moggallāna` (`moggallana`; minor) ? `terms/minor/moggallana.json`
- `mohamūla` (`moha-mula`; minor) ? `terms/minor/moha-mula.json`
- `mohagati` (`mohagati`; minor) ? `terms/minor/mohagati.json`
- `muditācetovimutti` (`mudita-cetovimutti`; minor) ? `terms/minor/mudita-cetovimutti.json`
- `muducitta` (`muducitta`; minor) ? `terms/minor/muducitta.json`
- `muncitukamyata-nana` (`muncitukamyata-nana`; minor) ? `terms/minor/muncitukamyata-nana.json`
- `musavada-veramani` (`musavada-veramani`; minor) ? `terms/minor/musavada-veramani.json`
- `mutta` (`mutta`; minor) ? `terms/minor/mutta.json`
- `naccagītavādita` (`nacca-gita-vadita`; minor) ? `terms/minor/nacca-gita-vadita.json`
- `naga` (`naga`; minor) ? `terms/minor/naga.json`
- `nakha` (`nakha`; minor) ? `terms/minor/nakha.json`
- `nāma` (`nama`; minor) ? `terms/minor/nama.json`
- `Nandaka` (`nandaka`; minor) ? `terms/minor/nandaka.json`
- `ñātaka` (`nataka`; minor) ? `terms/minor/nataka.json`
- `natthi-paccaya` (`natthi-paccaya`; minor) ? `terms/minor/natthi-paccaya.json`
- `natthi` (`natthi`; minor) ? `terms/minor/natthi.json`
- `navaka` (`navaka`; minor) ? `terms/minor/navaka.json`
- `naya` (`naya`; minor) ? `terms/minor/naya.json`
- `nekkhamma-dhātu` (`nekkhamma-dhatu`; minor) ? `terms/minor/nekkhamma-dhatu.json`
- `neyya` (`neyya`; minor) ? `terms/minor/neyya.json`
- `nharu` (`nharu`; minor) ? `terms/minor/nharu.json`
- `nigama` (`nigama`; minor) ? `terms/minor/nigama.json`
- `nirāmisa-pīti` (`niramisa-piti`; minor) ? `terms/minor/niramisa-piti.json`
- `nirāmisa-sukha` (`niramisa-sukha`; minor) ? `terms/minor/niramisa-sukha.json`
- `niraya-loka` (`niraya-loka`; minor) ? `terms/minor/niraya-loka.json`
- `niraya` (`niraya`; minor) ? `terms/minor/niraya.json`
- `nirodhasamāpatti` (`nirodha-samapatti`; minor) ? `terms/minor/nirodha-samapatti.json`
- `nirodha-sanna` (`nirodha-sanna`; minor) ? `terms/minor/nirodha-sanna.json`
- `nirodhanissita` (`nirodhanissita`; minor) ? `terms/minor/nirodhanissita.json`
- `okāsa` (`okasa`; minor) ? `terms/minor/okasa.json`
- `ottappa-dhana` (`ottappa-dhana`; minor) ? `terms/minor/ottappa-dhana.json`
- `ovāda` (`ovada`; minor) ? `terms/minor/ovada.json`
- `pabbajita` (`pabbajita`; minor) ? `terms/minor/pabbajita.json`
- `pabbajjākamma` (`pabbajja-kamma`; minor) ? `terms/minor/pabbajja-kamma.json`
- `pacchajata-paccaya` (`pacchajata-paccaya`; minor) ? `terms/minor/pacchajata-paccaya.json`
- `pacchajata` (`pacchajata`; minor) ? `terms/minor/pacchajata.json`
- `padaparama` (`padaparama`; minor) ? `terms/minor/padaparama.json`
- `padhāna` (`padhana`; minor) ? `terms/minor/padhana.json`
- `pamāda` (`pamada`; minor) ? `terms/minor/pamada.json`
- `panatipata-veramani` (`panatipata-veramani`; minor) ? `terms/minor/panatipata-veramani.json`
- `panca-bala` (`panca-bala`; minor) ? `terms/minor/panca-bala.json`
- `panca-indriya` (`panca-indriya`; minor) ? `terms/minor/panca-indriya.json`
- `paṇḍita` (`pandita`; minor) ? `terms/minor/pandita.json`
- `panna-dhana` (`panna-dhana`; minor) ? `terms/minor/panna-dhana.json`
- `paññābala` (`pannabala`; minor) ? `terms/minor/pannabala.json`
- `paññindriya` (`pannindriya`; minor) ? `terms/minor/pannindriya.json`
- `papa-kamma` (`papa-kamma`; minor) ? `terms/minor/papa-kamma.json`
- `papaka-mitta` (`papaka-mitta`; minor) ? `terms/minor/papaka-mitta.json`
- `pāpamittatā` (`papamittata`; minor) ? `terms/minor/papamittata.json`
- `papphasa` (`papphasa`; minor) ? `terms/minor/papphasa.json`
- `paribbajaka` (`paribbajaka`; minor) ? `terms/minor/paribbajaka.json`
- `paribbajika` (`paribbajika`; minor) ? `terms/minor/paribbajika.json`
- `parikamma-nimitta` (`parikamma-nimitta`; minor) ? `terms/minor/parikamma-nimitta.json`
- `parikamma-samadhi` (`parikamma-samadhi`; minor) ? `terms/minor/parikamma-samadhi.json`
- `parikkhāra` (`parikkhara`; minor) ? `terms/minor/parikkhara.json`
- `parisā` (`parisa`; minor) ? `terms/minor/parisa.json`
- `parivāsa` (`parivasa`; minor) ? `terms/minor/parivasa.json`
- `pariyatti` (`pariyatti`; minor) ? `terms/minor/pariyatti.json`
- `pariyāya` (`pariyaya`; minor) ? `terms/minor/pariyaya.json`
- `pasannacitta` (`pasannacitta`; minor) ? `terms/minor/pasannacitta.json`
- `Pasenadi` (`pasenadi`; minor) ? `terms/minor/pasenadi.json`
- `passaddhisambojjhaṅga` (`passaddhi-sambojjhanga`; minor) ? `terms/minor/passaddhi-sambojjhanga.json`
- `Paṭācārā` (`patacara`; minor) ? `terms/minor/patacara.json`
- `pathavi-dhatu` (`pathavi-dhatu`; minor) ? `terms/minor/pathavi-dhatu.json`
- `pathavi` (`pathavi`; minor) ? `terms/minor/pathavi.json`
- `patibhaga-nimitta` (`patibhaga-nimitta`; minor) ? `terms/minor/patibhaga-nimitta.json`
- `paṭinissagga` (`patinissagga`; minor) ? `terms/minor/patinissagga.json`
- `patipassaddhi` (`patipassaddhi`; minor) ? `terms/minor/patipassaddhi.json`
- `paṭipatti` (`patipatti`; minor) ? `terms/minor/patipatti.json`
- `patisallana` (`patisallana`; minor) ? `terms/minor/patisallana.json`
- `patisankha-nana` (`patisankha-nana`; minor) ? `terms/minor/patisankha-nana.json`
- `patisankha-yoniso` (`patisankha-yoniso`; minor) ? `terms/minor/patisankha-yoniso.json`
- `paṭivedha` (`pativedha`; minor) ? `terms/minor/pativedha.json`
- `patta` (`patta`; minor) ? `terms/minor/patta.json`
- `pavāraṇā` (`pavarana`; minor) ? `terms/minor/pavarana.json`
- `peta` (`peta`; minor) ? `terms/minor/peta.json`
- `petaloka` (`petaloka`; minor) ? `terms/minor/petaloka.json`
- `pettivisaya` (`pettivisaya`; minor) ? `terms/minor/pettivisaya.json`
- `phala-nana` (`phala-nana`; minor) ? `terms/minor/phala-nana.json`
- `phalasamāpatti` (`phalasamapatti`; minor) ? `terms/minor/phalasamapatti.json`
- `pharusa-vaca` (`pharusa-vaca`; minor) ? `terms/minor/pharusa-vaca.json`
- `phassa-dhātu` (`phassa-dhatu`; minor) ? `terms/minor/phassa-dhatu.json`
- `phassāyatana` (`phassayatana`; minor) ? `terms/minor/phassayatana.json`
- `photthabba-tanha` (`photthabba-tanha`; minor) ? `terms/minor/photthabba-tanha.json`
- `pihaka` (`pihaka`; minor) ? `terms/minor/pihaka.json`
- `piṇḍapāta` (`pindapata`; minor) ? `terms/minor/pindapata.json`
- `pisāca` (`pisaca`; minor) ? `terms/minor/pisaca.json`
- `pisuna-vaca` (`pisuna-vaca`; minor) ? `terms/minor/pisuna-vaca.json`
- `pitā` (`pita`; minor) ? `terms/minor/pita.json`
- `pītisambojjhaṅga` (`piti-sambojjhanga`; minor) ? `terms/minor/piti-sambojjhanga.json`
- `pitta` (`pitta`; minor) ? `terms/minor/pitta.json`
- `Pokkharasāti` (`pokkharasati`; minor) ? `terms/minor/pokkharasati.json`
- `pubba` (`pubba`; minor) ? `terms/minor/pubba.json`
- `puggala` (`puggala`; minor) ? `terms/minor/puggala.json`
- `puluvaka` (`puluvaka`; minor) ? `terms/minor/puluvaka.json`
- `punna-kamma` (`punna-kamma`; minor) ? `terms/minor/punna-kamma.json`
- `puññābhisaṅkhāra` (`punnabhisankhara`; minor) ? `terms/minor/punnabhisankhara.json`
- `purejata-paccaya` (`purejata-paccaya`; minor) ? `terms/minor/purejata-paccaya.json`
- `purejata` (`purejata`; minor) ? `terms/minor/purejata.json`
- `purisa` (`purisa`; minor) ? `terms/minor/purisa.json`
- `purisabhāva` (`purisabhava`; minor) ? `terms/minor/purisabhava.json`
- `putta` (`putta`; minor) ? `terms/minor/putta.json`
- `Rāhula` (`rahula`; minor) ? `terms/minor/rahula.json`
- `rajja` (`rajja`; minor) ? `terms/minor/rajja.json`
- `rasa-tanha` (`rasa-tanha`; minor) ? `terms/minor/rasa-tanha.json`
- `rukkhamūla` (`rukkhamula`; minor) ? `terms/minor/rukkhamula.json`
- `rūpa-dhātu` (`rupa-dhatu`; minor) ? `terms/minor/rupa-dhatu.json`
- `rupa-tanha` (`rupa-tanha`; minor) ? `terms/minor/rupa-tanha.json`
- `sabbaloke-anabhirata-sanna` (`sabbaloke-anabhirata-sanna`; minor) ? `terms/minor/sabbaloke-anabhirata-sanna.json`
- `sabhā` (`sabha`; minor) ? `terms/minor/sabha.json`
- `sadda-tanha` (`sadda-tanha`; minor) ? `terms/minor/sadda-tanha.json`
- `saddha-dhana` (`saddha-dhana`; minor) ? `terms/minor/saddha-dhana.json`
- `saddhābala` (`saddhabala`; minor) ? `terms/minor/saddhabala.json`
- `saddhindriya` (`saddhindriya`; minor) ? `terms/minor/saddhindriya.json`
- `sahajata-paccaya` (`sahajata-paccaya`; minor) ? `terms/minor/sahajata-paccaya.json`
- `sahajata` (`sahajata`; minor) ? `terms/minor/sahajata.json`
- `sahetuka` (`sahetuka`; minor) ? `terms/minor/sahetuka.json`
- `sakadagami-magga` (`sakadagami-magga`; minor) ? `terms/minor/sakadagami-magga.json`
- `sakadāgāmiphala` (`sakadagami-phala`; minor) ? `terms/minor/sakadagami-phala.json`
- `samādhisambojjhaṅga` (`samadhi-sambojjhanga`; minor) ? `terms/minor/samadhi-sambojjhanga.json`
- `samādhibala` (`samadhibala`; minor) ? `terms/minor/samadhibala.json`
- `samādhindriya` (`samadhindriya`; minor) ? `terms/minor/samadhindriya.json`
- `samagga` (`samagga`; minor) ? `terms/minor/samagga.json`
- `samāja` (`samaja`; minor) ? `terms/minor/samaja.json`
- `samaṇa` (`samana`; minor) ? `terms/minor/samana.json`
- `samanantara-paccaya` (`samanantara-paccaya`; minor) ? `terms/minor/samanantara-paccaya.json`
- `samanantara` (`samanantara`; minor) ? `terms/minor/samanantara.json`
- `sāmaṇera` (`samanera`; minor) ? `terms/minor/samanera.json`
- `sāmaṇerī` (`samaneri`; minor) ? `terms/minor/samaneri.json`
- `samatha-nimitta` (`samatha-nimitta`; minor) ? `terms/minor/samatha-nimitta.json`
- `samatha-vipassana` (`samatha-vipassana`; minor) ? `terms/minor/samatha-vipassana.json`
- `samathayata` (`samathayata`; minor) ? `terms/minor/samathayata.json`
- `sammappadhāna` (`sammapadhana`; minor) ? `terms/minor/sammapadhana.json`
- `sammasana-nana` (`sammasana-nana`; minor) ? `terms/minor/sammasana-nana.json`
- `sampajāno` (`sampajano`; minor) ? `terms/minor/sampajano.json`
- `sampasadana` (`sampasadana`; minor) ? `terms/minor/sampasadana.json`
- `sampayutta-paccaya` (`sampayutta-paccaya`; minor) ? `terms/minor/sampayutta-paccaya.json`
- `sampayutta` (`sampayutta`; minor) ? `terms/minor/sampayutta.json`
- `samphappalapa` (`samphappalapa`; minor) ? `terms/minor/samphappalapa.json`
- `samphassaja` (`samphassaja`; minor) ? `terms/minor/samphassaja.json`
- `samuccheda` (`samuccheda`; minor) ? `terms/minor/samuccheda.json`
- `saṅghakamma` (`sanghakamma`; minor) ? `terms/minor/sanghakamma.json`
- `sankappa` (`sankappa`; minor) ? `terms/minor/sankappa.json`
- `sankharupekkha-nana` (`sankharupekkha-nana`; minor) ? `terms/minor/sankharupekkha-nana.json`
- `saññā-dhātu` (`sanna-dhatu`; minor) ? `terms/minor/sanna-dhatu.json`
- `santosa` (`santosa`; minor) ? `terms/minor/santosa.json`
- `sappurisadhamma` (`sappurisa-dhamma`; minor) ? `terms/minor/sappurisa-dhamma.json`
- `sappurisa` (`sappurisa`; minor) ? `terms/minor/sappurisa.json`
- `sārambha` (`sarambha`; minor) ? `terms/minor/sarambha.json`
- `Sāriputta` (`sariputta`; minor) ? `terms/minor/sariputta.json`
- `satisambojjhaṅga` (`sati-sambojjhanga`; minor) ? `terms/minor/sati-sambojjhanga.json`
- `sati-sampajañña` (`sati-sampajanna`; minor) ? `terms/minor/sati-sampajanna.json`
- `satibala` (`satibala`; minor) ? `terms/minor/satibala.json`
- `satimā-sampajāno` (`satima-sampajano`; minor) ? `terms/minor/satima-sampajano.json`
- `satimā` (`satima`; minor) ? `terms/minor/satima.json`
- `satindriya` (`satindriya`; minor) ? `terms/minor/satindriya.json`
- `satta-bojjhanga` (`satta-bojjhanga`; minor) ? `terms/minor/satta-bojjhanga.json`
- `satta` (`satta`; minor) ? `terms/minor/satta.json`
- `semha` (`semha`; minor) ? `terms/minor/semha.json`
- `senāpati` (`senapati`; minor) ? `terms/minor/senapati.json`
- `senāsana` (`senasana`; minor) ? `terms/minor/senasana.json`
- `senāsanapaccaya` (`senasanapaccaya`; minor) ? `terms/minor/senasanapaccaya.json`
- `sila-dhana` (`sila-dhana`; minor) ? `terms/minor/sila-dhana.json`
- `singhanika` (`singhanika`; minor) ? `terms/minor/singhanika.json`
- `somanassa` (`somanassa`; minor) ? `terms/minor/somanassa.json`
- `Soṇa` (`sona`; minor) ? `terms/minor/sona.json`
- `sota-dvara` (`sota-dvara`; minor) ? `terms/minor/sota-dvara.json`
- `sotāpannaphala` (`sotapannaphala`; minor) ? `terms/minor/sotapannaphala.json`
- `sotapatti-magga` (`sotapatti-magga`; minor) ? `terms/minor/sotapatti-magga.json`
- `Subhūti` (`subhuti`; minor) ? `terms/minor/subhuti.json`
- `sucarita` (`sucarita`; minor) ? `terms/minor/sucarita.json`
- `sugati` (`sugati`; minor) ? `terms/minor/sugati.json`
- `sukhavedanā` (`sukha-vedana`; minor) ? `terms/minor/sukha-vedana.json`
- `sunnata-cetosamadhi` (`sunnata-cetosamadhi`; minor) ? `terms/minor/sunnata-cetosamadhi.json`
- `sunnata-samadhi` (`sunnata-samadhi`; minor) ? `terms/minor/sunnata-samadhi.json`
- `sunnata-vimokkha` (`sunnata-vimokkha`; minor) ? `terms/minor/sunnata-vimokkha.json`
- `surameraya-majjapamadatthana-veramani` (`surameraya-majjapamadatthana-veramani`; minor) ? `terms/minor/surameraya-majjapamadatthana-veramani.json`
- `suta-dhana` (`suta-dhana`; minor) ? `terms/minor/suta-dhana.json`
- `taco` (`taco`; minor) ? `terms/minor/taco.json`
- `tadaṅga-vimutti` (`tadanga-vimutti`; minor) ? `terms/minor/tadanga-vimutti.json`
- `tadanga` (`tadanga`; minor) ? `terms/minor/tadanga.json`
- `tejo-dhatu` (`tejo-dhatu`; minor) ? `terms/minor/tejo-dhatu.json`
- `tejo` (`tejo`; minor) ? `terms/minor/tejo.json`
- `thambha` (`thambha`; minor) ? `terms/minor/thambha.json`
- `thera` (`thera`; minor) ? `terms/minor/thera.json`
- `therī` (`theri`; minor) ? `terms/minor/theri.json`
- `ticīvara` (`ticivara`; minor) ? `terms/minor/ticivara.json`
- `tiracchāna-yoni` (`tiracchana-yoni`; minor) ? `terms/minor/tiracchana-yoni.json`
- `tiracchana` (`tiracchana`; minor) ? `terms/minor/tiracchana.json`
- `titthiya` (`titthiya`; minor) ? `terms/minor/titthiya.json`
- `ubhatobhāga-vimutti` (`ubhatobhaga-vimutti`; minor) ? `terms/minor/ubhatobhaga-vimutti.json`
- `uccāsayanamahāsayana` (`uccasayana-mahasayana`; minor) ? `terms/minor/uccasayana-mahasayana.json`
- `udariya` (`udariya`; minor) ? `terms/minor/udariya.json`
- `udayabbaya-nana` (`udayabbaya-nana`; minor) ? `terms/minor/udayabbaya-nana.json`
- `uddhumataka` (`uddhumataka`; minor) ? `terms/minor/uddhumataka.json`
- `uggaha-nimitta` (`uggaha-nimitta`; minor) ? `terms/minor/uggaha-nimitta.json`
- `ugghaṭitaññū` (`ugghatitannu`; minor) ? `terms/minor/ugghatitannu.json`
- `upacara-samadhi` (`upacara-samadhi`; minor) ? `terms/minor/upacara-samadhi.json`
- `upadhi-viveka` (`upadhi-viveka`; minor) ? `terms/minor/upadhi-viveka.json`
- `upajjhaya` (`upajjhaya`; minor) ? `terms/minor/upajjhaya.json`
- `upakkilesehi-upakkilittha` (`upakkilesehi-upakkilittha`; minor) ? `terms/minor/upakkilesehi-upakkilittha.json`
- `upanāha` (`upanaha`; minor) ? `terms/minor/upanaha.json`
- `upanissaya-paccaya` (`upanissaya-paccaya`; minor) ? `terms/minor/upanissaya-paccaya.json`
- `upanissaya` (`upanissaya`; minor) ? `terms/minor/upanissaya.json`
- `upasaka-sangha` (`upasaka-sangha`; minor) ? `terms/minor/upasaka-sangha.json`
- `upāsaka` (`upasaka`; minor) ? `terms/minor/upasaka.json`
- `upasampadākamma` (`upasampada-kamma`; minor) ? `terms/minor/upasampada-kamma.json`
- `upasika-sangha` (`upasika-sangha`; minor) ? `terms/minor/upasika-sangha.json`
- `upāsikā` (`upasika`; minor) ? `terms/minor/upasika.json`
- `upaṭṭhāka` (`upatthaka`; minor) ? `terms/minor/upatthaka.json`
- `upekkhācetovimutti` (`upekkha-cetovimutti`; minor) ? `terms/minor/upekkha-cetovimutti.json`
- `upekkhāsambojjhaṅga` (`upekkha-sambojjhanga`; minor) ? `terms/minor/upekkha-sambojjhanga.json`
- `upekkhā-sati-pārisuddhi` (`upekkha-sati-parisuddhi`; minor) ? `terms/minor/upekkha-sati-parisuddhi.json`
- `Uppalavaṇṇā` (`uppalavanna`; minor) ? `terms/minor/uppalavanna.json`
- `vaca` (`vaca`; minor) ? `terms/minor/vaca.json`
- `Vacchagotta` (`vacchagotta`; minor) ? `terms/minor/vacchagotta.json`
- `vaci-kamma` (`vaci-kamma`; minor) ? `terms/minor/vaci-kamma.json`
- `vacīsaṅkhāra` (`vaci-sankhara`; minor) ? `terms/minor/vaci-sankhara.json`
- `vakka` (`vakka`; minor) ? `terms/minor/vakka.json`
- `Vakkali` (`vakkali`; minor) ? `terms/minor/vakkali.json`
- `vasa` (`vasa`; minor) ? `terms/minor/vasa.json`
- `vassāvāsa` (`vassavasa`; minor) ? `terms/minor/vassavasa.json`
- `vayama` (`vayama`; minor) ? `terms/minor/vayama.json`
- `vayo-dhatu` (`vayo-dhatu`; minor) ? `terms/minor/vayo-dhatu.json`
- `vayo` (`vayo`; minor) ? `terms/minor/vayo.json`
- `vedanā-dhātu` (`vedana-dhatu`; minor) ? `terms/minor/vedana-dhatu.json`
- `vera` (`vera`; minor) ? `terms/minor/vera.json`
- `vicchiddaka` (`vicchiddaka`; minor) ? `terms/minor/vicchiddaka.json`
- `vigata-paccaya` (`vigata-paccaya`; minor) ? `terms/minor/vigata-paccaya.json`
- `vigata` (`vigata`; minor) ? `terms/minor/vigata.json`
- `vihāra` (`vihara`; minor) ? `terms/minor/vihara.json`
- `vikālabhojana` (`vikala-bhojana`; minor) ? `terms/minor/vikala-bhojana.json`
- `vikkhambhana` (`vikkhambhana`; minor) ? `terms/minor/vikkhambhana.json`
- `vikkhayitaka` (`vikkhayitaka`; minor) ? `terms/minor/vikkhayitaka.json`
- `vikkhittaka` (`vikkhittaka`; minor) ? `terms/minor/vikkhittaka.json`
- `vīmaṃsiddhipāda` (`vimamsa-iddhipada`; minor) ? `terms/minor/vimamsa-iddhipada.json`
- `vimokkhamukha` (`vimokkhamukha`; minor) ? `terms/minor/vimokkhamukha.json`
- `vinilaka` (`vinilaka`; minor) ? `terms/minor/vinilaka.json`
- `vinipāta` (`vinipata`; minor) ? `terms/minor/vinipata.json`
- `viññāṇadhātu` (`vinnana-dhatu`; minor) ? `terms/minor/vinnana-dhatu.json`
- `vipacitaññū` (`vipacitannu`; minor) ? `terms/minor/vipacitannu.json`
- `vipaka-paccaya` (`vipaka-paccaya`; minor) ? `terms/minor/vipaka-paccaya.json`
- `vipaka` (`vipaka`; minor) ? `terms/minor/vipaka.json`
- `vipassanayata` (`vipassanayata`; minor) ? `terms/minor/vipassanayata.json`
- `vipassi` (`vipassi`; minor) ? `terms/minor/vipassi.json`
- `vippayutta-paccaya` (`vippayutta-paccaya`; minor) ? `terms/minor/vippayutta-paccaya.json`
- `vippayutta` (`vippayutta`; minor) ? `terms/minor/vippayutta.json`
- `vipubbaka` (`vipubbaka`; minor) ? `terms/minor/vipubbaka.json`
- `viraga-sanna` (`viraga-sanna`; minor) ? `terms/minor/viraga-sanna.json`
- `viraganissita` (`viraganissita`; minor) ? `terms/minor/viraganissita.json`
- `viriyiddhipāda` (`viriya-iddhipada`; minor) ? `terms/minor/viriya-iddhipada.json`
- `viriyasambojjhaṅga` (`viriya-sambojjhanga`; minor) ? `terms/minor/viriya-sambojjhanga.json`
- `viriyabala` (`viriyabala`; minor) ? `terms/minor/viriyabala.json`
- `viriyindriya` (`viriyaindriya`; minor) ? `terms/minor/viriyaindriya.json`
- `Visākhā` (`visakha`; minor) ? `terms/minor/visakha.json`
- `visaya` (`visaya`; minor) ? `terms/minor/visaya.json`
- `vivāda` (`vivada`; minor) ? `terms/minor/vivada.json`
- `vivekaja` (`vivekaja`; minor) ? `terms/minor/vivekaja.json`
- `vivekanissita` (`vivekanissita`; minor) ? `terms/minor/vivekanissita.json`
- `yāgu` (`yagu`; minor) ? `terms/minor/yagu.json`
- `yakana` (`yakana`; minor) ? `terms/minor/yakana.json`
- `yakkha` (`yakkha`; minor) ? `terms/minor/yakkha.json`
- `yoniso-patisankha` (`yoniso-patisankha`; minor) ? `terms/minor/yoniso-patisankha.json`
- `yoniso` (`yoniso`; minor) ? `terms/minor/yoniso.json`
- `yonisomanasikara` (`yonisomanasikara`; minor) ? `terms/minor/yonisomanasikara.json`

### Missing `context_rules` (106 term entries)

- `abyāpādavitakka` (`abyapada-vitakka`; minor) ? `terms/minor/abyapada-vitakka.json`
- `adhivāsanā` (`adhivasana`; minor) ? `terms/minor/adhivasana.json`
- `amatapada` (`amatapada`; minor) ? `terms/minor/amatapada.json`
- `anatta-sanna` (`anatta-sanna`; minor) ? `terms/minor/anatta-sanna.json`
- `anattānupassanā` (`anattanupassana`; minor) ? `terms/minor/anattanupassana.json`
- `anicca-sanna` (`anicca-sanna`; minor) ? `terms/minor/anicca-sanna.json`
- `aniccānupassanā` (`aniccanupassana`; minor) ? `terms/minor/aniccanupassana.json`
- `anupādisesa-nibbāna-dhātu` (`anupadisesa-nibbana-dhatu`; minor) ? `terms/minor/anupadisesa-nibbana-dhatu.json`
- `ariya-atthangika-magga` (`ariya-atthangika-magga`; minor) ? `terms/minor/ariya-atthangika-magga.json`
- `asaṅkhata-dhātu` (`asankhata-dhatu`; minor) ? `terms/minor/asankhata-dhatu.json`
- `āsavānaṃ khayā` (`asavanam-khaya`; minor) ? `terms/minor/asavanam-khaya.json`
- `atammayatā` (`atammayata`; minor) ? `terms/minor/atammayata.json`
- `avihiṁsāvitakka` (`avihimsa-vitakka`; minor) ? `terms/minor/avihimsa-vitakka.json`
- `bhavā jāti bhūtassa jarāmaraṇaṁ` (`bhava-jati-bhutassa-jaramaranam`; minor) ? `terms/minor/bhava-jati-bhutassa-jaramaranam.json`
- `byāpādavitakka` (`byapada-vitakka`; minor) ? `terms/minor/byapada-vitakka.json`
- `cakkhāyatana` (`cakkhayatana`; minor) ? `terms/minor/cakkhayatana.json`
- `cakkhusamphassa` (`cakkhu-samphassa`; minor) ? `terms/minor/cakkhu-samphassa.json`
- `cattāro satipaṭṭhānā` (`cattaro-satipatthana`; minor) ? `terms/minor/cattaro-satipatthana.json`
- `catuttha-jhāna` (`catuttha-jhana`; minor) ? `terms/minor/catuttha-jhana.json`
- `chandarāga` (`chandaraga`; minor) ? `terms/minor/chandaraga.json`
- `cittānupassanā` (`cittanupassana`; minor) ? `terms/minor/cittanupassana.json`
- `dhammānupassanā` (`dhammanupassana`; minor) ? `terms/minor/dhammanupassana.json`
- `dhammāyatana` (`dhammayatana`; minor) ? `terms/minor/dhammayatana.json`
- `dukkha-ariyasacca` (`dukkha-ariyasacca`; minor) ? `terms/minor/dukkha-ariyasacca.json`
- `dukkha-sanna` (`dukkha-sanna`; minor) ? `terms/minor/dukkha-sanna.json`
- `dukkhānupassanā` (`dukkhanupassana`; minor) ? `terms/minor/dukkhanupassana.json`
- `dutiya-jhāna` (`dutiya-jhana`; minor) ? `terms/minor/dutiya-jhana.json`
- `etaṁ mama, esohamasmi, eso me attā` (`etam-mama-esohamasmi-eso-me-atta`; minor) ? `terms/minor/etam-mama-esohamasmi-eso-me-atta.json`
- `gandhāyatana` (`gandhayatana`; minor) ? `terms/minor/gandhayatana.json`
- `gehasita domanassa` (`gehasita-domanassa`; minor) ? `terms/minor/gehasita-domanassa.json`
- `gehasita somanassa` (`gehasita-somanassa`; minor) ? `terms/minor/gehasita-somanassa.json`
- `gehasita upekkhā` (`gehasita-upekkha`; minor) ? `terms/minor/gehasita-upekkha.json`
- `ghānasamphassa` (`ghana-samphassa`; minor) ? `terms/minor/ghana-samphassa.json`
- `ghānāyatana` (`ghanayatana`; minor) ? `terms/minor/ghanayatana.json`
- `jivhāsamphassa` (`jivha-samphassa`; minor) ? `terms/minor/jivha-samphassa.json`
- `jivhāyatana` (`jivhayatana`; minor) ? `terms/minor/jivhayatana.json`
- `kāmavitakka` (`kama-vitakka`; minor) ? `terms/minor/kama-vitakka.json`
- `kāmesu-micchācāra` (`kamesu-micchacara`; minor) ? `terms/minor/kamesu-micchacara.json`
- `kāyasamphassa` (`kaya-samphassa`; minor) ? `terms/minor/kaya-samphassa.json`
- `kāyānupassanā` (`kayanupassana`; minor) ? `terms/minor/kayanupassana.json`
- `kāyāyatana` (`kayayatana`; minor) ? `terms/minor/kayayatana.json`
- `khaye-ñāṇa` (`khaye-nana`; minor) ? `terms/minor/khaye-nana.json`
- `magga-ariyasacca` (`magga-ariyasacca`; minor) ? `terms/minor/magga-ariyasacca.json`
- `manāyatana` (`manayatana`; minor) ? `terms/minor/manayatana.json`
- `manosamphassa` (`mano-samphassa`; minor) ? `terms/minor/mano-samphassa.json`
- `manopavicara` (`manopavicara`; minor) ? `terms/minor/manopavicara.json`
- `ekāyano ayaṁ, bhikkhave, maggo sattānaṁ visuddhiyā` (`mn10-direct-path-opening`; minor) ? `terms/minor/mn10-direct-path-opening.json`
- `ajjhattaṁ vā kāye kāyānupassī viharati, bahiddhā vā kāye kāyānupassī viharati, ajjhattabahiddhā vā kāye kāyānupassī viharati` (`mn10-kayanupassi-internal-external`; minor) ? `terms/minor/mn10-kayanupassi-internal-external.json`
- `'atthi kāyo'ti vā panassa sati paccupaṭṭhitā hoti ... anissito ca viharati, na ca kiñci loke upādiyati` (`mn10-kayo-anchor-nonappropriation`; minor) ? `terms/minor/mn10-kayo-anchor-nonappropriation.json`
- `ātāpī sampajāno satimā, vineyya loke abhijjhādomanassaṁ` (`mn10-satipatthana-qualifier`; minor) ? `terms/minor/mn10-satipatthana-qualifier.json`
- `passambhayaṁ kāyasaṅkhāraṁ assasissāmīti sikkhati, passambhayaṁ kāyasaṅkhāraṁ passasissāmīti sikkhati` (`mn118-body-conditioner-training`; minor) ? `terms/minor/mn118-body-conditioner-training.json`
- `so satova assasati satova passasati` (`mn118-breathing-remembrance-line`; minor) ? `terms/minor/mn118-breathing-remembrance-line.json`
- `sabbakāyapaṭisaṁvedī assasissāmīti sikkhati, sabbakāyapaṭisaṁvedī passasissāmīti sikkhati` (`mn118-whole-body-training`; minor) ? `terms/minor/mn118-whole-body-training.json`
- `tatra idaṁ nissāya idaṁ pajahatha` (`mn137-supported-by-this-give-up-that`; minor) ? `terms/minor/mn137-supported-by-this-give-up-that.json`
- `tayo satipaṭṭhānā` (`mn137-three-establishments-of-sati`; minor) ? `terms/minor/mn137-three-establishments-of-sati.json`
- `catunnaṁ ariyasaccānaṁ ācikkhanā desanā paññāpanā paṭṭhapanā vivaraṇā vibhajanā uttānīkammaṁ` (`mn141-four-truths-analysis-opening`; minor) ? `terms/minor/mn141-four-truths-analysis-opening.json`
- `yo tassāyeva taṇhāya asesavirāganirodho cāgo paṭinissaggo mutti anālayo` (`mn141-tanha-release-tail`; minor) ? `terms/minor/mn141-tanha-release-tail.json`
- `adukkhamasukhāya vedanāya phuṭṭho samāno tassā vedanāya samudayañca atthaṅgamañca assādañca ādīnavañca nissaraṇañca yathābhūtaṁ na pajānāti` (`mn148-mixed-feeling-undiscerned-response`; minor) ? `terms/minor/mn148-mixed-feeling-undiscerned-response.json`
- `dukkhāya vedanāya phuṭṭho samāno na socati na kilamati na paridevati na uraṁtadati na sammohaṁ āpajjati` (`mn148-painful-feeling-trained-response`; minor) ? `terms/minor/mn148-painful-feeling-trained-response.json`
- `dukkhāya vedanāya phuṭṭho samāno socati kilamati paridevati uraṁtadati sammohaṁ āpajjati` (`mn148-painful-feeling-untrained-response`; minor) ? `terms/minor/mn148-painful-feeling-untrained-response.json`
- `sukhāya vedanāya phuṭṭho samāno na abhinandati na abhivadati na ajjhosāya tiṭṭhati` (`mn148-pleasant-feeling-trained-response`; minor) ? `terms/minor/mn148-pleasant-feeling-trained-response.json`
- `ñāṇadassana` (`nanadassana`; minor) ? `terms/minor/nanadassana.json`
- `nandī dukkhassa mūlan` (`nandi-dukkhassa-mulan`; minor) ? `terms/minor/nandi-dukkhassa-mulan.json`
- `nandirāgasahagatā` (`nandiraga-sahagata`; minor) ? `terms/minor/nandiraga-sahagata.json`
- `nāparaṃ itthattāyāti pajānāti` (`naparam-itthattayati-pajanati`; minor) ? `terms/minor/naparam-itthattayati-pajanati.json`
- `nekkhammavitakka` (`nekkhamma-vitakka`; minor) ? `terms/minor/nekkhamma-vitakka.json`
- `nekkhammasita domanassa` (`nekkhammasita-domanassa`; minor) ? `terms/minor/nekkhammasita-domanassa.json`
- `nekkhammasita somanassa` (`nekkhammasita-somanassa`; minor) ? `terms/minor/nekkhammasita-somanassa.json`
- `nekkhammasita upekkhā` (`nekkhammasita-upekkha`; minor) ? `terms/minor/nekkhammasita-upekkha.json`
- `netaṁ mama, nesohamasmi, na me so attā` (`netam-mama-nesohamasmi-na-me-so-atta`; minor) ? `terms/minor/netam-mama-nesohamasmi-na-me-so-atta.json`
- `nibbāna-dhātu` (`nibbana-dhatu`; minor) ? `terms/minor/nibbana-dhatu.json`
- `nirodha-ariyasacca` (`nirodha-ariyasacca`; minor) ? `terms/minor/nirodha-ariyasacca.json`
- `pañca-nīvaraṇā` (`panca-nivarana`; minor) ? `terms/minor/panca-nivarana.json`
- `parinibbāna-dhātu` (`parinibbana-dhatu`; minor) ? `terms/minor/parinibbana-dhatu.json`
- `parivajjanā` (`parivajjana`; minor) ? `terms/minor/parivajjana.json`
- `paṭhama-jhāna` (`pathama-jhana`; minor) ? `terms/minor/pathama-jhana.json`
- `paṭhaviṃ paṭhavito abhiññāya paṭhaviṃ mā maññi` (`pathavim-pathavito-abhinnaya-pathavim-ma-manni`; minor) ? `terms/minor/pathavim-pathavito-abhinnaya-pathavim-ma-manni.json`
- `paṭhaviṃ paṭhavito abhiññāya paṭhaviṃ na maññati` (`pathavim-pathavito-abhinnaya-pathavim-na-mannati`; minor) ? `terms/minor/pathavim-pathavito-abhinnaya-pathavim-na-mannati.json`
- `paṭhaviṃ paṭhavito saññatvā paṭhaviṃ maññati` (`pathavim-pathavito-sannatva-pathavim-mannati`; minor) ? `terms/minor/pathavim-pathavito-sannatva-pathavim-mannati.json`
- `paṭisevanā` (`patisevana`; minor) ? `terms/minor/patisevana.json`
- `phoṭṭhabbāyatana` (`photthabbatana`; minor) ? `terms/minor/photthabbatana.json`
- `rasāyatana` (`rasayatana`; minor) ? `terms/minor/rasayatana.json`
- `rūpāyatana` (`rupayatana`; minor) ? `terms/minor/rupayatana.json`
- `saddāyatana` (`saddayatana`; minor) ? `terms/minor/saddayatana.json`
- `samudaya-ariyasacca` (`samudaya-ariyasacca`; minor) ? `terms/minor/samudaya-ariyasacca.json`
- `sa-upādisesa-nibbāna-dhātu` (`saupadisesa-nibbana-dhatu`; minor) ? `terms/minor/saupadisesa-nibbana-dhatu.json`
- `savitakkaṁ savicāraṁ` (`savitakka-savicara`; minor) ? `terms/minor/savitakka-savicara.json`
- `sotasamphassa` (`sota-samphassa`; minor) ? `terms/minor/sota-samphassa.json`
- `sotāyatana` (`sotayatana`; minor) ? `terms/minor/sotayatana.json`
- `sukhāya vedanāya phuṭṭho samāno abhinandati abhivadati ajjhosāya tiṭṭhati` (`sukhaya-vedanaya-phuttho-samano-abhinandati-abhivadati-ajjhosaya-titthati`; minor) ? `terms/minor/sukhaya-vedanaya-phuttho-samano-abhinandati-abhivadati-ajjhosaya-titthati.json`
- `tatiya-jhāna` (`tatiya-jhana`; minor) ? `terms/minor/tatiya-jhana.json`
- `tatratatrābhinandinī` (`tatratatrabhinandini`; minor) ? `terms/minor/tatratatrabhinandini.json`
- `upasamānussati` (`upasamanussati`; minor) ? `terms/minor/upasamanussati.json`
- `vedanānupassanā` (`vedananupassana`; minor) ? `terms/minor/vedananupassana.json`
- `vedanāya samudayañca atthaṅgamañca assādañca ādīnavañca nissaraṇañca yathābhūtaṁ pajānāti` (`vedanaya-samudayanca-atthangamanca-assadanca-adinavanca-nissarananca-yathabhutam-pajanati`; minor) ? `terms/minor/vedanaya-samudayanca-atthangamanca-assadanca-adinavanca-nissarananca-yathabhutam-pajanati.json`
- `vihiṁsāvitakka` (`vihimsa-vitakka`; minor) ? `terms/minor/vihimsa-vitakka.json`
- `vimutti-ñāṇadassana` (`vimutti-nanadassana`; minor) ? `terms/minor/vimutti-nanadassana.json`
- `vinodanā` (`vinodana`; minor) ? `terms/minor/vinodana.json`
- `vivicceva kāmehi vivicca akusalehi dhammehi` (`vivicceva-kamehi-vivicca-akusalehi-dhammehi`; minor) ? `terms/minor/vivicceva-kamehi-vivicca-akusalehi-dhammehi.json`
- `vossaggapariṇāmi` (`vossaggaparinami`; minor) ? `terms/minor/vossaggaparinami.json`
- `yāyaṃ taṇhā ponobbhavikā` (`ya-tanha-ponobbhavika`; minor) ? `terms/minor/ya-tanha-ponobbhavika.json`
- `yaṁ papañceti tato nidānaṁ purisaṁ papañcasaññāsaṅkhā samudācaranti` (`yam-papanceti-tato-nidanam-purisam-papanca-sanna-sankha-samudacaranti`; minor) ? `terms/minor/yam-papanceti-tato-nidanam-purisam-papanca-sanna-sankha-samudacaranti.json`
- `yaṁ sañjānāti taṁ vitakketi` (`yam-sanjanati-tam-vitakketi`; minor) ? `terms/minor/yam-sanjanati-tam-vitakketi.json`
- `yaṁ vedeti taṁ sañjānāti` (`yam-vedeti-tam-sanjanati`; minor) ? `terms/minor/yam-vedeti-tam-sanjanati.json`
- `yaṁ vitakketi taṁ papañceti` (`yam-vitakketi-tam-papanceti`; minor) ? `terms/minor/yam-vitakketi-tam-papanceti.json`
- `yathābhūtaṃ pajānāti` (`yathabhutam-pajanati`; minor) ? `terms/minor/yathabhutam-pajanati.json`

### Missing `context_rules`, `example_phrases` (105 term entries)

- `adhiṭṭhāna` (`adhitthana`; minor) ? `terms/minor/adhitthana.json`
- `adinnādāna` (`adinnadana`; minor) ? `terms/minor/adinnadana.json`
- `ākāsa-kasiṇa` (`akasa-kasina`; minor) ? `terms/minor/akasa-kasina.json`
- `ākāsānañcāyatana` (`akasanancayatana`; minor) ? `terms/minor/akasanancayatana.json`
- `ākiñcaññāyatana` (`akincannayatana`; minor) ? `terms/minor/akincannayatana.json`
- `alābha` (`alabha`; minor) ? `terms/minor/alabha.json`
- `āloka-kasiṇa` (`aloka-kasina`; minor) ? `terms/minor/aloka-kasina.json`
- `anagāra` (`anagara`; minor) ? `terms/minor/anagara.json`
- `anumodanā` (`anumodana`; minor) ? `terms/minor/anumodana.json`
- `āpatti` (`apatti`; minor) ? `terms/minor/apatti.json`
- `āpo-kasiṇa` (`apo-kasina`; minor) ? `terms/minor/apo-kasina.json`
- `appicchatā` (`appicchata`; minor) ? `terms/minor/appicchata.json`
- `arhat` (`arhat`; minor) ? `terms/minor/arhat.json`
- `asaṃsagga` (`asamsagga`; minor) ? `terms/minor/asamsagga.json`
- `ayasa` (`ayasa`; minor) ? `terms/minor/ayasa.json`
- `bhante` (`bhante`; minor) ? `terms/minor/bhante.json`
- `bhikkhunī` (`bhikkhuni`; minor) ? `terms/minor/bhikkhuni.json`
- `bodhisattva` (`bodhisattva`; minor) ? `terms/minor/bodhisattva.json`
- `brahmacariya` (`brahmacariya`; minor) ? `terms/minor/brahmacariya.json`
- `cāga` (`caga`; minor) ? `terms/minor/caga.json`
- `cāgānussati` (`caganussati`; minor) ? `terms/minor/caganussati.json`
- `devadhītā` (`devadhita`; minor) ? `terms/minor/devadhita.json`
- `devatānussati` (`devatanussati`; minor) ? `terms/minor/devatanussati.json`
- `dhammavinaya` (`dhammavinaya`; minor) ? `terms/minor/dhammavinaya.json`
- `dharma` (`dharma`; minor) ? `terms/minor/dharma.json`
- `ehipassiko` (`ehipassiko`; minor) ? `terms/minor/ehipassiko.json`
- `hīnayāna` (`hinayana`; minor) ? `terms/minor/hinayana.json`
- `kalyāṇamitta` (`kalyanamitta`; minor) ? `terms/minor/kalyanamitta.json`
- `kaṭhina` (`kathina`; minor) ? `terms/minor/kathina.json`
- `kāyaduccarita` (`kayaduccarita`; minor) ? `terms/minor/kayaduccarita.json`
- `kāyasucarita` (`kayasucarita`; minor) ? `terms/minor/kayasucarita.json`
- `khanti` (`khanti`; minor) ? `terms/minor/khanti.json`
- `khattiya` (`khattiya`; minor) ? `terms/minor/khattiya.json`
- `lābha` (`labha`; minor) ? `terms/minor/labha.json`
- `lohita-kasiṇa` (`lohita-kasina`; minor) ? `terms/minor/lohita-kasina.json`
- `mahāyāna` (`mahayana`; minor) ? `terms/minor/mahayana.json`
- `maṇḍala` (`mandala`; minor) ? `terms/minor/mandala.json`
- `manoduccarita` (`manoduccarita`; minor) ? `terms/minor/manoduccarita.json`
- `manosucarita` (`manosucarita`; minor) ? `terms/minor/manosucarita.json`
- `mantra` (`mantra`; minor) ? `terms/minor/mantra.json`
- `māra` (`mara`; minor) ? `terms/minor/mara.json`
- `maraṇassati` (`maranassati`; minor) ? `terms/minor/maranassati.json`
- `mārga` (`marga`; minor) ? `terms/minor/marga.json`
- `micchā-ājīva` (`miccha-ajiva`; minor) ? `terms/minor/miccha-ajiva.json`
- `micchā-diṭṭhi` (`miccha-ditthi`; minor) ? `terms/minor/miccha-ditthi.json`
- `micchā-kammanta` (`miccha-kammanta`; minor) ? `terms/minor/miccha-kammanta.json`
- `micchā-ñāṇa` (`miccha-nana`; minor) ? `terms/minor/miccha-nana.json`
- `micchā-samādhi` (`miccha-samadhi`; minor) ? `terms/minor/miccha-samadhi.json`
- `micchāsaṅkappa` (`miccha-sankappa`; minor) ? `terms/minor/miccha-sankappa.json`
- `micchā-sati` (`miccha-sati`; minor) ? `terms/minor/miccha-sati.json`
- `micchā-vācā` (`miccha-vaca`; minor) ? `terms/minor/miccha-vaca.json`
- `micchā-vāyāma` (`miccha-vayama`; minor) ? `terms/minor/miccha-vayama.json`
- `micchā-vimutti` (`miccha-vimutti`; minor) ? `terms/minor/miccha-vimutti.json`
- `mudrā` (`mudra`; minor) ? `terms/minor/mudra.json`
- `musāvāda` (`musavada`; minor) ? `terms/minor/musavada.json`
- `nevasaññānāsaññāyatana` (`nevasannanasannayatana`; minor) ? `terms/minor/nevasannanasannayatana.json`
- `nīla-kasiṇa` (`nila-kasina`; minor) ? `terms/minor/nila-kasina.json`
- `nimitta` (`nimitta`; minor) ? `terms/minor/nimitta.json`
- `nindā` (`ninda`; minor) ? `terms/minor/ninda.json`
- `nissaya` (`nissaya`; minor) ? `terms/minor/nissaya.json`
- `odāta-kasiṇa` (`odata-kasina`; minor) ? `terms/minor/odata-kasina.json`
- `pabbajjā` (`pabbajja`; minor) ? `terms/minor/pabbajja.json`
- `paccavekkhaṇā` (`paccavekkhana`; minor) ? `terms/minor/paccavekkhana.json`
- `paṃsukūla` (`pamsukula`; minor) ? `terms/minor/pamsukula.json`
- `pāṇātipāta` (`panatipata`; minor) ? `terms/minor/panatipata.json`
- `pāpamitta` (`papamitta`; minor) ? `terms/minor/papamitta.json`
- `pāramitā` (`paramita`; minor) ? `terms/minor/paramita.json`
- `pārisuddhi` (`parisuddhi`; minor) ? `terms/minor/parisuddhi.json`
- `paritta` (`paritta`; minor) ? `terms/minor/paritta.json`
- `pasāda` (`pasada`; minor) ? `terms/minor/pasada.json`
- `pasaṃsā` (`pasamsa`; minor) ? `terms/minor/pasamsa.json`
- `pathavī-kasiṇa` (`pathavi-kasina`; minor) ? `terms/minor/pathavi-kasina.json`
- `paviveka` (`paviveka`; minor) ? `terms/minor/paviveka.json`
- `pīta-kasiṇa` (`pita-kasina`; minor) ? `terms/minor/pita-kasina.json`
- `prajñā` (`prajna`; minor) ? `terms/minor/prajna.json`
- `pūjā` (`puja`; minor) ? `terms/minor/puja.json`
- `sagga` (`sagga`; minor) ? `terms/minor/sagga.json`
- `sallekha` (`sallekha`; minor) ? `terms/minor/sallekha.json`
- `samatha` (`samatha`; minor) ? `terms/minor/samatha.json`
- `saṃskāra` (`samskara`; minor) ? `terms/minor/samskara.json`
- `saṃvega` (`samvega`; minor) ? `terms/minor/samvega.json`
- `saṅgha` (`sangha`; minor) ? `terms/minor/sangha.json`
- `santuṭṭhi` (`santutthi`; minor) ? `terms/minor/santutthi.json`
- `saraṇa` (`sarana`; minor) ? `terms/minor/sarana.json`
- `sikkhā` (`sikkha`; minor) ? `terms/minor/sikkha.json`
- `sīlānussati` (`silanussati`; minor) ? `terms/minor/silanussati.json`
- `srotāpanna` (`srotapanna`; minor) ? `terms/minor/srotapanna.json`
- `sudda` (`sudda`; minor) ? `terms/minor/sudda.json`
- `śūnyatā` (`sunyata`; minor) ? `terms/minor/sunyata.json`
- `surāmeraya-majjapamādaṭṭhāna` (`surameraya-majjapamadatthana`; minor) ? `terms/minor/surameraya-majjapamadatthana.json`
- `tejo-kasiṇa` (`tejo-kasina`; minor) ? `terms/minor/tejo-kasina.json`
- `upasampadā` (`upasampada`; minor) ? `terms/minor/upasampada.json`
- `upāya` (`upaya`; minor) ? `terms/minor/upaya.json`
- `uposathāgāra` (`uposathagara`; minor) ? `terms/minor/uposathagara.json`
- `vacīduccarita` (`vaciduccarita`; minor) ? `terms/minor/vaciduccarita.json`
- `vacīsucarita` (`vacisucarita`; minor) ? `terms/minor/vacisucarita.json`
- `vajrayāna` (`vajrayana`; minor) ? `terms/minor/vajrayana.json`
- `vandanā` (`vandana`; minor) ? `terms/minor/vandana.json`
- `vassa` (`vassa`; minor) ? `terms/minor/vassa.json`
- `vāyo-kasiṇa` (`vayo-kasina`; minor) ? `terms/minor/vayo-kasina.json`
- `vessa` (`vessa`; minor) ? `terms/minor/vessa.json`
- `vinaya` (`vinaya`; minor) ? `terms/minor/vinaya.json`
- `viññāṇañcāyatana` (`vinnananancayatana`; minor) ? `terms/minor/vinnananancayatana.json`
- `vipassanā` (`vipassana`; minor) ? `terms/minor/vipassana.json`
- `yasa` (`yasa`; minor) ? `terms/minor/yasa.json`

### Missing `discouraged_translations`, `context_rules` (78 term entries)

- `abhijjhā kāyagantha` (`abhijjha-kayagantha`; minor) ? `terms/minor/abhijjha-kayagantha.json`
- `ajjhatta-sampasadana` (`ajjhatta-sampasadana`; minor) ? `terms/minor/ajjhatta-sampasadana.json`
- `āsavakkhaya` (`asavakkhaya`; minor) ? `terms/minor/asavakkhaya.json`
- `asesavirāganirodha` (`asesa-viraga-nirodha`; minor) ? `terms/minor/asesa-viraga-nirodha.json`
- `avijjā-anusaya` (`avijja-anusaya`; minor) ? `terms/minor/avijja-anusaya.json`
- `avijja-nirodha` (`avijja-nirodha`; minor) ? `terms/minor/avijja-nirodha.json`
- `avijja-paccaya` (`avijja-paccaya`; minor) ? `terms/minor/avijja-paccaya.json`
- `avijjāsava` (`avijjasava`; minor) ? `terms/minor/avijjasava.json`
- `avijjāyoga` (`avijjayoga`; minor) ? `terms/minor/avijjayoga.json`
- `avijjogha` (`avijjogha`; minor) ? `terms/minor/avijjogha.json`
- `avitakka-avicara` (`avitakka-avicara`; minor) ? `terms/minor/avitakka-avicara.json`
- `bhava-nirodha` (`bhava-nirodha`; minor) ? `terms/minor/bhava-nirodha.json`
- `bhava-paccaya` (`bhava-paccaya`; minor) ? `terms/minor/bhava-paccaya.json`
- `bhavasamudaya` (`bhava-samudaya`; minor) ? `terms/minor/bhava-samudaya.json`
- `bhavarāga-anusaya` (`bhavaraga-anusaya`; minor) ? `terms/minor/bhavaraga-anusaya.json`
- `bhavāsava` (`bhavasava`; minor) ? `terms/minor/bhavasava.json`
- `bhavayoga` (`bhavayoga`; minor) ? `terms/minor/bhavayoga.json`
- `bhavogha` (`bhavogha`; minor) ? `terms/minor/bhavogha.json`
- `bojjhaṅgabhāvanā` (`bojjhanga-bhavana`; minor) ? `terms/minor/bojjhanga-bhavana.json`
- `byāpāda kāyagantha` (`byapada-kayagantha`; minor) ? `terms/minor/byapada-kayagantha.json`
- `cattārome, bhikkhave, ganthā` (`cattarome-bhikkhave-gantha`; minor) ? `terms/minor/cattarome-bhikkhave-gantha.json`
- `cattārome, bhikkhave, oghā` (`cattarome-bhikkhave-ogha`; minor) ? `terms/minor/cattarome-bhikkhave-ogha.json`
- `cattārome, bhikkhave, yogā` (`cattarome-bhikkhave-yoga`; minor) ? `terms/minor/cattarome-bhikkhave-yoga.json`
- `cetaso-ekodibhava` (`cetaso-ekodibhava`; minor) ? `terms/minor/cetaso-ekodibhava.json`
- `chandiddhipāda` (`chanda-iddhipada`; minor) ? `terms/minor/chanda-iddhipada.json`
- `diṭṭhadhammanibbāna` (`ditthadhammanibbana`; minor) ? `terms/minor/ditthadhammanibbana.json`
- `diṭṭhāsava` (`ditthasava`; minor) ? `terms/minor/ditthasava.json`
- `diṭṭhi-anusaya` (`ditthi-anusaya`; minor) ? `terms/minor/ditthi-anusaya.json`
- `diṭṭhiyoga` (`ditthiyoga`; minor) ? `terms/minor/ditthiyoga.json`
- `diṭṭhogha` (`ditthogha`; minor) ? `terms/minor/ditthogha.json`
- `dukkhasamudaya` (`dukkha-samudaya`; minor) ? `terms/minor/dukkha-samudaya.json`
- `idaṃsaccābhinivesa kāyagantha` (`idamsacca-abhinivesa-kayagantha`; minor) ? `terms/minor/idamsacca-abhinivesa-kayagantha.json`
- `indriyasaṁvara` (`indriya-samvara`; minor) ? `terms/minor/indriya-samvara.json`
- `jati-nirodha` (`jati-nirodha`; minor) ? `terms/minor/jati-nirodha.json`
- `jati-paccaya` (`jati-paccaya`; minor) ? `terms/minor/jati-paccaya.json`
- `jātisamudaya` (`jati-samudaya`; minor) ? `terms/minor/jati-samudaya.json`
- `kāma-dhātu` (`kama-dhatu`; minor) ? `terms/minor/kama-dhatu.json`
- `kāmarāga-anusaya` (`kamaraga-anusaya`; minor) ? `terms/minor/kamaraga-anusaya.json`
- `kāmāsava` (`kamasava`; minor) ? `terms/minor/kamasava.json`
- `kāmayoga` (`kamayoga`; minor) ? `terms/minor/kamayoga.json`
- `kāmogha` (`kamogha`; minor) ? `terms/minor/kamogha.json`
- `kāyasaṅkhāra` (`kaya-sankhara`; minor) ? `terms/minor/kaya-sankhara.json`
- `kāyagantha` (`kayagantha`; minor) ? `terms/minor/kayagantha.json`
- `mānānusaya` (`mana-anusaya`; minor) ? `terms/minor/mana-anusaya.json`
- `namarupa-nirodha` (`namarupa-nirodha`; minor) ? `terms/minor/namarupa-nirodha.json`
- `namarupa-paccaya` (`namarupa-paccaya`; minor) ? `terms/minor/namarupa-paccaya.json`
- `nāmarūpasamudaya` (`namarupa-samudaya`; minor) ? `terms/minor/namarupa-samudaya.json`
- `orambhāgiya-saṃyojana` (`orambhagiya-samyojana`; minor) ? `terms/minor/orambhagiya-samyojana.json`
- `pabhassara-citta` (`pabhassara-citta`; minor) ? `terms/minor/pabhassara-citta.json`
- `pahāna-saññā` (`pahana-sanna`; minor) ? `terms/minor/pahana-sanna.json`
- `paṭigha-anusaya` (`patigha-anusaya`; minor) ? `terms/minor/patigha-anusaya.json`
- `phassa-nirodha` (`phassa-nirodha`; minor) ? `terms/minor/phassa-nirodha.json`
- `phassa-paccaya` (`phassa-paccaya`; minor) ? `terms/minor/phassa-paccaya.json`
- `rāga-anusaya` (`raga-anusaya`; minor) ? `terms/minor/raga-anusaya.json`
- `salayatana-nirodha` (`salayatana-nirodha`; minor) ? `terms/minor/salayatana-nirodha.json`
- `salayatana-paccaya` (`salayatana-paccaya`; minor) ? `terms/minor/salayatana-paccaya.json`
- `samadhija-piti-sukha` (`samadhija-piti-sukha`; minor) ? `terms/minor/samadhija-piti-sukha.json`
- `samphassa` (`samphassa`; minor) ? `terms/minor/samphassa.json`
- `sankhara-nirodha` (`sankhara-nirodha`; minor) ? `terms/minor/sankhara-nirodha.json`
- `sankhara-paccaya` (`sankhara-paccaya`; minor) ? `terms/minor/sankhara-paccaya.json`
- `sīlabbata-parāmāsa kāyagantha` (`silabbata-paramasa-kayagantha`; minor) ? `terms/minor/silabbata-paramasa-kayagantha.json`
- `tanha-nirodha` (`tanha-nirodha`; minor) ? `terms/minor/tanha-nirodha.json`
- `tanha-paccaya` (`tanha-paccaya`; minor) ? `terms/minor/tanha-paccaya.json`
- `taṇhāsamudaya` (`tanha-samudaya`; minor) ? `terms/minor/tanha-samudaya.json`
- `uddhambhāgiya-saṃyojana` (`uddhambhagiya-samyojana`; minor) ? `terms/minor/uddhambhagiya-samyojana.json`
- `upadana-nirodha` (`upadana-nirodha`; minor) ? `terms/minor/upadana-nirodha.json`
- `upadana-paccaya` (`upadana-paccaya`; minor) ? `terms/minor/upadana-paccaya.json`
- `upādānasamudaya` (`upadana-samudaya`; minor) ? `terms/minor/upadana-samudaya.json`
- `upekkha-satiparisuddha` (`upekkha-satiparisuddha`; minor) ? `terms/minor/upekkha-satiparisuddha.json`
- `upekkha-satiparisuddhi` (`upekkha-satiparisuddhi`; minor) ? `terms/minor/upekkha-satiparisuddhi.json`
- `upekkha-sukha` (`upekkha-sukha`; minor) ? `terms/minor/upekkha-sukha.json`
- `vedana-nirodha` (`vedana-nirodha`; minor) ? `terms/minor/vedana-nirodha.json`
- `vedana-paccaya` (`vedana-paccaya`; minor) ? `terms/minor/vedana-paccaya.json`
- `vedanāsamudaya` (`vedana-samudaya`; minor) ? `terms/minor/vedana-samudaya.json`
- `vicikicchā-anusaya` (`vicikiccha-anusaya`; minor) ? `terms/minor/vicikiccha-anusaya.json`
- `vinnana-nirodha` (`vinnana-nirodha`; minor) ? `terms/minor/vinnana-nirodha.json`
- `vinnana-paccaya` (`vinnana-paccaya`; minor) ? `terms/minor/vinnana-paccaya.json`
- `vivekaja-piti-sukha` (`vivekaja-piti-sukha`; minor) ? `terms/minor/vivekaja-piti-sukha.json`

### Missing `discouraged_translations` (15 term entries)

- `avijjāpaccayā saṅkhārā` (`avijjapaccaya-sankhara`; minor) ? `terms/minor/avijjapaccaya-sankhara.json`
- `bhavapaccayā jāti` (`bhavapaccaya-jati`; minor) ? `terms/minor/bhavapaccaya-jati.json`
- `imasmiṃ asati idaṃ na hoti` (`imasmim-asati-idam-na-hoti`; minor) ? `terms/minor/imasmim-asati-idam-na-hoti.json`
- `imasmiṃ sati idaṃ hoti` (`imasmim-sati-idam-hoti`; minor) ? `terms/minor/imasmim-sati-idam-hoti.json`
- `imassa nirodhā idaṃ nirujjhati` (`imassa-nirodha-idam-nirujjhati`; minor) ? `terms/minor/imassa-nirodha-idam-nirujjhati.json`
- `imassuppādā idaṃ uppajjati` (`imassuppada-idam-uppajjati`; minor) ? `terms/minor/imassuppada-idam-uppajjati.json`
- `jātipaccayā jarāmaraṇaṃ` (`jatipaccaya-jaramaranam`; minor) ? `terms/minor/jatipaccaya-jaramaranam.json`
- `nāmarūpapaccayā saḷāyatanaṃ` (`namarupapaccaya-salayatanam`; minor) ? `terms/minor/namarupapaccaya-salayatanam.json`
- `phassapaccayā vedanā` (`phassapaccaya-vedana`; minor) ? `terms/minor/phassapaccaya-vedana.json`
- `saḷāyatanapaccayā phasso` (`salayatanapaccaya-phasso`; minor) ? `terms/minor/salayatanapaccaya-phasso.json`
- `saṅkhārapaccayā viññāṇaṃ` (`sankharapaccaya-vinnana`; minor) ? `terms/minor/sankharapaccaya-vinnana.json`
- `taṇhāpaccayā upādānaṃ` (`tanhapaccaya-upadana`; minor) ? `terms/minor/tanhapaccaya-upadana.json`
- `upādānapaccayā bhavo` (`upadanapaccaya-bhavo`; minor) ? `terms/minor/upadanapaccaya-bhavo.json`
- `vedanāpaccayā taṇhā` (`vedanapaccaya-tanha`; minor) ? `terms/minor/vedanapaccaya-tanha.json`
- `viññāṇapaccayā nāmarūpaṃ` (`vinnanapaccaya-namarupa`; minor) ? `terms/minor/vinnanapaccaya-namarupa.json`

### Missing `example_phrases` (8 term entries)

- `buddhānussati` (`buddhanussati`; minor) ? `terms/minor/buddhanussati.json`
- `dāna` (`dana`; minor) ? `terms/minor/dana.json`
- `dhammānussati` (`dhammanussati`; minor) ? `terms/minor/dhammanussati.json`
- `saṅghānussati` (`sanghanussati`; minor) ? `terms/minor/sanghanussati.json`
- `sikkhāpada` (`sikkhapada`; minor) ? `terms/minor/sikkhapada.json`
- `tisaraṇa` (`tisarana`; minor) ? `terms/minor/tisarana.json`
- `uposatha` (`uposatha`; minor) ? `terms/minor/uposatha.json`
- `viveka` (`viveka`; minor) ? `terms/minor/viveka.json`

## 4. Drift-Danger Terms (Top 25)

Ranking is based on doctrinal centrality, formula reach, context sensitivity, observed variant count, cross-entry collision exposure, and documentation surface area.

| Rank | Pali term | Preferred | Audit evidence | Brief justification |
| --- | --- | --- | --- | --- |
| 1 | `dukkha` (`dukkha`) | `dissatisfaction` | 4 variants, 5 context rules, 1 discouraged, 2 collision touches, 484 repo refs (56 generated, 24 translations) | High consistency risk because it is tagged three-marks, core-doctrine, four-noble-truths, participates in 5 context rule(s), has 4 governed rendering surface(s), and touches 2 cross-entry collision(s). |
| 2 | `saṅkhārā` (`sankhara`) | `putting things together` | 8 variants, 5 context rules, 2 discouraged, 0 collision touches, 114 repo refs (21 generated, 6 translations) | High consistency risk because it is tagged core-doctrine, dependent-origination, aggregates, context-sensitive, participates in 5 context rule(s), has 8 governed rendering surface(s), and touches 0 cross-entry collision(s). |
| 3 | `viññāṇa` (`vinnana`) | `knowing` | 8 variants, 4 context rules, 5 discouraged, 3 collision touches, 210 repo refs (31 generated, 14 translations) | High consistency risk because it is tagged dependent-origination, aggregates, sense-fields, core-doctrine, context-sensitive, translation-sensitive, participates in 4 context rule(s), has 8 governed rendering surface(s), and touches 3 cross-entry collision(s). |
| 4 | `nibbāna` (`nibbana`) | `nibbāna` | 13 variants, 7 context rules, 6 discouraged, 5 collision touches, 296 repo refs (41 generated, 36 translations) | High consistency risk because it is tagged core-doctrine, translation-sensitive, liberation, consummation-interface, participates in 7 context rule(s), has 13 governed rendering surface(s), and touches 5 cross-entry collision(s). |
| 5 | `sati` (`sati`) | `remembering` | 7 variants, 8 context rules, 3 discouraged, 0 collision touches, 1482 repo refs (217 generated, 226 translations) | High consistency risk because it is tagged core-practice, mental-qualities, translation-sensitive, participates in 8 context rule(s), has 7 governed rendering surface(s), and touches 0 cross-entry collision(s). |
| 6 | `nirodha` (`nirodha`) | `quenching` | 9 variants, 9 context rules, 3 discouraged, 3 collision touches, 484 repo refs (77 generated, 25 translations) | High consistency risk because it is tagged four-noble-truths, core-doctrine, translation-sensitive, liberation, participates in 9 context rule(s), has 9 governed rendering surface(s), and touches 3 cross-entry collision(s). |
| 7 | `taṇhā` (`tanha`) | `ignorant wanting` | 7 variants, 5 context rules, 2 discouraged, 4 collision touches, 256 repo refs (28 generated, 12 translations) | High consistency risk because it is tagged four-noble-truths, dependent-origination, core-doctrine, translation-sensitive, participates in 5 context rule(s), has 7 governed rendering surface(s), and touches 4 cross-entry collision(s). |
| 8 | `upādāna` (`upadana`) | `taking personally` | 8 variants, 8 context rules, 2 discouraged, 4 collision touches, 299 repo refs (53 generated, 11 translations) | High consistency risk because it is tagged core-doctrine, dependent-origination, four-noble-truths, aggregates, translation-sensitive, participates in 8 context rule(s), has 8 governed rendering surface(s), and touches 4 cross-entry collision(s). |
| 9 | `dhamma` (`dhamma`) | `dhamma` | 10 variants, 11 context rules, 1 discouraged, 2 collision touches, 608 repo refs (80 generated, 189 translations) | High consistency risk because it is tagged core-doctrine, translation-sensitive, participates in 11 context rule(s), has 10 governed rendering surface(s), and touches 2 cross-entry collision(s). |
| 10 | `vedanā` (`vedana`) | `felt experience` | 8 variants, 6 context rules, 3 discouraged, 2 collision touches, 195 repo refs (38 generated, 21 translations) | High consistency risk because it is tagged core-doctrine, dependent-origination, aggregates, context-sensitive, translation-sensitive, participates in 6 context rule(s), has 8 governed rendering surface(s), and touches 2 cross-entry collision(s). |
| 11 | `paccaya` (`paccaya`) | `condition` | 4 variants, 4 context rules, 1 discouraged, 4 collision touches, 530 repo refs (146 generated, 6 translations) | High consistency risk because it is tagged core-doctrine, dependent-origination, causality, translation-sensitive, participates in 4 context rule(s), has 4 governed rendering surface(s), and touches 4 cross-entry collision(s). |
| 12 | `paṭiccasamuppāda` (`paticcasamuppada`) | `dependent arising` | 4 variants, 6 context rules, 1 discouraged, 0 collision touches, 64 repo refs (4 generated, 4 translations) | High consistency risk because it is tagged core-doctrine, dependent-origination, context-sensitive, translation-sensitive, participates in 6 context rule(s), has 4 governed rendering surface(s), and touches 0 cross-entry collision(s). |
| 13 | `samādhi` (`samadhi`) | `mental composure` | 9 variants, 6 context rules, 3 discouraged, 1 collision touches, 184 repo refs (20 generated, 19 translations) | High consistency risk because it is tagged core-practice, mental-qualities, participates in 6 context rule(s), has 9 governed rendering surface(s), and touches 1 cross-entry collision(s). |
| 14 | `jhāna` (`jhana`) | `mental theme` | 8 variants, 5 context rules, 4 discouraged, 0 collision touches, 218 repo refs (21 generated, 18 translations) | High consistency risk because it is tagged core-practice, core-doctrine, meditative-development, jhana-factors, participates in 5 context rule(s), has 8 governed rendering surface(s), and touches 0 cross-entry collision(s). |
| 15 | `saññā` (`sanna`) | `recognition` | 5 variants, 3 context rules, 3 discouraged, 0 collision touches, 115 repo refs (20 generated, 13 translations) | High consistency risk because it is tagged core-doctrine, aggregates, translation-sensitive, context-sensitive, participates in 3 context rule(s), has 5 governed rendering surface(s), and touches 0 cross-entry collision(s). |
| 16 | `anattā` (`anatta`) | `not-self` | 6 variants, 4 context rules, 2 discouraged, 0 collision touches, 71 repo refs (16 generated, 5 translations) | High consistency risk because it is tagged core-doctrine, three-marks, aggregates, translation-sensitive, participates in 4 context rule(s), has 6 governed rendering surface(s), and touches 0 cross-entry collision(s). |
| 17 | `anicca` (`anicca`) | `impermanent` | 5 variants, 3 context rules, 1 discouraged, 0 collision touches, 134 repo refs (21 generated, 4 translations) | High consistency risk because it is tagged core-doctrine, three-marks, participates in 3 context rule(s), has 5 governed rendering surface(s), and touches 0 cross-entry collision(s). |
| 18 | `āsava` (`asava`) | `outflow` | 8 variants, 4 context rules, 4 discouraged, 1 collision touches, 100 repo refs (13 generated, 4 translations) | High consistency risk because it is tagged core-doctrine, mental-qualities, liberation, translation-sensitive, participates in 4 context rule(s), has 8 governed rendering surface(s), and touches 1 cross-entry collision(s). |
| 19 | `anusaya` (`anusaya`) | `underlying tendency` | 6 variants, 4 context rules, 3 discouraged, 2 collision touches, 172 repo refs (35 generated, 4 translations) | High consistency risk because it is tagged core-doctrine, mental-qualities, translation-sensitive, participates in 4 context rule(s), has 6 governed rendering surface(s), and touches 2 cross-entry collision(s). |
| 20 | `saṃyojana` (`samyojana`) | `fetter` | 5 variants, 4 context rules, 2 discouraged, 4 collision touches, 50 repo refs (7 generated, 0 translations) | High consistency risk because it is tagged core-doctrine, mental-qualities, liberation, translation-sensitive, participates in 4 context rule(s), has 5 governed rendering surface(s), and touches 4 cross-entry collision(s). |
| 21 | `chanda` (`chanda`) | `desire` | 5 variants, 4 context rules, 2 discouraged, 7 collision touches, 150 repo refs (23 generated, 1 translations) | High consistency risk because it is tagged core-doctrine, core-practice, mental-qualities, translation-sensitive, context-sensitive, participates in 4 context rule(s), has 5 governed rendering surface(s), and touches 7 cross-entry collision(s). |
| 22 | `rāga` (`raga`) | `passion` | 6 variants, 3 context rules, 3 discouraged, 4 collision touches, 154 repo refs (23 generated, 3 translations) | High consistency risk because it is tagged mental-qualities, core-doctrine, liberation, translation-sensitive, participates in 3 context rule(s), has 6 governed rendering surface(s), and touches 4 cross-entry collision(s). |
| 23 | `magga` (`magga`) | `path` | 3 variants, 5 context rules, 1 discouraged, 0 collision touches, 189 repo refs (52 generated, 18 translations) | High consistency risk because it is tagged core-doctrine, core-practice, four-noble-truths, participates in 5 context rule(s), has 3 governed rendering surface(s), and touches 0 cross-entry collision(s). |
| 24 | `citta` (`citta`) | `feeling mind` | 9 variants, 7 context rules, 2 discouraged, 6 collision touches, 221 repo refs (50 generated, 25 translations) | High consistency risk because it is tagged core-doctrine, core-practice, mental-qualities, participates in 7 context rule(s), has 9 governed rendering surface(s), and touches 6 cross-entry collision(s). |
| 25 | `phassa` (`phassa`) | `contact` | 5 variants, 4 context rules, 3 discouraged, 1 collision touches, 332 repo refs (73 generated, 21 translations) | High consistency risk because it is tagged core-doctrine, dependent-origination, sense-fields, translation-sensitive, context-sensitive, participates in 4 context rule(s), has 5 governed rendering surface(s), and touches 1 cross-entry collision(s). |

## 5. Recommended Fix Strategy

1. Triage assertive unregistered renderings first. Start with `pabbajita` -> `renunciate`, `patimokkha` orthography, source-profile `vitakka`/`vic?ra` renderings, `samma-sankappa` -> `attitude`, and ellipsis placeholders such as `upekkh? cetovimutti` -> `liberation of mind through ...`.
2. Resolve cross-entry collisions family by family, not by global search-and-replace. For example, handle `desire` across `chanda`, `ta?h?`, `r?ga`, `k?ma`, and `kamacchanda` in one review pass.
3. Add explicit contrast notes for intentional collisions. If one entry prefers a rendering that another discourages, both entries should cross-link through `related_terms` or explain the contrast in `notes`/`context_rules`.
4. Backfill missing rule fields in risk order. Start with minor entries that appear in the conflict list, generated docs, translation notes, or compounds of the Top 25 drift-danger terms.
5. Keep generated docs downstream. Change live term records or generator code first, regenerate `docs/generated/`, then rerun freshness checks.
6. Add an automated explicit-rendering audit with an allowlist for intentional guardrails and source-profile exceptions.
7. Add a cross-entry collision allowlist with rationale, owner terms, and family notes.
8. Rerun `python scripts/validate_terms.py --strict`, `python scripts/check_translation_drift.py --strict`, `python scripts/check_generated_docs.py`, `python scripts/check_translation_formula_consistency.py --format json`, and affected cluster-policy tests after fixes.

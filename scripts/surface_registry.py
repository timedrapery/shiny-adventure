#!/usr/bin/env python3
"""Registry of outward-facing translation and generated surfaces."""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path

try:
    from scripts.cluster_registry import CLUSTER_SURFACES, ClusterSurface, REPO_ROOT
except ModuleNotFoundError:
    from cluster_registry import CLUSTER_SURFACES, ClusterSurface, REPO_ROOT


@dataclass(frozen=True)
class ReadabilityReview:
    """Integrity state for a surface revised under the plain-English standard."""

    standard: str
    status: str
    reviewed_on: str
    body_sha256: str


@dataclass(frozen=True)
class TranslationSurface:
    key: str
    label: str
    main_relpath: str
    notes_relpath: str
    readability_review: ReadabilityReview | None = None

    @property
    def main_path(self) -> Path:
        return REPO_ROOT / self.main_relpath

    @property
    def notes_path(self) -> Path:
        return REPO_ROOT / self.notes_relpath

    @property
    def main_name(self) -> str:
        return Path(self.main_relpath).name

    @property
    def notes_name(self) -> str:
        return Path(self.notes_relpath).name


TRANSLATION_SURFACES: tuple[TranslationSurface, ...] = (
    TranslationSurface(
        key="mn1",
        label="MN 1",
        main_relpath="docs/translations/mn1-mulapariyaya-sutta.md",
        notes_relpath="docs/translations/mn1-mulapariyaya-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn2",
        label="MN 2",
        main_relpath="docs/translations/mn2-sabbasava-sutta.md",
        notes_relpath="docs/translations/mn2-sabbasava-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn7",
        label="MN 7",
        main_relpath="docs/translations/mn7-vattha-sutta.md",
        notes_relpath="docs/translations/mn7-vattha-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn9",
        label="MN 9",
        main_relpath="docs/translations/mn9-sammaditthi-sutta.md",
        notes_relpath="docs/translations/mn9-sammaditthi-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn10",
        label="MN 10",
        main_relpath="docs/translations/mn10-satipatthana-sutta.md",
        notes_relpath="docs/translations/mn10-satipatthana-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn11",
        label="MN 11",
        main_relpath="docs/translations/mn11-culasihanada-sutta.md",
        notes_relpath="docs/translations/mn11-culasihanada-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn18",
        label="MN 18",
        main_relpath="docs/translations/mn18-madhupindika-sutta.md",
        notes_relpath="docs/translations/mn18-madhupindika-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn19",
        label="MN 19",
        main_relpath="docs/translations/mn19-dvedhavitakka-sutta.md",
        notes_relpath="docs/translations/mn19-dvedhavitakka-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn22",
        label="MN 22",
        main_relpath="docs/translations/mn22-alagaddupama-sutta.md",
        notes_relpath="docs/translations/mn22-alagaddupama-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn26",
        label="MN 26",
        main_relpath="docs/translations/mn26-pasarasi-sutta.md",
        notes_relpath="docs/translations/mn26-pasarasi-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn38",
        label="MN 38",
        main_relpath="docs/translations/mn38-mahatanhasankhaya-sutta.md",
        notes_relpath="docs/translations/mn38-mahatanhasankhaya-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn39",
        label="MN 39",
        main_relpath="docs/translations/mn39-maha-assapura-sutta.md",
        notes_relpath="docs/translations/mn39-maha-assapura-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn43",
        label="MN 43",
        main_relpath="docs/translations/mn43-mahavedalla-sutta.md",
        notes_relpath="docs/translations/mn43-mahavedalla-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn44",
        label="MN 44",
        main_relpath="docs/translations/mn44-culavedalla-sutta.md",
        notes_relpath="docs/translations/mn44-culavedalla-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn61",
        label="MN 61",
        main_relpath="docs/translations/mn61-ambalatthikarahulovada-sutta.md",
        notes_relpath="docs/translations/mn61-ambalatthikarahulovada-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn63",
        label="MN 63",
        main_relpath="docs/translations/mn63-culamalukya-sutta.md",
        notes_relpath="docs/translations/mn63-culamalukya-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn64",
        label="MN 64",
        main_relpath="docs/translations/mn64-mahamalukya-sutta.md",
        notes_relpath="docs/translations/mn64-mahamalukya-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn99",
        label="MN 99",
        main_relpath="docs/translations/mn99-subha-sutta.md",
        notes_relpath="docs/translations/mn99-subha-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn117",
        label="MN 117",
        main_relpath="docs/translations/mn117-mahacattarisaka-sutta.md",
        notes_relpath="docs/translations/mn117-mahacattarisaka-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn118",
        label="MN 118",
        main_relpath="docs/translations/mn118-anapanasati-sutta.md",
        notes_relpath="docs/translations/mn118-anapanasati-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn119",
        label="MN 119",
        main_relpath="docs/translations/mn119-kayagatasati-sutta.md",
        notes_relpath="docs/translations/mn119-kayagatasati-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn131",
        label="MN 131",
        main_relpath="docs/translations/mn131-bhaddekaratta-sutta.md",
        notes_relpath="docs/translations/mn131-bhaddekaratta-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn137",
        label="MN 137",
        main_relpath="docs/translations/mn137-salayatanavibhanga-sutta.md",
        notes_relpath="docs/translations/mn137-salayatanavibhanga-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn141",
        label="MN 141",
        main_relpath="docs/translations/mn141-saccavibhanga-sutta.md",
        notes_relpath="docs/translations/mn141-saccavibhanga-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn148",
        label="MN 148",
        main_relpath="docs/translations/mn148-chachakka-sutta.md",
        notes_relpath="docs/translations/mn148-chachakka-sutta-notes.md",
    ),
    TranslationSurface(
        key="sn12_11",
        label="SN 12.11",
        main_relpath="docs/translations/sn12-11-ahara-sutta.md",
        notes_relpath="docs/translations/sn12-11-ahara-sutta-notes.md",
    ),
    TranslationSurface(
        key="sn12_61",
        label="SN 12.61",
        main_relpath="docs/translations/sn12-61-assutava-sutta.md",
        notes_relpath="docs/translations/sn12-61-assutava-sutta-notes.md",
    ),
    TranslationSurface(
        key="sn12_15",
        label="SN 12.15",
        main_relpath="docs/translations/sn12-15-kaccanagotta-sutta.md",
        notes_relpath="docs/translations/sn12-15-kaccanagotta-sutta-notes.md",
    ),
    TranslationSurface(
        key="sn12_23",
        label="SN 12.23",
        main_relpath="docs/translations/sn12-23-upanisa-sutta.md",
        notes_relpath="docs/translations/sn12-23-upanisa-sutta-notes.md",
    ),
    TranslationSurface(
        key="sn12_2",
        label="SN 12.2",
        main_relpath="docs/translations/sn12-2-paticcasamuppada-vibhanga-sutta.md",
        notes_relpath="docs/translations/sn12-2-paticcasamuppada-vibhanga-sutta-notes.md",
    ),
    TranslationSurface(
        key="sn51_13",
        label="SN 51.13",
        main_relpath="docs/translations/sn51-13-chandasamadhi-sutta.md",
        notes_relpath="docs/translations/sn51-13-chandasamadhi-sutta-notes.md",
    ),
    TranslationSurface(
        key="sn1_1",
        label="SN 1.1",
        main_relpath="docs/translations/sn1-1-oghatara-sutta.md",
        notes_relpath="docs/translations/sn1-1-oghatara-sutta-notes.md",
    ),
    TranslationSurface(
        key="sn55_5",
        label="SN 55.5",
        main_relpath="docs/translations/sn55-5-dutiyasariputta-sutta.md",
        notes_relpath="docs/translations/sn55-5-dutiyasariputta-sutta-notes.md",
    ),
    TranslationSurface(
        key="sn56_11",
        label="SN 56.11",
        main_relpath="docs/translations/sn56-11-dhammacakkappavattana-sutta.md",
        notes_relpath="docs/translations/sn56-11-dhammacakkappavattana-sutta-notes.md",
    ),
    TranslationSurface(
        key="sn22_59",
        label="SN 22.59",
        main_relpath="docs/translations/sn22-59-anattalakkhana-sutta.md",
        notes_relpath="docs/translations/sn22-59-anattalakkhana-sutta-notes.md",
    ),
    TranslationSurface(
        key="sn22_48",
        label="SN 22.48",
        main_relpath="docs/translations/sn22-48-khandha-sutta.md",
        notes_relpath="docs/translations/sn22-48-khandha-sutta-notes.md",
    ),
    TranslationSurface(
        key="sn22_89",
        label="SN 22.89",
        main_relpath="docs/translations/sn22-89-khemaka-sutta.md",
        notes_relpath="docs/translations/sn22-89-khemaka-sutta-notes.md",
    ),
    TranslationSurface(
        key="sn22_86",
        label="SN 22.86",
        main_relpath="docs/translations/sn22-86-anuradha-sutta.md",
        notes_relpath="docs/translations/sn22-86-anuradha-sutta-notes.md",
    ),
    TranslationSurface(
        key="sn35_28",
        label="SN 35.28",
        main_relpath="docs/translations/sn35-28-aditta-sutta.md",
        notes_relpath="docs/translations/sn35-28-aditta-sutta-notes.md",
    ),
    TranslationSurface(
        key="sn45_2",
        label="SN 45.2",
        main_relpath="docs/translations/sn45-2-upaddha-sutta.md",
        notes_relpath="docs/translations/sn45-2-upaddha-sutta-notes.md",
    ),
    TranslationSurface(
        key="sn36_6",
        label="SN 36.6",
        main_relpath="docs/translations/sn36-6-salla-sutta.md",
        notes_relpath="docs/translations/sn36-6-salla-sutta-notes.md",
    ),
    TranslationSurface(
        key="sn46_51",
        label="SN 46.51",
        main_relpath="docs/translations/sn46-51-ahara-sutta.md",
        notes_relpath="docs/translations/sn46-51-ahara-sutta-notes.md",
    ),
    TranslationSurface(
        key="sn48_10",
        label="SN 48.10",
        main_relpath="docs/translations/sn48-10-dutiyavibhanga-sutta.md",
        notes_relpath="docs/translations/sn48-10-dutiyavibhanga-sutta-notes.md",
    ),
    TranslationSurface(
        key="an2_9",
        label="AN 2.9",
        main_relpath="docs/translations/an2-9-cariya-sutta.md",
        notes_relpath="docs/translations/an2-9-cariya-sutta-notes.md",
    ),
    TranslationSurface(
        key="an3_65",
        label="AN 3.65",
        main_relpath="docs/translations/an3-65-kesamutta-sutta.md",
        notes_relpath="docs/translations/an3-65-kesamutta-sutta-notes.md",
    ),
    TranslationSurface(
        key="an3_69",
        label="AN 3.69",
        main_relpath="docs/translations/an3-69-akusalamula-sutta.md",
        notes_relpath="docs/translations/an3-69-akusalamula-sutta-notes.md",
    ),
    TranslationSurface(
        key="an4_5",
        label="AN 4.5",
        main_relpath="docs/translations/an4-5-anusota-sutta.md",
        notes_relpath="docs/translations/an4-5-anusota-sutta-notes.md",
    ),
    TranslationSurface(
        key="an4_113",
        label="AN 4.113",
        main_relpath="docs/translations/an4-113-patoda-sutta.md",
        notes_relpath="docs/translations/an4-113-patoda-sutta-notes.md",
    ),
    TranslationSurface(
        key="an6_63",
        label="AN 6.63",
        main_relpath="docs/translations/an6-63-nibbedhika-sutta.md",
        notes_relpath="docs/translations/an6-63-nibbedhika-sutta-notes.md",
    ),
    TranslationSurface(
        key="an8_6",
        label="AN 8.6",
        main_relpath="docs/translations/an8-6-dutiyalokadhamma-sutta.md",
        notes_relpath="docs/translations/an8-6-dutiyalokadhamma-sutta-notes.md",
    ),
    TranslationSurface(
        key="an10_60",
        label="AN 10.60",
        main_relpath="docs/translations/an10-60-giriminanda-sutta.md",
        notes_relpath="docs/translations/an10-60-giriminanda-sutta-notes.md",
    ),
    TranslationSurface(
        key="an11_9",
        label="AN 11.9",
        main_relpath="docs/translations/an11-9-saddha-sutta.md",
        notes_relpath="docs/translations/an11-9-saddha-sutta-notes.md",
    ),
    TranslationSurface(
        key="dn2",
        label="DN 2",
        main_relpath="docs/translations/dn2-samannaphala-sutta.md",
        notes_relpath="docs/translations/dn2-samannaphala-sutta-notes.md",
    ),
    TranslationSurface(
        key="dn15",
        label="DN 15",
        main_relpath="docs/translations/dn15-mahanidana-sutta.md",
        notes_relpath="docs/translations/dn15-mahanidana-sutta-notes.md",
    ),
    TranslationSurface(
        key="iti44",
        label="Iti 44",
        main_relpath="docs/translations/iti44-nibbanadhatu-sutta.md",
        notes_relpath="docs/translations/iti44-nibbanadhatu-sutta-notes.md",
    ),
)


READABILITY_BODY_SHA256: dict[str, str] = {
    "mn1": "f31b212f0f4adc6f284574023d82cd182c4956d5e8bc39ec8f1452b77d543cdf",
    "mn2": "09782d8ad37ed3a3d5689cdd7c9b7c5b75d7a3e3e5f61e7779d9d677f0920f98",
    "mn7": "5a7fe259f744027b4bd37566ce894b0d88ee52a5d9a25012d3b140b7311af870",
    "mn9": "b8b5bd840ed8d7f9d4777cc7349221f3c03609cfdb02b85d97e37f6b28b8a4d7",
    "mn10": "f23b995475667c0cb2f4fd8f84f2dfc8832530c09858265f0e2f70345e8260f5",
    "mn11": "1b8811594f7e00ed3f54d8d1ffc9ecf3b9ff2c21dc92d0ecd41b0e2ab1dae761",
    "mn18": "7a7dd6b91af02d2c11b138cd9935d0bb3e13e4ae4f57c9dd065d7d83fb92802e",
    "mn19": "cbd316fc12b13ac6362a881d0c084300195e4abaf848d9ca1b1daa5e666fb012",
    "mn22": "c4d78501fbf276810b7f9e5bca28f2b8aed3c99895745c7410347555729ff43e",
    "mn26": "839a76a0fe62caa29f03c7ee03a21ccbf0f2e5f245472183a2e8a5a1734921a2",
    "mn38": "04cb1af6c20c7c80fd2ecc339386f6efbe427ed8c61c45e417e7c17478f0fe82",
    "mn39": "2d7ef3498aed55c1c45d2a39afd96ef1d63fa60427469ef7e706b13ba52701a3",
    "mn43": "89e8048c79bb6800263f7b4640e5ff88f9c15a39238797cfa6e59674a2e1adc1",
    "mn44": "8ebf5a76faa284802e000f9ba46c2822aa15627f900c65a036e783c8bd266179",
    "mn61": "6224dad79a4f97b99992407ea1f63f333370bf81f986706de44f243395a4ff25",
    "mn63": "24d4fdba2728415fb92c273deb97d17e189841c8a0927516a4b2a62d712bf946",
    "mn64": "fe75862e43caf1286ae35d43b7d399562687006f3b164046abd010bdbf5deb65",
    "mn99": "fe958da081881326fbc5f0e379908c48a1c68500b01feb379b34510a966f2d5c",
    "mn117": "e5d69b1863169ccc9a9f3fb503b413294aa84aa0951eca6c5a571dcb34261b60",
    "mn118": "21e66145b96bad998cfc4ffb60162d3c01d0471c18a24ef1dcf1576cf626c653",
    "mn119": "d7be0fc71bfe595116ec6b72009a75f9ba210d90ea084818447fc19666e437a5",
    "mn131": "6c6498fe1ee6c5763b1ae962c2e0dd2c22018ef53d59fd7a8cd50d078f67912f",
    "mn137": "af7beff3ec76703d37e219397f9996880768fe9532a83d48162851447ccbdbc3",
    "mn141": "a91647e933848b1215c94b313e7deccb01dabec1bf56330feb46806179239976",
    "mn148": "cc80f649865587452fd0a52fd39ecd47ea518bb3b34c36e9203c8ac27f5407c1",
    "sn12_11": "1e477e680b47e78332c3a7a6b0168aa0b0801d4ff6a4b9c9a6e15da921b5f522",
    "sn12_61": "d6425a0e787dbd6c87cb12ad3e52fd50c192bdd7b655a26554a560038b9eb11c",
    "sn12_15": "f4edd91be61c2e628c09ed7e4dca8dc7fd2933f5f69ad44544a6a8d7e4e12aaf",
    "sn12_23": "2c2f48345aaea34edc489a04ca3a56e963f91d7ce2216f1a67f57482b282de1a",
    "sn12_2": "29ceade9662e6be88c86dad8995040ffd62a12158f544959b605b79ccbddaa83",
    "sn51_13": "9bab46d9c0f2feb7e1994f3bdbd265a74b9acae41e9058ecb3d700573af15763",
    "sn1_1": "88ae416984752a677d3ec1b16af2da325087413fa095f5ec493690da2a2beaa7",
    "sn55_5": "ce0bbcfd5619eae08a38c0d01fab39674c232f73f2bab3c806d8b4968913ef2c",
    "sn56_11": "7be7a57e337b8d536d1419f8e7e7f19921596cfd5edf416a29127114890f0a89",
    "sn22_59": "5930c6f6002ce701ce478afa5c118259b6f7f5279e788bdf14e6a0e0e1792c1c",
    "sn22_48": "b5ac6f591e4b8d397e205f8cae8b75629c974c4e9e0d84a7b9b3d1b808a5b49f",
    "sn22_89": "5576eb92bb12962fd92605a1d7bc28071d300d2ce207eb766bb700d73914a1b0",
    "sn22_86": "87b39d295adc90ee1681ca017149892e5c98b5096d04ff0367ef5c72cc93bd09",
    "sn35_28": "b159e8dd510ce49333e7be928a5fd807c6b585af52fe3722e4677036a63b90a3",
    "sn45_2": "044d73b1c4a850b57400a297bad0fc923b9d8a75b48b4ff16295278264b03321",
    "sn36_6": "0199c3d1f32f78ce1cf5ca14669a237ca25c5088053fb3b8d67c7eeda9f64085",
    "sn46_51": "089c5d05fdadf815ca6ab2fa0cbca72f7df0a9375d3fb5ba5d48544647584cb4",
    "sn48_10": "a7c91d4ed5b885b4e287022b0718eac6c0cf1e8bcbd17eab97776f39d01c90ec",
    "an2_9": "b5c2faee1db36d2fd41866fda2422e1258649b9d621a8ccfcc9746faea5d4790",
    "an3_65": "e0d025b9597ca291e006f0cb8cf7a0cd2e369d67f2dd657ae0f571f44efb3986",
    "an3_69": "70ab99be572724b9051681ae7a8525b99dc129c518dbacf37dace77488aa0e44",
    "an4_5": "c869ec99776dfd12c82e1d93a5b0bc4a16c6e27fee0966a82e165303f3b31837",
    "an4_113": "fcd415f18a8c6738f548ff4eaa1733bebe4b850e6f50e4787527ed2e2a08a166",
    "an6_63": "d40dbfbf1d64a355fffa1a14d98d2dcc07661ff33b73d59cd0815f697bc3fc6c",
    "an8_6": "0f532dc82ac30bda4c3a1d4300404280c988c6c08bf1272da8a91df46618d7da",
    "an10_60": "55a08fcdd577c9177b17bb62672d11c27c278f6f27d23a0641279411285c54fc",
    "an11_9": "5be8a71c5b42fe60e4b30d4aa7ee37f5a7eaf6e0b67f7279352c1d4d04ac1abd",
    "dn2": "e14ae3eb8758d509eac9c1868993c55eb3ac51bd18763bfe28bb2a68c47ce323",
    "dn15": "8461edc9ebaee7f98b372823f02660f84fba4534308cc3b74f3f17922f37c9f1",
    "iti44": "bc0e4a36775633d0ea0fa487d86851a0a7957f9384a4b31720718556716fd768",
}

READABILITY_REVIEWED_ON: dict[str, str] = {
    "an2_9": "2026-08-24",
    "an3_69": "2026-08-24",
    "an4_5": "2026-08-24",
    "sn1_1": "2026-08-24",
    "mn131": "2026-08-24",
    "sn22_86": "2026-08-24",
    "mn119": "2026-08-24",
    "sn45_2": "2026-08-24",
    "an8_6": "2026-08-24",
    "mn38": "2026-08-24",
    "mn137": "2026-08-24",
    "sn12_15": "2026-08-24",
    "an10_60": "2026-08-24",
}

TRANSLATION_SURFACES = tuple(
    replace(
        surface,
        readability_review=ReadabilityReview(
            standard="plain-english-v1",
            status="provisional",
            reviewed_on=READABILITY_REVIEWED_ON.get(surface.key, "2026-08-23"),
            body_sha256=READABILITY_BODY_SHA256[surface.key],
        ),
    )
    for surface in TRANSLATION_SURFACES
)


def generated_surface_groups() -> tuple[ClusterSurface, ...]:
    """Return the CI-enforced generated doc groups backed by report scripts."""

    return CLUSTER_SURFACES


@dataclass(frozen=True)
class ReaderMeta:
    """Reader-facing metadata for one governed translation surface.

    This lives beside TRANSLATION_SURFACES rather than in a second registry, so
    there is exactly one place that knows the corpus. The reader generator in
    `scripts/generate_reader.py` derives page titles, the newcomer reading
    path, the All Suttas index, and the site navigation from these fields.

    reader_title  A plain-English title for readers, or None to fall back to
                  the Pali title. Only texts with a hand-written "About this
                  text" introduction normally get one.
    pali_title    The Pali name, without the collection reference.
    stage         Which stage of the newcomer reading path the text sits in.
    order         Position within that stage.
    path_note     The one-line editorial note shown on the Start Here page.
                  This is reader-facing editorial content, not a summary
                  generated from the translation.
    """

    pali_title: str
    stage: int
    order: int
    path_note: str
    reader_title: str | None = None


STAGES: tuple[tuple[int, str, str], ...] = (
    (
        1,
        "Before Any Doctrine",
        "Texts that set the tone before anything technical shows up: why to "
        "trust this material at all, why some questions get deliberately left "
        "unanswered, and who was actually asking these questions.",
    ),
    (
        2,
        "The Basic Diagnosis and the Path",
        "The core claim and the practical response to it, kept concrete.",
    ),
    (
        3,
        "Learning to Look at Your Own Mind",
        "Practical method. This is where the material stops being about ideas "
        "and starts being about what you actually do.",
    ),
    (
        4,
        "Not-Self and Dependent Arising",
        "The harder doctrinal core. Everything here assumes the practical "
        "vocabulary from the earlier stages, and tests it against the two "
        "hardest ideas in the material.",
    ),
    (
        5,
        "Advanced and Reference Texts",
        "Technical material that rewards already knowing the vocabulary cold. "
        "These are texts people return to rather than read straight through.",
    ),
)

# Five suggested entry points that together introduce the collection's main
# themes. Keys index into TRANSLATION_SURFACES.
ESSENTIAL_FIVE: tuple[str, ...] = (
    "an3_65", "sn56_11", "sn36_6", "mn63", "sn22_59",
)

READER_METADATA: dict[str, ReaderMeta] = {
    # Stage 1 -- Before Any Doctrine
    "an3_65": ReaderMeta(
        "Kesamutta Sutta", 1, 1,
        "A practical starting point for judging a teaching: tradition, "
        "reasoning, and a teacher's authority are not sufficient on their own. "
        "Examine what happens when a teaching is put into practice.",
        reader_title="How to Test a Teaching",
    ),
    "sn45_2": ReaderMeta(
        "Upaḍḍha Sutta", 1, 2,
        "Ānanda calls good friendship half the spiritual life; the Buddha calls "
        "it the whole. A short, social bridge from testing a teaching to "
        "actually developing the path.",
        reader_title="Good Friendship Is the Whole Path",
    ),
    "mn63": ReaderMeta(
        "Cūḷamālukya Sutta", 1, 3,
        "Why the teaching refuses to answer certain metaphysical questions. "
        "Directly answers the objection a skeptical reader will already be "
        "forming after the first text.",
        reader_title="The Man Struck by a Poisoned Arrow",
    ),
    "mn26": ReaderMeta(
        "Pāsarāsi Sutta", 1, 4,
        "The Buddha's own account of leaving home, studying under two teachers, "
        "and finding them insufficient. A narrative, not a doctrine — a human "
        "anchor before the vocabulary gets technical.",
        reader_title="The Two Searches",
    ),
    # Stage 2 -- The Basic Diagnosis and the Path
    "sn56_11": ReaderMeta(
        "Dhammacakkappavattana Sutta", 2, 1,
        "The first sermon: the four noble truths and the eightfold path stated "
        "directly. Foundational, but reads better once Stage 1 has set the "
        "frame — taken cold, its formulaic structure can feel like a list to "
        "memorize rather than a diagnosis to recognize.",
        reader_title="The First Teaching",
    ),
    "sn36_6": ReaderMeta(
        "Salla Sutta", 2, 2,
        "The one-arrow/two-arrows teaching: physical pain versus the added "
        "mental suffering piled on top of it. Concrete, bodily, and "
        "immediately recognizable.",
        reader_title="One Arrow, Not Two",
    ),
    "an8_6": ReaderMeta(
        "Dutiyalokadhamma Sutta", 2, 3,
        "Gain and loss, praise and blame, pleasure and pain happen to everyone. "
        "The difference is whether they take over the heart.",
        reader_title="When Life Goes Up and Down",
    ),
    "an2_9": ReaderMeta(
        "Cariya Sutta", 2, 4,
        "Two bright qualities protect the human world: conscience, the inward "
        "sense of integrity, and moral caution about harm and consequences.",
        reader_title="What Keeps the World Human",
    ),
    "mn7": ReaderMeta(
        "Vattha Sutta", 2, 5,
        "A mind is like cloth: dye it while it is dirty and the colour comes "
        "out wrong. Ethics introduced through a simile instead of a rule list.",
        reader_title="The Dirty Cloth",
    ),
    "an3_69": ReaderMeta(
        "Akusalamūla Sutta", 2, 6,
        "Greed, aversion, and delusion are traced from their roots to their "
        "effects on action, speech, power, and the heart—then contrasted with "
        "non-greed, non-aversion, and clarity.",
        reader_title="What Drives Harm—and What Ends It",
    ),
    "an4_5": ReaderMeta(
        "Anusota Sutta", 2, 7,
        "Four ways of meeting the current: drifting with it, struggling "
        "against it, standing firm, and completing the crossing to dry land.",
        reader_title="Going With the Stream—or Against It",
    ),
    "sn1_1": ReaderMeta(
        "Oghataraṇa Sutta", 2, 8,
        "A deity asks how the Buddha crossed a flood. The answer refuses both "
        "standing still and forceful struggle, preserving a compact paradox.",
        reader_title="How Do You Cross the Flood?",
    ),
    "an4_113": ReaderMeta(
        "Patoda Sutta", 2, 9,
        "Four kinds of horses, four kinds of people, and what it actually takes "
        "to be moved to practice. A jolt of urgency after three fairly calm "
        "texts.",
        reader_title="Four Horses",
    ),
    "sn55_5": ReaderMeta(
        "Dutiyasāriputta Sutta", 2, 10,
        "What actually leads to the path, in four steps that are ordinary "
        "enough to follow: find good company, hear the teaching, attend to it "
        "carefully, then practise in line with it. The first item is social, "
        "not inward.",
        reader_title="Four Steps That Lead to the Path",
    ),
    "an11_9": ReaderMeta(
        "Saddha Sutta", 2, 11,
        "A wild colt tied to its trough can think of nothing but \"Fodder, "
        "fodder!\" The contrast with a trained horse becomes a contrast between "
        "two ways of sitting down to meditate.",
        reader_title="Think Like a Thoroughbred",
    ),
    # Stage 3 -- Learning to Look at Your Own Mind
    "mn19": ReaderMeta(
        "Dvedhāvitakka Sutta", 3, 1,
        "Sorting thoughts into two bins and learning what to do with each. The "
        "simplest possible entry point into mind-training.",
        reader_title="Two Kinds of Thinking",
    ),
    "mn61": ReaderMeta(
        "Ambalaṭṭhikarāhulovāda Sutta", 3, 2,
        "The Buddha teaches his own son Rāhula, using a water vessel emptied "
        "and turned upside down, then a war elephant, to make the case that "
        "someone who feels no shame lying has nothing left to hold them back. "
        "From there: a nine-part checklist for examining any action of body, "
        "speech, or mind before, during, and after doing it.",
        reader_title="The Water Vessel",
    ),
    "mn2": ReaderMeta(
        "Sabbāsava Sutta", 3, 3,
        "Seven concrete methods for handling what erodes the mind: restraint, "
        "use, endurance, avoidance, removal, development. A toolkit, not a "
        "theory.",
        reader_title="Seven Ways to Handle What Erodes the Mind",
    ),
    "mn118": ReaderMeta(
        "Ānāpānasati Sutta", 3, 4,
        "Step-by-step instructions for remembering the Dhamma while breathing "
        "in and out. The first text on this list that is a practice manual "
        "rather than a teaching about practice.",
        reader_title="Remembering the Dhamma While Breathing In and Out",
    ),
    "mn10": ReaderMeta(
        "Satipaṭṭhāna Sutta", 3, 5,
        "The four foundations of remembering, and the longest, densest text so "
        "far. Not really a one-sitting read: it is the reference manual for "
        "the pieces above, worth returning to rather than finishing.",
        reader_title="The Four Foundations of Remembering",
    ),
    "mn119": ReaderMeta(
        "Kāyagatāsati Sutta", 3, 6,
        "A long practice sequence directing remembering to breathing, movement, "
        "the body's contents and fate, deep composure, resilience, and ten "
        "claimed results.",
        reader_title="Remembering Directed to the Body",
    ),
    "dn2": ReaderMeta(
        "Sāmaññaphala Sutta", 3, 7,
        "A king asks what a renunciant actually gets out of the life. A full "
        "narrative walk through the gradual path from an outsider's curious, "
        "slightly skeptical point of view.",
        reader_title="What Does a Renunciant Gain?",
    ),
    "an10_60": ReaderMeta(
        "Girimānanda Sutta", 3, 8,
        "Ten perceptions taught to a sick monk. Practical and, unusually for "
        "this stage, comforting.",
        reader_title="Ten Perceptions for a Sick Monk",
    ),
    "mn39": ReaderMeta(
        "Mahā-Assapura Sutta", 3, 9,
        "What actually makes someone a genuine renunciant, as opposed to "
        "someone who merely looks like one. Ethics and practice fused.",
        reader_title="What Makes a Genuine Renunciant?",
    ),
    "sn46_51": ReaderMeta(
        "Āhāra Sutta", 3, 10,
        "What feeds the distractions that block practice, and what starves "
        "them. A closing, practical text for this stage.",
        reader_title="What Feeds and Starves Distraction",
    ),
    # Stage 4 -- Not-Self and Dependent Arising
    "sn22_59": ReaderMeta(
        "Anattalakkhaṇa Sutta", 4, 1,
        "The second sermon. Not-self laid out as a clean, followable argument "
        "rather than an assertion.",
        reader_title="What Is Fit to Call Self?",
    ),
    "mn22": ReaderMeta(
        "Alagaddūpama Sutta", 4, 2,
        "The snake simile and the raft simile carry genuinely difficult "
        "not-self doctrine on strong enough imagery that it stays followable.",
        reader_title="The Snake and the Raft",
    ),
    "sn22_48": ReaderMeta(
        "Khandha Sutta", 4, 3,
        "What the five heaps actually are, stated directly.",
        reader_title="The Five Heaps",
    ),
    "sn22_86": ReaderMeta(
        "Anurādha Sutta", 4, 4,
        "Anurādha tries to place the Tathāgata outside four claims about what "
        "happens after death. The Buddha asks whether the Tathāgata can be "
        "pinned down through the five heaps even here and now.",
        reader_title="Can You Pin Down the Tathāgata?",
    ),
    "sn22_89": ReaderMeta(
        "Khemaka Sutta", 4, 5,
        "A subtler point: even someone who has genuinely seen not-self can "
        "still carry a faint, hard-to-locate sense of \"I am.\"",
        reader_title="The Lingering Sense of 'I Am'",
    ),
    "mn131": ReaderMeta(
        "Bhaddekaratta Sutta", 4, 6,
        "Do not chase the past or long for the future — but do not mistake "
        "that for a slogan about living in the moment. The explanation asks "
        "whether you are turning any part of present experience into self.",
        reader_title="Don't Chase the Past or Long for the Future",
    ),
    "mn148": ReaderMeta(
        "Chachakka Sutta", 4, 7,
        "A systematic, almost mechanical working-through of not-self across "
        "every sense door. Dense, but by this point the pattern should be "
        "familiar.",
        reader_title="Not-Self at the Six Sense Doors",
    ),
    "sn12_15": ReaderMeta(
        "Kaccānagotta Sutta", 4, 8,
        "One page, defining right view as the middle between \"it exists\" and "
        "\"it doesn't.\" The clearest, shortest bridge into dependent arising.",
        reader_title="Between 'It Exists' and 'It Doesn't'",
    ),
    "sn12_61": ReaderMeta(
        "Assutavā Sutta", 4, 9,
        "An argument that runs the opposite way from what you expect: if you "
        "must identify with something, the body is the safer choice, because "
        "its changing is visible and the mind's is not.",
        reader_title="Body and Mind Keep Changing",
    ),
    "sn12_23": ReaderMeta(
        "Upanisa Sutta", 4, 10,
        "The positive chain, dissatisfaction leading step by step to freedom, "
        "mirroring the well-known negative chain.",
        reader_title="From Dissatisfaction to Freedom",
    ),
    "sn12_11": ReaderMeta(
        "Āhāra Sutta", 4, 11,
        "Four things that keep a life going, traced back to wanting and then "
        "all the way back along the chain. Not to be confused with SN 46.51, "
        "which shares its name.",
        reader_title="What Keeps a Life Going",
    ),
    "sn12_2": ReaderMeta(
        "Paṭiccasamuppāda-vibhaṅga Sutta", 4, 12,
        "The standard formula of dependent arising, defined term by term.",
        reader_title="Dependent Arising, Term by Term",
    ),
    "mn38": ReaderMeta(
        "Mahātaṇhāsaṅkhaya Sutta", 4, 13,
        "A monk's wrong view — that the same consciousness travels on "
        "unchanged — gets corrected, and dependent arising gets restated in "
        "narrative, argued form rather than as a bare formula.",
        reader_title="Does the Same Consciousness Continue?",
    ),
    "dn15": ReaderMeta(
        "Mahānidāna Sutta", 4, 14,
        "The deepest and longest exposition of dependent arising in the set. "
        "The capstone of this stage, not an entry point to it.",
        reader_title="Dependent Arising in Depth",
    ),
    "mn9": ReaderMeta(
        "Sammādiṭṭhi Sutta", 4, 15,
        "Right view examined through more than a dozen different doctrinal "
        "lenses in one text. Reads best as a review once the pieces it is "
        "reviewing are already familiar.",
        reader_title="Right View from Many Angles",
    ),
    # Stage 5 -- Advanced and Reference Texts
    "mn43": ReaderMeta(
        "Mahāvedalla Sutta", 5, 2,
        "The longer companion to MN 44, and the same format: two senior "
        "disciples working through the vocabulary point by point. Read it "
        "second — it assumes more.",
        reader_title="The Longer Questions and Answers",
    ),
    "mn44": ReaderMeta(
        "Cūḷavedalla Sutta", 5, 1,
        "A systematic question-and-answer exchange between two disciples, "
        "covering a wide sweep of doctrine efficiently.",
        reader_title="Questions and Answers on the Teaching",
    ),
    "sn51_13": ReaderMeta(
        "Chandasamādhi Sutta", 5, 3,
        "One short formula, stated four times, defining the four bases of "
        "power. Useful mainly as a reference for how the effort formula is "
        "built.",
        reader_title="The Four Bases of Power",
    ),
    "sn48_10": ReaderMeta(
        "Dutiyavibhaṅga Sutta", 5, 4,
        "Five definitions, one per faculty, each written as something a "
        "person does rather than something they have. The shortest place to "
        "see confidence, energy, remembering, composure, and discernment "
        "treated as one set.",
        reader_title="The Five Faculties",
    ),
    "mn64": ReaderMeta(
        "Mahāmālukya Sutta", 5, 5,
        "The five lower fetters, and the companion piece to MN 63 — same "
        "disciple, later in his practice.",
        reader_title="The Five Lower Fetters",
    ),
    "mn11": ReaderMeta(
        "Cūḷasīhanāda Sutta", 5, 6,
        "A claim about who counts as a genuine practitioner, grounded in "
        "whether a teaching can account for all four ways of taking things "
        "personally — including taking a doctrine of self personally.",
        reader_title="Who Counts as a Genuine Practitioner?",
    ),
    "mn137": ReaderMeta(
        "Saḷāyatanavibhaṅga Sutta", 5, 7,
        "A technical analysis of the six fields of experience.",
        reader_title="The Six Fields of Experience",
    ),
    "mn141": ReaderMeta(
        "Saccavibhaṅga Sutta", 5, 8,
        "The four noble truths again, now in full analytical detail rather "
        "than the compressed form from Stage 2.",
        reader_title="The Four Truths in Detail",
    ),
    "mn117": ReaderMeta(
        "Mahācattārīsaka Sutta", 5, 9,
        "A technical analysis of the eightfold path, factor by factor.",
        reader_title="The Eightfold Path in Detail",
    ),
    "an6_63": ReaderMeta(
        "Nibbedhika Sutta", 5, 10,
        "One analytical frame applied six times over, to sensuality, feeling, "
        "recognition, the outflows, action, and dissatisfaction. Includes the "
        "line that defines action as intention.",
        reader_title="Six Things Examined",
    ),
    "sn35_28": ReaderMeta(
        "Āditta Sutta", 5, 11,
        "The fire sermon. Iconic imagery carrying a genuinely abstract point "
        "about the senses.",
        reader_title="The Fire Sermon",
    ),
    "mn18": ReaderMeta(
        "Madhupiṇḍika Sutta", 5, 12,
        "The honey-ball sutta, on how recognition snowballs into proliferating "
        "thought. Famously dense even by this collection's standards.",
        reader_title="How Thought Snowballs",
    ),
    "mn99": ReaderMeta(
        "Subha Sutta", 5, 13,
        "A dialogue defending renunciant life against a brahmin's claim that "
        "household life is better. Good late-stage read for weighing the whole "
        "path against the alternative.",
        reader_title="Household Life or Renunciant Life?",
    ),
    "mn1": ReaderMeta(
        "Mūlapariyāya Sutta", 5, 14,
        "\"The root of all things.\" Traditionally regarded as one of the most "
        "difficult texts in the collection. Deliberately last: it rewards "
        "everything that came before it and rewards very little read cold.",
        reader_title="The Root of All Things",
    ),
    "iti44": ReaderMeta(
        "Nibbānadhātu Sutta", 5, 15,
        "A short reference text defining the two nibbāna elements. Read it "
        "for one distinction: what has already happened to a living arahant's "
        "mind, and what happens to everything they feel.",
        reader_title="The Two Nibbāna Elements",
    ),
}


# Discovery metadata is intentionally expressed as named groups rather than as
# free-form tags copied into forty-eight records.  That keeps the public filter
# vocabulary small, makes omissions testable, and lets one surface appear under
# more than one useful reader question.
TOPIC_GROUPS: dict[str, tuple[str, ...]] = {
    "Getting started": (
        "an3_65", "sn45_2", "mn63", "mn26", "an2_9",
    ),
    "Ethics and conduct": (
        "mn61", "mn7", "mn39", "dn2", "mn99", "an4_113", "mn11",
        "an2_9", "an3_69", "an4_5",
    ),
    "Meditation": (
        "mn19", "mn2", "mn118", "mn10", "dn2", "an10_60", "mn39",
        "sn46_51", "sn51_13", "sn48_10", "mn119",
    ),
    "Four truths and path": (
        "sn56_11", "sn36_6", "sn55_5", "an11_9", "mn9", "mn141",
        "mn117", "an6_63", "sn45_2", "an8_6", "an4_5", "sn1_1",
    ),
    "Not-self": (
        "sn22_59", "mn22", "sn22_48", "sn22_86", "sn22_89", "mn131",
        "mn148", "mn1", "iti44",
    ),
    "Dependent arising": (
        "sn12_15", "sn12_61", "sn12_23", "sn12_11", "sn12_2", "mn38",
        "dn15", "mn9",
    ),
    "Mind and senses": (
        "mn137", "sn35_28", "mn18", "mn43", "mn44", "mn64", "mn148",
        "mn38", "an8_6", "an3_69", "sn1_1",
    ),
}

FORM_GROUPS: dict[str, tuple[str, ...]] = {
    "Dialogue": (
        "an3_65", "mn63", "mn26", "mn61", "dn2", "mn44", "mn43",
        "mn64", "mn99", "mn18", "mn38", "sn22_86", "sn22_89",
        "sn12_15", "sn45_2", "sn1_1",
    ),
    "Practice instructions": (
        "mn2", "mn10", "mn118", "mn19", "mn39", "an10_60", "sn46_51",
        "sn51_13", "sn48_10", "mn119",
    ),
    "Analysis": (
        "mn9", "mn117", "mn137", "mn141", "mn148", "sn12_2",
        "sn22_48", "an6_63", "dn15",
    ),
    "Teaching with verse": (
        "mn131", "iti44", "an11_9", "an8_6", "an4_5",
    ),
}

DIFFICULTY_BY_STAGE: dict[int, str] = {
    1: "Introductory",
    2: "Introductory",
    3: "Practical",
    4: "Intermediate",
    5: "Advanced",
}


def reader_topics(surface: TranslationSurface) -> tuple[str, ...]:
    """Curated public topics for one surface, in display order."""
    return tuple(
        topic for topic, keys in TOPIC_GROUPS.items() if surface.key in keys
    )


def reader_form(surface: TranslationSurface) -> str:
    """The surface's dominant literary form for reader discovery."""
    for form, keys in FORM_GROUPS.items():
        if surface.key in keys:
            return form
    return "Teaching"


def reader_difficulty(surface: TranslationSurface) -> str:
    """A plain orientation label derived from the governed reading stage."""
    return DIFFICULTY_BY_STAGE[reader_meta(surface).stage]


def canonical_reference(surface: TranslationSurface) -> str:
    """SuttaCentral UID derived from a display reference such as `SN 22.86`."""
    return surface.label.casefold().replace(" ", "")


def canonical_pali_url(surface: TranslationSurface) -> str:
    """Canonical Mahāsaṅgīti Pali source used by the translation workflow."""
    return f"https://suttacentral.net/{canonical_reference(surface)}/pli/ms"


def reader_meta(surface: TranslationSurface) -> ReaderMeta:
    """The reader metadata for a surface. Every surface must have one."""
    return READER_METADATA[surface.key]


def reader_slug(surface: TranslationSurface) -> str:
    """The reader page filename for a surface, without the directory."""
    return surface.main_name


def display_title(surface: TranslationSurface) -> str:
    """The title shown to readers: the reader title if there is one."""
    meta = reader_meta(surface)
    return meta.reader_title or f"{surface.label}: {meta.pali_title}"


def surfaces_in_reading_order() -> tuple[TranslationSurface, ...]:
    """Every surface, ordered by reading stage then position within it."""
    by_key = {s.key: s for s in TRANSLATION_SURFACES}
    ordered = sorted(
        READER_METADATA.items(), key=lambda kv: (kv[1].stage, kv[1].order)
    )
    return tuple(by_key[key] for key, _ in ordered)

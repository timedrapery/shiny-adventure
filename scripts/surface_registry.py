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
        key="mn36",
        label="MN 36",
        main_relpath="docs/translations/mn36-mahasaccaka-sutta.md",
        notes_relpath="docs/translations/mn36-mahasaccaka-sutta-notes.md",
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
        key="mn113",
        label="MN 113",
        main_relpath="docs/translations/mn113-sappurisa-sutta.md",
        notes_relpath="docs/translations/mn113-sappurisa-sutta-notes.md",
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
        key="mn121",
        label="MN 121",
        main_relpath="docs/translations/mn121-culasunnata-sutta.md",
        notes_relpath="docs/translations/mn121-culasunnata-sutta-notes.md",
    ),
    TranslationSurface(
        key="mn122",
        label="MN 122",
        main_relpath="docs/translations/mn122-mahasunnata-sutta.md",
        notes_relpath="docs/translations/mn122-mahasunnata-sutta-notes.md",
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
        key="sn12_44",
        label="SN 12.44",
        main_relpath="docs/translations/sn12-44-loka-sutta.md",
        notes_relpath="docs/translations/sn12-44-loka-sutta-notes.md",
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
        key="sn12_20",
        label="SN 12.20",
        main_relpath="docs/translations/sn12-20-paccaya-sutta.md",
        notes_relpath="docs/translations/sn12-20-paccaya-sutta-notes.md",
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
        key="sn56_17",
        label="SN 56.17",
        main_relpath="docs/translations/sn56-17-avijja-sutta.md",
        notes_relpath="docs/translations/sn56-17-avijja-sutta-notes.md",
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
        key="sn22_22",
        label="SN 22.22",
        main_relpath="docs/translations/sn22-22-bhara-sutta.md",
        notes_relpath="docs/translations/sn22-22-bhara-sutta-notes.md",
    ),
    TranslationSurface(
        key="sn22_26",
        label="SN 22.26",
        main_relpath="docs/translations/sn22-26-assada-sutta.md",
        notes_relpath="docs/translations/sn22-26-assada-sutta-notes.md",
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
        key="sn45_8",
        label="SN 45.8",
        main_relpath="docs/translations/sn45-8-vibhanga-sutta.md",
        notes_relpath="docs/translations/sn45-8-vibhanga-sutta-notes.md",
    ),
    TranslationSurface(
        key="sn36_6",
        label="SN 36.6",
        main_relpath="docs/translations/sn36-6-salla-sutta.md",
        notes_relpath="docs/translations/sn36-6-salla-sutta-notes.md",
    ),
    TranslationSurface(
        key="sn46_1",
        label="SN 46.1",
        main_relpath="docs/translations/sn46-1-himavanta-sutta.md",
        notes_relpath="docs/translations/sn46-1-himavanta-sutta-notes.md",
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
        key="an6_19",
        label="AN 6.19",
        main_relpath="docs/translations/an6-19-maranassati-sutta.md",
        notes_relpath="docs/translations/an6-19-maranassati-sutta-notes.md",
    ),
    TranslationSurface(
        key="an5_14",
        label="AN 5.14",
        main_relpath="docs/translations/an5-14-vitthata-sutta.md",
        notes_relpath="docs/translations/an5-14-vitthata-sutta-notes.md",
    ),
    TranslationSurface(
        key="an3_136",
        label="AN 3.136",
        main_relpath="docs/translations/an3-136-uppada-sutta.md",
        notes_relpath="docs/translations/an3-136-uppada-sutta-notes.md",
    ),
    TranslationSurface(
        key="an3_69",
        label="AN 3.69",
        main_relpath="docs/translations/an3-69-akusalamula-sutta.md",
        notes_relpath="docs/translations/an3-69-akusalamula-sutta-notes.md",
    ),
    TranslationSurface(
        key="an3_88",
        label="AN 3.88",
        main_relpath="docs/translations/an3-88-tatiyasikkha-sutta.md",
        notes_relpath="docs/translations/an3-88-tatiyasikkha-sutta-notes.md",
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
        key="an8_39",
        label="AN 8.39",
        main_relpath="docs/translations/an8-39-abhisanda-sutta.md",
        notes_relpath="docs/translations/an8-39-abhisanda-sutta-notes.md",
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
        key="an11_12",
        label="AN 11.12",
        main_relpath="docs/translations/an11-12-dutiyamahanama-sutta.md",
        notes_relpath="docs/translations/an11-12-dutiyamahanama-sutta-notes.md",
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
    TranslationSurface(
        key="ud8_3",
        label="Ud 8.3",
        main_relpath="docs/translations/ud8-3-tatiyanibbanapatisamyutta-sutta.md",
        notes_relpath="docs/translations/ud8-3-tatiyanibbanapatisamyutta-sutta-notes.md",
    ),
    TranslationSurface(
        key="iti49",
        label="Iti 49",
        main_relpath="docs/translations/iti49-ditthigata-sutta.md",
        notes_relpath="docs/translations/iti49-ditthigata-sutta-notes.md",
    ),
    TranslationSurface(
        key="dhp21_32",
        label="Dhp 21-32",
        main_relpath="docs/translations/dhp21-32-appamadavagga.md",
        notes_relpath="docs/translations/dhp21-32-appamadavagga-notes.md",
    ),
    TranslationSurface(
        key="an8_54",
        label="AN 8.54",
        main_relpath="docs/translations/an8-54-dighajanu-sutta.md",
        notes_relpath="docs/translations/an8-54-dighajanu-sutta-notes.md",
    ),
    TranslationSurface(
        key="an8_41",
        label="AN 8.41",
        main_relpath="docs/translations/an8-41-sankhittuposatha-sutta.md",
        notes_relpath="docs/translations/an8-41-sankhittuposatha-sutta-notes.md",
    ),
    TranslationSurface(
        key="snp1_8",
        label="Snp 1.8",
        main_relpath="docs/translations/snp1-8-metta-sutta.md",
        notes_relpath="docs/translations/snp1-8-metta-sutta-notes.md",
    ),
    TranslationSurface(
        key="dhp179_196",
        label="Dhp 179-196",
        main_relpath="docs/translations/dhp179-196-buddhavagga.md",
        notes_relpath="docs/translations/dhp179-196-buddhavagga-notes.md",
    ),
    TranslationSurface(
        key="dhp273_289",
        label="Dhp 273-289",
        main_relpath="docs/translations/dhp273-289-maggavagga.md",
        notes_relpath="docs/translations/dhp273-289-maggavagga-notes.md",
    ),
)


READABILITY_BODY_SHA256: dict[str, str] = {
    "mn113": "92e65f00bb8f1bb6000278d988c3132b96f382411fcbec3cc7a379d39ac688ab",
    "an8_54": "25fa010bbc6ec8ccacddb04828bdf1d823cbe5415df523f816fca1dfcee36fa2",
    "an8_41": "845ee70b4d28387a391db3e4f77432daee33b8658d26f32916932788cabaa83c",
    "snp1_8": "41bc1fb2b97f5db229624a6716c1d27b8d27808d9f55f7b7bc940aa3fcabf763",
    "dhp179_196": "35d74b3f9f89e92f87b2dbcac9f729951e38ecf10e5fc8cd88371853baff7c6a",
    "mn121": "7979493bb72d9f0baca8ff4658ff44d10fc5e4e531acec99b952c9102554789d",
    "an6_19": "8db14b637564e4746361b0c7b9880af71c5ce6564577adbb4bc8a5390b8d4b14",
    "dhp273_289": "16d60e08b3c3f0714f4681d8a2f633f4acd188e6a5fb6e7dca2b3495bb9567df",
    "an5_14": "c8b71291aafe6b6ae394cb4a0dfaa295c23d6b8688cbc60c52364fc9cb8dec2e",
    "an3_136": "e02e5035d59c9dfb3462d04accca32f2b9fbd631d71c80571a1c4e6b2bf87f4d",
    "mn1": "de3c8da710c0be78d19dab74616ce1ed6343982cd2d720d1fa89cc8fe7d44553",
    "mn2": "7b387b9585411d3f566918558b56459a0997702e5585a5f481e193b4881a5e44",
    "mn7": "e33d4501cc5764c896080a626a057bbce557c36e3a5d2e81e801839690d34ec2",
    "mn9": "5c31b105d41b34c9f76d4dc7e473c4382b6e1160d30af84fe44ac4cde72efbe3",
    "mn10": "75e03a8bd2796f152e2aa858a81426311bd2fcbfe2cd4c8df40ba36459b55b45",
    "mn11": "0cdf78600ada25558c9ebfe94f8f3d955b320fec2b6dc3ca11e12562283c0ae7",
    "mn18": "7a7dd6b91af02d2c11b138cd9935d0bb3e13e4ae4f57c9dd065d7d83fb92802e",
    "mn19": "be7796b474bcf43063c6a539ea646197db7a2b2f95006b9ad0eb9922c86b7227",
    "mn22": "f732679544986a626414b744a4348973c10055b40f7aa319306dabed312e4b06",
    "mn26": "fad88e4bd95c0667f0eb399e02777fb873d856943d059717e61f10398413a83b",
    "mn36": "474dba642b30650df556e45268e873ec0f481e7608c1d3ea495a7e52e973d3d0",
    "mn38": "689b67125860fb45ba2395ea2e4ddc14a9acacb17d3dceac65ee6569e4adde63",
    "mn39": "2c16fa7ff5e85c3b392bb29e014b65f0b2df9f3af0adf0bbd06af546d59d1da6",
    "mn43": "5619145e10c5906fe0336dd1861a29562be081a08879bd528d2c887fd0f88d89",
    "mn44": "331cdd147bbd7ee44d87bf9f02fc5951d2c286d70c94a1c170f8e727804a146c",
    "mn61": "218807c23d672ac40682951b9897d29be36049800ddb5c42f50d02817b1eacbc",
    "mn63": "efa71b5f46cb6b95f295add3aed4632b26baaa7d4eecc91e5f56529a9827583c",
    "mn64": "5dc4fca5dc726cd343d32ed75a40080f341fe7d7fc4e8bc8d63715f4d9db6417",
    "mn99": "d3899bf346d6961b8a3b656bc8057d10ce2e5467c7b4a4cc978093e158539d28",
    "mn117": "bff129d9662289a4df5b3f80907c0b0a83485895d65479550fa58a7f5b893f30",
    "mn118": "1f765b0431a91ca73b501bfc87dcfb658e8f31028a3b0077b6bd6ec660790e30",
    "mn122": "a17ddc965de1fbec8c227ef03ba0d07aa6dacb0c176a5560c65396120310b053",
    "mn119": "dfdbf65a89f1088cd7110ceb23ee8f7089ef30e3008ae4a43aa3b38c4bafd157",
    "mn131": "67d01f7421477463a394ca31c9cdfde9d3a9e5c02df3c3c3af105758879fb672",
    "mn137": "0af1fc42153eb60dd3a62dabf0b8435470d7fcdb33b833841172051b1bf7f7d2",
    "mn141": "4b7012b3429dc201c38c47c301070eb4f15803ac290e6502fa9824a2a6b20449",
    "mn148": "82fbe31e03d38c1c65dbd8281c44fb3a9aa5721fc29debfd6ad0ed31291a2730",
    "sn12_11": "5c398557b2b38955f9a9c1b605da04cc5aac408d5ef4c843aef9b1cafdfe1ad8",
    "sn12_61": "e6baa3440db183f95ae75032f41a2f1403e4917552dfc8a6ad4b03cf0c52289d",
    "sn12_15": "f4edd91be61c2e628c09ed7e4dca8dc7fd2933f5f69ad44544a6a8d7e4e12aaf",
    "sn12_44": "d96035f8601aebff22abc0d3471d2bd7c38014e0fafccf46fe07741136d206c7",
    "sn12_23": "8ca128e1a2e7cf0509365f80b95cc4a9aa894ba74238a5ddf6079547ad405c84",
    "sn12_2": "10524ad1c459d115191ebdbfdb3604872d118b9cf53a31d7e5a4728c0ba5a596",
    "sn12_20": "5e9d316330bb4e6f046f4df819f1a63fb2d748b4ab74cae805efb797aadd72c6",
    "sn51_13": "bcc9fa51a7c154ddb0b8116bff6eb71e19c74ff2c527402b53a9c855c9822048",
    "sn1_1": "88ae416984752a677d3ec1b16af2da325087413fa095f5ec493690da2a2beaa7",
    "sn55_5": "5572c6b6440b2e34b68f61e81192971002d15b8795cd2a90751b5588e4ffaf64",
    "sn56_11": "b7daaea35de198898414f52c4b8066f0b212301b53d48624d41e714f6faded45",
    "sn56_17": "eb7c6d437ff1752a470fdeea4c8167d9c9f8378e78c6d75e83b5d758db077835",
    "sn22_59": "5930c6f6002ce701ce478afa5c118259b6f7f5279e788bdf14e6a0e0e1792c1c",
    "sn22_48": "fb38ded19ba1ca7f34b49d5c30465237d03d5aff7aced3a501743ab223a04d61",
    "sn22_22": "b7f1f96aeca0d4fe6ad3ee18eb184632c382ee7f04e4706a69e4d30558d74ddd",
    "sn22_26": "ac14ba830a1faf02eddf5b50f4a1ea9a777dd9e5d67d857733135806dbcf0fe7",
    "dhp21_32": "49f334a4480939df786153a07bdb084f5a2143934d772516c66baba38fe807c4",
    "sn22_89": "5576eb92bb12962fd92605a1d7bc28071d300d2ce207eb766bb700d73914a1b0",
    "sn22_86": "35d9b785e82161ce72bcd4d2c8cf709815f0e14720fddaf499b9d3c5acfdc699",
    "sn35_28": "417a6e30521efb4c9b22d2addf3311ef30bee30c6e780581fdf1cce6e2d1fd7b",
    "sn45_2": "cab859023c9c9e40ce176d8207f828a66b3bf5251c802f7484597e15c753ccfc",
    "sn45_8": "d1d6cc56cefa6fc87570c23003c3f7c0d4dcbc119f1e41ad3b726a13e6dfa511",
    "sn36_6": "19c36b08d2e8dd0fde0087a3c5ffd93de62de453535b44a416169796248fd569",
    "sn46_1": "84d634d705f8092eb678e81deda93826db5f810b8d54299b801125bf0d127a9f",
    "sn46_51": "996f341d677fc2a93f203b9419dbf1e44c0dc2de700357f9e82d311a98ea9a87",
    "sn48_10": "546fc20edaa828485f4c5ebf0e120a4536a9cce52d0713b491508b8368a69cc7",
    "an2_9": "b5c2faee1db36d2fd41866fda2422e1258649b9d621a8ccfcc9746faea5d4790",
    "an3_65": "e6aceddf78a3d2b0361438aca13cd83bff9088367722eb2244aa5680b4cbeb6d",
    "an3_69": "70ab99be572724b9051681ae7a8525b99dc129c518dbacf37dace77488aa0e44",
    "an3_88": "462c5d1ef734fa32796158af0185d44e2a016897a284b8e29520a21c78bd2865",
    "an4_5": "42417d4a25fecfeb9bafa28af0923804f2cf9fa9235f9fbb97ad298761d982d8",
    "an4_113": "5b174ac0addaa28cc8293860070f9ccfc709fab9c79882399e255f43c0565eec",
    "an6_63": "4f0c7aaedac4b39d1c5a883ebf144cd4e3c375368a40edb5d5810e5b40400209",
    "an8_6": "3a757a0765f5aab18f1086ae6dcfdef72669b2e1ae63a44870f56858eb6ed0e0",
    "an10_60": "dfa291050a0a8e5a5e61b7859fb3189417aba575029a9f4fab49ff925297ed6e",
    "an11_9": "68e0a02f93bf51d72194c42dc60d6e2f7e703e58642ee5a8750cb81049fe7cb9",
    "an8_39": "a11ba7de50b051609e12ae7fb28bf71b3fda14609ea980bedb336bfc2998ad16",
    "an11_12": "fae0dd24a101f9a3a8c3673a177e7d032dc046178d308f1ccc3df50be1652b1d",
    "dn2": "ca0319f99fb06f8046969005552e19987a1a656ee870637c12be5f3d62448d94",
    "dn15": "1924f2a37620922a7ed1fa046d762b459f782ad7b33e3b88f935939645aef731",
    "iti44": "f767898d2afd2f9cef53e9fbf4414a6f2cee52553aa32390d14eafc7c2ecbe8d",
    "ud8_3": "69dcf68d448d22ef132e026a169e4019c7a8cbaad5c31ff7534bc8cfd7818ef3",
    "iti49": "d848f1253c59708156f051c256560ec8f67148a0939867d26e8feebdba5814ca",
}

READABILITY_REVIEWED_ON: dict[str, str] = {
    "mn113": "2026-11-09",
    "an8_54": "2026-11-09",
    "an8_41": "2026-11-09",
    "snp1_8": "2026-11-09",
    "dhp179_196": "2026-11-09",
    "mn121": "2026-11-09",
    "an6_19": "2026-11-09",
    "dhp273_289": "2026-11-09",
    "an5_14": "2026-11-09",
    "an3_136": "2026-11-09",
    "mn122": "2026-11-09",
    "sn22_26": "2026-11-09",
    "dhp21_32": "2026-11-09",
    "sn22_22": "2026-11-08",
    # Body re-touched for the samādhi / nīvaraṇa ruling (composure -> unification
    # of mind, distraction -> hindrance, and the five hindrance names), 2026-11-08.
    "mn64": "2026-11-08",
    "an3_65": "2026-11-08",
    "an11_9": "2026-11-08",
    "mn2": "2026-11-08",
    "mn7": "2026-11-08",
    "mn9": "2026-11-08",
    "mn10": "2026-11-08",
    "mn19": "2026-11-08",
    "mn26": "2026-11-08",
    "mn36": "2026-11-08",
    "mn38": "2026-11-08",
    "mn39": "2026-11-08",
    "mn43": "2026-11-08",
    "mn44": "2026-11-08",
    "mn99": "2026-11-08",
    "mn117": "2026-11-08",
    "mn118": "2026-11-08",
    "mn119": "2026-11-08",
    "mn141": "2026-11-08",
    "sn12_23": "2026-11-08",
    "sn51_13": "2026-11-08",
    "sn55_5": "2026-11-08",
    "sn56_11": "2026-11-08",
    "sn45_2": "2026-11-08",
    "sn45_8": "2026-11-08",
    "sn46_1": "2026-11-08",
    "sn46_51": "2026-11-08",
    "sn48_10": "2026-11-08",
    "an3_88": "2026-11-08",
    "an4_5": "2026-11-08",
    "an6_63": "2026-11-08",
    "an10_60": "2026-11-08",
    "an11_12": "2026-11-08",
    "dn2": "2026-11-08",
    # Body re-touched for the saññā-compound ruling (perception -> recognition).
    "an2_9": "2026-08-24",
    "an3_69": "2026-08-24",
    "sn1_1": "2026-08-24",
    "mn131": "2026-08-24",
    "sn22_86": "2026-08-24",
    "an8_6": "2026-08-24",
    "mn137": "2026-08-24",
    "sn12_15": "2026-08-24",
    "sn12_44": "2026-08-25",
    "sn56_17": "2026-08-25",
    "iti49": "2026-08-25",
    "sn12_20": "2026-08-27",
    "an8_39": "2026-09-13",
    "ud8_3": "2026-09-13",
    # Bodies re-touched for the `moghapurisa` ruling (misguided/foolish man ->
    # stupid man, and `misguided persons` -> `stupid persons` in MN 22).
    "mn22": "2026-09-15",
    "mn63": "2026-09-15",
}

# Surfaces that have cleared all three human evidence gates. A surface is
# listed here only once `reviews/newcomer-review-ledger.json` carries the
# evidence for the *current* body: `scripts/check_newcomer_reviews.py` fails
# if this map and the ledger disagree in either direction, so promotion is a
# two-key operation rather than a line edit.
READABILITY_STATUS: dict[str, str] = {}

TRANSLATION_SURFACES = tuple(
    replace(
        surface,
        readability_review=ReadabilityReview(
            standard="plain-english-v1",
            status=READABILITY_STATUS.get(surface.key, "provisional"),
            reviewed_on=READABILITY_REVIEWED_ON.get(surface.key, "2026-08-23"),
            body_sha256=READABILITY_BODY_SHA256[surface.key],
        ),
    )
    for surface in TRANSLATION_SURFACES
)


# Generated docs that are not cluster surfaces. These are freshness-enforced
# like the cluster reports, but they are deliberately kept out of
# CLUSTER_SURFACES so `scripts/check_cluster_surfaces.py` does not demand an
# authority document for them and `run_checks.py` does not run them in strict
# family mode. They report on the repository rather than governing a doctrinal
# family.
NON_CLUSTER_GENERATED_SURFACES: tuple[ClusterSurface, ...] = (
    ClusterSurface(
        key="health_dashboard",
        label="Editorial health dashboard",
        doc_relpath="docs/generated/health-dashboard.md",
        script_relpath="scripts/health_dashboard.py",
        test_relpaths=("tests/test_health_dashboard.py",),
    ),
    ClusterSurface(
        key="next_sutta_priority",
        label="Next-sutta priority table",
        doc_relpath="docs/generated/next-sutta-priority-table.md",
        script_relpath="scripts/next_sutta_priority_report.py",
        test_relpaths=("tests/test_next_sutta_priority_report.py",),
    ),
)


def generated_surface_groups() -> tuple[ClusterSurface, ...]:
    """Return the CI-enforced generated doc groups backed by report scripts."""

    return CLUSTER_SURFACES + NON_CLUSTER_GENERATED_SURFACES


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

# The deliberately small, newcomer-tested front door to the full corpus.
# This order is independent of both canonical order and the five-stage reading
# path: it starts with short, recognizable teachings before asking a new reader
# to take on the longer foundational texts.
FIRST_TWELVE: tuple[str, ...] = (
    "an2_9",
    "sn45_2",
    "sn56_17",
    "sn36_6",
    "an8_6",
    "an11_12",
    "an3_65",
    "mn63",
    "sn56_11",
    "sn22_59",
    "mn19",
    "sn12_44",
)

QUICK_START = "sn45_2"

# Short, human-centered ways into the First 12. A path may reuse a text from
# another path; the purpose is to answer the reader's present question, not to
# partition the corpus.
NEWCOMER_PATHWAYS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    (
        "I am curious but skeptical",
        "Begin with how to evaluate a teaching and why some questions are set aside.",
        ("an3_65", "mn63", "sn45_2"),
    ),
    (
        "I am dealing with stress or pain",
        "Start with pain, changing circumstances, and the practical meaning of ignorance.",
        ("sn36_6", "an8_6", "sn56_17"),
    ),
    (
        "I want something practical to try",
        "Begin with ethical awareness, everyday recollection, and training thought.",
        ("an2_9", "an11_12", "mn19"),
    ),
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
    "sn56_17": ReaderMeta(
        "Avijjā Sutta", 2, 2,
        "A bhikkhu asks what ignorance means. The answer is precise: not "
        "understanding dissatisfaction, where it comes from, how it ends, "
        "and the path that leads to its ending.",
        reader_title="What Ignorance Means",
    ),
    "an3_136": ReaderMeta(
        "Uppāda Sutta", 2, 3,
        "Three short claims about everything that has been put together, and "
        "a frame that says they hold whether or not a Buddha ever appears.",
        reader_title="True Whether or Not a Buddha Appears",
    ),
    "sn45_8": ReaderMeta(
        "Vibhaṅga Sutta", 2, 4,
        "The eightfold path unpacked one factor at a time: how to understand, "
        "speak, act, work, train, remember, and unify the heart.",
        reader_title="What the Eightfold Path Means",
    ),
    "an3_88": ReaderMeta(
        "Tatiyasikkhā Sutta", 2, 5,
        "More than 150 monastic rules gathered into three trainings—conduct, "
        "the mind, and discernment. Minor mistakes can be repaired, and even "
        "partial training still bears fruit.",
        reader_title="Three Trainings Cover Everything",
    ),
    "sn36_6": ReaderMeta(
        "Salla Sutta", 2, 6,
        "The one-arrow/two-arrows teaching: physical pain versus the added "
        "mental suffering piled on top of it. Concrete, bodily, and "
        "immediately recognizable.",
        reader_title="One Arrow, Not Two",
    ),
    "an8_6": ReaderMeta(
        "Dutiyalokadhamma Sutta", 2, 7,
        "Gain and loss, praise and blame, pleasure and pain happen to everyone. "
        "The difference is whether they take over the heart.",
        reader_title="When Life Goes Up and Down",
    ),
    "an2_9": ReaderMeta(
        "Cariya Sutta", 2, 8,
        "Two bright qualities protect the human world: conscience, the inward "
        "sense of integrity, and moral caution about harm and consequences.",
        reader_title="What Keeps the World Human",
    ),
    "an8_39": ReaderMeta(
        "Abhisanda Sutta", 2, 9,
        "Keeping the five precepts described from the other side: every being "
        "who might have been harmed is given freedom from fear, and the "
        "person who gave it comes to share in it.",
        reader_title="Eight Streams of Benefit",
    ),
    "mn7": ReaderMeta(
        "Vattha Sutta", 2, 10,
        "A mind is like cloth: dye it while it is dirty and the colour comes "
        "out wrong. Ethics introduced through a simile instead of a rule list.",
        reader_title="The Dirty Cloth",
    ),
    "snp1_8": ReaderMeta(
        "Metta Sutta", 2, 11,
        "Ten verses on friendliness: the character it starts from, the wish "
        "for all beings to be happy, and a mother's care for her only child.",
        reader_title="May All Beings Be Happy",
    ),
    "an8_41": ReaderMeta(
        "Saṅkhittūposatha Sutta", 2, 12,
        "The eight factors of the observance day: for one night and day, a lay "
        "disciple lives as the arahants live for life.",
        reader_title="Living Like an Arahant for a Day",
    ),
    "an8_54": ReaderMeta(
        "Dīghajāṇu Sutta", 2, 13,
        "A householder asks how to live well now and later. Four things for "
        "this life, four drains on wealth, and four things for the life to come.",
        reader_title="A Good Life Now and Later",
    ),
    "an3_69": ReaderMeta(
        "Akusalamūla Sutta", 2, 14,
        "Greed, aversion, and delusion are traced from their roots to their "
        "effects on action, speech, power, and the heart—then contrasted with "
        "non-greed, non-aversion, and clarity.",
        reader_title="What Drives Harm—and What Ends It",
    ),
    "an4_5": ReaderMeta(
        "Anusota Sutta", 2, 15,
        "Four ways of meeting the current: drifting with it, struggling "
        "against it, standing firm, and completing the crossing to dry land.",
        reader_title="Going With the Stream—or Against It",
    ),
    "sn1_1": ReaderMeta(
        "Oghataraṇa Sutta", 2, 16,
        "A deity asks how the Buddha crossed a flood. The answer refuses both "
        "standing still and forceful struggle, preserving a compact paradox.",
        reader_title="How Do You Cross the Flood?",
    ),
    "an4_113": ReaderMeta(
        "Patoda Sutta", 2, 17,
        "Four kinds of horses, four kinds of people, and what it actually takes "
        "to be moved to practice. A jolt of urgency after three fairly calm "
        "texts.",
        reader_title="Four Horses",
    ),
    "sn55_5": ReaderMeta(
        "Dutiyasāriputta Sutta", 2, 18,
        "What actually leads to the path, in four steps that are ordinary "
        "enough to follow: find good company, hear the teaching, attend to it "
        "carefully, then practise in line with it. The first item is social, "
        "not inward.",
        reader_title="Four Steps That Lead to the Path",
    ),
    "an11_9": ReaderMeta(
        "Saddha Sutta", 2, 19,
        "A wild colt tied to its trough can think of nothing but \"Fodder, "
        "fodder!\" The contrast with a trained horse becomes a contrast between "
        "two ways of sitting down to meditate.",
        reader_title="Think Like a Thoroughbred",
    ),
    "dhp21_32": ReaderMeta(
        "Appamādavagga", 2, 20,
        "Twelve verses on one quality: heedfulness, the path to the "
        "deathless. Short, memorable, and the first verse page in the set.",
        reader_title="Heedfulness Is the Path to the Deathless",
    ),
    "dhp273_289": ReaderMeta(
        "Maggavagga", 2, 21,
        "Seventeen verses on the path: you must make the effort yourself, and "
        "seeing impermanence, unsatisfactoriness, and not-self is the way.",
        reader_title="The Path",
    ),
    "dhp179_196": ReaderMeta(
        "Buddhavagga", 2, 22,
        "Eighteen verses on the Buddha, including the four-line summary of the "
        "whole teaching and what a real refuge is.",
        reader_title="The Teaching of the Buddhas",
    ),
    # Stage 3 -- Learning to Look at Your Own Mind
    "mn19": ReaderMeta(
        "Dvedhāvitakka Sutta", 3, 1,
        "Sorting thoughts into two bins and learning what to do with each. The "
        "simplest possible entry point into mind-training.",
        reader_title="Two Kinds of Thinking",
    ),
    "mn36": ReaderMeta(
        "Mahāsaccaka Sutta", 3, 2,
        "A debater says some people train the body and others the mind. The "
        "Buddha answers with his own story: two teachers, self-torment that "
        "nearly killed him, and the memory that pointed another way. Through "
        "all of it, neither pain nor pleasure took over his heart.",
        reader_title="Could This Be the Path to Awakening?",
    ),
    "mn61": ReaderMeta(
        "Ambalaṭṭhikarāhulovāda Sutta", 3, 3,
        "The Buddha teaches his own son Rāhula, using a water vessel emptied "
        "and turned upside down, then a war elephant, to make the case that "
        "someone who feels no shame lying has nothing left to hold them back. "
        "From there: a nine-part checklist for examining any action of body, "
        "speech, or mind before, during, and after doing it.",
        reader_title="The Water Vessel",
    ),
    "mn2": ReaderMeta(
        "Sabbāsava Sutta", 3, 4,
        "Seven concrete methods for handling what erodes the mind: restraint, "
        "use, endurance, avoidance, removal, development. A toolkit, not a "
        "theory.",
        reader_title="Seven Ways to Handle What Erodes the Mind",
    ),
    "an11_12": ReaderMeta(
        "Dutiyamahānāma Sutta", 3, 5,
        "Mahānāma asks how to practice in ordinary life while the Buddha "
        "is away. The answer gives five qualities to stand on and six things "
        "to remember while moving, working, or living with family.",
        reader_title="Six Things to Remember Anywhere",
    ),
    "mn118": ReaderMeta(
        "Ānāpānasati Sutta", 3, 6,
        "Step-by-step instructions for remembering the Dhamma while breathing "
        "in and out. The first text on this list that is a practice manual "
        "rather than a teaching about practice.",
        reader_title="Remembering the Dhamma While Breathing In and Out",
    ),
    "mn10": ReaderMeta(
        "Satipaṭṭhāna Sutta", 3, 7,
        "The four foundations of remembering, and the longest, densest text so "
        "far. Not really a one-sitting read: it is the reference manual for "
        "the pieces above, worth returning to rather than finishing.",
        reader_title="The Four Foundations of Remembering",
    ),
    "mn119": ReaderMeta(
        "Kāyagatāsati Sutta", 3, 8,
        "A long practice sequence directing remembering to breathing, movement, "
        "the body's contents and fate, deep unification of mind, resilience, "
        "and ten "
        "claimed results.",
        reader_title="Remembering Directed to the Body",
    ),
    "mn122": ReaderMeta(
        "Mahāsuññata Sutta", 3, 9,
        "The Buddha's own way of dwelling in emptiness, how to train toward "
        "it when the heart will not go there, and why a teacher who keeps "
        "correcting you is a friend.",
        reader_title="Dwelling in Emptiness",
    ),
    "mn121": ReaderMeta(
        "Cūḷasuññata Sutta", 3, 10,
        "Emptiness entered step by step: each time, notice what has dropped "
        "away and what remains, until only this living body is left.",
        reader_title="Emptiness, Step by Step",
    ),
    "dn2": ReaderMeta(
        "Sāmaññaphala Sutta", 3, 11,
        "A king asks what a renunciant actually gets out of the life. A full "
        "narrative walk through the gradual path from an outsider's curious, "
        "slightly skeptical point of view.",
        reader_title="What Does a Renunciant Gain?",
    ),
    "an10_60": ReaderMeta(
        "Girimānanda Sutta", 3, 12,
        "Ten recognitions taught to a sick monk. Practical and, unusually for "
        "this stage, comforting.",
        reader_title="Ten Recognitions for a Sick Monk",
    ),
    "an6_19": ReaderMeta(
        "Maraṇassati Sutta", 3, 13,
        "Six monks say how they recollect death, each with less time than the "
        "last. The Buddha sorts the heedless from the heedful.",
        reader_title="Recollecting Death, One Breath at a Time",
    ),
    "mn39": ReaderMeta(
        "Mahā-Assapura Sutta", 3, 14,
        "What actually makes someone a genuine renunciant, as opposed to "
        "someone who merely looks like one. Ethics and practice fused.",
        reader_title="What Makes a Genuine Renunciant?",
    ),
    "mn113": ReaderMeta(
        "Sappurisa Sutta", 3, 15,
        "Twenty-six things a monk might be proud of, from family to deep "
        "meditation, and how a good person refuses to rank themselves by them.",
        reader_title="The Good Person and the Bad Person",
    ),
    "sn46_51": ReaderMeta(
        "Āhāra Sutta", 3, 16,
        "What feeds the hindrances that block practice, and what starves "
        "them. A closing, practical text for this stage.",
        reader_title="What Feeds and Starves the Hindrances",
    ),
    "sn46_1": ReaderMeta(
        "Himavanta Sutta", 3, 17,
        "Nāgas grow big enough for the ocean by first growing on a mountain. "
        "Conduct is put in the mountain's place: it is what the seven "
        "awakening factors get large on.",
        reader_title="Conduct Is Where Practice Grows",
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
    "sn22_22": ReaderMeta(
        "Bhāra Sutta", 4, 4,
        "The five heaps as a burden, ignorant wanting as picking it up, and its "
        "fading as putting it down. The second and third truths in one image.",
        reader_title="Putting Down the Burden",
    ),
    "sn22_26": ReaderMeta(
        "Assāda Sutta", 4, 5,
        "Before his awakening, the Buddha asks three questions of each of the "
        "five heaps: what it offers, what is wrong with it, and the way out.",
        reader_title="What the Heaps Offer, and the Way Out",
    ),
    "sn22_86": ReaderMeta(
        "Anurādha Sutta", 4, 6,
        "Anurādha tries to place the Tathāgata outside four claims about what "
        "happens after death. The Buddha asks whether the Tathāgata can be "
        "pinned down through the five heaps even here and now.",
        reader_title="Can You Pin Down the Tathāgata?",
    ),
    "sn22_89": ReaderMeta(
        "Khemaka Sutta", 4, 7,
        "A subtler point: even someone who has genuinely seen not-self can "
        "still carry a faint, hard-to-locate sense of \"I am.\"",
        reader_title="The Lingering Sense of 'I Am'",
    ),
    "mn131": ReaderMeta(
        "Bhaddekaratta Sutta", 4, 8,
        "Do not chase the past or long for the future — but do not mistake "
        "that for a slogan about living in the moment. The explanation asks "
        "whether you are turning any part of present experience into self.",
        reader_title="Don't Chase the Past or Long for the Future",
    ),
    "mn148": ReaderMeta(
        "Chachakka Sutta", 4, 9,
        "A systematic, almost mechanical working-through of not-self across "
        "every sense door. Dense, but by this point the pattern should be "
        "familiar.",
        reader_title="Not-Self at the Six Sense Doors",
    ),
    "sn12_15": ReaderMeta(
        "Kaccānagotta Sutta", 4, 10,
        "One page, defining right view as the middle between \"it exists\" and "
        "\"it doesn't.\" The clearest, shortest bridge into dependent arising.",
        reader_title="Between 'It Exists' and 'It Doesn't'",
    ),
    "iti49": ReaderMeta(
        "Diṭṭhigata Sutta", 4, 11,
        "Two views can take over: clinging to continued becoming, or treating "
        "annihilation as peace. The alternative is to see what has come to be "
        "without turning it into something permanent.",
        reader_title="Taken Over by Views",
    ),
    "sn12_44": ReaderMeta(
        "Loka Sutta", 4, 12,
        "How the lived world develops through the six senses into wanting, "
        "taking experience personally, and dissatisfaction—and how that "
        "process ends without the senses having to disappear.",
        reader_title="How the World Arises—and Ends",
    ),
    "sn12_61": ReaderMeta(
        "Assutavā Sutta", 4, 13,
        "An argument that runs the opposite way from what you expect: if you "
        "must identify with something, the body is the safer choice, because "
        "its changing is visible and the mind's is not.",
        reader_title="Body and Mind Keep Changing",
    ),
    "sn12_23": ReaderMeta(
        "Upanisa Sutta", 4, 14,
        "The positive chain, dissatisfaction leading step by step to freedom, "
        "mirroring the well-known negative chain.",
        reader_title="From Dissatisfaction to Freedom",
    ),
    "sn12_11": ReaderMeta(
        "Āhāra Sutta", 4, 15,
        "Four things that keep a life going, traced back to wanting and then "
        "all the way back along the chain. Not to be confused with SN 46.51, "
        "which shares its name.",
        reader_title="What Keeps a Life Going",
    ),
    "sn12_2": ReaderMeta(
        "Paṭiccasamuppāda-vibhaṅga Sutta", 4, 16,
        "The standard formula of dependent arising, defined term by term.",
        reader_title="Dependent Arising, Term by Term",
    ),
    "sn12_20": ReaderMeta(
        "Paccaya Sutta", 4, 17,
        "Dependent arising stated as a pattern that holds whether or not "
        "anyone discovers it, kept carefully apart from the changing things "
        "the pattern runs through—and why someone who sees this stops "
        "interrogating their own past and future.",
        reader_title="Discovered, Not Invented",
    ),
    "mn38": ReaderMeta(
        "Mahātaṇhāsaṅkhaya Sutta", 4, 18,
        "A monk's wrong view — that the same consciousness travels on "
        "unchanged — gets corrected, and dependent arising gets restated in "
        "narrative, argued form rather than as a bare formula.",
        reader_title="Does the Same Consciousness Continue?",
    ),
    "dn15": ReaderMeta(
        "Mahānidāna Sutta", 4, 19,
        "The deepest and longest exposition of dependent arising in the set. "
        "The capstone of this stage, not an entry point to it.",
        reader_title="Dependent Arising in Depth",
    ),
    "mn9": ReaderMeta(
        "Sammādiṭṭhi Sutta", 4, 20,
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
        "see confidence, energy, remembering, unification of mind, and "
        "discernment "
        "treated as one set.",
        reader_title="The Five Faculties",
    ),
    "an5_14": ReaderMeta(
        "Vitthata Sutta", 5, 5,
        "The five strengths named and defined, in the same words SN 48.10 "
        "uses for the five faculties.",
        reader_title="The Five Strengths",
    ),
    "mn64": ReaderMeta(
        "Mahāmālukya Sutta", 5, 6,
        "The five lower fetters, and the companion piece to MN 63 — same "
        "disciple, later in his practice.",
        reader_title="The Five Lower Fetters",
    ),
    "mn11": ReaderMeta(
        "Cūḷasīhanāda Sutta", 5, 7,
        "A claim about who counts as a genuine practitioner, grounded in "
        "whether a teaching can account for all four ways of taking things "
        "personally — including taking a doctrine of self personally.",
        reader_title="Who Counts as a Genuine Practitioner?",
    ),
    "mn137": ReaderMeta(
        "Saḷāyatanavibhaṅga Sutta", 5, 8,
        "A technical analysis of the six fields of experience.",
        reader_title="The Six Fields of Experience",
    ),
    "mn141": ReaderMeta(
        "Saccavibhaṅga Sutta", 5, 9,
        "The four noble truths again, now in full analytical detail rather "
        "than the compressed form from Stage 2.",
        reader_title="The Four Truths in Detail",
    ),
    "mn117": ReaderMeta(
        "Mahācattārīsaka Sutta", 5, 10,
        "A technical analysis of the eightfold path, factor by factor.",
        reader_title="The Eightfold Path in Detail",
    ),
    "an6_63": ReaderMeta(
        "Nibbedhika Sutta", 5, 11,
        "One analytical frame applied six times over, to sensuality, feeling, "
        "recognition, the outflows, action, and dissatisfaction. Includes the "
        "line that defines action as intention.",
        reader_title="Six Things Examined",
    ),
    "sn35_28": ReaderMeta(
        "Āditta Sutta", 5, 12,
        "The fire sermon. Iconic imagery carrying a genuinely abstract point "
        "about the senses.",
        reader_title="The Fire Sermon",
    ),
    "mn18": ReaderMeta(
        "Madhupiṇḍika Sutta", 5, 13,
        "The honey-ball sutta, on how recognition snowballs into proliferating "
        "thought. Famously dense even by this collection's standards.",
        reader_title="How Thought Snowballs",
    ),
    "mn99": ReaderMeta(
        "Subha Sutta", 5, 14,
        "A dialogue defending renunciant life against a brahmin's claim that "
        "household life is better. Good late-stage read for weighing the whole "
        "path against the alternative.",
        reader_title="Household Life or Renunciant Life?",
    ),
    "mn1": ReaderMeta(
        "Mūlapariyāya Sutta", 5, 15,
        "\"The root of all things.\" Traditionally regarded as one of the most "
        "difficult texts in the collection. Deliberately last: it rewards "
        "everything that came before it and rewards very little read cold.",
        reader_title="The Root of All Things",
    ),
    "iti44": ReaderMeta(
        "Nibbānadhātu Sutta", 5, 16,
        "A short reference text defining the two nibbāna elements. Read it "
        "for one distinction: what has already happened to a living arahant's "
        "mind, and what happens to everything they feel.",
        reader_title="The Two Nibbāna Elements",
    ),
    "ud8_3": ReaderMeta(
        "Tatiyanibbānapaṭisaṁyutta Sutta", 5, 17,
        "One minute, and one argument: there would be no way out of what is "
        "born, made and conditioned unless there were something that is not. "
        "It says that there is, and nothing more about it.",
        reader_title="Why There Is a Way Out",
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
        "an2_9", "an3_69", "an4_5", "an8_39", "sn46_1", "snp1_8", "an8_41", "an8_54", "mn113",
    ),
    "Meditation": (
        "mn19", "mn2", "mn118", "mn10", "dn2", "an10_60", "mn39",
        "sn46_51", "sn46_1", "sn51_13", "sn48_10", "mn119", "an11_12",
        "mn36", "mn122", "an5_14", "an6_19", "mn121", "snp1_8",
    ),
    "Four truths and path": (
        "sn56_11", "sn56_17", "sn36_6", "sn55_5", "an11_9", "mn9", "mn141",
        "mn117", "an6_63", "sn45_2", "sn45_8", "an8_6", "an4_5", "sn1_1",
        "an3_88", "ud8_3", "dhp21_32", "an3_136", "dhp273_289", "dhp179_196",
    ),
    "Not-self": (
        "sn22_59", "mn22", "sn22_48", "sn22_22", "sn22_26", "sn22_86",
        "sn22_89", "an3_136",
        "mn131", "mn148", "mn1", "iti44", "iti49",
    ),
    "Dependent arising": (
        "sn12_15", "sn12_44", "sn12_61", "sn12_23", "sn12_11",
        "sn12_2", "sn12_20", "mn38", "dn15", "mn9", "iti49",
    ),
    "Mind and senses": (
        "mn137", "sn35_28", "mn18", "mn43", "mn44", "mn64", "mn148",
        "mn38", "sn12_44", "an8_6", "an3_69", "sn1_1", "an11_12",
    ),
}

FORM_GROUPS: dict[str, tuple[str, ...]] = {
    "Dialogue": (
        "an3_65", "mn63", "mn26", "mn61", "dn2", "mn44", "mn43",
        "mn64", "mn99", "mn18", "mn38", "sn22_86", "sn22_89",
        "sn12_15", "sn45_2", "sn1_1", "sn56_17", "mn36",
    ),
    "Practice instructions": (
        "mn2", "mn10", "mn118", "mn19", "mn39", "an10_60", "sn46_51",
        "sn46_1",
        "sn51_13", "sn48_10", "mn119", "an11_12", "mn122", "an5_14", "an6_19", "mn121", "an8_41",
    ),
    "Analysis": (
        "mn9", "mn117", "mn137", "mn141", "mn148", "sn12_2",
        "sn12_20", "sn22_48", "sn22_26", "sn45_8", "sn12_44", "an6_63", "dn15",
    ),
    "Teaching with verse": (
        "mn131", "iti44", "iti49", "an11_9", "an8_6", "an4_5", "sn22_22",
        "dhp21_32", "dhp273_289", "dhp179_196", "snp1_8",
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

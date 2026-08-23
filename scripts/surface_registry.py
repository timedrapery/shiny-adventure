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
        key="sn35_28",
        label="SN 35.28",
        main_relpath="docs/translations/sn35-28-aditta-sutta.md",
        notes_relpath="docs/translations/sn35-28-aditta-sutta-notes.md",
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
        key="an3_65",
        label="AN 3.65",
        main_relpath="docs/translations/an3-65-kesamutta-sutta.md",
        notes_relpath="docs/translations/an3-65-kesamutta-sutta-notes.md",
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
    "mn2": "3db7bb2ac46537fe306f7c750f39d96139271be740fb9291573f022d495f7bc8",
    "mn7": "6bdfe1732b54248ac9bbb316665b06fbef587c2b669819978d33c84e172a9bc5",
    "mn9": "1adaab28e55052714021b36963f0002992f9b11fa9c8791a61651ee6955f4985",
    "mn10": "9a06b71b31cd2c746a97a01a59c6dac5d7b86bdeae4a7be6ab7f46f611eafbb9",
    "mn11": "1b8811594f7e00ed3f54d8d1ffc9ecf3b9ff2c21dc92d0ecd41b0e2ab1dae761",
    "mn18": "7a7dd6b91af02d2c11b138cd9935d0bb3e13e4ae4f57c9dd065d7d83fb92802e",
    "mn19": "5b9f00a388ed022641a5d8fb266c4894e1131aa9a5fe585de42af6db8cc6963d",
    "mn22": "e6ca1e27798c4cfb4c4411831fd2c71a72bf838ed3a473b2db69d8a75da9bbb3",
    "mn26": "4b0598934de27de9670e52c934cc6fee3552c3a6b97dc7c23a017443a0918971",
    "mn38": "643b40254ac9970f39dbbffce8d7515f9350d277885c0646e091adb0320d73dc",
    "mn39": "bf6a34706fd6bc69854bc10c411a6afdb852dfadddf0384e86d9570edde88205",
    "mn43": "217f3fbc5d8743e300fbb833c399e2a19f4f33d819e04e1b8365b2df8bc86ea2",
    "mn44": "ca53a52751ee580ce35acbca2bfa7d2e033e1aa754dafaa9010df87f2ad9b18b",
    "mn61": "6224dad79a4f97b99992407ea1f63f333370bf81f986706de44f243395a4ff25",
    "mn63": "24d4fdba2728415fb92c273deb97d17e189841c8a0927516a4b2a62d712bf946",
    "mn64": "d185b589c4e097b86e2a533db738a36c097a0e02f31e826e4273f99c0a7a2cfc",
    "mn99": "df265af3b80bee9d56935b188bb07c2b83f5b0be1502370ded55720632acf847",
    "mn117": "6fc4e6dad5d739f92e281e642e8b046a4c358b9f3cfd3e22055dc9bb9f4dca3f",
    "mn118": "b882e148df56f98ff6378f5f68e7ce38f6fe5417d14929461927c72cb703397f",
    "mn137": "0d52c976e54168c4bc1401b65fb7d03022317e96c1f5555ebf0c4df648622ccb",
    "mn141": "011df1083e53b454b2e84c2a659b087ca9ec2d748ae6f3baa3c1b2a101e25d8d",
    "mn148": "cc80f649865587452fd0a52fd39ecd47ea518bb3b34c36e9203c8ac27f5407c1",
    "sn12_11": "1e477e680b47e78332c3a7a6b0168aa0b0801d4ff6a4b9c9a6e15da921b5f522",
    "sn12_61": "19eae4ff65bda3f47787e1c84621a25d0904ad6bbdac23ad4ffd92711f5082cb",
    "sn12_15": "12967655fb0abb09953d69070d171a4a47bb95877c356a0ae0c6bf6dd8bfbb8c",
    "sn12_23": "2c2f48345aaea34edc489a04ca3a56e963f91d7ce2216f1a67f57482b282de1a",
    "sn12_2": "29ceade9662e6be88c86dad8995040ffd62a12158f544959b605b79ccbddaa83",
    "sn51_13": "870c81ac319f5b86848ae1184f16e5160ac28e355ab83735acf5a77bf5261341",
    "sn55_5": "8aaeed7d9768d97f2fcf3838ab798e9609c1243977ad28ada1149883fc0c0672",
    "sn56_11": "8263ffa4b2f4236f464e1f22ffded02d95dd16fa65092b33029ad8123e9581b3",
    "sn22_59": "5930c6f6002ce701ce478afa5c118259b6f7f5279e788bdf14e6a0e0e1792c1c",
    "sn22_48": "b5ac6f591e4b8d397e205f8cae8b75629c974c4e9e0d84a7b9b3d1b808a5b49f",
    "sn22_89": "5576eb92bb12962fd92605a1d7bc28071d300d2ce207eb766bb700d73914a1b0",
    "sn35_28": "2392364c6a47b71dbbd4a21bc8593e612b7c169080c60c009d04bac82b07ac9f",
    "sn36_6": "39cd01829b1062587bee1568c8f3f2bcc8de13c9fd50f834da804bcdcc08b1d6",
    "sn46_51": "f897531d01d27cb3428efeb9fdceb1ed4425ac08e977cced56ee85c839c0e927",
    "sn48_10": "6427267dc6dfabc8a46b537dbce6a67776ca52c5d12d078d6c2ae666fac47594",
    "an3_65": "44d2b4b891a50e11a1c4b5eedb5aed65837b4f64f4c41a62503f75b7bd870956",
    "an4_113": "fcd415f18a8c6738f548ff4eaa1733bebe4b850e6f50e4787527ed2e2a08a166",
    "an6_63": "685e9cdbcb056ead938635e310292b4dd3f25ead2f335cd24f3588d575276f87",
    "an10_60": "2ea40997cdfcc07157ec132ea7330f65f38202b6c6df16c8104f12a1a6bed78e",
    "an11_9": "e386de70be3267ede96f43880b8c95772dba20ebaa1471b07cee783599cff4c3",
    "dn2": "9d31e1bd2ceef134d94832ad6850d431965e05f4f45615d262ba0b76b8d07b20",
    "dn15": "8461edc9ebaee7f98b372823f02660f84fba4534308cc3b74f3f17922f37c9f1",
    "iti44": "cd8889506ec57be7071869300e6fe09a515ad7a982afcf7e9591eb6afd1da884",
}

TRANSLATION_SURFACES = tuple(
    replace(
        surface,
        readability_review=ReadabilityReview(
            standard="plain-english-v1",
            status="provisional",
            reviewed_on="2026-08-22",
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
    "mn63": ReaderMeta(
        "Cūḷamālukya Sutta", 1, 2,
        "Why the teaching refuses to answer certain metaphysical questions. "
        "Directly answers the objection a skeptical reader will already be "
        "forming after the first text.",
        reader_title="The Man Struck by a Poisoned Arrow",
    ),
    "mn26": ReaderMeta(
        "Pāsarāsi Sutta", 1, 3,
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
    "mn7": ReaderMeta(
        "Vattha Sutta", 2, 3,
        "A mind is like cloth: dye it while it is dirty and the colour comes "
        "out wrong. Ethics introduced through a simile instead of a rule list.",
        reader_title="The Dirty Cloth",
    ),
    "an4_113": ReaderMeta(
        "Patoda Sutta", 2, 4,
        "Four kinds of horses, four kinds of people, and what it actually takes "
        "to be moved to practice. A jolt of urgency after three fairly calm "
        "texts.",
        reader_title="Four Horses",
    ),
    "sn55_5": ReaderMeta(
        "Dutiyasāriputta Sutta", 2, 5,
        "What actually leads to the path, in four steps that are ordinary "
        "enough to follow: find good company, hear the teaching, attend to it "
        "carefully, then practise in line with it. The first item is social, "
        "not inward.",
        reader_title="Four Steps That Lead to the Path",
    ),
    "an11_9": ReaderMeta(
        "Saddha Sutta", 2, 6,
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
        "Structured breath-meditation instructions. The first text on this "
        "list that is a practice manual rather than a teaching about practice.",
        reader_title="Breath Meditation, Step by Step",
    ),
    "mn10": ReaderMeta(
        "Satipaṭṭhāna Sutta", 3, 5,
        "The four foundations of remembering, and the longest, densest text so "
        "far. Not really a one-sitting read: it is the reference manual for "
        "the pieces above, worth returning to rather than finishing.",
        reader_title="The Four Foundations of Remembering",
    ),
    "dn2": ReaderMeta(
        "Sāmaññaphala Sutta", 3, 6,
        "A king asks what a renunciant actually gets out of the life. A full "
        "narrative walk through the gradual path from an outsider's curious, "
        "slightly skeptical point of view.",
        reader_title="What Does a Renunciant Gain?",
    ),
    "an10_60": ReaderMeta(
        "Girimānanda Sutta", 3, 7,
        "Ten perceptions taught to a sick monk. Practical and, unusually for "
        "this stage, comforting.",
        reader_title="Ten Perceptions for a Sick Monk",
    ),
    "mn39": ReaderMeta(
        "Mahā-Assapura Sutta", 3, 8,
        "What actually makes someone a genuine renunciant, as opposed to "
        "someone who merely looks like one. Ethics and practice fused.",
        reader_title="What Makes a Genuine Renunciant?",
    ),
    "sn46_51": ReaderMeta(
        "Āhāra Sutta", 3, 9,
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
    "sn22_89": ReaderMeta(
        "Khemaka Sutta", 4, 4,
        "A subtler point: even someone who has genuinely seen not-self can "
        "still carry a faint, hard-to-locate sense of \"I am.\"",
        reader_title="The Lingering Sense of 'I Am'",
    ),
    "mn148": ReaderMeta(
        "Chachakka Sutta", 4, 5,
        "A systematic, almost mechanical working-through of not-self across "
        "every sense door. Dense, but by this point the pattern should be "
        "familiar.",
        reader_title="Not-Self at the Six Sense Doors",
    ),
    "sn12_15": ReaderMeta(
        "Kaccānagotta Sutta", 4, 6,
        "One page, defining right view as the middle between \"it exists\" and "
        "\"it doesn't.\" The clearest, shortest bridge into dependent arising.",
        reader_title="Between 'It Exists' and 'It Doesn't'",
    ),
    "sn12_61": ReaderMeta(
        "Assutavā Sutta", 4, 7,
        "An argument that runs the opposite way from what you expect: if you "
        "must identify with something, the body is the safer choice, because "
        "its changing is visible and the mind's is not.",
        reader_title="Body and Mind Keep Changing",
    ),
    "sn12_23": ReaderMeta(
        "Upanisa Sutta", 4, 8,
        "The positive chain, dissatisfaction leading step by step to freedom, "
        "mirroring the well-known negative chain.",
        reader_title="From Dissatisfaction to Freedom",
    ),
    "sn12_11": ReaderMeta(
        "Āhāra Sutta", 4, 9,
        "Four things that keep a life going, traced back to wanting and then "
        "all the way back along the chain. Not to be confused with SN 46.51, "
        "which shares its name.",
        reader_title="What Keeps a Life Going",
    ),
    "sn12_2": ReaderMeta(
        "Paṭiccasamuppāda-vibhaṅga Sutta", 4, 10,
        "The standard formula of dependent arising, defined term by term.",
        reader_title="Dependent Arising, Term by Term",
    ),
    "mn38": ReaderMeta(
        "Mahātaṇhāsaṅkhaya Sutta", 4, 11,
        "A monk's wrong view — that the same consciousness travels on "
        "unchanged — gets corrected, and dependent arising gets restated in "
        "narrative, argued form rather than as a bare formula.",
        reader_title="Does the Same Consciousness Continue?",
    ),
    "dn15": ReaderMeta(
        "Mahānidāna Sutta", 4, 12,
        "The deepest and longest exposition of dependent arising in the set. "
        "The capstone of this stage, not an entry point to it.",
        reader_title="Dependent Arising in Depth",
    ),
    "mn9": ReaderMeta(
        "Sammādiṭṭhi Sutta", 4, 13,
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

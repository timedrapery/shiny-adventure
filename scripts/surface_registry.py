#!/usr/bin/env python3
"""Registry of outward-facing translation and generated surfaces."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

try:
    from scripts.cluster_registry import CLUSTER_SURFACES, ClusterSurface, REPO_ROOT
except ModuleNotFoundError:
    from cluster_registry import CLUSTER_SURFACES, ClusterSurface, REPO_ROOT


@dataclass(frozen=True)
class TranslationSurface:
    key: str
    label: str
    main_relpath: str
    notes_relpath: str

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

# The five texts that give the whole shape of the teaching in under a thousand
# words. Keys index into TRANSLATION_SURFACES.
ESSENTIAL_FIVE: tuple[str, ...] = (
    "an3_65", "sn56_11", "sn36_6", "mn63", "sn22_59",
)

READER_METADATA: dict[str, ReaderMeta] = {
    # Stage 1 -- Before Any Doctrine
    "an3_65": ReaderMeta(
        "Kesamutta Sutta", 1, 1,
        "\"Don't take my word for it, or anyone else's.\" The most naturally "
        "modern-feeling starting point: an explicit instruction to test claims "
        "against your own experience rather than accept them on authority.",
        reader_title="Test It Yourself",
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
    ),
    "mn118": ReaderMeta(
        "Ānāpānasati Sutta", 3, 4,
        "Structured breath-meditation instructions. The first text on this "
        "list that is a practice manual rather than a teaching about practice.",
    ),
    "mn10": ReaderMeta(
        "Satipaṭṭhāna Sutta", 3, 5,
        "The four foundations of remembering, and the longest, densest text so "
        "far. Not really a one-sitting read: it is the reference manual for "
        "the pieces above, worth returning to rather than finishing.",
    ),
    "dn2": ReaderMeta(
        "Sāmaññaphala Sutta", 3, 6,
        "A king asks what a renunciant actually gets out of the life. A full "
        "narrative walk through the gradual path from an outsider's curious, "
        "slightly skeptical point of view.",
    ),
    "an10_60": ReaderMeta(
        "Girimānanda Sutta", 3, 7,
        "Ten perceptions taught to a sick monk. Practical and, unusually for "
        "this stage, comforting.",
    ),
    "mn39": ReaderMeta(
        "Mahā-Assapura Sutta", 3, 8,
        "What actually makes someone a genuine renunciant, as opposed to "
        "someone who merely looks like one. Ethics and practice fused.",
    ),
    "sn46_51": ReaderMeta(
        "Āhāra Sutta", 3, 9,
        "What feeds the distractions that block practice, and what starves "
        "them. A closing, practical text for this stage.",
    ),
    # Stage 4 -- Not-Self and Dependent Arising
    "sn22_59": ReaderMeta(
        "Anattalakkhaṇa Sutta", 4, 1,
        "The second sermon. Not-self laid out as a clean, followable argument "
        "rather than an assertion.",
        reader_title="Nothing Here Is You",
    ),
    "mn22": ReaderMeta(
        "Alagaddūpama Sutta", 4, 2,
        "The snake simile and the raft simile carry genuinely difficult "
        "not-self doctrine on strong enough imagery that it stays followable.",
    ),
    "sn22_48": ReaderMeta(
        "Khandha Sutta", 4, 3,
        "What the five heaps actually are, stated directly.",
    ),
    "sn22_89": ReaderMeta(
        "Khemaka Sutta", 4, 4,
        "A subtler point: even someone who has genuinely seen not-self can "
        "still carry a faint, hard-to-locate sense of \"I am.\"",
    ),
    "mn148": ReaderMeta(
        "Chachakka Sutta", 4, 5,
        "A systematic, almost mechanical working-through of not-self across "
        "every sense door. Dense, but by this point the pattern should be "
        "familiar.",
    ),
    "sn12_15": ReaderMeta(
        "Kaccānagotta Sutta", 4, 6,
        "One page, defining right view as the middle between \"it exists\" and "
        "\"it doesn't.\" The clearest, shortest bridge into dependent arising.",
    ),
    "sn12_61": ReaderMeta(
        "Assutavā Sutta", 4, 7,
        "An argument that runs the opposite way from what you expect: if you "
        "must identify with something, the body is the safer choice, because "
        "its changing is visible and the mind's is not.",
    ),
    "sn12_23": ReaderMeta(
        "Upanisa Sutta", 4, 8,
        "The positive chain, dissatisfaction leading step by step to freedom, "
        "mirroring the well-known negative chain.",
    ),
    "sn12_11": ReaderMeta(
        "Āhāra Sutta", 4, 9,
        "Four things that keep a life going, traced back to wanting and then "
        "all the way back along the chain. Not to be confused with SN 46.51, "
        "which shares its name.",
    ),
    "sn12_2": ReaderMeta(
        "Paṭiccasamuppāda-vibhaṅga Sutta", 4, 10,
        "The standard formula of dependent arising, defined term by term.",
    ),
    "mn38": ReaderMeta(
        "Mahātaṇhāsaṅkhaya Sutta", 4, 11,
        "A monk's wrong view — that the same consciousness travels on "
        "unchanged — gets corrected, and dependent arising gets restated in "
        "narrative, argued form rather than as a bare formula.",
    ),
    "dn15": ReaderMeta(
        "Mahānidāna Sutta", 4, 12,
        "The deepest and longest exposition of dependent arising in the set. "
        "The capstone of this stage, not an entry point to it.",
    ),
    "mn9": ReaderMeta(
        "Sammādiṭṭhi Sutta", 4, 13,
        "Right view examined through more than a dozen different doctrinal "
        "lenses in one text. Reads best as a review once the pieces it is "
        "reviewing are already familiar.",
    ),
    # Stage 5 -- Advanced and Reference Texts
    "mn43": ReaderMeta(
        "Mahāvedalla Sutta", 5, 2,
        "The longer companion to MN 44, and the same format: two senior "
        "disciples working through the vocabulary point by point. Read it "
        "second — it assumes more.",
    ),
    "mn44": ReaderMeta(
        "Cūḷavedalla Sutta", 5, 1,
        "A systematic question-and-answer exchange between two disciples, "
        "covering a wide sweep of doctrine efficiently.",
    ),
    "sn51_13": ReaderMeta(
        "Chandasamādhi Sutta", 5, 3,
        "One short formula, stated four times, defining the four bases of "
        "power. Useful mainly as a reference for how the effort formula is "
        "built.",
    ),
    "mn64": ReaderMeta(
        "Mahāmālukya Sutta", 5, 4,
        "The five lower fetters, and the companion piece to MN 63 — same "
        "disciple, later in his practice.",
    ),
    "mn11": ReaderMeta(
        "Cūḷasīhanāda Sutta", 5, 5,
        "A claim about who counts as a genuine practitioner, grounded in "
        "whether a teaching can account for all four ways of taking things "
        "personally — including taking a doctrine of self personally.",
    ),
    "mn137": ReaderMeta(
        "Saḷāyatanavibhaṅga Sutta", 5, 6,
        "A technical analysis of the six fields of experience.",
    ),
    "mn141": ReaderMeta(
        "Saccavibhaṅga Sutta", 5, 7,
        "The four noble truths again, now in full analytical detail rather "
        "than the compressed form from Stage 2.",
    ),
    "mn117": ReaderMeta(
        "Mahācattārīsaka Sutta", 5, 8,
        "A technical analysis of the eightfold path, factor by factor.",
    ),
    "an6_63": ReaderMeta(
        "Nibbedhika Sutta", 5, 9,
        "One analytical frame applied six times over, to sensuality, feeling, "
        "recognition, the outflows, action, and dissatisfaction. Includes the "
        "line that defines action as intention.",
    ),
    "sn35_28": ReaderMeta(
        "Āditta Sutta", 5, 10,
        "The fire sermon. Iconic imagery carrying a genuinely abstract point "
        "about the senses.",
    ),
    "mn18": ReaderMeta(
        "Madhupiṇḍika Sutta", 5, 11,
        "The honey-ball sutta, on how recognition snowballs into proliferating "
        "thought. Famously dense even by this collection's standards.",
    ),
    "mn99": ReaderMeta(
        "Subha Sutta", 5, 12,
        "A dialogue defending renunciant life against a brahmin's claim that "
        "household life is better. Good late-stage read for weighing the whole "
        "path against the alternative.",
    ),
    "mn1": ReaderMeta(
        "Mūlapariyāya Sutta", 5, 13,
        "\"The root of all things.\" Traditionally regarded as one of the most "
        "difficult texts in the collection. Deliberately last: it rewards "
        "everything that came before it and rewards very little read cold.",
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

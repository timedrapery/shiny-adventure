#!/usr/bin/env python3
"""Registry of outward-facing translation and generated surfaces."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, replace
from pathlib import Path

try:
    from scripts.cluster_registry import CLUSTER_SURFACES, ClusterSurface, REPO_ROOT
except ModuleNotFoundError:
    from cluster_registry import CLUSTER_SURFACES, ClusterSurface, REPO_ROOT


@dataclass(frozen=True)
class ReadabilityReview:
    """Integrity state for a surface revised under the plain-English standard.

    `revised_on` is the date the body with this `body_sha256` was last
    revised. It is a version date, not a claim that anyone reviewed the text
    on that day; human review evidence is recorded, bound to the hash, in
    `reviews/newcomer-review-ledger.json`.
    """

    standard: str
    status: str
    revised_on: str
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


BODY_VERSIONS_RELPATH = "reviews/body-versions.json"


def load_body_versions(path: Path | None = None) -> dict[str, dict[str, str]]:
    """Return {surface key: {"body_sha256", "revised_on"}} from the version record.

    The hash and the date used to live in two parallel tables in this module,
    and nothing made them move together: a body could be re-hashed while its
    date stayed behind, and the reader then published a date older than the
    text beside it. They are one record per surface now, written by
    `scripts/refresh_derived.py`.
    """

    effective_path = path or (REPO_ROOT / BODY_VERSIONS_RELPATH)
    data = json.loads(effective_path.read_text(encoding="utf-8"))
    surfaces = data.get("surfaces")
    if not isinstance(surfaces, dict):
        raise ValueError(f"{effective_path}: expected a `surfaces` object")
    return surfaces


def _body_version(versions: dict[str, dict[str, str]], key: str) -> dict[str, str]:
    record = versions.get(key)
    if not isinstance(record, dict) or "body_sha256" not in record or "revised_on" not in record:
        raise ValueError(
            f"{BODY_VERSIONS_RELPATH} has no complete record for `{key}`; "
            "run `python scripts/refresh_derived.py --write`"
        )
    return record


BODY_VERSIONS = load_body_versions()

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
            revised_on=_body_version(BODY_VERSIONS, surface.key)["revised_on"],
            body_sha256=_body_version(BODY_VERSIONS, surface.key)["body_sha256"],
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
        "Texts that set the tone before anything technical. Why trust "
        "this material at all? Why do some questions stay unanswered on "
        "purpose? And who was asking them?",
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
        "The first sermon: the four noble truths and the eightfold path, "
        "stated directly. It is foundational, but it reads better after "
        "Stage 1 sets the frame. Taken cold, its formulas can feel like a"
        " list to memorize, not a diagnosis to recognize.",
        reader_title="The First Teaching",
    ),
    "sn56_17": ReaderMeta(
        "Avijjā Sutta", 2, 2,
        "A bhikkhu asks what ignorance means. The answer is precise: not "
        "seeing dissatisfaction, where it comes from, when it ends, "
        "and how to end it again.",
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
        "More than 150 monastic rules, gathered into three trainings: "
        "conduct, the mind, and discernment. You can repair minor "
        "mistakes, and even partial training still bears fruit.",
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
        "The five precepts seen from the other side. Keeping them gives "
        "every being you might have harmed freedom from fear, and you "
        "come to share in that freedom.",
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
        "The text traces greed, aversion, and delusion from their roots "
        "to their effects on action, speech, power, and the heart. Then "
        "it contrasts them with non-greed, non-aversion, and clarity.",
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
        "Four kinds of horses, four kinds of people, and what it takes to"
        " move someone to practice. A jolt of urgency after three fairly "
        "calm texts.",
        reader_title="Four Horses",
    ),
    "sn55_5": ReaderMeta(
        "Dutiyasāriputta Sutta", 2, 18,
        "What leads to the path, in four ordinary steps: find good "
        "company, hear the teaching, attend to it carefully, then "
        "practise in line with it. The first step is social, not inward.",
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
        "The Buddha teaches his son Rāhula with a water vessel, emptied "
        "and turned upside down, and then a war elephant. His point: "
        "someone who feels no shame in lying has nothing left to hold "
        "them back. Then comes a nine-part check for any action of body, "
        "speech, or mind, before, during, and after it.",
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
        "The Buddha's own way of dwelling in emptiness. How to train "
        "toward it when the heart will not go there, and why a teacher "
        "who keeps correcting you is a friend.",
        reader_title="Dwelling in Emptiness",
    ),
    "mn121": ReaderMeta(
        "Cūḷasuññata Sutta", 3, 10,
        "Emptiness, step by step: each time, notice what has dropped away"
        " and what remains, until only this living body remains.",
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
        "Before awakening, the Buddha asks three things of each of the "
        "five heaps: its appeal, its danger, and the way out.",
        reader_title="What the Heaps Offer, and the Way Out",
    ),
    "sn22_86": ReaderMeta(
        "Anurādha Sutta", 4, 6,
        "Anurādha tries to place the Tathāgata outside four claims about "
        "what happens after death. The Buddha asks whether you can pin "
        "down the Tathāgata through the five heaps even here and now.",
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
        "How the lived world grows through the six senses into wanting, "
        "taking experience personally, and dissatisfaction. And how that "
        "process ends, without the senses having to disappear.",
        reader_title="How the World Arises—and Ends",
    ),
    "sn12_61": ReaderMeta(
        "Assutavā Sutta", 4, 13,
        "An argument that runs the opposite way from what you expect. If "
        "you must identify with something, the body is the safer choice, "
        "because its changes are easy to see and the mind's are not.",
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
        "Four things that keep a life going, traced back to wanting and "
        "then all the way back along the chain. It shares its name with "
        "SN 46.51, a different text.",
        reader_title="What Keeps a Life Going",
    ),
    "sn12_2": ReaderMeta(
        "Paṭiccasamuppāda-vibhaṅga Sutta", 4, 16,
        "The standard formula of dependent arising, defined term by term.",
        reader_title="Dependent Arising, Term by Term",
    ),
    "sn12_20": ReaderMeta(
        "Paccaya Sutta", 4, 17,
        "Dependent arising as a pattern that holds whether or not anyone "
        "discovers it, kept apart from the changing things it runs "
        "through. And why someone who sees this stops questioning their "
        "own past and future.",
        reader_title="Discovered, Not Invented",
    ),
    "mn38": ReaderMeta(
        "Mahātaṇhāsaṅkhaya Sutta", 4, 18,
        "A monk holds a wrong view: that the same consciousness travels "
        "on unchanged. The Buddha corrects it and restates dependent "
        "arising as a reasoned story, not a bare formula.",
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
        "Who counts as a genuine practitioner? The answer turns on "
        "whether a teaching can account for all four ways of taking "
        "things personally, including taking a doctrine of self "
        "personally.",
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
    """The citation a surface's Pali source is located by, such as `SN 22.86`.

    A verse range such as `Dhp 21-32` is cited by its first verse.
    """
    return re.sub(r"-\d+$", "", surface.label.strip())


# The Pali edition the source checks read since 2026-11-10: the Vipassana
# Research Institute's Chaṭṭha Saṅgāyana Tipiṭaka. Its terms ask for
# attribution, which the reader page gives. See docs/source-text-policy.md.
PALI_EDITION_NAME = "Chaṭṭha Saṅgāyana Tipiṭaka, Vipassana Research Institute"
PALI_EDITION_URL = "https://tipitaka.org/romn/"

# Which VRI book holds a citation, computed from the reference alone so the
# reader can be generated without the (uncommitted) VRI files.
_VRI_BOOK_RANGES: dict[str, tuple[tuple[int, int, str], ...]] = {
    "DN": ((1, 13, "Dīghanikāya, Sīlakkhandhavaggapāḷi"), (14, 23, "Dīghanikāya, Mahāvaggapāḷi"),
           (24, 34, "Dīghanikāya, Pāthikavaggapāḷi")),
    "MN": ((1, 50, "Majjhimanikāya, Mūlapaṇṇāsapāḷi"), (51, 100, "Majjhimanikāya, Majjhimapaṇṇāsapāḷi"),
           (101, 152, "Majjhimanikāya, Uparipaṇṇāsapāḷi")),
    "SN": ((1, 11, "Saṃyuttanikāya, Sagāthāvaggapāḷi"), (12, 21, "Saṃyuttanikāya, Nidānavaggapāḷi"),
           (22, 34, "Saṃyuttanikāya, Khandhavaggapāḷi"), (35, 44, "Saṃyuttanikāya, Saḷāyatanavaggapāḷi"),
           (45, 56, "Saṃyuttanikāya, Mahāvaggapāḷi")),
}
_VRI_AN_BOOKS = (
    "Ekakanipātapāḷi", "Dukanipātapāḷi", "Tikanipātapāḷi", "Catukkanipātapāḷi",
    "Pañcakanipātapāḷi", "Chakkanipātapāḷi", "Sattakanipātapāḷi", "Aṭṭhakanipātapāḷi",
    "Navakanipātapāḷi", "Dasakanipātapāḷi", "Ekādasakanipātapāḷi",
)
_VRI_KN_BOOKS = {
    "Dhp": "Khuddakanikāya, Dhammapadapāḷi", "Ud": "Khuddakanikāya, Udānapāḷi",
    "Iti": "Khuddakanikāya, Itivuttakapāḷi", "Snp": "Khuddakanikāya, Suttanipātapāḷi",
}


def pali_source_book(surface: TranslationSurface) -> str:
    """The VRI book that holds a surface's Pali text, by name."""

    collection, _, number = canonical_reference(surface).partition(" ")
    first = int(number.split(".")[0])
    if collection in _VRI_KN_BOOKS:
        return _VRI_KN_BOOKS[collection]
    if collection == "AN":
        return f"Aṅguttaranikāya, {_VRI_AN_BOOKS[first - 1]}"
    for low, high, name in _VRI_BOOK_RANGES[collection]:
        if low <= first <= high:
            return name
    raise ValueError(f"{surface.label}: no VRI book covers this reference")


def canonical_pali_url(surface: TranslationSurface) -> str:
    """Where a reader can find the Pali edition the source checks use."""
    return PALI_EDITION_URL


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

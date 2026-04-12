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
        key="mn10",
        label="MN 10",
        main_relpath="docs/translations/mn10-satipatthana-sutta.md",
        notes_relpath="docs/translations/mn10-satipatthana-sutta-notes.md",
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
)


def generated_surface_groups() -> tuple[ClusterSurface, ...]:
    """Return the CI-enforced generated doc groups backed by report scripts."""

    return CLUSTER_SURFACES

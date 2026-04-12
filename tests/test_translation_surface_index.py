from __future__ import annotations

import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


surface_registry = load_module("surface_registry", "scripts/surface_registry.py")
translation_surface_index = load_module(
    "translation_surface_index",
    "scripts/translation_surface_index.py",
)


class TranslationSurfaceIndexTests(unittest.TestCase):
    def test_collect_surface_failures_accepts_current_registry_and_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            translations_dir = repo_root / "docs" / "translations"
            translations_dir.mkdir(parents=True, exist_ok=True)

            surface = surface_registry.TranslationSurface(
                key="mn-test",
                label="MN Test",
                main_relpath="docs/translations/mn-test-sutta.md",
                notes_relpath="docs/translations/mn-test-sutta-notes.md",
            )
            (repo_root / surface.main_relpath).write_text(
                "# Main\n\n- Companion translator notes: [notes](mn-test-sutta-notes.md)\n",
                encoding="utf-8",
            )
            (repo_root / surface.notes_relpath).write_text(
                "# Notes\n\nSee [main translation](mn-test-sutta.md).\n",
                encoding="utf-8",
            )
            index_path = translations_dir / "translation-documents.md"
            index_path.write_text(
                translation_surface_index.render_index((surface,)),
                encoding="utf-8",
            )

            failures = translation_surface_index.collect_surface_failures(
                repo_root,
                (surface,),
                index_path=index_path,
            )

        self.assertEqual(failures, [])

    def test_collect_surface_failures_reports_missing_cross_links_and_stale_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            translations_dir = repo_root / "docs" / "translations"
            translations_dir.mkdir(parents=True, exist_ok=True)

            surface = surface_registry.TranslationSurface(
                key="mn-test",
                label="MN Test",
                main_relpath="docs/translations/mn-test-sutta.md",
                notes_relpath="docs/translations/mn-test-sutta-notes.md",
            )
            (repo_root / surface.main_relpath).write_text(
                "# Main\n\nNo companion link here.\n",
                encoding="utf-8",
            )
            (repo_root / surface.notes_relpath).write_text(
                "# Notes\n\nNo back-link here either.\n",
                encoding="utf-8",
            )
            index_path = translations_dir / "translation-documents.md"
            index_path.write_text("# Stale\n", encoding="utf-8")

            failures = translation_surface_index.collect_surface_failures(
                repo_root,
                (surface,),
                index_path=index_path,
            )

        self.assertEqual(len(failures), 3)
        self.assertIn("main translation does not link", failures[0])
        self.assertIn("companion notes do not link back", failures[1])
        self.assertIn("Stale translation surface index", failures[2])

    def test_main_supports_write_and_check(self) -> None:
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            translations_dir = repo_root / "docs" / "translations"
            translations_dir.mkdir(parents=True, exist_ok=True)

            surface = surface_registry.TranslationSurface(
                key="mn-test",
                label="MN Test",
                main_relpath="docs/translations/mn-test-sutta.md",
                notes_relpath="docs/translations/mn-test-sutta-notes.md",
            )
            (repo_root / surface.main_relpath).write_text(
                "# Main\n\n- Companion translator notes: [notes](mn-test-sutta-notes.md)\n",
                encoding="utf-8",
            )
            (repo_root / surface.notes_relpath).write_text(
                "# Notes\n\nSee [main translation](mn-test-sutta.md).\n",
                encoding="utf-8",
            )

            with mock.patch.object(
                translation_surface_index,
                "TRANSLATION_SURFACES",
                (surface,),
            ):
                with mock.patch.object(translation_surface_index, "REPO_ROOT", repo_root):
                    with mock.patch.object(
                        translation_surface_index,
                        "TRANSLATIONS_DIR",
                        translations_dir,
                    ):
                        with mock.patch.object(
                            translation_surface_index,
                            "INDEX_PATH",
                            translations_dir / "translation-documents.md",
                        ):
                            with mock.patch(
                                "sys.argv",
                                [
                                    "translation_surface_index.py",
                                    "--write-docs",
                                    "--check",
                                ],
                            ):
                                with mock.patch("sys.stdout", output):
                                    result = translation_surface_index.main()

        self.assertEqual(result, 0)
        self.assertIn("Translation surface check passed", output.getvalue())


if __name__ == "__main__":
    unittest.main()

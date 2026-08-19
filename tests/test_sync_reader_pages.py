from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.helpers import load_module


sync = load_module("sync_reader_pages", "scripts/sync_reader_pages.py")


SURFACE = """# SN 0.0: Test Sutta

## Editorial Note

- Apparatus that reader pages do not carry.

## Translation

### The Difference

They felt it plainly.

### Verses

They discern rightly.
"""

READER = """# A Reader Title

*SN 0.0, the Test Sutta*

## About this text

A plain-English introduction that belongs only to the reader page.

## The Difference

They felt it plainly.

## Verses

They discern rightly.
"""


def make_repo(tmpdir: str, surface: str = SURFACE, reader: str = READER):
    root = Path(tmpdir)
    translations = root / "docs" / "translations"
    readers = root / "reader-src" / "suttas"
    translations.mkdir(parents=True)
    readers.mkdir(parents=True)
    (translations / "sn0-0-test-sutta.md").write_text(surface, encoding="utf-8")
    (readers / "sn0-0-test-sutta.md").write_text(reader, encoding="utf-8")
    return root, readers, translations


class ExtractionTests(unittest.TestCase):
    def test_surface_body_demotes_headings(self) -> None:
        body = sync.surface_body(SURFACE)
        self.assertIn("## The Difference", body)
        self.assertNotIn("### The Difference", body)
        self.assertNotIn("Editorial Note", body)

    def test_reader_head_keeps_title_and_intro(self) -> None:
        head = sync.reader_head(READER)
        self.assertIn("A Reader Title", head)
        self.assertIn("About this text", head)
        self.assertNotIn("The Difference", head)

    def test_surface_body_requires_translation_section(self) -> None:
        with self.assertRaises(ValueError):
            sync.surface_body("# Title\n\nNo translation section.\n")


class NormalizeTests(unittest.TestCase):
    def test_emphasis_and_rules_are_ignored(self) -> None:
        a = "The discourse is finished."
        b = "---\n\n*The discourse is finished.*"
        self.assertEqual(sync.normalize(a), sync.normalize(b))

    def test_whitespace_and_wrapping_are_ignored(self) -> None:
        self.assertEqual(sync.normalize("one two\nthree"), sync.normalize("one   two three"))

    def test_real_word_change_is_not_ignored(self) -> None:
        self.assertNotEqual(sync.normalize("they felt it"), sync.normalize("one felt it"))


class ReportTests(unittest.TestCase):
    def test_matching_pages_report_no_divergence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, readers, translations = make_repo(tmp)
            report = sync.build_report(root, readers, translations)
        self.assertEqual(report["summary"]["diverged"], 0)
        self.assertEqual(report["summary"]["checked"], 1)

    def test_presentation_only_difference_is_tolerated(self) -> None:
        reader = READER.replace("They discern rightly.", "---\n\n*They discern rightly.*")
        with tempfile.TemporaryDirectory() as tmp:
            root, readers, translations = make_repo(tmp, reader=reader)
            report = sync.build_report(root, readers, translations)
        self.assertEqual(report["summary"]["diverged"], 0)

    def test_content_drift_is_detected(self) -> None:
        reader = READER.replace("They felt it plainly.", "One felt it plainly.")
        with tempfile.TemporaryDirectory() as tmp:
            root, readers, translations = make_repo(tmp, reader=reader)
            report = sync.build_report(root, readers, translations)
        self.assertEqual(report["summary"]["diverged"], 1)

    def test_reader_page_without_surface_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, readers, translations = make_repo(tmp)
            (readers / "orphan.md").write_text("# Orphan\n", encoding="utf-8")
            report = sync.build_report(root, readers, translations)
        self.assertEqual(report["orphans"], ["orphan.md"])


class WriteTests(unittest.TestCase):
    def test_write_repairs_drift_and_keeps_the_intro(self) -> None:
        reader = READER.replace("They felt it plainly.", "One felt it plainly.")
        with tempfile.TemporaryDirectory() as tmp:
            root, readers, translations = make_repo(tmp, reader=reader)
            written = sync.write_pages(root, readers, translations)
            self.assertEqual(len(written), 1)

            text = (readers / "sn0-0-test-sutta.md").read_text(encoding="utf-8")
            self.assertIn("A Reader Title", text)
            self.assertIn("About this text", text)
            self.assertIn("They felt it plainly.", text)
            self.assertNotIn("One felt it plainly.", text)

            report = sync.build_report(root, readers, translations)
            self.assertEqual(report["summary"]["diverged"], 0)

    def test_write_is_a_noop_when_already_in_sync(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, readers, translations = make_repo(tmp)
            self.assertEqual(sync.write_pages(root, readers, translations), [])


if __name__ == "__main__":
    unittest.main()

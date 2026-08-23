from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.helpers import load_module


plain_audit = load_module("plain_english_audit", "scripts/plain_english_audit.py")


class StripApparatusTests(unittest.TestCase):
    def test_editorial_note_is_not_scanned(self) -> None:
        text = (
            "# MN 0: Test\n"
            "\n"
            "## Editorial Note\n"
            "\n"
            "- One dwells here and the Blessed One said thus.\n"
            "\n"
            "## Translation\n"
            "\n"
            "The Buddha said this.\n"
        )
        findings = plain_audit.scan_text(text, "sample.md")
        self.assertEqual(findings, [])

    def test_reader_about_block_is_not_scanned(self) -> None:
        text = (
            "# Title\n\n## About this text\n\nOne who reads this dwells thus.\n"
            "\n## The Teaching\n\nThey listened.\n"
        )
        self.assertEqual(plain_audit.scan_text(text, "reader.md"), [])

    def test_fenced_code_is_not_scanned(self) -> None:
        text = "## Translation\n\n```\none who dwells thus\n```\n\nPlain sentence.\n"
        self.assertEqual(plain_audit.scan_text(text, "sample.md"), [])

    def test_line_numbers_survive_stripping(self) -> None:
        text = "## Translation\n\nfiller\n\nWhen one recognizes earth, it ends.\n"
        findings = plain_audit.scan_text(text, "sample.md")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["line"], 5)


class SignalTests(unittest.TestCase):
    def _labels(self, body: str) -> set[str]:
        text = f"## Translation\n\n{body}\n"
        return {str(f["label"]) for f in plain_audit.scan_text(text, "sample.md")}

    def test_generic_one_is_flagged(self) -> None:
        self.assertIn("generic one as subject", self._labels("Then one recognizes earth."))

    def test_generic_possessive_and_reflexive_are_flagged(self) -> None:
        labels = self._labels("They beat one's chest and take oneself to be earth.")
        self.assertIn("generic one possessive", labels)
        self.assertIn("generic oneself", labels)

    def test_having_participle_is_flagged(self) -> None:
        self.assertIn(
            "having-participle opener",
            self._labels("Having recognized earth as earth, they stopped."),
        )

    def test_blessed_one_is_flagged(self) -> None:
        self.assertIn("blessed one epithet", self._labels("Then the Blessed One spoke."))

    def test_plain_sentence_is_clean(self) -> None:
        self.assertEqual(self._labels("They recognized earth and let it go."), set())

    def test_they_pronoun_is_not_flagged(self) -> None:
        self.assertEqual(self._labels("They take themselves to be earth."), set())


class LexiconAwarenessTests(unittest.TestCase):
    def test_governed_nominalization_is_suppressed(self) -> None:
        governed = {"recognition of impermanence"}
        text = "## Translation\n\nThey practise the recognition of impermanence.\n"
        self.assertEqual(plain_audit.scan_text(text, "s.md", governed), [])

    def test_ungoverned_nominalization_is_flagged(self) -> None:
        text = "## Translation\n\nIt led to the cessation of the establishment.\n"
        labels = {str(f["label"]) for f in plain_audit.scan_text(text, "s.md", set())}
        self.assertIn("nominalization chain", labels)

    def test_governed_genre_label_suppresses_archaic_connective(self) -> None:
        governed = {"'thus it was said' texts"}
        text = "## Translation\n\nverses, 'thus it was said' texts, birth stories\n"
        self.assertEqual(plain_audit.scan_text(text, "s.md", governed), [])

    def test_bare_thus_is_still_flagged(self) -> None:
        # The governed rendering contains `thus`, so a containment-only test
        # would wrongly suppress every `thus` in the corpus.
        governed = {"'thus it was said' texts"}
        text = "## Translation\n\nThus, Ananda, these two dhammas meet.\n"
        labels = {str(f["label"]) for f in plain_audit.scan_text(text, "s.md", governed)}
        self.assertIn("archaic connective", labels)

    def test_no_one_constructions_are_not_flagged(self) -> None:
        text = (
            "## Translation\n\n"
            "No one kills, there is no one who kills, and no one takes a life.\n"
        )
        self.assertEqual(plain_audit.scan_text(text, "s.md", set()), [])

    def test_is_governed_window_requires_rendering_present(self) -> None:
        self.assertTrue(plain_audit.is_governed("thus", {"thus it was said"}, "a thus it was said b"))
        self.assertFalse(plain_audit.is_governed("thus", {"thus it was said"}, "and thus he left"))

    def test_is_governed_matches_either_direction(self) -> None:
        self.assertTrue(plain_audit.is_governed("escape", {"element of escape"}))
        self.assertTrue(plain_audit.is_governed("element of escape", {"escape"}))
        self.assertFalse(plain_audit.is_governed("something else", {"escape"}))

    def test_load_governed_renderings_reads_records(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            terms = Path(tmpdir) / "minor"
            terms.mkdir(parents=True)
            (terms / "x.json").write_text(
                '{"preferred_translation": "quenching",'
                ' "alternative_translations": ["cessation"],'
                ' "context_rules": [{"rendering": "ending"}]}',
                encoding="utf-8",
            )
            found = plain_audit.load_governed_renderings(Path(tmpdir))
        self.assertEqual(found, {"quenching", "cessation", "ending"})


class ReportTests(unittest.TestCase):
    def _repo(self, tmpdir: str, body: str) -> Path:
        repo_root = Path(tmpdir)
        translations = repo_root / "docs" / "translations"
        translations.mkdir(parents=True)
        (translations / "sample.md").write_text(
            f"## Translation\n\n{body}\n", encoding="utf-8"
        )
        (translations / "sample-notes.md").write_text(
            "## Notes\n\nOne who dwells thus.\n", encoding="utf-8"
        )
        return repo_root

    def test_notes_files_are_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = self._repo(tmpdir, "They spoke plainly.")
            report = plain_audit.build_report(
                repo_root,
                translations_dir=repo_root / "docs" / "translations",
                reader_dir=repo_root / "missing",
            )
        self.assertEqual(report["summary"]["files_scanned"], 1)
        self.assertEqual(report["summary"]["matches"], 0)

    def test_report_counts_signals(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = self._repo(tmpdir, "Then one recognizes earth as earth.")
            report = plain_audit.build_report(
                repo_root,
                translations_dir=repo_root / "docs" / "translations",
                reader_dir=repo_root / "missing",
            )
        self.assertEqual(report["summary"]["matches"], 1)
        self.assertIn("generic one as subject", report["label_counts"])

    def test_render_text_reports_clean_corpus(self) -> None:
        report = {
            "summary": {"files_scanned": 1, "matches": 0},
            "label_counts": {},
            "top_files": [],
            "findings": [],
        }
        self.assertIn("No register signals found", plain_audit.render_text(report, 5))


if __name__ == "__main__":
    unittest.main()

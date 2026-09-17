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


class SpokenRegisterTests(unittest.TestCase):
    """The distributional read-aloud measures.

    These are not signals. Each test pins down a measurement decision that was
    made deliberately, so that a later change to the numbers is a choice rather
    than an accident.
    """

    def _profile(self, body: str) -> dict:
        return plain_audit.profile_text(f"## Translation\n\n{body}\n", "sample.md")

    def test_speech_runs_across_continuation_paragraphs(self) -> None:
        """A speech opens with a quote and continues until it closes.

        Continuation paragraphs are not re-opened in this corpus, so a
        paragraph-local test would miss most of the dialogue.
        """
        body = (
            'He said this.\n'
            '\n'
            '"Bhikkhus, this does not last.\n'
            '\n'
            'It is not mine either."\n'
            '\n'
            'They were glad.\n'
        )
        profile = self._profile(body)
        # Both quoted paragraphs count; neither bare narration paragraph does.
        self.assertEqual(profile["dialogue"]["contractible_negations"], 2)

    def test_narration_negation_is_not_counted_as_dialogue(self) -> None:
        profile = self._profile("He did not answer, and she was not there.")
        self.assertEqual(profile["dialogue"]["contractible_negations"], 0)

    def test_contractions_are_counted(self) -> None:
        profile = self._profile('"Bhikkhus, that isn\'t mine and it doesn\'t last."')
        self.assertEqual(profile["dialogue"]["contractions"], 2)

    def test_vocative_positions_are_distinguished(self) -> None:
        body = (
            '"Bhikkhus, listen now.\n'
            '\n'
            'And what, bhikkhus, is right view?\n'
            '\n'
            'That is the difference, bhikkhus."\n'
        )
        profile = self._profile(body)
        self.assertEqual(profile["vocatives"]["initial"], 1)
        self.assertEqual(profile["vocatives"]["medial"], 1)
        self.assertEqual(profile["vocatives"]["final"], 1)

    def test_list_items_are_separate_units(self) -> None:
        """Bulleted items are delivered one at a time, not on one breath."""
        item = " ".join(["word"] * 30)
        body = f"They train in these:\n\n- {item}\n- {item}\n"
        profile = self._profile(body)
        # Glued together the two items would be a 60-word span; apart, neither
        # item passes the limit.
        self.assertEqual(profile["over_breath_limit"], 0)

    def test_breath_span_does_not_merge_across_paragraphs(self) -> None:
        """Q&A exchanges are separate paragraphs, not one enormous sentence."""
        line = " ".join(["word"] * 30) + "."
        body = f"{line}\n\n{line}\n"
        profile = self._profile(body)
        self.assertEqual(profile["over_breath_limit"], 0)
        self.assertEqual(profile["longest_unit"], 0)

    def test_long_sentence_is_measured(self) -> None:
        body = " ".join(["word"] * 50) + "."
        profile = self._profile(body)
        self.assertEqual(profile["over_breath_limit"], 1)
        self.assertEqual(profile["longest_unit"], 50)

    def test_repeated_unit_weight_counts_rehearings(self) -> None:
        sentence = "This is the sentence a reader hears again and again."
        profile = self._profile("\n\n".join([sentence] * 4))
        unit = profile["repeated_units"][0]
        self.assertEqual(unit["occurrences"], 4)
        # Weight is words x re-hearings: the first time is not a repeat.
        self.assertEqual(unit["weight"], unit["words"] * 3)

    def test_short_refrains_are_below_threshold(self) -> None:
        profile = self._profile("\n\n".join(["Yes, Bhante."] * 5))
        self.assertEqual(profile["repeated_units"], [])

    def test_shared_units_span_surfaces(self) -> None:
        """A formula said once per sutta still repeats for the reader."""
        sentence = "That is what the Buddha said to the bhikkhus that day."
        profiles = [
            plain_audit.profile_text(f"## Translation\n\n{sentence}\n", f"s{i}.md")
            for i in range(3)
        ]
        aggregate = plain_audit.aggregate_profiles(profiles)
        # No single surface repeats it, so it is absent from the per-surface list.
        self.assertEqual(aggregate["repeated_units"], [])
        shared = aggregate["shared_units"]
        self.assertEqual(len(shared), 1)
        self.assertEqual(shared[0]["surfaces"], 3)
        self.assertEqual(shared[0]["occurrences"], 3)

    def test_apparatus_is_excluded_from_the_profile(self) -> None:
        text = (
            "# MN 0: Test\n\n## Editorial Note\n\n"
            '- "Bhikkhus, this is not mine," the note says.\n\n'
            "## Translation\n\nThey listened.\n"
        )
        profile = plain_audit.profile_text(text, "sample.md")
        self.assertEqual(profile["dialogue"]["contractible_negations"], 0)


class SpokenRegisterReportingTests(unittest.TestCase):
    def _repo(self, tmpdir: str, body: str) -> Path:
        repo_root = Path(tmpdir)
        translations = repo_root / "docs" / "translations"
        translations.mkdir(parents=True)
        (translations / "mn0-sample-sutta.md").write_text(
            f"# MN 0: Sample\n\n## Translation\n\n{body}\n", encoding="utf-8"
        )
        (repo_root / "terms").mkdir()
        return repo_root

    def test_profile_does_not_become_a_gated_signal(self) -> None:
        """The spoken profile must never change the --strict verdict."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = self._repo(
                tmpdir, '"Bhikkhus, this does not last and it is not mine."'
            )
            report = plain_audit.build_report(
                repo_root,
                translations_dir=repo_root / "docs" / "translations",
                reader_dir=repo_root / "missing",
            )
        self.assertEqual(report["summary"]["matches"], 0)
        self.assertGreater(
            report["spoken_register"]["dialogue"]["contractible_negations"], 0
        )

    def test_repeat_tables_do_not_reach_the_report(self) -> None:
        """The per-unit tables are plumbing for the cross-surface rollup.

        Left on the profiles they put every sentence of the corpus, keyed
        twice, into `--format json` -- which took that output from 105KB to
        1.9MB when this was first written.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = self._repo(tmpdir, "The Buddha said this to the bhikkhus.")
            report = plain_audit.build_report(
                repo_root,
                translations_dir=repo_root / "docs" / "translations",
                reader_dir=repo_root / "missing",
            )
        for profile in report["surface_profiles"]:
            self.assertNotIn("_unit_counts", profile)
            self.assertNotIn("_unit_examples", profile)

    def test_spoken_section_is_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = self._repo(tmpdir, '"Bhikkhus, this does not last."')
            report = plain_audit.build_report(
                repo_root,
                translations_dir=repo_root / "docs" / "translations",
                reader_dir=repo_root / "missing",
            )
        self.assertNotIn("Spoken register profile", plain_audit.render_text(report, 5))
        self.assertIn(
            "Spoken register profile",
            plain_audit.render_text(report, 5, spoken=True),
        )


if __name__ == "__main__":
    unittest.main()

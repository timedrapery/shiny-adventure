from __future__ import annotations

import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module

lint_terms = load_module("lint_terms", "scripts/lint_terms.py")


class LintEncodingTests(unittest.TestCase):
    def test_placeholder_text_is_reported(self) -> None:
        terms = {
            "sangha": {
                "term": "sa?gha",
                "preferred_translation": "sa\u1e45gha",
                "literal_meaning": "community",
                "definition": "The noble community.",
            }
        }

        issues = lint_terms.check_suspicious_placeholders(terms)

        self.assertEqual(
            issues,
            [
                "sangha.json: field 'term' contains '?' placeholder text; check for encoding loss"
            ],
        )


class LintRuleTests(unittest.TestCase):
    def test_missing_related_terms_are_reported(self) -> None:
        terms = {
            "sati": {"related_terms": ["samadhi", "pa\u00f1\u00f1\u0101"]},
            "samadhi": {"related_terms": ["sati"]},
        }

        issues = lint_terms.check_missing_related_terms(terms)

        self.assertEqual(
            issues,
            ["sati.json: related term 'pa\\xf1\\xf1\\u0101' does not resolve to a local entry"],
        )

    def test_one_way_related_terms_are_reported(self) -> None:
        terms = {
            "sati": {"related_terms": ["samadhi"]},
            "samadhi": {"related_terms": []},
        }

        issues = lint_terms.check_one_way_related_terms(terms)

        self.assertEqual(
            issues,
            ["sati.json -> samadhi.json: related_terms link is not reciprocal"],
        )

    def test_major_reviewed_entries_require_sutta_references(self) -> None:
        terms = {
            "dukkha": {"entry_type": "major", "status": "reviewed", "sutta_references": []},
            "anicca": {"entry_type": "minor", "status": "reviewed", "sutta_references": []},
        }

        issues = lint_terms.check_missing_sutta_references(terms)

        self.assertEqual(
            issues,
            ["dukkha.json: major reviewed entry is missing sutta_references"],
        )

    def test_untranslated_preference_requires_gloss(self) -> None:
        terms = {
            "nibbana": {"untranslated_preferred": True},
            "sangha": {
                "untranslated_preferred": True,
                "gloss_on_first_occurrence": "sa\u1e45gha (community)",
            },
        }

        issues = lint_terms.check_untranslated_preferences(terms)

        self.assertEqual(
            issues,
            ["nibbana.json: untranslated_preferred is true but gloss_on_first_occurrence is missing"],
        )


class LintCliTests(unittest.TestCase):
    def test_main_reports_missing_terms_directory(self) -> None:
        output = io.StringIO()

        with tempfile.TemporaryDirectory() as tmpdir:
            missing_dir = Path(tmpdir) / "missing-terms"
            with mock.patch.object(lint_terms, "TERMS_DIR", missing_dir):
                with mock.patch("sys.argv", ["lint_terms.py"]):
                    with mock.patch("sys.stdout", output):
                        result = lint_terms.main()

        self.assertEqual(result, 1)
        self.assertIn("ERROR: Terms directory not found", output.getvalue())

    def test_main_returns_warning_exit_code_zero_without_strict(self) -> None:
        output = io.StringIO()
        terms = {
            "sati": {"related_terms": ["samadhi"]},
            "samadhi": {"related_terms": []},
        }

        with mock.patch.object(lint_terms, "load_terms", return_value=terms):
            with mock.patch("sys.argv", ["lint_terms.py"]):
                with mock.patch("sys.stdout", output):
                    result = lint_terms.main()

        self.assertEqual(result, 0)
        self.assertIn("Editorial lint warnings:", output.getvalue())
        self.assertIn("Completed with 1 warning(s).", output.getvalue())

    def test_main_returns_warning_exit_code_one_with_strict(self) -> None:
        output = io.StringIO()
        terms = {
            "sati": {"related_terms": ["samadhi"]},
            "samadhi": {"related_terms": []},
        }

        with mock.patch.object(lint_terms, "load_terms", return_value=terms):
            with mock.patch("sys.argv", ["lint_terms.py", "--strict"]):
                with mock.patch("sys.stdout", output):
                    result = lint_terms.main()

        self.assertEqual(result, 1)
        self.assertIn("Editorial lint warnings:", output.getvalue())
        self.assertNotIn("Completed with 1 warning(s).", output.getvalue())

    def test_main_returns_error_for_placeholder_text(self) -> None:
        output = io.StringIO()
        terms = {
            "sangha": {
                "term": "sa?gha",
                "preferred_translation": "sa\u1e45gha",
                "definition": "The noble community.",
            }
        }

        with mock.patch.object(lint_terms, "load_terms", return_value=terms):
            with mock.patch("sys.argv", ["lint_terms.py"]):
                with mock.patch("sys.stdout", output):
                    result = lint_terms.main()

        self.assertEqual(result, 1)
        self.assertIn("Editorial lint failed:", output.getvalue())
        self.assertIn("Encoding:", output.getvalue())


if __name__ == "__main__":
    unittest.main()

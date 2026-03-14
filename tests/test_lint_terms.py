from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_module(module_name: str, relative_path: str):
    path = REPO_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


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


if __name__ == "__main__":
    unittest.main()

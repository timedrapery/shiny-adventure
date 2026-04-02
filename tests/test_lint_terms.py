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

    def test_mojibake_sequences_are_reported(self) -> None:
        terms = {
            "samadhi": {
                "term": "samÄdhi",
                "preferred_translation": "mental composure",
                "definition": "A settled mind.",
            }
        }

        issues = lint_terms.check_mojibake_patterns(terms)

        self.assertEqual(len(issues), 1)
        self.assertIn(
            "samadhi.json.term: contains suspicious mojibake sequence",
            issues[0],
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

    def test_minor_phrase_related_terms_do_not_require_reciprocal_links(self) -> None:
        terms = {
            "imasmim-sati-idam-hoti": {
                "entry_type": "minor",
                "part_of_speech": "phrase",
                "related_terms": ["paticcasamuppada"],
            },
            "paticcasamuppada": {"related_terms": []},
        }

        issues = lint_terms.check_one_way_related_terms(terms)

        self.assertEqual(issues, [])

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

    def test_stabilized_terms_must_be_major_and_rule_bearing(self) -> None:
        terms = {
            stem: {
                "entry_type": "major",
                "status": "reviewed",
                "notes": "Rule-bearing note.",
                "context_rules": [{"context": "default", "rendering": "x"}, {"context": "alt", "rendering": "y"}],
                "related_terms": ["other"],
                "example_phrases": [{"pali": "x"}],
                "sutta_references": ["SN 1.1"],
            }
            for stem in lint_terms.STABILIZED_RULE_TERMS
        }
        terms["ditthi"]["entry_type"] = "minor"
        terms["dhamma"]["context_rules"] = [{"context": "default", "rendering": "dhamma"}]

        issues = lint_terms.check_stabilized_term_policy(terms)

        self.assertIn(
            "ditthi.json: stabilized drift-danger term must be a major entry",
            issues,
        )
        self.assertIn(
            "dhamma.json: stabilized drift-danger term must include at least two context_rules",
            issues,
        )

    def test_translation_policy_requires_leave_untranslated_guidance(self) -> None:
        terms = {
            "nibbana": {
                "entry_type": "major",
                "untranslated_preferred": True,
                "translation_policy": {
                    "default_scope": "source-facing prose",
                    "drift_risk": "Avoid narrowing the term.",
                    "compound_inheritance": "case-by-case",
                },
            }
        }

        issues = lint_terms.check_translation_policy_consistency(terms)

        self.assertIn(
            "nibbana.json: untranslated-preferred policy should explain leave_untranslated_when in translation_policy",
            issues,
        )

    def test_translation_policy_inherit_requires_compound_note(self) -> None:
        terms = {
            "sati": {
                "entry_type": "major",
                "notes": "Default path-factor rendering.",
                "context_rules": [{"context": "most path contexts", "rendering": "remembering"}],
                "translation_policy": {
                    "default_scope": "path contexts",
                    "compound_inheritance": "inherit",
                    "drift_risk": "Avoid mindfulness drift.",
                },
            }
        }

        issues = lint_terms.check_translation_policy_consistency(terms)

        self.assertIn(
            "sati.json: translation_policy sets compound_inheritance to inherit but notes/context_rules do not mention compounds",
            issues,
        )

    def test_authority_basis_sources_should_appear_in_notes(self) -> None:
        terms = {
            "dukkha": {
                "notes": "House preference is dissatisfaction.",
                "authority_basis": [
                    {
                        "source": "OSF glossary",
                        "scope": "Supports the preferred translation.",
                    }
                ],
            }
        }

        issues = lint_terms.check_authority_basis_consistency(terms)

        self.assertEqual(
            issues,
            [
                "dukkha.json: authority_basis[1] source 'OSF glossary' is not reflected in notes"
            ],
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
            "sati": {
                "entry_type": "major",
                "status": "reviewed",
                "notes": "Rule-bearing note.",
                "context_rules": [{"context": "default", "rendering": "remembering"}, {"context": "alt", "rendering": "sati"}],
                "related_terms": ["samadhi"],
                "example_phrases": [{"pali": "sati"}],
                "sutta_references": ["MN 10"],
            },
            "samadhi": {
                "entry_type": "major",
                "status": "reviewed",
                "notes": "Rule-bearing note.",
                "context_rules": [{"context": "default", "rendering": "mental composure"}, {"context": "alt", "rendering": "composure"}],
                "related_terms": [],
                "example_phrases": [{"pali": "samādhi"}],
                "sutta_references": ["MN 44"],
            },
        }

        with mock.patch.object(lint_terms, "load_terms", return_value=terms):
            with mock.patch.object(lint_terms, "STABILIZED_RULE_TERMS", {"sati"}):
                with mock.patch("sys.argv", ["lint_terms.py"]):
                    with mock.patch("sys.stdout", output):
                        result = lint_terms.main()

        self.assertEqual(result, 0)
        self.assertIn("Editorial lint warnings:", output.getvalue())
        self.assertIn("Completed with 1 warning(s).", output.getvalue())

    def test_main_returns_warning_exit_code_one_with_strict(self) -> None:
        output = io.StringIO()
        terms = {
            "sati": {
                "entry_type": "major",
                "status": "reviewed",
                "notes": "Rule-bearing note.",
                "context_rules": [{"context": "default", "rendering": "remembering"}, {"context": "alt", "rendering": "sati"}],
                "related_terms": ["samadhi"],
                "example_phrases": [{"pali": "sati"}],
                "sutta_references": ["MN 10"],
            },
            "samadhi": {
                "entry_type": "major",
                "status": "reviewed",
                "notes": "Rule-bearing note.",
                "context_rules": [{"context": "default", "rendering": "mental composure"}, {"context": "alt", "rendering": "composure"}],
                "related_terms": [],
                "example_phrases": [{"pali": "samādhi"}],
                "sutta_references": ["MN 44"],
            },
        }

        with mock.patch.object(lint_terms, "load_terms", return_value=terms):
            with mock.patch.object(lint_terms, "STABILIZED_RULE_TERMS", {"sati"}):
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

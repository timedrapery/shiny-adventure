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
                "term": "samÃ„Âdhi",
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

    def test_major_reviewed_entries_require_example_sources(self) -> None:
        terms = {
            "dukkha": {
                "entry_type": "major",
                "status": "reviewed",
                "example_phrases": [
                    {"pali": "dukkha", "translation": "dissatisfaction"},
                    {"pali": "dukkha", "translation": "dissatisfaction", "source": "SN 12.2"},
                ],
            },
            "anicca": {
                "entry_type": "minor",
                "status": "reviewed",
                "example_phrases": [{"pali": "anicca", "translation": "impermanence"}],
            },
        }

        issues = lint_terms.check_missing_example_sources(terms)

        self.assertEqual(
            issues,
            ["dukkha.json: major reviewed entry has example_phrases missing source on item(s) 1"],
        )

    def test_major_reviewed_entries_warn_on_thin_governance_surfaces(self) -> None:
        terms = {
            "hetu": {
                "entry_type": "major",
                "status": "reviewed",
                "notes": "Cause.",
                "context_rules": [
                    {"context": "default", "rendering": "cause"},
                    {"context": "explanatory", "rendering": "reason"},
                ],
                "example_phrases": [{"pali": "hetu", "translation": "cause", "source": "AN 3.134"}],
            },
            "paccaya": {
                "entry_type": "major",
                "status": "stable",
                "notes": (
                    "The project keeps condition as the default in dependent-arising contexts, "
                    "distinguishes it from narrower cause-language, and uses the note to explain "
                    "the main drift risk the entry is meant to prevent in later translation work."
                ),
                "context_rules": [
                    {"context": "default", "rendering": "condition"},
                    {"context": "formula", "rendering": "condition"},
                ],
                "example_phrases": [
                    {"pali": "paccaya", "translation": "condition", "source": "SN 12.2"},
                    {"pali": "avijjāpaccayā saṅkhārā", "translation": "with ignorance as condition, putting together", "source": "SN 12.2"},
                ],
            },
        }

        issues = lint_terms.check_thin_governance_surfaces(terms)

        self.assertEqual(
            issues,
            [
                "hetu.json: major reviewed entry has a thin governance surface (context_rules=2, example_phrases=1, note_words=1); expand the note or add another rule/example"
            ],
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

    def test_reviewed_major_entries_cannot_keep_generic_authority_basis(self) -> None:
        terms = {
            "mannati": {
                "entry_type": "major",
                "status": "stable",
                "authority_basis": [
                    {
                        "source": "Repository editorial record",
                        "scope": "Placeholder provenance.",
                    }
                ],
            }
        }

        issues = lint_terms.check_generic_authority_basis_refinement(terms)

        self.assertEqual(
            issues,
            [
                "mannati.json: reviewed/stable major entry still uses generic authority_basis source 'Repository editorial record'; refine provenance before merge"
            ],
        )

    def test_collect_lint_results_groups_example_source_warnings(self) -> None:
        terms = {
            "dukkha": {
                "entry_type": "major",
                "status": "reviewed",
                "notes": "The OSF glossary supports the default translation here and the note explains the drift prevention logic in explicit project language.",
                "context_rules": [
                    {"context": "default", "rendering": "dissatisfaction"},
                    {"context": "contrast", "rendering": "stress"},
                ],
                "related_terms": ["nirodha"],
                "example_phrases": [{"pali": "dukkha", "translation": "dissatisfaction"}],
                "sutta_references": ["SN 12.2"],
                "translation_policy": {
                    "default_scope": "most doctrinal contexts",
                    "drift_risk": "Avoid suffering drift.",
                    "compound_inheritance": "case-by-case",
                },
                "authority_basis": [{"source": "OSF glossary", "scope": "Supports the project default."}],
            },
            "nirodha": {
                "entry_type": "major",
                "status": "reviewed",
                "notes": "The OSF glossary supports the default translation here and the note explains the drift prevention logic in explicit project language.",
                "context_rules": [
                    {"context": "default", "rendering": "quenching"},
                    {"context": "contrast", "rendering": "ending"},
                ],
                "related_terms": ["dukkha"],
                "example_phrases": [{"pali": "nirodha", "translation": "quenching", "source": "SN 12.2"}],
                "sutta_references": ["SN 12.2"],
                "translation_policy": {
                    "default_scope": "most doctrinal contexts",
                    "drift_risk": "Avoid cessation flattening.",
                    "compound_inheritance": "case-by-case",
                },
                "authority_basis": [{"source": "OSF glossary", "scope": "Supports the project default."}],
            },
        }

        errors, warnings = lint_terms.collect_lint_results(
            terms,
            enforce_stabilized_terms=False,
        )

        self.assertEqual(errors, {})
        self.assertEqual(
            warnings["Example Sources"],
            ["dukkha.json: major reviewed entry has example_phrases missing source on item(s) 1"],
        )

    def test_collect_lint_results_groups_thin_governance_warnings(self) -> None:
        terms = {
            "hetu": {
                "entry_type": "major",
                "status": "reviewed",
                "notes": "Cause.",
                "context_rules": [
                    {"context": "default", "rendering": "cause"},
                    {"context": "explanatory", "rendering": "reason"},
                ],
                "related_terms": ["paccaya"],
                "example_phrases": [{"pali": "hetu", "translation": "cause", "source": "AN 3.134"}],
                "sutta_references": ["AN 3.134"],
                "translation_policy": {
                    "default_scope": "most analytical contexts",
                    "drift_risk": "Avoid condition drift.",
                    "compound_inheritance": "case-by-case",
                },
            },
            "paccaya": {
                "entry_type": "major",
                "status": "reviewed",
                "notes": (
                    "The OSF glossary supports the default translation here, the note explains the "
                    "broader conditional scope, and it records the drift risk the project wants to "
                    "prevent when translators are tempted to collapse the term into cause-language."
                ),
                "context_rules": [
                    {"context": "default", "rendering": "condition"},
                    {"context": "formula", "rendering": "condition"},
                ],
                "related_terms": ["hetu"],
                "example_phrases": [
                    {"pali": "paccaya", "translation": "condition", "source": "SN 12.2"},
                    {"pali": "imasmiṃ sati idaṃ hoti", "translation": "when this is present, this comes to be", "source": "SN 12.61"},
                ],
                "sutta_references": ["SN 12.2"],
                "translation_policy": {
                    "default_scope": "most analytical contexts",
                    "drift_risk": "Avoid cause drift.",
                    "compound_inheritance": "case-by-case",
                },
                "authority_basis": [{"source": "OSF glossary", "scope": "Supports the project default."}],
            },
        }

        errors, warnings = lint_terms.collect_lint_results(
            terms,
            enforce_stabilized_terms=False,
        )

        self.assertEqual(errors, {})
        self.assertEqual(
            warnings["Governance Surface"],
            [
                "hetu.json: major reviewed entry has a thin governance surface (context_rules=2, example_phrases=1, note_words=1); expand the note or add another rule/example"
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
                "notes": (
                    "The project keeps remembering as the default, explains why mindfulness is not "
                    "the uncontrolled house default, and records the specific drift risk the entry "
                    "is meant to prevent in later path and practice translation work."
                ),
                "context_rules": [{"context": "default", "rendering": "remembering"}, {"context": "alt", "rendering": "sati"}],
                "related_terms": ["samadhi"],
                "example_phrases": [{"pali": "sati", "source": "MN 10"}, {"pali": "satipaṭṭhāna", "source": "DN 22"}],
                "sutta_references": ["MN 10"],
            },
            "samadhi": {
                "entry_type": "major",
                "status": "reviewed",
                "notes": (
                    "The project keeps mental composure as the default, explains the distinction "
                    "from generic concentration language, and records the practical drift risk the "
                    "entry is meant to prevent in later meditative translation work."
                ),
                "context_rules": [{"context": "default", "rendering": "mental composure"}, {"context": "alt", "rendering": "composure"}],
                "related_terms": [],
                "example_phrases": [{"pali": "samādhi", "source": "MN 44"}, {"pali": "sammā-samādhi", "source": "MN 117"}],
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
                "notes": (
                    "The project keeps remembering as the default, explains why mindfulness is not "
                    "the uncontrolled house default, and records the specific drift risk the entry "
                    "is meant to prevent in later path and practice translation work."
                ),
                "context_rules": [{"context": "default", "rendering": "remembering"}, {"context": "alt", "rendering": "sati"}],
                "related_terms": ["samadhi"],
                "example_phrases": [{"pali": "sati", "source": "MN 10"}, {"pali": "satipaṭṭhāna", "source": "DN 22"}],
                "sutta_references": ["MN 10"],
            },
            "samadhi": {
                "entry_type": "major",
                "status": "reviewed",
                "notes": (
                    "The project keeps mental composure as the default, explains the distinction "
                    "from generic concentration language, and records the practical drift risk the "
                    "entry is meant to prevent in later meditative translation work."
                ),
                "context_rules": [{"context": "default", "rendering": "mental composure"}, {"context": "alt", "rendering": "composure"}],
                "related_terms": [],
                "example_phrases": [{"pali": "samādhi", "source": "MN 44"}, {"pali": "sammā-samādhi", "source": "MN 117"}],
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

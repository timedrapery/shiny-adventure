from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


repo_health = load_module("repo_health", "scripts/repo_health.py")


class RepoHealthTests(unittest.TestCase):
    def test_build_report_tracks_missing_advanced_fields_and_source_gaps(self) -> None:
        terms = {
            "dukkha": {
                "entry_type": "major",
                "status": "stable",
                "preferred_translation": "dissatisfaction",
                "notes": "The default translation is dissatisfaction in most doctrinal contexts and this note explains the rule to prevent suffering drift.",
                "context_rules": [
                    {"context": "default doctrinal prose", "rendering": "dissatisfaction"},
                    {"context": "narrow practical gloss", "rendering": "stress"},
                ],
                "tags": ["core-doctrine"],
                "example_phrases": [{"pali": "dukkha", "translation": "dissatisfaction"}],
            },
            "vedana": {
                "entry_type": "major",
                "status": "reviewed",
                "preferred_translation": "feeling",
                "notes": "The default translation is feeling in most contexts, this note explains the distinction in direct rule-bearing language, and it records the drift risk the policy is meant to prevent in later translation work.",
                "context_rules": [
                    {"context": "default doctrinal prose", "rendering": "feeling"},
                    {"context": "threefold classification sheet", "rendering": "mixed feeling"},
                ],
                "authority_basis": [{"source": "OSF glossary", "scope": "default"}],
                "translation_policy": {
                    "default_scope": "default",
                    "when_not_to_apply": "Do not flatten this into emotion language.",
                    "compound_inheritance": "case-by-case",
                    "drift_risk": "Avoid sensation drift.",
                },
                "example_phrases": [{"pali": "vedanā", "source": "SN 12.2"}],
            },
            "sanna": {
                "entry_type": "minor",
                "status": "reviewed",
                "preferred_translation": "perception",
            },
        }

        report = repo_health.build_report(terms)

        self.assertEqual(report["summary"]["term_files"], 3)
        self.assertEqual(report["summary"]["major_terms"], 2)
        self.assertEqual(report["major_policy_coverage"]["authority_basis_missing"], ["dukkha"])
        self.assertEqual(report["major_policy_coverage"]["translation_policy_missing"], ["dukkha"])
        self.assertEqual(report["major_policy_coverage"]["generic_authority_basis"], [])
        self.assertEqual(
            report["example_source_gaps"],
            [{"term": "dukkha", "missing_example_indexes": [1], "total_examples": 1}],
        )
        self.assertEqual(
            report["example_source_gap_tags"],
            [{"tag": "core-doctrine", "terms_with_source_gaps": 1}],
        )
        self.assertEqual(
            report["rule_strength"]["weak_major_entries"],
            [
                {
                    "term": "dukkha",
                    "status": "stable",
                    "reasons": [
                        "missing_authority_basis",
                        "missing_translation_policy",
                    ],
                }
            ],
        )
        self.assertEqual(report["minor_governance"]["high_load_minors"], [])

    def test_build_report_groups_major_translation_collisions(self) -> None:
        terms = {
            "metta": {
                "entry_type": "major",
                "status": "stable",
                "preferred_translation": "friendliness",
                "example_phrases": [{"pali": "mettā", "source": "MN 7"}],
            },
            "karuna": {
                "entry_type": "major",
                "status": "stable",
                "preferred_translation": "friendliness",
                "example_phrases": [{"pali": "karuṇā", "source": "MN 7"}],
            },
        }

        collisions = repo_health.collect_preferred_translation_collisions(terms)

        self.assertEqual(
            collisions,
            [{"preferred_translation": "friendliness", "terms": ["karuna", "metta"]}],
        )

    def test_build_report_skips_disambiguated_major_translation_collisions(self) -> None:
        terms = {
            "citta": {
                "entry_type": "major",
                "status": "reviewed",
                "preferred_translation": "mind",
                "related_terms": ["mano"],
                "example_phrases": [{"pali": "citta", "source": "DN 22"}],
            },
            "mano": {
                "entry_type": "major",
                "status": "reviewed",
                "preferred_translation": "mind",
                "related_terms": ["citta"],
                "example_phrases": [{"pali": "mano", "source": "MN 148"}],
            },
        }

        collisions = repo_health.collect_preferred_translation_collisions(terms)

        self.assertEqual(collisions, [])

    def test_main_reports_missing_terms_directory(self) -> None:
        output = io.StringIO()

        with tempfile.TemporaryDirectory() as tmpdir:
            missing_dir = Path(tmpdir) / "missing-terms"
            with mock.patch.object(repo_health, "TERMS_DIR", missing_dir):
                with mock.patch("sys.argv", ["repo_health.py"]):
                    with mock.patch("sys.stdout", output):
                        result = repo_health.main()

        self.assertEqual(result, 1)
        self.assertIn("ERROR: Terms directory not found", output.getvalue())

    def test_main_supports_json_output(self) -> None:
        output = io.StringIO()
        terms = {
            "sati": {
                "entry_type": "major",
                "status": "stable",
                "preferred_translation": "remembering",
                "authority_basis": [{"source": "OSF glossary", "scope": "default"}],
                "translation_policy": {"default_scope": "most contexts"},
                "example_phrases": [{"pali": "sati", "source": "MN 10"}],
            }
        }

        with mock.patch.object(repo_health, "load_terms", return_value=terms):
            with mock.patch("sys.argv", ["repo_health.py", "--format", "json"]):
                with mock.patch("sys.stdout", output):
                    result = repo_health.main()

        self.assertEqual(result, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["summary"]["major_terms"], 1)

    def test_build_report_includes_generic_authority_basis_details(self) -> None:
        terms = {
            "abhijanati": {
                "entry_type": "major",
                "status": "stable",
                "preferred_translation": "directly knows",
                "tags": ["core-doctrine", "verbal-knowing-cluster"],
                "authority_basis": [
                    {"source": "Repository editorial record", "scope": "Placeholder provenance."}
                ],
                "example_phrases": [{"pali": "abhijānāti", "source": "MN 1"}],
            }
        }

        report = repo_health.build_report(terms)

        self.assertEqual(
            report["major_policy_coverage"]["generic_authority_basis"],
            [
                {
                    "term": "abhijanati",
                    "status": "stable",
                    "tags": ["core-doctrine", "verbal-knowing-cluster"],
                }
            ],
        )

    def test_build_report_surfaces_weak_major_rule_entries(self) -> None:
        terms = {
            "sati": {
                "entry_type": "major",
                "status": "reviewed",
                "preferred_translation": "remembering",
                "notes": "Memory.",
                "context_rules": [
                    {"context": "path factor", "rendering": "right remembering"},
                    {"context": "source-facing prose", "rendering": "sati"},
                ],
                "authority_basis": [],
                "translation_policy": {},
                "example_phrases": [{"pali": "sati", "source": "MN 10"}],
            }
        }

        report = repo_health.build_report(terms)

        self.assertEqual(
            report["rule_strength"]["weak_major_entries"],
            [
                {
                    "term": "sati",
                    "status": "reviewed",
                    "reasons": [
                        "thin_notes",
                        "missing_authority_basis",
                        "missing_default_scope",
                        "missing_when_not_to_apply",
                        "missing_compound_inheritance",
                        "missing_drift_risk",
                        "preferred_not_in_context_rules",
                    ],
                }
            ],
        )

    def test_build_report_surfaces_high_load_minor_queue(self) -> None:
        terms = {
            "asavanam-khaya": {
                "entry_type": "minor",
                "status": "reviewed",
                "part_of_speech": "phrase",
                "preferred_translation": "through the wearing away of the outflows",
                "notes": "Whole-phrase liberation formula.",
                "example_phrases": [{"pali": "āsavānaṁ khayā", "source": "MN 2"}],
                "sutta_references": ["MN 2", "MN 36"],
                "tags": ["core-doctrine", "formula", "liberation", "translation-sensitive"],
            }
        }

        report = repo_health.build_report(terms)

        self.assertEqual(
            report["minor_governance"]["high_load_minors"],
            [
                {
                    "term": "asavanam-khaya",
                    "status": "reviewed",
                    "score": 11,
                    "missing_fields": ["translation_policy"],
                    "sutta_reference_count": 2,
                    "tags": ["core-doctrine", "formula", "liberation", "translation-sensitive"],
                }
            ],
        )

    def test_build_report_flags_slug_naming_a_different_phrase(self) -> None:
        terms = {
            "pancime-bhikkhave-upadanakkhandha": {
                "term": "katame ca, bhikkhave, pañcupādānakkhandhā",
                "normalized_term": "pancime-bhikkhave-upadanakkhandha",
                "entry_type": "minor",
                "part_of_speech": "phrase",
                "status": "stable",
            }
        }

        report = repo_health.build_report(terms)

        self.assertEqual(
            report["slug_headword_mismatches"],
            [
                {
                    "term": "pancime-bhikkhave-upadanakkhandha",
                    "headword": "katame ca, bhikkhave, pañcupādānakkhandhā",
                    "normalized_term": "pancime-bhikkhave-upadanakkhandha",
                    "orphan_tokens": ["pancime"],
                    "status": "stable",
                }
            ],
        )

    def test_build_report_allows_conventional_slug_respellings(self) -> None:
        terms = {
            # sandhi split out for readability
            "chanda-iddhipada": {
                "term": "chandiddhipāda",
                "normalized_term": "chanda-iddhipada",
                "entry_type": "minor",
                "part_of_speech": "compound",
                "status": "stable",
            },
            # sandhi collapsed instead
            "sammapadhana": {
                "term": "sammappadhāna",
                "normalized_term": "sammapadhana",
                "entry_type": "minor",
                "part_of_speech": "compound",
                "status": "stable",
            },
            # descriptive label keyed to its sutta
            "mn10-direct-path-opening": {
                "term": "ekāyano ayaṁ, bhikkhave, maggo sattānaṁ visuddhiyā",
                "normalized_term": "mn10-direct-path-opening",
                "entry_type": "minor",
                "part_of_speech": "phrase",
                "status": "stable",
            },
            # house -formula suffix
            "kim-nidana-kim-samudaya-formula": {
                "term": "kiṁnidānaṁ kiṁsamudayaṁ",
                "normalized_term": "kim-nidana-kim-samudaya-formula",
                "entry_type": "minor",
                "part_of_speech": "phrase",
                "status": "stable",
            },
        }

        report = repo_health.build_report(terms)

        self.assertEqual(report["slug_headword_mismatches"], [])

    def test_build_report_allows_inflected_formula_slug_stems(self) -> None:
        terms = {
            "panca-brahmana-dhamma": {
                "term": "pañcahi dhammehi samannāgato brāhmaṇo",
                "normalized_term": "panca-brahmana-dhamma",
                "entry_type": "minor",
                "part_of_speech": "phrase",
                "status": "reviewed",
            }
        }
        report = repo_health.build_report(terms)
        self.assertEqual(report["slug_headword_mismatches"], [])

    def test_declaration_regex_reads_both_house_shapes(self) -> None:
        matches = repo_health.RENDERING_DECLARATION.findall(
            "`pīti` is rendered `rejoicing`, and `sukha` → `satisfaction`."
        )
        self.assertEqual(
            matches, [("pīti", "rejoicing"), ("sukha", "satisfaction")]
        )

    def test_canonical_rendering_folds_wrapping_case_and_final_stop(self) -> None:
        # declarations are hard-wrapped at 79 columns, so the same phrase
        # arrives with a newline inside it
        self.assertEqual(
            repo_health.canonical_rendering("clear\n  knowing."),
            repo_health.canonical_rendering("Clear knowing"),
        )

    def test_flags_a_document_declaring_two_renderings_for_one_headword(self) -> None:
        # the trace the piti delight -> rejoicing migration left behind while
        # it sat half-finished
        terms = {
            "piti": {
                "term": "pīti",
                "normalized_term": "piti",
                "entry_type": "major",
                "preferred_translation": "rejoicing",
                "alternative_translations": ["delight"],
                "status": "reviewed",
            }
        }
        declarations = {
            "an10-60-giriminanda-sutta-notes.md": [
                ("pīti", "rejoicing"),
                ("pīti", "delight"),
            ]
        }

        report = repo_health.build_report(terms, declarations)

        self.assertEqual(
            report["governed_rendering_drift"],
            [
                {
                    "document": "an10-60-giriminanda-sutta-notes.md",
                    "headword": "pīti",
                    "kind": "self_contradiction",
                    "declared": ["delight", "rejoicing"],
                    "preferred": "rejoicing",
                }
            ],
        )

    def test_does_not_call_noun_and_verb_a_self_contradiction(self) -> None:
        terms = {
            "nibbida": {
                "term": "nibbidā",
                "normalized_term": "nibbida",
                "entry_type": "major",
                "preferred_translation": "disenchantment",
                "alternative_translations": ["grows disenchanted"],
                "status": "reviewed",
            }
        }
        declarations = {"a.md": [("nibbidā", "disenchantment"), ("nibbindati", "grows disenchanted")]}
        report = repo_health.build_report(terms, declarations)
        self.assertFalse(any(item["kind"] == "self_contradiction" for item in report["governed_rendering_drift"]))

    def test_flags_a_declared_rendering_the_record_discourages(self) -> None:
        terms = {
            "sukha": {
                "term": "sukha",
                "normalized_term": "sukha",
                "entry_type": "major",
                "preferred_translation": "satisfaction",
                "discouraged_translations": ["happiness"],
                "status": "reviewed",
            }
        }
        declarations = {"mn39-maha-assapura-sutta.md": [("sukha", "happiness")]}

        report = repo_health.build_report(terms, declarations)
        drift = report["governed_rendering_drift"]

        self.assertEqual(len(drift), 1)
        self.assertEqual(drift[0]["kind"], "discouraged")

    def test_allows_alternates_and_context_rule_renderings(self) -> None:
        terms = {
            "piti": {
                "term": "pīti",
                "normalized_term": "piti",
                "entry_type": "major",
                "preferred_translation": "rejoicing",
                "alternative_translations": ["delight"],
                "context_rules": [
                    {"context": "explanatory prose", "rendering": "joy"}
                ],
                "status": "reviewed",
            }
        }
        declarations = {
            "a.md": [("pīti", "rejoicing")],
            "b.md": [("pīti", "delight")],
            "c.md": [("pīti", "joy")],
        }

        report = repo_health.build_report(terms, declarations)

        self.assertEqual(report["governed_rendering_drift"], [])

    def test_json_output_is_ascii_safe(self) -> None:
        # CI writes this report with `> repo-health.json`. On Windows a
        # redirected stdout is cp1252, and dumping raw Pali diacritics there
        # raises partway through the write, leaving truncated JSON with a
        # traceback inside it.
        report = {"headword": "aniccā sabbasaṅkhārā"}
        encoded = json.dumps(report, ensure_ascii=True, indent=2)

        encoded.encode("cp1252")  # must not raise
        self.assertEqual(json.loads(encoded)["headword"], "aniccā sabbasaṅkhārā")

    def test_skips_headwords_with_no_record_of_their_own(self) -> None:
        # inflected forms and compounds are declared constantly and are not
        # drift; there is nothing to compare them against
        declarations = {"a.md": [("taṇhākkhayo", "the wearing away of wanting")]}

        report = repo_health.build_report({}, declarations)

        self.assertEqual(report["governed_rendering_drift"], [])


if __name__ == "__main__":
    unittest.main()

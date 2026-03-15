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
                "tags": ["core-doctrine"],
                "example_phrases": [{"pali": "dukkha", "translation": "dissatisfaction"}],
            },
            "vedana": {
                "entry_type": "major",
                "status": "reviewed",
                "preferred_translation": "feeling",
                "authority_basis": [{"source": "OSF glossary", "scope": "default"}],
                "translation_policy": {"default_scope": "default"},
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


if __name__ == "__main__":
    unittest.main()

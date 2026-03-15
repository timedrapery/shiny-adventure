from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


validate_terms = load_module("validate_terms", "scripts/validate_terms.py")


class ValidateTermsTests(unittest.TestCase):
    def test_main_reports_missing_schema_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            terms_dir = tmp_path / "terms"
            terms_dir.mkdir()
            output = io.StringIO()

            with mock.patch.object(validate_terms, "SCHEMA_PATH", tmp_path / "missing-schema.json"):
                with mock.patch.object(validate_terms, "TERMS_DIR", terms_dir):
                    with mock.patch("sys.stdout", output):
                        result = validate_terms.main()

        self.assertEqual(result, 1)
        self.assertIn("ERROR: Schema file not found", output.getvalue())

    def test_main_reports_invalid_json_term_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            schema_path = tmp_path / "schema.json"
            terms_dir = tmp_path / "terms"
            term_path = terms_dir / "sati.json"
            terms_dir.mkdir()
            schema_path.write_text(
                json.dumps(
                    {
                        "type": "object",
                        "properties": {"term": {"type": "string"}},
                        "required": ["term"],
                    }
                ),
                encoding="utf-8",
            )
            term_path.write_text('{"term": "sati"', encoding="utf-8")
            output = io.StringIO()

            with mock.patch.object(validate_terms, "SCHEMA_PATH", schema_path):
                with mock.patch.object(validate_terms, "TERMS_DIR", terms_dir):
                    with mock.patch("sys.stdout", output):
                        result = validate_terms.main()

        self.assertEqual(result, 1)
        self.assertIn("Schema validation failed:", output.getvalue())
        self.assertIn("invalid JSON", output.getvalue())

    def test_main_reports_filename_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            schema_path = tmp_path / "schema.json"
            terms_dir = tmp_path / "terms"
            term_path = terms_dir / "sati.json"
            terms_dir.mkdir()
            schema_path.write_text(
                json.dumps(
                    {
                        "type": "object",
                        "properties": {
                            "term": {"type": "string"},
                            "normalized_term": {"type": "string"},
                        },
                        "required": ["term", "normalized_term"],
                    }
                ),
                encoding="utf-8",
            )
            term_path.write_text(
                json.dumps({"term": "sati", "normalized_term": "samadhi"}),
                encoding="utf-8",
            )
            output = io.StringIO()

            with mock.patch.object(validate_terms, "SCHEMA_PATH", schema_path):
                with mock.patch.object(validate_terms, "TERMS_DIR", terms_dir):
                    with mock.patch("sys.stdout", output):
                        result = validate_terms.main()

        self.assertEqual(result, 1)
        self.assertIn("does not match filename stem", output.getvalue())

    def test_main_reports_duplicate_headwords(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            schema_path = tmp_path / "schema.json"
            terms_dir = tmp_path / "terms"
            terms_dir.mkdir()
            schema_path.write_text(
                json.dumps(
                    {
                        "type": "object",
                        "properties": {
                            "term": {"type": "string"},
                            "normalized_term": {"type": "string"},
                        },
                        "required": ["term", "normalized_term"],
                    }
                ),
                encoding="utf-8",
            )
            (terms_dir / "sati.json").write_text(
                json.dumps({"term": "sati", "normalized_term": "sati"}),
                encoding="utf-8",
            )
            (terms_dir / "sati_2.json").write_text(
                json.dumps({"term": "sati", "normalized_term": "sati_2"}),
                encoding="utf-8",
            )
            output = io.StringIO()

            with mock.patch.object(validate_terms, "SCHEMA_PATH", schema_path):
                with mock.patch.object(validate_terms, "TERMS_DIR", terms_dir):
                    with mock.patch("sys.stdout", output):
                        result = validate_terms.main()

        self.assertEqual(result, 1)
        self.assertIn("term 'sati' is duplicated across files", output.getvalue())

    def test_main_reports_preferred_translation_collisions_as_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            schema_path = tmp_path / "schema.json"
            terms_dir = tmp_path / "terms"
            terms_dir.mkdir()
            schema_path.write_text(
                json.dumps(
                    {
                        "type": "object",
                        "properties": {
                            "term": {"type": "string"},
                            "normalized_term": {"type": "string"},
                            "entry_type": {"type": "string"},
                            "preferred_translation": {"type": "string"},
                        },
                        "required": [
                            "term",
                            "normalized_term",
                            "entry_type",
                            "preferred_translation",
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (terms_dir / "citta.json").write_text(
                json.dumps(
                    {
                        "term": "citta",
                        "normalized_term": "citta",
                        "entry_type": "major",
                        "preferred_translation": "mind",
                    }
                ),
                encoding="utf-8",
            )
            (terms_dir / "mano.json").write_text(
                json.dumps(
                    {
                        "term": "mano",
                        "normalized_term": "mano",
                        "entry_type": "major",
                        "preferred_translation": "mind",
                    }
                ),
                encoding="utf-8",
            )
            output = io.StringIO()

            with mock.patch.object(validate_terms, "SCHEMA_PATH", schema_path):
                with mock.patch.object(validate_terms, "TERMS_DIR", terms_dir):
                    with mock.patch("sys.stdout", output):
                        result = validate_terms.main()

        self.assertEqual(result, 0)
        self.assertIn("Warnings:", output.getvalue())
        self.assertIn("major preferred_translation collision 'mind'", output.getvalue())


if __name__ == "__main__":
    unittest.main()

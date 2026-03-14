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


if __name__ == "__main__":
    unittest.main()

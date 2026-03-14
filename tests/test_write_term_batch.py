from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


write_term_batch = load_module("write_term_batch", "scripts/write_term_batch.py")


class WriteTermBatchTests(unittest.TestCase):
    def test_validate_record_rejects_placeholder_text(self) -> None:
        record = {
            "normalized_term": "sangha",
            "term": "sa?gha",
            "definition": "The community.",
        }

        with self.assertRaisesRegex(ValueError, "contains '\\?'"):
            write_term_batch.validate_record(record, 1)

    def test_main_writes_utf8_json(self) -> None:
        record = {
            "term": "sa\u1e45gha",
            "normalized_term": "sangha",
            "entry_type": "minor",
            "part_of_speech": "noun",
            "preferred_translation": "sa\u1e45gha",
            "alternative_translations": ["community"],
            "discouraged_translations": ["church"],
            "untranslated_preferred": True,
            "definition": "The noble community.",
            "gloss_on_first_occurrence": "sa\u1e45gha (community)",
            "status": "reviewed",
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            batch_path = tmp_path / "batch.json"
            output_dir = tmp_path / "terms"
            output_dir.mkdir()
            batch_path.write_text(
                json.dumps([record], ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            with mock.patch.object(write_term_batch, "TERMS_DIR", output_dir):
                with mock.patch("sys.argv", ["write_term_batch.py", str(batch_path)]):
                    result = write_term_batch.main()

            self.assertEqual(result, 0)
            output_path = output_dir / "sangha.json"
            self.assertTrue(output_path.exists())
            contents = output_path.read_text(encoding="utf-8")
            self.assertIn("sa\u1e45gha", contents)
            self.assertNotIn("\\u1e45", contents)
            self.assertIn(b"sa\xe1\xb9\x85gha", output_path.read_bytes())

    def test_main_rejects_schema_invalid_batch(self) -> None:
        record = {
            "term": "sa\u1e45gha",
            "normalized_term": "sangha",
            "part_of_speech": "noun",
            "preferred_translation": "sa\u1e45gha",
            "definition": "The noble community.",
            "status": "reviewed",
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            batch_path = tmp_path / "batch.json"
            output_dir = tmp_path / "terms"
            output_dir.mkdir()
            batch_path.write_text(
                json.dumps([record], ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            with mock.patch.object(write_term_batch, "TERMS_DIR", output_dir):
                with mock.patch("sys.argv", ["write_term_batch.py", str(batch_path)]):
                    result = write_term_batch.main()

            self.assertEqual(result, 1)
            self.assertFalse((output_dir / "sangha.json").exists())

    def test_main_rejects_lint_invalid_batch(self) -> None:
        record = {
            "term": "nibb\u0101na",
            "normalized_term": "nibbana",
            "entry_type": "minor",
            "part_of_speech": "noun",
            "preferred_translation": "nibb\u0101na",
            "untranslated_preferred": True,
            "definition": "Liberation.",
            "status": "reviewed",
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            batch_path = tmp_path / "batch.json"
            output_dir = tmp_path / "terms"
            output_dir.mkdir()
            batch_path.write_text(
                json.dumps([record], ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            with mock.patch.object(write_term_batch, "TERMS_DIR", output_dir):
                with mock.patch("sys.argv", ["write_term_batch.py", str(batch_path)]):
                    result = write_term_batch.main()

            self.assertEqual(result, 1)
            self.assertFalse((output_dir / "nibbana.json").exists())


if __name__ == "__main__":
    unittest.main()

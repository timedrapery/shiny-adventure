from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_module(module_name: str, relative_path: str):
    path = REPO_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lint_terms = load_module("lint_terms", "scripts/lint_terms.py")
write_term_batch = load_module("write_term_batch", "scripts/write_term_batch.py")


class LintEncodingTests(unittest.TestCase):
    def test_placeholder_text_is_reported(self) -> None:
        terms = {
            "sangha": {
                "term": "sa?gha",
                "preferred_translation": "saṅgha",
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
            "term": "saṅgha",
            "normalized_term": "sangha",
            "entry_type": "minor",
            "part_of_speech": "noun",
            "preferred_translation": "saṅgha",
            "alternative_translations": ["community"],
            "discouraged_translations": ["church"],
            "untranslated_preferred": True,
            "definition": "The noble community.",
            "gloss_on_first_occurrence": "saṅgha (community)",
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
            self.assertIn("saṅgha", contents)
            self.assertNotIn("\\u1e45", contents)
            self.assertIn(b"sa\xe1\xb9\x85gha", output_path.read_bytes())


if __name__ == "__main__":
    unittest.main()

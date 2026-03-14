from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


scaffold_policy_metadata = load_module(
    "scaffold_policy_metadata", "scripts/scaffold_policy_metadata.py"
)


class ScaffoldPolicyMetadataTests(unittest.TestCase):
    def test_build_translation_policy_placeholder_adds_untranslated_guidance(self) -> None:
        policy = scaffold_policy_metadata.build_translation_policy_placeholder(
            {
                "preferred_translation": "nibbāna",
                "untranslated_preferred": True,
            }
        )

        self.assertIn("leave_untranslated_when", policy)

    def test_scaffold_file_populates_missing_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "sati.json"
            path.write_text(
                json.dumps(
                    {
                        "term": "sati",
                        "normalized_term": "sati",
                        "entry_type": "major",
                        "part_of_speech": "noun",
                        "preferred_translation": "remembering",
                        "definition": "Remembering.",
                        "status": "reviewed",
                    }
                ),
                encoding="utf-8",
            )

            changed = scaffold_policy_metadata.scaffold_file(path)
            payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertTrue(changed)
        self.assertIn("authority_basis", payload)
        self.assertIn("translation_policy", payload)

    def test_main_supports_check_only(self) -> None:
        output = io.StringIO()
        terms = {
            "sati": {
                "entry_type": "major",
                "preferred_translation": "remembering",
            }
        }

        with mock.patch.object(
            scaffold_policy_metadata,
            "select_targets",
            return_value=[Path("terms") / "sati.json"],
        ):
            with mock.patch("sys.argv", ["scaffold_policy_metadata.py", "--check-only", "sati"]):
                with mock.patch("sys.stdout", output):
                    result = scaffold_policy_metadata.main()

        self.assertEqual(result, 0)
        self.assertIn("Would scaffold 1 file(s).", output.getvalue())


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


draft_major_review_queue = load_module(
    "draft_major_review_queue", "scripts/draft_major_review_queue.py"
)


class DraftMajorReviewQueueTests(unittest.TestCase):
    def test_build_report_tracks_draft_major_entries_and_tags(self) -> None:
        terms = {
            "sati": {
                "term": "sati",
                "entry_type": "major",
                "status": "draft",
                "preferred_translation": "remembering",
                "tags": ["core-practice", "mental-qualities"],
                "related_terms": ["samadhi"],
                "sutta_references": ["MN 10"],
            },
            "samadhi": {
                "term": "samādhi",
                "entry_type": "major",
                "status": "reviewed",
                "preferred_translation": "mental composure",
                "tags": ["core-practice"],
            },
            "vedana": {
                "term": "vedanā",
                "entry_type": "minor",
                "status": "draft",
                "preferred_translation": "feeling",
            },
        }

        report = draft_major_review_queue.build_report(terms)

        self.assertEqual(report["summary"]["draft_major_terms"], 1)
        self.assertEqual(report["summary"]["major_terms"], 2)
        self.assertEqual(report["tag_clusters"], [{"tag": "core-practice", "draft_terms": 1}, {"tag": "mental-qualities", "draft_terms": 1}])
        self.assertEqual(report["queue"][0]["normalized_term"], "sati")

    def test_main_reports_missing_terms_directory(self) -> None:
        output = io.StringIO()

        with tempfile.TemporaryDirectory() as tmpdir:
            missing_dir = Path(tmpdir) / "missing-terms"
            with mock.patch.object(draft_major_review_queue, "TERMS_DIR", missing_dir):
                with mock.patch("sys.argv", ["draft_major_review_queue.py"]):
                    with mock.patch("sys.stdout", output):
                        result = draft_major_review_queue.main()

        self.assertEqual(result, 1)
        self.assertIn("ERROR: Terms directory not found", output.getvalue())

    def test_main_supports_json_output(self) -> None:
        output = io.StringIO()
        terms = {
            "sati": {
                "term": "sati",
                "entry_type": "major",
                "status": "draft",
                "preferred_translation": "remembering",
            }
        }

        with mock.patch.object(draft_major_review_queue, "load_terms", return_value=terms):
            with mock.patch("sys.argv", ["draft_major_review_queue.py", "--format", "json"]):
                with mock.patch("sys.stdout", output):
                    result = draft_major_review_queue.main()

        self.assertEqual(result, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["summary"]["draft_major_terms"], 1)


if __name__ == "__main__":
    unittest.main()

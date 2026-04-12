from __future__ import annotations

import json
import unittest
from pathlib import Path

from tests.helpers import load_module


REPO_ROOT = Path(__file__).resolve().parent.parent
surface_report = load_module(
    "practice_text_surface_report_policy",
    "scripts/practice_text_surface_report.py",
)


def load_term(path: str) -> dict[str, object]:
    with (REPO_ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class PracticeTextPolicyTests(unittest.TestCase):
    def test_shared_breathing_control_records_remain_stable(self) -> None:
        breathing = load_term("terms/minor/mn118-breathing-remembrance-line.json")
        whole_body = load_term("terms/minor/mn118-whole-body-training.json")
        body_conditioner = load_term("terms/minor/mn118-body-conditioner-training.json")

        self.assertEqual(
            breathing["preferred_translation"],
            "one breathes in remembering the Dhamma; one breathes out remembering the Dhamma",
        )
        self.assertEqual(
            whole_body["preferred_translation"],
            "one trains: 'Breathing in, I will experience the whole body.' One trains: 'Breathing out, I will experience the whole body.'",
        )
        self.assertEqual(
            body_conditioner["preferred_translation"],
            "one trains: 'Breathing in, I will calm the body conditioner.' One trains: 'Breathing out, I will calm the body conditioner.'",
        )

    def test_live_practice_text_surface_has_no_errors(self) -> None:
        report = surface_report.build_report(surface_report.load_terms())

        self.assertEqual(report["errors"]["missing_headwords"], [])
        self.assertEqual(report["errors"]["missing_supporting_terms"], [])
        self.assertEqual(report["errors"]["missing_control_records"], [])
        self.assertEqual(report["errors"]["control_example_source_gaps"], [])
        self.assertEqual(report["errors"]["missing_translation_surfaces"], [])
        self.assertEqual(report["errors"]["translation_control_line_gaps"], [])


if __name__ == "__main__":
    unittest.main()

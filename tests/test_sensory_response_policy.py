from __future__ import annotations

import json
import unittest
from pathlib import Path

from tests.helpers import load_module


REPO_ROOT = Path(__file__).resolve().parent.parent
surface_report = load_module(
    "sensory_response_surface_report_policy",
    "scripts/sensory_response_surface_report.py",
)


def load_term(path: str) -> dict[str, object]:
    with (REPO_ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class SensoryResponsePolicyTests(unittest.TestCase):
    def test_household_and_renunciation_labels_remain_stable(self) -> None:
        self.assertEqual(
            load_term("terms/minor/gehasita-somanassa.json")["preferred_translation"],
            "gladness tied to the household life",
        )
        self.assertEqual(
            load_term("terms/minor/nekkhammasita-upekkha.json")["preferred_translation"],
            "dynamic balance tied to renunciation",
        )

    def test_mn148_response_lines_remain_stable(self) -> None:
        self.assertEqual(
            load_term("terms/minor/mn148-pleasant-feeling-trained-response.json")["preferred_translation"],
            "when one is touched by pleasant feeling, one does not delight in it, does not affirm it, and does not keep taking it personally",
        )
        self.assertEqual(
            load_term("terms/minor/mn148-painful-feeling-untrained-response.json")["preferred_translation"],
            "when one is touched by painful feeling, one sorrows, grows worn down, laments, beats one's chest and cries, and falls into confusion",
        )
        self.assertEqual(
            load_term("terms/minor/mn148-mixed-feeling-undiscerned-response.json")["preferred_translation"],
            "when one is touched by mixed feeling, one does not discern that feeling's arising and vanishing, gratification, danger, and escape as they have come to be",
        )

    def test_live_sensory_response_surface_has_no_errors(self) -> None:
        report = surface_report.build_report(surface_report.load_terms())

        self.assertEqual(report["errors"]["missing_headwords"], [])
        self.assertEqual(report["errors"]["missing_supporting_terms"], [])
        self.assertEqual(report["errors"]["missing_control_records"], [])
        self.assertEqual(report["errors"]["control_example_source_gaps"], [])
        self.assertEqual(report["errors"]["missing_translation_surfaces"], [])
        self.assertEqual(report["errors"]["translation_control_line_gaps"], [])


if __name__ == "__main__":
    unittest.main()

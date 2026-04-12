from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


surface_report = load_module(
    "practice_text_surface_report",
    "scripts/practice_text_surface_report.py",
)


def make_record(stem: str, **overrides: object) -> dict[str, object]:
    data: dict[str, object] = {
        "term": stem,
        "normalized_term": stem,
        "entry_type": "major" if stem in surface_report.HEADWORD_TERMS else "minor",
        "part_of_speech": "phrase" if stem in surface_report.CONTROL_RECORDS else "noun",
        "preferred_translation": surface_report.EXPECTED_PREFERRED_TRANSLATIONS.get(
            stem, f"{stem} translation"
        ),
        "alternative_translations": [f"{stem} alt"],
        "discouraged_translations": [f"{stem} discouraged"],
        "definition": f"{stem} definition",
        "notes": f"{stem} note with enough detail to function as an editorial policy surface.",
        "context_rules": [
            {"context": "default", "rendering": f"{stem} translation", "notes": "default"},
        ],
        "related_terms": ["related-term"],
        "example_phrases": [{"pali": stem, "translation": f"{stem} translation", "source": "MN 10"}],
        "sutta_references": ["MN 10"],
        "tags": ["core-practice"],
        "authority_basis": [
            {"source": "source-a", "scope": "scope-a"},
            {"source": "source-b", "scope": "scope-b"},
        ],
        "translation_policy": {
            "default_scope": "default",
            "when_not_to_apply": "never",
            "compound_inheritance": "blocked",
            "drift_risk": "avoid drift",
        },
        "status": "reviewed",
    }
    data.update(overrides)
    return data


def write_required_surfaces(repo_root: Path) -> None:
    for surface in surface_report.TRANSLATION_SURFACE_REQUIREMENTS:
        path = repo_root / str(surface["relpath"])
        path.parent.mkdir(parents=True, exist_ok=True)
        text = "\n\n".join(
            surface_report.EXPECTED_PREFERRED_TRANSLATIONS[str(stem)]
            for stem in surface["required_terms"]
        )
        path.write_text(text + "\n", encoding="utf-8")


class PracticeTextSurfaceReportTests(unittest.TestCase):
    def test_build_report_flags_missing_control_records(self) -> None:
        terms = {
            stem: make_record(stem)
            for stem in surface_report.HEADWORD_TERMS + surface_report.SUPPORTING_TERMS
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            report = surface_report.build_report(terms, repo_root=Path(tmpdir))

        self.assertIn(
            "mn118-breathing-remembrance-line",
            report["errors"]["missing_control_records"],
        )

    def test_build_report_flags_missing_translation_control_line(self) -> None:
        stems = (
            surface_report.HEADWORD_TERMS
            + surface_report.SUPPORTING_TERMS
            + surface_report.CONTROL_RECORDS
        )
        terms = {stem: make_record(stem) for stem in stems}

        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            write_required_surfaces(repo_root)
            mn118_path = repo_root / "docs/translations/mn118-anapanasati-sutta.md"
            mn118_path.write_text(
                "One breathes in remembering the Dhamma; one breathes out remembering the Dhamma.\n",
                encoding="utf-8",
            )

            report = surface_report.build_report(terms, repo_root=repo_root)

        self.assertTrue(
            any(
                "mn118-whole-body-training" in item
                for item in report["errors"]["translation_control_line_gaps"]
            )
        )

    def test_write_outputs_creates_expected_file(self) -> None:
        stems = (
            surface_report.HEADWORD_TERMS
            + surface_report.SUPPORTING_TERMS
            + surface_report.CONTROL_RECORDS
        )
        terms = {stem: make_record(stem) for stem in stems}

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            with mock.patch.object(surface_report, "OUTPUT_DIR", output_dir):
                written = surface_report.write_outputs(terms)

        self.assertEqual(len(written), 1)
        self.assertEqual(written[0].name, "practice-text-control-sheet.md")

    def test_main_emits_json(self) -> None:
        output = io.StringIO()
        fake_report = {
            "summary": {
                "headwords_present": 1,
                "headwords_expected": 1,
                "supporting_terms_present": 1,
                "supporting_terms_expected": 1,
                "control_records_present": 1,
                "control_records_expected": 1,
                "translation_surfaces_present": 1,
                "translation_surfaces_expected": 1,
            },
            "errors": {
                "missing_headwords": [],
                "missing_supporting_terms": [],
                "missing_control_records": [],
                "control_example_source_gaps": [],
                "missing_translation_surfaces": [],
                "translation_control_line_gaps": [],
            },
            "warnings": {
                "headwords_with_thin_authority_basis": [],
                "supporting_terms_still_thin": [],
                "preferred_rendering_mismatches": [],
            },
        }

        with mock.patch.object(surface_report, "load_terms", return_value={}):
            with mock.patch.object(surface_report, "build_report", return_value=fake_report):
                with mock.patch("sys.argv", ["practice_text_surface_report.py", "--format", "json"]):
                    with mock.patch("sys.stdout", output):
                        result = surface_report.main()

        self.assertEqual(result, 0)
        parsed = json.loads(output.getvalue())
        self.assertEqual(parsed["summary"]["control_records_present"], 1)


if __name__ == "__main__":
    unittest.main()

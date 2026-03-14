from __future__ import annotations

import importlib.util
import io
import sys
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
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


audit_term_coverage = load_module("audit_term_coverage", "scripts/audit_term_coverage.py")


class CoverageAuditTests(unittest.TestCase):
    def test_family_progress_tracks_present_and_missing_terms(self) -> None:
        family = audit_term_coverage.CoverageFamily(
            "Training Trio",
            5,
            ("adhisila", "adhicitta", "adhipanna"),
        )
        terms = {
            "adhisila": {},
            "adhicitta": {},
        }

        present, missing = audit_term_coverage.family_progress(terms, family)

        self.assertEqual(present, ["adhisila", "adhicitta"])
        self.assertEqual(missing, ["adhipanna"])

    def test_candidate_scores_accumulate_weights_across_families(self) -> None:
        family_one = audit_term_coverage.CoverageFamily("Family One", 5, ("sati", "samadhi"))
        family_two = audit_term_coverage.CoverageFamily("Family Two", 7, ("samadhi", "panna"))
        terms = {"sati": {}}

        with mock.patch.object(audit_term_coverage, "COVERAGE_FAMILIES", (family_one, family_two)):
            ranked = audit_term_coverage.compute_candidate_scores(terms)

        self.assertEqual(
            ranked,
            [
                ("samadhi", 12, ["Family One", "Family Two"]),
                ("panna", 7, ["Family Two"]),
            ],
        )

    def test_main_reports_empty_term_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            output = io.StringIO()

            with mock.patch.object(audit_term_coverage, "TERMS_DIR", tmp_path):
                with mock.patch("sys.argv", ["audit_term_coverage.py"]):
                    with mock.patch("sys.stdout", output):
                        result = audit_term_coverage.main()

        self.assertEqual(result, 0)
        self.assertIn("WARNING: No term files found in terms/", output.getvalue())


if __name__ == "__main__":
    unittest.main()

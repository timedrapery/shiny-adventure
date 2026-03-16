from __future__ import annotations

import io
import subprocess
import sys
import unittest
from unittest import mock

from tests.helpers import load_module


run_checks = load_module("run_checks", "scripts/run_checks.py")


class RunChecksTests(unittest.TestCase):
    def test_main_runs_all_checks(self) -> None:
        output = io.StringIO()

        with mock.patch.object(run_checks.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)) as run_mock:
            with mock.patch("sys.stdout", output):
                result = run_checks.main()

        self.assertEqual(result, 0)
        self.assertEqual(run_mock.call_count, len(run_checks.CHECKS))
        self.assertIn(
            [sys.executable, "scripts/check_docs_integrity.py"],
            [call.args[0] for call in run_mock.call_args_list],
        )
        self.assertIn(
            [sys.executable, "scripts/check_translation_drift.py", "--strict"],
            [call.args[0] for call in run_mock.call_args_list],
        )
        self.assertIn(
            [sys.executable, "scripts/dependent_arising_cluster_report.py", "--strict"],
            [call.args[0] for call in run_mock.call_args_list],
        )
        self.assertIn(
            [sys.executable, "scripts/five_heaps_cluster_report.py", "--strict"],
            [call.args[0] for call in run_mock.call_args_list],
        )
        self.assertIn(
            [sys.executable, "scripts/identity_construction_cluster_report.py", "--strict"],
            [call.args[0] for call in run_mock.call_args_list],
        )
        self.assertIn(
            [sys.executable, "scripts/bondage_residue_cluster_report.py", "--strict"],
            [call.args[0] for call in run_mock.call_args_list],
        )
        self.assertIn(
            [sys.executable, "scripts/bondage_imagery_cluster_report.py", "--strict"],
            [call.args[0] for call in run_mock.call_args_list],
        )
        self.assertIn(
            [sys.executable, "scripts/abandonment_sequence_cluster_report.py", "--strict"],
            [call.args[0] for call in run_mock.call_args_list],
        )
        self.assertIn(
            [sys.executable, "scripts/crossing_release_interface_cluster_report.py", "--strict"],
            [call.args[0] for call in run_mock.call_args_list],
        )
        self.assertIn(
            [sys.executable, "scripts/consummation_interface_cluster_report.py", "--strict"],
            [call.args[0] for call in run_mock.call_args_list],
        )
        self.assertIn(
            [sys.executable, "scripts/osf_reconciliation_report.py", "--strict"],
            [call.args[0] for call in run_mock.call_args_list],
        )
        self.assertIn(
            [sys.executable, "scripts/craving_appropriation_cluster_report.py", "--strict"],
            [call.args[0] for call in run_mock.call_args_list],
        )
        self.assertIn(
            [sys.executable, "scripts/kama_cluster_report.py", "--strict"],
            [call.args[0] for call in run_mock.call_args_list],
        )
        self.assertIn(
            [sys.executable, "scripts/experience_process_cluster_report.py", "--strict"],
            [call.args[0] for call in run_mock.call_args_list],
        )
        self.assertIn("All checks passed.", output.getvalue())

    def test_main_stops_on_first_failure(self) -> None:
        output = io.StringIO()
        side_effect = [
            subprocess.CompletedProcess([], 0),
            subprocess.CompletedProcess([], 2),
        ]

        with mock.patch.object(run_checks.subprocess, "run", side_effect=side_effect) as run_mock:
            with mock.patch("sys.stdout", output):
                result = run_checks.main()

        self.assertEqual(result, 2)
        self.assertEqual(run_mock.call_count, 2)
        self.assertIn("Documentation integrity failed with exit code 2.", output.getvalue())


if __name__ == "__main__":
    unittest.main()

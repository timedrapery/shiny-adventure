from __future__ import annotations

import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


cluster_registry = load_module("cluster_registry", "scripts/cluster_registry.py")
check_cluster_surfaces = load_module(
    "check_cluster_surfaces",
    "scripts/check_cluster_surfaces.py",
)


class CheckClusterSurfacesTests(unittest.TestCase):
    def test_collect_issues_reports_missing_cluster_doc(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            scripts_dir = root / "scripts"
            tests_dir = root / "tests"
            scripts_dir.mkdir()
            tests_dir.mkdir()
            (scripts_dir / "demo_cluster_report.py").write_text("# demo\n", encoding="utf-8")
            (tests_dir / "test_demo_cluster_report.py").write_text("# demo\n", encoding="utf-8")

            cluster = cluster_registry.ClusterSurface(
                key="demo",
                label="Demo cluster",
                doc_relpath="docs/demo-cluster-map.md",
                script_relpath="scripts/demo_cluster_report.py",
                test_relpaths=("tests/test_demo_cluster_report.py",),
            )

            with mock.patch.object(check_cluster_surfaces, "REPO_ROOT", root):
                with mock.patch.object(check_cluster_surfaces, "SCRIPTS_DIR", scripts_dir):
                    with mock.patch.object(check_cluster_surfaces, "TESTS_DIR", tests_dir):
                        with mock.patch.object(check_cluster_surfaces, "CLUSTER_SURFACES", (cluster,)):
                            issues = check_cluster_surfaces.collect_issues()

        self.assertEqual(
            issues,
            ["demo: cluster authority doc is missing: docs/demo-cluster-map.md"],
        )

    def test_collect_issues_reports_unmanaged_cluster_script(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs_dir = root / "docs"
            scripts_dir = root / "scripts"
            tests_dir = root / "tests"
            docs_dir.mkdir()
            scripts_dir.mkdir()
            tests_dir.mkdir()
            (docs_dir / "demo-cluster-map.md").write_text("# demo\n", encoding="utf-8")
            (scripts_dir / "demo_cluster_report.py").write_text("# demo\n", encoding="utf-8")
            (tests_dir / "test_demo_cluster_report.py").write_text("# demo\n", encoding="utf-8")
            (scripts_dir / "rogue_cluster_report.py").write_text("# rogue\n", encoding="utf-8")

            cluster = cluster_registry.ClusterSurface(
                key="demo",
                label="Demo cluster",
                doc_relpath="docs/demo-cluster-map.md",
                script_relpath="scripts/demo_cluster_report.py",
                test_relpaths=("tests/test_demo_cluster_report.py",),
            )

            with mock.patch.object(check_cluster_surfaces, "REPO_ROOT", root):
                with mock.patch.object(check_cluster_surfaces, "DOCS_DIR", docs_dir):
                    with mock.patch.object(check_cluster_surfaces, "SCRIPTS_DIR", scripts_dir):
                        with mock.patch.object(check_cluster_surfaces, "TESTS_DIR", tests_dir):
                            with mock.patch.object(check_cluster_surfaces, "CLUSTER_SURFACES", (cluster,)):
                                issues = check_cluster_surfaces.collect_issues()

        self.assertEqual(
            issues,
            [
                "unmanaged cluster report script present without registry coverage: scripts/rogue_cluster_report.py"
            ],
        )

    def test_main_reports_success_when_all_cluster_surfaces_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs_dir = root / "docs"
            scripts_dir = root / "scripts"
            tests_dir = root / "tests"
            docs_dir.mkdir()
            scripts_dir.mkdir()
            tests_dir.mkdir()
            (docs_dir / "demo-cluster-map.md").write_text("# demo\n", encoding="utf-8")
            (scripts_dir / "demo_cluster_report.py").write_text("# demo\n", encoding="utf-8")
            (tests_dir / "test_demo_cluster_report.py").write_text("# demo\n", encoding="utf-8")

            cluster = cluster_registry.ClusterSurface(
                key="demo",
                label="Demo cluster",
                doc_relpath="docs/demo-cluster-map.md",
                script_relpath="scripts/demo_cluster_report.py",
                test_relpaths=("tests/test_demo_cluster_report.py",),
            )
            output = io.StringIO()

            with mock.patch.object(check_cluster_surfaces, "REPO_ROOT", root):
                with mock.patch.object(check_cluster_surfaces, "DOCS_DIR", docs_dir):
                    with mock.patch.object(check_cluster_surfaces, "SCRIPTS_DIR", scripts_dir):
                        with mock.patch.object(check_cluster_surfaces, "TESTS_DIR", tests_dir):
                            with mock.patch.object(check_cluster_surfaces, "CLUSTER_SURFACES", (cluster,)):
                                with mock.patch("sys.stdout", output):
                                    result = check_cluster_surfaces.main()

        self.assertEqual(result, 0)
        self.assertIn("Cluster surface coverage passed for 1 cluster(s).", output.getvalue())

    def test_issue_to_diagnostic_for_missing_doc_includes_repair_guidance(self) -> None:
        diagnostic = check_cluster_surfaces.issue_to_diagnostic(
            "demo: cluster authority doc is missing: docs/demo-cluster-map.md"
        )

        self.assertEqual(diagnostic.code, "missing_cluster_doc")
        self.assertEqual(diagnostic.file, "docs/demo-cluster-map.md")
        self.assertIn("authority doc", diagnostic.rule)
        self.assertIn("docs/", diagnostic.fix)
        self.assertIn("docs/knowledge-seeing-understanding-cluster-map.md", diagnostic.examples)


if __name__ == "__main__":
    unittest.main()

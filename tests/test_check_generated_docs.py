from __future__ import annotations

import tempfile
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace

from tests.helpers import load_module


check_generated_docs = load_module(
    "check_generated_docs",
    "scripts/check_generated_docs.py",
)


def write_fake_generator(repo_root: Path) -> None:
    scripts_dir = repo_root / "scripts"
    docs_dir = repo_root / "docs" / "generated"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)
    (scripts_dir / "fake_cluster_report.py").write_text(
        textwrap.dedent(
            """
            from pathlib import Path

            OUTPUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "generated"

            def load_terms():
                return {"fake": {"term": "fake"}}

            def write_outputs(terms):
                OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
                path = OUTPUT_DIR / "fake-generated.md"
                path.write_text("# Fake\\n\\nCurrent output.\\n", encoding="utf-8")
                return [path]
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )


class CheckGeneratedDocsTests(unittest.TestCase):
    def test_collect_generated_doc_failures_accepts_current_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            write_fake_generator(repo_root)
            (repo_root / "docs" / "generated" / "fake-generated.md").write_text(
                "# Fake\n\nCurrent output.\n",
                encoding="utf-8",
            )

            failures = check_generated_docs.collect_generated_doc_failures(
                repo_root,
                (
                    SimpleNamespace(
                        label="Fake cluster",
                        script_relpath="scripts/fake_cluster_report.py",
                    ),
                ),
            )

        self.assertEqual(failures, [])

    def test_collect_generated_doc_failures_reports_stale_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            write_fake_generator(repo_root)
            (repo_root / "docs" / "generated" / "fake-generated.md").write_text(
                "# Fake\n\nStale output.\n",
                encoding="utf-8",
            )

            failures = check_generated_docs.collect_generated_doc_failures(
                repo_root,
                (
                    SimpleNamespace(
                        label="Fake cluster",
                        script_relpath="scripts/fake_cluster_report.py",
                    ),
                ),
            )

        self.assertEqual(
            failures,
            ["Fake cluster: stale generated doc docs/generated/fake-generated.md"],
        )


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tests.helpers import load_module


refresh = load_module("refresh_derived", "scripts/refresh_derived.py")

REPO_ROOT = Path(__file__).resolve().parent.parent
OLD = "a" * 64


def make_repo(root: Path, recorded_hash: str = OLD) -> tuple:
    """A one-surface repository whose recorded hash may or may not be current."""

    (root / "docs").mkdir()
    (root / "reviews").mkdir()
    (root / "docs/t.md").write_text("# T\n\n## Translation\n\nBody text.\n", encoding="utf-8")
    surface = refresh.TranslationSurface(
        key="t1", label="T 1", main_relpath="docs/t.md", notes_relpath="docs/t-notes.md"
    )
    (root / "reviews/body-versions.json").write_text(
        json.dumps(
            {
                "_comment": "kept",
                "surfaces": {
                    "t1": {"body_sha256": recorded_hash, "revised_on": "2026-01-01"},
                    "gone": {"body_sha256": OLD, "revised_on": "2026-01-01"},
                },
            }
        ),
        encoding="utf-8",
    )
    return (surface,)


class BodyVersionTests(unittest.TestCase):
    def test_live_repository_has_no_stale_body_versions(self) -> None:
        self.assertEqual(refresh.stale_body_versions(), {})

    def test_changed_body_gets_its_hash_and_date_together(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            surfaces = make_repo(root)
            stale = refresh.stale_body_versions(surfaces, root)
            self.assertEqual(list(stale), ["t1"])
            self.assertEqual(stale["t1"][0], OLD)

            refresh.write_body_versions(stale, "2026-11-10", surfaces, root)

            data = json.loads((root / "reviews/body-versions.json").read_text(encoding="utf-8"))
            self.assertEqual(data["_comment"], "kept")
            self.assertEqual(
                data["surfaces"],
                {"t1": {"body_sha256": stale["t1"][1], "revised_on": "2026-11-10"}},
            )
            self.assertEqual(refresh.stale_body_versions(surfaces, root), {})

    def test_unchanged_body_keeps_its_date(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            surfaces = make_repo(root)
            current = refresh.translation_body_sha256(root / "docs/t.md")
            surfaces = make_repo_again(root, current)

            refresh.write_body_versions({}, "2026-11-10", surfaces, root)

            data = json.loads((root / "reviews/body-versions.json").read_text(encoding="utf-8"))
            self.assertEqual(data["surfaces"]["t1"]["revised_on"], "2026-01-01")


def make_repo_again(root: Path, recorded_hash: str) -> tuple:
    for path in (root / "docs/t.md", root / "reviews/body-versions.json"):
        path.unlink()
    (root / "docs").rmdir()
    (root / "reviews").rmdir()
    return make_repo(root, recorded_hash)


class OrphanedEvidenceTests(unittest.TestCase):
    def ledger(self, root: Path, record: dict) -> Path:
        path = root / "ledger.json"
        path.write_text(json.dumps({"surfaces": {"t1": record}}), encoding="utf-8")
        return path

    def test_evidence_bound_to_the_previous_body_is_named(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = self.ledger(
                root,
                {
                    "source_fidelity": {"status": "complete", "body_sha256": OLD},
                    "human_read_aloud": {"status": "complete", "body_sha256": OLD},
                    "newcomer_reviews": [{"body_sha256": OLD}, {"body_sha256": "b" * 64}],
                },
            )
            findings = refresh.orphaned_evidence({"t1": (OLD, "c" * 64)}, root, path)
            self.assertEqual(
                findings,
                [
                    "t1: source-fidelity sign-off",
                    "t1: read-aloud review",
                    "t1: 1 newcomer review(s)",
                ],
            )

    def test_open_gates_and_untouched_surfaces_are_not_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = self.ledger(
                root,
                {
                    "source_fidelity": {"status": "pending"},
                    "human_read_aloud": {"status": "pending", "reviewers": []},
                    "newcomer_reviews": [],
                },
            )
            self.assertEqual(refresh.orphaned_evidence({"t1": (OLD, "c" * 64)}, root, path), [])
            self.assertEqual(refresh.orphaned_evidence({}, root, path), [])

    def test_the_ledger_is_never_written(self) -> None:
        source = (REPO_ROOT / "scripts/refresh_derived.py").read_text(encoding="utf-8")
        self.assertEqual(source.count("write_text("), 1)
        self.assertIn("BODY_VERSIONS_RELPATH", source)


class GeneratorCoverageTests(unittest.TestCase):
    def test_every_generator_accepts_the_flag_it_is_given(self) -> None:
        for label, (script, flag) in refresh.generator_commands():
            with self.subTest(generator=label):
                source = (REPO_ROOT / script).read_text(encoding="utf-8")
                if "common.run_cli(" in source:
                    # Cluster reports share one command line.
                    source = (REPO_ROOT / "scripts" / "cluster_report_common.py").read_text(encoding="utf-8")
                self.assertIn(f'"{flag}"', source)

    def test_every_registered_generated_document_is_refreshed(self) -> None:
        scripts = {arguments[0] for _label, arguments in refresh.generator_commands()}
        for group in refresh.CLUSTER_SURFACES + refresh.NON_CLUSTER_GENERATED_SURFACES:
            self.assertIn(group.script_relpath, scripts)


if __name__ == "__main__":
    unittest.main()

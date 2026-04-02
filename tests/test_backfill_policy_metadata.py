from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock
import io

from tests.helpers import load_module


backfill_policy_metadata = load_module(
    "backfill_policy_metadata", "scripts/backfill_policy_metadata.py"
)


class BackfillPolicyMetadataTests(unittest.TestCase):
    def test_infer_authority_basis_uses_named_sources_when_notes_contain_them(self) -> None:
        basis = backfill_policy_metadata.infer_authority_basis(
            {
                "term": "sati",
                "notes": "The OSF glossary and Dhammarato both support this preference.",
            }
        )

        self.assertEqual(basis[0]["source"], "OSF glossary")
        self.assertEqual(basis[1]["source"], "Dhammarato")

    def test_infer_authority_basis_detects_hillside_stream(self) -> None:
        basis = backfill_policy_metadata.infer_authority_basis(
            {
                "term": "nimitta",
                "notes": "Hillside and Ñāṇamoli materials support the anti-objectifying handling here.",
            }
        )

        self.assertEqual(basis[0]["source"], "Hillside / Ñāṇamoli")

    def test_infer_authority_basis_detects_idappaccayata_support_profile(self) -> None:
        basis = backfill_policy_metadata.infer_authority_basis(
            {
                "term": "idappaccayata",
                "notes": "The Idappaccayatā practical talk profile reinforces the practical handling here.",
            }
        )

        self.assertEqual(basis[0]["source"], "Idappaccayatā practical talk profile")
        self.assertEqual(basis[0]["priority"], "buddhadasa-support")

    def test_infer_authority_basis_falls_back_to_repository_record(self) -> None:
        basis = backfill_policy_metadata.infer_authority_basis(
            {"term": "akusala", "notes": "The project prefers unwholesome."}
        )

        self.assertEqual(
            basis,
            [
                {
                    "source": "Repository editorial record",
                    "priority": "osf-house",
                    "kind": "rationale",
                    "scope": "Current house policy is preserved from the existing rule-bearing entry; source-specific provenance still needs refinement.",
                }
            ],
        )

    def test_infer_translation_policy_handles_untranslated_terms(self) -> None:
        policy = backfill_policy_metadata.infer_translation_policy(
            {
                "preferred_translation": "dhamma",
                "untranslated_preferred": True,
                "notes": "Keep the term untranslated.",
            }
        )

        self.assertIn("leave_untranslated_when", policy)

    def test_backfill_term_adds_missing_fields(self) -> None:
        updated, changed = backfill_policy_metadata.backfill_term(
            {
                "term": "akusala",
                "normalized_term": "akusala",
                "entry_type": "major",
                "preferred_translation": "unwholesome",
                "notes": "The project prefers unwholesome.",
                "discouraged_translations": ["bad"],
            }
        )

        self.assertTrue(changed)
        self.assertIn("authority_basis", updated)
        self.assertIn("translation_policy", updated)

    def test_main_check_only_reports_files_to_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            terms_dir = Path(tmpdir)
            (terms_dir / "akusala.json").write_text(
                json.dumps(
                    {
                        "term": "akusala",
                        "normalized_term": "akusala",
                        "entry_type": "major",
                        "preferred_translation": "unwholesome",
                        "notes": "The project prefers unwholesome.",
                        "discouraged_translations": ["bad"],
                    }
                ),
                encoding="utf-8",
            )

            original = backfill_policy_metadata.TERMS_DIR
            backfill_policy_metadata.TERMS_DIR = terms_dir
            try:
                with mock.patch("sys.argv", ["backfill_policy_metadata.py", "--check-only"]):
                    with mock.patch("sys.stdout", io.StringIO()):
                        result = backfill_policy_metadata.main()
            finally:
                backfill_policy_metadata.TERMS_DIR = original

        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()

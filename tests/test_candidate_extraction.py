from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


extract_candidate_terms = load_module(
    "extract_candidate_terms",
    "scripts/extract_candidate_terms.py",
)
generate_candidate_report = load_module(
    "generate_candidate_report",
    "scripts/generate_candidate_report.py",
)
scaffold_candidate_terms = load_module(
    "scaffold_candidate_terms",
    "scripts/scaffold_candidate_terms.py",
)


class CandidateExtractionTests(unittest.TestCase):
    def test_collect_candidates_ranks_unresolved_doctrinal_formula_highly(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            terms_dir = tmp_path / "terms"
            source_dir = tmp_path / "sources"
            terms_dir.mkdir()
            source_dir.mkdir()

            (terms_dir / "dukkha.json").write_text(
                json.dumps(
                    {
                        "term": "dukkha",
                        "normalized_term": "dukkha",
                        "entry_type": "major",
                        "part_of_speech": "noun",
                        "preferred_translation": "dissatisfaction",
                        "definition": "A core doctrinal term.",
                        "status": "stable",
                        "notes": "Rule-bearing note.",
                        "context_rules": [
                            {"context": "default", "rendering": "dissatisfaction", "notes": "Default."},
                            {"context": "alt", "rendering": "stress", "notes": "Alt."},
                        ],
                        "related_terms": ["nirodha"],
                        "example_phrases": [{"pali": "dukkha", "translation": "dissatisfaction"}],
                        "alternative_translations": ["stress"],
                        "discouraged_translations": ["suffering"],
                        "sutta_references": ["SN 56.11"],
                        "tags": ["core-doctrine"],
                    }
                ),
                encoding="utf-8",
            )
            (terms_dir / "nirodha.json").write_text(
                json.dumps(
                    {
                        "term": "nirodha",
                        "normalized_term": "nirodha",
                        "entry_type": "major",
                        "part_of_speech": "noun",
                        "preferred_translation": "quenching",
                        "definition": "Another core doctrinal term.",
                        "status": "stable",
                        "notes": "Rule-bearing note.",
                        "context_rules": [
                            {"context": "default", "rendering": "quenching", "notes": "Default."},
                            {"context": "alt", "rendering": "cessation", "notes": "Alt."},
                        ],
                        "related_terms": ["dukkha"],
                        "example_phrases": [{"pali": "nirodha", "translation": "quenching"}],
                        "alternative_translations": ["cessation"],
                        "discouraged_translations": ["annihilation"],
                        "sutta_references": ["SN 56.11"],
                        "tags": ["core-doctrine"],
                    }
                ),
                encoding="utf-8",
            )

            source_path = source_dir / "sample.txt"
            source_path.write_text(
                "dukkha nirodha dukkha nirodha\n"
                "dukkha-nirodha dukkha-nirodha\n"
                "sati ca ca ca\n",
                encoding="utf-8",
            )

            with mock.patch.object(extract_candidate_terms, "TERMS_DIR", terms_dir):
                documents = extract_candidate_terms.load_documents([source_path])
                report = extract_candidate_terms.collect_candidates(
                    documents,
                    extract_candidate_terms.load_lexicon_index(),
                )

        candidates = {item["normalized"]: item for item in report["candidates"]}
        self.assertEqual(candidates["dukkhanirodha"]["status"], "unresolved")
        self.assertEqual(candidates["dukkhanirodha"]["priority"], "create_now")
        self.assertEqual(candidates["dukkha"]["priority"], "ignore")

    def test_variant_of_existing_term_is_marked_for_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            terms_dir = tmp_path / "terms"
            source_dir = tmp_path / "sources"
            terms_dir.mkdir()
            source_dir.mkdir()

            (terms_dir / "pamojja.json").write_text(
                json.dumps(
                    {
                        "term": "pāmojja",
                        "normalized_term": "pamojja",
                        "entry_type": "minor",
                        "part_of_speech": "noun",
                        "preferred_translation": "gladness",
                        "definition": "Gladness.",
                        "status": "reviewed",
                    }
                ),
                encoding="utf-8",
            )
            source_path = source_dir / "variant.txt"
            source_path.write_text("pamoja pamoja", encoding="utf-8")

            with mock.patch.object(extract_candidate_terms, "TERMS_DIR", terms_dir):
                report = extract_candidate_terms.collect_candidates(
                    extract_candidate_terms.load_documents([source_path]),
                    extract_candidate_terms.load_lexicon_index(),
                )

        candidates = {item["normalized"]: item for item in report["candidates"]}
        self.assertEqual(candidates["pamoja"]["status"], "variant_of_existing")
        self.assertEqual(candidates["pamoja"]["priority"], "create_now")


class CandidateReportTests(unittest.TestCase):
    def test_markdown_report_groups_candidates_by_priority(self) -> None:
        report = {
            "source_documents": ["sources/sample.txt"],
            "summary": {
                "documents": 1,
                "total_candidates": 2,
                "priority_counts": {"create_now": 1, "review_soon": 1},
                "status_counts": {"unresolved": 2},
            },
            "candidates": [
                {
                    "text": "dukkha nirodha",
                    "total_count": 4,
                    "document_count": 1,
                    "status": "unresolved",
                    "matched_terms": ["dukkha", "nirodha"],
                    "priority": "create_now",
                    "reasons": ["appears in repeated multi-word expression"],
                    "snippets": [{"path": "sources/sample.txt", "line": 1, "snippet": "dukkha nirodha"}],
                },
                {
                    "text": "pamoja",
                    "total_count": 2,
                    "document_count": 1,
                    "status": "variant_of_existing",
                    "matched_terms": ["pamojja"],
                    "priority": "review_soon",
                    "reasons": ["possible spelling or normalization variant of an existing term"],
                    "snippets": [{"path": "sources/sample.txt", "line": 2, "snippet": "pamoja"}],
                },
            ],
        }

        markdown = generate_candidate_report.render_markdown(report)

        self.assertIn("## Create Now", markdown)
        self.assertIn("## Review Soon", markdown)
        self.assertIn("`dukkha nirodha`", markdown)
        self.assertIn("`pamoja`", markdown)

    def test_scaffold_writes_review_packets_not_term_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            input_path = tmp_path / "candidate_terms.json"
            output_dir = tmp_path / "scaffolds"
            input_path.write_text(
                json.dumps(
                    {
                        "candidates": [
                            {
                                "text": "dukkha nirodha",
                                "normalized": "dukkhanirodha",
                                "priority": "create_now",
                                "status": "unresolved",
                                "doctrinal_signal": True,
                                "formula_signal": True,
                                "total_count": 4,
                                "document_count": 1,
                                "document_paths": ["sources/sample.txt"],
                                "snippets": [{"path": "sources/sample.txt", "line": 1, "snippet": "dukkha nirodha"}],
                                "matched_terms": ["dukkha", "nirodha"],
                                "reasons": ["appears in repeated multi-word expression"],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            output = io.StringIO()
            with mock.patch("sys.argv", ["scaffold_candidate_terms.py", "--input", str(input_path), "--output-dir", str(output_dir)]):
                with mock.patch("sys.stdout", output):
                    result = scaffold_candidate_terms.main()

            self.assertEqual(result, 0)
            packet_path = output_dir / "dukkhanirodha.review.json"
            self.assertTrue(packet_path.exists())
            payload = json.loads(packet_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["review_status"], "review-required")
            self.assertTrue(payload["do_not_merge_into_terms_without_editorial_review"])


if __name__ == "__main__":
    unittest.main()

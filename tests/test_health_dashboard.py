from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from tests.helpers import load_module


health_dashboard = load_module("health_dashboard", "scripts/health_dashboard.py")
backfill_check_history = load_module(
    "backfill_check_history",
    "scripts/backfill_check_history.py",
)


def make_record(stem: str, **overrides: object) -> dict[str, object]:
    data: dict[str, object] = {
        "term": stem,
        "normalized_term": stem,
        "entry_type": "major",
        "part_of_speech": "noun",
        "preferred_translation": f"{stem} rendering",
        "definition": f"{stem} definition",
        "tags": ["core-doctrine"],
        "status": "reviewed",
    }
    data.update(overrides)
    return data


class FoldTests(unittest.TestCase):
    def test_case_ending_folds_to_the_governing_record(self) -> None:
        index = health_dashboard.headword_index({"citta": make_record("citta")})
        for surface in ("cittam", "cittena", "cittassa", "cittani"):
            with self.subTest(surface=surface):
                key, route = health_dashboard.resolve_token(surface, index)
                self.assertEqual(key, "citta")
                self.assertEqual(route, "inflected")

    def test_exact_headword_is_not_reported_as_inflected(self) -> None:
        index = health_dashboard.headword_index({"citta": make_record("citta")})
        self.assertEqual(health_dashboard.resolve_token("citta", index), ("citta", "exact"))

    def test_stem_vowel_is_restored_after_a_case_ending(self) -> None:
        # `dhamme` folds to `dhamm`, which is not a record. Restoring the stem
        # vowel is what connects it back to `dhamma`.
        index = health_dashboard.headword_index({"dhamma": make_record("dhamma")})
        self.assertEqual(health_dashboard.resolve_token("dhamme", index), ("dhamma", "inflected"))

    def test_fold_does_not_eat_more_than_a_case_ending(self) -> None:
        # `veramaṇī` must not be folded onto `vera`: dropping four characters
        # crosses from inflection into a different word.
        index = health_dashboard.headword_index({"vera": make_record("vera")})
        key, route = health_dashboard.resolve_token("veramani", index)
        self.assertIsNone(key)
        self.assertEqual(route, "none")

    def test_compound_of_two_governed_headwords_resolves(self) -> None:
        index = health_dashboard.headword_index(
            {"jati": make_record("jati"), "dhamma": make_record("dhamma")}
        )
        key, route = health_dashboard.resolve_token("jatidhamma", index)
        self.assertEqual(key, "jati")
        self.assertEqual(route, "compound")

    def test_hyphenated_slug_matches_the_run_together_surface(self) -> None:
        index = health_dashboard.headword_index(
            {"samma-ditthi": make_record("sammā-diṭṭhi", normalized_term="samma-ditthi")}
        )
        key, _route = health_dashboard.resolve_token("sammaditthi", index)
        self.assertEqual(key, "samma-ditthi")

    def test_ungoverned_surface_reports_no_record(self) -> None:
        index = health_dashboard.headword_index({"citta": make_record("citta")})
        self.assertEqual(health_dashboard.resolve_token("uppajjati", index), (None, "none"))


class CorpusTests(unittest.TestCase):
    def test_only_backticked_spans_carrying_diacritics_count_as_pali(self) -> None:
        text = "The word `heart` renders `cittaṃ pariyuṭṭhitaṃ` in this passage."
        self.assertEqual(health_dashboard.pali_tokens(text), ["cittam", "pariyutthitam"])

    def test_rendering_declarations_seed_the_corpus_without_diacritics(self) -> None:
        text = "`dukkha` is rendered `dissatisfaction` throughout."
        self.assertIn("dukkha", health_dashboard.pali_tokens(text))

    def test_stopwords_and_short_tokens_are_filtered(self) -> None:
        text = "`evaṃ kho bhikkhave taṃ`"
        self.assertEqual(health_dashboard.pali_tokens(text), [])

    def test_coverage_counts_governed_and_ungoverned_surfaces(self) -> None:
        terms = {"citta": make_record("citta")}
        with tempfile.TemporaryDirectory() as tmpdir:
            translations = Path(tmpdir)
            (translations / "one-notes.md").write_text(
                "`cittaṃ` here, and `uppajjatī` there.",
                encoding="utf-8",
            )
            coverage = health_dashboard.collect_coverage(terms, translations)

        self.assertEqual(coverage["distinct_surfaces"], 2)
        self.assertEqual(coverage["governed_surfaces"], 1)
        self.assertEqual(coverage["ungoverned_surfaces"], 1)
        self.assertEqual(coverage["surface_coverage_pct"], 50.0)
        self.assertEqual(coverage["top_ungoverned"][0]["surface"], "uppajjati")

    def test_coverage_is_empty_without_a_translations_directory(self) -> None:
        coverage = health_dashboard.collect_coverage({}, Path("does-not-exist"))
        self.assertEqual(coverage["distinct_surfaces"], 0)
        self.assertEqual(coverage["surface_coverage_pct"], 0.0)


class ReviewQueueTests(unittest.TestCase):
    def test_draft_entries_join_the_queue_and_reviewed_ones_do_not(self) -> None:
        terms = {
            "alpha": make_record("alpha", status="draft"),
            "beta": make_record("beta", status="reviewed"),
        }
        queue = health_dashboard.collect_review_queue(
            terms,
            candidates_dir=Path("does-not-exist"),
            reviews_dir=Path("does-not-exist"),
        )
        self.assertEqual(queue["total"], 1)
        self.assertEqual(queue["items"][0]["id"], "alpha")
        self.assertEqual(queue["by_kind"], {"draft_entry": 1})

    def test_unfinished_ledger_surfaces_join_the_queue(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            reviews = Path(tmpdir)
            (reviews / "newcomer-review-ledger.json").write_text(
                json.dumps(
                    {
                        "surfaces": {
                            # `validated` is the ledger's terminal status;
                            # `complete` belongs to the sub-steps and is not a
                            # legal surface status at all.
                            "done": {"status": "validated"},
                            "waiting": {
                                "status": "recruiting",
                                "source_fidelity": {"completed_on": "2026-01-02"},
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            queue = health_dashboard.collect_review_queue(
                {},
                candidates_dir=Path("does-not-exist"),
                reviews_dir=reviews,
            )

        self.assertEqual(queue["total"], 1)
        self.assertEqual(queue["items"][0]["id"], "waiting")
        self.assertEqual(queue["items"][0]["waiting_since"], "2026-01-02")

    def test_a_reopened_gate_keeps_its_queue_date(self) -> None:
        # Reopening a sign-off that could not be tied to the current body moved
        # its date into the superseded block. Reading only the live field made
        # those surfaces look newer than they are.
        with tempfile.TemporaryDirectory() as tmpdir:
            reviews = Path(tmpdir)
            (reviews / "newcomer-review-ledger.json").write_text(
                json.dumps(
                    {
                        "surfaces": {
                            "waiting": {
                                "status": "recruiting",
                                "source_fidelity": {
                                    "status": "pending",
                                    "superseded_signoff": {"completed_on": "2026-01-02"},
                                },
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            queue = health_dashboard.collect_review_queue(
                {},
                candidates_dir=Path("does-not-exist"),
                reviews_dir=reviews,
            )

        self.assertEqual(queue["items"][0]["waiting_since"], "2026-01-02")

    def test_ages_are_bucketed_against_the_reference_date(self) -> None:
        queue = {
            "items": [
                {"kind": "draft_entry", "id": "fresh", "waiting_since": "2026-03-01"},
                {"kind": "draft_entry", "id": "old", "waiting_since": "2025-01-01"},
                {"kind": "draft_entry", "id": "undated", "waiting_since": None},
            ]
        }
        aged = health_dashboard.bucket_review_queue(queue, date(2026, 3, 5))
        self.assertEqual(aged["buckets"]["0-7 days"], 1)
        self.assertEqual(aged["buckets"][health_dashboard.STALE_OVERFLOW], 1)
        self.assertEqual(aged["buckets"]["unknown"], 1)
        self.assertEqual(aged["items"][0]["id"], "old")

    def test_unparseable_dates_are_reported_rather_than_crashing(self) -> None:
        queue = {"items": [{"kind": "candidate", "id": "x", "waiting_since": "not-a-date"}]}
        aged = health_dashboard.bucket_review_queue(queue, date(2026, 3, 5))
        self.assertEqual(aged["buckets"], {"unknown": 1})


class CheckHistoryTests(unittest.TestCase):
    def test_missing_history_reports_an_empty_series(self) -> None:
        failures = health_dashboard.collect_check_failures(Path("does-not-exist"))
        self.assertEqual(failures["weeks_recorded"], 0)
        self.assertIsNone(failures["first_week"])

    def test_history_totals_and_failing_weeks(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "check-history.jsonl"
            path.write_text(
                "\n".join(
                    [
                        json.dumps({"week": "2026-W02", "schema_failures": 0, "lint_failures": 3}),
                        json.dumps({"week": "2026-W01", "schema_failures": 2, "lint_failures": 0}),
                        "",
                        "not json",
                    ]
                ),
                encoding="utf-8",
            )
            failures = health_dashboard.collect_check_failures(path)

        self.assertEqual(failures["weeks_recorded"], 2)
        self.assertEqual(failures["first_week"], "2026-W01")
        self.assertEqual(failures["last_week"], "2026-W02")
        self.assertEqual(failures["schema_failures_total"], 2)
        self.assertEqual(failures["lint_failures_total"], 3)
        self.assertEqual(failures["failing_weeks"], 2)

    def test_findings_are_counted_from_repair_diagnostics(self) -> None:
        output = (
            "Editorial lint failed:\n\n"
            "- Rule violated: first rule\n  File: terms/major/a.json\n"
            "- Rule violated: second rule\n  File: terms/major/b.json\n"
        )
        self.assertEqual(backfill_check_history.count_failures(output), 2)

    def test_legacy_diagnostic_format_is_still_counted(self) -> None:
        output = "- terms/major/a.json: broke a rule\n- terms/major/b.json: broke another\n"
        self.assertEqual(backfill_check_history.count_failures(output), 2)

    def test_unparseable_failure_output_counts_as_one(self) -> None:
        self.assertEqual(backfill_check_history.count_failures("Missing dependency"), 1)


class SeparateMeasuresTests(unittest.TestCase):
    """Drift, formula agreement, and human evidence are different questions."""

    def test_formula_disagreements_are_counted_apart_from_drift(self) -> None:
        # Two records quote one formula with different English. Drift (a
        # document-vs-record question) has nothing to say; formula agreement
        # must still report it.
        terms = {
            "piti": make_record("piti", example_phrases=[{"pali": "vivekajaṃ pītisukhaṃ", "translation": "a"}]),
            "sukha": make_record("sukha", example_phrases=[{"pali": "vivekajaṃ pītisukhaṃ", "translation": "b"}]),
        }
        report = health_dashboard.build_report(
            terms, translations_dir=Path("does-not-exist"), history_path=Path("does-not-exist")
        )
        self.assertEqual(report["drift"]["findings_total"], 0)
        self.assertEqual(report["formula_agreement"]["unexplained"], 1)
        self.assertEqual(report["formula_agreement"]["groups"][0]["records"], ["piti", "sukha"])

    def test_human_evidence_reads_the_ledger_counts(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            reviews = Path(tmpdir)
            (reviews / "newcomer-review-ledger.json").write_text(
                json.dumps(
                    {
                        "surfaces": {
                            "a": {
                                "status": "validated",
                                "source_fidelity": {"status": "complete"},
                                "human_read_aloud": {"status": "complete"},
                                "newcomer_reviews": [{}, {}, {}],
                            },
                            "b": {
                                "status": "recruiting",
                                "source_fidelity": {"status": "complete"},
                                "human_read_aloud": {"status": "pending"},
                                "newcomer_reviews": [],
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            evidence = health_dashboard.collect_human_evidence(reviews)
        self.assertEqual(
            evidence,
            {
                "surfaces": 2,
                "source_fidelity_complete": 2,
                "read_aloud_complete": 1,
                "newcomer_reviews_recorded": 3,
                "newcomer_reviews_counting": 0,
                "surfaces_validated": 1,
            },
        )

    def test_only_reviews_of_the_current_body_count(self) -> None:
        # Recorded and counting are different numbers. Two readers reviewed an
        # earlier draft; reporting all three as progress would claim credit the
        # gate does not give.
        with tempfile.TemporaryDirectory() as tmpdir:
            reviews = Path(tmpdir)
            (reviews / "newcomer-review-ledger.json").write_text(
                json.dumps(
                    {
                        "surfaces": {
                            "a": {
                                "status": "in-review",
                                "source_fidelity": {"status": "complete"},
                                "human_read_aloud": {"status": "pending"},
                                "newcomer_reviews": [
                                    {"body_sha256": "a" * 64},
                                    {"body_sha256": "b" * 64},
                                    {"body_sha256": "b" * 64},
                                ],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            evidence = health_dashboard.collect_human_evidence(
                reviews, current_hash=lambda key: "a" * 64
            )
        self.assertEqual(evidence["newcomer_reviews_recorded"], 3)
        self.assertEqual(evidence["newcomer_reviews_counting"], 1)

    def test_missing_ledger_reports_zeros_not_an_error(self) -> None:
        evidence = health_dashboard.collect_human_evidence(Path("does-not-exist"))
        self.assertEqual(evidence["surfaces"], 0)
        self.assertEqual(evidence["newcomer_reviews_recorded"], 0)

    def test_markdown_shows_both_sections(self) -> None:
        report = health_dashboard.build_report(
            {"citta": make_record("citta")},
            translations_dir=Path("does-not-exist"),
            history_path=Path("does-not-exist"),
        )
        rendered = health_dashboard.render_dashboard(report)
        self.assertIn("## Formula agreement", rendered)
        self.assertIn("## Human review evidence", rendered)
        self.assertIn("| Newcomer reviews recorded |", rendered)


class RenderTests(unittest.TestCase):
    def test_dashboard_renders_every_section(self) -> None:
        report = health_dashboard.build_report(
            {"citta": make_record("citta")},
            translations_dir=Path("does-not-exist"),
            history_path=Path("does-not-exist"),
        )
        rendered = health_dashboard.render_dashboard(report)
        for heading in ("## Coverage", "## Drift", "## Review queue", "per week"):
            self.assertIn(heading, rendered)

    def test_rendered_dashboard_carries_no_wall_clock_values(self) -> None:
        # The committed file is compared byte for byte by
        # `scripts/check_generated_docs.py`, so it must not embed today's date
        # or a day count that moves overnight.
        report = health_dashboard.build_report(
            {"alpha": make_record("alpha", status="draft")},
            translations_dir=Path("does-not-exist"),
            history_path=Path("does-not-exist"),
        )
        rendered = health_dashboard.render_dashboard(report)
        self.assertNotIn(date.today().isoformat(), rendered)
        self.assertNotIn("waiting_days", rendered)

    def test_pipes_in_values_do_not_break_the_table(self) -> None:
        self.assertEqual(health_dashboard.md_escape("a|b"), "a\\|b")

    def test_write_outputs_writes_into_the_module_output_dir(self) -> None:
        original = health_dashboard.OUTPUT_DIR
        with tempfile.TemporaryDirectory() as tmpdir:
            health_dashboard.OUTPUT_DIR = Path(tmpdir)
            try:
                written = health_dashboard.write_outputs({"citta": make_record("citta")})
            finally:
                health_dashboard.OUTPUT_DIR = original

            self.assertEqual([path.name for path in written], ["health-dashboard.md"])

    def test_generator_exposes_the_freshness_check_contract(self) -> None:
        # `scripts/check_generated_docs.py` reaches for exactly these three.
        for attribute in ("OUTPUT_DIR", "load_terms", "write_outputs"):
            self.assertTrue(hasattr(health_dashboard, attribute), attribute)


class RegressionTests(unittest.TestCase):
    """Cases that shipped broken in the first cut of this dashboard."""

    def test_finished_ledger_surfaces_use_the_ledger_vocabulary(self) -> None:
        # `scripts/check_newcomer_reviews.py` allows recruiting, in-review,
        # ready, validated. Testing for `complete` excluded nothing.
        with tempfile.TemporaryDirectory() as tmpdir:
            reviews = Path(tmpdir)
            (reviews / "newcomer-review-ledger.json").write_text(
                json.dumps(
                    {
                        "surfaces": {
                            "finished": {"status": "validated"},
                            "open": {"status": "ready"},
                        }
                    }
                ),
                encoding="utf-8",
            )
            queue = health_dashboard.collect_review_queue(
                {},
                candidates_dir=Path("does-not-exist"),
                reviews_dir=reviews,
            )

        self.assertEqual([row["id"] for row in queue["items"]], ["open"])

    def test_a_declaration_does_not_count_its_headword_twice(self) -> None:
        # The declaration is itself a backticked span, so a diacriticked
        # headword was counted by both scans and inflated every occurrence.
        self.assertEqual(
            health_dashboard.pali_tokens("`dukkhā` is rendered `suffering`"),
            ["dukkha"],
        )

    def test_an_ascii_declaration_headword_is_still_collected(self) -> None:
        self.assertEqual(
            health_dashboard.pali_tokens("`dukkha` is rendered `suffering`"),
            ["dukkha"],
        )

    def test_declaration_headwords_are_tokenized(self) -> None:
        # Taken whole, `araddhosmi ... araddhacittosmi` became one junk surface.
        self.assertEqual(
            health_dashboard.pali_tokens("`araddhosmi ... araddhacittosmi` is rendered `x`"),
            ["araddhosmi", "araddhacittosmi"],
        )

    def test_uppercase_diacritics_are_recognized_as_pali(self) -> None:
        self.assertEqual(health_dashboard.pali_tokens("`Āsava` here"), ["asava"])

    def test_a_four_character_ending_still_folds(self) -> None:
        # The strip cap made `smim`, `anam` and `assa` unreachable, so the
        # locative never folded at all.
        index = health_dashboard.headword_index({"rupa": make_record("rupa")})
        self.assertEqual(
            health_dashboard.resolve_token("rupasmim", index), ("rupa", "inflected")
        )

    def test_the_report_carries_every_ungoverned_row(self) -> None:
        # The JSON promised full detail lists but shipped a 25-row preview.
        terms = {"citta": make_record("citta")}
        with tempfile.TemporaryDirectory() as tmpdir:
            translations = Path(tmpdir)
            surfaces = " ".join(f"`ungoverned{n}ṃ`" for n in range(30))
            (translations / "one-notes.md").write_text(surfaces, encoding="utf-8")
            coverage = health_dashboard.collect_coverage(terms, translations)

        self.assertEqual(len(coverage["top_ungoverned"]), coverage["ungoverned_total"])
        self.assertGreater(coverage["ungoverned_total"], 25)

    def test_a_partial_replay_keeps_the_weeks_it_did_not_measure(self) -> None:
        # `--limit` rewrote the file with only the weeks it looked at.
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "check-history.jsonl"
            path.write_text(
                json.dumps({"week": "2026-W01", "schema_failures": 0, "lint_failures": 0}) + "\n",
                encoding="utf-8",
            )
            backfill_check_history.write_history(
                [{"week": "2026-W02", "schema_failures": 1, "lint_failures": 0}], path
            )
            weeks = [json.loads(line)["week"] for line in path.read_text().splitlines()]

        self.assertEqual(weeks, ["2026-W01", "2026-W02"])

    def test_a_rewritten_week_wins_over_the_stored_one(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "check-history.jsonl"
            path.write_text(
                json.dumps({"week": "2026-W01", "schema_failures": 9, "lint_failures": 0}) + "\n",
                encoding="utf-8",
            )
            backfill_check_history.write_history(
                [{"week": "2026-W01", "schema_failures": 0, "lint_failures": 0}], path
            )
            rows = [json.loads(line) for line in path.read_text().splitlines()]

        self.assertEqual(rows, [{"week": "2026-W01", "schema_failures": 0, "lint_failures": 0}])

    def test_an_output_path_outside_the_repository_is_displayable(self) -> None:
        # `relative_to` raised only after the multi-minute replay had run.
        self.assertEqual(
            backfill_check_history.display_path(Path("/tmp/elsewhere.jsonl")),
            "/tmp/elsewhere.jsonl",
        )

    def test_a_missing_dependency_is_not_recorded_as_a_finding(self) -> None:
        self.assertTrue(backfill_check_history.is_environment_failure("Missing dependency: jsonschema"))
        self.assertFalse(backfill_check_history.is_environment_failure("- Rule violated: x"))


if __name__ == "__main__":
    unittest.main()

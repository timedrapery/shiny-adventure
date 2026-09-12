from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.helpers import load_module


check = load_module("check_formula_agreement", "scripts/check_formula_agreement.py")


def record(key: str, *phrases: tuple[str, str]) -> dict[str, object]:
    return {
        "term": key,
        "normalized_term": key,
        "example_phrases": [{"pali": pali, "translation": translation} for pali, translation in phrases],
    }


class NormalizationTests(unittest.TestCase):
    def test_anusvara_spellings_fold_to_one_phrase(self) -> None:
        # Records write the anusvāra both ways; without folding, the same
        # formula looks like two unrelated phrases and never gets compared.
        self.assertEqual(
            check.normalize_pali("vivekajaṁ pītisukhaṁ"),
            check.normalize_pali("Vivekajaṃ pītisukhaṃ."),
        )

    def test_punctuation_and_spacing_do_not_split_a_phrase(self) -> None:
        self.assertEqual(check.normalize_pali("sabbe  saṅkhārā, aniccā"), "sabbe saṅkhārā aniccā")


class DisagreementTests(unittest.TestCase):
    def test_agreeing_copies_are_silent(self) -> None:
        terms = {
            "piti": record("piti", ("vivekajaṃ pītisukhaṃ", "rejoicing and satisfaction born of seclusion")),
            "sukha": record("sukha", ("vivekajaṁ pītisukhaṁ", "Rejoicing and satisfaction born of seclusion")),
        }
        unexplained, waived = check.collect_disagreements(terms)
        self.assertEqual((unexplained, waived), ([], []))

    def test_disagreeing_copies_are_reported_with_every_rendering(self) -> None:
        terms = {
            "piti": record("piti", ("vivekajaṃ pītisukhaṃ", "rejoicing and satisfaction born of seclusion")),
            "sukha": record("sukha", ("vivekajaṃ pītisukhaṃ", "delight and satisfaction born of seclusion")),
            "jhana": record("jhana", ("paṭhamaṃ jhānaṃ", "the first mental theme")),
        }
        unexplained, _waived = check.collect_disagreements(terms)
        self.assertEqual(len(unexplained), 1)
        self.assertEqual(unexplained[0]["records"], ["piti", "sukha"])
        self.assertEqual(len(unexplained[0]["renderings"]), 2)

    def test_a_scoped_exception_waives_the_disagreement(self) -> None:
        terms = {
            "piti": record("piti", ("vivekajaṃ pītisukhaṃ", "rejoicing and satisfaction born of seclusion")),
            "sukha": record("sukha", ("vivekajaṃ pītisukhaṃ", "delight and satisfaction born of seclusion")),
        }
        exceptions = {
            check.normalize_pali("vivekajaṃ pītisukhaṃ"): {
                "pali": "vivekajaṃ pītisukhaṃ",
                "renderings": {
                    "piti": "rejoicing and satisfaction born of seclusion",
                    "sukha": "Delight and satisfaction born of seclusion",
                },
                "rationale": "sukha quotes the formula under its own contrast rule",
            }
        }
        unexplained, waived = check.collect_disagreements(terms, exceptions)
        self.assertEqual(unexplained, [])
        self.assertEqual(len(waived), 1)
        self.assertIn("contrast rule", waived[0]["rationale"])

    def test_an_exception_does_not_cover_a_record_it_does_not_name(self) -> None:
        # A new copy of the formula drifted after the exception was written:
        # the waiver must not silently stretch to cover it.
        terms = {
            "piti": record("piti", ("vivekajaṃ pītisukhaṃ", "rejoicing and satisfaction born of seclusion")),
            "sukha": record("sukha", ("vivekajaṃ pītisukhaṃ", "delight and satisfaction born of seclusion")),
            "jhana": record("jhana", ("vivekajaṃ pītisukhaṃ", "rapture and ease born of seclusion")),
        }
        exceptions = {
            check.normalize_pali("vivekajaṃ pītisukhaṃ"): {
                "pali": "vivekajaṃ pītisukhaṃ",
                "renderings": {
                    "piti": "rejoicing and satisfaction born of seclusion",
                    "sukha": "delight and satisfaction born of seclusion",
                },
                "rationale": "scoped to two records",
            }
        }
        unexplained, waived = check.collect_disagreements(terms, exceptions)
        self.assertEqual(waived, [])
        self.assertEqual(unexplained[0]["exception_gap"], ["jhana"])

    def test_an_exception_lapses_when_a_named_record_changes_its_english(self) -> None:
        # The waiver pinned specific English. A named record drifting to a
        # third rendering is a new decision nobody made, so it is reported.
        terms = {
            "piti": record("piti", ("vivekajaṃ pītisukhaṃ", "rejoicing and satisfaction born of seclusion")),
            "sukha": record("sukha", ("vivekajaṃ pītisukhaṃ", "something else entirely")),
        }
        exceptions = {
            check.normalize_pali("vivekajaṃ pītisukhaṃ"): {
                "pali": "vivekajaṃ pītisukhaṃ",
                "renderings": {
                    "piti": "rejoicing and satisfaction born of seclusion",
                    "sukha": "delight and satisfaction born of seclusion",
                },
                "rationale": "pinned",
            }
        }
        unexplained, waived = check.collect_disagreements(terms, exceptions)
        self.assertEqual(waived, [])
        self.assertEqual(unexplained[0]["exception_gap"], ["sukha"])


class BaselineTests(unittest.TestCase):
    def finding(self, pali: str, *pairs: tuple[str, str]) -> dict[str, object]:
        return {"pali": pali, "records": sorted(k for k, _t in pairs), "renderings": sorted(pairs)}

    def test_a_known_group_with_unchanged_variants_is_not_a_regression(self) -> None:
        f = self.finding("x y", ("a", "one"), ("b", "two"))
        baseline = {check.normalize_pali("x y"): check.variant_key(f)}
        regressions, stale = check.compare_to_baseline([f], baseline)
        self.assertEqual((regressions, stale), ([], []))

    def test_a_group_not_in_the_baseline_is_a_regression(self) -> None:
        f = self.finding("x y", ("a", "one"), ("b", "two"))
        regressions, _stale = check.compare_to_baseline([f], {})
        self.assertEqual(regressions, [f])

    def test_a_known_group_with_changed_variants_is_a_regression(self) -> None:
        # Fixing one group must not pay for breaking another: the variants
        # are compared, not the count.
        old = self.finding("x y", ("a", "one"), ("b", "two"))
        new = self.finding("x y", ("a", "one"), ("b", "three"))
        baseline = {check.normalize_pali("x y"): check.variant_key(old)}
        regressions, _stale = check.compare_to_baseline([new], baseline)
        self.assertEqual(regressions, [new])

    def test_a_resolved_group_still_in_the_baseline_is_stale(self) -> None:
        baseline = {check.normalize_pali("x y"): ["a\tone", "b\ttwo"]}
        regressions, stale = check.compare_to_baseline([], baseline)
        self.assertEqual(regressions, [])
        self.assertEqual(stale, [check.normalize_pali("x y")])

    def test_baseline_round_trips_through_the_file(self) -> None:
        f = self.finding("Vivekajaṁ pītisukhaṁ", ("a", "One"), ("b", "two"))
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "formula-baseline.json"
            check.write_baseline_document({str(f["pali"]): check.variant_key(f)}, path)
            loaded = check.load_baseline(path)
        self.assertEqual(loaded, {check.normalize_pali("vivekajaṃ pītisukhaṃ"): check.variant_key(f)})


class BaselineMaintenanceTests(unittest.TestCase):
    """Cleanup and accepting new debt are two different decisions."""

    def finding(self, pali: str, *pairs: tuple[str, str]) -> dict[str, object]:
        return {"pali": pali, "records": sorted(k for k, _t in pairs), "renderings": sorted(pairs)}

    def setUp(self) -> None:
        self.resolved = self.finding("x y", ("a", "one"), ("b", "two"))
        self.still_broken = self.finding("p q", ("a", "three"), ("b", "four"))
        self.new_debt = self.finding("m n", ("a", "five"), ("b", "six"))

    def baseline_file(self, tmpdir: str, *findings: dict[str, object]) -> Path:
        path = Path(tmpdir) / "formula-baseline.json"
        check.write_baseline_document({str(f["pali"]): check.variant_key(f) for f in findings}, path)
        return path

    def test_pruning_removes_resolved_groups_and_nothing_else(self) -> None:
        # The mixed case: one old disagreement is resolved while a new one
        # appears. A cleanup must not absorb the new one -- that is how routine
        # tidying silently increased the accepted backlog.
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self.baseline_file(tmpdir, self.resolved, self.still_broken)
            regressions, stale = check.compare_to_baseline(
                [self.still_broken, self.new_debt], check.load_baseline(path)
            )
            self.assertEqual([f["pali"] for f in regressions], ["m n"])
            groups, removed = check.prune_baseline(check.load_baseline_document(path), stale)

        self.assertEqual(removed, ["x y"])
        self.assertEqual(sorted(groups), ["p q"])
        self.assertNotIn("m n", groups)

    def test_pruning_keeps_a_known_group_exactly_as_acknowledged(self) -> None:
        # A changed variant set on a known group is a regression, so pruning
        # must not quietly re-acknowledge it with its new English.
        changed = self.finding("p q", ("a", "three"), ("b", "different now"))
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self.baseline_file(tmpdir, self.still_broken)
            _regressions, stale = check.compare_to_baseline([changed], check.load_baseline(path))
            groups, _removed = check.prune_baseline(check.load_baseline_document(path), stale)

        self.assertEqual(groups["p q"], check.variant_key(self.still_broken))

    def test_accepting_new_debt_records_the_reason_and_the_groups(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self.baseline_file(tmpdir, self.still_broken)
            document = check.load_baseline_document(path)
            groups, acknowledgements = check.accept_new_debt(
                document, [self.still_broken, self.new_debt], [self.new_debt], "agreed with the editor"
            )
            check.write_baseline_document(groups, path, acknowledgements)
            written = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(sorted(written["groups"]), ["m n", "p q"])
        self.assertEqual(written["acknowledgements"][-1]["groups"], ["m n"])
        self.assertIn("agreed with the editor", written["acknowledgements"][-1]["reason"])

    def test_acknowledgement_history_is_kept(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self.baseline_file(tmpdir, self.still_broken)
            check.write_baseline_document(
                {str(self.still_broken["pali"]): check.variant_key(self.still_broken)},
                path,
                [{"reason": "an older decision", "groups": ["p q"]}],
            )
            groups, acknowledgements = check.accept_new_debt(
                check.load_baseline_document(path), [self.new_debt], [self.new_debt], "a new decision"
            )

        self.assertEqual([entry["reason"] for entry in acknowledgements], ["an older decision", "a new decision"])


class BaselineCommandTests(unittest.TestCase):
    REPO = Path(__file__).resolve().parent.parent

    def run_check(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "scripts/check_formula_agreement.py", *args],
            cwd=self.REPO,
            capture_output=True,
            text=True,
        )

    def test_accepting_debt_without_a_reason_is_refused(self) -> None:
        result = self.run_check("--accept-new-debt")

        self.assertEqual(result.returncode, 1)
        self.assertIn("requires --reason", result.stdout)

    def test_the_two_operations_cannot_be_combined(self) -> None:
        result = self.run_check("--prune-baseline", "--accept-new-debt", "--reason", "no")

        self.assertEqual(result.returncode, 1)
        self.assertIn("separate operations", result.stdout)

    def test_pruning_with_nothing_resolved_leaves_the_file_alone(self) -> None:
        baseline = self.REPO / "reviews" / "formula-baseline.json"
        before = baseline.read_bytes()

        result = self.run_check("--prune-baseline")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(baseline.read_bytes(), before)


class ExceptionFileTests(unittest.TestCase):
    def test_missing_file_means_no_exceptions(self) -> None:
        self.assertEqual(check.load_exceptions(Path("does-not-exist.json")), {})

    def write(self, tmpdir: str, entries: list[dict[str, object]]) -> Path:
        path = Path(tmpdir) / "formula-exceptions.json"
        path.write_text(json.dumps({"exceptions": entries}), encoding="utf-8")
        return path

    def test_an_exception_without_a_rationale_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self.write(tmpdir, [{"pali": "x y", "renderings": {"a": "one"}}])
            with self.assertRaises(ValueError):
                check.load_exceptions(path)

    def test_an_exception_without_renderings_is_rejected(self) -> None:
        # A rationale alone waived the whole disagreement for every record,
        # present and future. The approved English is the scope.
        with tempfile.TemporaryDirectory() as tmpdir:
            for bad in ({"pali": "x y", "rationale": "why"}, {"pali": "x y", "rationale": "why", "renderings": {}}):
                path = self.write(tmpdir, [bad])
                with self.assertRaises(ValueError):
                    check.load_exceptions(path)

    def test_duplicate_entries_for_one_phrase_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self.write(
                tmpdir,
                [
                    {"pali": "x y", "rationale": "first", "renderings": {"a": "one"}},
                    {"pali": "X Y.", "rationale": "second", "renderings": {"a": "one"}},
                ],
            )
            with self.assertRaises(ValueError):
                check.load_exceptions(path)

    def test_exceptions_are_keyed_by_normalized_pali(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self.write(
                tmpdir,
                [{"pali": "Vivekajaṁ pītisukhaṁ", "rationale": "why", "renderings": {"piti": "x"}}],
            )
            loaded = check.load_exceptions(path)
        self.assertIn(check.normalize_pali("vivekajaṃ pītisukhaṃ"), loaded)


class JsonOutputTests(unittest.TestCase):
    def test_json_mode_emits_one_parseable_document(self) -> None:
        # The regression and stale-baseline summaries were printed after the
        # JSON document, so the output no parser would accept -- found when a
        # `--json | python -m json.tool` pipeline choked on it.
        import io
        import subprocess
        import sys

        result = subprocess.run(
            [sys.executable, "scripts/check_formula_agreement.py", "--json"],
            cwd=Path(__file__).resolve().parent.parent,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        for key in ("unexplained", "waived", "regressions", "stale_baseline"):
            self.assertIn(key, payload)


if __name__ == "__main__":
    unittest.main()

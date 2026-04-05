from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import load_module


check_translation_drift = load_module(
    "check_translation_drift",
    "scripts/check_translation_drift.py",
)


def make_record(stem: str, **overrides: object) -> check_translation_drift.TermRecord:
    data: dict[str, object] = {
        "term": stem,
        "normalized_term": stem,
        "entry_type": "major",
        "part_of_speech": "noun",
        "preferred_translation": f"{stem} translation",
        "alternative_translations": [f"{stem} alt"],
        "discouraged_translations": [f"{stem} discouraged"],
        "definition": f"{stem} definition",
        "notes": (
            f"The default translation for {stem} is explicit, context-sensitive, and "
            "meant to prevent drift in translation choices."
        ),
        "context_rules": [
            {
                "context": "default context",
                "rendering": f"{stem} translation",
                "notes": "Default rendering applies here.",
            },
            {
                "context": "alternate context",
                "rendering": f"{stem} alt",
                "notes": "Alternate rendering applies here.",
            },
        ],
        "related_terms": [f"{stem}-related"],
        "example_phrases": [{"pali": stem, "translation": f"{stem} translation"}],
        "sutta_references": ["SN 1.1"],
        "tags": ["core-doctrine"],
        "authority_basis": [
            {
                "source": "Repository editorial record",
                "scope": "Supports the rule-bearing entry.",
            }
        ],
        "translation_policy": {
            "default_scope": "Default doctrinal usage.",
            "when_not_to_apply": "Do not rotate ad hoc.",
            "compound_inheritance": "case-by-case",
            "drift_risk": "Avoid drift.",
        },
        "status": "reviewed",
    }
    data.update(overrides)
    path = check_translation_drift.REPO_ROOT / "terms" / "major" / f"{stem}.json"
    return check_translation_drift.TermRecord(path=path, stem=stem, data=data)


class DriftCheckRuleTests(unittest.TestCase):
    def test_conflicting_preferred_translations_for_same_lemma_are_errors(self) -> None:
        findings: list[check_translation_drift.Finding] = []
        records = [
            make_record("sankhara_a", term="saṅkhāra", normalized_term="sankhara_a", preferred_translation="constructed thing"),
            make_record("sankhara_b", term="saṅkhāra", normalized_term="sankhara_b", preferred_translation="formation"),
        ]

        check_translation_drift.check_conflicting_preferred_translations(records, findings)

        self.assertEqual(len(findings), 2)
        self.assertTrue(all(item.code == "conflicting_preferred_translation" for item in findings))
        self.assertTrue(all(item.severity == "error" for item in findings))

    def test_duplicate_major_preferred_renderings_warn_when_not_cross_related(self) -> None:
        findings: list[check_translation_drift.Finding] = []
        records = [
            make_record("citta", preferred_translation="mind", related_terms=["vedana"]),
            make_record("mano", preferred_translation="mind", related_terms=["sati"]),
        ]

        check_translation_drift.check_duplicate_preferred_renderings(records, findings)

        self.assertEqual(len(findings), 2)
        self.assertTrue(all(item.code == "duplicate_preferred_rendering" for item in findings))

    def test_major_entries_missing_rule_fields_are_errors(self) -> None:
        findings: list[check_translation_drift.Finding] = []
        record = make_record("sati", translation_policy=None)

        check_translation_drift.check_rule_bearing_fields([record], findings)

        self.assertEqual(
            findings[0].code,
            "missing_rule_field",
        )

    def test_alternate_overlap_and_discouraged_context_use_are_errors(self) -> None:
        findings: list[check_translation_drift.Finding] = []
        record = make_record(
            "passaddhi",
            preferred_translation="settling",
            alternative_translations=["settling", "relaxation"],
            discouraged_translations=["relaxation"],
            context_rules=[
                {
                    "context": "pedagogical prose",
                    "rendering": "relaxation",
                    "notes": "This should be caught.",
                },
                {
                    "context": "default context",
                    "rendering": "settling",
                    "notes": "Default rendering applies here.",
                },
            ],
        )

        check_translation_drift.check_alternate_consistency([record], findings)
        codes = {item.code for item in findings}

        self.assertEqual(
            codes,
            {
                "preferred_listed_as_alternate",
                "alternate_discouraged_overlap",
                "context_rule_uses_discouraged_rendering",
            },
        )
        severities = {item.code: item.severity for item in findings}
        self.assertEqual(severities["preferred_listed_as_alternate"], "error")
        self.assertEqual(severities["alternate_discouraged_overlap"], "error")
        self.assertEqual(severities["context_rule_uses_discouraged_rendering"], "error")

    def test_context_sensitive_entries_require_rule_notes(self) -> None:
        findings: list[check_translation_drift.Finding] = []
        record = make_record(
            "sankhara",
            tags=["context-sensitive"],
            context_rules=[
                {"context": "dependent arising", "rendering": "choices"},
                {
                    "context": "general doctrinal prose",
                    "rendering": "constructed things",
                    "notes": "Notes are present here.",
                },
            ],
        )

        check_translation_drift.check_context_sensitive_notes([record], findings)

        self.assertEqual(findings[0].code, "context_sensitive_missing_note")

    def test_context_sensitive_entries_require_distinct_renderings(self) -> None:
        findings: list[check_translation_drift.Finding] = []
        record = make_record(
            "sankhara",
            tags=["context-sensitive"],
            context_rules=[
                {
                    "context": "dependent arising",
                    "rendering": "choices",
                    "notes": "Use this in the sequence.",
                },
                {
                    "context": "general doctrinal prose",
                    "rendering": "choices",
                    "notes": "This should still be caught.",
                },
            ],
        )

        check_translation_drift.check_context_sensitive_notes([record], findings)

        self.assertEqual(findings[0].code, "context_sensitive_indistinct_renderings")

    def test_major_entries_require_preferred_translation_in_context_rules(self) -> None:
        findings: list[check_translation_drift.Finding] = []
        record = make_record(
            "sati",
            preferred_translation="remembering",
            context_rules=[
                {
                    "context": "path factor gloss",
                    "rendering": "right remembering",
                    "notes": "Use this in compounds.",
                },
                {
                    "context": "source-facing prose",
                    "rendering": "sati",
                    "notes": "Use this when the Pali should remain visible.",
                },
            ],
        )

        check_translation_drift.check_default_rendering_coverage([record], findings)

        self.assertEqual(findings[0].code, "preferred_not_covered_by_context_rules")

    def test_headword_normalization_mismatch_is_reported(self) -> None:
        findings: list[check_translation_drift.Finding] = []
        record = make_record("samadhi", term="samādhi", normalized_term="samatha")

        check_translation_drift.check_headword_normalization([record], findings)

        self.assertEqual(findings[0].code, "normalized_term_mismatch")

    def test_compound_normalization_editorial_slug_does_not_warn(self) -> None:
        findings: list[check_translation_drift.Finding] = []
        record = make_record(
            "chanda-iddhipada",
            term="chandiddhipāda",
            normalized_term="chanda-iddhipada",
            part_of_speech="compound",
        )

        check_translation_drift.check_headword_normalization([record], findings)

        self.assertEqual(findings, [])

    def test_phrase_normalization_editorial_slug_does_not_warn(self) -> None:
        findings: list[check_translation_drift.Finding] = []
        record = make_record(
            "imasmim-sati-idam-hoti",
            term="imasmiá¹ƒ sati idaá¹ƒ hoti",
            normalized_term="imasmim-sati-idam-hoti",
            part_of_speech="phrase",
        )

        check_translation_drift.check_headword_normalization([record], findings)

        self.assertEqual(findings, [])

    def test_major_entry_that_lacks_rule_signals_warns_as_definitional(self) -> None:
        findings: list[check_translation_drift.Finding] = []
        record = make_record(
            "bhava",
            notes="Existence.",
            context_rules=[],
            authority_basis=[],
            translation_policy={},
        )

        check_translation_drift.check_major_entry_rule_strength([record], findings)

        self.assertEqual(findings[0].code, "major_entry_too_definitional")


class DriftCheckCliTests(unittest.TestCase):
    def test_finding_to_diagnostic_includes_same_pass_guidance_for_conflicts(self) -> None:
        diagnostic = check_translation_drift.finding_to_diagnostic(
            check_translation_drift.Finding(
                severity="error",
                category="Preferred Translation",
                code="conflicting_preferred_translation",
                message="lemma 'sankhara' has conflicting preferred translations: formation, putting together",
                path="terms/major/sankhara.json",
            )
        )

        self.assertEqual(diagnostic.code, "conflicting_preferred_translation")
        self.assertIn("same pass", diagnostic.fix)
        self.assertIn("terms/major/sankhara.json", diagnostic.examples)

    def test_main_emits_json_report(self) -> None:
        output = io.StringIO()
        findings = [
            check_translation_drift.Finding(
                severity="warning",
                category="Preferred Translation",
                code="duplicate_preferred_rendering",
                message="rendering is shared",
                path="terms/major/citta.json",
            )
        ]

        with mock.patch.object(check_translation_drift, "collect_findings", return_value=(findings, 2)):
            with mock.patch("sys.argv", ["check_translation_drift.py", "--json"]):
                with mock.patch("sys.stdout", output):
                    result = check_translation_drift.main()

        self.assertEqual(result, 0)
        report = json.loads(output.getvalue())
        self.assertEqual(report["term_files"], 2)
        self.assertEqual(report["warnings"][0]["code"], "duplicate_preferred_rendering")

    def test_main_fails_in_strict_mode_when_only_warnings_exist(self) -> None:
        output = io.StringIO()
        findings = [
            check_translation_drift.Finding(
                severity="warning",
                category="Preferred Translation",
                code="duplicate_preferred_rendering",
                message="rendering is shared",
                path="terms/major/citta.json",
            )
        ]

        with mock.patch.object(check_translation_drift, "collect_findings", return_value=(findings, 2)):
            with mock.patch("sys.argv", ["check_translation_drift.py", "--strict"]):
                with mock.patch("sys.stdout", output):
                    result = check_translation_drift.main()

        self.assertEqual(result, 1)
        self.assertIn("Translation drift warnings:", output.getvalue())

    def test_collect_findings_reports_missing_terms_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            findings, record_count = check_translation_drift.collect_findings(Path(tmpdir) / "missing")

        self.assertEqual(record_count, 0)
        self.assertEqual(findings[0].code, "missing_terms_dir")

    def test_collect_findings_passes_terms_dir_to_schema_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            terms_dir = tmp_path / "terms"
            terms_dir.mkdir()
            (terms_dir / "sati.json").write_text("{}", encoding="utf-8")

            with mock.patch.object(
                check_translation_drift,
                "collect_validation_failures",
                return_value=(["schema issue"], []),
            ) as validation_mock:
                findings, record_count = check_translation_drift.collect_findings(terms_dir)

        self.assertEqual(record_count, 1)
        validation_mock.assert_called_once_with(terms_dir)
        self.assertEqual(findings[0].code, "schema_violation")


if __name__ == "__main__":
    unittest.main()

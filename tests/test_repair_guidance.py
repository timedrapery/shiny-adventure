from __future__ import annotations

import contextlib
import io
import json
import unittest

from tests.helpers import REPO_ROOT, load_module


guidance = load_module("repair_guidance", "scripts/repair_guidance.py")


def diagnostic(**overrides):
    values = dict(
        severity="error",
        rule="rule-a",
        summary="what failed",
        why="why it matters",
        fix="the fix",
    )
    values.update(overrides)
    return guidance.RepairDiagnostic(**values)


class RepairGuidanceTests(unittest.TestCase):
    def test_every_field_snippet_is_valid_json(self) -> None:
        for field, snippet in guidance.FIELD_SNIPPETS.items():
            with self.subTest(field=field):
                json.loads(snippet)

    def test_every_cited_example_file_exists(self) -> None:
        cited = set(guidance.MAJOR_POLICY_EXAMPLES)
        cited |= set(guidance.RELATIONSHIP_EXAMPLES)
        cited |= set(guidance.STATUS_EXAMPLES)
        cited |= set(guidance.CLUSTER_DOC_EXAMPLES)
        for examples in guidance.FIELD_MODEL_EXAMPLES.values():
            cited |= set(examples)
        for relative in sorted(cited):
            with self.subTest(path=relative):
                self.assertTrue((REPO_ROOT / relative).is_file())

    def test_unknown_field_falls_back_to_major_policy_examples(self) -> None:
        self.assertIsNone(guidance.field_snippet("no-such-field"))
        self.assertEqual(guidance.field_examples("no-such-field"), guidance.MAJOR_POLICY_EXAMPLES)

    def test_diagnostics_serialize_to_plain_dicts(self) -> None:
        [row] = guidance.diagnostics_as_json([diagnostic(file="terms/major/sati.json")])
        self.assertEqual(row["rule"], "rule-a")
        self.assertEqual(row["file"], "terms/major/sati.json")
        self.assertEqual(row["examples"], ())

    def test_print_groups_by_category_and_skips_empty_lists(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            guidance.print_diagnostics("Nothing", [])
            guidance.print_diagnostics(
                "Problems",
                [
                    diagnostic(category="Schema", rule="r1"),
                    diagnostic(category="Schema", rule="r2", examples=("terms/major/sati.json",)),
                    diagnostic(category="Lint", rule="r3"),
                ],
            )
        text = out.getvalue()
        self.assertNotIn("Nothing", text)
        self.assertTrue(text.startswith("Problems:\n"))
        self.assertEqual(text.count("Schema:"), 1)
        self.assertEqual(text.count("Lint:"), 1)
        self.assertIn("Good repo example(s): terms/major/sati.json", text)


if __name__ == "__main__":
    unittest.main()

"""Pinned term decisions, checked from one table.

Each row in `tests/term_policy_pins.json` names a rule and the term records it
pins. A term is named by its path under `terms/` without `.json`. Each check
is a field path and a value:

- `"field": value`: the field equals the value.
- `"field includes": [...]`: each item is in the field (a list item, or text
  inside a string).
- `"field mention": [...]`: each item appears as text inside at least one
  value of a list field.
- `"field differs from": [...]`: the field differs from the same field of
  each named term.

A dotted path walks into the record. A step through a list of objects
collects that key from each object, so `authority_basis.source` is the list
of sources.
"""

from __future__ import annotations

import json
import unittest
from functools import cache
from pathlib import Path

from tests.helpers import load_module


REPO_ROOT = Path(__file__).resolve().parent.parent
PINS_PATH = REPO_ROOT / "tests" / "term_policy_pins.json"


@cache
def load_term(name: str) -> dict[str, object]:
    with (REPO_ROOT / "terms" / f"{name}.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def resolve(value: object, path: str) -> object:
    for key in path.split("."):
        if isinstance(value, list):
            value = [item[key] for item in value]
        else:
            value = value[key]
    return value


def check(test: unittest.TestCase, term: str, key: str, expected: object) -> None:
    path, _, op = key.partition(" ")
    actual = resolve(load_term(term), path)
    if op == "":
        test.assertEqual(actual, expected)
    elif op == "includes":
        for item in expected:
            test.assertIn(item, actual)
    elif op == "mention":
        for item in expected:
            test.assertTrue(any(item in value for value in actual), f"{item!r} not mentioned in {path}")
    elif op == "differs from":
        for other in expected:
            test.assertNotEqual(actual, resolve(load_term(other), path))
    else:
        test.fail(f"unknown check {op!r} in {key!r}")


class TermPolicyPinTests(unittest.TestCase):
    def test_pinned_term_decisions_hold(self) -> None:
        for row in json.loads(PINS_PATH.read_text(encoding="utf-8")):
            for term, checks in row["terms"].items():
                for key, expected in checks.items():
                    with self.subTest(group=row["group"], rule=row["rule"], term=term, check=key):
                        check(self, term, key, expected)

    def test_rules_are_unique(self) -> None:
        rows = json.loads(PINS_PATH.read_text(encoding="utf-8"))
        names = [(row["group"], row["rule"]) for row in rows]
        self.assertEqual(len(names), len(set(names)))

    def test_a_broken_pin_fails(self) -> None:
        result = unittest.TestResult()

        class Probe(unittest.TestCase):
            def runTest(self) -> None:
                check(self, "major/kama", "preferred_translation", "not the real rendering")

        Probe().run(result)
        self.assertEqual(len(result.failures), 1)


class LiveSurfaceTests(unittest.TestCase):
    """The practice-text and sensory-response surfaces report no errors."""

    def test_live_surfaces_have_no_errors(self) -> None:
        for script in ("practice_text_surface_report", "sensory_response_surface_report"):
            with self.subTest(script=script):
                report_module = load_module(f"{script}_pins", f"scripts/{script}.py")
                report = report_module.build_report(report_module.load_terms())
                for key in (
                    "missing_headwords",
                    "missing_supporting_terms",
                    "missing_control_records",
                    "control_example_source_gaps",
                    "missing_translation_surfaces",
                    "translation_control_line_gaps",
                ):
                    self.assertEqual(report["errors"][key], [], key)


if __name__ == "__main__":
    unittest.main()

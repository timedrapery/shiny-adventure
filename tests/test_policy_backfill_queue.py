from __future__ import annotations

import io
import json
import unittest
from unittest import mock

from tests.helpers import load_module


policy_backfill_queue = load_module(
    "policy_backfill_queue", "scripts/policy_backfill_queue.py"
)


class PolicyBackfillQueueTests(unittest.TestCase):
    def test_build_queue_prioritizes_stable_core_terms(self) -> None:
        terms = {
            "dukkha": {
                "entry_type": "major",
                "status": "stable",
                "tags": ["core-doctrine", "four-noble-truths"],
            },
            "sangha": {
                "entry_type": "major",
                "status": "reviewed",
                "tags": ["persons"],
            },
            "sati": {
                "entry_type": "major",
                "status": "stable",
                "tags": ["core-practice"],
                "authority_basis": [{"source": "OSF glossary", "scope": "default"}],
            },
        }

        queue = policy_backfill_queue.build_queue(terms)

        self.assertEqual(queue[0].term, "dukkha")
        self.assertEqual(queue[0].missing_fields, ("authority_basis", "translation_policy"))
        self.assertEqual(queue[0].refinement_fields, ())
        self.assertEqual(queue[1].term, "sati")
        self.assertEqual(queue[1].missing_fields, ("translation_policy",))
        self.assertEqual(queue[1].refinement_fields, ())

    def test_build_queue_keeps_generic_authority_refinement_visible(self) -> None:
        terms = {
            "akusala": {
                "entry_type": "major",
                "status": "stable",
                "tags": ["core-doctrine"],
                "authority_basis": [
                    {
                        "source": "Repository editorial record",
                        "scope": "Legacy policy.",
                    }
                ],
                "translation_policy": {"default_scope": "default"},
            }
        }

        queue = policy_backfill_queue.build_queue(terms)

        self.assertEqual(queue[0].term, "akusala")
        self.assertEqual(queue[0].missing_fields, ())
        self.assertEqual(queue[0].refinement_fields, ("authority_basis_source",))

    def test_main_supports_json_output(self) -> None:
        output = io.StringIO()
        queue = [
            policy_backfill_queue.QueueItem(
                term="dukkha",
                score=20,
                missing_fields=("authority_basis",),
                refinement_fields=(),
                status="stable",
                tags=("core-doctrine",),
            )
        ]

        with mock.patch.object(policy_backfill_queue, "build_queue", return_value=queue):
            with mock.patch.object(policy_backfill_queue, "load_terms", return_value={"dukkha": {}}):
                with mock.patch("sys.argv", ["policy_backfill_queue.py", "--format", "json"]):
                    with mock.patch("sys.stdout", output):
                        result = policy_backfill_queue.main()

        self.assertEqual(result, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload[0]["term"], "dukkha")


if __name__ == "__main__":
    unittest.main()

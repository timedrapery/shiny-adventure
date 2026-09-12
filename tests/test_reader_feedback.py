from __future__ import annotations

import copy
import json
import unittest

from tests.helpers import load_module


paragraph_ids = load_module("paragraph_ids", "scripts/paragraph_ids.py")
reader_feedback = load_module("reader_feedback", "scripts/reader_feedback.py")
registry = load_module("surface_registry", "scripts/surface_registry.py")


def surface(key: str):
    return next(s for s in registry.TRANSLATION_SURFACES if s.key == key)


class ConfigTests(unittest.TestCase):
    def test_committed_config_is_valid(self) -> None:
        config = reader_feedback.load_config()
        self.assertEqual(reader_feedback.config_problems(config), [])

    def test_public_site_ships_without_an_endpoint(self) -> None:
        # No service is deployed yet. The reader script shows nothing until
        # an operator sets the endpoint, so the public site must not claim one.
        self.assertIsNone(reader_feedback.load_config()["endpoint"])

    def test_endpoint_must_be_an_origin(self) -> None:
        config = reader_feedback.load_config()
        config["endpoint"] = "feedback.example.org"
        self.assertTrue(any("endpoint" in p for p in reader_feedback.config_problems(config)))
        config["endpoint"] = "https://feedback.example.org/"
        self.assertTrue(any("slash" in p for p in reader_feedback.config_problems(config)))
        config["endpoint"] = "https://feedback.example.org"
        self.assertEqual(reader_feedback.config_problems(config), [])

    def test_unregistered_enabled_surface_is_rejected(self) -> None:
        config = reader_feedback.load_config()
        config["enabled_surfaces"] = ["nope"]
        self.assertTrue(any("not registered" in p for p in reader_feedback.config_problems(config)))


class TermMapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = reader_feedback.load_term_map("sn36_6")
        self.passage_ids = {
            e["id"] for e in paragraph_ids.load_map(paragraph_ids.map_path("sn36_6"))["passages"]
        }
        self.term_ids = reader_feedback.known_term_ids()

    def test_pilot_term_map_is_valid(self) -> None:
        self.assertEqual(
            reader_feedback.term_map_problems("sn36_6", self.data, self.passage_ids, self.term_ids),
            [],
        )

    def test_unknown_term_and_passage_are_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        data["mappings"]["p999"] = ["not-a-term"]
        problems = reader_feedback.term_map_problems("sn36_6", data, self.passage_ids, self.term_ids)
        self.assertTrue(any("p999 is not a current passage" in p for p in problems))
        self.assertTrue(any("unknown term 'not-a-term'" in p for p in problems))

    def test_basis_is_required(self) -> None:
        data = copy.deepcopy(self.data)
        data["basis"] = ""
        problems = reader_feedback.term_map_problems("sn36_6", data, self.passage_ids, self.term_ids)
        self.assertTrue(any("basis" in p for p in problems))


class QuestionSetTests(unittest.TestCase):
    def test_pilot_question_sets_are_valid_drafts(self) -> None:
        for key in ("sn36_6", "an2_9", "an3_65"):
            data = reader_feedback.load_question_set(key)
            self.assertIsNotNone(data, key)
            self.assertEqual(reader_feedback.question_set_problems(key, data), [], key)
            self.assertEqual(data["editorial_status"], "draft", key)
            self.assertIsNone(data["approved_on"], key)

    def test_approval_needs_evidence_in_the_repository(self) -> None:
        data = copy.deepcopy(reader_feedback.load_question_set("sn36_6"))
        data["editorial_status"] = "approved"
        problems = reader_feedback.question_set_problems("sn36_6", data)
        self.assertTrue(any("approved_on" in p for p in problems))
        self.assertTrue(any("approval_evidence" in p for p in problems))
        data["approved_on"] = "2026-09-12"
        data["approval_evidence"] = "docs/does-not-exist.md"
        problems = reader_feedback.question_set_problems("sn36_6", data)
        self.assertTrue(any("repository file" in p for p in problems))

    def test_draft_must_not_carry_approval_fields(self) -> None:
        data = copy.deepcopy(reader_feedback.load_question_set("sn36_6"))
        data["approved_on"] = "2026-09-12"
        problems = reader_feedback.question_set_problems("sn36_6", data)
        self.assertTrue(any("must not carry approval" in p for p in problems))

    def test_each_role_appears_exactly_once(self) -> None:
        data = copy.deepcopy(reader_feedback.load_question_set("sn36_6"))
        data["questions"] = data["questions"][:2]
        problems = reader_feedback.question_set_problems("sn36_6", data)
        self.assertTrue(any("role 'reread'" in p for p in problems))

    def test_content_version_changes_when_a_prompt_changes(self) -> None:
        data = reader_feedback.load_question_set("sn36_6")
        before = reader_feedback.question_set_sha256(data)
        edited = copy.deepcopy(data)
        edited["questions"][1]["prompt"] += " Really?"
        self.assertNotEqual(before, reader_feedback.question_set_sha256(edited))
        # Guidance is for assessors, not readers, so it is not part of what
        # readers saw.
        guidance_only = copy.deepcopy(data)
        guidance_only["assessment_guidance"]["paraphrase"] += " More."
        self.assertEqual(before, reader_feedback.question_set_sha256(guidance_only))

    def test_assessment_guidance_must_say_house_terms_are_not_required(self) -> None:
        data = copy.deepcopy(reader_feedback.load_question_set("sn36_6"))
        del data["assessment_guidance"]["specific"]["not_required"]
        problems = reader_feedback.question_set_problems("sn36_6", data)
        self.assertTrue(any("not_required" in p for p in problems))


class RepositoryInputTests(unittest.TestCase):
    def test_all_feedback_inputs_pass(self) -> None:
        self.assertEqual(reader_feedback.check(), [])

    def test_only_the_pilot_text_is_enabled(self) -> None:
        self.assertEqual(reader_feedback.enabled_surfaces(), ["sn36_6"])


class ManifestScriptTests(unittest.TestCase):
    def test_manifest_script_cannot_be_closed_early(self) -> None:
        text = reader_feedback.manifest_script({"format": 1, "x": "</script><b>"})
        self.assertEqual(text.count("</script>"), 1)
        self.assertIn('id="reader-feedback-manifest"', text)
        body = text.split(">", 1)[1].rsplit("<", 1)[0]
        self.assertEqual(json.loads(body)["x"], "</script><b>")


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schema" / "PALI_TERM_SCHEMA.json"
DATA_DICTIONARY_PATH = REPO_ROOT / "docs" / "data-dictionary.md"
AUTHORITY_DOC_PATH = REPO_ROOT / "docs" / "osf-editorial-authority.md"
TERMS_DIR = REPO_ROOT / "terms"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_priorities() -> set[str]:
    schema = load_json(SCHEMA_PATH)
    authority_basis = schema["$defs"]["authorityBasis"]["properties"]["priority"]
    return set(authority_basis["enum"])


def term_priorities() -> set[str]:
    priorities: set[str] = set()
    for path in sorted(TERMS_DIR.rglob("*.json")):
        data = load_json(path)
        if not isinstance(data, dict):
            continue
        authority_basis = data.get("authority_basis")
        if not isinstance(authority_basis, list):
            continue
        for item in authority_basis:
            if not isinstance(item, dict):
                continue
            priority = item.get("priority")
            if isinstance(priority, str):
                priorities.add(priority)
    return priorities


class AuthorityPriorityModelTests(unittest.TestCase):
    def test_schema_allows_all_priorities_used_in_live_terms(self) -> None:
        allowed = schema_priorities()
        used = term_priorities()
        unsupported = sorted(used - allowed)
        self.assertEqual(unsupported, [], f"unsupported priorities in live terms: {unsupported}")

    def test_docs_list_all_schema_priority_values(self) -> None:
        priorities = schema_priorities()
        data_dictionary = DATA_DICTIONARY_PATH.read_text(encoding="utf-8")
        authority_doc = AUTHORITY_DOC_PATH.read_text(encoding="utf-8")

        missing_from_dictionary = sorted(
            priority for priority in priorities if f"`{priority}`" not in data_dictionary
        )
        missing_from_authority_doc = sorted(
            priority for priority in priorities if f"`{priority}`" not in authority_doc
        )

        self.assertEqual(
            missing_from_dictionary,
            [],
            f"missing priority values in data dictionary: {missing_from_dictionary}",
        )
        self.assertEqual(
            missing_from_authority_doc,
            [],
            f"missing priority values in editorial authority doc: {missing_from_authority_doc}",
        )


if __name__ == "__main__":
    unittest.main()

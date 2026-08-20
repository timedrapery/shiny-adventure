"""Every governed term a cluster declares must appear in its glossary.

Cluster reports declare their members in HEADWORD_TERMS and SUPPORTING_TERMS
and validate that the records exist, but several render_glossary functions
iterated a hardcoded subset -- one representative member per family. The
result was governed vocabulary that existed as JSON and appeared in no output
anywhere: ten of the bondage-imagery cluster's seventeen terms, including the
four floods and all four bodily knots.

A translator consulting the repository's own generated sheets would never have
seen them, which defeats the point of governing them.
"""

from __future__ import annotations

import importlib
import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.cluster_registry import CLUSTER_SURFACES  # noqa: E402


def load_terms() -> dict[str, dict[str, object]]:
    terms = {}
    for path in (REPO_ROOT / "terms").rglob("*.json"):
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        stem = data.get("normalized_term")
        if stem:
            terms[stem] = data
    return terms


class ClusterGlossaryCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.terms = load_terms()

    def test_every_declared_term_appears_in_its_glossary(self) -> None:
        checked = 0
        for cluster in CLUSTER_SURFACES:
            module_name = cluster.script_relpath.replace("/", ".").removesuffix(".py")
            try:
                module = importlib.import_module(module_name)
            except Exception:
                continue
            render = getattr(module, "render_glossary", None)
            headwords = getattr(module, "HEADWORD_TERMS", None)
            supporting = getattr(module, "SUPPORTING_TERMS", None)
            if render is None or headwords is None or supporting is None:
                continue

            with self.subTest(cluster=cluster.label):
                glossary = render(self.terms)
                missing = []
                for stem in list(headwords) + list(supporting):
                    record = self.terms.get(stem)
                    if record is None:
                        continue
                    # The glossary prints the display term, not the stem.
                    if str(record.get("term", "")) not in glossary:
                        missing.append(stem)
                self.assertEqual(
                    missing,
                    [],
                    f"{cluster.label}: declared but not rendered: {missing}",
                )
                checked += 1

        self.assertGreater(checked, 10, "expected to check most clusters")

    def test_bondage_imagery_renders_all_four_of_each_set(self) -> None:
        """The specific regression: one representative member per family."""
        module = importlib.import_module("scripts.bondage_imagery_cluster_report")
        glossary = module.render_glossary(self.terms)

        for stem in (
            "kamogha", "bhavogha", "ditthogha", "avijjogha",
            "kamayoga", "bhavayoga", "ditthiyoga", "avijjayoga",
            "abhijjha-kayagantha", "byapada-kayagantha",
            "silabbata-paramasa-kayagantha", "idamsacca-abhinivesa-kayagantha",
        ):
            with self.subTest(term=stem):
                self.assertIn(str(self.terms[stem]["term"]), glossary)


if __name__ == "__main__":
    unittest.main()

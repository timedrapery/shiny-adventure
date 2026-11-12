#!/usr/bin/env python3
"""Audit and generate translator-facing outputs for the five-heaps cluster."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from scripts import cluster_report_common as common
    from scripts.cluster_report_common import load_terms, missing_terms, example_source_gaps, weak_authority_terms
except ModuleNotFoundError:
    import cluster_report_common as common
    from cluster_report_common import load_terms, missing_terms, example_source_gaps, weak_authority_terms


REPO_ROOT = Path(__file__).resolve().parent.parent
TERMS_DIR = REPO_ROOT / "terms"
OUTPUT_DIR = REPO_ROOT / "docs" / "generated"

HEADWORD_TERMS = [
    "khandha",
    "rupa",
    "vedana",
    "sanna",
    "sankhara",
    "vinnana",
    "upadana",
    "sakkaya",
    "sakkaya-ditthi",
    "atta",
    "anatta",
]

COLLECTIVE_TERMS = [
    "pancakkhandha",
    "pancupadanakkhandha",
    "rupakkhandha",
    "vedanakkhandha",
    "sannakkhandha",
    "sankharakkhandha",
    "vinnanakkhandha",
]

FORMULA_TERMS = [
    "katame-ca-bhikkhave-pancupadanakkhandha",
    "yam-kinci-rupam-vedana-sanna-sankhara-vinnanam",
    "katamo-ca-bhikkhave-sakkayo",
    "bharo-have-pancakkhandha",
    "imesam-pancannam-upadanakkhandhanam-assadanca-adinavanca-nissarananca",
]


def thin_collective_terms(terms: dict[str, dict[str, object]]) -> list[str]:
    thin: list[str] = []
    for stem in COLLECTIVE_TERMS:
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        examples = data.get("example_phrases")
        policy = data.get("translation_policy")
        related = data.get("related_terms")
        if not isinstance(examples, list) or not examples or not isinstance(policy, dict) or not isinstance(related, list):
            thin.append(stem)
    return thin


def inconsistent_clung_to_heap_terms(terms: dict[str, dict[str, object]]) -> list[str]:
    flagged: list[str] = []
    expected = {
        "pancupadanakkhandha": "five clung-to heaps",
        "katame-ca-bhikkhave-pancupadanakkhandha": "and what, bhikkhus, are the five clung-to heaps",
        "katamo-ca-bhikkhave-sakkayo": "and what, bhikkhus, is identity, the five clung-to heaps",
        "imesam-pancannam-upadanakkhandhanam-assadanca-adinavanca-nissarananca": "of these five clung-to heaps, the gratification as gratification, the danger as danger, and the escape as escape",
    }
    for stem, expected_rendering in expected.items():
        data = terms.get(stem)
        if not isinstance(data, dict):
            continue
        preferred = data.get("preferred_translation")
        if preferred != expected_rendering:
            flagged.append(stem)
    return flagged


def build_report(terms: dict[str, dict[str, object]]) -> dict[str, object]:
    all_priority = HEADWORD_TERMS + COLLECTIVE_TERMS + FORMULA_TERMS
    return {
        "summary": {
            "headwords_present": len(HEADWORD_TERMS) - len(missing_terms(terms, HEADWORD_TERMS)),
            "headwords_expected": len(HEADWORD_TERMS),
            "collective_terms_present": len(COLLECTIVE_TERMS) - len(missing_terms(terms, COLLECTIVE_TERMS)),
            "collective_terms_expected": len(COLLECTIVE_TERMS),
            "formula_records_present": len(FORMULA_TERMS) - len(missing_terms(terms, FORMULA_TERMS)),
            "formula_records_expected": len(FORMULA_TERMS),
        },
        "errors": {
            "missing_headwords": missing_terms(terms, HEADWORD_TERMS),
            "missing_collective_terms": missing_terms(terms, COLLECTIVE_TERMS),
            "missing_formula_records": missing_terms(terms, FORMULA_TERMS),
            "cluster_example_source_gaps": example_source_gaps(terms, all_priority),
        },
        "warnings": {
            "headwords_with_thin_authority_basis": weak_authority_terms(terms, HEADWORD_TERMS),
            "collective_terms_still_thin": thin_collective_terms(terms),
            "inconsistent_clung_to_heap_renderings": inconsistent_clung_to_heap_terms(terms),
        },
    }


def render_glossary(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Five Heaps Cluster Glossary",
        "",
        "| Pali | Default | Allowed alternates | Discouraged |",
        "| --- | --- | --- | --- |",
    ]
    for stem in HEADWORD_TERMS + ["pancakkhandha", "pancupadanakkhandha"]:
        data = terms[stem]
        alts = ", ".join(data.get("alternative_translations", []))
        discouraged = ", ".join(data.get("discouraged_translations", []))
        lines.append(
            f"| {data.get('term')} | {data.get('preferred_translation')} | {alts or '-'} | {discouraged or '-'} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_consistency_sheet(terms: dict[str, dict[str, object]]) -> str:
    members = [
        "rupa",
        "vedana",
        "sanna",
        "sankhara",
        "vinnana",
        "rupakkhandha",
        "vedanakkhandha",
        "sannakkhandha",
        "sankharakkhandha",
        "vinnanakkhandha",
    ]
    lines = [
        "# Five Heaps Consistency Sheet",
        "",
        "## Headwords",
        "",
    ]
    for stem in members[:5]:
        data = terms[stem]
        lines.append(f"- `{data.get('term')}`: `{data.get('preferred_translation')}`")
    lines.extend(["", "## Constituent Heap Compounds", ""])
    for stem in members[5:]:
        data = terms[stem]
        lines.append(f"- `{data.get('term')}`: `{data.get('preferred_translation')}`")
    return "\n".join(lines)


def render_formula_sheet(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Five Heaps Formula Sheet",
        "",
    ]
    for stem in FORMULA_TERMS:
        data = terms[stem]
        lines.append(f"- `{data.get('term')}` -> {data.get('preferred_translation')}")
    return "\n".join(lines)


def render_translator_brief(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Heaps vs. Clung-To Heaps Brief",
        "",
        "## Defaults",
        "",
        f"- Keep `{terms['khandha']['term']}` as `{terms['khandha']['preferred_translation']}`.",
        f"- Keep `{terms['pancakkhandha']['term']}` as `{terms['pancakkhandha']['preferred_translation']}`.",
        f"- Keep `{terms['pancupadanakkhandha']['term']}` as `{terms['pancupadanakkhandha']['preferred_translation']}`.",
        f"- Keep `{terms['sakkaya']['term']}` as `{terms['sakkaya']['preferred_translation']}` and read it through the five clung-to heaps.",
        "",
        "## Practical Distinctions",
        "",
        "- Do not flatten `pañcakkhandhā` and `pañcupādānakkhandhā` into the same English.",
        "- In heap context, keep `saṅkhārā` as `putting-together activities` rather than importing the dependent-arising link or `volitional formations` by habit.",
        "- In heap context, keep `viññāṇa` as `knowing` unless comparative prose clearly calls for `consciousness`.",
        "- Use the dedicated phrase records for the standard headings, the `yaṃ kiñci ...` pattern, the burden line, and the `sakkāya` equation.",
    ]
    return "\n".join(lines)


def render_cross_cluster_note(terms: dict[str, dict[str, object]]) -> str:
    lines = [
        "# Five Heaps Cross-Cluster Note",
        "",
        f"- `{terms['upadana']['term']}` stays `{terms['upadana']['preferred_translation']}` as a headword, but `{terms['pancupadanakkhandha']['term']}` is governed as `{terms['pancupadanakkhandha']['preferred_translation']}` as a fixed whole expression.",
        f"- `{terms['sankhara']['term']}` keeps a heap-context override as `{terms['sankharakkhandha']['preferred_translation']}` while preserving its dependent-arising policy elsewhere.",
        f"- `{terms['vinnana']['term']}` stays `{terms['vinnana']['preferred_translation']}` across both heap and dependent-arising contexts; use the formula records to keep the voice stable.",
        f"- `{terms['anatta']['term']}` and `{terms['atta']['term']}` are tied to the heap family through the standard not-self and self-view formulas rather than through abstract metaphysical claims.",
    ]
    return "\n".join(lines)


def write_outputs(terms: dict[str, dict[str, object]]) -> list[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        OUTPUT_DIR / "five-heaps-cluster-glossary.md": render_glossary(terms),
        OUTPUT_DIR / "five-heaps-consistency-sheet.md": render_consistency_sheet(terms),
        OUTPUT_DIR / "five-heaps-formula-sheet.md": render_formula_sheet(terms),
        OUTPUT_DIR / "heaps-vs-clung-to-heaps-brief.md": render_translator_brief(terms),
        OUTPUT_DIR / "five-heaps-cross-cluster-note.md": render_cross_cluster_note(terms),
    }
    for path, content in outputs.items():
        path.write_text(content + "\n", encoding="utf-8")
    return sorted(outputs)


def print_text_report(report: dict[str, object]) -> None:
    common.print_text_report("Five Heaps Cluster Report", report)


def main() -> int:
    return common.run_cli(sys.modules[__name__])


if __name__ == "__main__":
    sys.exit(main())

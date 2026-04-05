#!/usr/bin/env python3
"""Shared helpers for actionable enforcement diagnostics."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field


MAJOR_POLICY_EXAMPLES = (
    "terms/major/dukkha.json",
    "terms/major/sati.json",
    "terms/major/sankhara.json",
)
RELATIONSHIP_EXAMPLES = (
    "terms/major/sati.json",
    "terms/major/samadhi.json",
)
STATUS_EXAMPLES = (
    "docs/review-status-model.md",
    "terms/major/dukkha.json",
)
CLUSTER_DOC_EXAMPLES = (
    "docs/knowledge-seeing-understanding-cluster-map.md",
    "docs/bondage-imagery-cluster-map.md",
)

FIELD_SNIPPETS = {
    "authority_basis": json.dumps(
        [
            {
                "source": "OSF glossary",
                "scope": "Supports the preferred translation.",
            }
        ],
        ensure_ascii=False,
    ),
    "translation_policy": json.dumps(
        {
            "default_scope": "most doctrinal contexts",
            "when_not_to_apply": "Use a recorded context override instead of rotating ad hoc.",
            "compound_inheritance": "case-by-case",
            "drift_risk": "Prevents uncontrolled synonym drift.",
        },
        ensure_ascii=False,
    ),
    "context_rules": json.dumps(
        [
            {
                "context": "most doctrinal contexts",
                "rendering": "house default",
                "notes": "Use this by default.",
            }
        ],
        ensure_ascii=False,
    ),
    "related_terms": json.dumps(["samadhi", "samma-sati"], ensure_ascii=False),
    "discouraged_translations": json.dumps(
        ["common but uncontrolled alternate"], ensure_ascii=False
    ),
    "example_phrases": json.dumps(
        [{"pali": "headword", "translation": "house default", "source": "SN 12.2"}],
        ensure_ascii=False,
    ),
    "sutta_references": json.dumps(["SN 12.2"], ensure_ascii=False),
}

FIELD_MODEL_EXAMPLES = {
    "authority_basis": ("terms/major/dukkha.json", "terms/major/sankhara.json"),
    "translation_policy": (
        "terms/major/paticcasamuppada.json",
        "terms/major/nibbana.json",
    ),
    "context_rules": ("terms/major/dukkha.json", "terms/major/sankhara.json"),
    "discouraged_translations": ("terms/major/dukkha.json", "terms/major/sati.json"),
    "related_terms": RELATIONSHIP_EXAMPLES,
    "example_phrases": ("terms/major/dukkha.json", "terms/major/paticcasamuppada.json"),
    "sutta_references": ("terms/major/dukkha.json", "terms/major/nibbana.json"),
    "notes": MAJOR_POLICY_EXAMPLES,
}


@dataclass(frozen=True)
class RepairDiagnostic:
    severity: str
    rule: str
    summary: str
    why: str
    fix: str
    file: str | None = None
    category: str | None = None
    code: str | None = None
    examples: tuple[str, ...] = field(default_factory=tuple)


def diagnostics_as_json(diagnostics: list[RepairDiagnostic]) -> list[dict[str, object]]:
    return [asdict(diagnostic) for diagnostic in diagnostics]


def print_diagnostics(title: str, diagnostics: list[RepairDiagnostic]) -> None:
    if not diagnostics:
        return

    print(f"{title}:")
    current_category: str | None = None
    for diagnostic in diagnostics:
        if diagnostic.category and diagnostic.category != current_category:
            print(f"{diagnostic.category}:")
            current_category = diagnostic.category
        print(f"- Rule violated: {diagnostic.rule}")
        if diagnostic.file:
            print(f"  File: {diagnostic.file}")
        if diagnostic.code:
            print(f"  Code: {diagnostic.code}")
        print(f"  What failed: {diagnostic.summary}")
        print(f"  Why it matters: {diagnostic.why}")
        print(f"  Minimal safe fix: {diagnostic.fix}")
        if diagnostic.examples:
            print(f"  Good repo example(s): {', '.join(diagnostic.examples)}")
        print()


def field_snippet(field: str) -> str | None:
    return FIELD_SNIPPETS.get(field)


def field_examples(field: str) -> tuple[str, ...]:
    return FIELD_MODEL_EXAMPLES.get(field, MAJOR_POLICY_EXAMPLES)

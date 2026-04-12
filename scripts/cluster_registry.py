#!/usr/bin/env python3
"""Authoritative registry of CI-enforced family surfaces."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class ClusterSurface:
    key: str
    label: str
    doc_relpath: str
    script_relpath: str
    test_relpaths: tuple[str, ...]

    @property
    def doc_path(self) -> Path:
        return REPO_ROOT / self.doc_relpath

    @property
    def script_path(self) -> Path:
        return REPO_ROOT / self.script_relpath

    @property
    def test_paths(self) -> tuple[Path, ...]:
        return tuple(REPO_ROOT / relpath for relpath in self.test_relpaths)


CLUSTER_SURFACES: tuple[ClusterSurface, ...] = (
    ClusterSurface(
        key="abandonment_sequence",
        label="Abandonment-sequence cluster",
        doc_relpath="docs/abandonment-quenching-exhaustion-map.md",
        script_relpath="scripts/abandonment_sequence_cluster_report.py",
        test_relpaths=(
            "tests/test_abandonment_sequence_cluster_report.py",
            "tests/test_abandonment_sequence_policy.py",
        ),
    ),
    ClusterSurface(
        key="bondage_imagery",
        label="Bondage-imagery cluster",
        doc_relpath="docs/bondage-imagery-cluster-map.md",
        script_relpath="scripts/bondage_imagery_cluster_report.py",
        test_relpaths=(
            "tests/test_bondage_imagery_cluster_report.py",
            "tests/test_bondage_imagery_policy.py",
        ),
    ),
    ClusterSurface(
        key="bondage_residue",
        label="Bondage / residue cluster",
        doc_relpath="docs/bondage-residue-cluster-map.md",
        script_relpath="scripts/bondage_residue_cluster_report.py",
        test_relpaths=(
            "tests/test_bondage_residue_cluster_report.py",
            "tests/test_bondage_residue_policy.py",
        ),
    ),
    ClusterSurface(
        key="consummation_interface",
        label="Consummation / unconditioned interface cluster",
        doc_relpath="docs/consummation-unconditioned-interface-map.md",
        script_relpath="scripts/consummation_interface_cluster_report.py",
        test_relpaths=(
            "tests/test_consummation_interface_cluster_report.py",
            "tests/test_consummation_interface_policy.py",
        ),
    ),
    ClusterSurface(
        key="craving_appropriation",
        label="Craving / appropriation cluster",
        doc_relpath="docs/craving-appropriation-affective-attachment-map.md",
        script_relpath="scripts/craving_appropriation_cluster_report.py",
        test_relpaths=(
            "tests/test_craving_appropriation_cluster_report.py",
            "tests/test_craving_appropriation_policy.py",
        ),
    ),
    ClusterSurface(
        key="crossing_release_interface",
        label="Crossing / release interface cluster",
        doc_relpath="docs/crossing-escape-release-interface-map.md",
        script_relpath="scripts/crossing_release_interface_cluster_report.py",
        test_relpaths=(
            "tests/test_crossing_release_interface_cluster_report.py",
            "tests/test_crossing_release_interface_policy.py",
        ),
    ),
    ClusterSurface(
        key="dependent_arising",
        label="Dependent arising cluster",
        doc_relpath="docs/dependent-arising-cluster-audit.md",
        script_relpath="scripts/dependent_arising_cluster_report.py",
        test_relpaths=(
            "tests/test_dependent_arising_cluster_report.py",
        ),
    ),
    ClusterSurface(
        key="emptiness_signless_wishless",
        label="Emptiness / signless / wishless interface cluster",
        doc_relpath="docs/emptiness-signless-wishless-interface-map.md",
        script_relpath="scripts/emptiness_signless_wishless_cluster_report.py",
        test_relpaths=(
            "tests/test_emptiness_signless_wishless_cluster_report.py",
            "tests/test_emptiness_signless_wishless_policy.py",
        ),
    ),
    ClusterSurface(
        key="experience_process",
        label="Experience / process cluster",
        doc_relpath="docs/experience-process-cluster-map.md",
        script_relpath="scripts/experience_process_cluster_report.py",
        test_relpaths=(
            "tests/test_experience_process_cluster_report.py",
            "tests/test_experience_process_policy.py",
        ),
    ),
    ClusterSurface(
        key="five_heaps",
        label="Five heaps cluster",
        doc_relpath="docs/five-heaps-cluster-audit.md",
        script_relpath="scripts/five_heaps_cluster_report.py",
        test_relpaths=(
            "tests/test_five_heaps_cluster_report.py",
        ),
    ),
    ClusterSurface(
        key="four_noble_truths",
        label="Four noble truths cluster",
        doc_relpath="docs/four-noble-truths-correct-noble-practice.md",
        script_relpath="scripts/four_noble_truths_cluster_report.py",
        test_relpaths=(
            "tests/test_four_noble_truths_cluster_report.py",
            "tests/test_four_noble_truths_practice_policy.py",
            "tests/test_dukkha_nirodha_scope_policy.py",
        ),
    ),
    ClusterSurface(
        key="identity_construction",
        label="Identity-construction cluster",
        doc_relpath="docs/identity-construction-cluster-map.md",
        script_relpath="scripts/identity_construction_cluster_report.py",
        test_relpaths=(
            "tests/test_identity_construction_cluster_report.py",
            "tests/test_identity_construction_policy.py",
        ),
    ),
    ClusterSurface(
        key="jhana",
        label="Jhana cluster",
        doc_relpath="docs/jhana-cluster-map.md",
        script_relpath="scripts/jhana_cluster_report.py",
        test_relpaths=(
            "tests/test_jhana_cluster_report.py",
        ),
    ),
    ClusterSurface(
        key="kama",
        label="Kama cluster",
        doc_relpath="docs/kama-sensuality-cluster-map.md",
        script_relpath="scripts/kama_cluster_report.py",
        test_relpaths=(
            "tests/test_kama_cluster_report.py",
            "tests/test_kama_policy.py",
        ),
    ),
    ClusterSurface(
        key="knowledge",
        label="Knowledge / seeing / understanding cluster",
        doc_relpath="docs/knowledge-seeing-understanding-cluster-map.md",
        script_relpath="scripts/knowledge_cluster_report.py",
        test_relpaths=(
            "tests/test_knowledge_cluster_report.py",
            "tests/test_knowledge_policy.py",
        ),
    ),
    ClusterSurface(
        key="osf_reconciliation",
        label="OSF reconciliation layer",
        doc_relpath="docs/osf-reconciliation-framework.md",
        script_relpath="scripts/osf_reconciliation_report.py",
        test_relpaths=(
            "tests/test_osf_reconciliation_report.py",
            "tests/test_osf_reconciliation_policy.py",
        ),
    ),
    ClusterSurface(
        key="path_factor",
        label="Path-factor cluster",
        doc_relpath="docs/path-factor-core-loop.md",
        script_relpath="scripts/path_factor_cluster_report.py",
        test_relpaths=(
            "tests/test_path_factor_cluster_report.py",
            "tests/test_path_factor_core_loop_policy.py",
        ),
    ),
    ClusterSurface(
        key="practice_text_surface",
        label="Practice-text surface",
        doc_relpath="docs/practice-text-surface-map.md",
        script_relpath="scripts/practice_text_surface_report.py",
        test_relpaths=(
            "tests/test_practice_text_surface_report.py",
            "tests/test_practice_text_policy.py",
        ),
    ),
    ClusterSurface(
        key="sensory_response_surface",
        label="Sensory-response surface",
        doc_relpath="docs/sensory-response-surface-map.md",
        script_relpath="scripts/sensory_response_surface_report.py",
        test_relpaths=(
            "tests/test_sensory_response_surface_report.py",
            "tests/test_sensory_response_policy.py",
        ),
    ),
    ClusterSurface(
        key="sense_fields",
        label="Sense-fields cluster",
        doc_relpath="docs/sense-fields-cluster-map.md",
        script_relpath="scripts/sense_fields_cluster_report.py",
        test_relpaths=(
            "tests/test_sense_fields_cluster_report.py",
        ),
    ),
    ClusterSurface(
        key="three_marks",
        label="Three marks cluster",
        doc_relpath="docs/three-marks-cluster-map.md",
        script_relpath="scripts/three_marks_cluster_report.py",
        test_relpaths=(
            "tests/test_three_marks_cluster_report.py",
        ),
    ),
    ClusterSurface(
        key="verbal_knowing",
        label="Verbal knowing / recognition cluster",
        doc_relpath="docs/verbal-knowing-recognition-cluster-map.md",
        script_relpath="scripts/verbal_knowing_cluster_report.py",
        test_relpaths=(
            "tests/test_verbal_knowing_cluster_report.py",
            "tests/test_verbal_knowing_policy.py",
        ),
    ),
)


def build_cluster_checks(python_executable: str) -> tuple[tuple[str, list[str]], ...]:
    return tuple(
        (
            cluster.label,
            [python_executable, cluster.script_relpath, "--strict"],
        )
        for cluster in CLUSTER_SURFACES
    )

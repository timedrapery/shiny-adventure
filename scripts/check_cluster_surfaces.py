#!/usr/bin/env python3
"""Verify that each CI-enforced family surface has its required files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from scripts.cluster_registry import CLUSTER_SURFACES
    from scripts.repair_guidance import (
        RepairDiagnostic,
        diagnostics_as_json,
        print_diagnostics,
        CLUSTER_DOC_EXAMPLES,
    )
except ModuleNotFoundError:
    from cluster_registry import CLUSTER_SURFACES
    from repair_guidance import (
        RepairDiagnostic,
        diagnostics_as_json,
        print_diagnostics,
        CLUSTER_DOC_EXAMPLES,
    )


REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
SCRIPTS_DIR = REPO_ROOT / "scripts"
TESTS_DIR = REPO_ROOT / "tests"

MISSING_DOC_RE = re.compile(
    r"^(?P<cluster>[^:]+): cluster authority doc is missing: (?P<path>.+)$"
)
MISSING_SCRIPT_RE = re.compile(
    r"^(?P<cluster>[^:]+): cluster report script is missing: (?P<path>.+)$"
)
MISSING_TEST_RE = re.compile(
    r"^(?P<cluster>[^:]+): cluster regression test is missing: (?P<path>.+)$"
)
UNMANAGED_SCRIPT_RE = re.compile(
    r"^unmanaged cluster report script present without registry coverage: (?P<path>.+)$"
)
UNMANAGED_TEST_RE = re.compile(
    r"^unmanaged cluster report test present without registry coverage: (?P<path>.+)$"
)
DUPLICATE_RE = re.compile(
    r"^(?P<cluster>[^:]+): duplicate cluster (?P<kind>doc|script|test) path '(?P<path>.+)' in registry$"
)


def collect_expected_cluster_script_names() -> set[str]:
    return {Path(cluster.script_relpath).name for cluster in CLUSTER_SURFACES}


def collect_expected_cluster_test_names() -> set[str]:
    names: set[str] = set()
    for cluster in CLUSTER_SURFACES:
        names.update(Path(relpath).name for relpath in cluster.test_relpaths)
    return names


def collect_issues() -> list[str]:
    issues: list[str] = []

    seen_doc_paths: set[str] = set()
    seen_script_paths: set[str] = set()
    seen_test_paths: set[str] = set()

    for cluster in CLUSTER_SURFACES:
        doc_path = REPO_ROOT / cluster.doc_relpath
        script_path = REPO_ROOT / cluster.script_relpath

        if cluster.doc_relpath in seen_doc_paths:
            issues.append(
                f"{cluster.key}: duplicate cluster doc path '{cluster.doc_relpath}' in registry"
            )
        seen_doc_paths.add(cluster.doc_relpath)

        if cluster.script_relpath in seen_script_paths:
            issues.append(
                f"{cluster.key}: duplicate cluster script path '{cluster.script_relpath}' in registry"
            )
        seen_script_paths.add(cluster.script_relpath)

        if not doc_path.exists():
            issues.append(
                f"{cluster.key}: cluster authority doc is missing: {cluster.doc_relpath}"
            )
        if not script_path.exists():
            issues.append(
                f"{cluster.key}: cluster report script is missing: {cluster.script_relpath}"
            )

        for relpath in cluster.test_relpaths:
            path = REPO_ROOT / relpath
            if relpath in seen_test_paths:
                issues.append(
                    f"{cluster.key}: duplicate cluster test path '{relpath}' in registry"
                )
            seen_test_paths.add(relpath)
            if not path.exists():
                issues.append(
                    f"{cluster.key}: cluster regression test is missing: {relpath}"
                )

    actual_cluster_scripts = {
        path.name
        for path in SCRIPTS_DIR.glob("*_cluster_report.py")
    }
    actual_cluster_scripts.update(
        path.name
        for path in SCRIPTS_DIR.glob("osf_reconciliation_report.py")
    )
    expected_cluster_scripts = collect_expected_cluster_script_names()
    unmanaged_scripts = sorted(actual_cluster_scripts - expected_cluster_scripts)
    for name in unmanaged_scripts:
        issues.append(
            f"unmanaged cluster report script present without registry coverage: scripts/{name}"
        )

    actual_cluster_tests = {
        path.name
        for path in TESTS_DIR.glob("test_*_cluster_report.py")
    }
    actual_cluster_tests.update(
        path.name
        for path in TESTS_DIR.glob("test_osf_reconciliation_report.py")
    )
    expected_cluster_tests = collect_expected_cluster_test_names()
    unmanaged_tests = sorted(actual_cluster_tests - expected_cluster_tests)
    for name in unmanaged_tests:
        issues.append(
            f"unmanaged cluster report test present without registry coverage: tests/{name}"
        )

    return issues


def issue_to_diagnostic(issue: str) -> RepairDiagnostic:
    match = MISSING_DOC_RE.match(issue)
    if match:
        return RepairDiagnostic(
            severity="error",
            category="Cluster Surfaces",
            code="missing_cluster_doc",
            file=match.group("path"),
            rule="Each CI-enforced cluster needs one authority document",
            summary=f"The cluster registry expects `{match.group('path')}`, but it is missing",
            why="Without an authority doc, contributors have no family-level editorial surface to consult when the cluster report fails.",
            fix="Add the missing markdown authority doc in `docs/` using the existing cluster-map style, then rerun `python scripts/check_cluster_surfaces.py`.",
            examples=CLUSTER_DOC_EXAMPLES,
        )

    match = MISSING_SCRIPT_RE.match(issue)
    if match:
        return RepairDiagnostic(
            severity="error",
            category="Cluster Surfaces",
            code="missing_cluster_script",
            file=match.group("path"),
            rule="Each CI-enforced cluster needs one report script",
            summary=f"The cluster registry expects `{match.group('path')}`, but it is missing",
            why="Without the report script, CI cannot enforce the family's internal consistency or generate its governed outputs.",
            fix="Add the missing cluster report script in `scripts/` and keep its headword set aligned with the authority doc and tests.",
            examples=("scripts/knowledge_cluster_report.py", "scripts/bondage_imagery_cluster_report.py"),
        )

    match = MISSING_TEST_RE.match(issue)
    if match:
        return RepairDiagnostic(
            severity="error",
            category="Cluster Surfaces",
            code="missing_cluster_test",
            file=match.group("path"),
            rule="Each CI-enforced cluster needs regression coverage",
            summary=f"The cluster registry expects `{match.group('path')}`, but it is missing",
            why="Without tests, the cluster script can change behavior without a stable contract for CI to enforce.",
            fix="Add the missing regression test in `tests/` and cover the cluster's expected presence, mismatch, and write-output behaviors.",
            examples=("tests/test_knowledge_cluster_report.py", "tests/test_bondage_imagery_cluster_report.py"),
        )

    match = UNMANAGED_SCRIPT_RE.match(issue)
    if match:
        return RepairDiagnostic(
            severity="error",
            category="Cluster Surfaces",
            code="unmanaged_cluster_script",
            file=match.group("path"),
            rule="Cluster report scripts must be registered if CI is meant to enforce them",
            summary=f"`{match.group('path')}` exists but is not represented in the cluster registry",
            why="Unregistered cluster scripts are easy to forget, which leaves family enforcement partial and inconsistent.",
            fix="Either register the script in `scripts/cluster_registry.py` with its authority doc and tests, or remove the unmanaged script if it is not ready for CI enforcement.",
            examples=("scripts/cluster_registry.py",),
        )

    match = UNMANAGED_TEST_RE.match(issue)
    if match:
        return RepairDiagnostic(
            severity="error",
            category="Cluster Surfaces",
            code="unmanaged_cluster_test",
            file=match.group("path"),
            rule="Cluster regression tests must map to a registered CI-enforced family",
            summary=f"`{match.group('path')}` exists but is not represented in the cluster registry",
            why="If tests are not tied to a registered cluster, contributors cannot tell whether the family is intentionally enforced or half-integrated.",
            fix="Either register the corresponding cluster in `scripts/cluster_registry.py` or remove the stray test if the cluster is not supposed to be CI-enforced yet.",
            examples=("scripts/cluster_registry.py",),
        )

    match = DUPLICATE_RE.match(issue)
    if match:
        return RepairDiagnostic(
            severity="error",
            category="Cluster Surfaces",
            code="duplicate_cluster_registry_path",
            file=match.group("path"),
            rule="Each registered cluster surface path must be unique",
            summary=f"The registry reuses `{match.group('path')}` as a cluster {match.group('kind')} path",
            why="Duplicate registry paths make cluster ownership ambiguous and can silently hide missing surfaces in another family.",
            fix="Give each cluster its own doc, script, and test paths in `scripts/cluster_registry.py` so CI can reason about one family at a time.",
            examples=("scripts/cluster_registry.py",),
        )

    return RepairDiagnostic(
        severity="error",
        category="Cluster Surfaces",
        code="cluster_surface_issue",
        file=None,
        rule="Cluster surface coverage must be explicit and complete",
        summary=issue,
        why="CI needs a complete authority doc, script, and test chain for every enforced doctrinal family.",
        fix="Repair the missing or ambiguous cluster surface named above, then rerun `python scripts/check_cluster_surfaces.py`.",
        examples=("scripts/cluster_registry.py",),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit a JSON report with actionable repair guidance.",
    )
    if argv is None and __name__ != "__main__":
        argv = []
    args = parser.parse_args(argv)

    issues = collect_issues()
    if issues:
        diagnostics = [issue_to_diagnostic(issue) for issue in issues]
        if args.json:
            json.dump({"errors": diagnostics_as_json(diagnostics)}, sys.stdout, ensure_ascii=False, indent=2)
            sys.stdout.write("\n")
        else:
            print("Cluster surface coverage failed:\n")
            print_diagnostics("Errors", diagnostics)
        return 1

    if args.json:
        json.dump({"errors": []}, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"Cluster surface coverage passed for {len(CLUSTER_SURFACES)} cluster(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

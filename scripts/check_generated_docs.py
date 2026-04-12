#!/usr/bin/env python3
"""Check that registered generated docs are present and current."""

from __future__ import annotations

import argparse
import importlib.util
import sys
import tempfile
from pathlib import Path
from types import ModuleType

try:
    from scripts.surface_registry import REPO_ROOT, generated_surface_groups
except ModuleNotFoundError:
    from surface_registry import REPO_ROOT, generated_surface_groups


def load_module(module_name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def repo_relpath(path: Path, repo_root: Path | None = None) -> str:
    effective_repo_root = repo_root or REPO_ROOT
    return path.relative_to(effective_repo_root).as_posix()


def collect_generated_doc_failures(
    repo_root: Path | None = None,
    surfaces: tuple[object, ...] | None = None,
) -> list[str]:
    effective_repo_root = repo_root or REPO_ROOT
    failures: list[str] = []
    cluster_surfaces = surfaces or generated_surface_groups()

    for cluster in cluster_surfaces:
        script_relpath = getattr(cluster, "script_relpath", None)
        label = getattr(cluster, "label", "<unknown>")
        if not isinstance(script_relpath, str):
            failures.append(f"{label}: missing script_relpath in surface registry")
            continue

        script_path = effective_repo_root / script_relpath
        if not script_path.exists():
            failures.append(f"{label}: missing generator script {script_relpath}")
            continue

        module_name = f"generated_doc_check_{script_path.stem}"
        try:
            module = load_module(module_name, script_path)
        except Exception as exc:  # pragma: no cover - defensive import failure path
            failures.append(f"{label}: could not import generator {script_relpath}: {exc}")
            continue

        if not hasattr(module, "OUTPUT_DIR") or not hasattr(module, "load_terms") or not hasattr(module, "write_outputs"):
            failures.append(
                f"{label}: generator must expose OUTPUT_DIR, load_terms(), and write_outputs()"
            )
            continue

        original_output_dir = Path(module.OUTPUT_DIR)

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_output_dir = Path(tmpdir)
            module.OUTPUT_DIR = temp_output_dir
            try:
                terms = module.load_terms()
                generated_paths = module.write_outputs(terms)
            except Exception as exc:
                failures.append(f"{label}: generator failed while rendering docs: {exc}")
                module.OUTPUT_DIR = original_output_dir
                continue
            finally:
                module.OUTPUT_DIR = original_output_dir

            if not isinstance(generated_paths, list):
                failures.append(f"{label}: write_outputs() must return a list of written paths")
                continue

            if not generated_paths:
                failures.append(f"{label}: generator returned no generated paths")
                continue

            for path_like in generated_paths:
                generated_path = Path(path_like)
                try:
                    relative_generated_path = generated_path.relative_to(temp_output_dir)
                except ValueError:
                    failures.append(
                        f"{label}: generated path `{generated_path}` was written outside the temporary output directory"
                    )
                    continue

                actual_path = original_output_dir / relative_generated_path
                if not actual_path.exists():
                    failures.append(
                        f"{label}: missing generated doc {repo_relpath(actual_path, effective_repo_root)}"
                    )
                    continue

                expected = generated_path.read_text(encoding="utf-8")
                current = actual_path.read_text(encoding="utf-8")
                if current != expected:
                    failures.append(
                        f"{label}: stale generated doc {repo_relpath(actual_path, effective_repo_root)}"
                    )

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()

    failures = collect_generated_doc_failures()
    if failures:
        print("Generated docs check failed:\n")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Generated docs check passed for {len(generated_surface_groups())} generator(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

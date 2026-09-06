"""Compile a generated Prove2Me platform tree in dependency order.

The pinned Lake project is supplied by the caller.  This keeps the release
gate honest: the generator never declares a tree compiled merely because its
files exist, and the script records every command, output, warning count, and
source hash in a receipt.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from percolation_workflow.upload_plan import compare_elaborated_types, load_jsonl


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _phase(path: str) -> int:
    if path.startswith("Definitions/"):
        return 0
    if path.startswith("Theorems/"):
        return 1
    if path.startswith("Solutions/"):
        return 2
    return 3


_IMPORT_LINE = re.compile(
    r"^[ \t]*import[ \t]+(?P<module>[A-Za-z_][A-Za-z0-9_.]*)[ \t]*(?:--.*)?$"
)
_PLATFORM_MODULE_PREFIXES = ("Definitions.", "Theorems.", "Solutions.")


def _module_name(relative: str) -> str:
    return relative[:-len(".lean")].replace("/", ".")


def _ordered_paths(paths: list[tuple[str, Path]]) -> list[tuple[str, Path]]:
    """Topologically order generated modules using their explicit imports.

    The old phase/name sort was insufficient: ``Thm_A`` can import
    ``Thm_B`` even when A sorts first, and an existing `.olean` could hide the
    mistake.  Only imports whose module is present in this generated tree are
    graph edges; external Mathlib/project imports remain Lake responsibilities.
    """
    by_module = {_module_name(relative): (relative, path) for relative, path in paths}
    if len(by_module) != len(paths):
        raise ValueError("tree manifest maps multiple files to one module")
    incoming = {module: set() for module in by_module}
    for module, (_, path) in by_module.items():
        for line in path.read_text(encoding="utf-8").splitlines():
            match = _IMPORT_LINE.match(line)
            imported = match.group("module") if match else None
            if (imported is not None
                    and imported.startswith(_PLATFORM_MODULE_PREFIXES)
                    and imported not in by_module):
                raise ValueError(
                    f"platform source imports a module absent from the tree manifest: {imported}")
            if imported in by_module:
                incoming[module].add(imported)
    result: list[tuple[str, Path]] = []
    while incoming:
        ready = [module for module, dependencies in incoming.items() if not dependencies]
        if not ready:
            raise ValueError("generated platform import graph contains a cycle")
        ready.sort(key=lambda module: (_phase(by_module[module][0]), by_module[module][0]))
        for module in ready:
            result.append(by_module[module])
            incoming.pop(module)
        for dependencies in incoming.values():
            dependencies.difference_update(ready)
    return result


def _text(value: str | bytes | None) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value or ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("tree_root", type=Path)
    parser.add_argument("--lake-project", type=Path, required=True,
                        help="pinned Lake project used only as the compiler environment")
    parser.add_argument("--timeout", type=float, default=900.0)
    parser.add_argument("--original-types", type=Path,
                        help="optional Lean JSONL type rows from the source project")
    parser.add_argument("--staged-types", type=Path,
                        help="optional Lean JSONL type rows from the generated tree")
    args = parser.parse_args()
    root = args.tree_root.resolve()
    lake_project = args.lake_project.resolve()
    manifest_path = root / "tree-manifest.json"
    if not manifest_path.is_file():
        parser.error(f"missing tree manifest: {manifest_path}")
    if not lake_project.is_dir():
        parser.error(f"missing Lake project: {lake_project}")
    if bool(args.original_types) != bool(args.staged_types):
        parser.error("--original-types and --staged-types must be supplied together")
    type_diff = None
    if args.original_types:
        try:
            type_diff = compare_elaborated_types(
                load_jsonl(args.original_types), load_jsonl(args.staged_types))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            parser.error(f"type diff could not be loaded: {exc}")
        if not type_diff["ok"]:
            parser.error("elaborated type comparator rejected the generated tree")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        files = manifest["files"]
        if not isinstance(files, list) or not files:
            raise ValueError("tree manifest files must be nonempty")
        paths = []
        for relative in files:
            if not isinstance(relative, str) or not relative.endswith(".lean"):
                raise ValueError("tree manifest contains a non-Lean file")
            path = (root / relative).resolve()
            if not path.is_file() or not path.is_relative_to(root):
                raise ValueError(f"tree manifest source is missing or outside root: {relative}")
            paths.append((relative.replace("\\", "/"), path))
        paths = _ordered_paths(paths)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        parser.error(str(exc))

    sorry_violations = []
    for relative, source in paths:
        contains_sorry = re.search(r"\bsorry\b", source.read_text(encoding="utf-8")) is not None
        if relative.startswith(("Definitions/", "Solutions/")) and contains_sorry:
            sorry_violations.append(relative)
        if relative.startswith("Theorems/") and not contains_sorry:
            sorry_violations.append(relative + " (stub has no sorry placeholder)")
    if sorry_violations:
        parser.error("platform sorry gate failed: " + ", ".join(sorry_violations))

    old_lean_path = os.environ.get("LEAN_PATH", "")
    env = os.environ.copy()
    env["LEAN_PATH"] = str(root) + (os.pathsep + old_lean_path if old_lean_path else "")
    records = []
    for relative, source in paths:
        output = source.with_suffix(".olean")
        command = ["lake", "env", "lean", "-R", str(root), "-o", str(output), str(source)]
        source_before = hashlib.sha256(source.read_bytes()).hexdigest()
        try:
            completed = subprocess.run(command, cwd=lake_project, env=env,
                                       capture_output=True, text=True,
                                       encoding="utf-8", errors="replace",
                                       timeout=args.timeout)
            stdout, stderr = completed.stdout, completed.stderr
            source_after = hashlib.sha256(source.read_bytes()).hexdigest()
            source_changed = source_before != source_after
            status = "passed" if completed.returncode == 0 and not source_changed else "failed"
            error = "source changed during compilation" if source_changed else None
        except subprocess.TimeoutExpired as exc:
            stdout = _text(exc.stdout)
            stderr = _text(exc.stderr) + "\nplatform-tree compile timed out"
            completed = None
            status = "failed"
            error = "timeout"
            source_after = hashlib.sha256(source.read_bytes()).hexdigest()
            source_changed = source_before != source_after
        except OSError as exc:
            stdout, stderr = "", str(exc)
            completed = None
            status = "failed"
            error = repr(exc)
            source_after = hashlib.sha256(source.read_bytes()).hexdigest()
            source_changed = source_before != source_after
        records.append({
            "path": relative,
            "status": status,
            "returncode": completed.returncode if completed is not None else None,
            "command": command,
            "source_sha256": source_before,
            "source_sha256_after": source_after,
            "source_changed_during_compile": source_changed,
            "stdout": stdout,
            "stderr": stderr,
            "warning_count": sum(1 for line in (stdout + "\n" + stderr).splitlines()
                                  if "warning:" in line),
            "error": error,
            "finished_at": _now(),
        })
        if status != "passed":
            break

    receipt = {
        "schema_version": 1,
        "algorithm": "prove2me_platform_compile/v1",
        "status": "passed" if len(records) == len(paths) and all(
            item["status"] == "passed" for item in records) else "failed",
        "type_diff": type_diff,
        "sorry_gate": "passed",
        "tree_manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        "lake_project": str(lake_project),
        "modules": records,
        "finished_at": _now(),
    }
    receipt_path = root / "compile-receipt.json"
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "modules": len(records),
                      "receipt": str(receipt_path)}, ensure_ascii=False))
    return 0 if receipt["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

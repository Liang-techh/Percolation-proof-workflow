"""Materialize a Prove2Me Definitions/Theorems/Solutions tree from a plan."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from percolation_workflow.upload_plan import (
    generate_definition_module, generate_solution_module, generate_theorem_stub,
    join_stage_facts, load_jsonl, rewrite_imports,
)


def _mapping(values: list[str], *, label: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"{label} must be NAME=VALUE")
        key, raw = value.split("=", 1)
        vals = [part for part in raw.split(",") if part]
        if not key or not vals:
            raise ValueError(f"{label} contains an empty mapping")
        result[key] = vals
    return result


def _import_mappings(values: list[str]) -> tuple[dict[str, list[str]], dict[str, dict[str, list[str]]]]:
    """Parse global ``IMPORTED=...`` and scoped ``CONTEXT::IMPORTED=...`` maps."""
    global_map: dict[str, list[str]] = {}
    scoped: dict[str, dict[str, list[str]]] = {}
    for value in values:
        if "=" not in value:
            raise ValueError("--import must be IMPORTED=VALUE or CONTEXT::IMPORTED=VALUE")
        left, raw = value.split("=", 1)
        vals = [part for part in raw.split(",") if part]
        if not left or not vals:
            raise ValueError("--import contains an empty mapping")
        if "::" in left:
            context, imported = left.split("::", 1)
            if not context or not imported:
                raise ValueError("--import scoped mapping is malformed")
            scoped.setdefault(context, {})[imported] = vals
        else:
            global_map[left] = vals
    return global_map, scoped


def _slug(name: str) -> str:
    return name.replace(".", "_")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("graph", type=Path)
    parser.add_argument("--sketch", action="append", required=True,
                        help="MODULE=STAGE2_JSONL; repeat for every participating module")
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--import", dest="imports", action="append", default=[],
                        help="IMPORTED=PLATFORM_IMPORT[,PLATFORM_IMPORT] or CONTEXT::IMPORTED=...")
    parser.add_argument("--extra-import", action="append", default=[],
                        help="SOURCE_MODULE=IMPORT[,IMPORT]")
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
        graph = load_jsonl(args.graph)
        sketch_map = _mapping(args.sketch, label="--sketch")
        if any(len(paths) != 1 for paths in sketch_map.values()):
            raise ValueError("each --sketch mapping must name exactly one JSONL file")
        imports, scoped_imports = _import_mappings(args.imports)
        extras = _mapping(args.extra_import, label="--extra-import")
        sketch = {module: load_jsonl(paths[0]) for module, paths in sketch_map.items()}
        all_graph = [row for row in graph if row.get("startLine", 0) != 0]
        joined = join_stage_facts(all_graph, sketch)
        if not isinstance(plan, dict) or not isinstance(plan.get("nodes"), list):
            raise ValueError("plan has no nodes list")
        selected = {row["name"]: row for row in plan["nodes"]}
        output_root = args.output_root.resolve()
        output_root.mkdir(parents=True, exist_ok=True)
        written = []

        modules = sorted({row["module"] for row in selected.values()
                          if row.get("destination") == "definition_material"})
        for module in modules:
            source = (args.source_root / (module.replace(".", "/") + ".lean")).resolve()
            if not source.is_file() or not source.is_relative_to(args.source_root.resolve()):
                raise ValueError(f"source module is missing: {module}")
            module_facts = {name: fact for name, fact in joined.items()
                            if fact["module"] == module}
            keep = [name for name, row in selected.items()
                    if row.get("module") == module and row.get("destination") == "definition_material"]
            text = generate_definition_module(source.read_text(encoding="utf-8"), module_facts, keep)
            replacements = dict(imports)
            replacements.update(scoped_imports.get(module, {}))
            text = rewrite_imports(text, replacements, extra_imports=extras.get(module, []))
            destination = output_root / "Definitions" / f"Def_{_slug(module)}.lean"
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(text, encoding="utf-8")
            written.append(destination)

        theorem_rows = [row for row in selected.values() if row.get("destination") == "theorem_node"]
        for row in sorted(theorem_rows, key=lambda item: item["name"]):
            name = row["name"]
            module = row["module"]
            source = (args.source_root / (module.replace(".", "/") + ".lean")).resolve()
            module_facts = {decl_name: fact for decl_name, fact in joined.items()
                            if fact["module"] == module}
            text = generate_theorem_stub(source.read_text(encoding="utf-8"), module_facts, name)
            replacements = dict(imports)
            replacements.update(scoped_imports.get(module, {}))
            text = rewrite_imports(text, replacements, extra_imports=extras.get(module, []))
            destination = output_root / "Theorems" / f"Thm_{_slug(name)}.lean"
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(text, encoding="utf-8")
            written.append(destination)

            inline = [inline_name for inline_name, inline_row in selected.items()
                      if inline_row.get("module") == module and
                      inline_row.get("destination") == "inline_helper"]
            solution = generate_solution_module(
                source.read_text(encoding="utf-8"), module_facts, name, inline,
                namespace_prefix=name.rsplit(".", 1)[0] if "." in name else None)
            solution = rewrite_imports(solution, replacements, extra_imports=extras.get(module, []))
            solution_path = output_root / "Solutions" / f"Sol_{_slug(name)}.lean"
            solution_path.parent.mkdir(parents=True, exist_ok=True)
            solution_path.write_text(solution, encoding="utf-8")
            written.append(solution_path)

        manifest = {
            "schema_version": 1,
            "algorithm": "prove2me_platform_tree/v1",
            "plan_sha256": hashlib.sha256(args.plan.read_bytes()).hexdigest(),
            "files": [str(path.relative_to(output_root).as_posix()) for path in written],
        }
        (output_root / "tree-manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"output_root": str(output_root), "files": len(written)},
                         ensure_ascii=False))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

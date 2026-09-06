"""Emit a deterministic Prove2Me Stage-1/Stage-2 upload plan."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from percolation_workflow.upload_plan import build_upload_plan, load_jsonl, ordered_upload_actions


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", help="Stage-1 declaration graph JSONL")
    parser.add_argument("--sketch", action="append", required=True,
                        help="Stage-2 sketch JSONL; repeat once per module")
    parser.add_argument("--module", action="append", required=True,
                        help="MODULE=SKETCH_JSONL mapping, matching --sketch files")
    parser.add_argument("--root", action="append", required=True)
    parser.add_argument("--force-node", action="append", default=[])
    parser.add_argument("--source-paper-name", action="append", default=[])
    parser.add_argument("--source-root", help="source project root for module path/digest evidence")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    mappings = dict(item.split("=", 1) for item in args.module)
    missing = [path for path in args.sketch if path not in mappings.values()]
    if missing:
        parser.error("every --sketch path must have a --module mapping")
    sketch = {module: load_jsonl(path) for module, path in mappings.items()}
    plan = build_upload_plan(load_jsonl(args.graph), sketch, args.root,
                             force_nodes=args.force_node,
                             source_paper_names=args.source_paper_name,
                             source_root=args.source_root)
    plan['ordered_actions'] = ordered_upload_actions(plan)
    Path(args.output).write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(Path(args.output).resolve()), "nodes": len(plan["nodes"]),
                      "reachable": len(plan["reachable"]),
                      "spanless_dropped": len(plan["spanless_dropped"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

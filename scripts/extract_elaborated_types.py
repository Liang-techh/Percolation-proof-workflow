"""Extract elaborated declaration types from a pinned Lake project."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile


_LEAN_PROBE = r'''import Lean
import Lean.Util.CollectAxioms

open Lean in
run_meta do
  let wanted : List String := __WANTED__
  let env ← getEnv
  let mut found : List String := []
  for (name, ci) in env.constants.toList do
    if wanted.contains name.toString then
      let typ ← withOptions (fun opts => opts.setBool `pp.all true) do
        Lean.Meta.ppExpr ci.type
      let axioms ← collectAxioms name
      let row := Json.mkObj [
        ("name", toJson name.toString),
        ("type", toJson typ.pretty),
        ("levelParams", toJson (ci.levelParams.map Name.toString)),
        ("axioms", toJson (axioms.map Name.toString))]
      IO.println ("PERCO_TYPE " ++ row.compress)
      found := name.toString :: found
  let missing := wanted.filter (fun name => !found.contains name)
  if !missing.isEmpty then
    IO.println ("PERCO_MISSING " ++ (Json.arr (missing.toArray.map Json.str)).compress)
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lake-project", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, action="append", required=True)
    parser.add_argument("--import", dest="imports", action="append", required=True)
    parser.add_argument("--name", dest="names", action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=900.0)
    args = parser.parse_args()
    if any(not value or any(ch.isspace() for ch in value) for value in args.imports + args.names):
        parser.error("imports and names must be single Lean identifiers")
    lake_project = args.lake_project.resolve()
    roots = [path.resolve() for path in args.source_root]
    if not lake_project.is_dir() or any(not root.is_dir() for root in roots):
        parser.error("lake project and source roots must be directories")
    wanted = json.dumps(args.names, ensure_ascii=False)
    content = "\n".join(f"import {module}" for module in args.imports)
    content += "\n" + _LEAN_PROBE.replace("__WANTED__", wanted)
    with tempfile.TemporaryDirectory(prefix="percolation-type-probe-") as directory:
        probe = Path(directory) / "TypeProbe.lean"
        probe.write_text(content, encoding="utf-8", newline="\n")
        env = os.environ.copy()
        old_lean_path = env.get("LEAN_PATH", "")
        env["LEAN_PATH"] = os.pathsep.join(str(root) for root in roots) + (
            os.pathsep + old_lean_path if old_lean_path else "")
        command = ["lake", "env", "lean"]
        for root in roots:
            command.extend(["-R", str(root)])
        command.append(str(probe))
        try:
            completed = subprocess.run(command, cwd=lake_project, env=env,
                                       capture_output=True, text=True,
                                       encoding="utf-8", errors="replace",
                                       timeout=args.timeout)
        except (OSError, subprocess.TimeoutExpired) as exc:
            parser.error(f"type probe failed: {exc}")
        if completed.returncode != 0:
            parser.error("type probe failed:\n" + completed.stdout + completed.stderr)
        rows = []
        missing = None
        for line in completed.stdout.splitlines():
            if line.startswith("PERCO_TYPE "):
                rows.append(json.loads(line[len("PERCO_TYPE "):]))
            elif line.startswith("PERCO_MISSING "):
                missing = json.loads(line[len("PERCO_MISSING "):])
        if missing or {row.get("name") for row in rows} != set(args.names):
            parser.error(f"type probe did not produce exactly the requested names: {missing or args.names}")
    rows.sort(key=lambda row: row["name"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True)
                                       for row in rows) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output.resolve()), "names": len(rows)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

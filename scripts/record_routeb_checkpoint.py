"""Append reviewed Route-B research artifacts; never promote a theorem.

Call only after creating a recoverable state backup and running the adapter's
tracking migration. This attaches a proposed mathematical DAG without treating
it as a kernel-checked reduction or changing existing theorem dependencies.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.model import NodeStatus
from percolation_workflow.store import StateStore


def record(path: Path) -> dict:
    path = path.resolve(strict=True)
    if not path.is_relative_to(ROOT):
        raise ValueError("checkpoint artifacts must be inside the workflow workspace")
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--dag", type=Path, required=True)
    args = parser.parse_args()
    if not args.state.is_file():
        parser.error("existing state required")
    audit_ref, graph_ref = record(args.audit), record(args.dag)
    audit = json.loads(args.audit.read_text(encoding="utf-8"))
    graph = json.loads(args.dag.read_text(encoding="utf-8"))
    if audit["schema"] != "routeb-provenance-correction-audit-v1":
        raise ValueError("unexpected provenance receipt")
    if graph["status"] != "proposed_not_kernel_checked" or graph["formal_certificate_allowed"] is not False:
        raise ValueError("only an explicitly unverified proof proposal is accepted")
    ids = {n["id"] for n in graph["nodes"]}
    if len(ids) != len(graph["nodes"]) or graph["root"] not in ids:
        raise ValueError("malformed proposed graph")
    by_id = {n["id"]: n for n in graph["nodes"]}
    seen, visiting = set(), set()
    def visit(key):
        if key not in by_id or key in visiting:
            raise ValueError("dangling dependency or cycle in proposed graph")
        if key in seen:
            return
        visiting.add(key)
        for dep in by_id[key]["dependencies"]:
            visit(dep)
        visiting.remove(key)
        seen.add(key)
    for key in ids:
        visit(key)
    store = StateStore(args.state)
    state = store.load()
    if any(n.status == NodeStatus.IN_PROGRESS for n in state.nodes.values()):
        raise ValueError("refuse checkpoint metadata updates during active attempts")
    if state.project != "routeb-6dof-external":
        raise ValueError("wrong project")
    if any(e.get("kind") == "routeb_provenance_correction_checkpoint" and
           e.get("audit", {}).get("sha256") == audit_ref["sha256"] and
           e.get("proposed_dag", {}).get("sha256") == graph_ref["sha256"] for e in state.events):
        print("Checkpoint already recorded; no changes")
        return 0
    nodes = {n.name.split(".")[0]: n for n in state.nodes.values()}
    if Path(nodes["P0"].metadata["target_root"]).resolve() != Path(audit["target_root"]).resolve():
        raise ValueError("audit target differs from state target")
    nodes["P0"].metadata.setdefault("provenance_audits", []).append(audit_ref)
    nodes["M4"].metadata.setdefault("proposed_mathematical_dags", []).append(graph_ref)
    state.event("routeb_provenance_correction_checkpoint", audit=audit_ref,
                proposed_dag=graph_ref, mathematical_edges_checked=False,
                current_baseline_complete=audit["current_baseline_complete"],
                unresolved_issues=audit["issues"],
                retracted_claim="current checker-chain reproducibility based on relabelled historical source hashes",
                registry_promotions=0, formal_certificate_allowed=False)
    store.save(state)
    print(f"Checkpoint appended; revision={state.revision}; registry={len(state.registry)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

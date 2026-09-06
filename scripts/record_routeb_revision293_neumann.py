"""Record the strict weighted Neumann theorem and its repair history."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    if state.revision != 292 or state.registry:
        raise ValueError("revision-293 recorder requires revision 292 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v246.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v247.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision293.json"
    side = ROOT / "artifacts/task_FLT_neumann_20260908"
    required = [old, side / "WeightedInfinityNeumann.lean", side / "REPORT.md", side / "REPAIR_LOG.md", side / "receipt.json", side / "lean-toolchain"]
    if not all(path.is_file() for path in required):
        raise ValueError("missing weighted Neumann evidence")
    receipt = json.loads((side / "receipt.json").read_text(encoding="utf-8"))
    if receipt.get("compile", {}).get("exit_code") != 0 or receipt.get("formal_certificate_allowed") is not False:
        raise ValueError("Neumann leaf is not a strict non-admitting pass")
    record = {
        "kind": "routeb_weighted_infinity_neumann_leaf",
        "status": receipt["status"],
        "evidence_level": "current-pin-strict-kernel-verified-abstract-linear-algebra",
        "files": [ref(side / name) for name in ("WeightedInfinityNeumann.lean", "REPORT.md", "REPAIR_LOG.md", "receipt.json", "lean-toolchain")],
        "proved": receipt["proved"],
        "mathematical_output": "two-sided inverse C with ||C||_w <= ||B||_w/(1-q)",
        "repair_history_retained": True,
        "open_obligations": receipt["open"],
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45.neumann_inverse_bound",
        "status": "abstract_neumann_closed_concrete_residual_open",
        "reason": "Kernel-verified weighted Neumann theorem is available; concrete interval residual membership and physical source binding remain open.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v247", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision293_neumann/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": str(side),
        "evidence_sha256": sha(side / "receipt.json"),
        "strict_compile": True,
        "abstract_inverse_theorem": True,
        "concrete_binding_open": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision293_neumann_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        weighted_neumann_theorem=True,
        two_sided_inverse=True,
        same_weight_norm=True,
        concrete_residual_binding=False,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()

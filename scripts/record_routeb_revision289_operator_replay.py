"""Record the completed one-cell operator replay and norm-consistency repair."""
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
    if state.revision != 288 or state.registry:
        raise ValueError("revision-289 recorder requires revision 288 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v242.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v243.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision289.json"
    side = ROOT / "artifacts/task_FLT_operator_binding_20260908"
    required = [old, side / "FLTOperatorBindingContracts.lean", side / "REPORT.md", side / "VERIFICATION.md", side / "receipt.json"]
    if not all(path.is_file() for path in required):
        raise ValueError("missing completed operator replay evidence")
    receipt = json.loads((side / "receipt.json").read_text(encoding="utf-8"))
    if receipt.get("status") != "PASS_CONDITIONAL_OPERATOR_CONTRACT_SINGLE_CELL_SOURCE_BRIDGE_OPEN":
        raise ValueError("unexpected operator replay status")
    if receipt.get("verification", {}).get("exact_rational_replay") != "PASS":
        raise ValueError("exact rational replay did not pass")
    record = {
        "kind": "routeb_operator_single_cell_exact_replay",
        "status": receipt["status"],
        "evidence_level": "strict-lean-plus-exact-rational-single-cell",
        "files": [ref(side / name) for name in ("FLTOperatorBindingContracts.lean", "REPORT.md", "VERIFICATION.md", "receipt.json")],
        "cell": receipt["cell"],
        "weighted_contract": receipt["operator_contract"],
        "coercivity_contract": receipt["coercivity_contract"],
        "repaired_mismatch": "unweighted 67.398... diagnostic excluded; same weighted norm uses preconditioner bound 64",
        "open_obligations": receipt["fail_closed"],
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45.operator_binding_single_cell",
        "status": "exact_replay_closed_source_bridge_open",
        "reason": "One-cell rational replay validates the same-norm arithmetic only; source semantics, Neumann implementation, interval membership, and coverage remain open.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v243", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision289_operator_replay/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": str(side),
        "evidence_sha256": sha(side / "receipt.json"),
        "exact_rational_replay": True,
        "single_cell_only": True,
        "source_bridge_open": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision289_operator_replay_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        exact_rational_replay=True,
        weighted_norm_consistency_repaired=True,
        single_cell_only=True,
        source_interval_semantics=False,
        coverage_closed=False,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()

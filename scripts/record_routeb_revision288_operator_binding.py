"""Record the matrix-level operator binding contract as an open leaf."""
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
    if state.revision != 287 or state.registry:
        raise ValueError("revision-288 recorder requires revision 287 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v241.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v242.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision288.json"
    side = ROOT / "artifacts/task_FLT_operator_binding_20260908"
    required = [old, side / "FLTOperatorBindingContracts.lean", side / "REPORT.md", side / "receipt.json", side / "extract_numeric_evidence.jl"]
    if not all(path.is_file() for path in required):
        raise ValueError("missing operator binding evidence")
    receipt = json.loads((side / "receipt.json").read_text(encoding="utf-8"))
    if receipt.get("compile", {}).get("exit_code") != 0 or receipt.get("registry_promoted") is not False:
        raise ValueError("operator contract is not a strict non-admitting pass")
    record = {
        "kind": "routeb_operator_level_krawczyk_schur_binding_leaf",
        "status": receipt["status"],
        "evidence_level": "current-pin-strict-compile-matrix-contract",
        "files": [ref(side / name) for name in ("FLTOperatorBindingContracts.lean", "REPORT.md", "receipt.json", "extract_numeric_evidence.jl")],
        "proved": receipt["proved"],
        "open_obligations": receipt["open"],
        "residual_orientation": "I - X * MNN",
        "norm_boundary": "weighted infinity residual and preconditioner bounds are separate contracts",
        "numeric_extractor_run": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45.operator_binding",
        "status": "matrix_contract_closed_numeric_binding_open",
        "reason": "Lean proves the exact consumer contract, but no claim is made that the deployed Julia payload satisfies it.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v242", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision288_operator_binding/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": str(side),
        "evidence_sha256": sha(side / "receipt.json"),
        "strict_compile": True,
        "numeric_extractor_run": False,
        "physical_binding_open": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision288_operator_binding_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        weighted_infinity_contract=True,
        schur_coercivity_contract=True,
        concrete_numeric_binding=False,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()

"""Record the strict Schur/Krawczyk scalar witness without physical admission."""
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
    if state.revision != 283 or state.registry:
        raise ValueError("revision-284 recorder requires revision 283 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v237.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v238.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision284.json"
    side = ROOT / "artifacts/task_FLT_schur_witness_20260908"
    required = [old, side / "FLTSchurWitness.lean", side / "REPORT.md", side / "lean-toolchain", side / "lake-manifest.json"]
    if not all(path.is_file() for path in required):
        raise ValueError("missing Schur witness evidence")
    report = (side / "REPORT.md").read_text(encoding="utf-8")
    if "PASS_CURRENT_PIN_SCALAR_LEAF_NUMERIC_BINDING_OPEN" not in report:
        raise ValueError("Schur witness report is not a strict pass with open binding")
    source = (side / "FLTSchurWitness.lean").read_text(encoding="utf-8")
    if any(token in source for token in ("sorry", "admit", "axiom ", "unsafe", "native_decide")):
        raise ValueError("escape hatch found in Schur witness source")
    record = {
        "kind": "routeb_schur_krawczyk_scalar_witness_leaf",
        "status": "PASS_CURRENT_PIN_SCALAR_LEAF_NUMERIC_BINDING_OPEN",
        "evidence_level": "current-pin-strict-compile-scalar-interface",
        "files": [ref(side / name) for name in ("FLTSchurWitness.lean", "REPORT.md", "lean-toolchain", "lake-manifest.json")],
        "proved": ["mLower>0", "0<=kappa<1", "preconditionerNorm/(1-kappa) inverse bound", "missing witness rejects certification"],
        "open_obligations": ["concrete Schur enclosure binding", "norm-consistent kappa binding", "outward preconditioner norm binding"],
        "legacy_invnorm_removed": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45.schur_krawczyk",
        "status": "scalar_witness_closed_physical_binding_open",
        "reason": "Lean closes the scalar guard algebra and fail-closed option semantics; matrix/domain enclosure binding remains open.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v238", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision284_schur_witness/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": "FLTSchurWitness current-pin sidecar",
        "evidence_sha256": sha(side / "FLTSchurWitness.lean"),
        "strict_compile": True,
        "physical_binding_open": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision284_schur_witness_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        scalar_schur_guard=True,
        scalar_krawczyk_guard=True,
        physical_matrix_binding=False,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()

"""Record the abstract exact-real trig interval Lean leaf."""
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
    if state.revision != 297 or state.registry:
        raise ValueError("revision-298 recorder requires revision 297 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v251.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v252.json"
    side = Path(r"C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\artifacts\task_FLT_trig_lean_leaf_20260908")
    required = [old, side / "FLT_TrigIntervalLeaf.lean", side / "FLT_TrigIntervalLeaf.olean", side / "RECEIPT.md", side / "REPORT.md", side / "AxiomAudit.lean"]
    if not all(path.is_file() for path in required):
        raise ValueError("missing Lean trig leaf evidence")
    source_sha = "4c95afe62390022c3e70c7e5c1289c17360fc947e4bc64d410569944cfa01b4f"
    olean_sha = "f776d62c5e8bbe6db0f48d7d2e604eaedf55a78cc99e6b884c538aa8a37e3eda"
    if sha(side / "FLT_TrigIntervalLeaf.lean") != source_sha or sha(side / "FLT_TrigIntervalLeaf.olean") != olean_sha:
        raise ValueError("Lean trig leaf hash mismatch")
    receipt_text = (side / "RECEIPT.md").read_text(encoding="utf-8")
    if "Result: exit code `0`" not in receipt_text or "FORBIDDEN_DECLARATION_SCAN_OK" not in receipt_text:
        raise ValueError("strict Lean receipt markers missing")
    record = {
        "kind": "routeb_abstract_trig_interval_lean_leaf",
        "status": "LEAN_VERIFIED_ABSTRACT_EXACT_REAL_TRIG_BRIDGE_SOURCE_BINDING_OPEN",
        "evidence_level": "strict-lean-compile-plus-axiom-audit-plus-placeholder-scan",
        "files": [ref(side / name) for name in ("FLT_TrigIntervalLeaf.lean", "FLT_TrigIntervalLeaf.olean", "RECEIPT.md", "REPORT.md", "AxiomAudit.lean")],
        "lean_toolchain": "leanprover/lean4:v4.33.0",
        "mathlib_revision": "db584cd6d46c92f209a44c0f1c829460d327499d",
        "source_sha256": source_sha,
        "olean_sha256": olean_sha,
        "strict_compile": True,
        "custom_axioms": False,
        "concrete_julia_binding": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45.trig_rounding",
        "status": "abstract_exact_real_leaf_verified",
        "reason": "Mathlib proves endpoint monotonicity and center-radius composition; concrete Julia/MPFR endpoint inequalities and source binding remain open.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v252", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision298.json"
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision298_trig_lean_leaf/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": str(side),
        "evidence_sha256": sha(side / "RECEIPT.md"),
        "strict_compile": True,
        "abstract_only": True,
        "concrete_julia_binding": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision298_trig_lean_leaf_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        strict_compile=True,
        abstract_only=True,
        concrete_julia_binding=False,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()

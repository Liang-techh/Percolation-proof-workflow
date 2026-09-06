"""Record the abstract exact finite-payload F3 q1-invariance leaf."""
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
    if state.revision != 324 or state.registry:
        raise ValueError("revision-325 recorder requires revision 324 and empty registry")
    side = ROOT / "artifacts/task_routeb_f3_q1_invariance_current"
    result, checker, source, log, witness = (side / n for n in
        ("CHECK_RESULT.json", "check_exact.py", "FourierQ1Invariance.lean", "compile_strict.log", "support_witness.json"))
    report = ROOT / "artifacts/task_routeb_revision325_f3_q1_invariance/REPORT.md"
    if not all(p.is_file() for p in (result, checker, source, log, witness, report)):
        raise ValueError("missing F3 q1-invariance evidence")
    check = json.loads(result.read_text(encoding="utf-8"))
    layer = check.get("layers", {})
    payload = layer.get("fourier_payload", {})
    if (check.get("status") != "PASS_MINIMAL_EXACT_PAYLOAD_WITNESS__TRUE_DH_BINDING_OPEN"
            or payload.get("status") != "PROVED_EXACT_FOR_PINNED_FINITE_PAYLOAD"
            or check.get("coverage") is not False
            or check.get("coverage_complete") is not False
            or check.get("registry_eligible") is not False
            or check.get("formal_certificate_allowed") is not False
            or check.get("physical_theorem") is not False
            or check.get("layers", {}).get("true_dh_source", {}).get("source_to_fourier_extensional_equality_proved") is not False
            or "RouteBF3Fourier.exponent_q1_invariant" not in log.read_text(encoding="utf-8")):
        raise ValueError("F3 checker did not pass with the required boundary")
    witness_data = json.loads(witness.read_text(encoding="utf-8"))
    if witness_data.get("nu1_nonzero_aggregate_rows") != 0 or witness_data.get("nu1_nonzero_body_rows") != 0:
        raise ValueError("F3 support witness contains nonzero q1 frequencies")

    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v278.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v279.json"
    graph = json.loads(old.read_text(encoding="utf-8"))
    record = {
        "kind": "routeb_f3_q1_invariance_exact_payload",
        "status": check["status"],
        "evidence_level": "strict-lean-finite-payload-support-witness",
        "files": [ref(report), ref(result), ref(checker), ref(source), ref(log), ref(witness)],
        "aggregate_rows": witness_data["aggregate_rows"],
        "body_trace_rows": witness_data["body_trace_rows"],
        "nu1_nonzero_aggregate_rows": 0,
        "nu1_nonzero_body_rows": 0,
        "strict_lean_support_theorem": True,
        "true_dh_source_binding": False,
        "coverage": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("workflow_hardening", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "GCN-F3-q1-invariance",
        "status": "finite_payload_closed_true_dh_q1_binding_open",
        "reason": "all finite Fourier frequencies have nu1=0 and Lean support theorem compiles; deployed DH yaw equivariance remains open",
        "evidence": ref(result),
    })
    graph.update(schema="routeb-proposed-proof-dag-v279", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checkpoint = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision325.json"
    if not checkpoint.exists():
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, checkpoint)
    graph_sha = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision325_f3_q1_invariance/v1",
        "graph_sha256": graph_sha, "roots": [], "selected_nodes": [],
        "evidence_sha256": sha(report), "checker_sha256": sha(checker),
        "result_sha256": sha(result), "source_sha256": sha(source),
        "witness_sha256": sha(witness), "strict_lean_support_theorem": True,
        "true_dh_source_binding": False, "coverage": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision325_f3_q1_invariance_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=graph_sha,
        aggregate_rows=witness_data["aggregate_rows"], body_trace_rows=witness_data["body_trace_rows"],
        nu1_nonzero_aggregate_rows=0, nu1_nonzero_body_rows=0,
        strict_lean_support_theorem=True, true_dh_source_binding=False,
        coverage=False, registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry),
                      "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()

"""Record the targeted B45-1.g q=0 mass bridge without registry promotion."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 55 and len(state.nodes) == 64 and not state.registry

    side = ROOT / "examples/routeb_mass_zero_bridge_lean"
    receipt = side / "FINAL_RECEIPT.md"
    source = side / "output/run-1MOYjiQB/MassZeroBridge.lean"
    olean = side / "output/run-1MOYjiQB/MassZeroBridge.olean"
    log = side / "output/run-1MOYjiQB/terminal.log"
    audit = side / "output/audit-20260905T221316Z/result.json"
    csv = side.parent / "routeb_source_binding_audit/snapshots/current_exact/routeB_fourier_mass_full_rational.csv"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v19.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v20.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision55.json"

    for path in (receipt, source, olean, log, audit, csv, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists()
    assert sha(csv) == "a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8"
    assert sha(source) == "8d5c2f19ef316b4016951f41414ad7a5f64132343455e423edf4a826904ece7d"
    assert sha(olean) == "b6a682f878eb7119a474061161b1d0a9db1c107184ad3f837f98a8453aac653a"
    assert sha(log) == "3893ce7825765e061e018ef6d026d91a73f1ce56d898c80ac808c6527523ba02"
    audit_result = json.loads(audit.read_text(encoding="utf-8"))
    assert audit_result["status"] == "EXACT_CSV_Q0_PAYLOAD_AUDIT_PASSED"
    assert audit_result["csv_rows"] == 610
    assert audit_result["frozen_payload_matches_csv"]
    assert audit_result["regularized_payload_matches_M0"]
    assert audit_result["lean_file_reading"] is False
    log_text = log.read_text(encoding="utf-8")
    for marker in (
        "MassZeroBridge_COMPILE_EXIT_CODE=0",
        "VERIFY_EXIT_CODE=0",
        "SNAPSHOT_HASHES_UNCHANGED=true",
        "propext",
        "Classical.choice",
        "Quot.sound",
    ):
        assert marker in log_text
    assert "sorry" not in source.read_text(encoding="utf-8").lower()
    assert "admit" not in source.read_text(encoding="utf-8").lower()

    state.event(
        "routeb_b45_1_mass_zero_bridge_lean",
        receipt=ref(receipt), source=ref(source), olean=ref(olean),
        terminal_log=ref(log), csv_audit=ref(audit), csv=ref(csv),
        csv_sha256=sha(csv), csv_rows=610, compile_exit=0, verify_exit=0,
        standard_axioms_only=True, no_sorry=True, no_admit=True,
        source_unbound=True, physical_DH_binding=False, float64_bridge=False,
        registry_promoted=False, formal_certificate_allowed=False,
        evidence_level="LEAN_KERNEL_VERIFIED_FINITE_PAYLOAD_PLUS_EXTERNAL_EXACT_CSV_PROVENANCE",
    )

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.update(
        schema="routeb-proposed-proof-dag-v20",
        supersedes="block45-obligations-v19.json",
        active_strategy="q0_mass_bridge_compiled_full_mass_binding_open",
    )
    nodes = {node["id"]: node for node in graph["nodes"]}
    nodes["B45-1_csv_q0_provenance"] = {
        "id": "B45-1_csv_q0_provenance",
        "status": "external_exact_audit_pass",
        "dependencies": [],
        "source": "../../examples/routeb_mass_zero_bridge_lean/verify.py",
        "statement": (
            "Hash-pinned 610-row Fourier mass CSV is re-aggregated at q=0 "
            "with exact rationals; sparse omitted entries and zero imaginary "
            "parts are checked externally."),
        "verification": {
            "result": "../../examples/routeb_mass_zero_bridge_lean/output/audit-20260905T221316Z/result.json",
            "csv_sha256": sha(csv), "csv_rows": 610,
            "explicit_matrix_pairs": 32, "omitted_pairs_are_zero": True,
            "all_imaginary_aggregates_zero": True,
            "lean_file_reading": False, "registry_eligible": False,
        },
    }
    nodes["B45-1_zero_point_M0_bridge"].update({
        "status": "compiled_candidate_comparator_pending",
        "dependencies": ["B45-1_csv_q0_provenance"],
        "source": "../../examples/routeb_mass_zero_bridge_lean/MassZeroBridge.lean",
        "statement": (
            "Kernel-check the frozen exact q=0 aggregate of all 610 Fourier "
            "mass rows plus (1/1000000) I equals the Lean literal M0; this "
            "is a finite payload bridge, not the q-dependent source identity."),
        "verification": {
            "receipt": str(receipt.resolve()), "run": "output/run-1MOYjiQB",
            "compile_exit": 0, "verify_exit": 0,
            "standard_axioms_only": True, "no_sorry": True, "no_admit": True,
            "source_sha256": sha(source), "olean_sha256": sha(olean),
            "csv_audit": str(audit.resolve()), "registry_promoted": False,
        },
        "kernel_payload_boundary": "frozen_exact_rational_36_entry_matrix",
    })
    for obligation in graph["source_binding_obligations"]:
        if obligation["id"] == "B45-1":
            obligation["subnodes"] = [
                "B45-1_mass_functional_identity",
                "B45-1_regularized_mass_adapter",
                "B45-1_regularizer_kernel_leaf",
                "B45-1_csv_q0_provenance",
                "B45-1_zero_point_M0_bridge",
                "B45-1_float64_enclosure_bridge",
            ]
            obligation["zero_point_M0_bridge"] = "compiled_candidate_comparator_pending"
            obligation["csv_q0_provenance"] = "external_exact_audit_pass"
    graph["next_frontier"] = [
        item for item in graph["next_frontier"]
        if item != "B45-1.g q=0 M0 bridge in Lean"
    ]
    graph["next_frontier"].insert(1, "B45-1.g q-dependent payload remains open after q=0 bridge")
    graph["nodes"] = list(nodes.values())

    def visit(key: str, stack: set[str]) -> None:
        assert key not in stack
        for dep in nodes[key].get("dependencies", []):
            assert dep in nodes, (key, dep)
            visit(dep, stack | {key})

    for key in nodes:
        visit(key, set())
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    m4 = next(node for node in state.nodes.values()
              if node.name.startswith("M4.") and node.name != "M4.correlated_momentum_closure")
    m4.metadata.setdefault("proposed_mathematical_dags", []).append(ref(graph_path))
    m4.metadata["next_mathematical_frontier"] = graph["next_frontier"]
    state.event(
        "routeb_mass_zero_bridge_checkpoint", proposed_dag=ref(graph_path),
        original_target_unchanged=True, actual_J_proved=False,
        formal_certificate_allowed=False, comparator_accepted=False,
        registry_promotions=0, broad_regression_run=False,
        source_binding_functional_identity_open=True,
    )
    if not backup.exists():
        import shutil
        shutil.copy2(store.path, backup)
    store.save(state)
    print(json.dumps({
        "revision": state.revision, "nodes": len(state.nodes),
        "graph_nodes": len(nodes), "registry": len(state.registry),
        "formal_certificate_allowed": False,
        "bridge": "compiled_candidate_comparator_pending",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()

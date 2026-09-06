"""Persist the bounded host-repair and corrupt-receipt workflow guards."""
import json
import shutil

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def main():
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 133 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v87.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v88.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision134.json"
    assert old_graph.is_file()
    assert not graph_path.exists() and not backup.exists()

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph["workflow_guards"] = {
        "host_repair_policy": {
            "max_rounds": 3,
            "policy": "bounded-host-repair-v1",
            "exhaustion_state": "repair_exhausted",
            "dispatch_blocked_after_exhaustion": True,
        },
        "compiler_receipt_policy": {
            "missing_receipt": "remain_checking_until_reclaim",
            "published_malformed_receipt": "compile_error_and_repairable",
            "invalid_receipt_exit_code": 124,
            "registry_promotion": "forbidden_without_comparator_and_lean_receipt",
        },
    }
    graph.update(schema="routeb-proposed-proof-dag-v88", supersedes="block45-obligations-v87.json")
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    shutil.copy2(store.path, backup)
    state.event(
        "routeb_repair_loop_hardening_recorded",
        proposed_dag=ref(graph_path),
        max_repair_rounds=3,
        repair_policy="bounded-host-repair-v1",
        corrupt_receipt_transition="compile_error",
        corrupt_receipt_exit_code=124,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(graph["nodes"]),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()

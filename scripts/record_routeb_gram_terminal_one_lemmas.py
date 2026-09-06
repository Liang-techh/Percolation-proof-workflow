"""Attach the single-block Gram surrogate and pinned terminal-interface lemma."""
import hashlib
import json
import shutil

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 144 and not state.registry
    gram = ROOT / "artifacts/routeb_agent_gram_one_block_20260906T080058Z"
    terminal = ROOT / "artifacts/routeb_agent_terminal_one_lemma_20260906T075912Z"
    gram_report, gram_manifest = gram / "AUDIT.md", gram / "manifest.json"
    gram_csv, gram_pivots = gram / "block4_corrected_gram.csv", gram / "block4_shifted_ldl_pivots.csv"
    terminal_source = terminal / "RouteBTerminalOneLemma.lean"
    terminal_receipt = terminal / "FINAL_RECEIPT.md"
    terminal_readme = terminal / "README.md"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v98.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v99.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision145.json"
    for path in (gram_report, gram_manifest, gram_csv, gram_pivots, terminal_source,
                 terminal_receipt, terminal_readme, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    gdata = json.loads(gram_manifest.read_text(encoding="utf-8"))
    assert gdata["block"] == 4
    assert gdata["original_exported_gram_identity_exact"] is False
    assert gdata["corrected_gram_identity_exact"] is True
    assert gdata["shifted_corrected_gram_exact_spd"] is True
    assert "not a source-level" in gdata["corrected_gram_semantics"]
    receipt_text = terminal_receipt.read_text(encoding="utf-8")
    assert "COMPILE_EXIT_CODE=0" in receipt_text
    assert "sorry" in receipt_text.lower() and "OPEN" in receipt_text

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    gram_node_id = "B45-P6_exact_gram_identity_obstruction"
    gram_node = nodes[gram_node_id]
    gram_node.setdefault("verification", {}).setdefault("single_block_audits", []).append({
        "report": ref(gram_report), "manifest": ref(gram_manifest),
        "corrected_gram": ref(gram_csv), "shifted_pivots": ref(gram_pivots),
        "report_sha256": sha(gram_report), "manifest_sha256": sha(gram_manifest),
        "corrected_gram_sha256": sha(gram_csv), "shifted_pivots_sha256": sha(gram_pivots),
        "block": 4, "original_identity_exact": False,
        "corrected_target_identity_exact": True, "shift_delta": "1/1000",
        "shifted_spd": True, "status": "EXPORTED_TARGET_SURROGATE_ONLY",
        "registry_eligible": False, "formal_certificate_allowed": False,
    })
    gram_node.setdefault("open_bridges", []).append(
        "obtain source-faithful exact export or prove a bounded Float64 rounding remainder for original PMI"
    )
    terminal_node_id = "B45-8_terminal_flowpipe_first_exit_interface"
    terminal_node = nodes[terminal_node_id]
    terminal_node.setdefault("verification", {}).setdefault("pinned_conditional_lemmas", []).append({
        "source": ref(terminal_source), "receipt": ref(terminal_receipt),
        "readme": ref(terminal_readme), "source_sha256": sha(terminal_source),
        "receipt_sha256": sha(terminal_receipt), "readme_sha256": sha(terminal_readme),
        "compile_exit": 0, "sorry_admit_axiom": False,
        "lemmas": ["first_exit_implication_of_interval_energy_gap",
                    "terminal_target_of_minimal_qpoly12_premise",
                    "terminal_qpoly12_of_exact_remainder_budget",
                    "b45_8_conditional_interface"],
        "status": "PINNED_CONDITIONAL_INTERFACE_ONLY",
        "true_dh_binding": False, "registry_eligible": False,
        "formal_certificate_allowed": False,
    })
    terminal_node.setdefault("open_bridges", []).append(
        "instantiate the exact remainder budget and first-exit premises from deployed true-DH flowpipe"
    )
    graph.update(schema="routeb-proposed-proof-dag-v99", supersedes="block45-obligations-v98.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dependency in candidate.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_gram_terminal_one_lemmas_recorded",
        gram_report=ref(gram_report), gram_manifest=ref(gram_manifest),
        gram_status="EXPORTED_TARGET_SURROGATE_ONLY", gram_original_identity_exact=False,
        terminal_source=ref(terminal_source), terminal_status="PINNED_CONDITIONAL_INTERFACE_ONLY",
        terminal_compile_exit=0, terminal_true_dh_binding=False,
        registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()

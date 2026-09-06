"""Persist the explicit kc/M_BD and numerical Gram obstruction audit."""
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
    assert state.revision == 126 and not state.registry
    base = ROOT / "artifacts/routeb_agent_kc_mismatch_20260906_011114"
    report = base / "AUDIT_REPORT.md"
    recompute = base / "INDEPENDENT_RECOMPUTE.csv"
    evidence = base / "EVIDENCE_SHA256.txt"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v80.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v81.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision127.json"
    for path in (report, recompute, evidence, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    report_text = report.read_text(encoding="utf-8")
    assert "rho_kc" in report_text and "M_BD" in report_text
    assert "4.69716887607774e-8" in report_text
    assert "formal_certificate_allowed" in report_text

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-5_kc_mismatch_and_mbd_obstruction"
    assert node_id not in nodes
    nodes[node_id] = {
        "id": node_id,
        "status": "source_audit_open",
        "dependencies": ["B45-5_fullstate_descriptor_terminal_interface"],
        "source": "../../artifacts/routeb_agent_kc_mismatch_20260906_011114/AUDIT_REPORT.md",
        "statement": (
            "Audit the exact PMI-versus-deployed-torque kc mismatch, the true "
            "remote M_BD a_D term, and the numerical Gram reconstruction residual."
        ),
        "verification": {
            "report": ref(report), "recompute": ref(recompute), "evidence": ref(evidence),
            "report_sha256": sha(report), "recompute_sha256": sha(recompute),
            "evidence_sha256": sha(evidence),
            "kc_residual": "(q5/100, q4/200)",
            "remote_term": "M_BD(q)a_D",
            "projection_countermodel": "a_D=lambda*e1 at q=0 is unbounded in lambda",
            "pmi_gram_reconstruction_error": "4.69716887607774e-8",
            "pmi_gram_min_eigenvalue": "1.8088679623979735e-10",
            "registry_eligible": False, "formal_certificate_allowed": False,
        },
        "closed_subclaims": [
            "kc mismatch is an explicit residual, not removable noise",
            "remote descriptor term is M_BD a_D, not (M-M0)_BD a_D",
            "current PMI projection omits an unbounded remote variable",
            "PMI Gram reconstruction residual is numerical certificate error, not physical residual",
        ],
        "open_bridges": [
            "bind actual descriptor acceleration a_D on a bounded full-state domain",
            "uniform M_BD a_D and total residual absorption",
            "resolve PMI torque model versus deployed torque law",
            "exact rational Gram/LDL with strict positive margin",
            "first-exit, flowpipe, and terminal transfer",
        ],
        "semantic_boundary": "negative source/model-consistency audit; no theorem or registry evidence",
    }
    graph["next_frontier"] = [
        "resolve kc mismatch by explicit source/model contract",
        "supply bounded descriptor a_D and M_BD enclosure",
        "replace numeric Gram residual with exact rational Gram/LDL proof",
        "close uniform residual absorption and terminal flowpipe",
    ] + [x for x in graph.get("next_frontier", []) if "kc mismatch" not in x and "Gram" not in x]
    graph.update(schema="routeb-proposed-proof-dag-v81", supersedes="block45-obligations-v80.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for node in nodes.values():
        for dep in node.get("dependencies", []):
            if dep not in ids:
                raise ValueError(f"dangling dependency: {dep}")

    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_kc_mismatch_obstruction_recorded",
        node_id=node_id, report=ref(report), recompute=ref(recompute), evidence=ref(evidence),
        kc_residual="(q5/100, q4/200)", remote_descriptor_term="M_BD a_D",
        pmi_gram_reconstruction_error="4.69716887607774e-8",
        registry_eligible=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()

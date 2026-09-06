"""Persist the exact-Gram identity obstruction audit."""
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
    assert state.revision == 129 and not state.registry
    base = ROOT / "artifacts/routeb_agent_exact_gram_20260906_012110"
    report = base / "AUDIT_REPORT.md"
    summary = base / "audit_summary.json"
    blocks = base / "block_summary.csv"
    witnesses = base / "identity_witnesses.csv"
    pivots = base / "min_ldl_pivots.csv"
    evidence = base / "EVIDENCE_SHA256.txt"
    runlog = base / "run.log"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v83.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v84.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision130.json"
    for path in (report, summary, blocks, witnesses, pivots, evidence, runlog, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    data = json.loads(summary.read_text(encoding="utf-8"))
    assert data["blocks"] == 20
    assert data["decimal_rationalization"]["all_exact_ldl_pivots_positive"] is True
    assert data["decimal_rationalization"]["all_exact_coefficient_identities"] is False
    assert len(data["decimal_rationalization"]["blocks_with_identity_mismatch"]) == 20
    assert data["binary64_rationalization"]["all_exact_coefficient_identities"] is False
    report_text = report.read_text(encoding="utf-8")
    assert "exact LDL" in report_text and "identity" in report_text

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-P6_exact_gram_identity_obstruction"
    assert node_id not in nodes
    nodes[node_id] = {
        "id": node_id,
        "status": "source_audit_open",
        "dependencies": ["B45-P3_global_coverage_interval_interface"],
        "source": "../../artifacts/routeb_agent_exact_gram_20260906_012110/AUDIT_REPORT.md",
        "statement": (
            "Audit whether the exported alpha=12 Float64 Gram matrices provide an "
            "exact rational SOS/PMI identity and strict PSD margin for all 20 blocks."
        ),
        "verification": {
            "report": ref(report), "summary": ref(summary), "blocks": ref(blocks),
            "identity_witnesses": ref(witnesses), "min_ldl_pivots": ref(pivots),
            "evidence": ref(evidence), "run_log": ref(runlog),
            "report_sha256": sha(report), "summary_sha256": sha(summary),
            "blocks_sha256": sha(blocks), "witnesses_sha256": sha(witnesses),
            "pivots_sha256": sha(pivots), "evidence_sha256": sha(evidence),
            "blocks": 20, "all_exact_ldl_pivots_positive": True,
            "all_exact_coefficient_identities": False,
            "global_min_exact_margin_lower_bound": "8.381926250113816e-18",
            "registry_eligible": False, "formal_certificate_allowed": False,
        },
        "closed_subclaims": [
            "all 20 exported Gram matrices admit positive exact LDL pivots",
            "a conservative positive rational PSD margin can be computed for the exported matrices",
            "all 20 exported matrices fail exact target-polynomial coefficient identity",
            "positive matrix definiteness is separated from SOS identity validity",
        ],
        "open_bridges": [
            "recover or generate a rational Gram with exact polynomial identity",
            "prove strict margin for the identity-valid Gram, not merely exported matrix",
            "connect exact Gram to true-DH residual/source semantics",
            "cellwise coverage, residual absorption, flowpipe, and terminal transfer",
        ],
        "semantic_boundary": "negative exact-SOS identity audit; exported PD is not a proof of target PMI",
    }
    graph["next_frontier"] = [
        "construct identity-valid rational Gram/LDL witnesses for all required blocks",
        "record exact coefficient equality and strict PSD margin in a pinned checker",
        "bind Gram polynomial to true-DH residual and global coverage",
    ] + [x for x in graph.get("next_frontier", []) if "Gram" not in x and "SOS" not in x]
    graph.update(schema="routeb-proposed-proof-dag-v84", supersedes="block45-obligations-v83.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for node in nodes.values():
        for dep in node.get("dependencies", []):
            if dep not in ids:
                raise ValueError(f"dangling dependency: {dep}")

    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_exact_gram_identity_obstruction_recorded",
        node_id=node_id, report=ref(report), summary=ref(summary),
        blocks=20, exact_ldl_pivots_positive=True,
        exact_coefficient_identities=False, registry_eligible=False,
        formal_certificate_allowed=False, proposed_dag=ref(graph_path),
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()

"""Record the conditional F4 arithmetic leaf and its exact counterexample."""
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
    if state.revision != 311 or state.registry:
        raise ValueError("revision-312 recorder requires revision 311 and empty registry")
    side = ROOT / "artifacts/task_routeb_terminal_arithmetic_current"
    report, checker, result = (side / name for name in ("REPORT.md", "check_exact.py", "CHECK_RESULT.json"))
    if not all(p.is_file() for p in (report, checker, result)):
        raise ValueError("missing revision-312 evidence")
    check = json.loads(result.read_text(encoding="utf-8"))
    exact = check.get("exact", {})
    checks = check.get("checks", {})
    if (check.get("status") != "PASS_CONDITIONAL_ARITHMETIC_ONLY"
            or check.get("normalization_id") != "routeb_f4_direct_LgD_exact_v1"
            or not checks.get("D_gate_lt_D_max") or not checks.get("strict_margin_positive")
            or checks.get("p_cap_implies_qpoly_12") is not False
            or exact.get("witness_p") != "5/1" or exact.get("witness_qpoly") != "25/2"):
        raise ValueError("terminal arithmetic checker did not pass")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v265.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v266.json"
    record = {
        "kind": "routeb_f4_terminal_exact_arithmetic",
        "status": "PASS_CONDITIONAL_F4_ARITHMETIC_F0_F3_OPEN",
        "evidence_level": "exact-rational-normalization-check",
        "files": [ref(report), ref(checker), ref(result)],
        "normalization_id": check["normalization_id"],
        "exact": exact,
        "checks": checks,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("workflow_hardening", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "M4.F4_direct_terminal_comparator",
        "status": "conditional_exact_arithmetic_closed",
        "reason": "fixed normalization has positive strict margin; exact witness rejects p-only terminal shortcut; F0-F3 remain premises.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v266", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checkpoint = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision312.json"
    if not checkpoint.exists():
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, checkpoint)
    graph_sha = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision312_terminal_arithmetic/v1",
        "graph_sha256": graph_sha, "roots": [], "selected_nodes": [],
        "evidence_sha256": sha(report), "checker_sha256": sha(checker),
        "result_sha256": sha(result), "normalization_id": check["normalization_id"],
        "conditional_arithmetic_only": True, "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision312_terminal_arithmetic_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=graph_sha,
        normalization_id=check["normalization_id"], strict_margin_positive=True,
        p_only_terminal_shortcut_rejected=True, F0_F3_open=True,
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry), "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()

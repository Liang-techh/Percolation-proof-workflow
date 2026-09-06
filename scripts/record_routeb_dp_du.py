"""Record DP-DU progress and preserve fail-closed proof boundaries."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ev(*names: str) -> dict[str, Path]:
    out = {}
    for n in names:
        p = ROOT / n
        assert p.is_file(), p
        out[str(n)] = p
    return out


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 205 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v159.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v160.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision206.json"
    assert old.is_file() and not new.exists()
    audits = [
        ("routeb_physical_schur_margin", "CONDITIONAL_MARGIN_FORMULA_PHYSICAL_OPEN", "e_mu=mu*bBD*bDB/(a*(a-mu)) and 1-rho_reg-e_mu are exact conditions; physical receipts absent", ev("artifacts/task_DP_physical_schur_margin_20260906/REPORT.md", "artifacts/task_DP_physical_schur_margin_20260906/ledger.json", "artifacts/task_DP_physical_schur_margin_20260906/check.py")),
        ("routeb_cell16_indexed_partition", "OPEN_SYMBOLIC_PARTITION_ONLY", "indexed 33^4 partition avoids enumeration but child rho/source/coverage receipts are absent", ev("artifacts/task_DQ_cell16_partition_ledger_20260906/REPORT.md", "artifacts/task_DQ_cell16_partition_ledger_20260906/ledger.json", "artifacts/task_DQ_cell16_partition_ledger_20260906/checker.py")),
        ("routeb_p3_branch_comparator", "STATEMENT_MISMATCH_FAIL_CLOSED", "explicit evaluator is not interchangeable with Julia/libm expression", ev("artifacts/task_DR_p3_branch_comparator_20260906/README.md", "artifacts/task_DR_p3_branch_comparator_20260906/contract.json", "artifacts/task_DR_p3_branch_comparator_20260906/check.py")),
        ("routeb_p4_runtime_parse_gate", "OPEN_RUNTIME_PARSE", "Julia is unavailable in PATH; static hook evidence does not certify parsing/runtime", ev("artifacts/task_DS_p4_runtime_parse_gate_20260906/RUNTIME_PARSE_GATE.md")),
        ("routeb_flowpipe_terminal_obligations", "SCHEMA_READY_CERTIFICATE_DATA_OPEN", "initial-step-continuation-terminal parent DAG is explicit without numeric receipt", ev("artifacts/task_DT_flowpipe_terminal_obligations_20260906/README.md", "artifacts/task_DT_flowpipe_terminal_obligations_20260906/receipt_schema.json")),
        ("routeb_repair_receipt_core_api", "PURE_FUNCTION_API_READY", "path/schema/hash/manual-review classification is exposed without admission or registry mutation", ev("artifacts/task_DU_repair_receipt_core_20260906/REPORT.md", "src/percolation_workflow/disjoint.py", "tests/test_disjoint.py")),
    ]
    graph = json.loads(old.read_text(encoding="utf-8"))
    for kind, status, reason, evidence in audits:
        graph.setdefault("bottleneck_audits", []).append({"kind": kind, "status": status, "evidence_level": "bounded_math_or_core_workflow_api", "semantic_boundary": reason, "registry_promoted": False, "formal_certificate_allowed": False, "files": {k: {"path": ref(v), "sha256": sha(v)} for k, v in evidence.items()}})
        graph.setdefault("open_frontier_updates", []).append({"node": kind, "status": status.lower(), "reason": reason})
    graph.update(schema="routeb-proposed-proof-dag-v160", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    for kind, _status, _reason, evidence in audits:
        first = next(iter(evidence.values()))
        state.graph_artifacts.append({"schema_version": 1, "algorithm": kind + "/v1", "graph_sha256": digest, "roots": [], "selected_nodes": [], "source": str(first), "evidence_sha256": sha(first), "registry_promoted": False, "formal_certificate_allowed": False})
    state.event("routeb_dp_du_recorded", proposed_dag=ref(new), proposed_dag_sha256=digest, audits=[x[0] for x in audits], registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()

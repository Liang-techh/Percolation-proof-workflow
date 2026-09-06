"""Record the actual Julia extraction and exact-rational replay rerun."""
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
    if state.revision != 291 or state.registry:
        raise ValueError("revision-292 recorder requires revision 291 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v245.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v246.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision292.json"
    side = ROOT / "artifacts/task_FLT_operator_binding_20260908"
    required = [old, side / "extraction.out", side / "exact_rational_replay_20260906.out", side / "check_exact_rational.py", side / "extract_numeric_evidence.jl", side / "receipt.json"]
    if not all(path.is_file() for path in required):
        raise ValueError("missing numeric rerun evidence")
    replay = json.loads((side / "exact_rational_replay_20260906.out").read_text(encoding="utf-8-sig"))
    if replay.get("status") != "PASS_EXACT_RATIONAL_SINGLE_CELL" or replay.get("formal_certificate_allowed") is not False:
        raise ValueError("numeric replay is not fail-closed pass")
    text = (side / "extraction.out").read_text(encoding="utf-8-sig")
    if "schema=routeb.operator_binding.numeric_evidence.v1" not in text or "cell=GCC_q1_1_over_64" not in text:
        raise ValueError("Julia extraction output is not the expected cell")
    record = {
        "kind": "routeb_operator_numeric_extraction_and_replay_rerun",
        "status": "PASS_EXACT_RATIONAL_SINGLE_CELL_SOURCE_SEMANTICS_OPEN",
        "evidence_level": "actual-julia-extraction-plus-fraction-replay",
        "files": [ref(side / name) for name in ("extraction.out", "exact_rational_replay_20260906.out", "check_exact_rational.py", "extract_numeric_evidence.jl", "receipt.json")],
        "cell": replay["cell"],
        "checks": replay["checks"],
        "claim_scope": replay["claim_scope"],
        "source_interval_semantics_formalized": False,
        "domain_coverage_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45.operator_numeric_replay",
        "status": "single_cell_replay_pass_source_semantics_open",
        "reason": "Julia extraction and exact Fraction replay are reproducible for one cell; they do not establish interval soundness or coverage.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v246", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision292_numeric_replay_rerun/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": str(side),
        "evidence_sha256": sha(side / "exact_rational_replay_20260906.out"),
        "julia_extraction": True,
        "exact_rational_replay": True,
        "single_cell_only": True,
        "source_semantics_open": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision292_numeric_replay_rerun_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        julia_extraction_exit_code=0,
        exact_rational_replay_exit_code=0,
        single_cell_only=True,
        source_interval_semantics=False,
        domain_coverage_complete=False,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()

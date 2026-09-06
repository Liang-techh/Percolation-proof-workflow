"""Persist source semantic equivalence as a non-admissive candidate."""
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
    assert state.revision == 245 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v199.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v200.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision246.json"
    sidecar = ROOT / "artifacts/task_GBF_source_semantic_equivalence_20260907"
    files = [sidecar / "equivalence.json", sidecar / "checker.py", sidecar / "REPORT.md"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    graph = json.loads(old.read_text(encoding="utf-8"))
    reason = (
        "Original and dense-Mq interval executable text is identical after removing "
        "only full-line comments, and dhport_lib bytes match; raw interval SHA and "
        "declared-version gates remain open, so this is a light-adaptation candidate only."
    )
    audit = {
        "kind": "routeb_source_semantic_equivalence_audit",
        "status": "SEMANTIC_EQUIVALENCE_CANDIDATE_RAW_GATE_OPEN",
        "evidence_level": "independent_sidecar_source_audit",
        "semantic_boundary": reason, "sidecar": str(sidecar.resolve()),
        "files": [ref(path) for path in files], "registry_promoted": False,
        "formal_certificate_allowed": False,
        "normalized_sha256": "bd0f6359ddf11065e7ed62017f85176852f11b683f91293eee626c076c912cf1",
        "raw_identity": False, "version_declared": False,
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "local-routeb-revision246-source-semantic-equivalence",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "semantic_equivalence_candidate_raw_gate_open", "reason": reason,
    })
    graph.update(schema="routeb-proposed-proof-dag-v200", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision246_source_semantic_equivalence/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecar:GBF-source-semantic-equivalence",
        "evidence_sha256": sha(sidecar / "equivalence.json"), "strict_compile": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision246_source_semantic_equivalence_recorded", proposed_dag=ref(new),
        proposed_dag_sha256=digest, audit={"kind": audit["kind"], "status": audit["status"]},
        registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()

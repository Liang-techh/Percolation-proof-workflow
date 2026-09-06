"""Record the JSON-key normalization repair in the DD-DI importer."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 203 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v157.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v158.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision204.json"
    script = ROOT / "scripts/record_routeb_dd_di.py"
    assert old.is_file() and not new.exists() and script.is_file()
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("repair_audits", []).append({"kind": "routeb_dd_di_json_key_normalization", "status": "REPAIRED_REPLAY_PASS", "error_class": "serialization_path_type", "before": "WindowsPath used as JSON object key", "after": "ev helper stringifies evidence keys", "registry_promoted": False, "formal_certificate_allowed": False, "files": {"script": {"path": ref(script), "sha256": sha(script)}}})
    graph.setdefault("open_frontier_updates", []).append({"node": "Workflow.routeb_dd_di_importer", "status": "repaired_replay_pass", "reason": "WindowsPath evidence keys normalized before JSON serialization"})
    graph.update(schema="routeb-proposed-proof-dag-v158", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({"schema_version": 1, "algorithm": "routeb_dd_di_json_key_normalization/v1", "graph_sha256": digest, "roots": [], "selected_nodes": [], "source": str(script), "evidence_sha256": sha(script), "repair_class": "serialization_path_type", "registry_promoted": False, "formal_certificate_allowed": False})
    state.event("routeb_dd_di_importer_repaired", proposed_dag=ref(new), proposed_dag_sha256=digest, script=ref(script), script_sha256=sha(script), replay="revision203_recorded", registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()

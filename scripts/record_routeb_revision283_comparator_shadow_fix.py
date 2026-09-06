"""Record the reproducible, read-only comparator shadow-manifest fix."""
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
    if state.revision != 282 or state.registry:
        raise ValueError("revision-283 recorder requires revision 282 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v236.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v237.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision283.json"
    comparator = ROOT / "artifacts/task_FLT_adapter_manifest_comparator_20260908/comparator.py"
    corrected = ROOT / "artifacts/task_FLT_manifest_repair_20260908/corrected_manifest.json"
    pass_receipt = ROOT / "artifacts/task_FLT_manifest_repair_20260908/recheck_corrected_v3.json"
    main_receipt = ROOT / "artifacts/task_FLT_manifest_repair_20260908/recheck_main_v3.json"
    report = ROOT / "artifacts/task_FLT_manifest_repair_20260908/REPORT.md"
    required = [old, comparator, corrected, pass_receipt, main_receipt, report]
    if not all(path.is_file() for path in required):
        raise ValueError("missing comparator repair evidence")
    pass_obj = json.loads(pass_receipt.read_text(encoding="utf-8"))
    main_obj = json.loads(main_receipt.read_text(encoding="utf-8"))
    if pass_obj.get("result") != "PASS" or pass_obj.get("failure_count") != 0:
        raise ValueError("shadow comparator did not pass reproducibly")
    if main_obj.get("result") != "FAIL_CLOSED_MANIFEST_BOUNDARY_MISMATCH":
        raise ValueError("main manifest lost its expected fail-closed boundary")

    record = {
        "kind": "flt_manifest_comparator_shadow_argument_fix",
        "status": "PASS_SHADOW_AND_FAIL_CLOSED_MAIN",
        "evidence_level": "reproducible-read-only-comparator",
        "comparator": ref(comparator),
        "corrected_manifest": ref(corrected),
        "shadow_receipt": ref(pass_receipt),
        "main_manifest_receipt": ref(main_receipt),
        "shadow_failure_count": pass_obj["failure_count"],
        "main_failure_names": main_obj["failure_names"],
        "repair": [
            "--manifest selects an explicit shadow manifest",
            "source_bindings are checked against pinned repository commit/blob/content SHA",
            "legacy default invocation still checks canonical manifest and retains its failures",
        ],
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("workflow_repairs", []).append(record)
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "FLT.current_pin_manifest_comparator",
        "status": "shadow_pass_main_fail_closed",
        "reason": "Comparator now has a reproducible cross-repository source-binding path while canonical manifest remains unmodified and non-admitting.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v237", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision283_comparator_shadow_fix/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": "read-only FLT manifest comparator",
        "evidence_sha256": sha(pass_receipt),
        "shadow_pass": True,
        "canonical_fail_closed": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision283_comparator_shadow_fix_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        comparator_supports_shadow_manifest=True,
        source_bindings_rechecked=True,
        canonical_manifest_unchanged=True,
        canonical_fail_closed=True,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()

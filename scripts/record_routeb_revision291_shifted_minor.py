"""Record the repaired shifted-minor coercivity leaf."""
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
    if state.revision != 290 or state.registry:
        raise ValueError("revision-291 recorder requires revision 290 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v244.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v245.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision291.json"
    side = ROOT / "artifacts/task_FLT_shifted_minor_20260908"
    required = [old, side / "ShiftedMinor.lean", side / "REPORT.md", side / "receipt.json", side / "lean-toolchain", side / "lakefile.toml"]
    if not all(path.is_file() for path in required):
        raise ValueError("missing shifted-minor evidence")
    receipt = json.loads((side / "receipt.json").read_text(encoding="utf-8"))
    if receipt.get("compile", {}).get("exit_code") != 0 or receipt.get("formal_certificate_allowed") is not False:
        raise ValueError("shifted-minor leaf is not a strict non-admitting pass")
    record = {
        "kind": "routeb_shifted_principal_minor_coercivity_leaf",
        "status": receipt["status"],
        "evidence_level": "current-pin-strict-compile-exact-rational-interface",
        "files": [ref(side / name) for name in ("ShiftedMinor.lean", "REPORT.md", "receipt.json", "lean-toolchain", "lakefile.toml")],
        "proved": receipt["proved"],
        "rational_certificate": receipt["rational_certificate"],
        "open_obligations": receipt["open"],
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45.shifted_principal_minor",
        "status": "algebraic_coercivity_closed_physical_membership_open",
        "reason": "The 2x2 shifted-minor implication and rational certificate are kernel-checked; physical Schur interval membership remains open.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v245", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision291_shifted_minor/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": str(side),
        "evidence_sha256": sha(side / "receipt.json"),
        "strict_compile": True,
        "physical_membership_open": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision291_shifted_minor_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        shifted_minor_theorem=True,
        exact_rational_certificate=True,
        physical_schur_membership=False,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()

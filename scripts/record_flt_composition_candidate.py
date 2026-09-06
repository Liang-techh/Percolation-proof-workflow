"""Record the isolated FLT spectral/pairing composition as an open candidate."""
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
    assert state.revision == 217 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v171.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v172.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision218.json"
    sidecar = ROOT / "artifacts/task_FP_flt_spectral_pairing_composition_20260907"
    files = [
        sidecar / "FLTComposition.lean",
        sidecar / "COMPILE_LOG.txt",
        sidecar / "AXIOMS.txt",
        sidecar / "FORBIDDEN_TOKEN_SCAN.txt",
        sidecar / "PROVENANCE.md",
        sidecar / "REPORT.md",
    ]
    assert old.is_file() and not new.exists() and all(p.is_file() for p in files)

    source_commit = "aa2d8b34692b16c70f699536de0d8e75b9a3e9ef"
    mathlib_pin = "0df444a360eaa60ab8c11dca51a86af692955474"
    evidence = {
        "kind": "anthropic_flt_spectral_pairing_composition",
        "status": "CURRENT_PIN_STRICT_COMPILE_PASS_CANDIDATE_ONLY",
        "evidence_level": "isolated_lean_kernel_compile",
        "semantic_boundary": (
            "The sidecar composes generic spectral and pairing transport interfaces; "
            "it does not establish physical DH, PDE, trajectory, numerical, or "
            "registry claims."
        ),
        "source_repository": "https://github.com/anthropics/fermats-last-theorem",
        "source_commit": source_commit,
        "mathlib_pin": mathlib_pin,
        "strict_compile": True,
        "forbidden_token_scan": True,
        "axioms": ["propext", "Classical.choice", "Quot.sound"],
        "files": [ref(p) for p in files],
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("external_intakes", []).append(
        {
            "kind": evidence["kind"],
            "source": evidence["source_repository"],
            "commit": source_commit,
            "mathlib_pin": mathlib_pin,
            "sidecar": str(sidecar.resolve()),
            "files": evidence["files"],
            "strict_compile": True,
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        }
    )
    graph.setdefault("bottleneck_audits", []).append(evidence)
    graph.setdefault("open_frontier_updates", []).append(
        {"node": evidence["kind"], "status": "adapter_candidate_open", "reason": evidence["semantic_boundary"]}
    )
    graph.update(schema="routeb-proposed-proof-dag-v172", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)

    digest = sha(new)
    state.graph_artifacts.append(
        {
            "schema_version": 1,
            "algorithm": "anthropic_flt_spectral_pairing_composition/v1",
            "graph_sha256": digest,
            "roots": [],
            "selected_nodes": [],
            "source": str(sidecar),
            "evidence_sha256": sha(files[0]),
            "source_commit": source_commit,
            "mathlib_pin": mathlib_pin,
            "strict_compile": True,
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        }
    )
    state.event(
        "anthropic_flt_spectral_pairing_composition_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        sidecar=str(sidecar.resolve()),
        source_commit=source_commit,
        mathlib_pin=mathlib_pin,
        strict_compile=True,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()

"""Record the successful FLT spectral adapter current-pin reproof."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ev(*names: str) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for name in names:
        path = ROOT / name
        assert path.is_file(), path
        result[name] = path
    return result


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 214 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v168.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v169.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision215.json"
    assert old.is_file() and not new.exists()
    evidence = ev(
        "artifacts/task_FLT_spectral_current_pin_reprove_20260906/SpectralCurrentPin.lean",
        "artifacts/task_FLT_spectral_current_pin_reprove_20260906/COMPILE_LOG.txt",
        "artifacts/task_FLT_spectral_current_pin_reprove_20260906/PROVENANCE.md",
        "artifacts/task_FLT_spectral_current_pin_reprove_20260906/FORBIDDEN_TOKEN_SCAN.txt",
        "artifacts/task_FLT_spectral_current_pin_reprove_20260906/REPORT.md",
    )

    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("external_intakes", []).append(
        {
            "kind": "anthropic_fermats_spectral_current_pin_reproof",
            "source": "https://github.com/anthropics/fermats-last-theorem",
            "commit": "aa2d8b34692b16c70f699536de0d8e75b9a3e9ef",
            "source_path": "P2M/Sol/S_ContinuousLinearMap_map_eigenspace_orthogonal_le_of_commute.lean",
            "source_blob": "eba829798335659835b4741843c9cc626f0805ff",
            "source_sha256": "F7F958B0F0FC4CB337C989BF8118D6F0473F1B3107F02413609E9419FEA8EE22",
            "reproof_sha256": "17CFA354178901007B4A27CE56A5EECA643560F0A027B3CC917622D9E1A28056",
            "flt_mathlib_pin": "db584cd6d46c92f209a44c0f1c829460d327499d",
            "routeb_mathlib_pin": "0df444a360eaa60ab8c11dca51a86af692955474",
            "lean_toolchain": "leanprover/lean4:v4.33.1",
            "status": "PASS_CURRENT_PIN",
            "permitted_axioms": ["propext", "Classical.choice", "Quot.sound"],
            "registry_promoted": False,
            "formal_certificate_allowed": False,
            "evidence": {key: {"path": ref(path), "sha256": sha(path)} for key, path in evidence.items()},
        }
    )
    audit = {
        "kind": "anthropic_flt_spectral_adapter_current_pin",
        "status": "REUSE_APPROVED_COMPILED_CANDIDATE",
        "evidence_level": "current_pin_lean_compile_and_axiom_audit",
        "semantic_boundary": "generic commuting continuous-linear spectral transport is compiled; no Route-B physical, coverage, dynamics or certificate claim",
        "source_commit": "aa2d8b34692b16c70f699536de0d8e75b9a3e9ef",
        "source_path": "P2M/Sol/S_ContinuousLinearMap_map_eigenspace_orthogonal_le_of_commute.lean",
        "registry_promoted": False,
        "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in evidence.items()},
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("open_frontier_updates", []).append(
        {"node": audit["kind"], "status": "reuse_approved_compiled_candidate", "reason": audit["semantic_boundary"]}
    )
    graph.update(schema="routeb-proposed-proof-dag-v169", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)

    digest = sha(new)
    state.graph_artifacts.append(
        {
            "schema_version": 1,
            "algorithm": "anthropic_flt_spectral_current_pin_reproof/v1",
            "graph_sha256": digest,
            "roots": [],
            "selected_nodes": [],
            "source": str(next(iter(evidence.values()))),
            "evidence_sha256": sha(next(iter(evidence.values()))),
            "source_commit": "aa2d8b34692b16c70f699536de0d8e75b9a3e9ef",
            "routeb_mathlib_pin": "0df444a360eaa60ab8c11dca51a86af692955474",
            "permitted_axioms": ["propext", "Classical.choice", "Quot.sound"],
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        }
    )
    state.event(
        "anthropic_flt_spectral_current_pin_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        source_commit="aa2d8b34692b16c70f699536de0d8e75b9a3e9ef",
        source_sha256="F7F958B0F0FC4CB337C989BF8118D6F0473F1B3107F02413609E9419FEA8EE22",
        reproof_sha256="17CFA354178901007B4A27CE56A5EECA643560F0A027B3CC917622D9E1A28056",
        status="PASS_CURRENT_PIN",
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()

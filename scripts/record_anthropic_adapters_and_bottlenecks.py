"""Record isolated current-pin adapters and new Route-B bottleneck audits."""
import hashlib
import json
import shutil

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def entry(path, **extra):
    data = {"path": ref(path), "sha256": sha(path)}
    data.update(extra)
    return data


def main():
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 161 and not state.registry
    base = ROOT / "artifacts/anthropic_fermats_intake/adapters"
    spectral = base / "RouteBSpectralTransportAdapter.lean"
    quotient = base / "RouteBAnthropicTransportAdapter.lean"
    adapter_report = base / "ADAPTER_REPORT.md"
    p6 = ROOT / "artifacts/routeb_agent_p6_next_20260906T085329Z/REPORT.md"
    p6_checks = p6.parent / "exact_checks.json"
    schur = ROOT / "artifacts/routeb_agent_schur_next_20260906_025603/AUDIT.md"
    schur_numbers = schur.parent / "NUMBERS.json"
    for path in (spectral, quotient, adapter_report, p6, p6_checks, schur, schur_numbers):
        assert path.is_file(), path
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v115.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v116.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision162.json"
    assert old_graph.is_file()
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph["external_intakes"] = graph.get("external_intakes", [])
    graph["external_intakes"].append({
        "kind": "anthropic_current_pin_adapters",
        "source": "https://github.com/anthropics/fermats-last-theorem",
        "commit": "aa2d8b34692b16c70f699536de0d8e75b9a3e9ef",
        "adapter_report": entry(adapter_report, status="PASS_ISOLATED_CURRENT_PIN"),
        "spectral_adapter": entry(spectral, source_candidate="P2M/Sol/S_ContinuousLinearMap_map_eigenspace_orthogonal_le_of_commute.lean", status="PASS"),
        "quotient_adapter": entry(quotient, source_candidate="Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean", status="PASS_PARTIAL_QUOTIENT_PI_PENDING"),
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    graph["bottleneck_audits"] = graph.get("bottleneck_audits", [])
    graph["bottleneck_audits"].extend([
        {"kind": "P6_augmented_absorption", "report": entry(p6, evidence_level="E2_exact_rational_audit", status="CONDITIONAL_OPEN"), "checks": entry(p6_checks)},
        {"kind": "B45_schur_d_row_elimination", "report": entry(schur, evidence_level="E1_E2_q0_and_conditional_algebra", status="CONDITIONAL_OPEN"), "numbers": entry(schur_numbers)},
    ])
    graph.update(schema="routeb-proposed-proof-dag-v116", supersedes="block45-obligations-v115.json")
    ids = {node["id"] for node in graph["nodes"]}
    for node in graph["nodes"]:
        for dependency in node.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    if not backup.exists():
        shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    digest = sha(graph_path)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "anthropic_adapters_and_bottlenecks/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "local current-pin sidecars and Route-B independent audits",
        "commit": "aa2d8b34692b16c70f699536de0d8e75b9a3e9ef",
        "adapter_report_sha256": sha(adapter_report), "spectral_adapter_sha256": sha(spectral),
        "quotient_adapter_sha256": sha(quotient), "formal_certificate_allowed": False,
    })
    state.event(
        "anthropic_adapters_and_routeb_bottlenecks_recorded",
        adapter_report=ref(adapter_report), adapter_report_sha256=sha(adapter_report),
        spectral_adapter=ref(spectral), spectral_adapter_sha256=sha(spectral), spectral_status="PASS",
        quotient_adapter=ref(quotient), quotient_adapter_sha256=sha(quotient), quotient_status="PASS_PARTIAL_QUOTIENT_PI_PENDING",
        p6_report=ref(p6), p6_report_sha256=sha(p6), p6_status="CONDITIONAL_OPEN",
        schur_report=ref(schur), schur_report_sha256=sha(schur), schur_status="CONDITIONAL_OPEN",
        registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), proposed_dag_sha256=digest, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": graph_path.name, "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()

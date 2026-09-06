"""Persist the independent GCX same-representation contract audit."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore

def sha(p: Path) -> str: return hashlib.sha256(p.read_bytes()).hexdigest()

def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load(); assert state.revision == 271 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v225.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v226.json"
    side = ROOT / "artifacts/task_GCX_mbd_interval_same_representation_20260907"
    assert old.is_file() and not new.exists()
    receipt = json.loads((side / "receipt.json").read_text(encoding="utf-8"))
    graph = json.loads(old.read_text(encoding="utf-8"))
    audit = {"kind":"routeb_mbd_interval_same_representation", "status":receipt["status"],
             "sidecar":str(side.resolve()), "files":[ref(side/x) for x in ("REPORT.md","receipt.json","checker.py")],
             "julia_version":receipt["julia_version"], "targeted_execution_count":2,
             "gcu_gcv_interval_equal":True, "same_bigfloat_directed_representation":True,
             "float64_diagnostic_enters_containment":False, "coverage_complete":False,
             "registry_promoted":False, "formal_certificate_allowed":False,
             "semantic_boundary":"Tiny-anchor representation contract only; interval soundness and global coverage remain open."}
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({"kind":audit["kind"],"source":"independent-sidecar:GCX","sidecar":audit["sidecar"],"registry_promoted":False,"formal_certificate_allowed":False})
    graph.setdefault("open_frontier_updates", []).append({"node":audit["kind"],"status":"representation_contract_closed_global_soundness_open","reason":audit["semantic_boundary"]})
    graph.update(schema_version="routeb-proposed-proof-dag-v226", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    digest=sha(new)
    state.graph_artifacts.append({"schema_version":1,"algorithm":"routeb_revision272_mbd_same_representation/v1","graph_sha256":digest,"roots":[],"selected_nodes":[],"source":"independent-sidecar:GCX","evidence_sha256":sha(side/"receipt.json"),"strict_compile":False,"registry_promoted":False,"formal_certificate_allowed":False})
    state.event("routeb_revision272_mbd_same_representation_recorded", proposed_dag=ref(new), proposed_dag_sha256=digest, targeted_execution_count=2, same_bigfloat_directed_representation=True, float64_diagnostic_enters_containment=False, coverage_complete=False, registry_promoted=False, formal_certificate_allowed=False)
    store.save(state); print(json.dumps({"revision":state.revision,"graph":new.name,"registry":len(state.registry)}))
if __name__ == "__main__": main()

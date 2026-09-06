"""Record the refreshed Anthropic FLT reuse catalog without registry promotion."""
import hashlib
import json
import shutil

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 160 and not state.registry
    base = ROOT / "artifacts/anthropic_fermats_intake"
    catalog, provenance, plan = (base / name for name in ("catalog.json", "PROVENANCE.md", "REUSE_PLAN.md"))
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v114.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v115.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision161.json"
    for path in (catalog, provenance, plan, old_graph):
        assert path.is_file(), path
    data = json.loads(catalog.read_text(encoding="utf-8"))
    assert data["schema_version"] == "anthropic-fermats-intake-v1"
    assert data["commit"] == "aa2d8b34692b16c70f699536de0d8e75b9a3e9ef"
    assert data["lean_toolchain"] == "leanprover/lean4:v4.33.1"
    assert data["mathlib_revision"] == "db584cd6d46c92f209a44c0f1c829460d327499d"
    classes = {int(item["classification"]) for item in data["candidates"]}
    assert classes == {1, 2, 3}
    counts = {str(k): sum(int(c["classification"]) == k for c in data["candidates"]) for k in (1, 2, 3)}
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph["external_intakes"] = graph.get("external_intakes", [])
    graph["external_intakes"].append({
        "source": data["repository"], "commit": data["commit"],
        "catalog": ref(catalog), "catalog_sha256": sha(catalog),
        "provenance": ref(provenance), "provenance_sha256": sha(provenance),
        "reuse_plan": ref(plan), "reuse_plan_sha256": sha(plan),
        "candidate_count": len(data["candidates"]), "classification_counts": counts,
        "mathlib_revision": data["mathlib_revision"], "refresh": True,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.update(schema="routeb-proposed-proof-dag-v115", supersedes="block45-obligations-v114.json")
    ids = {node["id"] for node in graph["nodes"]}
    for node in graph["nodes"]:
        for dependency in node.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    if not backup.exists():
        shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    graph_digest = sha(graph_path)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "anthropic_fermats_intake/v1-refresh",
        "graph_sha256": graph_digest, "roots": [], "selected_nodes": [],
        "source": data["repository"], "commit": data["commit"],
        "catalog_sha256": sha(catalog), "candidate_count": len(data["candidates"]),
        "classification_counts": counts, "formal_certificate_allowed": False,
    })
    state.event(
        "anthropic_fermats_candidate_catalog_refreshed", source=data["repository"],
        commit=data["commit"], catalog=ref(catalog), catalog_sha256=sha(catalog),
        provenance=ref(provenance), provenance_sha256=sha(provenance),
        reuse_plan=ref(plan), reuse_plan_sha256=sha(plan), candidate_count=len(data["candidates"]),
        classification_counts=counts, mathlib_revision=data["mathlib_revision"],
        registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), proposed_dag_sha256=graph_digest,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "candidates": len(data["candidates"]),
           "classification_counts": counts, "registry": len(state.registry),
           "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()

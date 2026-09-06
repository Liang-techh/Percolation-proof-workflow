"""Record compiled Anthropic chain/pairing sidecars as non-registry evidence."""
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
    assert state.revision == 163 and not state.registry
    base = ROOT / "artifacts/anthropic_fermats_intake/adapters_chain_pairing_20260906T085350Z"
    receipt = base / "RECEIPT.md"
    chain = base / "LinearMapKernelQuotientAdapter.lean"
    pairing = base / "TransportGluePairingAdapter.lean"
    entry = base / "ChainPairingAdapters.lean"
    chain_olean = base / ".lake/build/lib/lean/LinearMapKernelQuotientAdapter.olean"
    pairing_olean = base / ".lake/build/lib/lean/TransportGluePairingAdapter.olean"
    entry_olean = base / ".lake/build/lib/lean/ChainPairingAdapters.olean"
    for path in (receipt, chain, pairing, entry, chain_olean, pairing_olean, entry_olean):
        assert path.is_file(), path
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v117.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v118.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision164.json"
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph["external_intakes"] = graph.get("external_intakes", [])
    graph["external_intakes"].append({
        "kind": "anthropic_chain_pairing_current_pin_sidecar",
        "source": "https://github.com/anthropics/fermats-last-theorem",
        "commit": "aa2d8b34692b16c70f699536de0d8e75b9a3e9ef",
        "receipt": {"path": ref(receipt), "sha256": sha(receipt), "status": "PASS"},
        "chain_adapter": {"path": ref(chain), "sha256": sha(chain), "status": "PASS"},
        "pairing_adapter": {"path": ref(pairing), "sha256": sha(pairing), "status": "PASS"},
        "entry_adapter": {"path": ref(entry), "sha256": sha(entry), "status": "PASS"},
        "olean_sha256": {"chain": sha(chain_olean), "pairing": sha(pairing_olean), "entry": sha(entry_olean)},
        "lean_toolchain": "leanprover/lean4:v4.33.1",
        "mathlib_commit": "0df444a360eaa60ab8c11dca51a86af692955474",
        "permitted_axioms": ["propext", "Classical.choice", "Quot.sound"],
        "forbidden_token_scan": "PASS",
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    graph.update(schema="routeb-proposed-proof-dag-v118", supersedes="block45-obligations-v117.json")
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
        "schema_version": 1, "algorithm": "anthropic_chain_pairing_adapters/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "isolated current-pin chain/pairing Lean sidecars",
        "commit": "aa2d8b34692b16c70f699536de0d8e75b9a3e9ef",
        "receipt_sha256": sha(receipt), "chain_sha256": sha(chain),
        "pairing_sha256": sha(pairing), "formal_certificate_allowed": False,
    })
    state.event(
        "anthropic_chain_pairing_adapters_recorded", receipt=ref(receipt), receipt_sha256=sha(receipt),
        chain_adapter=ref(chain), chain_adapter_sha256=sha(chain), pairing_adapter=ref(pairing),
        pairing_adapter_sha256=sha(pairing), entry_adapter=ref(entry), entry_adapter_sha256=sha(entry),
        chain_olean_sha256=sha(chain_olean), pairing_olean_sha256=sha(pairing_olean), entry_olean_sha256=sha(entry_olean),
        status="PASS_ISOLATED_CURRENT_PIN", permitted_axioms=["propext", "Classical.choice", "Quot.sound"],
        forbidden_token_scan="PASS", registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), proposed_dag_sha256=digest, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": graph_path.name, "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()

"""Persist the focused P3 mass-entry compile receipt as conditional evidence.

This records a reusable proof attempt in the research state without creating a
verified theorem or silently binding the Julia Float64 evaluator to the exact
DH model.  The durable JSON receipt is the authority for idempotence; ignored
compiler output remains referenced by its run id and hashes.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore  # noqa: E402


def file_ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main() -> None:
    side = ROOT / "examples" / "routeb_p3_mass_entry_bridge_lean"
    receipt_path = side / "compile_receipt.json"
    source = side / "MassEntryBridge.lean"
    verifier = side / "verify.sh"
    toolchain = side / "lean-toolchain"
    for path in (receipt_path, source, verifier, toolchain):
        if not path.is_file():
            raise FileNotFoundError(path)

    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if receipt.get("status") != "COMPILED_CANDIDATE":
        raise ValueError("receipt is not a compiled candidate")
    if receipt.get("compile_exit_code") != 0:
        raise ValueError("receipt compile exit code is not zero")
    if receipt.get("source_sha256") != file_ref(source)["sha256"]:
        raise ValueError("receipt source hash does not match current sidecar")
    if receipt.get("verifier_sha256") != file_ref(verifier)["sha256"]:
        raise ValueError("receipt verifier hash does not match current verifier")
    if receipt.get("toolchain_file_sha256") != file_ref(toolchain)["sha256"]:
        raise ValueError("receipt toolchain hash does not match current pin")
    if receipt.get("registry_promoted") or receipt.get("formal_certificate_allowed"):
        raise ValueError("conditional receipt cannot authorize admission")

    store = StateStore(ROOT / "artifacts" / "routeb_6dof" / "state.json")
    state = store.load()
    if state.project != "routeb-6dof-external":
        raise ValueError("wrong persistent project")
    receipt_ref = file_ref(receipt_path)
    event_kind = "routeb_p3_mass_entry_compile_recorded"
    if any(e.get("kind") == event_kind and e.get("receipt_sha256") == receipt_ref["sha256"]
           for e in state.events):
        print({"integrated": False, "state_revision": state.revision, "reason": "already_recorded"})
        return

    parent = next(node for node in state.nodes.values()
                  if node.name == "P3.strict_true_dh_bounds")
    graph_projection = {
        "schema_version": 1,
        "parent": parent.id,
        "child_statement": receipt["statement_ids"][0],
        "receipt_sha256": receipt_ref["sha256"],
    }
    graph_digest = hashlib.sha256(
        json.dumps(graph_projection, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    parent.metadata.setdefault("conditional_children", []).append({
        "statement_id": receipt["statement_ids"][0],
        "status": "compiled_candidate",
        "receipt": receipt_ref,
        "physical_source_binding": False,
        "global_coverage": False,
        "registry_promoted": False,
    })
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_p3_mass_entry_bridge/v1",
        "graph_sha256": graph_digest,
        "roots": [parent.id],
        "selected_nodes": [parent.id],
        "graph_projection": graph_projection,
        "receipt": receipt_ref,
        "source": file_ref(source),
        "verifier": file_ref(verifier),
        "toolchain": file_ref(toolchain),
        "status": "COMPILED_CANDIDATE",
        "physical_source_binding": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    })
    state.event(
        event_kind,
        node_id=parent.id,
        statement_ids=receipt["statement_ids"],
        receipt=str(receipt_path.resolve()),
        receipt_sha256=receipt_ref["sha256"],
        source_sha256=receipt["source_sha256"],
        olean_sha256=receipt["olean_sha256"],
        compile_log_sha256=receipt["compile_log_sha256"],
        compile_exit_code=0,
        status="COMPILED_CANDIDATE",
        physical_source_binding=False,
        global_coverage=False,
        registry_promoted=False,
        formal_certificate_allowed=False,
    )
    store.save(state)
    print({"integrated": True, "state_revision": state.revision,
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()

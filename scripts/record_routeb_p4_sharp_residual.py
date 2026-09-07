"""Persist the exact scalar P4 sharp-residual child as conditional evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore  # noqa: E402


def ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main() -> None:
    side = ROOT / "examples" / "routeb_p4_sharp_residual_lean"
    receipt_path = side / "compile_receipt.json"
    source = side / "SharpResidualBridge.lean"
    verifier = side / "verify.sh"
    toolchain = side / "lean-toolchain"
    for path in (receipt_path, source, verifier, toolchain):
        if not path.is_file():
            raise FileNotFoundError(path)
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    source_ref, verifier_ref, toolchain_ref = ref(source), ref(verifier), ref(toolchain)
    if receipt.get("status") != "COMPILED_CANDIDATE" or receipt.get("compile_exit_code") != 0:
        raise ValueError("P4 sharp receipt is not a successful compiled candidate")
    if receipt.get("source_sha256") != source_ref["sha256"]:
        raise ValueError("P4 sharp source hash mismatch")
    if receipt.get("verifier_sha256") != verifier_ref["sha256"]:
        raise ValueError("P4 sharp verifier hash mismatch")
    if receipt.get("toolchain_file_sha256") != toolchain_ref["sha256"]:
        raise ValueError("P4 sharp toolchain hash mismatch")
    if receipt.get("registry_promoted") or receipt.get("formal_certificate_allowed"):
        raise ValueError("P4 sharp conditional receipt cannot authorize admission")

    store = StateStore(ROOT / "artifacts" / "routeb_6dof" / "state.json")
    state = store.load()
    if state.project != "routeb-6dof-external":
        raise ValueError("wrong persistent project")
    node = next(n for n in state.nodes.values() if n.name == "P4.residual_schur_pmi")
    receipt_ref = ref(receipt_path)
    event_kind = "routeb_p4_sharp_residual_compile_recorded"
    if any(e.get("kind") == event_kind and e.get("receipt_sha256") == receipt_ref["sha256"]
           for e in state.events):
        print({"integrated": False, "state_revision": state.revision,
               "reason": "already_recorded"})
        return

    projection = {"schema_version": 1, "parent": node.id,
                  "child_statements": receipt["statement_ids"],
                  "receipt_sha256": receipt_ref["sha256"]}
    graph_digest = hashlib.sha256(
        json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    node.metadata.setdefault("conditional_children", []).append({
        "statement_ids": receipt["statement_ids"],
        "status": "compiled_candidate",
        "receipt": receipt_ref,
        "source_residual_units_bound": False,
        "physical_source_binding": False,
        "global_coverage": False,
        "registry_promoted": False,
    })
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_p4_sharp_residual/v1",
        "graph_sha256": graph_digest,
        "roots": [node.id],
        "selected_nodes": [node.id],
        "graph_projection": projection,
        "receipt": receipt_ref,
        "source": source_ref,
        "verifier": verifier_ref,
        "toolchain": toolchain_ref,
        "status": "COMPILED_CANDIDATE",
        "source_residual_units_bound": False,
        "physical_source_binding": False,
        "global_coverage": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    })
    state.event(
        event_kind,
        node_id=node.id,
        statement_ids=receipt["statement_ids"],
        receipt=str(receipt_path.resolve()),
        receipt_sha256=receipt_ref["sha256"],
        source_sha256=receipt["source_sha256"],
        verifier_sha256=receipt["verifier_sha256"],
        toolchain_file_sha256=receipt["toolchain_file_sha256"],
        olean_sha256=receipt["olean_sha256"],
        compile_log_sha256=receipt["compile_log_sha256"],
        compile_exit_code=0,
        status="COMPILED_CANDIDATE",
        source_residual_units_bound=False,
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

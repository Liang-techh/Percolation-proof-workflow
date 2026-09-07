"""Refresh the non-authoritative Anthropic FLT adapter overlay.

The overlay is intentionally not merged into authoritative ``ProofNode``
dependencies.  It is a hash-bound sidecar used only for provenance and an
opt-in scheduler tie-break after the authoritative frontier is computed.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "artifacts/routeb_6dof/state.json"
TEMPLATE = ROOT / "artifacts/task_FLT_adapter_frontier_integration_20260908/proposed_overlay.example.json"
OUT = ROOT / "artifacts/anthropic_fermats_intake/advisory_overlay.current.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    template = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    nodes = state.get("nodes", {})
    if not isinstance(nodes, dict) or not state.get("root_id") in nodes:
        raise ValueError("authoritative state has no valid root")

    overlay = dict(template)
    overlay["base_graph"] = {
        "path": "artifacts/routeb_6dof/state.json",
        "sha256": sha(STATE),
        "root_id": state["root_id"],
    }
    missing = [
        edge["from_node_id"] for edge in overlay.get("reuse_edges", [])
        if edge.get("from_node_id") not in nodes
    ]
    if missing:
        raise ValueError("overlay has stale authoritative node ids: " + ",".join(missing))
    if overlay.get("authority") != "non_authoritative":
        raise ValueError("overlay authority boundary changed")
    for adapter in overlay.get("adapters", []):
        if adapter.get("registry_eligible") is not False or adapter.get("formal_certificate_allowed") is not False:
            raise ValueError("overlay adapter crosses admission boundary")
    for edge in overlay.get("reuse_edges", []):
        if edge.get("edge_kind") != "advisory_reuse" or edge.get("closure_effect") is not False or edge.get("registry_effect") is not False:
            raise ValueError("overlay edge crosses closure/registry boundary")

    OUT.write_text(json.dumps(overlay, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {
        "schema_version": 1,
        "algorithm": "anthropic_advisory_overlay_refresh/v1",
        "overlay": str(OUT.relative_to(ROOT)).replace("\\", "/"),
        "overlay_sha256": sha(OUT),
        "base_state_revision": state.get("revision"),
        "base_state_sha256": sha(STATE),
        "adapter_count": len(overlay.get("adapters", [])),
        "reuse_edge_count": len(overlay.get("reuse_edges", [])),
        "authoritative_dependencies_modified": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    receipt_path = OUT.with_name("advisory_overlay.current.receipt.json")
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

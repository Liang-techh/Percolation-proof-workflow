"""Attach completed O0/O2 static reviews without admitting a theorem.

The GitHub/host agents return research reports, not coordinator receipts.  This
small intake layer records their hashes and mathematical blockers in the DAG
while keeping compilation, comparator, registry, and certificate admission
explicitly closed.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTE_B = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
TASKS = {
    "o0": {
        "directory": ROOT / "artifacts/task_routeb_o0_rounding_bridge_audit_20260907",
        "node": "P4.true_dh_regularizer_semantics_bridge",
        "status_keys": ("status",),
        "expected_status": "OPEN_MINIMAL_OUTWARD_INCLUSION_DESIGN",
        "source": ROUTE_B / "robot_final" / "dhport_lib.jl",
    },
    "o2": {
        "directory": ROOT / "artifacts/task_routeb_o2_evaluator_minimal_decomposition_20260907",
        "node": "P4.true_dh_float64_evaluator_enclosure",
        "status_keys": ("decision",),
        "expected_status": "OPEN_MINIMAL_DECOMPOSITION_COMPLETE",
        "source": ROUTE_B / "routeB_dense_Mq" / "dhport_lib.jl",
    },
    "o1": {
        "directory": ROOT / "artifacts/task_routeb_o1_lean_api_audit_20260907",
        "node": "P4.true_dh_exact_real_coefficient_identity",
        "status_keys": ("status",),
        "expected_status": "UNCOMPILED__NON_VERIFIED",
        "source": ROOT / "artifacts/task_routeb_exact_real_coefficient_identity_20260907" / "REPORT.md",
    },
}

sys.path.insert(0, str(ROOT / "src"))
from percolation_workflow.store import StateStore  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()), "sha256": sha256(path)}


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def load_review(spec: dict) -> dict:
    directory = spec["directory"]
    report = directory / "REPORT.md"
    receipt = directory / "RECEIPT.json"
    for path in (report, receipt, spec["source"]):
        if not path.is_file():
            raise FileNotFoundError(path)
    data = json.loads(receipt.read_text(encoding="utf-8"))
    status = next((data.get(key) for key in spec["status_keys"]), None)
    if status != spec["expected_status"]:
        raise ValueError(f"unexpected review status: {status!r}")
    claims = data.get("claims", {})
    verification = data.get("verification", {})
    formal_allowed = data.get(
        "formal_certificate_allowed",
        claims.get("formal_certificate_allowed", verification.get("formal_certificate_allowed", False)),
    )
    safety = data.get("safety", {})
    registry_promoted = data.get(
        "registry_promoted",
        claims.get(
            "registry_promoted",
            verification.get("registry_promotion", safety.get("registry_promoted", False)),
        ),
    )
    if formal_allowed is not False:
        raise ValueError("review crosses formal certificate boundary")
    if registry_promoted is not False:
        raise ValueError("review crosses registry boundary")
    report_hash = sha256(report)
    declared_report_hash = data.get("report_sha256")
    if declared_report_hash is not None and declared_report_hash.upper() != report_hash:
        raise ValueError("report hash does not match receipt")
    source_ref = ref(spec["source"])
    declared_hashes = data.get("source_hashes_sha256", {})
    if declared_hashes and source_ref["sha256"].lower() not in {
        str(value).lower() for value in declared_hashes.values()
    }:
        raise ValueError("live source hash is absent from review receipt")
    return {
        "schema_version": 1,
        "review_status": status,
        "receipt_schema": data.get("schema", data.get("schema_version")),
        "review_artifacts": [ref(report), ref(receipt)],
        "source_artifact": source_ref,
        "evidence_level": data.get("evidence_level", data.get("scope")),
        "claims": claims,
        "unresolved": data.get("unresolved", []),
        "minimal_decomposition": data.get("minimal_decomposition", []),
        "formal_certificate_allowed": False,
        "registry_promoted": False,
        "admission_status": "pending_coordinator_admission",
    }


def main() -> int:
    reviews = {key: load_review(spec) for key, spec in TASKS.items()}
    store = StateStore(STATE)
    state = store.load()
    changed = False
    for key, spec in TASKS.items():
        node = find(state, spec["node"])
        child_changed = False
        prior = list(node.metadata.get("independent_static_reviews", []))
        if reviews[key] not in prior:
            prior.append(reviews[key])
            node.metadata["independent_static_reviews"] = prior
            changed = True
            child_changed = True
        unresolved = list(node.metadata.get("unresolved", []))
        marker = f"{key}_review_mathematical_obligations_open"
        if marker not in unresolved:
            unresolved.append(marker)
            node.metadata["unresolved"] = unresolved
            changed = True
            child_changed = True
        if child_changed:
            state.event(
                "routeb_child_static_review_recorded",
                node_id=node.id,
                child=key,
                review_status=reviews[key]["review_status"],
                admission_status="pending_coordinator_admission",
                registry_promoted=False,
                formal_certificate_allowed=False,
            )
    if changed:
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "children": {key: value["review_status"] for key, value in reviews.items()},
        "state_revision": store.load().revision,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

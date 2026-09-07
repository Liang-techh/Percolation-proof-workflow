"""Intake one external O2 runtime receipt into the persistent frontier.

This is a coordinator-side evidence intake only.  It records pending,
rejected, or ready-for-admission audits and never closes O2 or promotes a
registry entry.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "artifacts/routeb_6dof/state.json"
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.routeb_o2_receipt import (  # noqa: E402
    audit_routeb_o2_runtime_receipt,
)
from percolation_workflow.store import StateStore  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()
    receipt_path = args.receipt.resolve()
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_float64_evaluator_enclosure")
    dag = node.metadata.get("o2_dag_propagation", {})
    source_ref = dag.get("source_artifact", {})
    expected_source = source_ref.get("sha256")
    expected_schedule = dag.get("operation_schedule_hash")
    if not expected_source or not expected_schedule:
        raise ValueError("O2 node has no source/schedule binding for receipt intake")
    audit = audit_routeb_o2_runtime_receipt(
        receipt,
        expected_source_sha256=expected_source,
        expected_operation_schedule_hash=expected_schedule,
    )
    record = {
        "schema_version": 1,
        "receipt_artifact": {
            "path": str(receipt_path),
            "sha256": sha(receipt_path),
        },
        "source_binding": {
            "expected_source_sha256": expected_source,
            "expected_operation_schedule_hash": expected_schedule,
        },
        "audit": asdict(audit),
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    audits = list(node.metadata.get("runtime_receipt_audits", []))
    changed = record not in audits
    if changed:
        audits.append(record)
        node.metadata["runtime_receipt_audits"] = audits
        state.event(
            "routeb_o2_runtime_receipt_audited",
            node_id=node.id,
            audit_status=audit.status,
            receipt_sha256=record["receipt_artifact"]["sha256"],
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "audit_status": audit.status,
        "missing": list(audit.missing),
        "errors": list(audit.errors),
        "state_revision": store.load().revision,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0 if audit.status != "REJECTED" else 2


if __name__ == "__main__":
    raise SystemExit(main())

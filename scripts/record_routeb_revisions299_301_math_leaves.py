"""Record the next three independent Route-B mathematical bottleneck leaves."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def append_revision(store: StateStore, state, old: Path, new: Path, record: dict, algorithm: str, evidence: Path, event_kind: str, **flags):
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).append(flags.pop("frontier_update"))
    graph.update(schema=flags.pop("schema"), supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    backup = ROOT / f"artifacts/routeb_storage_checkpoint_20260908/state-before-revision{state.revision + 1}.json"
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    artifact = {
        "schema_version": 1,
        "algorithm": algorithm,
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": str(record["files"][0]) if record.get("files") else "",
        "evidence_sha256": sha(evidence),
        **flags,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    state.graph_artifacts.append(artifact)
    state.event(event_kind, proposed_dag=ref(new), proposed_dag_sha256=digest,
                registry_promoted=False, formal_certificate_allowed=False,
                broad_regression_run=False, **flags)
    store.save(state)


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    if state.revision != 298 or state.registry:
        raise ValueError("revision-299..301 recorder requires revision 298 and empty registry")

    # Revision 299: coverage receipt exporter design and synthetic structural smoke.
    side = ROOT / "artifacts/task_FLT_coverage_receipt_export_design_20260908"
    report, smoke = side / "REPORT.md", side / "receipt_schema_smoke.py"
    if not all(p.is_file() for p in (report, smoke)):
        raise ValueError("missing coverage receipt design")
    record = {
        "kind": "routeb_coverage_receipt_export_design",
        "status": "DESIGN_READY_STRUCTURAL_SMOKE_PASS_DYNAMICS_COVERAGE_OPEN",
        "evidence_level": "read-only-source-audit-plus-synthetic-receipt-schema-check",
        "files": [str(report), str(smoke)],
        "schema": "routeb-coverage-receipt-v1",
        "dimensions": 13,
        "requires": ["box_lo", "box_hi", "raw_box_lo", "raw_box_hi", "parent", "split_axis", "split_cut", "children", "leaf_classification", "pending_ids", "discarded_ids", "source_hashes"],
        "structural_smoke_pass": True,
        "canonical_exporter_implemented": False,
        "dynamics_coverage_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    append_revision(store, state, ROOT / "artifacts/routeb_6dof/block45-obligations-v252.json", ROOT / "artifacts/routeb_6dof/block45-obligations-v253.json", record, "routeb_revision299_coverage_receipt_design/v1", report, "routeb_revision299_coverage_receipt_design_recorded", schema="routeb-proposed-proof-dag-v253", audit_only=True, structural_smoke_pass=True, dynamics_coverage_complete=False, frontier_update={"node": "B45.coverage", "status": "receipt_export_design_ready", "reason": "A 13D adaptive-tree receipt schema and synthetic structural checker are ready; canonical exporter and dynamics coverage remain open."})

    # Revision 300: explicit rounding failure ledger, retained as open evidence.
    side = ROOT / "artifacts/task_FLT_rounding_audit_20260908"
    report = side / "REPORT.md"
    if not report.is_file():
        raise ValueError("missing rounding audit")
    record = {
        "kind": "routeb_rounding_and_source_semantics_audit",
        "status": "FAIL_CLOSED",
        "evidence_level": "read-only-code-audit-plus-targeted-counterexamples",
        "files": [str(report)],
        "conditional_bi_add_sub_mul_div": True,
        "unsafe_or_open": ["square_bounds", "radius", "scalar_aggregation", "qext", "decimal_conversion", "float64_bigfloat_semantics"],
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    append_revision(store, state, ROOT / "artifacts/routeb_6dof/block45-obligations-v253.json", ROOT / "artifacts/routeb_6dof/block45-obligations-v254.json", record, "routeb_revision300_rounding_audit/v1", report, "routeb_revision300_rounding_audit_recorded", schema="routeb-proposed-proof-dag-v254", audit_only=True, source_semantics_open=True, frontier_update={"node": "B45.rounding", "status": "fail_closed_scalar_rounding_open", "reason": "BI binary operations are conditional; square, radius, scalar sums, qext and conversion seams can still contract bounds."})

    # Revision 301: strict abstract interval-operation Lean leaf.
    side = ROOT / "artifacts/task_FLT_interval_ops_lean_leaf_20260908"
    lean, olean, receipt, report = (side / n for n in ("FLTIntervalOps.lean", "FLTIntervalOps.olean", "RECEIPT.md", "REPORT.md"))
    if not all(p.is_file() for p in (lean, olean, receipt, report)):
        raise ValueError("missing interval-ops Lean leaf")
    expected_lean = "a169444c91d0e14008e5abd6e7a9ec80845e91322100edd5f9d3b4f01de6e593"
    expected_olean = "2fa66f548b124d8d34e8a65f552d53b39f4e1df6209f2a48649fbbe55e470aaf"
    if sha(lean) != expected_lean or sha(olean) != expected_olean:
        raise ValueError("interval-ops Lean hashes do not match receipt")
    receipt_text = receipt.read_text(encoding="utf-8")
    if "Strict compile: exit code `0`" not in receipt_text or "no `sorry`, no `admit`, no custom `axiom`" not in receipt_text:
        raise ValueError("strict interval-ops receipt markers missing")
    record = {
        "kind": "routeb_abstract_interval_operations_lean_leaf",
        "status": "LEAN_VERIFIED_ABSTRACT_REAL_INTERVAL_OPERATIONS_SOURCE_BINDING_OPEN",
        "evidence_level": "strict-lean-compile-plus-abstract-receipt",
        "files": [str(lean), str(olean), str(receipt), str(report)],
        "lean_toolchain": "leanprover/lean4:v4.33.1",
        "mathlib_revision": "0df444a360eaa60ab8c11dca51a86af692955474",
        "source_sha256": expected_lean,
        "olean_sha256": expected_olean,
        "strict_compile": True,
        "custom_axioms": False,
        "concrete_julia_binding": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    append_revision(store, state, ROOT / "artifacts/routeb_6dof/block45-obligations-v254.json", ROOT / "artifacts/routeb_6dof/block45-obligations-v255.json", record, "routeb_revision301_interval_ops_lean_leaf/v1", receipt, "routeb_revision301_interval_ops_lean_leaf_recorded", schema="routeb-proposed-proof-dag-v255", strict_compile=True, abstract_only=True, concrete_julia_binding=False, frontier_update={"node": "B45.rounding", "status": "abstract_interval_ops_verified", "reason": "Exact-real interval arithmetic and square interfaces compile in Lean; concrete Julia rounding/source semantics remain open."})
    print(json.dumps({"revision": state.revision, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()

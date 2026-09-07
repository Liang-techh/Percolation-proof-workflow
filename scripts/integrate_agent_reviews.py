"""Idempotently integrate pending inbox records as fail-closed metadata.

The inbox is intentionally append-only.  This command never promotes a node,
changes the registry, or edits an input record.  It records provenance on a
matching Route-B node or, for external-library scans, an event-only catalog
record, then writes a small processed marker so a periodic runner can safely
invoke it repeatedly.  In addition to review results, the collector accepts
typed ``handoff`` and ``companion_log`` records so useful agent output is not
lost merely because it was emitted under a different filename.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore
from percolation_workflow.routeb_residual_l1_contract import (
    audit_routeb_residual_l1_lean_receipt,
)


TASK_TARGETS = {
    "T-P0-001": ("P0.reproducibility_baseline", "reproducibility_baseline_blocked"),
    "T-DAG-002": ("M4.block45_full_certificate", "child_dag_refinement_proposal"),
    "T-P3-003": ("P3.strict_true_dh_bounds", "pending_source_manifest_binding"),
    "T-P4-003": ("P4.residual_schur_pmi", "conditional_typed_normalization"),
    "T-P4-004": ("P4.residual_schur_pmi", "conditional_typed_normalization_sidecar"),
    "T-P8-003": ("P8.independent_reachability", "explicit_time_contract_recommended"),
    "T-P8-004": ("P8.independent_reachability", "explicit_time_typed_sidecar"),
    "T-P5-001": ("P5.sparse_disjunctive_sos", "energy_syzygy_reuse_audit"),
    "T-P3-004": ("P3.strict_true_dh_bounds", "pending_source_semantic_adapter"),
    "T-P3-005": ("P3.strict_true_dh_bounds", "pending_semantic_binding_child"),
    "T-P5-002": ("P5.sparse_disjunctive_sos", "pending_energy_child"),
    "T-P3-006": ("P3.strict_true_dh_bounds", "pending_semantic_binding_sidecar"),
    "T-P5-003": ("P5.sparse_disjunctive_sos", "pending_christoffel_power_sidecar"),
    "T-P5-004": ("P5.sparse_disjunctive_sos", "pending_dissipative_residual_power_child"),
    "T-P5-005": ("P5.sparse_disjunctive_sos", "pending_relative_residual_strict_decay"),
    "T-P5-006": ("P5.componentwise_relative_decay", "pending_component_relative_decay_sidecar"),
    "T-P5-007": ("P5.sparse_disjunctive_sos", "pending_weighted_dual_decay_obstruction"),
    "T-P5-008": ("P5.sparse_disjunctive_sos", "pending_force_error_bias_split"),
    "T-P5-009": ("P5.sparse_disjunctive_sos", "pending_fd_relative_scaling_obstruction"),
    # External FLT scans are deliberately event-only: they are advisory
    # catalog evidence, not Route-B theorem nodes or registry entries.
    "T-FLT-DERIV-CALC": (None, "flt_derivation_calculus_scan"),
    "T-FLT-TOPOLOGY-QUOTIENT-CLM": (None, "flt_topology_quotient_scan"),
    "T-FLT-SPECTRAL-LINEAR": (None, "flt_spectral_linear_scan"),
    "T-FLT-TRANSPORT-ADAPTER": (None, "flt_transport_adapter_scan"),
    "T-FLT-INFRA-REGISTRY": (None, "flt_registry_graph_scan"),
    "T-FLT-SPECTRAL-SIDECAR": (None, "flt_spectral_sidecar"),
    "T-FLT-SPECTRAL-PREDICATE": (None, "flt_spectral_predicate_sidecar"),
    "T-FLT-QUOTIENT-SIDECAR": (None, "flt_quotient_transport_sidecar"),
    "T-P4-KC-COORDINATE-ADAPTER": ("P4.residual_schur_pmi", "pending_kc_coordinate_adapter"),
    "T-P4-MBD-PROJECTION": ("P4.residual_schur_pmi", "pending_mbd_projection_obstruction"),
    "T-P4-012": ("P4.residual_schur_pmi", "pending_typed_remote_binding_contract"),
    "T-P4-013": ("P4.residual_schur_pmi", "pending_remote_budget_pmi_composition"),
    "T-P4-014": ("P4.residual_schur_pmi", "pending_vector_remote_pmi_composition"),
    "T-P4-015": ("P4.residual_schur_pmi", "pending_nominal_distal_descriptor_bridge"),
    "T-P4-016": ("P4.residual_schur_pmi", "pending_nominal_distal_tail_pmi"),
    "T-P4-017": ("P4.residual_schur_pmi", "pending_tail_gram_reconstruction"),
    "T-P4-018": ("P4.nominal_distal_residual_l1_lean_seam",
                 "pending_residual_l1_lean_seam"),
    "T-P3-007": ("P3.strict_true_dh_bounds", "pending_concrete_mass_entry_bridge"),
    "T-P4-005": ("P4.residual_schur_pmi", "pending_one_channel_source_binding"),
    "T-P4-006": ("P4.residual_schur_pmi", "pending_sharp_schur_formalization"),
    "T-P4-007": ("P4.residual_schur_pmi", "pending_actual_block45_residual_decomposition"),
    "T-P4-008": ("P4.residual_schur_pmi", "pending_kc_mbd_obstruction_formalization"),
    "T-P4-011": ("P4.residual_schur_pmi", "pending_canonical_kc_budget"),
    "T-P3-008": ("P3.strict_true_dh_bounds", "pending_central_fd_christoffel_binding"),
    "T-P3-009": ("P3.strict_true_dh_bounds", "pending_block45_positive_inverse_bounds"),
    "T-P3-010": ("P3.strict_true_dh_bounds", "pending_block45_mass_interval_derivation"),
    "T-P3-011": ("P3.strict_true_dh_bounds", "pending_link_jacobian_block_lower_bound"),
    "T-P3-012": ("P3.true_dh_derivative_hull_leaf", "pending_flt_derivative_leaf_review"),
    "T-P3-013": ("P3.strict_true_dh_bounds", "pending_concrete_true_dh_derivative_hull_instance"),
    "T-P3-014": ("P3.trig_endpoint_enclosure_leaf", "pending_concrete_trig_source_binding"),
    "T-P3-015": ("P3.m33_exact_fourier_source_leaf", "pending_m33_fourier_leaf_lift"),
    "T-P3-016": ("P3.m33_exact_lower_bound", "pending_m33_exact_lower_bound_compile"),
    "T-P3-017": ("P3.rotational_prefix_mass_lower_bound", "pending_rotational_mass_lower_bound_lift"),
    "T-P4-019": ("P4.block45_global_mass_geometry_schur", "pending_block45_global_geometry_schur_lift"),
    "T-P4-020": ("P4.residual_schur_pmi", "pending_one_cell_residual_remainder_absorption"),
    "T-P4-021": ("P4.residual_port_frobenius_bound", "pending_resolved_cell_frobenius_port_lift"),
    "T-P4-022": ("P4.frobenius_operator_norm_bridge", "pending_frobenius_operator_bridge_compile"),
    "T-M4-008": ("M4.energy_to_schur_budget_bridge", "pending_conditional_energy_schur_bridge"),
    "T-P8-005": ("P8.independent_reachability", "pending_terminal_transfer_interface"),
    "T-P8-006": ("P8.ramp_reconstruction_compiled_candidate", "pending_ramp_reconstruction_child"),
    "T-P8-007": ("P8.independent_reachability", "pending_ramp_sidecar_validation"),
    "T-P8-009": ("P8.independent_reachability", "pending_interval_local_ramp_calculus"),
    "T-P8-010": ("P8.ramp_reconstruction_compiled_candidate", "pending_compiled_candidate_gate_review"),
    "T-P8-011": ("P8.interval_local_endpoint_adapter", "pending_interval_local_ramp_endpoint_adapter"),
    "T-P8-008": ("P8.independent_reachability", "pending_first12_explicit_time_adapter"),
    "T-P0-002": ("P0.reproducibility_baseline", "pending_fresh_receipt_reaudit"),
    "T-M4-002": ("M4.block45_full_certificate", "pending_dependency_cone_reaudit"),
    "T-M4-003": ("M4.block45_full_certificate", "pending_weighted_terminal_split"),
    "T-M4-004": ("M4.block45_full_certificate", "pending_generic_weighted_qpoly_sidecar"),
    "T-M4-005": ("M4.block45_full_certificate", "pending_eta81_terminal_corollary"),
    "T-M4-006": ("M4.block45_full_certificate", "pending_cross_branch_budget_transfer"),
    "T-M4-007": ("M4.cross_branch_budget_transfer", "pending_pure_budget_transfer_formalization"),
    "T-P7-001": ("P7.strict_tail_fallback", "pending_tail_obligation_audit"),
    "T-P7-002": ("P7.tail_schur_completion_2x2", "pending_typed_tail_schur_completion"),
    "T-DAG-003": ("M4.block45_full_certificate", "pending_shared_lemma_projection"),
    "T-REPAIR-001": ("P3.strict_true_dh_bounds", "pending_repair_loop_audit"),
}

REVIEW_ID_ALIASES = {
    "review-FLT-topology-quotient-clm": "T-FLT-TOPOLOGY-QUOTIENT-CLM",
}

RECORD_GLOBS = (
    "review-*.md", "handoff-*.md", "handoff-*.json",
    "companion-*.md", "companion-*.json",
)
RECORD_KINDS = {"review_result", "handoff", "companion_log"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def front_matter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) < 2:
        return {}
    # Accept the legacy inbox shape without an opening delimiter, but expose
    # the repair as metadata so malformed handoffs never look fully clean.
    legacy = lines[0].strip() != "---"
    start = 1 if not legacy else 0
    try:
        end = lines.index("---", start)
    except ValueError:
        if legacy:
            # A few periodic workers emit a key/value header without either
            # YAML delimiter.  Recover only the contiguous pre-heading
            # metadata; never scan the mathematical body for task fields.
            recovered: dict[str, str] = {}
            for line in lines:
                if line.lstrip().startswith("#"):
                    break
                match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)", line)
                if match:
                    recovered[match.group(1)] = match.group(2).strip().strip("'\"")
            if recovered.get("kind"):
                recovered["_format_warning"] = "missing_yaml_delimiters"
                return recovered
        return {}
    result: dict[str, str] = {}
    for line in lines[start:end]:
        match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)", line)
        if match:
            result[match.group(1)] = match.group(2).strip().strip("'\"")
    if legacy:
        result["_format_warning"] = "missing_opening_yaml_delimiter"
    return result


def record_header(path: Path) -> dict[str, str]:
    """Read the bounded metadata envelope for an inbox record."""
    if path.suffix.lower() == ".json":
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            return {}
        if not isinstance(value, dict):
            return {}
        return {str(key): str(item) if item is not None else ""
                for key, item in value.items()}
    return front_matter(path)


def record_kind(path: Path, header: dict[str, str]) -> str | None:
    """Return the accepted record kind, or ``None`` for planning/noise files."""
    kind = header.get("kind", "")
    if kind in RECORD_KINDS:
        return kind
    if kind:
        return None
    # A filename convention is a narrow compatibility fallback for old agent
    # envelopes that omitted ``kind``; it does not scan the mathematical body.
    name = path.name.lower()
    if name.startswith("review-"):
        return "review_result"
    if name.startswith("handoff-"):
        return "handoff"
    if name.startswith("companion-"):
        return "companion_log"
    return None


def inbox_records(inbox: Path) -> list[Path]:
    """Return unique root-level record paths in deterministic order."""
    return sorted({path for pattern in RECORD_GLOBS for path in inbox.glob(pattern)})


def source_commit(path: Path, header: dict[str, str]) -> str:
    """Recover an explicitly printed Git commit when agents put it in prose."""
    declared = str(header.get("commit", "")).strip()
    if declared:
        return declared
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])", text, re.IGNORECASE)
    return match.group(0) if match else "unknown"


def node_by_name(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"no Route-B node named {name!r}")


def routeb_residual_l1_receipt_audit(state, node, path: Path) -> dict | None:
    """Audit only a structured T-P4-018 JSON handoff, never prose claims."""
    if path.suffix.lower() != ".json":
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return {"status": "REJECTED", "errors": ["handoff_json_malformed"],
                "pending": []}
    if not isinstance(payload, dict):
        return {"status": "REJECTED", "errors": ["handoff_json_not_object"],
                "pending": []}
    receipt = payload.get("receipt", payload.get("lean_receipt"))
    if not isinstance(receipt, dict):
        return {"status": "PENDING", "errors": [],
                "pending": ["missing_structured_residual_l1_receipt"]}

    source_hash = None
    for artifact in node.metadata.get("source_artifacts", []):
        if (isinstance(artifact, dict) and
                str(artifact.get("path", "")).replace("\\", "/").endswith(
                    "examples/routeb_gram_residual_lean/GramResidual.lean")):
            source_hash = artifact.get("sha256")
            break
    candidate = None
    if node.parent_id and node.parent_id in state.nodes:
        candidate = state.nodes[node.parent_id].metadata.get(
            "candidate_reconstruction_receipt")
    audit = audit_routeb_residual_l1_lean_receipt(
        receipt,
        expected_source_sha256=source_hash,
        expected_coefficient_artifact_sha256=(
            candidate.get("artifact_sha256") if isinstance(candidate, dict) else None),
        candidate_receipt=candidate if isinstance(candidate, dict) else None,
    )
    return {
        "status": audit.status,
        "source_sha256": audit.source_sha256,
        "coefficient_artifact_sha256": audit.coefficient_artifact_sha256,
        "theorem_names": list(audit.theorem_names),
        "axioms": {name: list(values) for name, values in audit.axioms.items()},
        "errors": list(audit.errors),
        "pending": list(audit.pending),
        "formal_certificate_allowed": audit.formal_certificate_allowed,
        "registry_eligible": audit.registry_eligible,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path,
                        default=ROOT / "artifacts/routeb_6dof/state.json")
    parser.add_argument("--inbox", type=Path,
                        default=ROOT / "agent_review_inbox")
    args = parser.parse_args()
    state_path = args.state.resolve(strict=True)
    inbox = args.inbox.resolve(strict=True)
    processed = inbox / "processed"
    processed.mkdir(parents=True, exist_ok=True)

    candidates = []
    for path in inbox_records(inbox):
        header = record_header(path)
        kind = record_kind(path, header)
        if kind is None:
            continue
        if header.get("integration_status") == "integrated":
            continue
        task_id = header.get("task_id", "") or REVIEW_ID_ALIASES.get(
            header.get("review_id", ""), "")
        if task_id not in TASK_TARGETS:
            continue
        digest = sha256(path)
        marker = processed / path.with_suffix(".json").name
        previous = None
        if marker.exists():
            try:
                old = json.loads(marker.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                raise ValueError(f"malformed processed marker: {marker}") from exc
            if old.get("review_sha256", "").upper() == digest:
                continue
            # A changed same-name file is a correction/revision, not an excuse
            # to overwrite history.  Keep the old hash in the new provenance
            # record and require a second, explicit integration event.
            previous = old
        candidates.append((path, header, kind, digest, marker, previous))

    if not candidates:
        print(json.dumps({"integrated": [], "state_revision": StateStore(state_path).load().revision}))
        return 0

    store = StateStore(state_path)
    state = store.load()
    if state.project != "routeb-6dof-external":
        raise ValueError(f"unexpected project: {state.project!r}")
    if any(node.status.value == "in_progress" for node in state.nodes.values()):
        raise ValueError("refuse inbox integration while a node is in progress")

    integrated = []
    for path, header, kind, digest, marker, previous in candidates:
        task_id = header.get("task_id", "") or REVIEW_ID_ALIASES.get(
            header.get("review_id", ""), "")
        target_name, classification = TASK_TARGETS[task_id]
        record_file = str(path.relative_to(ROOT)).replace("\\", "/")
        ref = {
            "record_file": record_file,
            "record_kind": kind,
            "review_sha256": digest,
            "task_id": task_id,
            "source_agent": header.get("source_agent", "unknown"),
            "created_at": header.get("created_at", "unknown"),
            "integration_status": "integrated_as_pending_metadata",
            "classification": classification,
            "admission_effect": "none",
            "target_scope": "routeb_node" if target_name else "external_reuse_catalog",
            "source_commit": source_commit(path, header),
        }
        if kind == "review_result":
            # Keep the legacy field stable for downstream reports and old
            # processed markers while exposing the generic record envelope.
            ref["review_file"] = record_file
        if header.get("admission_label"):
            ref["admission_label"] = header["admission_label"]
        if previous is not None:
            ref["correction_of_sha256"] = previous.get("review_sha256")
            ref["classification"] = f"{classification}_revision"
        if header.get("_format_warning"):
            ref["format_warning"] = header["_format_warning"]
        if target_name:
            node = node_by_name(state, target_name)
            if task_id == "T-P4-018":
                receipt_audit = routeb_residual_l1_receipt_audit(state, node, path)
                if receipt_audit is not None:
                    ref["residual_l1_receipt_audit"] = receipt_audit
                    node.metadata.setdefault("residual_l1_receipt_audits", []).append({
                        "record_file": record_file,
                        "review_sha256": digest,
                        **receipt_audit,
                    })
            node.metadata.setdefault("agent_review_refs", []).append(ref)
        event_kind = {
            "review_result": "agent_review_integrated",
            "handoff": "agent_handoff_integrated",
            "companion_log": "agent_companion_integrated",
        }[kind]
        state.event(
            event_kind if target_name else f"external_reuse_{event_kind}",
            record_file=record_file,
            record_kind=kind,
            review_sha256=digest,
            task_id=task_id,
            classification=ref["classification"],
            admission_effect="none",
            registry_promoted=False,
            formal_certificate_allowed=False,
            **({"residual_l1_receipt_status": ref["residual_l1_receipt_audit"]["status"]}
               if "residual_l1_receipt_audit" in ref else {}),
            **({"node_id": node.id} if target_name else {
                "catalog": "anthropic-fermats-last-theorem",
            }),
        )
        integrated.append((path, marker, ref, state.events[-1]["at"]))

    # StateStore performs the optimistic revision check and checksum update.
    store.save(state)
    for path, marker, ref, event_at in integrated:
        marker.write_text(json.dumps({**ref, "integrated_at": event_at},
                                     ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")
    print(json.dumps({"integrated": [ref["task_id"] for _, _, ref, _ in integrated],
                      "state_revision": state.revision,
                      "registry_size": len(state.registry),
                      "formal_certificate_allowed": False}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

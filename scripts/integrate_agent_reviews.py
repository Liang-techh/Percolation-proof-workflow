"""Idempotently integrate pending agent review results as fail-closed metadata.

The inbox is intentionally append-only.  This command never promotes a node,
changes the registry, or edits the review itself.  It records provenance on a
matching Route-B node or, for external-library scans, an event-only catalog
record, then writes a small processed marker so a periodic runner can safely
invoke it repeatedly.
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
    # External FLT scans are deliberately event-only: they are advisory
    # catalog evidence, not Route-B theorem nodes or registry entries.
    "T-FLT-DERIV-CALC": (None, "flt_derivation_calculus_scan"),
    "T-FLT-TOPOLOGY-QUOTIENT-CLM": (None, "flt_topology_quotient_scan"),
    "T-FLT-SPECTRAL-LINEAR": (None, "flt_spectral_linear_scan"),
    "T-FLT-TRANSPORT-ADAPTER": (None, "flt_transport_adapter_scan"),
    "T-FLT-INFRA-REGISTRY": (None, "flt_registry_graph_scan"),
    "T-FLT-SPECTRAL-SIDECAR": (None, "flt_spectral_sidecar"),
    "T-FLT-SPECTRAL-PREDICATE": (None, "flt_spectral_predicate_sidecar"),
    "T-P3-007": ("P3.strict_true_dh_bounds", "pending_concrete_mass_entry_bridge"),
    "T-P4-005": ("P4.residual_schur_pmi", "pending_one_channel_source_binding"),
    "T-P8-005": ("P8.independent_reachability", "pending_terminal_transfer_interface"),
    "T-P0-002": ("P0.reproducibility_baseline", "pending_fresh_receipt_reaudit"),
    "T-M4-002": ("M4.block45_full_certificate", "pending_dependency_cone_reaudit"),
    "T-P7-001": ("P7.strict_tail_fallback", "pending_tail_obligation_audit"),
    "T-DAG-003": ("M4.block45_full_certificate", "pending_shared_lemma_projection"),
    "T-REPAIR-001": ("P3.strict_true_dh_bounds", "pending_repair_loop_audit"),
}

REVIEW_ID_ALIASES = {
    "review-FLT-topology-quotient-clm": "T-FLT-TOPOLOGY-QUOTIENT-CLM",
}


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


def source_commit(path: Path, header: dict[str, str]) -> str:
    """Recover an explicitly printed Git commit when agents put it in prose."""
    declared = header.get("commit", "").strip()
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
    for path in sorted(inbox.glob("review-*.md")):
        header = front_matter(path)
        if header.get("kind") != "review_result":
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
        candidates.append((path, header, digest, marker, previous))

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
    for path, header, digest, marker, previous in candidates:
        task_id = header.get("task_id", "") or REVIEW_ID_ALIASES.get(
            header.get("review_id", ""), "")
        target_name, classification = TASK_TARGETS[task_id]
        ref = {
            "review_file": str(path.relative_to(ROOT)).replace("\\", "/"),
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
        if header.get("admission_label"):
            ref["admission_label"] = header["admission_label"]
        if previous is not None:
            ref["correction_of_sha256"] = previous.get("review_sha256")
            ref["classification"] = f"{classification}_revision"
        if header.get("_format_warning"):
            ref["format_warning"] = header["_format_warning"]
        if target_name:
            node = node_by_name(state, target_name)
            node.metadata.setdefault("agent_review_refs", []).append(ref)
        state.event(
            "agent_review_integrated" if target_name else "external_reuse_review_integrated",
            review_file=ref["review_file"],
            review_sha256=digest,
            task_id=task_id,
            classification=ref["classification"],
            admission_effect="none",
            registry_promoted=False,
            formal_certificate_allowed=False,
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

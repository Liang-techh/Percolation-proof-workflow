"""Record the independently reviewed P8 ramp sidecar as a candidate child."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore


def ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    parent = find(state, "P8.independent_reachability")
    name = "P8.ramp_reconstruction_compiled_candidate"
    source_artifacts = [ref(path) for path in (
        ROOT / "examples/routeb_p8_ramp_reconstruction_sidecar/P8RampReconstruction.lean",
        ROOT / "examples/routeb_p8_ramp_reconstruction_sidecar/README.md",
        ROOT / "examples/routeb_p8_ramp_reconstruction_sidecar/lean-toolchain",
        ROOT / "examples/routeb_p8_ramp_reconstruction_sidecar/verify.sh",
    )]
    unresolved = [
        "coordinator_statement_identity_and_manifest_binding",
        "current_source_snapshot_recompile_binding",
        "first12_true_DH_source_binding",
        "interval_flowpipe_and_coverage",
    ]
    compiled_receipt = {
        "review_id": "T-P8-010",
        "review_file": "agent_review_inbox/review-T-P8-010-fengbujue-20260906T2318.md",
        "compiled_commit": "0723aea49d4051af7cb1c6e5848b1a1984e6bbdc",
        "workflow": "Lean agent sidecars",
        "run_id": "34085393805",
        "job_id": "101628339820",
        "runner": "ubuntu-24.04",
        "lean_toolchain": "leanprover/lean4:v4.32.0",
        "mathlib_commit": "81a5d257c8e410db227a6665ed08f64fea08e997",
        "source_blob": "0bcac8908b2492ae72279ef0cd05b2d6634bc3a9",
        "verifier_blob": "89144cf54bcdc1d71db8230b9387103c5298b1cf",
        "theorem_names": [
            "RouteBP8RampReconstruction.ramp_c_constant",
            "RouteBP8RampReconstruction.ramp_w_eq_mul",
            "RouteBP8RampReconstruction.ramp_reconstruction",
            "RouteBP8RampReconstruction.state_tail_reconstruction",
            "RouteBP8RampReconstruction.state_terminal_one",
        ],
        "axiom_audit": "passed",
        "compile_status": "passed",
        "admission_effect": "none",
    }
    existing = next((n for n in state.nodes.values() if n.name == name), None)
    if existing is None:
        node_id = state.add_node(
            name,
            "The abstract ramp equations reconstruct c(t)=c0 and w(t)=c0*t "
            "and transfer w(1)=c0 under the stated derivative hypotheses.",
            parent_id=parent.id,
            dependencies=[],
            proof_sketch=(
                "Use the independently reviewed ramp calculus candidate; "
                "keep first-12 source binding and interval flowpipe separate."),
            metadata={
                "verification_domain": "lean-compiled-candidate",
                "statement_status": "compiled_candidate_pending_registry",
                "evidence_level": "independently_reviewed_github_compile",
                "claim_status": "abstract_ramp_candidate_open",
                "registry_eligible": False,
                "comparator_accepted": False,
                "formal_certificate_allowed": False,
                "preferred_route": True,
                "unresolved": unresolved,
                "compiled_candidate_receipt": compiled_receipt,
                "source_artifacts": source_artifacts,
            },
        )
        state.event("routeb_p8_ramp_compiled_candidate_created",
                    node_id=node_id, parent_id=parent.id,
                    compiled_candidate_receipt=compiled_receipt,
                    source_artifacts=source_artifacts,
                    status="compiled_candidate_pending_registry",
                    formal_certificate_allowed=False, registry_promoted=False)
        store.save(state)
        print({"status": "recorded", "node_id": node_id,
               "state_revision": state.revision})
        return 0

    changed = False
    for key, value in (("source_artifacts", source_artifacts),
                       ("unresolved", unresolved),
                       ("compiled_candidate_receipt", compiled_receipt)):
        if existing.metadata.get(key) != value:
            existing.metadata[key] = value
            changed = True
    if existing.parent_id != parent.id:
        existing.parent_id = parent.id
        changed = True
    if existing.id not in parent.dependencies:
        parent.dependencies.append(existing.id)
        changed = True
    if changed:
        state.event("routeb_p8_ramp_candidate_provenance_refresh",
                    node_id=existing.id, parent_id=parent.id,
                    compiled_candidate_receipt=compiled_receipt,
                    status="compiled_candidate_pending_registry",
                    formal_certificate_allowed=False, registry_promoted=False)
        store.save(state)
        print({"status": "provenance_refreshed", "node_id": existing.id,
               "state_revision": state.revision})
    else:
        print({"status": "already_recorded", "node_id": existing.id,
               "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

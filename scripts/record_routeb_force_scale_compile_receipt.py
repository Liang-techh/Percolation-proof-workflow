"""Admit a fresh force-scale Lean receipt only as a compiled candidate."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-force-scale-adapter-lean-target-codex-20260907.md"
RECEIPT = ROOT / "examples/routeb_b45_5_residual_decomposition_lean/COMPILE_RECEIPT_forceScaleKc_20260907.md"
CANDIDATE = ROOT / "examples/routeb_b45_5_residual_decomposition_lean/ResidualDecomposition.lean"
ROUTE_B = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
DEPLOYED = ROUTE_B / "robot_final" / "dhport_lib.jl"
LIFTED = ROUTE_B / "routeB_dense_Mq" / "routeB_fourier_lifted_descriptor_model.jl"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()), "sha256": sha(path)}


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def field_hash(text: str, label: str) -> str:
    match = re.search(rf"{re.escape(label)}:\s*`?([0-9A-Fa-f]{{64}})`?", text)
    if not match:
        raise ValueError(f"receipt field missing: {label}")
    return match.group(1).upper()


def main() -> int:
    for path in (REVIEW, RECEIPT, CANDIDATE, DEPLOYED, LIFTED, STATE):
        if not path.is_file():
            raise FileNotFoundError(path)
    text = RECEIPT.read_text(encoding="utf-8", errors="replace")
    for phrase in (
        "Fresh pinned compile/axiom receipt",
        "Lean: `4.33.1`", "Mathlib commit:",
        "canonical `ResidualDecomposition.lean` compile exit: `0`",
        "fresh theorem-check exit: `0`", "sorry/admit` source scan: `PASS`",
        "forceScaleKc_eq_rhoKc", "standard Lean logic set",
        "exact statement comparator: `NOT RUN / OPEN`",
        "registry promotion: `false`", "deployed `tau` equivalence: `NOT CLAIMED / OPEN`",
    ):
        if phrase not in text:
            raise ValueError(f"force-scale receipt boundary missing: {phrase}")
    candidate_hash = field_hash(text, "Source SHA-256")
    if candidate_hash != sha(CANDIDATE):
        raise ValueError("force-scale candidate hash drifted")
    if b"sorry" in CANDIDATE.read_bytes().lower() or b"admit" in CANDIDATE.read_bytes().lower():
        raise ValueError("force-scale candidate contains sorry/admit")
    olean_hash = field_hash(text, "OLean SHA-256")
    review_entry = {
        "schema_version": 1,
        "task_id": "T-P4-KC-COORDINATE-ADAPTER",
        "source_agent": "codex-local",
        "review_status": "COMPILED_CANDIDATE_SOURCE_COMPARATOR_PENDING",
        "review_artifact": ref(REVIEW),
        "receipt_artifact": ref(RECEIPT),
        "candidate_artifact": ref(CANDIDATE),
        "candidate_sha256": candidate_hash,
        "olean_sha256": olean_hash,
        "theorems": ["RouteBB45ResidualDecomposition.forceScaleKc_eq_rhoKc"],
        "toolchain": {
            "lean": "4.33.1",
            "lean_commit": "819816b2e0a3bf405af45ae5c7af2491d8f5bee6",
            "mathlib_commit": "0df444a360eaa60ab8c11dca51a86af692955474",
        },
        "compile": {"candidate_exit_code": 0, "theorem_check_exit_code": 0,
                    "sorry_admit_scan": "PASS"},
        "axioms": ["propext", "Classical.choice", "Quot.sound"],
        "source_binding": "OPEN",
        "statement_comparator": "OPEN",
        "deployed_tau_equivalence": "NOT_CLAIMED",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
        "admission_status": "compiled_candidate_only",
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_force_descriptor_semantics")
    prior = list(node.metadata.get("compiled_candidate_receipts", []))
    changed = review_entry not in prior
    if changed:
        prior.append(review_entry)
        node.metadata["compiled_candidate_receipts"] = prior
    desired = {
        "status": "COMPILED_CANDIDATE_SOURCE_COMPARATOR_PENDING",
        "theorem": review_entry["theorems"][0],
        "candidate_sha256": candidate_hash,
        "receipt_sha256": sha(RECEIPT),
        "toolchain": review_entry["toolchain"],
        "axioms": review_entry["axioms"],
        "source_binding": "OPEN",
        "statement_comparator": "OPEN",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("force_scale_compiled_candidate") != desired:
        node.metadata["force_scale_compiled_candidate"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_force_scale_compiled_candidate_recorded",
            node_id=node.id,
            theorem=review_entry["theorems"][0],
            admission_status=review_entry["admission_status"],
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_status": review_entry["review_status"],
        "state_revision": store.load().revision,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

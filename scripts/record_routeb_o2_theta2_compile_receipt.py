"""Record the compiled exact-real theta2 child while keeping O2 open."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-036.2-range-reduction-lemma-codex-20260907.md"
SOURCE = ROOT / "artifacts/routeb_fd8_tensor_christoffel_enclosure_20260906/mathlib/DownstreamTest/Theta2ExactRealApi.lean"
OLEAN = ROOT / "artifacts/routeb_fd8_tensor_christoffel_enclosure_20260906/mathlib/DownstreamTest/Theta2ExactRealApi.olean"
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


def main() -> int:
    # The long directory component is intentionally checked below; a typo must
    # fail rather than silently recording an unpinned sidecar.
    for path in (REVIEW, SOURCE, OLEAN, STATE):
        if not path.is_file():
            raise FileNotFoundError(path)
    text = REVIEW.read_text(encoding="utf-8", errors="replace")
    for phrase in (
        "EXACT_REAL_THETA2_RANGE_REDUCTION_TAYLOR_DRAFT",
        "theta2_exact_real_interval",
        "exit_code: 0",
        "Lean (version 4.33.1",
        "coverage: OPEN",
        "formal_certificate_allowed: false",
        "registry_promoted: false",
    ):
        if phrase not in text:
            raise ValueError(f"theta2 receipt boundary missing: {phrase}")
    expected_source = "5E5C064FDC2179FE966FED6DE298564F45F69998DCB675D9CDB0AA59172BADAF"
    expected_olean = "BAAD80B24C28639EF8C9E0453ED0D20D8C8CFCD12CF748EC8C178B8F3DEA413B"
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_float64_evaluator_enclosure")
    if sha(SOURCE) != expected_source or sha(OLEAN) != expected_olean:
        rejection = {
            "schema_version": 1,
            "task_id": "T-P4-036.2",
            "source_agent": "codex-local",
            "review_status": "REJECTED_STALE_SOURCE_OR_OLEAN_HASH",
            "review_artifact": ref(REVIEW),
            "current_source_artifact": ref(SOURCE),
            "current_olean_artifact": ref(OLEAN),
            "expected_source_sha256": expected_source,
            "expected_olean_sha256": expected_olean,
            "coverage": "OPEN",
            "formal_certificate_allowed": False,
            "registry_promoted": False,
        }
        prior = list(node.metadata.get("o2_exact_real_children", []))
        changed = rejection not in prior
        if changed:
            prior.append(rejection)
            node.metadata["o2_exact_real_children"] = prior
        desired = {
            "status": rejection["review_status"],
            "task_id": rejection["task_id"],
            "expected_source_sha256": expected_source,
            "current_source_sha256": rejection["current_source_artifact"]["sha256"],
            "expected_olean_sha256": expected_olean,
            "current_olean_sha256": rejection["current_olean_artifact"]["sha256"],
            "coverage": "OPEN",
            "formal_certificate_allowed": False,
            "registry_promoted": False,
        }
        if node.metadata.get("o2_theta2_exact_real_child") != desired:
            node.metadata["o2_theta2_exact_real_child"] = desired
            changed = True
        if changed:
            state.event(
                "routeb_o2_theta2_receipt_rejected_stale_hash",
                node_id=node.id,
                expected_source_sha256=expected_source,
                current_source_sha256=rejection["current_source_artifact"]["sha256"],
                registry_promoted=False,
                formal_certificate_allowed=False,
            )
            state.validate()
            store.save(state)
        print({
            "status": "rejected_stale_hash",
            "state_revision": store.load().revision,
            "current_source_sha256": rejection["current_source_artifact"]["sha256"],
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        })
        return 2
    entry = {
        "schema_version": 1,
        "task_id": "T-P4-036.2",
        "source_agent": "codex-local",
        "review_status": "COMPILED_CONDITIONAL_EXACT_REAL_CHILD_FLOAT64_BINDING_OPEN",
        "review_artifact": ref(REVIEW),
        "source_artifact": ref(SOURCE),
        "olean_artifact": ref(OLEAN),
        "theorems": [
            "theta2_sin", "theta2_cos", "sin_linear_remainder",
            "cos_quadratic_lower", "cos_global_upper", "theta2_exact_real_interval",
        ],
        "toolchain": {
            "lean": "4.33.1",
            "lean_commit": "819816b2e0a3bf405af45ae5c7af2491d8f5bee6",
        },
        "compile_exit_code": 0,
        "axiom_scan": "not supplied by this review",
        "exact_real_scope": "link i=2, theta=q-pi/2, q in [-3/20,3/20]",
        "coverage": "OPEN",
        "float64_binding": "OPEN",
        "libm_binding": "OPEN",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    children = list(node.metadata.get("o2_exact_real_children", []))
    changed = entry not in children
    if changed:
        children.append(entry)
        node.metadata["o2_exact_real_children"] = children
    desired = {
        "status": entry["review_status"],
        "task_id": entry["task_id"],
        "theorem": "theta2_exact_real_interval",
        "source_sha256": expected_source,
        "olean_sha256": expected_olean,
        "compile_exit_code": 0,
        "coverage": "OPEN",
        "float64_binding": "OPEN",
        "libm_binding": "OPEN",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("o2_theta2_exact_real_child") != desired:
        node.metadata["o2_theta2_exact_real_child"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o2_theta2_exact_real_child_recorded",
            node_id=node.id,
            theorem="theta2_exact_real_interval",
            review_status=entry["review_status"],
            coverage="OPEN",
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_status": entry["review_status"],
        "state_revision": store.load().revision,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

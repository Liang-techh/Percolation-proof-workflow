"""Audit the O0 weighted adapter and expose the missing output-norm factor."""
from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "agent_review_inbox/receipt-T-P4-033-O0-exact-fourier-cell-weighted-port-adapter-20260907.json"
TUPLE_RECEIPT = ROOT / "agent_review_inbox/receipt-T-P4-033-O0-constructive-exact-fourier-cell-K-Br-Cf-20260907.json"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
METRIC_SOURCE = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized" / "routeB_dense_Mq/routeB_compact_port_implicit_cellwise_monotonicity_audit.py"
EXPECTED_METRIC_SHA = "E3C41F30BDDDB2FBAC9BB5BB651B307E81F21D210BC07C390CB1AC48B7C3C9A4"
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()), "sha256": sha(path)}


def frac(value: str) -> Fraction:
    return Fraction(value)


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    for path in (RECEIPT, TUPLE_RECEIPT, STATE, METRIC_SOURCE):
        if not path.is_file():
            raise FileNotFoundError(path)
    payload = json.loads(RECEIPT.read_text(encoding="utf-8"))
    tuple_payload = json.loads(TUPLE_RECEIPT.read_text(encoding="utf-8"))
    if payload.get("schema") != "routeb-o0-exact-fourier-cell-weighted-port-adapter-v1":
        raise ValueError("unexpected O0 weighted adapter schema")
    if payload.get("status") != "CONDITIONAL_WEIGHTED_ADAPTER_CONSTRUCTED":
        raise ValueError("unexpected O0 weighted adapter status")
    for key in ("formal_certificate_allowed", "registry_eligible", "consumes_schur_margin"):
        if payload.get("proof_boundary", {}).get(key) is not False:
            raise ValueError(f"weighted adapter is not fail-closed at {key}")
    if payload.get("source_key") != tuple_payload.get("source_key") or payload.get("state_key") != tuple_payload.get("state_key"):
        raise ValueError("weighted adapter does not use the exact tuple key")
    orientation = payload.get("orientation", {})
    if orientation.get("norm") != "induced_infinity" or orientation.get("B_one_based") != [4, 5]:
        raise ValueError("weighted adapter norm/orientation mismatch")
    metric = payload["exact_metric"]
    B11 = frac(metric["B_up"][0][0])
    B22 = frac(metric["B_up"][1][1])
    beta = frac(metric["beta"])
    s = frac(metric["s"])
    if not (B11 - beta == frac("1/15") and B22 - beta == 0 and s > 0 and s * s <= beta):
        raise ValueError("weighted metric arithmetic is not exact")
    if sha(METRIC_SOURCE) != EXPECTED_METRIC_SHA:
        raise ValueError("weighted metric source hash drifted")
    epsilon = frac(payload["input_bound"]["epsilon_R_unweighted"])
    expected_epsilon = frac(tuple_payload["regularizer_perturbation_check"]["epsilon_R_unweighted"])
    if epsilon != expected_epsilon:
        raise ValueError("weighted adapter epsilon does not match exact tuple")
    claimed = frac(payload["adapter"]["epsilon_R_weighted"])
    if claimed != epsilon / s:
        raise ValueError("weighted adapter claimed arithmetic is inconsistent")
    # The source bound is induced-infinity on a 2-vector.  A safe rational
    # conversion uses ||y||_2 <= 2 ||y||_infinity (sqrt(2) <= 2).
    safe = Fraction(2) * epsilon / s
    entry = {
        "schema_version": 1,
        "task_id": payload["task"],
        "source_agent": "codex-inbox",
        "review_status": "CONDITIONAL_METRIC_PRESENT_OUTPUT_NORM_CONVERSION_REQUIRED",
        "receipt_artifact": ref(RECEIPT),
        "tuple_receipt_artifact": ref(TUPLE_RECEIPT),
        "metric_source_artifact": ref(METRIC_SOURCE),
        "source_key": payload["source_key"],
        "state_key": payload["state_key"],
        "input_norm": "induced_infinity",
        "output_norm": "Euclidean_2",
        "metric_root_s": str(s),
        "claimed_epsilon_weighted": str(claimed),
        "safe_rational_epsilon_weighted_with_factor_2": str(safe),
        "missing_premise": "proved induced_infinity_output_to_Euclidean_2 conversion for Fin 2",
        "schur_margin_consumed": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
        "admission_status": "metric_child_only_pending_norm_conversion",
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_regularizer_semantics_bridge")
    prior = list(node.metadata.get("o0_weighted_adapter_audits", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["o0_weighted_adapter_audits"] = prior
    desired = {
        "status": entry["review_status"],
        "source_key": entry["source_key"],
        "state_key": entry["state_key"],
        "input_norm": "induced_infinity",
        "output_norm": "Euclidean_2",
        "metric_root_s": str(s),
        "claimed_epsilon_weighted": str(claimed),
        "safe_rational_epsilon_weighted_with_factor_2": str(safe),
        "output_norm_conversion": "OPEN",
        "schur_margin_consumed": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("o0_weighted_adapter") != desired:
        node.metadata["o0_weighted_adapter"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o0_weighted_adapter_audited",
            node_id=node.id,
            review_status=entry["review_status"],
            output_norm_conversion="OPEN",
            safe_factor=2,
            schur_margin_consumed=False,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_status": entry["review_status"],
        "claimed_epsilon_weighted": str(claimed),
        "safe_rational_epsilon_weighted_with_factor_2": str(safe),
        "state_revision": store.load().revision,
        "schur_margin_consumed": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

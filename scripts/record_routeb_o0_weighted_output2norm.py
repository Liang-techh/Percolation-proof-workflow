"""Admit the corrected exact-Fourier output-2 norm adapter conditionally."""
from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "agent_review_inbox/receipt-T-P4-033-O0-exact-fourier-cell-weighted-port-adapter-output-2norm-20260907.json"
TUPLE_RECEIPT = ROOT / "agent_review_inbox/receipt-T-P4-033-O0-constructive-exact-fourier-cell-K-Br-Cf-20260907.json"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.routeb_regularizer_semantics import (  # noqa: E402
    convert_routeb_infinity_port_bound_to_weighted_l2,
)
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
    for path in (RECEIPT, TUPLE_RECEIPT, STATE):
        if not path.is_file():
            raise FileNotFoundError(path)
    payload = json.loads(RECEIPT.read_text(encoding="utf-8"))
    tuple_payload = json.loads(TUPLE_RECEIPT.read_text(encoding="utf-8"))
    if payload.get("schema") != "routeb-o0-exact-fourier-cell-weighted-port-adapter-output-2norm-v1":
        raise ValueError("unexpected corrected weighted adapter schema")
    if payload.get("status") != "CONDITIONAL_WEIGHTED_OUTPUT_2NORM_ADAPTER_CONSTRUCTED":
        raise ValueError("unexpected corrected weighted adapter status")
    boundary = payload.get("boundary", {})
    for key in ("exact_fourier_one_cell_only", "deployed_float64_q_nonzero_binding", "global_coverage", "schur_margin_consumed", "formal_certificate_allowed", "registry_eligible"):
        expected = True if key == "exact_fourier_one_cell_only" else False
        if boundary.get(key) is not expected:
            raise ValueError(f"corrected adapter boundary mismatch at {key}")
    if payload.get("source_key") != tuple_payload.get("source_key") or payload.get("state_key") != tuple_payload.get("state_key"):
        raise ValueError("corrected adapter key mismatch")
    conversion = payload["exact_output_conversion"]
    if conversion.get("dimension_output") != 2 or conversion.get("rational_factor") != "2":
        raise ValueError("corrected adapter lacks the explicit Fin 2 factor")
    epsilon = frac(payload["input_bound"]["epsilon_R_infinity"])
    expected_epsilon = frac(tuple_payload["regularizer_perturbation_check"]["epsilon_R_unweighted"])
    if epsilon != expected_epsilon:
        raise ValueError("corrected adapter input bound differs from exact tuple")
    s = frac(payload["metric"]["s"])
    claimed = frac(conversion["epsilon_R_2_weighted"])
    if claimed != 2 * epsilon / s or conversion.get("arithmetic_exact") is not True:
        raise ValueError("corrected adapter epsilon arithmetic is invalid")
    model = convert_routeb_infinity_port_bound_to_weighted_l2(
        epsilon, Fraction(2), s,
        source_key=payload["source_key"], metric_source_key=payload["source_key"],
        output_norm_conversion_proven=True, metric_lower_bound_proven=True,
    )
    if model.weighted_l2_bound != claimed or model.status != "CONDITIONAL_INFINITY_TO_L2_WEIGHTED_BOUND":
        raise ValueError("corrected adapter does not match workflow math API")
    entry = {
        "schema_version": 1,
        "task_id": payload["task"],
        "source_agent": "codex-inbox",
        "review_status": payload["status"],
        "receipt_artifact": ref(RECEIPT),
        "tuple_receipt_artifact": ref(TUPLE_RECEIPT),
        "source_key": payload["source_key"],
        "state_key": payload["state_key"],
        "input_norm": "induced_infinity",
        "output_norm": "Euclidean_2",
        "output_norm_factor": "2",
        "metric_root_s": str(s),
        "epsilon_R_2_weighted": str(claimed),
        "metric_proven": True,
        "output_norm_conversion_proven": True,
        "exact_fourier_one_cell_only": True,
        "schur_margin_consumed": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
        "admission_status": "conditional_exact_fourier_weighted_child",
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_regularizer_semantics_bridge")
    prior = list(node.metadata.get("o0_weighted_output2norm_adapters", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["o0_weighted_output2norm_adapters"] = prior
    desired = {
        "status": payload["status"],
        "source_key": payload["source_key"],
        "state_key": payload["state_key"],
        "output_norm_factor": "2",
        "metric_root_s": str(s),
        "epsilon_R_2_weighted": str(claimed),
        "output_norm_conversion": "PROVED_BY_RECEIPT_PREMISE",
        "exact_fourier_one_cell_only": True,
        "schur_margin_consumed": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("o0_weighted_output2norm_adapter") != desired:
        node.metadata["o0_weighted_output2norm_adapter"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o0_weighted_output2norm_adapter_recorded",
            node_id=node.id,
            review_status=payload["status"],
            output_norm_factor=2,
            exact_fourier_one_cell_only=True,
            schur_margin_consumed=False,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_status": payload["status"],
        "epsilon_R_2_weighted": str(claimed),
        "state_revision": store.load().revision,
        "schur_margin_consumed": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

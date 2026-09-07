"""Check semantic consistency across the Route-B P4 port adapters.

This is a workflow lint, not a mathematical or Lean proof.  It catches
notation/metric drift before an agent receipt is attached to the wrong
consumer theorem.
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from percolation_workflow.store import StateStore


STATE = ROOT / "artifacts/routeb_6dof/state.json"


def audit_state() -> dict[str, object]:
    state = StateStore(STATE).load()
    by_name = {node.name: node for node in state.nodes.values()}
    required = {
        "P4.residual_port_frobenius_bound",
        "P4.weighted_frobenius_port_energy_bridge",
        "P4.combined_schur_port_energy_adapter",
        "P4.residual_schur_pmi",
    }
    errors: list[str] = []
    missing = sorted(required - set(by_name))
    if missing:
        errors.extend(f"missing_node:{name}" for name in missing)
    if errors:
        return {"status": "FAIL", "errors": errors,
                "proof_boundary": "workflow lint only"}

    port = by_name["P4.residual_port_frobenius_bound"]
    weighted = by_name["P4.weighted_frobenius_port_energy_bridge"]
    combined = by_name["P4.combined_schur_port_energy_adapter"]
    pmi = by_name["P4.residual_schur_pmi"]
    weighted_contract = weighted.metadata.get("mathematical_contract", {})
    combined_contract = combined.metadata.get("mathematical_contract", {})
    consumer = port.metadata.get("consumer_interface", {})
    source_binding = port.metadata.get("source_binding_receipt", {})

    checks = {
        "weighted_rho_is_squared": "rho_F^2" in weighted_contract.get("rho_semantics", ""),
        "combined_rho_is_squared": "rho_F^2" in combined_contract.get("rho_semantics", ""),
        "combined_energy_is_A_up": "A_up" in combined_contract.get("energy_symbol", ""),
        "weighted_binds_B_up": "B_up" in weighted_contract.get("routeb_binding", ""),
        "port_provides_squared_raw_budget": "rho_F^2" in consumer.get("provided_quantity", ""),
        "port_uses_B_up_normalization": "B_up" in consumer.get("source_map", ""),
        "combined_is_consumed_by_residual_pmi": combined.id in pmi.dependencies,
        "port_does_not_wait_for_combined": combined.id not in port.dependencies,
        "source_binding_receipt_is_fail_closed": (
            source_binding.get("status") ==
            "SOURCE_AND_NOMINAL_BRIDGE_PASS_BINDING_OPEN"
            and source_binding.get("formal_certificate_allowed") is False
            and source_binding.get("registry_eligible") is False
        ),
        "source_binding_preserves_force_kc_scale": (
            source_binding.get("force_coordinate_kc") == ["q5/100", "q4/200"]
        ),
        "source_binding_requires_actual_remote_term": (
            source_binding.get("required_remote_term") == "M_BD(q) * a_D"
        ),
        "global_gate_closed_only_explicitly": state.global_closure_report()["formal_certificate_allowed"] is False,
    }
    errors.extend(f"failed:{name}" for name, ok in checks.items() if not ok)
    result = {
        "state": str(STATE),
        "revision": state.revision,
        "checks": checks,
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
        "registry": len(state.registry),
        "proof_boundary": "workflow lint only; no Lean, source, coverage, or registry admission",
    }
    return result


def main() -> int:
    result = audit_state()
    print(result)
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

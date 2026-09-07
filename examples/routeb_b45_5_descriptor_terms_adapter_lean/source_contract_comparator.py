"""Focused, read-only comparator for the B45-5 force-scale source seam.

This is an anchor comparator, not a DH dynamics proof.  It deliberately reports
the lifted literal/inertia binding separately from deployed-tau equivalence.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path


EXPECTED = {
    "deployed_sha256": "aebe6db09b2d943448c5d701631109db a8f5eeb070cc66593e5dbaca26485936".replace(" ", ""),
    "lifted_sha256": "0fcf733144b3d7b1b08f328fe4ad24477057c56976f0ef53633c450d8fc4729d",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def anchor(lines: list[str], needle: str) -> dict[str, object]:
    hits = [i + 1 for i, line in enumerate(lines) if needle in line]
    return {"needle": needle, "lines": hits, "pass": bool(hits)}


def main() -> int:
    workflow = Path(__file__).resolve().parents[2]
    outer = workflow.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
    deployed_path = outer / "robot_final" / "dhport_lib.jl"
    lifted_path = outer / "routeB_dense_Mq" / "routeB_fourier_lifted_descriptor_model.jl"
    lean_path = workflow / "examples" / "routeb_b45_5_residual_decomposition_lean" / "ResidualDecomposition.lean"
    adapter_path = Path(__file__).with_name("DescriptorTermsAdapter.lean")

    deployed = deployed_path.read_text(encoding="utf-8").splitlines()
    lifted = lifted_path.read_text(encoding="utf-8").splitlines()
    lean = lean_path.read_text(encoding="utf-8")
    adapter = adapter_path.read_text(encoding="utf-8")

    deployed_tau = anchor(deployed, "tau = -Kp .* q - (Kd + b_fr) .* dq + G0v + (gw_coef .* I_val) .* w")
    lifted_anchors = [
        anchor(lifted, "Ival = Q[1, Q(3, 5), Q(7, 20), Q(1, 5), Q(1, 10), Q(1, 20)]"),
        anchor(lifted, "Q(1, 20) * q[5]"),
        anchor(lifted, "Q(1, 20) * q[4]"),
        anchor(lifted, "l4_expr = Ival[4] * f4"),
        anchor(lifted, "l5_expr = Ival[5] * f5"),
    ]
    lean_statement = [
        "theorem forceScaleKc_eq_rhoKc (q : Vec2) :",
        "    forceScaleKc q = rhoKc q := by",
    ]
    statement_pass = all(line in lean for line in lean_statement)
    adapter_seam_pass = all(
        needle in adapter
        for needle in (
            "theorem blockResidual_eq_descriptorResidualTotal_of_source_comparator",
            "(hforceBinding : sourceBlockForce = expectedSourceForce q v w t)",
            "(hblockDescriptor : sourceBlockForce = sourceDescriptorRhs t)",
        )
    )

    coefficient_pass = (
        Fraction(1, 20) * Fraction(1, 5) == Fraction(1, 100)
        and Fraction(1, 20) * Fraction(1, 10) == Fraction(1, 200)
    )
    lifted_pass = all(item["pass"] for item in lifted_anchors) and coefficient_pass
    hashes_pass = sha256(deployed_path).lower() == EXPECTED["deployed_sha256"] and sha256(lifted_path).lower() == EXPECTED["lifted_sha256"]

    result = {
        "comparator": "routeb_b45_5_force_scale_source_contract_v1",
        "statement_comparator": "PASS" if statement_pass else "FAIL",
        "adapter_premise_surface": "PASS" if adapter_seam_pass else "FAIL",
        "lifted_literal_inertia_anchors": "PASS" if lifted_pass else "FAIL",
        "source_hash_binding": "PASS" if hashes_pass else "FAIL",
        "derived_force_coefficients": {"q5": "1/100", "q4": "1/200", "pass": coefficient_pass},
        "deployed_tau_formula_anchor": deployed_tau,
        "deployed_tau_equivalence": "NOT_CLAIMED_OPEN",
        "source_binding_status": "ANCHOR_PASS_DH_EXECUTION_BINDING_OPEN" if statement_pass and adapter_seam_pass and lifted_pass and hashes_pass else "REJECTED",
        "paths": {"deployed": str(deployed_path), "lifted": str(lifted_path), "lean": str(lean_path), "adapter": str(adapter_path)},
        "sha256": {"deployed": sha256(deployed_path), "lifted": sha256(lifted_path), "lean": sha256(lean_path), "adapter": sha256(adapter_path)},
        "unresolved": [
            "no sourceBlockForce = expectedSourceForce witness was produced for a concrete Julia runtime state",
            "no sourceBlockForce = sourceDescriptorRhs witness was produced for the deployed solve",
            "no Float64-to-real, finite-difference, or matrix-solve equivalence was claimed",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["source_binding_status"] != "REJECTED" else 1


if __name__ == "__main__":
    raise SystemExit(main())

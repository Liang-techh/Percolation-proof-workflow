"""Small exact Fraction audit for the known a1=0 terminal obstruction.

No LP, trajectory, scan, source download, or registry/state mutation.
The literals below are the already-known exact witness values; this script
checks the first-order floor and the returned a1=0 tail at one predeclared
static point.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import sys


def main(run_dir: str) -> None:
    run = Path(run_dir)
    E = F(
        "7954729780571525062950308308715457359162746863876688481/"
        "2139693685849290060237084157997244412955032963896020129690764194800"
    )
    W0 = F(2002229, 9600000000)
    W0dot = F(-29, 8000)
    rho = F(1, 20)
    tau = F(1, 100)
    a8 = F(6995146470641, 1000000000000)
    a1 = F(0)

    # Source residual factor C=(21/25000)*rho^2*e1 and exact Gram factor.
    force_factor = F(21, 25000)
    gram_e1 = F(
        "40585356023324107464032185248548251832462994203452492250000000000/"
        "48143107931609026355334393554937999291488241687660452918042194383"
    )
    assert E == force_factor**2 * rho**4 * gram_e1

    f = a8 * tau**8
    fp = -8 * a8 * tau**7
    vdot = fp * W0 + f * W0dot
    total = E + vdot
    a1_floor = E / W0
    available = F(1) - F(835965494010387, 2500000000000000)

    assert E > 0
    assert W0 > 0
    assert total > 0
    assert a1_floor > 0
    assert E < available  # arithmetic only; not a uniform feasibility claim

    result = {
        "status": "BOUNDED_EXACT_A1_POSITIVE_SUPPLY_AUDIT",
        "point": {"rho": str(rho), "tau": str(tau), "a1": str(a1)},
        "residual_cost_E": str(E),
        "W0": str(W0),
        "W0dot": str(W0dot),
        "candidate_a8": str(a8),
        "candidate_f": str(f),
        "candidate_fprime": str(fp),
        "candidate_Vdot": str(vdot),
        "candidate_cost_plus_Vdot": str(total),
        "required_a1_at_tau_zero": str(a1_floor),
        "required_a1_at_tau_zero_display": float(a1_floor),
        "initial_budget_allowance_literal": str(available),
        "interpretation": (
            "The known a1=0 tail has positive cost+Vdot at one static terminal "
            "source point. This rejects that zero-supply candidate only."
        ),
        "uniform_positive_supply_certified": False,
        "feasibility_claim": False,
        "J_le_one_claim": False,
        "solver_calls": 0,
        "trajectory_runs": 0,
        "scan_runs": 0,
    }
    (run / "results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("EXACT_A1_POSITIVE_SUPPLY_AUDIT_PASS")
    print(f"COST_PLUS_VDOT={total} DISPLAY={float(total)}")
    print(f"A1_TERMINAL_FLOOR={a1_floor} DISPLAY={float(a1_floor)}")
    print("NO_FEASIBILITY_OR_J1_CLAIM")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) == 2 else ".")

"""Exact rational principal-row interface; not a source or admission checker.

Only standard-library arithmetic. No source loading, solver, Lean or file writes.
Passing checks concerns supplied rational tuples, never runtime/trajectory truth.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, replace
from fractions import Fraction as Q

Vec2 = tuple[Q, Q]


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def rational_values(*values: Q) -> None:
    require(all(type(x) is Q for x in values), "exact Fraction values required")


def pair(value: Vec2) -> None:
    require(type(value) is tuple and len(value) == 2, "two-coordinate tuple required")
    rational_values(*value)


@dataclass(frozen=True)
class PrincipalPoint:
    # A=[[a,b],[b,c]]; p includes remote forcing, z includes full actual defect.
    a: Q
    b: Q
    c: Q
    u: Vec2
    h: Vec2
    v: Q
    p: Vec2
    z: Vec2
    nu: Vec2

    def __post_init__(self) -> None:
        rational_values(self.a, self.b, self.c, self.v)
        for value in (self.u, self.h, self.p, self.z, self.nu):
            pair(value)

    def complete_rhs(self) -> Vec2:
        return tuple(self.p[i] + self.z[i] - self.h[i] * self.v for i in range(2))

    def apply_A(self) -> Vec2:
        return (self.a * self.u[0] + self.b * self.u[1],
                self.b * self.u[0] + self.c * self.u[1])

    def determinant(self) -> Q:
        return self.a * self.c - self.b * self.b

    def numerator(self) -> Q:
        f1, f2 = self.complete_rhs()
        return self.nu[0] * (self.c * f1 - self.b * f2) + self.nu[1] * (self.a * f2 - self.b * f1)

    def observable(self) -> Q:
        return self.nu[0] * self.u[0] + self.nu[1] * self.u[1]

    def check_rows(self) -> None:
        require(self.apply_A() == self.complete_rhs(), "principal source-row premise fails")

    def check_identity(self) -> None:
        self.check_rows()
        require(self.determinant() * self.observable() == self.numerator(), "adjugate identity fails")


def check_positive_packet(point: PrincipalPoint, delta: Q, radius: Q, cap: Q) -> dict:
    """Check a single rational point, not quantified SameCellEvidence."""
    rational_values(delta, radius, cap)
    point.check_identity()
    require(delta > 0, "positive denominator floor required")
    require(delta <= point.determinant(), "floor exceeds this determinant")
    require(abs(point.numerator()) <= radius, "complete signed numerator exceeds radius")
    require(radius <= delta * cap, "rational packet gate fails")
    require(abs(point.observable()) <= cap, "observable conclusion fails")
    return {"rational_point_pass": True, "source_bound": False,
            "cell_coverage_verified": False, "runtime_verified": False,
            "lean_executed": False, "registry_eligible": False}


def check_defect_split(z: Vec2, solve: Vec2, model: Vec2) -> None:
    for value in (z, solve, model):
        pair(value)
    require(z == tuple(solve[i] + model[i] for i in range(2)), "solve/model defect split fails")


def self_test() -> dict:
    point = PrincipalPoint(Q(2), Q(1), Q(3), (Q(1), Q(-2)),
                           (Q(3), Q(-1)), Q(2), (Q(11, 2), Q(-25, 4)),
                           (Q(1, 2), Q(-3, 4)), (Q(2), Q(-1)))
    result = check_positive_packet(point, Q(5), Q(20), Q(4))
    require(point.complete_rhs() == (Q(0), Q(-5)), "complete RHS regression")
    require(point.numerator() == 20 and point.observable() == 4, "signed calculation regression")
    check_defect_split(point.z, (Q(1, 4), Q(-1, 2)), (Q(1, 4), Q(-1, 4)))
    singular = PrincipalPoint(Q(1), Q(1), Q(1), (Q(1), Q(-1)),
                              (Q(0), Q(0)), Q(0), (Q(0), Q(0)),
                              (Q(0), Q(0)), (Q(1), Q(0)))
    singular.check_identity()  # identity needs no invertibility; cap gate does.
    negatives = {
        "drop_joint6_coupling": lambda: replace(point, h=(Q(0), Q(0))).check_rows(),
        "drop_physical_defect": lambda: replace(point, z=(Q(0), Q(0))).check_rows(),
        "omit_model_defect": lambda: check_defect_split(point.z, (Q(1, 4), Q(-1, 2)), (Q(0), Q(0))),
        "wrong_determinant_floor": lambda: check_positive_packet(point, Q(6), Q(20), Q(4)),
        "underbound_numerator": lambda: check_positive_packet(point, Q(5), Q(19), Q(4)),
        "insufficient_cap": lambda: check_positive_packet(point, Q(5), Q(20), Q(3)),
        "singular_positive_gate": lambda: check_positive_packet(singular, Q(1), Q(0), Q(1)),
        "float_input": lambda: replace(point, v=2.0),
    }
    rejected = []
    for name, action in negatives.items():
        try:
            action()
        except ValueError:
            rejected.append(name)
        else:
            raise RuntimeError(f"negative control accepted: {name}")
    return {**result, "complete_rhs": list(map(str, point.complete_rhs())),
            "determinant": str(point.determinant()), "numerator": str(point.numerator()),
            "negative_controls_rejected": rejected,
            "singular_identity_pass": True,
            "scope": "synthetic_rational_points_only_not_physical_counterexamples"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", required=True)
    parser.parse_args()
    print(json.dumps(self_test(), indent=2))

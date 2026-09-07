"""Emit one exact rational Route-B receipt leaf as a Lean adapter target.

This is intentionally a one-leaf bridge.  It validates the named coordinate
order and parses the recorded decimal strings through Fraction before emitting
exact ℚ literals.  It never claims partition completeness or source/runtime
soundness.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path


COORDINATES = (
    "q1", "q2", "q3", "q4", "q5", "q6",
    "dq1", "dq2", "dq3", "dq4", "dq5", "dq6", "w",
)
COORD_CONSTRUCTORS = tuple(name for name in COORDINATES)


def _frac(value: object, field: str) -> Fraction:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a rational/decimal string")
    try:
        return Fraction(value)
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{field} is not an exact rational string") from exc


def _lean_fraction(value: Fraction) -> str:
    return f"({value.numerator} / {value.denominator} : ℚ)"


def read_leaf(path: Path) -> tuple[dict, str]:
    raw = path.read_bytes()
    document = json.loads(raw.decode("utf-8"))
    candidate = document.get("p3_candidate")
    if not isinstance(candidate, dict):
        raise ValueError("p3_candidate is missing")
    if candidate.get("cell_id") != "1":
        raise ValueError("this minimal adapter is pinned to cell_id '1'")
    if tuple(candidate.get("coordinate_order", ())) != COORDINATES:
        raise ValueError("coordinate_order does not match canonical 13-coordinate order")
    box = candidate.get("box")
    if not isinstance(box, dict):
        raise ValueError("p3_candidate.box is missing")
    endpoints: list[tuple[Fraction, Fraction]] = []
    for coordinate in COORDINATES:
        interval = box.get(coordinate)
        if not isinstance(interval, dict):
            raise ValueError(f"box.{coordinate} is missing")
        lo, hi = _frac(interval.get("lo"), f"box.{coordinate}.lo"), _frac(interval.get("hi"), f"box.{coordinate}.hi")
        if lo > hi:
            raise ValueError(f"box.{coordinate} has lo > hi")
        endpoints.append((lo, hi))
    return {"id": 1, "endpoints": endpoints}, hashlib.sha256(raw).hexdigest()


def emit(leaf: dict, input_sha256: str) -> str:
    endpoints = leaf["endpoints"]
    lo = ",\n      ".join(_lean_fraction(pair[0]) for pair in endpoints)
    hi = ",\n      ".join(_lean_fraction(pair[1]) for pair in endpoints)
    order = ", ".join(f". {name}" for name in COORD_CONSTRUCTORS)
    return f'''import DownstreamTest.Theta2ExactRealApi

set_option autoImplicit false

noncomputable section

namespace RouteBTheta2ReceiptAdapter

open RouteBTheta2ExactRealApi

inductive ReceiptCoord
  | q1 | q2 | q3 | q4 | q5 | q6
  | dq1 | dq2 | dq3 | dq4 | dq5 | dq6 | w
  deriving DecidableEq

abbrev ReceiptState13 := Fin 13 → ℚ

structure ReceiptLeaf13 where
  leafId : Nat
  coordinateOrder : Fin 13 → ReceiptCoord
  lo : ReceiptState13
  hi : ReceiptState13
  ordered : ∀ i, lo i ≤ hi i

def canonicalOrder : Fin 13 → ReceiptCoord := ![ReceiptCoord.q1, ReceiptCoord.q2,
  ReceiptCoord.q3, ReceiptCoord.q4, ReceiptCoord.q5, ReceiptCoord.q6,
  ReceiptCoord.dq1, ReceiptCoord.dq2, ReceiptCoord.dq3, ReceiptCoord.dq4,
  ReceiptCoord.dq5, ReceiptCoord.dq6, ReceiptCoord.w]

def receiptLeaf1 : ReceiptLeaf13 where
  leafId := 1
  coordinateOrder := canonicalOrder
  lo := ![
      {lo}
    ]
  hi := ![
      {hi}
    ]
  ordered := by
    intro i
    fin_cases i <;> norm_num

def ReceiptLeaf13.toRectBox (r : ReceiptLeaf13) : RectBox13 :=
  {{
    lo := fun i => (r.lo i : ℝ)
    hi := fun i => (r.hi i : ℝ)
    ordered := by
      intro i
      exact_mod_cast r.ordered i
  }}

theorem receipt_leaf1_id : receiptLeaf1.leafId = 1 := rfl

theorem receipt_leaf1_coordinate_order :
    receiptLeaf1.coordinateOrder = canonicalOrder := rfl

theorem receipt_leaf1_q2_lower :
    -(3 / 20 : ℝ) ≤ (receiptLeaf1.lo q2Index : ℝ) := by
  norm_num [receiptLeaf1, canonicalOrder, q2Index]

theorem receipt_leaf1_q2_upper :
    (receiptLeaf1.hi q2Index : ℝ) ≤ (3 / 20 : ℝ) := by
  norm_num [receiptLeaf1, canonicalOrder, q2Index]

theorem receipt_leaf1_in_rectbox {{x : State13}}
    (hx : InRectBox (receiptLeaf1.toRectBox) x) :
    InRectBox (receiptLeaf1.toRectBox) x := hx

theorem receipt_leaf1_theta2_exact_real_interval {{x : State13}}
    (hx : InRectBox (receiptLeaf1.toRectBox) x) :
    theta2 (x q2Index) + Real.pi / 2 = x q2Index ∧
    (-1 : ℝ) ≤ Real.sin (theta2 (x q2Index)) ∧
      Real.sin (theta2 (x q2Index)) ≤ -(791 / 800 : ℝ) ∧
    -(2409 / 16000 : ℝ) ≤ Real.cos (theta2 (x q2Index)) ∧
      Real.cos (theta2 (x q2Index)) ≤ 2409 / 16000 := by
  exact box_q2_theta2_exact_real_interval hx
    receipt_leaf1_q2_lower receipt_leaf1_q2_upper

#check receipt_leaf1_theta2_exact_real_interval
#print axioms receipt_leaf1_theta2_exact_real_interval

end RouteBTheta2ReceiptAdapter

-- receipt input sha256: {input_sha256}
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    leaf, digest = read_leaf(args.input)
    args.output.write_text(emit(leaf, digest), encoding="utf-8")
    print(json.dumps({"leaf_id": leaf["id"], "input_sha256": digest, "output": str(args.output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

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
import re
from fractions import Fraction
from pathlib import Path


COORDINATES = (
    "q1", "q2", "q3", "q4", "q5", "q6",
    "dq1", "dq2", "dq3", "dq4", "dq5", "dq6", "w",
)
COORD_CONSTRUCTORS = tuple(name for name in COORDINATES)
HANDOFF_SCHEMA = "routeb-theta2-leaf-handoff-v1"
HANDOFF_STATUS = "ENDPOINT_PROVENANCE_ONLY"


def _frac(value: object, field: str) -> Fraction:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a rational/decimal string")
    try:
        return Fraction(value)
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{field} is not an exact rational string") from exc


def _lean_fraction(value: Fraction) -> str:
    return f"({value.numerator} / {value.denominator} : ℚ)"


def _read_vector(document: dict, key: str) -> list[Fraction]:
    values = document.get(key)
    if not isinstance(values, list) or len(values) != len(COORDINATES):
        raise ValueError(f"{key} must contain exactly 13 entries")
    return [_frac(value, f"{key}[{index}]") for index, value in enumerate(values)]


def _read_handoff(document: dict) -> tuple[dict, str]:
    if document.get("schema") != HANDOFF_SCHEMA:
        raise ValueError("unsupported handoff schema")
    if document.get("authority_status") != HANDOFF_STATUS:
        raise ValueError(
            "this adapter accepts only ENDPOINT_PROVENANCE_ONLY; "
            "an authoritative dynamic leaf needs a newer source-bound schema"
        )
    if document.get("claim_boundary") != (
        "exact rational box endpoint and point-in-box transport only; "
        "no trajectory, Float64, libm, DAG, or coverage claim"
    ):
        raise ValueError("claim_boundary is missing or does not match the fail-closed handoff contract")
    if tuple(document.get("coordinate_order", ())) != COORDINATES:
        raise ValueError("coordinate_order does not match canonical 13-coordinate order")
    leaf_id = document.get("leaf_id")
    if not isinstance(leaf_id, str) or not re.fullmatch(r"[1-9][0-9]*", leaf_id):
        raise ValueError("leaf_id must be a positive decimal string")
    lo = _read_vector(document, "box_lo")
    hi = _read_vector(document, "box_hi")
    for index, (lower, upper) in enumerate(zip(lo, hi)):
        if lower > upper:
            raise ValueError(f"box_lo[{index}] is greater than box_hi[{index}]")

    source = document.get("source")
    if not isinstance(source, dict):
        raise ValueError("source is missing")
    source_path = source.get("receipt_path")
    source_hash = source.get("receipt_sha256")
    leaf_pointer = source.get("leaf_pointer")
    if not isinstance(source_path, str) or not source_path:
        raise ValueError("source.receipt_path is missing")
    if not isinstance(source_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", source_hash):
        raise ValueError("source.receipt_sha256 must be a lowercase SHA-256")
    if not isinstance(leaf_pointer, str) or not leaf_pointer:
        raise ValueError("source.leaf_pointer is missing")

    witness = document.get("witness")
    if not isinstance(witness, dict) or witness.get("kind") != "lower_corner":
        raise ValueError("witness.kind must be lower_corner")
    witness_point = _read_vector(witness, "point")
    if witness_point != lo:
        raise ValueError("lower_corner witness.point must equal box_lo exactly")

    return {
        "id": int(leaf_id),
        "endpoints": list(zip(lo, hi)),
        "witness": witness_point,
        "handoff_status": HANDOFF_STATUS,
        "source_path": source_path,
        "source_hash": source_hash,
        "leaf_pointer": leaf_pointer,
    }, hashlib.sha256(json.dumps(document, ensure_ascii=False, indent=2).encode("utf-8")).hexdigest()


def read_leaf(path: Path) -> tuple[dict, str]:
    raw = path.read_bytes()
    document = json.loads(raw.decode("utf-8"))
    if document.get("schema") == HANDOFF_SCHEMA:
        # The handoff digest is over the bytes consumed by the generator, just
        # like the legacy branch below.  Keep the parsed-document hash only as
        # a diagnostic if a caller supplied non-canonical JSON formatting.
        leaf, _ = _read_handoff(document)
        return leaf, hashlib.sha256(raw).hexdigest()
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
    witness = leaf.get("witness", [pair[0] for pair in endpoints])
    witness_code = ",\n      ".join(_lean_fraction(value) for value in witness)
    order = ", ".join(f". {name}" for name in COORD_CONSTRUCTORS)
    handoff_comment = ""
    if leaf.get("handoff_status"):
        handoff_comment = (
            f"-- handoff status: {leaf['handoff_status']}\n"
            f"-- source receipt: {leaf['source_path']}\n"
            f"-- source leaf pointer: {leaf['leaf_pointer']}\n"
            f"-- source receipt sha256: {leaf['source_hash']}\n"
        )
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

def receiptLeaf1Witness : State13 := ![
      {witness_code}
    ]

theorem receipt_leaf1_witness_in_rectbox :
    InRectBox (receiptLeaf1.toRectBox) receiptLeaf1Witness := by
  intro i
  fin_cases i <;> norm_num [InRectBox, receiptLeaf1, ReceiptLeaf13.toRectBox,
    receiptLeaf1Witness]

def BoxSubset (child parent : RectBox13) : Prop :=
  ∀ i, parent.lo i ≤ child.lo i ∧ child.hi i ≤ parent.hi i

theorem in_rectbox_parent_of_child
    {{parent child : RectBox13}} {{x : State13}}
    (hchild : BoxSubset child parent)
    (hx : InRectBox child x) :
    InRectBox parent x := by
  intro i
  have hsubset := hchild i
  have hbox := hx i
  exact ⟨hsubset.1.trans hbox.1, hbox.2.trans hsubset.2⟩

def CoverageJoin2 (parent child sibling : RectBox13) : Prop :=
  BoxSubset child parent ∧
  BoxSubset sibling parent ∧
  ∀ x, InRectBox parent x → InRectBox child x ∨ InRectBox sibling x

theorem coverage_join2_child_or_sibling
    {{parent child sibling : RectBox13}} {{x : State13}}
    (hjoin : CoverageJoin2 parent child sibling)
    (hx : InRectBox parent x) :
    InRectBox child x ∨ InRectBox sibling x :=
  hjoin.2.2 x hx

theorem receipt_leaf1_witness_parent_lift
    {{parent : RectBox13}}
    (hparent : BoxSubset (receiptLeaf1.toRectBox) parent) :
    InRectBox parent receiptLeaf1Witness :=
  in_rectbox_parent_of_child hparent receipt_leaf1_witness_in_rectbox

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
#check receipt_leaf1_witness_in_rectbox
#print axioms receipt_leaf1_witness_in_rectbox
#check receipt_leaf1_witness_parent_lift
#print axioms receipt_leaf1_witness_parent_lift
#check coverage_join2_child_or_sibling
#print axioms coverage_join2_child_or_sibling

end RouteBTheta2ReceiptAdapter

{handoff_comment}
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

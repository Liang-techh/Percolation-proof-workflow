import P8ContractAdapter
import Mathlib.Tactic

/-!
# P8 first-12 ramp-elimination adapter

Formalization follow-up for `T-P8-008` (mathematics by 古月方源).

This file proves only the source-independent algebraic seam between the literal
13-state source interface and the 14-state ramp lift.  It intentionally binds
only source coordinates `0..11`; the source tail remains a separate coordinate
with its own zero-tail premise.  No Julia source authentication, ODE existence,
interval enclosure, flowpipe coverage, admission, or registry mutation is
claimed here.
-/

namespace RouteBP8First12Adapter

set_option autoImplicit false

open RouteBP8PicardStep RouteBP8ContractAdapter

abbrev State12 := BaseState12

/-- Slot 12 (zero-based) of the 13-state source is its literal `w` tail. -/
def wSlot13 : Fin 13 := ⟨12, by omega⟩

/-- Canonical embedding of a mechanical coordinate into the 13-state source. -/
def embed12_13 (i : Fin 12) : Fin 13 := ⟨i.val, by omega⟩

/-- Canonical embedding of a mechanical coordinate into the 14-state ramp lift. -/
def embed12_14 (i : Fin 12) : Fin 14 := ⟨i.val, by omega⟩

/-- Pack a 12-state mechanical vector together with one scalar source tail. -/
def pack13 (m : State12) (w : ℝ) : State13 := fun i =>
  match i.val with
  | 0 => m ⟨0, by omega⟩
  | 1 => m ⟨1, by omega⟩
  | 2 => m ⟨2, by omega⟩
  | 3 => m ⟨3, by omega⟩
  | 4 => m ⟨4, by omega⟩
  | 5 => m ⟨5, by omega⟩
  | 6 => m ⟨6, by omega⟩
  | 7 => m ⟨7, by omega⟩
  | 8 => m ⟨8, by omega⟩
  | 9 => m ⟨9, by omega⟩
  | 10 => m ⟨10, by omega⟩
  | 11 => m ⟨11, by omega⟩
  | 12 => w
  | _ => 0

/-- Project the source state to its twelve mechanical coordinates. -/
def proj12_13 (x : State13) : State12 := fun i => x (embed12_13 i)

/-- Project a ramp-lifted state to its twelve mechanical coordinates. -/
def proj12_14 (z : State14) : State12 := fun i => z (embed12_14 i)

/-- The source-authenticated part of an arbitrary 13-state source field. -/
def sourceMechanical (S : VectorField13) (x : State13) : State12 :=
  proj12_13 (S x)

/-- Eliminate the ramp tail by the exact substitution `w = c*t`. -/
def explicitMechanical (S : VectorField13) (c t : ℝ) (m : State12) : State12 :=
  sourceMechanical S (pack13 m (c * t))

/-- Repair only the source tail derivative, preserving all twelve mechanical outputs. -/
def repair13 (S : VectorField13) (c : ℝ) (x : State13) : State13 :=
  pack13 (sourceMechanical S x) c

/-- The existing 14-state ramp lift forgets back to `(m, c*t)` exactly. -/
theorem forgetTail_rampLift (m : State12) (c t : ℝ) :
    forgetTail (rampLift m c t) = pack13 m (c * t) := by
  funext i
  fin_cases i <;> rfl

/-- On a ramp state, the first twelve coordinates of `timeLift` are exactly
    the explicit-time source mechanical field. -/
theorem timeLift_first12_on_ramp
    (S : VectorField13) (m : State12) (c t : ℝ) :
    proj12_14 (timeLift (fun _ x => S x) t (rampLift m c t)) =
      explicitMechanical S c t m := by
  funext i
  fin_cases i <;>
    simp [proj12_14, embed12_14, timeLift, explicitMechanical,
      sourceMechanical, proj12_13, embed12_13, forgetTail_rampLift]

/-- The two adapter-owned tail coordinates are `(w', c') = (c, 0)` on a ramp state. -/
theorem timeLift_tail_on_ramp
    (S : VectorField13) (m : State12) (c t : ℝ) :
    timeLift (fun _ x => S x) t (rampLift m c t) wSlot = c ∧
      timeLift (fun _ x => S x) t (rampLift m c t) cSlot = 0 := by
  constructor <;> rfl

/-- Repairing the tail does not alter any source-authenticated mechanical output. -/
theorem repair13_preserves_first12
    (S : VectorField13) (c : ℝ) (x : State13) :
    proj12_13 (repair13 S c x) = sourceMechanical S x := by
  funext i
  fin_cases i <;> rfl

/-- The repaired source tail is exactly the externally supplied ramp coefficient. -/
theorem repair13_tail
    (S : VectorField13) (c : ℝ) (x : State13) :
    repair13 S c x wSlot13 = c := by
  rfl

/-- At one state whose literal source tail derivative is zero, equality between
    repaired and literal source fields is possible exactly when `c = 0`. -/
theorem repair13_eq_source_at_iff_c_zero
    (S : VectorField13) (c : ℝ) (x : State13)
    (hzero : S x wSlot13 = 0) :
    repair13 S c x = S x ↔ c = 0 := by
  constructor
  · intro hEq
    have hw := congrFun hEq wSlot13
    simpa [repair13, pack13, wSlot13, hzero] using hw
  · intro hc
    subst c
    funext i
    fin_cases i <;>
      simp [repair13, pack13, sourceMechanical, proj12_13, embed12_13,
        wSlot13, hzero]

/-- If the literal source has zero tail everywhere, the whole repaired field
    equals it if and only if the ramp coefficient is zero. -/
theorem repair13_eq_source_iff_c_zero
    (S : VectorField13) (c : ℝ)
    (hzero : ∀ x : State13, S x wSlot13 = 0) :
    (fun x => repair13 S c x) = S ↔ c = 0 := by
  constructor
  · intro hEq
    let x0 : State13 := fun _ => 0
    have hx : repair13 S c x0 = S x0 := congrFun hEq x0
    exact (repair13_eq_source_at_iff_c_zero S c x0 (hzero x0)).mp hx
  · intro hc
    funext x
    exact (repair13_eq_source_at_iff_c_zero S c x (hzero x)).mpr hc

/-- Nonzero ramps therefore cannot be identified with the literal zero-tail source. -/
theorem repair13_ne_source_of_c_ne_zero
    (S : VectorField13) (c : ℝ)
    (hzero : ∀ x : State13, S x wSlot13 = 0)
    (hc : c ≠ 0) :
    (fun x => repair13 S c x) ≠ S := by
  intro hEq
  exact hc ((repair13_eq_source_iff_c_zero S c hzero).mp hEq)

#print axioms forgetTail_rampLift
#print axioms timeLift_first12_on_ramp
#print axioms timeLift_tail_on_ramp
#print axioms repair13_preserves_first12
#print axioms repair13_tail
#print axioms repair13_eq_source_at_iff_c_zero
#print axioms repair13_eq_source_iff_c_zero
#print axioms repair13_ne_source_of_c_ne_zero

end RouteBP8First12Adapter

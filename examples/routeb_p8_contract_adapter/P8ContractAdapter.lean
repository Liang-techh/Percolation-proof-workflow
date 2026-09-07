import RouteBP8PicardStep
import Mathlib.Tactic

/-!
# P8 13-to-14 contract adapter

This file records the smallest exact-real interface decision for the current
13-state source.  `zeroTailLift` models the literal source tail and is proved
not to satisfy the parent ramp premise.  `timeLift` is the conditional repair:
an abstract time-indexed 13-state field is lifted while the new `c` coordinate
drives `w`.  No source binding, interval receipt, ODE existence theorem, or
true-DH claim is made here.
-/

namespace RouteBP8ContractAdapter

set_option autoImplicit false

open RouteBP8PicardStep

abbrev State13 := Fin 13 → ℝ
abbrev VectorField13 := State13 → State13
abbrev TimeVectorField13 := ℝ → State13 → State13

def forgetTail (z : State14) : State13 := fun i => z ⟨i.val, by omega⟩

def zeroTailLift (G : VectorField13) : VectorField := fun z i =>
  match i.val with
  | 0 => G (forgetTail z) ⟨0, by omega⟩
  | 1 => G (forgetTail z) ⟨1, by omega⟩
  | 2 => G (forgetTail z) ⟨2, by omega⟩
  | 3 => G (forgetTail z) ⟨3, by omega⟩
  | 4 => G (forgetTail z) ⟨4, by omega⟩
  | 5 => G (forgetTail z) ⟨5, by omega⟩
  | 6 => G (forgetTail z) ⟨6, by omega⟩
  | 7 => G (forgetTail z) ⟨7, by omega⟩
  | 8 => G (forgetTail z) ⟨8, by omega⟩
  | 9 => G (forgetTail z) ⟨9, by omega⟩
  | 10 => G (forgetTail z) ⟨10, by omega⟩
  | 11 => G (forgetTail z) ⟨11, by omega⟩
  | 12 => 0
  | 13 => 0
  | _ => 0

theorem zeroTailLift_w (G : VectorField13) (z : State14) :
    zeroTailLift G z wSlot = 0 := by
  rfl

theorem zeroTailLift_c (G : VectorField13) (z : State14) :
    zeroTailLift G z cSlot = 0 := by
  rfl

theorem zeroTailLift_not_ramp (G : VectorField13) :
    ¬ RampRhsPremise (zeroTailLift G) := by
  intro hramp
  let z : State14 := fun i => if i = cSlot then 1 else 0
  have hw := (hramp z).1
  simp [full_rhs!, zeroTailLift, z, wSlot, cSlot] at hw

def timeLift (G : TimeVectorField13) (t : ℝ) : VectorField := fun z i =>
  match i.val with
  | 0 => G t (forgetTail z) ⟨0, by omega⟩
  | 1 => G t (forgetTail z) ⟨1, by omega⟩
  | 2 => G t (forgetTail z) ⟨2, by omega⟩
  | 3 => G t (forgetTail z) ⟨3, by omega⟩
  | 4 => G t (forgetTail z) ⟨4, by omega⟩
  | 5 => G t (forgetTail z) ⟨5, by omega⟩
  | 6 => G t (forgetTail z) ⟨6, by omega⟩
  | 7 => G t (forgetTail z) ⟨7, by omega⟩
  | 8 => G t (forgetTail z) ⟨8, by omega⟩
  | 9 => G t (forgetTail z) ⟨9, by omega⟩
  | 10 => G t (forgetTail z) ⟨10, by omega⟩
  | 11 => G t (forgetTail z) ⟨11, by omega⟩
  | 12 => z cSlot
  | 13 => 0
  | _ => 0

theorem timeLift_rampPremise (G : TimeVectorField13) (t : ℝ) :
    RampRhsPremise (timeLift G t) := by
  intro z
  constructor <;> rfl

theorem timeLift_is_conditional (G : TimeVectorField13) (t : ℝ) (z : State14) :
    timeLift G t z wSlot = z cSlot ∧ timeLift G t z cSlot = 0 := by
  exact (timeLift_rampPremise G t z)

#print axioms zeroTailLift_not_ramp
#print axioms timeLift_rampPremise

end RouteBP8ContractAdapter

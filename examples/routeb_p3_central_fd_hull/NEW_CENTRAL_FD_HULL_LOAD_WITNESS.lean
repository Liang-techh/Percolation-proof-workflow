import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# P3 assembled load-coefficient witness

This sidecar proves only the pointwise nonnegativity of an already selected
six-component load coefficient `weight[i] * squaredVelocity[i]`.  The resulting
witness is shaped for the existing pure-order consumer; no radius, cap, force,
or power theorem is rebuilt.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullLoadWitness

noncomputable section

abbrev I6 := Fin 6
abbrev Vector6 := I6 → ℝ

def assembledLoad6 (weight squaredVelocity : Vector6) : Vector6 :=
  fun i => weight i * squaredVelocity i

theorem assembledLoad6_nonneg
    (weight squaredVelocity : Vector6)
    (hweight : ∀ i, 0 ≤ weight i)
    (hsquaredVelocity : ∀ i, 0 ≤ squaredVelocity i) :
    ∀ i, 0 ≤ assembledLoad6 weight squaredVelocity i := by
  intro i
  unfold assembledLoad6
  exact mul_nonneg (hweight i) (hsquaredVelocity i)

/-- Minimal load witness expected by the pure order consumer. -/
structure PureOrderLoadWitness6 where
  load : Vector6
  load_nonneg : ∀ i, 0 ≤ load i

theorem assembled_load_witness6
    (weight squaredVelocity : Vector6)
    (hweight : ∀ i, 0 ≤ weight i)
    (hsquaredVelocity : ∀ i, 0 ≤ squaredVelocity i) :
    PureOrderLoadWitness6 :=
  { load := assembledLoad6 weight squaredVelocity
    load_nonneg := assembledLoad6_nonneg weight squaredVelocity
      hweight hsquaredVelocity }

/-! Common point/domain context is carried without changing the load proof. -/

structure LoadWitnessContext6 (D : Type*) where
  point : D
  commonDomain : D → Prop
  machine_in_common : commonDomain point
  centralFD_in_common : commonDomain point
  derivativeHull_in_common : commonDomain point
  exportCenter_in_common : commonDomain point
  weight : Vector6
  weight_nonneg : ∀ i, 0 ≤ weight i
  squaredVelocity : Vector6
  squaredVelocity_nonneg : ∀ i, 0 ≤ squaredVelocity i
  load : Vector6
  load_eq : load = assembledLoad6 weight squaredVelocity
  velocityPremise : Prop
  velocityPremise_ok : velocityPremise

theorem context_load_nonneg6
    {D : Type*} (C : LoadWitnessContext6 D) :
    ∀ i, 0 ≤ C.load i := by
  intro i
  rw [C.load_eq]
  exact assembledLoad6_nonneg C.weight C.squaredVelocity
    C.weight_nonneg C.squaredVelocity_nonneg i

theorem context_pure_order_load_witness6
    {D : Type*} (C : LoadWitnessContext6 D) :
    PureOrderLoadWitness6 :=
  { load := C.load
    load_nonneg := context_load_nonneg6 C }

end

end RouteBP3CentralFDHullLoadWitness

#print axioms RouteBP3CentralFDHullLoadWitness.assembledLoad6_nonneg
#print axioms RouteBP3CentralFDHullLoadWitness.assembled_load_witness6
#print axioms RouteBP3CentralFDHullLoadWitness.context_load_nonneg6
#print axioms RouteBP3CentralFDHullLoadWitness.context_pure_order_load_witness6

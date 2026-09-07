import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# P3 squared-velocity nonnegativity premise

This small leaf proves the real-algebra fact needed by the existing assembled
load witness: every coordinate square of an arbitrary `Fin 6` velocity is
nonnegative.  It does not redefine the load witness or assert how velocity was
obtained.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullSquaredVelocity

noncomputable section

abbrev I6 := Fin 6
abbrev Vector6 := I6 → ℝ

def squaredVelocity6 (velocity : Vector6) : Vector6 :=
  fun i => (velocity i) ^ 2

theorem squaredVelocity6_nonneg
    (velocity : Vector6) :
    ∀ i, 0 ≤ squaredVelocity6 velocity i := by
  intro i
  unfold squaredVelocity6
  exact sq_nonneg (velocity i)

/-- Generic assembled-load equality, ready to instantiate with the existing
`assembledLoad6` definition. -/
theorem assembled_load_nonneg_from_squared_velocity6
    (assembledLoad : Vector6 → Vector6 → Vector6)
    (weight velocity load : Vector6)
    (hweight : ∀ i, 0 ≤ weight i)
    (hLoadEq : ∀ i, load i =
      assembledLoad weight (squaredVelocity6 velocity) i)
    (hAssembled : ∀ weight squaredVelocity i,
      assembledLoad weight squaredVelocity i =
        weight i * squaredVelocity i) :
    ∀ i, 0 ≤ load i := by
  intro i
  rw [hLoadEq i, hAssembled]
  exact mul_nonneg (hweight i)
    (squaredVelocity6_nonneg velocity i)

structure SquaredVelocityContext6 (D : Type*) where
  point : D
  commonDomain : D → Prop
  machine_in_common : commonDomain point
  centralFD_in_common : commonDomain point
  derivativeHull_in_common : commonDomain point
  exportCenter_in_common : commonDomain point
  velocity : Vector6
  velocityPremise : Prop
  velocityPremise_ok : velocityPremise
  weight : Vector6
  weight_nonneg : ∀ i, 0 ≤ weight i
  load : Vector6
  assembledLoad : Vector6 → Vector6 → Vector6
  load_eq : ∀ i, load i =
    assembledLoad weight (squaredVelocity6 velocity) i
  assembledLoad_eq : ∀ weight squaredVelocity i,
    assembledLoad weight squaredVelocity i =
      weight i * squaredVelocity i

theorem context_load_nonneg6
    {D : Type*} (C : SquaredVelocityContext6 D) :
    ∀ i, 0 ≤ C.load i := by
  exact assembled_load_nonneg_from_squared_velocity6
    C.assembledLoad C.weight C.velocity C.load C.weight_nonneg
    C.load_eq C.assembledLoad_eq

end

end RouteBP3CentralFDHullSquaredVelocity

#print axioms RouteBP3CentralFDHullSquaredVelocity.squaredVelocity6_nonneg
#print axioms RouteBP3CentralFDHullSquaredVelocity.assembled_load_nonneg_from_squared_velocity6
#print axioms RouteBP3CentralFDHullSquaredVelocity.context_load_nonneg6

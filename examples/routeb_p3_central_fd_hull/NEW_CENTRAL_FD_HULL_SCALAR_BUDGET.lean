import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# P3 scalar budget seam after the unified derivative radius

The upstream consumer supplies a component radius `q : Fin 6 -> R` and an
inequality bounded by a weighted sum.  This sidecar compresses that sum into a
nonuniform cap budget or a single scalar cap budget.  It does not reprove the
force map, the derivative-radius monotonicity, or the weighted-power theorem.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP3CentralFDHullScalarBudget

noncomputable section

abbrev I6 := Fin 6
abbrev Vector6 := I6 → ℝ

/-- The nonnegative load coefficient multiplying a component radius. -/
def loadCoeff6 (weight velocity : Vector6) : Vector6 :=
  fun i => weight i * |velocity i|

/-- The weighted component-radius sum used by the existing consumer. -/
def weightedLoad6 (weight velocity q : Vector6) : ℝ :=
  ∑ i, loadCoeff6 weight velocity i * q i

/-- A nonuniform cap is consumed componentwise before any scalar collapse. -/
def capLoad6 (weight velocity qCap : Vector6) : ℝ :=
  ∑ i, loadCoeff6 weight velocity i * qCap i

theorem loadCoeff6_nonneg
    (weight velocity : Vector6)
    (hweight : ∀ i, 0 ≤ weight i) :
    ∀ i, 0 ≤ loadCoeff6 weight velocity i := by
  intro i
  unfold loadCoeff6
  exact mul_nonneg (hweight i) (abs_nonneg _)

theorem component_to_cap_load6
    (weight velocity q qCap : Vector6)
    (hweight : ∀ i, 0 ≤ weight i)
    (hq : ∀ i, 0 ≤ q i)
    (hqCap : ∀ i, 0 ≤ qCap i)
    (hqqCap : ∀ i, q i ≤ qCap i) :
    weightedLoad6 weight velocity q ≤ capLoad6 weight velocity qCap := by
  unfold weightedLoad6 capLoad6
  apply Finset.sum_le_sum
  intro i hi
  exact mul_le_mul_of_nonneg_left (hqqCap i)
    (loadCoeff6_nonneg weight velocity hweight i)

/-- A uniform scalar cap compresses the nonuniform cap load without square
roots or division. -/
def scalarCapLoad6 (weight velocity : Vector6) (cap : ℝ) : ℝ :=
  cap * ∑ i, loadCoeff6 weight velocity i

theorem cap_load_to_scalar6
    (weight velocity qCap : Vector6) (cap : ℝ)
    (hweight : ∀ i, 0 ≤ weight i)
    (hqCap : ∀ i, 0 ≤ qCap i)
    (hqCapScalar : ∀ i, qCap i ≤ cap) :
    capLoad6 weight velocity qCap ≤ scalarCapLoad6 weight velocity cap := by
  unfold capLoad6 scalarCapLoad6
  calc
    ∑ i, loadCoeff6 weight velocity i * qCap i ≤
        ∑ i, loadCoeff6 weight velocity i * cap := by
      apply Finset.sum_le_sum
      intro i hi
      exact mul_le_mul_of_nonneg_left (hqCapScalar i)
        (loadCoeff6_nonneg weight velocity hweight i)
    _ = cap * ∑ i, loadCoeff6 weight velocity i := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro i hi
      ring

/-! The context is explicit but the compression theorem remains agnostic about
how the velocity and domain premises were established. -/

structure ScalarBudgetContext6 (D : Type*) where
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

/-- Transitivity seam from an existing component-radius consumer to a scalar
downstream load budget. -/
theorem existing_consumer_to_scalar_budget6
    {D : Type*} (C : ScalarBudgetContext6 D)
    (consumerValue : ℝ) (q : Vector6) (budget : ℝ)
    (hConsumer : consumerValue ≤
      weightedLoad6 C.weight C.velocity q)
    (hBudget : weightedLoad6 C.weight C.velocity q ≤ budget) :
    consumerValue ≤ budget := by
  exact hConsumer.trans hBudget

theorem existing_consumer_to_scalar_cap6
    {D : Type*} (C : ScalarBudgetContext6 D)
    (consumerValue : ℝ) (q qCap : Vector6) (cap : ℝ)
    (hConsumer : consumerValue ≤
      weightedLoad6 C.weight C.velocity q)
    (hq : ∀ i, 0 ≤ q i)
    (hqCap : ∀ i, 0 ≤ qCap i)
    (hqqCap : ∀ i, q i ≤ qCap i)
    (hqCapScalar : ∀ i, qCap i ≤ cap) :
    consumerValue ≤ scalarCapLoad6 C.weight C.velocity cap := by
  have hCap : weightedLoad6 C.weight C.velocity q ≤
      capLoad6 C.weight C.velocity qCap :=
    component_to_cap_load6 C.weight C.velocity q qCap
      C.weight_nonneg hq hqCap hqqCap
  have hScalar : capLoad6 C.weight C.velocity qCap ≤
      scalarCapLoad6 C.weight C.velocity cap :=
    cap_load_to_scalar6 C.weight C.velocity qCap cap
      C.weight_nonneg hqCap hqCapScalar
  exact hConsumer.trans (hCap.trans hScalar)

end

end RouteBP3CentralFDHullScalarBudget

#print axioms RouteBP3CentralFDHullScalarBudget.component_to_cap_load6
#print axioms RouteBP3CentralFDHullScalarBudget.cap_load_to_scalar6
#print axioms RouteBP3CentralFDHullScalarBudget.existing_consumer_to_scalar_budget6
#print axioms RouteBP3CentralFDHullScalarBudget.existing_consumer_to_scalar_cap6

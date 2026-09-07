import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# P3 pure order bridge for an already assembled weighted load

The load coefficient is abstracted as a nonnegative `Fin 6` vector.  This
avoids repeating the radius-load payload and proves only the finite-sum order
step from component caps to cap-load, followed by a conditional capMax scalar
consumer.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP3CentralFDHullOrderConsumer

noncomputable section

abbrev I6 := Fin 6
abbrev Vector6 := I6 → ℝ
abbrev Load6 := Vector6

def weightedLoad6 (load q : Vector6) : ℝ :=
  ∑ i, load i * q i

def capLoad6 (load qCap : Vector6) : ℝ :=
  ∑ i, load i * qCap i

def capMaxLoad6 (load : Load6) (capMax : ℝ) : ℝ :=
  capMax * ∑ i, load i

theorem weightedLoad6_mono_component_cap
    (load q qCap : Vector6)
    (hload : ∀ i, 0 ≤ load i)
    (hqqCap : ∀ i, q i ≤ qCap i) :
    weightedLoad6 load q ≤ capLoad6 load qCap := by
  unfold weightedLoad6 capLoad6
  apply Finset.sum_le_sum
  intro i hi
  exact mul_le_mul_of_nonneg_left (hqqCap i) (hload i)

theorem capLoad6_le_capMaxLoad6
    (load qCap : Vector6) (capMax : ℝ)
    (hload : ∀ i, 0 ≤ load i)
    (hqCap : ∀ i, qCap i ≤ capMax) :
    capLoad6 load qCap ≤ capMaxLoad6 load capMax := by
  unfold capLoad6 capMaxLoad6
  calc
    ∑ i, load i * qCap i ≤ ∑ i, load i * capMax := by
      apply Finset.sum_le_sum
      intro i hi
      exact mul_le_mul_of_nonneg_left (hqCap i) (hload i)
    _ = capMax * ∑ i, load i := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro i hi
      ring

/-! The context carries the requested common-point premises while the order
lemmas remain independent of how those predicates are proved. -/

structure OrderConsumerContext6 (D : Type*) where
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
  load : Load6

theorem capMax_consumer_order_bridge6
    {D : Type*} (C : OrderConsumerContext6 D)
    (consumerValue : ℝ) (q qCap : Vector6) (capMax : ℝ)
    (hConsumer : consumerValue ≤ weightedLoad6 C.load q)
    (hload : ∀ i, 0 ≤ C.load i)
    (_hq : ∀ i, 0 ≤ q i)
    (_hqCap : ∀ i, 0 ≤ qCap i)
    (hqqCap : ∀ i, q i ≤ qCap i)
    (hqCapMax : ∀ i, qCap i ≤ capMax) :
    consumerValue ≤ capMaxLoad6 C.load capMax := by
  exact hConsumer.trans ((weightedLoad6_mono_component_cap C.load q qCap
    hload hqqCap).trans (capLoad6_le_capMaxLoad6 C.load qCap capMax
      hload hqCapMax))

end

end RouteBP3CentralFDHullOrderConsumer

#print axioms RouteBP3CentralFDHullOrderConsumer.weightedLoad6_mono_component_cap
#print axioms RouteBP3CentralFDHullOrderConsumer.capLoad6_le_capMaxLoad6
#print axioms RouteBP3CentralFDHullOrderConsumer.capMax_consumer_order_bridge6

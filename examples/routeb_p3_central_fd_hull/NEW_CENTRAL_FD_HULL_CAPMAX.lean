import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# P3 explicit finite cap-max witness

This leaf represents the maximum of a six-entry cap vector by an explicit
upper-bound and attainment witness.  It avoids relying on a particular
`Finset.sup'` API and proves only the resulting budget comparison.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP3CentralFDHullCapMax

noncomputable section

abbrev I6 := Fin 6
abbrev Vector6 := I6 → ℝ
abbrev Load6 := Vector6

/-- A finite maximum witness for a nonuniform six-entry cap vector. -/
structure CapMaxWitness6 where
  qCap : Vector6
  capMax : ℝ
  qCap_nonneg : ∀ i, 0 ≤ qCap i
  upper_bound : ∀ i, qCap i ≤ capMax
  attained : ∃ i, qCap i = capMax

theorem capMax_upper_bound6 (W : CapMaxWitness6) :
    ∀ i, W.qCap i ≤ W.capMax :=
  W.upper_bound

theorem capMax_attained6 (W : CapMaxWitness6) :
    ∃ i, W.qCap i = W.capMax :=
  W.attained

theorem capMax_nonneg6 (W : CapMaxWitness6) :
    0 ≤ W.capMax := by
  obtain ⟨i, hi⟩ := W.attained
  rw [← hi]
  exact W.qCap_nonneg i

def loadCapBudget6 (load qCap : Vector6) : ℝ :=
  ∑ i, load i * qCap i

def loadMaxCapBudget6 (load : Load6) (capMax : ℝ) : ℝ :=
  capMax * ∑ i, load i

theorem loadCapBudget6_le_maxCapBudget6
    (load : Load6) (W : CapMaxWitness6)
    (hload : ∀ i, 0 ≤ load i) :
    loadCapBudget6 load W.qCap ≤
      loadMaxCapBudget6 load W.capMax := by
  unfold loadCapBudget6 loadMaxCapBudget6
  calc
    ∑ i, load i * W.qCap i ≤
        ∑ i, load i * W.capMax := by
      apply Finset.sum_le_sum
      intro i hi
      exact mul_le_mul_of_nonneg_left
        (W.upper_bound i) (hload i)
    _ = W.capMax * ∑ i, load i := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro i hi
      ring

theorem loadMaxCapBudget6_nonneg
    (load : Load6) (W : CapMaxWitness6)
    (hload : ∀ i, 0 ≤ load i) :
    0 ≤ loadMaxCapBudget6 load W.capMax := by
  unfold loadMaxCapBudget6
  exact mul_nonneg (capMax_nonneg6 W)
    (Finset.sum_nonneg (fun i hi => hload i))

theorem capMax_budget_transit6
    (consumerValue : ℝ) (load : Load6) (W : CapMaxWitness6)
    (hload : ∀ i, 0 ≤ load i)
    (hConsumer : consumerValue ≤ loadCapBudget6 load W.qCap) :
    consumerValue ≤ loadMaxCapBudget6 load W.capMax := by
  exact hConsumer.trans (loadCapBudget6_le_maxCapBudget6 load W hload)

end

end RouteBP3CentralFDHullCapMax

#print axioms RouteBP3CentralFDHullCapMax.capMax_upper_bound6
#print axioms RouteBP3CentralFDHullCapMax.capMax_attained6
#print axioms RouteBP3CentralFDHullCapMax.loadCapBudget6_le_maxCapBudget6
#print axioms RouteBP3CentralFDHullCapMax.capMax_budget_transit6

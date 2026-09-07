import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# P3 capMax attainment and exact budget equality

This leaf treats the sharp single-support case.  A cap vector has an attained
capMax entry, and the load is zero away from that entry.  The resulting
nonuniform load budget equals the scalar capMax budget exactly.  The general
upper-bound inequality remains an upstream order boundary.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP3CentralFDHullCapMaxAttainment

noncomputable section

abbrev I6 := Fin 6
abbrev Vector6 := I6 → ℝ

/-- Same explicit upper-bound/attainment witness shape used by the capMax leaf.
-/
structure CapMaxWitness6 where
  qCap : Vector6
  capMax : ℝ
  upper_bound : ∀ i, qCap i ≤ capMax
  attained : ∃ i, qCap i = capMax

def loadCapBudget6 (load qCap : Vector6) : ℝ :=
  ∑ i, load i * qCap i

def loadMaxCapBudget6 (load : Vector6) (capMax : ℝ) : ℝ :=
  capMax * ∑ i, load i

theorem single_support_term_eq6
    (load qCap : Vector6) (capMax : ℝ) (iStar i : I6)
    (hAttained : qCap iStar = capMax)
    (hZeroOffSupport : i ≠ iStar → load i = 0) :
    load i * qCap i = load i * capMax := by
  by_cases hii : i = iStar
  · subst i
    rw [hAttained]
  · rw [hZeroOffSupport hii]
    ring

theorem single_support_budget_equality6
    (W : CapMaxWitness6) (load : Vector6) (iStar : I6)
    (hAttained : W.qCap iStar = W.capMax)
    (hZeroOffSupport : ∀ i, i ≠ iStar → load i = 0) :
    loadCapBudget6 load W.qCap = loadMaxCapBudget6 load W.capMax := by
  unfold loadCapBudget6 loadMaxCapBudget6
  calc
    ∑ i, load i * W.qCap i = ∑ i, load i * W.capMax := by
      apply Finset.sum_congr rfl
      intro i hi
      exact single_support_term_eq6 load W.qCap W.capMax iStar i
        hAttained (hZeroOffSupport i)
    _ = W.capMax * ∑ i, load i := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro i hi
      ring

theorem single_support_positive_mass_equality6
    (W : CapMaxWitness6) (load : Vector6) (iStar : I6)
    (hAttained : W.qCap iStar = W.capMax)
    (hPositive : 0 < load iStar)
    (hZeroOffSupport : ∀ i, i ≠ iStar → load i = 0) :
    loadCapBudget6 load W.qCap = loadMaxCapBudget6 load W.capMax ∧
      0 < load iStar := by
  exact ⟨single_support_budget_equality6 W load iStar hAttained
    hZeroOffSupport, hPositive⟩

/-- Equality is a sharp refinement of the ordinary order boundary. -/
theorem equality_refines_order_boundary6
    (nonuniformBudget scalarBudget : ℝ)
    (hEq : nonuniformBudget = scalarBudget) :
    nonuniformBudget ≤ scalarBudget := by
  rw [hEq]

end

end RouteBP3CentralFDHullCapMaxAttainment

#print axioms RouteBP3CentralFDHullCapMaxAttainment.single_support_term_eq6
#print axioms RouteBP3CentralFDHullCapMaxAttainment.single_support_budget_equality6
#print axioms RouteBP3CentralFDHullCapMaxAttainment.single_support_positive_mass_equality6
#print axioms RouteBP3CentralFDHullCapMaxAttainment.equality_refines_order_boundary6

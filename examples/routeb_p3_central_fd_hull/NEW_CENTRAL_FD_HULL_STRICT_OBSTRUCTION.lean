import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# P3 strict cap-load obstruction tracking

This sidecar records why the positive-load and strict-gap premises in the
strict order leaf cannot be dropped.  It proves only equality/negation
obstructions and supplies an explicit Fin 6 counterexample.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP3CentralFDHullStrictObstruction

noncomputable section

abbrev I6 := Fin 6
abbrev Vector6 := I6 → ℝ

def weightedLoad6 (load q : Vector6) : ℝ :=
  ∑ i, load i * q i

theorem no_strict_from_pointwise_term_equality6
    (load q qCap : Vector6)
    (hTerm : ∀ i, load i * q i = load i * qCap i) :
    ¬ weightedLoad6 load q < weightedLoad6 load qCap := by
  intro hStrict
  have hEq : weightedLoad6 load q = weightedLoad6 load qCap := by
    unfold weightedLoad6
    apply Finset.sum_congr rfl
    intro i hi
    exact hTerm i
  linarith

theorem no_strict_without_cap_gap6
    (load q qCap : Vector6)
    (hEqual : ∀ i, q i = qCap i) :
    ¬ weightedLoad6 load q < weightedLoad6 load qCap := by
  apply no_strict_from_pointwise_term_equality6 load q qCap
  intro i
  rw [hEqual i]

theorem no_strict_when_selected_load_zero6
    (load q qCap : Vector6) (jStar : I6)
    (hAllTerm : ∀ i, load i * q i = load i * qCap i) :
    load jStar = 0 →
      ¬ weightedLoad6 load q < weightedLoad6 load qCap := by
  intro hzero
  exact no_strict_from_pointwise_term_equality6 load q qCap hAllTerm

theorem explicit_zero_support_counterexample6 :
    ∃ (load q qCap : Vector6) (jStar : I6),
      (∀ i, 0 ≤ load i) ∧
      (∀ i, q i ≤ qCap i) ∧
      q jStar < qCap jStar ∧
      load jStar = 0 ∧
      weightedLoad6 load q = weightedLoad6 load qCap := by
  let load : Vector6 := fun _ => 0
  let q : Vector6 := fun _ => 0
  let qCap : Vector6 := fun i => if i = (0 : I6) then 1 else 0
  refine ⟨load, q, qCap, 0, ?_, ?_, ?_, ?_, ?_⟩
  · intro i
    rfl
  · intro i
    by_cases hi : i = (0 : I6)
    · simp [q, qCap, hi]
    · simp [q, qCap, hi]
  · simp [q, qCap]
  · rfl
  · simp [weightedLoad6, load, q, qCap]

end

end RouteBP3CentralFDHullStrictObstruction

#print axioms RouteBP3CentralFDHullStrictObstruction.no_strict_from_pointwise_term_equality6
#print axioms RouteBP3CentralFDHullStrictObstruction.no_strict_without_cap_gap6
#print axioms RouteBP3CentralFDHullStrictObstruction.explicit_zero_support_counterexample6

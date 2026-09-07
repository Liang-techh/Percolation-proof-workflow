import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# P3 quantitative strict-gap lower bound

This leaf quantifies an already available strict component gap.  It proves that
the total weighted-load gap is at least the selected positive term, assuming
all other component gaps are nonnegative.  It does not reprove strictness or
record the zero-load obstruction.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP3CentralFDHullQuantitativeGap

noncomputable section

abbrev I6 := Fin 6
abbrev Vector6 := I6 → ℝ

def weightedLoad6 (load q : Vector6) : ℝ :=
  ∑ i, load i * q i

def componentGap6 (load q qCap : Vector6) (i : I6) : ℝ :=
  load i * (qCap i - q i)

theorem weighted_gap_identity6
    (load q qCap : Vector6) :
    weightedLoad6 load qCap - weightedLoad6 load q =
      ∑ i, componentGap6 load q qCap i := by
  unfold weightedLoad6 componentGap6
  apply Finset.sum_congr rfl
  intro i hi
  ring

theorem weighted_gap_lower_bound6
    (load q qCap : Vector6) (jStar : I6)
    (hload : ∀ i, 0 ≤ load i)
    (horder : ∀ i, q i ≤ qCap i) :
    componentGap6 load q qCap jStar ≤
      weightedLoad6 load qCap - weightedLoad6 load q := by
  let f : I6 → ℝ := fun i => componentGap6 load q qCap i
  have hf_nonneg : ∀ i, 0 ≤ f i := by
    intro i
    dsimp [f, componentGap6]
    exact mul_nonneg (hload i) (sub_nonneg.mpr (horder i))
  have hrest : 0 ≤ ∑ i in Finset.univ.erase jStar, f i := by
    exact Finset.sum_nonneg (fun i hi => hf_nonneg i)
  have hsplit :
      (∑ i, f i) = f jStar + ∑ i in Finset.univ.erase jStar, f i := by
    simpa [add_comm] using
      (Finset.sum_erase_add f (Finset.mem_univ jStar)).symm
  have hlower : f jStar ≤ ∑ i, f i := by
    rw [hsplit]
    linarith
  rw [weighted_gap_identity6 load q qCap]
  exact hlower

theorem weighted_gap_lower_bound_strict_witness6
    (load q qCap : Vector6) (jStar : I6)
    (hload : ∀ i, 0 ≤ load i)
    (horder : ∀ i, q i ≤ qCap i)
    (hgap : 0 < componentGap6 load q qCap jStar) :
    0 < componentGap6 load q qCap jStar ∧
      componentGap6 load q qCap jStar ≤
        weightedLoad6 load qCap - weightedLoad6 load q := by
  exact ⟨hgap,
    weighted_gap_lower_bound6 load q qCap jStar hload horder⟩

end

end RouteBP3CentralFDHullQuantitativeGap

#print axioms RouteBP3CentralFDHullQuantitativeGap.weighted_gap_identity6
#print axioms RouteBP3CentralFDHullQuantitativeGap.weighted_gap_lower_bound6
#print axioms RouteBP3CentralFDHullQuantitativeGap.weighted_gap_lower_bound_strict_witness6

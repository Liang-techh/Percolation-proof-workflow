import NEW_FIXED_LAMBDA_ADMISSIBILITY_INDEX_TRANSPORT_OBSTRUCTIONS20260907
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaFiniteReindexSumEquality

open RouteBFixedLambdaIndexTransportObstructions

noncomputable section

/-!
This sidecar is the positive finite reindex equality adapter.  A map between
selected finite index sets is required to preserve membership, be injective
and surjective on those sets, and preserve the summand pointwise.  No equality
is inferred from cardinality alone.
-/

structure FiniteReindexWeightAdapter where
  source : Finset Nat
  target : Finset Nat
  rowMap : Nat → Nat
  sourceWeight : Nat → ℚ
  targetWeight : Nat → ℚ
  row_map_mem :
    ∀ i ∈ source, rowMap i ∈ target
  row_map_injective :
    ∀ {i j : Nat}, i ∈ source → j ∈ source →
      rowMap i = rowMap j → i = j
  row_map_surjective :
    ∀ j ∈ target, ∃ i ∈ source, rowMap i = j
  pointwise_weight_eq :
    ∀ i ∈ source, sourceWeight i = targetWeight (rowMap i)

theorem finite_reindex_weight_sum_eq
    (a : FiniteReindexWeightAdapter) :
    (∑ i in a.source, a.sourceWeight i) =
      ∑ j in a.target, a.targetWeight j := by
  refine Finset.sum_bij (fun i _ => a.rowMap i) ?_ ?_ ?_ ?_
  · intro i hi
    exact a.row_map_mem i hi
  · intro i hi j hj hmap
    exact a.row_map_injective hi hj hmap
  · intro j hj
    rcases a.row_map_surjective j hj with ⟨i, hi, hmap⟩
    exact ⟨i, hi, hmap⟩
  · intro i hi
    exact a.pointwise_weight_eq i hi

theorem finite_reindex_weight_sum_eq_of_explicit_equiv
    (a : FiniteReindexWeightAdapter)
    (hsource_target : a.source.card = a.target.card) :
    (∑ i in a.source, a.sourceWeight i) =
      ∑ j in a.target, a.targetWeight j := by
  exact finite_reindex_weight_sum_eq a

/-!
The next theorem keeps the previously recorded negative controls available to
reviewers.  They are imported rather than redefined here.
-/
theorem missing_bijection_or_pointwise_equality_has_counterexample :
    sourceSum noninjectiveSource unitLoad ≠
        targetSum noninjectiveTarget unitLoad ∧
      sourceSum nonsurjectiveSource unitLoad ≠
        targetSum nonsurjectiveTarget unitLoad ∧
      sourceSum equalIndexSource sourcePayload ≠
        targetSum equalIndexTarget targetPayload := by
  exact transport_is_not_derivable_without_all_premises

/- Admission boundary: this is a finite exact reindexing lemma only; no source,
   coverage, digest, receipt, Lean verification, or registry claim follows. -/

#print axioms finite_reindex_weight_sum_eq
#print axioms finite_reindex_weight_sum_eq_of_explicit_equiv
#print axioms missing_bijection_or_pointwise_equality_has_counterexample

end
end RouteBFixedLambdaFiniteReindexSumEquality

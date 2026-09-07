import NEW_FIXED_LAMBDA_ADMISSIBILITY_FINITE_REINDEX_SUM_EQUALITY20260907
import Mathlib.Data.Real.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaRatRealFiniteSumCast

open RouteBFixedLambdaFiniteReindexSumEquality

noncomputable section

/-!
This sidecar supplies the rational-to-real finite-sum cast adapter.  The
canonical coercion `ℚ → ℝ` is applied only after a finite `Finset` sum, and the
finite induction makes the sum/cast equality explicit for later consumers.
-/

theorem cast_finset_sum_rat_to_real
    {ι : Type*} (s : Finset ι) (q : ι → ℚ) :
    ((∑ i in s, q i) : ℝ) =
      ∑ i in s, (q i : ℝ) := by
  classical
  induction s using Finset.induction_on with
  | empty =>
      norm_num
  | @insert a s ha ih =>
      simp [Finset.sum_insert ha, ih]

def sourceRealSum
    (a : FiniteReindexWeightAdapter) : ℝ :=
  ∑ i in a.source, (a.sourceWeight i : ℝ)

def targetRealSum
    (a : FiniteReindexWeightAdapter) : ℝ :=
  ∑ j in a.target, (a.targetWeight j : ℝ)

theorem source_real_sum_eq_cast_source_rat_sum
    (a : FiniteReindexWeightAdapter) :
    sourceRealSum a =
      ((∑ i in a.source, a.sourceWeight i) : ℝ) := by
  unfold sourceRealSum
  symm
  exact cast_finset_sum_rat_to_real a.source a.sourceWeight

theorem target_real_sum_eq_cast_target_rat_sum
    (a : FiniteReindexWeightAdapter) :
    targetRealSum a =
      ((∑ j in a.target, a.targetWeight j) : ℝ) := by
  unfold targetRealSum
  symm
  exact cast_finset_sum_rat_to_real a.target a.targetWeight

theorem finite_reindex_weight_sum_eq_after_rat_real_cast
    (a : FiniteReindexWeightAdapter) :
    sourceRealSum a = targetRealSum a := by
  rw [source_real_sum_eq_cast_source_rat_sum a,
    target_real_sum_eq_cast_target_rat_sum a]
  exact congrArg (fun z : ℚ => (z : ℝ))
    (finite_reindex_weight_sum_eq a)

theorem finite_reindex_cast_chain
    (a : FiniteReindexWeightAdapter) :
    sourceRealSum a =
        ((∑ i in a.source, a.sourceWeight i) : ℝ) ∧
      ((∑ i in a.source, a.sourceWeight i) : ℝ) =
        ((∑ j in a.target, a.targetWeight j) : ℝ) ∧
      ((∑ j in a.target, a.targetWeight j) : ℝ) =
        targetRealSum a := by
  constructor
  · exact source_real_sum_eq_cast_source_rat_sum a
  constructor
  · exact congrArg (fun z : ℚ => (z : ℝ))
      (finite_reindex_weight_sum_eq a)
  · exact (target_real_sum_eq_cast_target_rat_sum a).symm

/-!
If the canonical cast or finite index domain is unavailable, this adapter has
no theorem to consume.  The missing structure is intentionally not replaced
by an untyped numerical coercion.
-/

#print axioms cast_finset_sum_rat_to_real
#print axioms finite_reindex_weight_sum_eq_after_rat_real_cast
#print axioms finite_reindex_cast_chain

end
end RouteBFixedLambdaRatRealFiniteSumCast

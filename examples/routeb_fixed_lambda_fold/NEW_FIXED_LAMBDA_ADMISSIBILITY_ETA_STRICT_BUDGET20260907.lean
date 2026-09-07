import NEW_FIXED_LAMBDA_ADMISSIBILITY_ETA_SUM_DECOMPOSITION20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaEtaStrictBudget

open RouteBFixedLambdaAdmissibility
open RouteBFixedLambdaTwoEtaUnion
open RouteBFixedLambdaUniformFeasibility
open RouteBFixedLambdaUniformMarginBudget
open RouteBFixedLambdaWeightedAbsorption
open RouteBFixedLambdaEtaSumDecomposition

noncomputable section

/-!
This sidecar combines the previously established eta sum decomposition with
the existing weighted term inequalities.  It adds no new global union
decomposition or strict-total theorem: only the two eta-local strict budgets
and their additive combination are stated here.
-/

theorem subpartition_strict_load_lt_delta
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformMarginLowerBound f lambda)
    (rows : Finset (EtaTag × Nat))
    (hrows : ∀ x ∈ rows, x ∈ unionRows f)
    (coeff load : (EtaTag × Nat) → ℚ)
    (hcoeff : NonnegativeCoefficient coeff)
    (hload : StrictLoadBelowDelta b load)
    (hnonempty : rows.Nonempty)
    (hpositive_coefficient : ∃ x ∈ rows, 0 < coeff x) :
    (∑ x in rows, coeff x * load x) <
      (∑ x in rows, coeff x * b.delta) := by
  apply Finset.sum_lt_sum
  · intro x hx
    exact weighted_load_term_le_delta_term b coeff load hcoeff hload x
      (hrows x hx)
  · rcases hpositive_coefficient with ⟨x, hx, hcx⟩
    exact ⟨x, hx,
      weighted_load_term_lt_delta_term_of_positive_coefficient
        b coeff load hload (hrows x hx) hcx⟩

theorem eta27_strict_weighted_load_lt_margin
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformMarginLowerBound f lambda)
    (p : ExplicitEtaSumPartition f)
    (coeff load : (EtaTag × Nat) → ℚ)
    (hcoeff : NonnegativeCoefficient coeff)
    (hload : StrictLoadBelowDelta b load)
    (hnonempty27 : p.eta27Rows.Nonempty)
    (hpositive27 : ∃ x ∈ p.eta27Rows, 0 < coeff x) :
    eta27WeightedLoadTotal p coeff load <
      eta27WeightedMarginTotal p coeff := by
  have hload_delta := subpartition_strict_load_lt_delta b p.eta27Rows
    (fun x hx => eta27_mem_union p hx) coeff load hcoeff hload
    hnonempty27 hpositive27
  exact lt_of_lt_of_le hload_delta
    (eta27_weighted_delta_le_eta_margin b p coeff hcoeff)

theorem eta56_strict_weighted_load_lt_margin
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformMarginLowerBound f lambda)
    (p : ExplicitEtaSumPartition f)
    (coeff load : (EtaTag × Nat) → ℚ)
    (hcoeff : NonnegativeCoefficient coeff)
    (hload : StrictLoadBelowDelta b load)
    (hnonempty56 : p.eta56Rows.Nonempty)
    (hpositive56 : ∃ x ∈ p.eta56Rows, 0 < coeff x) :
    eta56WeightedLoadTotal p coeff load <
      eta56WeightedMarginTotal p coeff := by
  have hload_delta := subpartition_strict_load_lt_delta b p.eta56Rows
    (fun x hx => eta56_mem_union p hx) coeff load hcoeff hload
    hnonempty56 hpositive56
  exact lt_of_lt_of_le hload_delta
    (eta56_weighted_delta_le_eta_margin b p coeff hcoeff)

/- The following theorem is only the additive combination of the two already
   proved eta-local strict budgets. -/
theorem combine_eta_strict_budgets
    {f : Declared577SparseFold} {lambda : ℚ}
    (p : ExplicitEtaSumPartition f)
    (coeff load : (EtaTag × Nat) → ℚ)
    (h27 : eta27WeightedLoadTotal p coeff load <
      eta27WeightedMarginTotal p coeff)
    (h56 : eta56WeightedLoadTotal p coeff load <
      eta56WeightedMarginTotal p coeff) :
    weightedLoadTotal coeff load < weightedMarginTotal coeff := by
  rw [weighted_load_union_eq_eta_sum p coeff load,
    weighted_margin_union_eq_eta_sum p coeff]
  linarith

structure EtaStrictBudgetCertificate
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformMarginLowerBound f lambda)
    (p : ExplicitEtaSumPartition f)
    (coeff load : (EtaTag × Nat) → ℚ) where
  eta27_nonempty : p.eta27Rows.Nonempty
  eta56_nonempty : p.eta56Rows.Nonempty
  eta27_load_lt_margin :
    eta27WeightedLoadTotal p coeff load <
      eta27WeightedMarginTotal p coeff
  eta56_load_lt_margin :
    eta56WeightedLoadTotal p coeff load <
      eta56WeightedMarginTotal p coeff
  union_load_lt_margin :
    weightedLoadTotal coeff load < weightedMarginTotal coeff

theorem build_eta_strict_budget_certificate
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformMarginLowerBound f lambda)
    (p : ExplicitEtaSumPartition f)
    (coeff load : (EtaTag × Nat) → ℚ)
    (hcoeff : NonnegativeCoefficient coeff)
    (hload : StrictLoadBelowDelta b load)
    (hnonempty27 : p.eta27Rows.Nonempty)
    (hnonempty56 : p.eta56Rows.Nonempty)
    (hpositive27 : ∃ x ∈ p.eta27Rows, 0 < coeff x)
    (hpositive56 : ∃ x ∈ p.eta56Rows, 0 < coeff x) :
    EtaStrictBudgetCertificate b p coeff load := by
  have h27 := eta27_strict_weighted_load_lt_margin b p coeff load
    hcoeff hload hnonempty27 hpositive27
  have h56 := eta56_strict_weighted_load_lt_margin b p coeff load
    hcoeff hload hnonempty56 hpositive56
  exact
    { eta27_nonempty := hnonempty27
      eta56_nonempty := hnonempty56
      eta27_load_lt_margin := h27
      eta56_load_lt_margin := h56
      union_load_lt_margin := combine_eta_strict_budgets p coeff load h27 h56 }

/- Admission boundary: strictness is finite eta-subset arithmetic only;
   source, receipt, digest, and physical coverage remain outside this leaf. -/

#print axioms subpartition_strict_load_lt_delta
#print axioms eta27_strict_weighted_load_lt_margin
#print axioms eta56_strict_weighted_load_lt_margin
#print axioms combine_eta_strict_budgets
#print axioms build_eta_strict_budget_certificate

end
end RouteBFixedLambdaEtaStrictBudget

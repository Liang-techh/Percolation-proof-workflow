import NEW_FIXED_LAMBDA_ADMISSIBILITY_WEIGHTED_ABSORPTION20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaStrictTotalAbsorption

open RouteBFixedLambdaAdmissibility
open RouteBFixedLambdaTwoEtaUnion
open RouteBFixedLambdaUniformFeasibility
open RouteBFixedLambdaUniformMarginBudget
open RouteBFixedLambdaWeightedAbsorption

noncomputable section

/-!
This sidecar adds the strict finite-sum step.  Nonnegative coefficients alone
give only a non-strict total inequality; a selected-row witness with strictly
positive coefficient is retained explicitly to obtain strictness.
-/

structure StrictTotalAbsorptionCertificate
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformMarginLowerBound f lambda)
    (coeff load : (EtaTag × Nat) → ℚ) where
  union_nonempty : (unionRows f).Nonempty
  total_load_lt_delta :
    weightedLoadTotal coeff load < weightedDeltaTotal b.delta coeff
  total_load_lt_margin :
    weightedLoadTotal coeff load < weightedMarginTotal coeff

theorem strict_total_weighted_load_lt_delta
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformMarginLowerBound f lambda)
    (coeff load : (EtaTag × Nat) → ℚ)
    (hcoeff : NonnegativeCoefficient coeff)
    (hload : StrictLoadBelowDelta b load)
    (hnonempty : (unionRows f).Nonempty)
    (hpositive_coefficient :
      ∃ x ∈ unionRows f, 0 < coeff x) :
    weightedLoadTotal coeff load < weightedDeltaTotal b.delta coeff := by
  unfold weightedLoadTotal weightedDeltaTotal
  apply Finset.sum_lt_sum
  · intro x hx
    exact weighted_load_term_le_delta_term b coeff load hcoeff hload x hx
  · rcases hpositive_coefficient with ⟨x, hx, hcx⟩
    exact ⟨x, hx,
      weighted_load_term_lt_delta_term_of_positive_coefficient
        b coeff load hload hx hcx⟩

theorem strict_total_weighted_load_lt_margin
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformMarginLowerBound f lambda)
    (coeff load : (EtaTag × Nat) → ℚ)
    (hcoeff : NonnegativeCoefficient coeff)
    (hload : StrictLoadBelowDelta b load)
    (hnonempty : (unionRows f).Nonempty)
    (hpositive_coefficient :
      ∃ x ∈ unionRows f, 0 < coeff x) :
    weightedLoadTotal coeff load < weightedMarginTotal coeff := by
  exact lt_of_lt_of_le
    (strict_total_weighted_load_lt_delta
      b coeff load hcoeff hload hnonempty hpositive_coefficient)
    (total_delta_le_total_weighted_margin b coeff hcoeff)

theorem build_strict_total_absorption_certificate
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformMarginLowerBound f lambda)
    (coeff load : (EtaTag × Nat) → ℚ)
    (hcoeff : NonnegativeCoefficient coeff)
    (hload : StrictLoadBelowDelta b load)
    (hnonempty : (unionRows f).Nonempty)
    (hpositive_coefficient :
      ∃ x ∈ unionRows f, 0 < coeff x) :
    StrictTotalAbsorptionCertificate b coeff load := by
  exact
    { union_nonempty := hnonempty
      total_load_lt_delta := strict_total_weighted_load_lt_delta
        b coeff load hcoeff hload hnonempty hpositive_coefficient
      total_load_lt_margin := strict_total_weighted_load_lt_margin
        b coeff load hcoeff hload hnonempty hpositive_coefficient }

/- Admission boundary: the strict total result is a finite weighted inequality
   over supplied typed premises, not a residual/source or coverage theorem. -/

#print axioms strict_total_weighted_load_lt_delta
#print axioms strict_total_weighted_load_lt_margin
#print axioms build_strict_total_absorption_certificate

end
end RouteBFixedLambdaStrictTotalAbsorption

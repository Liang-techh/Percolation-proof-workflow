import NEW_FIXED_LAMBDA_ADMISSIBILITY_STRICT_MARGIN_CONSUMER20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaWeightedAbsorption

open RouteBFixedLambdaAdmissibility
open RouteBFixedLambdaTwoEtaUnion
open RouteBFixedLambdaUniformFeasibility
open RouteBFixedLambdaUniformMarginBudget
open RouteBFixedLambdaUniformMarginBudgetRevised
open RouteBFixedLambdaStrictMarginConsumer

noncomputable section

/-!
This sidecar is only the weighted finite-sum consumer.  The lower-bound record
supplies `delta ≤ marginAt`; the load and coefficient conditions below are
explicit inputs.  No residual/source semantics are hidden in the definitions.
-/

def weightedLoadTotal
    {f : Declared577SparseFold}
    (coeff load : (EtaTag × Nat) → ℚ) : ℚ :=
  ∑ x in unionRows f, coeff x * load x

def weightedDeltaTotal
    {f : Declared577SparseFold} (delta : ℚ)
    (coeff : (EtaTag × Nat) → ℚ) : ℚ :=
  ∑ x in unionRows f, coeff x * delta

def weightedMarginTotal
    {f : Declared577SparseFold} {lambda : ℚ}
    (coeff : (EtaTag × Nat) → ℚ) : ℚ :=
  ∑ x in unionRows f, coeff x * marginAt lambda (unionRow f x)

def NonnegativeCoefficient
    {f : Declared577SparseFold}
    (coeff : (EtaTag × Nat) → ℚ) : Prop :=
  ∀ x ∈ unionRows f, 0 ≤ coeff x

def StrictLoadBelowDelta
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformMarginLowerBound f lambda)
    (load : (EtaTag × Nat) → ℚ) : Prop :=
  ∀ x ∈ unionRows f,
    0 ≤ load x ∧ load x < b.delta

theorem weighted_load_term_le_delta_term
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformMarginLowerBound f lambda)
    (coeff load : (EtaTag × Nat) → ℚ)
    (hcoeff : NonnegativeCoefficient coeff)
    (hload : StrictLoadBelowDelta b load)
    (x : EtaTag × Nat) (hx : x ∈ unionRows f) :
    coeff x * load x ≤ coeff x * b.delta := by
  exact mul_le_mul_of_nonneg_left
    (le_of_lt (hload x hx).2) (hcoeff x hx)

theorem weighted_load_term_lt_delta_term_of_positive_coefficient
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformMarginLowerBound f lambda)
    (coeff load : (EtaTag × Nat) → ℚ)
    (hload : StrictLoadBelowDelta b load)
    {x : EtaTag × Nat} (hx : x ∈ unionRows f)
    (hcoeff_pos : 0 < coeff x) :
    coeff x * load x < coeff x * b.delta := by
  exact mul_lt_mul_of_pos_left (hload x hx).2 hcoeff_pos

theorem weighted_delta_term_le_margin_term
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformMarginLowerBound f lambda)
    (coeff : (EtaTag × Nat) → ℚ)
    (hcoeff : NonnegativeCoefficient coeff)
    (x : EtaTag × Nat) (hx : x ∈ unionRows f) :
    coeff x * b.delta ≤
      coeff x * marginAt lambda (unionRow f x) := by
  exact mul_le_mul_of_nonneg_left (b.lower_bound x hx) (hcoeff x hx)

/- The first total bound is the explicit finite weighted load budget. -/
theorem total_weighted_load_le_total_delta
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformMarginLowerBound f lambda)
    (coeff load : (EtaTag × Nat) → ℚ)
    (hcoeff : NonnegativeCoefficient coeff)
    (hload : StrictLoadBelowDelta b load) :
    weightedLoadTotal coeff load ≤ weightedDeltaTotal b.delta coeff := by
  unfold weightedLoadTotal weightedDeltaTotal
  apply Finset.sum_le_sum
  intro x hx
  exact weighted_load_term_le_delta_term b coeff load hcoeff hload x hx

theorem total_delta_le_total_weighted_margin
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformMarginLowerBound f lambda)
    (coeff : (EtaTag × Nat) → ℚ)
    (hcoeff : NonnegativeCoefficient coeff) :
    weightedDeltaTotal b.delta coeff ≤ weightedMarginTotal coeff := by
  unfold weightedDeltaTotal weightedMarginTotal
  apply Finset.sum_le_sum
  intro x hx
  exact weighted_delta_term_le_margin_term b coeff hcoeff x hx

theorem total_weighted_load_le_total_weighted_margin
    {f : Declared577SparseFold} {lambda : ℚ}
    (b : UniformMarginLowerBound f lambda)
    (coeff load : (EtaTag × Nat) → ℚ)
    (hcoeff : NonnegativeCoefficient coeff)
    (hload : StrictLoadBelowDelta b load) :
    weightedLoadTotal coeff load ≤ weightedMarginTotal coeff := by
  exact le_trans
    (total_weighted_load_le_total_delta b coeff load hcoeff hload)
    (total_delta_le_total_weighted_margin b coeff hcoeff)

/-!
The strict rowwise load premise is preserved in the total-budget chain.  A
strict total inequality additionally requires a positive coefficient on at
least one selected row; that stronger claim is intentionally left as an
explicit future premise rather than inferred from nonnegative coefficients.
-/

#print axioms weighted_load_term_le_delta_term
#print axioms weighted_load_term_lt_delta_term_of_positive_coefficient
#print axioms weighted_delta_term_le_margin_term
#print axioms total_weighted_load_le_total_delta
#print axioms total_delta_le_total_weighted_margin
#print axioms total_weighted_load_le_total_weighted_margin

end
end RouteBFixedLambdaWeightedAbsorption

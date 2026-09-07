import NEW_FIXED_LAMBDA_ADMISSIBILITY_ETA_STRICT_BUDGET20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaFinalStrictExport

open RouteBFixedLambdaAdmissibility
open RouteBFixedLambdaTwoEtaUnion
open RouteBFixedLambdaUniformFeasibility
open RouteBFixedLambdaUniformMarginBudget
open RouteBFixedLambdaWeightedAbsorption
open RouteBFixedLambdaEtaSumDecomposition
open RouteBFixedLambdaEtaStrictBudget

noncomputable section

/-!
This is the final typed export seam for the fixed-lambda lane.  The global
strict weighted budget comes from the existing eta certificate.  The separate
two-row premise carries `CellMarginData`, hence its positive denominator,
ratio, and declared margin fields; only the strict `lambdaUpper > 2` row
condition is consumed here to expose the final admissibility result.
-/

structure TwoRowMarginDenominatorPremise
    (q : FixedLambdaParameters ℚ) where
  rows : Fin 2 → CellMarginData ℚ
  upper_strict : ∀ i, 2 < (rows i).lambdaUpper

structure FinalStrictConsumerExport
    {f : Declared577SparseFold}
    (q : FixedLambdaParameters ℚ)
    (b : UniformMarginLowerBound f q.lambda)
    (p : ExplicitEtaSumPartition f)
    (coeff load : (EtaTag × Nat) → ℚ)
    (two : TwoRowMarginDenominatorPremise q) where
  union_load_lt_margin :
    weightedLoadTotal coeff load < weightedMarginTotal coeff
  two_row_upper_strict : ∀ i, 2 < (two.rows i).lambdaUpper
  two_row_positive_margin : ∀ i, 0 < (two.rows i).candidateMargin
  two_row_admissible : ∀ i, rowAdmissible q (two.rows i)

theorem two_row_positive_margin_of_upper
    {q : FixedLambdaParameters ℚ}
    (two : TwoRowMarginDenominatorPremise q) :
    ∀ i, 0 < (two.rows i).candidateMargin := by
  intro i
  exact (strict_upper_iff_positive_margin q (two.rows i)).mp
    (by
      rw [q.lambda_eq_two]
      exact two.upper_strict i)

theorem two_row_admissible_of_upper
    {q : FixedLambdaParameters ℚ}
    (two : TwoRowMarginDenominatorPremise q) :
    ∀ i, rowAdmissible q (two.rows i) := by
  intro i
  apply (rowAdmissible_iff_two_upper_and_positive q (two.rows i)).mpr
  exact ⟨two.upper_strict i,
    (two_row_positive_margin_of_upper two) i⟩

/-!
The certificate and the two-row premise are exported together.  The type of
`b` is `UniformMarginLowerBound f q.lambda`, so the finite budget and the
two-row consumer are forced to use the same fixed lambda value.
-/
theorem build_final_strict_consumer_export
    {f : Declared577SparseFold}
    (q : FixedLambdaParameters ℚ)
    (b : UniformMarginLowerBound f q.lambda)
    (p : ExplicitEtaSumPartition f)
    (coeff load : (EtaTag × Nat) → ℚ)
    (two : TwoRowMarginDenominatorPremise q)
    (certificate : EtaStrictBudgetCertificate b p coeff load) :
    FinalStrictConsumerExport q b p coeff load two := by
  exact
    { union_load_lt_margin := certificate.union_load_lt_margin
      two_row_upper_strict := two.upper_strict
      two_row_positive_margin := two_row_positive_margin_of_upper two
      two_row_admissible := two_row_admissible_of_upper two }

theorem final_export_retains_exact_lambda_and_theta
    {f : Declared577SparseFold}
    (q : FixedLambdaParameters ℚ)
    (b : UniformMarginLowerBound f q.lambda)
    (p : ExplicitEtaSumPartition f)
    (coeff load : (EtaTag × Nat) → ℚ)
    (two : TwoRowMarginDenominatorPremise q)
    (certificate : EtaStrictBudgetCertificate b p coeff load) :
    q.lambda = 2 ∧ q.theta = 1 := by
  exact ⟨q.lambda_eq_two, q.theta_eq_one⟩

/- Admission boundary: this export combines already supplied finite typed
   evidence; it is not a source, coverage, comparator, or registry theorem. -/

#print axioms two_row_positive_margin_of_upper
#print axioms two_row_admissible_of_upper
#print axioms build_final_strict_consumer_export
#print axioms final_export_retains_exact_lambda_and_theta

end
end RouteBFixedLambdaFinalStrictExport

import NEW_FIXED_LAMBDA_ADMISSIBILITY_UNIFORM_FEASIBILITY20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaMonotonicity

open RouteBFixedLambdaAdmissibility
open RouteBFixedLambdaTwoEtaUnion
open RouteBFixedLambdaUniformFeasibility

noncomputable section

/-!
This sidecar is the generic downward-monotonicity leaf.  Unlike the earlier
fixed-2 witness, `UniformCandidateWitness` permits an arbitrary shared
candidate `lambda₀`; the conclusion can then lower it to any
`1 < lambda ≤ lambda₀`.
-/

theorem row_margin_monotone_downward
    {lambda lambda₀ : ℚ}
    (c : CellMarginData ℚ)
    (hle : lambda ≤ lambda₀) :
    marginAt lambda₀ c ≤ marginAt lambda c := by
  have hprod : lambda * c.cellGamma ≤ lambda₀ * c.cellGamma :=
    mul_le_mul_of_nonneg_right hle (le_of_lt c.cellGamma_pos)
  unfold marginAt
  linarith

structure UniformCandidateWitness
    (f : Declared577SparseFold) where
  lambda₀ : ℚ
  union_nonempty : (unionRows f).Nonempty
  feasible : uniformCandidateFeasible f lambda₀

theorem uniform_candidate_feasible_downward
    {f : Declared577SparseFold}
    (w : UniformCandidateWitness f)
    {lambda : ℚ}
    (hlower : 1 < lambda)
    (hle : lambda ≤ w.lambda₀) :
    uniformCandidateFeasible f lambda := by
  intro x hx
  rcases w.feasible x hx with ⟨_, hupper₀, hmargin₀⟩
  have hupper : lambda < (unionRow f x).lambdaUpper :=
    lt_of_le_of_lt hle hupper₀
  have hmargin_le :
      marginAt w.lambda₀ (unionRow f x) ≤
        marginAt lambda (unionRow f x) :=
    row_margin_monotone_downward (unionRow f x) hle
  have hmargin : 0 < marginAt lambda (unionRow f x) :=
    lt_of_lt_of_le hmargin₀ hmargin_le
  exact ⟨hlower, hupper, hmargin⟩

/-!
The exact fixed parameter record is a separate output object.  The only new
premise is `2 ≤ lambda₀`; the proof uses monotonicity, not a repeated fixed-2
feasibility argument.
-/
theorem reduce_feasible_candidate_to_exact_two
    {f : Declared577SparseFold}
    (w : UniformCandidateWitness f)
    (htwo_le : (2 : ℚ) ≤ w.lambda₀) :
    UniformLambdaFeasibilityWitness f := by
  refine
    { params := exactLambdaTwoThetaOne
      union_nonempty := w.union_nonempty
      feasible := ?_ }
  apply uniform_candidate_feasible_downward w
  · norm_num [exactLambdaTwoThetaOne]
  · simpa [exactLambdaTwoThetaOne] using htwo_le

theorem reduced_witness_has_exact_lambda_and_theta
    {f : Declared577SparseFold}
    (w : UniformCandidateWitness f)
    (htwo_le : (2 : ℚ) ≤ w.lambda₀) :
    ∃ v : UniformLambdaFeasibilityWitness f,
      v.params.lambda = 2 ∧ v.params.theta = 1 := by
  let v := reduce_feasible_candidate_to_exact_two w htwo_le
  exact ⟨v, v.params.lambda_eq_two, v.params.theta_eq_one⟩

/- Admission boundary: monotonicity is over the supplied finite union and
   typed positive denominators; it does not create source or coverage facts. -/

#print axioms row_margin_monotone_downward
#print axioms uniform_candidate_feasible_downward
#print axioms reduce_feasible_candidate_to_exact_two
#print axioms reduced_witness_has_exact_lambda_and_theta

end
end RouteBFixedLambdaMonotonicity

import NEW_FIXED_LAMBDA_ADMISSIBILITY_TWO_ETA_UNION20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaUniformFeasibility

open RouteBFixedLambdaAdmissibility
open RouteBFixedLambdaCoefficientBridge
open RouteBFixedLambdaSparseDigestFold
open RouteBFixedLambdaTwoEtaUnion

noncomputable section

/-!
This sidecar formalizes the finite-union feasibility seam.  A candidate scalar
lambda is tested against every element of the tagged sparse union.  The
fixed-lambda witness uses the existing exact parameter record, so lambda is a
single scalar shared by all rows and is not a state-dependent function.
-/

def marginAt
    (lambda : ℚ) (c : CellMarginData ℚ) : ℚ :=
  c.externalGamma - lambda * c.cellGamma

theorem marginAt_fixed_lambda_eq_declared
    (p : FixedLambdaParameters ℚ) (c : CellMarginData ℚ) :
    marginAt p.lambda c = c.candidateMargin := by
  rw [marginAt, p.lambda_eq_two, c.candidateMargin_eq]

def uniformCandidateFeasible
    (f : Declared577SparseFold) (lambda : ℚ) : Prop :=
  ∀ x ∈ unionRows f,
    1 < lambda ∧
      lambda < (unionRow f x).lambdaUpper ∧
      0 < marginAt lambda (unionRow f x)

def declaredUnionPositiveMargins
    (f : Declared577SparseFold) : Prop :=
  ∀ x ∈ unionRows f,
    0 < (unionRow f x).candidateMargin

/- The two partition-level strict-upper premises imply positivity for every
   tagged row in the union, not merely for one selected row per box label. -/
theorem union_positive_margins_of_uniform_strict_upper
    (f : Declared577SparseFold)
    (p : FixedLambdaParameters ℚ)
    (hupper : uniformStrictUpper f) :
    declaredUnionPositiveMargins f := by
  intro x hx
  rcases x with ⟨tag, i⟩
  cases tag
  · have hi : i ∈ f.eta27.rows :=
      (mem_unionRows_eta27_iff f i).mp hx
    have hrow : p.lambda < (f.eta27.row i).lambdaUpper :=
      hupper.1 i hi
    simpa [declaredUnionPositiveMargins, unionRow] using
      (strict_upper_iff_positive_margin p (f.eta27.row i)).mp hrow
  · have hi : i ∈ f.eta56.rows :=
      (mem_unionRows_eta56_iff f i).mp hx
    have hrow : p.lambda < (f.eta56.row i).lambdaUpper :=
      hupper.2 i hi
    simpa [declaredUnionPositiveMargins, unionRow] using
      (strict_upper_iff_positive_margin p (f.eta56.row i)).mp hrow

structure UniformLambdaFeasibilityWitness
    (f : Declared577SparseFold) where
  params : FixedLambdaParameters ℚ
  union_nonempty : (unionRows f).Nonempty
  feasible : uniformCandidateFeasible f params.lambda

theorem uniform_feasible_witness_has_lambda_two
    {f : Declared577SparseFold}
    (w : UniformLambdaFeasibilityWitness f) :
    w.params.lambda = 2 := by
  exact w.params.lambda_eq_two

/-!
All selected rows having the declared positive margin is enough to construct a
uniform candidate.  The strict upper bound is recovered rowwise from the
positive denominator and the imported ratio/margin bridge.
-/
theorem fixed_two_uniform_feasibility_of_positive_margins
    (f : Declared577SparseFold)
    (p : FixedLambdaParameters ℚ)
    (hnonempty : (unionRows f).Nonempty)
    (hpositive : declaredUnionPositiveMargins f) :
    UniformLambdaFeasibilityWitness f := by
  refine
    { params := p
      union_nonempty := hnonempty
      feasible := ?_ }
  intro x hx
  have hdeclared : 0 < (unionRow f x).candidateMargin := hpositive x hx
  have hupper : p.lambda < (unionRow f x).lambdaUpper := by
    exact (strict_upper_iff_positive_margin p (unionRow f x)).mpr hdeclared
  have hmargin : 0 < marginAt p.lambda (unionRow f x) := by
    rw [marginAt_fixed_lambda_eq_declared p (unionRow f x)]
    exact hdeclared
  exact ⟨exact_lambda_is_above_one p, hupper, hmargin⟩

theorem fixed_two_uniform_feasibility_of_uniform_strict_upper
    (f : Declared577SparseFold)
    (p : FixedLambdaParameters ℚ)
    (hnonempty : (unionRows f).Nonempty)
    (hupper : uniformStrictUpper f) :
    UniformLambdaFeasibilityWitness f := by
  apply fixed_two_uniform_feasibility_of_positive_margins f p hnonempty
  exact union_positive_margins_of_uniform_strict_upper f p hupper

/-!
This is the pointwise-to-uniform statement in its most direct form.  It keeps
the finite index set explicit and records that the witness is exactly lambda=2
with theta=1 through `FixedLambdaParameters`.
-/
theorem all_union_rows_positive_imply_fixed_lambda_two_feasible
    (f : Declared577SparseFold)
    (p : FixedLambdaParameters ℚ)
    (hnonempty : (unionRows f).Nonempty)
    (hpositive : declaredUnionPositiveMargins f) :
    ∃ w : UniformLambdaFeasibilityWitness f,
      w.params.lambda = 2 ∧ w.params.theta = 1 := by
  let w := fixed_two_uniform_feasibility_of_positive_margins
    f p hnonempty hpositive
  exact ⟨w, w.params.lambda_eq_two, w.params.theta_eq_one⟩

/- Admission boundary: this is finite row feasibility over supplied typed
   data.  Nonemptiness is explicit, but no completeness or source theorem is
   inferred from it. -/

#print axioms marginAt_fixed_lambda_eq_declared
#print axioms union_positive_margins_of_uniform_strict_upper
#print axioms uniform_feasible_witness_has_lambda_two
#print axioms fixed_two_uniform_feasibility_of_positive_margins
#print axioms fixed_two_uniform_feasibility_of_uniform_strict_upper
#print axioms all_union_rows_positive_imply_fixed_lambda_two_feasible

end
end RouteBFixedLambdaUniformFeasibility

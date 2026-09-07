import Mathlib.Data.Fin.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaAdmissibility

noncomputable section

/-!
This is a source-independent typed consumer for the two-row fixed-lambda
obligation.  It intentionally does not mention a CSV, a decimal parser, a
source evaluator, a DH interval, or a coverage predicate.

The parameter is a value of the type, not a function of the cell or state:
the same `lambda` is identified with both the affine PMI parameter and the
Schur-complement parameter.  The two rows are indexed by `Fin 2`; this is a
two-row interface, not a claim that a declared ledger contains all domain
cells.
-/

structure FixedLambdaParameters (α : Type*) [LinearOrderedField α] where
  lambda : α
  theta : α
  lambda_eq_two : lambda = 2
  theta_eq_one : theta = 1
  lambda_theta_relation : lambda = 1 + 1 / theta

def exactLambdaTwoThetaOne : FixedLambdaParameters ℚ where
  lambda := 2
  theta := 1
  lambda_eq_two := rfl
  theta_eq_one := rfl
  lambda_theta_relation := by norm_num

theorem exact_lambda_is_above_one
    {α : Type*} [LinearOrderedField α]
    (p : FixedLambdaParameters α) :
    (1 : α) < p.lambda := by
  rw [p.lambda_eq_two]
  norm_num

theorem exact_theta_is_positive
    {α : Type*} [LinearOrderedField α]
    (p : FixedLambdaParameters α) :
    (0 : α) < p.theta := by
  rw [p.theta_eq_one]
  norm_num

/-!
`CellMarginData` records the scalar quantities consumed by the fixed
parameter step.  `cellGamma_pos` is explicit because it is the denominator
side condition for the ratio.  The two equalities are typed interfaces to
external evidence; they do not themselves provide that evidence.
-/
structure CellMarginData (α : Type*) [LinearOrderedField α] where
  cellGamma : α
  externalGamma : α
  lambdaUpper : α
  candidateMargin : α
  cellGamma_pos : 0 < cellGamma
  lambdaUpper_eq_ratio : lambdaUpper = externalGamma / cellGamma
  candidateMargin_eq : candidateMargin = externalGamma - 2 * cellGamma

def rowStrict
    {α : Type*} [LinearOrderedField α]
    (p : FixedLambdaParameters α) (c : CellMarginData α) : Prop :=
  p.lambda < c.lambdaUpper ∧ 0 < c.candidateMargin

def rowAdmissible
    {α : Type*} [LinearOrderedField α]
    (p : FixedLambdaParameters α) (c : CellMarginData α) : Prop :=
  1 < p.lambda ∧ rowStrict p c

theorem rowStrict_iff_two_upper_and_positive
    {α : Type*} [LinearOrderedField α]
    (p : FixedLambdaParameters α) (c : CellMarginData α) :
    rowStrict p c ↔ 2 < c.lambdaUpper ∧ 0 < c.candidateMargin := by
  simp [rowStrict, p.lambda_eq_two]

theorem rowAdmissible_iff_two_upper_and_positive
    {α : Type*} [LinearOrderedField α]
    (p : FixedLambdaParameters α) (c : CellMarginData α) :
    rowAdmissible p c ↔ 2 < c.lambdaUpper ∧ 0 < c.candidateMargin := by
  simp [rowAdmissible, rowStrict, p.lambda_eq_two]

/- The exact ratio and positive denominator turn `lambdaUpper > 2` into the
   corresponding positive Schur margin.  This is scalar algebra only. -/
theorem positive_margin_of_strict_upper
    {α : Type*} [LinearOrderedField α]
    (c : CellMarginData α)
    (hupper : 2 < c.lambdaUpper) :
    0 < c.candidateMargin := by
  rw [c.candidateMargin_eq, c.lambdaUpper_eq_ratio] at hupper ⊢
  have hcross : 2 * c.cellGamma < c.externalGamma :=
    (lt_div_iff₀ c.cellGamma_pos).mp hupper
  exact sub_pos.mpr hcross

/-!
This record is the two-row consumer.  Both parameter slots are tied to the
single fixed value by equality fields, ruling out a state-dependent or
cell-dependent replacement between the affine PMI and Schur steps.
-/
structure TwoRowFixedLambdaWitness
    (α : Type*) [LinearOrderedField α] where
  params : FixedLambdaParameters α
  rows : Fin 2 → CellMarginData α
  affinePMILambda : α
  schurLambda : α
  affinePMILambda_eq : affinePMILambda = params.lambda
  schurLambda_eq : schurLambda = params.lambda
  upper_strict : ∀ i, 2 < (rows i).lambdaUpper
  margin_positive : ∀ i, 0 < (rows i).candidateMargin

def TwoRowFixedLambdaWitness.admissible
    {α : Type*} [LinearOrderedField α]
    (w : TwoRowFixedLambdaWitness α) : Prop :=
  ∀ i, 1 < w.affinePMILambda ∧
    w.affinePMILambda < (w.rows i).lambdaUpper ∧
    0 < (w.rows i).candidateMargin

theorem TwoRowFixedLambdaWitness.admissible_of_strict_rows
    {α : Type*} [LinearOrderedField α]
    (w : TwoRowFixedLambdaWitness α) :
    w.admissible := by
  intro i
  have h_one : (1 : α) < w.affinePMILambda := by
    have h_params : (1 : α) < w.params.lambda :=
      exact_lambda_is_above_one w.params
    simpa [w.affinePMILambda_eq] using h_params
  have h_upper : w.affinePMILambda < (w.rows i).lambdaUpper := by
    calc
      w.affinePMILambda = w.params.lambda := w.affinePMILambda_eq
      _ = 2 := w.params.lambda_eq_two
      _ < (w.rows i).lambdaUpper := w.upper_strict i
  exact ⟨h_one, h_upper, w.margin_positive i⟩

theorem TwoRowFixedLambdaWitness.schur_parameter_is_same
    {α : Type*} [LinearOrderedField α]
    (w : TwoRowFixedLambdaWitness α) :
    w.schurLambda = w.affinePMILambda := by
  rw [w.schurLambda_eq, w.affinePMILambda_eq]

/-!
The following constructor is useful when a caller has already supplied the
two strict obligations.  It deliberately asks for those obligations rather
than deriving them from a ledger hidden behind this file.
-/
def TwoRowFixedLambdaWitness.of_strict_rows
    {α : Type*} [LinearOrderedField α]
    (params : FixedLambdaParameters α)
    (rows : Fin 2 → CellMarginData α)
    (upper_strict : ∀ i, 2 < (rows i).lambdaUpper)
    (margin_positive : ∀ i, 0 < (rows i).candidateMargin) :
    TwoRowFixedLambdaWitness α :=
  { params := params
    rows := rows
    affinePMILambda := params.lambda
    schurLambda := params.lambda
    affinePMILambda_eq := rfl
    schurLambda_eq := rfl
    upper_strict := upper_strict
    margin_positive := margin_positive }

/-!
Admission boundary: these declarations establish only a typed finite
two-row implication.  A source/CSV adapter, true-DH interval coverage, an
all-cell theorem, a Lean build receipt, comparator acceptance, and registry
promotion must be supplied separately.
-/

#print axioms exact_lambda_is_above_one
#print axioms exact_theta_is_positive
#print axioms rowStrict_iff_two_upper_and_positive
#print axioms rowAdmissible_iff_two_upper_and_positive
#print axioms positive_margin_of_strict_upper
#print axioms TwoRowFixedLambdaWitness.admissible_of_strict_rows
#print axioms TwoRowFixedLambdaWitness.schur_parameter_is_same

end
end RouteBFixedLambdaAdmissibility

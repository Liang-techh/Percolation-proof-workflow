import NEW_FIXED_LAMBDA_ADMISSIBILITY_REAL_FINAL_STRICT_CONSUMER20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaExactStatementBoundary

open RouteBFixedLambdaAdmissibility
open RouteBFixedLambdaRealFinalStrictConsumer

noncomputable section

/-!
This sidecar isolates the statement boundary after the real strict consumer.
The mathematical strict inequality, its tagged statement metadata, and the
separate comparator-input premises are distinct contracts.  No comparator
execution or acceptance is encoded by the boundary itself.
-/

structure TaggedFinalStatement where
  tag : String
  binder : String
  order : String
  normalization : String
  target : Prop

def realFinalTaggedStatement
    {f : Declared577SparseFold}
    (q : FixedLambdaParameters ℚ)
    (coeff load : (EtaTag × Nat) → ℚ) : TaggedFinalStatement :=
  { tag := "routeb-fixed-lambda-real-final"
    binder := "q : FixedLambdaParameters ℚ; coeff load : (EtaTag × Nat) → ℚ"
    order := "realLoadTotal coeff load < realMarginTotal q coeff"
    normalization := "canonical ℚ→ℝ casts; subtraction normalized in ℝ"
    target := realLoadTotal coeff load < realMarginTotal q coeff }

/-!
Every field below is required.  In particular, the target equality is the
only proposition-level transport used by the consumer theorem; binder/order/
normalization equalities prevent a merely numerically similar statement from
being treated as the comparator target.
-/
structure ExactStatementBoundaryContract
    (source target : TaggedFinalStatement) where
  tag_eq : source.tag = target.tag
  binder_eq : source.binder = target.binder
  order_eq : source.order = target.order
  normalization_eq : source.normalization = target.normalization
  target_eq : source.target = target.target

/-!
These are comparator-input premises only.  They remain separate from the
mathematical boundary contract and do not by themselves assert acceptance.
-/
structure ComparatorAcceptancePremises
    (target : TaggedFinalStatement) where
  checker_statement : TaggedFinalStatement
  checker_target_eq : checker_statement.target = target.target
  exitCode : Int
  exit_code_zero : exitCode = 0
  output : String
  standalone_success_output : output = "Your solution is okay!"

def StatementBoundaryObstruction
    (source target : TaggedFinalStatement) : Prop :=
  source.tag ≠ target.tag ∨
    source.binder ≠ target.binder ∨
    source.order ≠ target.order ∨
    source.normalization ≠ target.normalization ∨
    source.target ≠ target.target

theorem boundary_obstruction_excludes_exact_contract
    {source target : TaggedFinalStatement}
    (obstruction : StatementBoundaryObstruction source target) :
    ¬ ExactStatementBoundaryContract source target := by
  intro boundary
  rcases obstruction with htag | hbinder | horder | hnormalization | htarget
  · exact htag boundary.tag_eq
  · exact hbinder boundary.binder_eq
  · exact horder boundary.order_eq
  · exact hnormalization boundary.normalization_eq
  · exact htarget boundary.target_eq

/-!
The strict inequality is consumed only after the complete explicit statement
boundary is supplied.  Comparator premises are intentionally absent here.
-/
theorem consume_real_strict_inequality_through_exact_boundary
    {f : Declared577SparseFold}
    (q : FixedLambdaParameters ℚ)
    (coeff load : (EtaTag × Nat) → ℚ)
    {target : TaggedFinalStatement}
    (boundary : ExactStatementBoundaryContract
      (realFinalTaggedStatement q coeff load) target)
    (hstrict : realLoadTotal coeff load < realMarginTotal q coeff) :
    target.target := by
  exact boundary.target_eq ▸ hstrict

/-!
The following contract packages the separate real strict fact, exact
statement equivalence, and comparator-input premises without turning them into
an acceptance theorem.
-/
structure FinalStatementComparatorBoundary
    {f : Declared577SparseFold}
    (q : FixedLambdaParameters ℚ)
    (coeff load : (EtaTag × Nat) → ℚ)
    (target : TaggedFinalStatement) where
  strict_real_inequality : realLoadTotal coeff load < realMarginTotal q coeff
  statement_boundary : ExactStatementBoundaryContract
    (realFinalTaggedStatement q coeff load) target
  comparator_premises : ComparatorAcceptancePremises target

theorem consume_packaged_boundary_target
    {f : Declared577SparseFold}
    (q : FixedLambdaParameters ℚ)
    (coeff load : (EtaTag × Nat) → ℚ)
    {target : TaggedFinalStatement}
    (contract : FinalStatementComparatorBoundary q coeff load target) :
    target.target := by
  exact consume_real_strict_inequality_through_exact_boundary q coeff load
    contract.statement_boundary contract.strict_real_inequality

/- Admission boundary: this sidecar records a typed statement-equivalence
   gate and separate comparator-input premises only.  It does not run the
   comparator, assert comparator acceptance, promote a registry entry, or
   establish source/coverage/receipt evidence. -/

#print axioms boundary_obstruction_excludes_exact_contract
#print axioms consume_real_strict_inequality_through_exact_boundary
#print axioms consume_packaged_boundary_target

end
end RouteBFixedLambdaExactStatementBoundary

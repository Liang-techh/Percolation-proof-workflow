import NEW_FIXED_LAMBDA_ADMISSIBILITY_EXACT_STATEMENT_BOUNDARY20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaComparatorReceiptAdmission

open RouteBFixedLambdaExactStatementBoundary

noncomputable section

/-!
This sidecar defines a fail-closed comparator-receipt admission boundary.
Statement target equivalence, checker result, exact standalone output,
artifact hash, provenance, and registry promotion are separate contracts.
Nothing here runs a checker or promotes a registry entry.
-/

def comparatorSuccessOutput : String := "Your solution is okay!"

structure ComparatorReceiptRecord
    (source checker : TaggedFinalStatement) where
  statement_target_equivalence :
    Option (ExactStatementBoundaryContract source checker)
  checker_exit_code : Option Int
  standalone_success_output : Option String
  artifact_hash : Option String
  provenance : Option String

def ComparatorReceiptComplete
    {source checker : TaggedFinalStatement}
    (record : ComparatorReceiptRecord source checker) : Prop :=
  (∃ boundary,
      record.statement_target_equivalence = some boundary) ∧
    record.checker_exit_code = some 0 ∧
    record.standalone_success_output = some comparatorSuccessOutput ∧
    (∃ hash, record.artifact_hash = some hash ∧ hash ≠ "") ∧
    (∃ origin, record.provenance = some origin ∧ origin ≠ "")

/-!
This type is receipt admission only.  Registry promotion is intentionally not
a field of it and therefore cannot be inferred from receipt completeness.
-/
structure ComparatorReceiptAdmissionContract
    {source checker : TaggedFinalStatement}
    (record : ComparatorReceiptRecord source checker) where
  complete : ComparatorReceiptComplete record

inductive MissingComparatorReceiptField
    {source checker : TaggedFinalStatement}
    (record : ComparatorReceiptRecord source checker) : Prop
  | statement_target_equivalence
      (missing : record.statement_target_equivalence = none)
  | checker_exit_code
      (missing : record.checker_exit_code ≠ some 0)
  | standalone_success_output
      (missing :
        record.standalone_success_output ≠ some comparatorSuccessOutput)
  | artifact_hash
      (missing : ¬ ∃ hash,
        record.artifact_hash = some hash ∧ hash ≠ "")
  | provenance
      (missing : ¬ ∃ origin,
        record.provenance = some origin ∧ origin ≠ "")

/-!
Any missing receipt field makes the admission type uninhabited.  The theorem
does not classify the record as rejected: absence remains fail-closed pending
until the missing authoritative evidence is supplied.
-/
theorem missing_receipt_field_is_fail_closed
    {source checker : TaggedFinalStatement}
    {record : ComparatorReceiptRecord source checker}
    (missing : MissingComparatorReceiptField record) :
    ¬ Nonempty (ComparatorReceiptAdmissionContract record) := by
  intro admission
  rcases admission with ⟨admitted⟩
  have complete := admitted.complete
  rcases missing with hboundary | hexit | houtput | hhash | horigin
  · rcases complete.1 with ⟨boundary, hsome⟩
    exact hboundary (by
      rw [hsome]
      rfl)
  · exact hexit complete.2.1
  · exact houtput complete.2.2.1
  · exact hhash complete.2.2.2.1
  · exact horigin complete.2.2.2.2

/-!
Registry promotion is a separate explicit gate.  Even a complete receipt has
no promotion field and no automatic route to this structure.
-/
structure ExplicitRegistryPromotionGate
    {source checker : TaggedFinalStatement}
    (record : ComparatorReceiptRecord source checker)
    (admission : ComparatorReceiptAdmissionContract record) where
  registry_entry : String
  explicit_promotion_authorization : Prop
  authorization_proof : explicit_promotion_authorization

/- Admission boundary: no checker execution, exact hash algorithm, external
   provenance validation, comparator acceptance, VERIFIED status, or registry
   promotion is asserted.  Missing authoritative evidence remains fail-closed. -/

#print axioms missing_receipt_field_is_fail_closed

end
end RouteBFixedLambdaComparatorReceiptAdmission

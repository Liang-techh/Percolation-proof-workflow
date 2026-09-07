import NEW_FIXED_LAMBDA_ADMISSIBILITY_EXACT_STATEMENT_BOUNDARY20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaTypedReceiptAudit

open RouteBFixedLambdaExactStatementBoundary

noncomputable section

/-!
This sidecar is a typed audit seam for the fixed-lambda comparator receipt.
Byte hashes, source artifacts, exact statement digests, checker results, and
registry promotion are kept distinct.  Pending means authoritative fields are
missing; rejected means supplied fields mismatch.  Neither state is promoted
to VERIFIED or to a registry entry here.
-/

structure ByteHash where
  value : String

structure ExactStatementDigest where
  value : String

structure SourceArtifact where
  artifact_id : String
  provenance : Option String
  byte_hash : Option ByteHash

inductive StatementTargetEvidence
    (source checker : TaggedFinalStatement) where
  | missing
  | equivalent (boundary : ExactStatementBoundaryContract source checker)
  | mismatch

structure TypedComparatorReceiptRecord
    (source checker : TaggedFinalStatement) where
  source_artifact : Option SourceArtifact
  artifact_hash : Option ByteHash
  exact_statement_digest : Option ExactStatementDigest
  statement_target : StatementTargetEvidence source checker
  checker_exit_code : Option Int
  checker_output : Option String

def ReceiptAuditPending
    {source checker : TaggedFinalStatement}
    (record : TypedComparatorReceiptRecord source checker) : Prop :=
  record.source_artifact = none ∨
    (∃ artifact,
      record.source_artifact = some artifact ∧
        (artifact.provenance = none ∨ artifact.byte_hash = none)) ∨
    record.artifact_hash = none ∨
    record.exact_statement_digest = none ∨
    record.statement_target = StatementTargetEvidence.missing ∨
    record.checker_exit_code = none ∨
    record.checker_output = none

def ReceiptAuditRejected
    {source checker : TaggedFinalStatement}
    (expectedHash : ByteHash)
    (expectedDigest : ExactStatementDigest)
    (record : TypedComparatorReceiptRecord source checker) : Prop :=
  (∃ artifact,
      record.source_artifact = some artifact ∧
        (artifact.artifact_id = "" ∨
          (∃ origin, artifact.provenance = some origin ∧ origin = "") ∨
          (∃ hash, artifact.byte_hash = some hash ∧ hash ≠ expectedHash))) ∨
    (∃ hash,
      record.artifact_hash = some hash ∧ hash ≠ expectedHash) ∨
    (∃ digest,
      record.exact_statement_digest = some digest ∧ digest ≠ expectedDigest) ∨
    record.statement_target = StatementTargetEvidence.mismatch ∨
    (∃ code,
      record.checker_exit_code = some code ∧ code ≠ 0) ∨
    (∃ output,
      record.checker_output = some output ∧
        output ≠ comparatorSuccessOutput)

def ReceiptAuditComplete
    {source checker : TaggedFinalStatement}
    (expectedHash : ByteHash)
    (expectedDigest : ExactStatementDigest)
    (record : TypedComparatorReceiptRecord source checker) : Prop :=
  (∃ artifact,
      record.source_artifact = some artifact ∧
        artifact.artifact_id ≠ "" ∧
        (∃ origin, artifact.provenance = some origin ∧ origin ≠ "") ∧
        artifact.byte_hash = some expectedHash) ∧
    record.artifact_hash = some expectedHash ∧
    record.exact_statement_digest = some expectedDigest ∧
    (∃ boundary,
      record.statement_target = StatementTargetEvidence.equivalent boundary) ∧
    record.checker_exit_code = some 0 ∧
    record.checker_output = some comparatorSuccessOutput

structure ComparatorReceiptAuditAdmissionContract
    {source checker : TaggedFinalStatement}
    (expectedHash : ByteHash)
    (expectedDigest : ExactStatementDigest)
    (record : TypedComparatorReceiptRecord source checker) where
  complete : ReceiptAuditComplete expectedHash expectedDigest record
  pending_absent : ¬ ReceiptAuditPending record
  rejected_absent : ¬ ReceiptAuditRejected expectedHash expectedDigest record

inductive MissingTypedReceiptField
    {source checker : TaggedFinalStatement}
    (record : TypedComparatorReceiptRecord source checker) : Prop
  | source_artifact
      (missing : record.source_artifact = none)
  | source_artifact_provenance
      (missing : ∃ artifact,
        record.source_artifact = some artifact ∧ artifact.provenance = none)
  | source_artifact_byte_hash
      (missing : ∃ artifact,
        record.source_artifact = some artifact ∧ artifact.byte_hash = none)
  | artifact_hash
      (missing : record.artifact_hash = none)
  | exact_statement_digest
      (missing : record.exact_statement_digest = none)
  | statement_target_equivalence
      (missing : record.statement_target = StatementTargetEvidence.missing)
  | checker_exit_code
      (missing : record.checker_exit_code = none)
  | checker_output
      (missing : record.checker_output = none)

theorem missing_field_is_pending
    {source checker : TaggedFinalStatement}
    {record : TypedComparatorReceiptRecord source checker}
    (missing : MissingTypedReceiptField record) :
    ReceiptAuditPending record := by
  rcases missing with hsource | hprov | hbyte | hhash | hdigest |
    hstatement | hexit | houtput
  · exact Or.inl hsource
  · exact Or.inr (Or.inl hprov)
  · exact Or.inr (Or.inl hbyte)
  · exact Or.inr (Or.inr (Or.inl hhash))
  · exact Or.inr (Or.inr (Or.inr (Or.inl hdigest)))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl hstatement))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl hexit)))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr houtput)))))

theorem pending_is_fail_closed
    {source checker : TaggedFinalStatement}
    {expectedHash : ByteHash}
    {expectedDigest : ExactStatementDigest}
    {record : TypedComparatorReceiptRecord source checker}
    (pending : ReceiptAuditPending record) :
    ¬ Nonempty
      (ComparatorReceiptAuditAdmissionContract expectedHash expectedDigest record) := by
  intro admission
  rcases admission with ⟨admitted⟩
  exact admitted.pending_absent pending

theorem rejected_is_fail_closed
    {source checker : TaggedFinalStatement}
    {expectedHash : ByteHash}
    {expectedDigest : ExactStatementDigest}
    {record : TypedComparatorReceiptRecord source checker}
    (rejected : ReceiptAuditRejected expectedHash expectedDigest record) :
    ¬ Nonempty
      (ComparatorReceiptAuditAdmissionContract expectedHash expectedDigest record) := by
  intro admission
  rcases admission with ⟨admitted⟩
  exact admitted.rejected_absent rejected

/-!
The audit contract deliberately does not construct an admission from
`ReceiptAuditComplete` alone: an explicit non-pending/non-rejected audit gate
is retained.  Hash algorithm validation, byte-level source binding, and
provenance-chain validation remain external obligations.
-/

#print axioms missing_field_is_pending
#print axioms pending_is_fail_closed
#print axioms rejected_is_fail_closed

end
end RouteBFixedLambdaTypedReceiptAudit

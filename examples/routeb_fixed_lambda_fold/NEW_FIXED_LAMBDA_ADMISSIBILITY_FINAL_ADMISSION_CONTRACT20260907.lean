import NEW_FIXED_LAMBDA_ADMISSIBILITY_CANONICAL_DIGEST_NORMALIZATION20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaFinalAdmissionContract

open RouteBFixedLambdaExactStatementBoundary
open RouteBFixedLambdaTypedReceiptAudit
open RouteBFixedLambdaCanonicalDigestNormalization

noncomputable section

/-!
This sidecar is the final composition boundary for fixed-lambda receipt
admission.  It combines the exact tagged statement boundary, an explicit
representation binding into the canonical target proposition, the typed
checker receipt, and the canonical digest receipt.  No verification or
registry status is produced.
-/

structure FinalAdmissionRecord
    (taggedSource taggedChecker : TaggedFinalStatement)
    (canonicalCandidate canonicalTarget : CanonicalStatementForm)
    (canonicalTargetProp : Prop) where
  exact_statement_boundary :
    Option (ExactStatementBoundaryContract taggedSource taggedChecker)
  representation_binding : Option (taggedChecker.target = canonicalTargetProp)
  typed_receipt : Option (TypedComparatorReceiptRecord taggedSource taggedChecker)
  canonical_receipt :
    Option (CanonicalDigestReceiptRecord canonicalCandidate canonicalTarget)

def FinalAdmissionPending
    {taggedSource taggedChecker : TaggedFinalStatement}
    {canonicalCandidate canonicalTarget : CanonicalStatementForm}
    {canonicalTargetProp : Prop}
    (record : FinalAdmissionRecord taggedSource taggedChecker
      canonicalCandidate canonicalTarget canonicalTargetProp) : Prop :=
  record.exact_statement_boundary = none ∨
    record.representation_binding = none ∨
    record.typed_receipt = none ∨
    record.canonical_receipt = none ∨
    (∃ typed,
      record.typed_receipt = some typed ∧ ReceiptAuditPending typed) ∨
    (∃ canonical,
      record.canonical_receipt = some canonical ∧ CanonicalReceiptPending canonical)

def FinalAdmissionRejected
    {taggedSource taggedChecker : TaggedFinalStatement}
    {canonicalCandidate canonicalTarget : CanonicalStatementForm}
    {canonicalTargetProp : Prop}
    (oracle : CanonicalDigestOracle)
    (expectedHash : ByteHash)
    (expectedDigest : ExactStatementDigest)
    (record : FinalAdmissionRecord taggedSource taggedChecker
      canonicalCandidate canonicalTarget canonicalTargetProp) : Prop :=
  (∃ typed,
    record.typed_receipt = some typed ∧
      ReceiptAuditRejected expectedHash expectedDigest typed) ∨
  (∃ canonical,
    record.canonical_receipt = some canonical ∧
      CanonicalReceiptRejected oracle expectedHash expectedDigest canonical)

/-!
The final contract keeps each layer's complete admission witness and adds
explicit cross-layer equalities for source artifact, byte hash, and statement
digest.  It has no field that could be read as VERIFIED or registry promotion.
-/
structure FinalAdmissionContract
    {taggedSource taggedChecker : TaggedFinalStatement}
    {canonicalCandidate canonicalTarget : CanonicalStatementForm}
    {canonicalTargetProp : Prop}
    (oracle : CanonicalDigestOracle)
    (expectedHash : ByteHash)
    (expectedDigest : ExactStatementDigest)
    (record : FinalAdmissionRecord taggedSource taggedChecker
      canonicalCandidate canonicalTarget canonicalTargetProp) where
  boundary : ExactStatementBoundaryContract taggedSource taggedChecker
  representation_binding : taggedChecker.target = canonicalTargetProp
  typed : TypedComparatorReceiptRecord taggedSource taggedChecker
  canonical : CanonicalDigestReceiptRecord canonicalCandidate canonicalTarget
  boundary_present : record.exact_statement_boundary = some boundary
  representation_binding_present :
    record.representation_binding = some representation_binding
  typed_present : record.typed_receipt = some typed
  canonical_present : record.canonical_receipt = some canonical
  typed_admission :
    ComparatorReceiptAuditAdmissionContract expectedHash expectedDigest typed
  canonical_admission :
    CanonicalDigestReceiptAdmissionContract
      oracle expectedHash expectedDigest canonical
  source_artifact_eq : typed.source_artifact = canonical.source_artifact
  byte_hash_eq : typed.artifact_hash = canonical.artifact_hash
  statement_digest_eq :
    typed.exact_statement_digest = canonical.exact_statement_digest
  pending_absent : ¬ FinalAdmissionPending record
  rejected_absent :
    ¬ FinalAdmissionRejected oracle expectedHash expectedDigest record

theorem pending_final_admission_is_impossible
    {taggedSource taggedChecker : TaggedFinalStatement}
    {canonicalCandidate canonicalTarget : CanonicalStatementForm}
    {canonicalTargetProp : Prop}
    {oracle : CanonicalDigestOracle}
    {expectedHash : ByteHash}
    {expectedDigest : ExactStatementDigest}
    {record : FinalAdmissionRecord taggedSource taggedChecker
      canonicalCandidate canonicalTarget canonicalTargetProp}
    (pending : FinalAdmissionPending record) :
    ¬ Nonempty
      (FinalAdmissionContract oracle expectedHash expectedDigest record) := by
  intro admission
  rcases admission with ⟨admitted⟩
  exact admitted.pending_absent pending

theorem rejected_final_admission_is_impossible
    {taggedSource taggedChecker : TaggedFinalStatement}
    {canonicalCandidate canonicalTarget : CanonicalStatementForm}
    {canonicalTargetProp : Prop}
    {oracle : CanonicalDigestOracle}
    {expectedHash : ByteHash}
    {expectedDigest : ExactStatementDigest}
    {record : FinalAdmissionRecord taggedSource taggedChecker
      canonicalCandidate canonicalTarget canonicalTargetProp}
    (rejected : FinalAdmissionRejected
      oracle expectedHash expectedDigest record) :
    ¬ Nonempty
      (FinalAdmissionContract oracle expectedHash expectedDigest record) := by
  intro admission
  rcases admission with ⟨admitted⟩
  exact admitted.rejected_absent rejected

/-!
`FinalAdmissionContract` is deliberately only an evidence bundle.  Its
existence does not define a VERIFIED proposition, a registry transition, or a
comparator execution result; those remain separate downstream gates.
-/

#print axioms pending_final_admission_is_impossible
#print axioms rejected_final_admission_is_impossible

end
end RouteBFixedLambdaFinalAdmissionContract

import NEW_FIXED_LAMBDA_ADMISSIBILITY_PINNED_KERNEL_RECEIPT_FAIL_CLOSED20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaVerifiedRegistryEntryInvariant

open RouteBFixedLambdaExactStatementBoundary
open RouteBFixedLambdaTypedReceiptAudit
open RouteBFixedLambdaCanonicalDigestNormalization
open RouteBFixedLambdaFinalAdmissionContract
open RouteBFixedLambdaPinnedKernelReceiptFailClosed

noncomputable section

/-!
This sidecar defines only the constructor invariant for a future verified
registry entry.  The type has one evidence-bundle path; compiled-only,
pending, and rejected inputs have no constructor path to an entry.
-/

structure CompiledCandidateOnly where
  artifact_hash : ByteHash
  compiled_exit_code : Int
  evidence_complete : Bool

structure ExplicitVerifiedEvidenceBundle
    {taggedSource taggedChecker : TaggedFinalStatement}
    {canonicalCandidate canonicalTarget : CanonicalStatementForm}
    {canonicalTargetProp : Prop}
    (oracle : CanonicalDigestOracle)
    (expectedHash : ByteHash)
    (expectedDigest : ExactStatementDigest)
    (expectedProjectCommit expectedToolchain expectedTheorem : String)
    (expectedKernelArtifactDigest : KernelArtifactDigest)
    (finalRecord : FinalAdmissionRecord taggedSource taggedChecker
      canonicalCandidate canonicalTarget canonicalTargetProp)
    (kernelRecord : PinnedKernelReceiptAuditRecord) where
  final_admission : FinalAdmissionContract oracle expectedHash expectedDigest finalRecord
  kernel_admission : PinnedKernelReceiptAdmissionContract
    expectedProjectCommit expectedToolchain expectedTheorem
    expectedKernelArtifactDigest kernelRecord
  comparator_receipt : ComparatorReceiptReference
  comparator_receipt_complete :
    ComparatorReceiptReferenceComplete expectedHash expectedDigest comparator_receipt
  source_identity : ProvenanceSourceIdentity
  source_identity_complete :
    ProvenanceSourceIdentityComplete expectedHash source_identity
  promotion_authorization : IndependentPromotionAuthorization
  promotion_authorization_complete :
    IndependentPromotionAuthorizationComplete promotion_authorization
  artifact_hash_eq : comparator_receipt.artifact_hash = source_identity.byte_hash
  statement_digest_eq : comparator_receipt.statement_digest = expectedDigest
  kernel_artifact_digest_repr_eq :
    expectedKernelArtifactDigest.value = expectedHash.value

structure VerifiedRegistryEntryInvariant
    {taggedSource taggedChecker : TaggedFinalStatement}
    {canonicalCandidate canonicalTarget : CanonicalStatementForm}
    {canonicalTargetProp : Prop}
    (oracle : CanonicalDigestOracle)
    (expectedHash : ByteHash)
    (expectedDigest : ExactStatementDigest)
    (expectedProjectCommit expectedToolchain expectedTheorem : String)
    (expectedKernelArtifactDigest : KernelArtifactDigest)
    (finalRecord : FinalAdmissionRecord taggedSource taggedChecker
      canonicalCandidate canonicalTarget canonicalTargetProp)
    (kernelRecord : PinnedKernelReceiptAuditRecord) where
  evidence : ExplicitVerifiedEvidenceBundle
    oracle expectedHash expectedDigest
    expectedProjectCommit expectedToolchain expectedTheorem
    expectedKernelArtifactDigest finalRecord kernelRecord

inductive RegistryAdmissionInput
    {taggedSource taggedChecker : TaggedFinalStatement}
    {canonicalCandidate canonicalTarget : CanonicalStatementForm}
    {canonicalTargetProp : Prop}
    (oracle : CanonicalDigestOracle)
    (expectedHash : ByteHash)
    (expectedDigest : ExactStatementDigest)
    (expectedProjectCommit expectedToolchain expectedTheorem : String)
    (expectedKernelArtifactDigest : KernelArtifactDigest)
    (finalRecord : FinalAdmissionRecord taggedSource taggedChecker
      canonicalCandidate canonicalTarget canonicalTargetProp)
    (kernelRecord : PinnedKernelReceiptAuditRecord) where
  | compiledOnly (candidate : CompiledCandidateOnly)
  | pending (reason : String)
  | rejected (reason : String)
  | explicit
      (bundle : ExplicitVerifiedEvidenceBundle
        oracle expectedHash expectedDigest
        expectedProjectCommit expectedToolchain expectedTheorem
        expectedKernelArtifactDigest finalRecord kernelRecord)

def admitRegistryEntry
    {taggedSource taggedChecker : TaggedFinalStatement}
    {canonicalCandidate canonicalTarget : CanonicalStatementForm}
    {canonicalTargetProp : Prop}
    (oracle : CanonicalDigestOracle)
    (expectedHash : ByteHash)
    (expectedDigest : ExactStatementDigest)
    (expectedProjectCommit expectedToolchain expectedTheorem : String)
    (expectedKernelArtifactDigest : KernelArtifactDigest)
    (finalRecord : FinalAdmissionRecord taggedSource taggedChecker
      canonicalCandidate canonicalTarget canonicalTargetProp)
    (kernelRecord : PinnedKernelReceiptAuditRecord) :
    RegistryAdmissionInput oracle expectedHash expectedDigest
      expectedProjectCommit expectedToolchain expectedTheorem
      expectedKernelArtifactDigest finalRecord kernelRecord →
      Option (VerifiedRegistryEntryInvariant oracle expectedHash expectedDigest
        expectedProjectCommit expectedToolchain expectedTheorem
        expectedKernelArtifactDigest finalRecord kernelRecord)
  | .compiledOnly _ => none
  | .pending _ => none
  | .rejected _ => none
  | .explicit bundle => some ⟨bundle⟩

theorem compiled_candidate_only_is_not_admitted
    {taggedSource taggedChecker : TaggedFinalStatement}
    {canonicalCandidate canonicalTarget : CanonicalStatementForm}
    {canonicalTargetProp : Prop}
    (oracle : CanonicalDigestOracle)
    (expectedHash : ByteHash)
    (expectedDigest : ExactStatementDigest)
    (expectedProjectCommit expectedToolchain expectedTheorem : String)
    (expectedKernelArtifactDigest : KernelArtifactDigest)
    (finalRecord : FinalAdmissionRecord taggedSource taggedChecker
      canonicalCandidate canonicalTarget canonicalTargetProp)
    (kernelRecord : PinnedKernelReceiptAuditRecord)
    (candidate : CompiledCandidateOnly) :
    admitRegistryEntry oracle expectedHash expectedDigest
      expectedProjectCommit expectedToolchain expectedTheorem
      expectedKernelArtifactDigest finalRecord kernelRecord
      (.compiledOnly candidate) = none := by
  rfl

theorem pending_input_is_not_admitted
    {taggedSource taggedChecker : TaggedFinalStatement}
    {canonicalCandidate canonicalTarget : CanonicalStatementForm}
    {canonicalTargetProp : Prop}
    (oracle : CanonicalDigestOracle)
    (expectedHash : ByteHash)
    (expectedDigest : ExactStatementDigest)
    (expectedProjectCommit expectedToolchain expectedTheorem : String)
    (expectedKernelArtifactDigest : KernelArtifactDigest)
    (finalRecord : FinalAdmissionRecord taggedSource taggedChecker
      canonicalCandidate canonicalTarget canonicalTargetProp)
    (kernelRecord : PinnedKernelReceiptAuditRecord)
    (reason : String) :
    admitRegistryEntry oracle expectedHash expectedDigest
      expectedProjectCommit expectedToolchain expectedTheorem
      expectedKernelArtifactDigest finalRecord kernelRecord
      (.pending reason) = none := by
  rfl

theorem rejected_input_is_not_admitted
    {taggedSource taggedChecker : TaggedFinalStatement}
    {canonicalCandidate canonicalTarget : CanonicalStatementForm}
    {canonicalTargetProp : Prop}
    (oracle : CanonicalDigestOracle)
    (expectedHash : ByteHash)
    (expectedDigest : ExactStatementDigest)
    (expectedProjectCommit expectedToolchain expectedTheorem : String)
    (expectedKernelArtifactDigest : KernelArtifactDigest)
    (finalRecord : FinalAdmissionRecord taggedSource taggedChecker
      canonicalCandidate canonicalTarget canonicalTargetProp)
    (kernelRecord : PinnedKernelReceiptAuditRecord)
    (reason : String) :
    admitRegistryEntry oracle expectedHash expectedDigest
      expectedProjectCommit expectedToolchain expectedTheorem
      expectedKernelArtifactDigest finalRecord kernelRecord
      (.rejected reason) = none := by
  rfl

/- Admission boundary: no entry instance is constructed here.  The only
   `some` branch consumes the explicit evidence bundle, including final
   admission, pinned zero-audit kernel receipt, comparator/provenance identity,
   digest equalities, and independent authorization. -/

#print axioms compiled_candidate_only_is_not_admitted
#print axioms pending_input_is_not_admitted
#print axioms rejected_input_is_not_admitted

end
end RouteBFixedLambdaVerifiedRegistryEntryInvariant

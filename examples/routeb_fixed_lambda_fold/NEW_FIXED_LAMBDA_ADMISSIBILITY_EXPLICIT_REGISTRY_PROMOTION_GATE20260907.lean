import NEW_FIXED_LAMBDA_ADMISSIBILITY_FINAL_ADMISSION_CONTRACT20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaExplicitRegistryPromotionGate

open RouteBFixedLambdaExactStatementBoundary
open RouteBFixedLambdaTypedReceiptAudit
open RouteBFixedLambdaCanonicalDigestNormalization
open RouteBFixedLambdaFinalAdmissionContract

noncomputable section

/-!
This sidecar is the explicit authorization boundary after final admission.
Final admission, a pinned Lean kernel receipt, a comparator receipt, source /
provenance identity, and promotion authorization remain separate evidence
objects.  No object below defines VERIFIED or performs a registry mutation.
-/

structure PinnedLeanKernelReceipt where
  lean_version : String
  lake_manifest_digest : String
  theorem_name : String
  receipt_digest : String
  exit_code : Int

def PinnedLeanKernelReceiptComplete
    (receipt : PinnedLeanKernelReceipt) : Prop :=
  receipt.lean_version ≠ "" ∧
    receipt.lake_manifest_digest ≠ "" ∧
    receipt.theorem_name ≠ "" ∧
    receipt.receipt_digest ≠ "" ∧
    receipt.exit_code = 0

structure ComparatorReceiptReference where
  receipt_id : String
  artifact_hash : ByteHash
  statement_digest : ExactStatementDigest
  exit_code : Int
  output : String

def ComparatorReceiptReferenceComplete
    (expectedHash : ByteHash)
    (expectedDigest : ExactStatementDigest)
    (receipt : ComparatorReceiptReference) : Prop :=
  receipt.receipt_id ≠ "" ∧
    receipt.artifact_hash = expectedHash ∧
    receipt.statement_digest = expectedDigest ∧
    receipt.exit_code = 0 ∧
    receipt.output = comparatorSuccessOutput

structure ProvenanceSourceIdentity where
  source_root : String
  artifact_id : String
  provenance_id : String
  byte_hash : ByteHash

def ProvenanceSourceIdentityComplete
    (expectedHash : ByteHash)
    (identity : ProvenanceSourceIdentity) : Prop :=
  identity.source_root ≠ "" ∧
    identity.artifact_id ≠ "" ∧
    identity.provenance_id ≠ "" ∧
    identity.byte_hash = expectedHash

structure IndependentPromotionAuthorization where
  authorization_id : String
  actor : String
  scope : String
  decision : Bool

def IndependentPromotionAuthorizationComplete
    (authorization : IndependentPromotionAuthorization) : Prop :=
  authorization.authorization_id ≠ "" ∧
    authorization.actor ≠ "" ∧
    authorization.scope ≠ "" ∧
    authorization.decision = true

structure RegistryPromotionRecord
    {taggedSource taggedChecker : TaggedFinalStatement}
    {canonicalCandidate canonicalTarget : CanonicalStatementForm}
    {canonicalTargetProp : Prop}
    (oracle : CanonicalDigestOracle)
    (expectedHash : ByteHash)
    (expectedDigest : ExactStatementDigest)
    (finalRecord : FinalAdmissionRecord taggedSource taggedChecker
      canonicalCandidate canonicalTarget canonicalTargetProp) where
  final_admission :
    Option (FinalAdmissionContract oracle expectedHash expectedDigest finalRecord)
  kernel_receipt : Option PinnedLeanKernelReceipt
  comparator_receipt : Option ComparatorReceiptReference
  source_identity : Option ProvenanceSourceIdentity
  promotion_authorization : Option IndependentPromotionAuthorization

def RegistryPromotionPending
    {taggedSource taggedChecker : TaggedFinalStatement}
    {canonicalCandidate canonicalTarget : CanonicalStatementForm}
    {canonicalTargetProp : Prop}
    {oracle : CanonicalDigestOracle}
    {expectedHash : ByteHash}
    {expectedDigest : ExactStatementDigest}
    {finalRecord : FinalAdmissionRecord taggedSource taggedChecker
      canonicalCandidate canonicalTarget canonicalTargetProp}
    (record : RegistryPromotionRecord oracle expectedHash expectedDigest finalRecord) : Prop :=
  record.final_admission = none ∨
    record.kernel_receipt = none ∨
    record.comparator_receipt = none ∨
    record.source_identity = none ∨
    record.promotion_authorization = none

def RegistryPromotionRejected
    {taggedSource taggedChecker : TaggedFinalStatement}
    {canonicalCandidate canonicalTarget : CanonicalStatementForm}
    {canonicalTargetProp : Prop}
    (oracle : CanonicalDigestOracle)
    (expectedHash : ByteHash)
    (expectedDigest : ExactStatementDigest)
    {finalRecord : FinalAdmissionRecord taggedSource taggedChecker
      canonicalCandidate canonicalTarget canonicalTargetProp}
    (record : RegistryPromotionRecord oracle expectedHash expectedDigest finalRecord) : Prop :=
  (∃ receipt,
    record.kernel_receipt = some receipt ∧
      ¬ PinnedLeanKernelReceiptComplete receipt) ∨
  (∃ receipt,
    record.comparator_receipt = some receipt ∧
      ¬ ComparatorReceiptReferenceComplete expectedHash expectedDigest receipt) ∨
  (∃ identity,
    record.source_identity = some identity ∧
      ¬ ProvenanceSourceIdentityComplete expectedHash identity) ∨
  (∃ authorization,
    record.promotion_authorization = some authorization ∧
      ¬ IndependentPromotionAuthorizationComplete authorization)

/-!
This is an evidence contract, not a promotion command.  Every component is
required independently and the negative pending/rejected gates are retained.
-/
structure ExplicitRegistryPromotionContract
    {taggedSource taggedChecker : TaggedFinalStatement}
    {canonicalCandidate canonicalTarget : CanonicalStatementForm}
    {canonicalTargetProp : Prop}
    (oracle : CanonicalDigestOracle)
    (expectedHash : ByteHash)
    (expectedDigest : ExactStatementDigest)
    {finalRecord : FinalAdmissionRecord taggedSource taggedChecker
      canonicalCandidate canonicalTarget canonicalTargetProp}
    (record : RegistryPromotionRecord oracle expectedHash expectedDigest finalRecord) where
  final_admission : FinalAdmissionContract oracle expectedHash expectedDigest finalRecord
  kernel_receipt : PinnedLeanKernelReceipt
  comparator_receipt : ComparatorReceiptReference
  source_identity : ProvenanceSourceIdentity
  promotion_authorization : IndependentPromotionAuthorization
  final_admission_present : record.final_admission = some final_admission
  kernel_receipt_present : record.kernel_receipt = some kernel_receipt
  comparator_receipt_present : record.comparator_receipt = some comparator_receipt
  source_identity_present : record.source_identity = some source_identity
  promotion_authorization_present :
    record.promotion_authorization = some promotion_authorization
  kernel_receipt_complete : PinnedLeanKernelReceiptComplete kernel_receipt
  comparator_receipt_complete :
    ComparatorReceiptReferenceComplete expectedHash expectedDigest comparator_receipt
  source_identity_complete :
    ProvenanceSourceIdentityComplete expectedHash source_identity
  promotion_authorization_complete :
    IndependentPromotionAuthorizationComplete promotion_authorization
  pending_absent : ¬ RegistryPromotionPending record
  rejected_absent :
    ¬ RegistryPromotionRejected oracle expectedHash expectedDigest record

theorem pending_registry_promotion_is_impossible
    {taggedSource taggedChecker : TaggedFinalStatement}
    {canonicalCandidate canonicalTarget : CanonicalStatementForm}
    {canonicalTargetProp : Prop}
    {oracle : CanonicalDigestOracle}
    {expectedHash : ByteHash}
    {expectedDigest : ExactStatementDigest}
    {finalRecord : FinalAdmissionRecord taggedSource taggedChecker
      canonicalCandidate canonicalTarget canonicalTargetProp}
    {record : RegistryPromotionRecord oracle expectedHash expectedDigest finalRecord}
    (pending : RegistryPromotionPending record) :
    ¬ Nonempty
      (ExplicitRegistryPromotionContract oracle expectedHash expectedDigest record) := by
  intro promotion
  rcases promotion with ⟨contract⟩
  exact contract.pending_absent pending

theorem rejected_registry_promotion_is_impossible
    {taggedSource taggedChecker : TaggedFinalStatement}
    {canonicalCandidate canonicalTarget : CanonicalStatementForm}
    {canonicalTargetProp : Prop}
    {oracle : CanonicalDigestOracle}
    {expectedHash : ByteHash}
    {expectedDigest : ExactStatementDigest}
    {finalRecord : FinalAdmissionRecord taggedSource taggedChecker
      canonicalCandidate canonicalTarget canonicalTargetProp}
    {record : RegistryPromotionRecord oracle expectedHash expectedDigest finalRecord}
    (rejected : RegistryPromotionRejected
      oracle expectedHash expectedDigest record) :
    ¬ Nonempty
      (ExplicitRegistryPromotionContract oracle expectedHash expectedDigest record) := by
  intro promotion
  rcases promotion with ⟨contract⟩
  exact contract.rejected_absent rejected

/- Admission boundary: this sidecar never constructs VERIFIED, never mutates a
   registry, and never treats final admission or receipt completeness as an
   implicit promotion authorization. -/

#print axioms pending_registry_promotion_is_impossible
#print axioms rejected_registry_promotion_is_impossible

end
end RouteBFixedLambdaExplicitRegistryPromotionGate

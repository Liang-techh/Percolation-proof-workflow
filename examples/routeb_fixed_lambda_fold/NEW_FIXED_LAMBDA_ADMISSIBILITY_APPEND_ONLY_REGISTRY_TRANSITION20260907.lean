import NEW_FIXED_LAMBDA_ADMISSIBILITY_VERIFIED_REGISTRY_ENTRY_INVARIANT20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaAppendOnlyRegistryTransition

open RouteBFixedLambdaExactStatementBoundary
open RouteBFixedLambdaTypedReceiptAudit
open RouteBFixedLambdaCanonicalDigestNormalization
open RouteBFixedLambdaFinalAdmissionContract
open RouteBFixedLambdaPinnedKernelReceiptFailClosed
open RouteBFixedLambdaExplicitRegistryPromotionGate
open RouteBFixedLambdaVerifiedRegistryEntryInvariant

noncomputable section

/-!
This sidecar maps the explicit verified-evidence bundle to an append-only
registry event.  Entry identity, artifact/statement digests, parent closure,
and independent authorization are event fields; overwrite and delete have no
successful transition branch.
-/

structure RegistryEntryIdentity where
  entry_id : String
  artifact_hash : ByteHash
  statement_digest : ExactStatementDigest

structure ParentClosureWitness where
  parent_entry_id : String
  parent_artifact_hash : ByteHash
  parent_statement_digest : ExactStatementDigest
  closure_digest : String

def RegistryEntryIdentityComplete
    (expectedHash : ByteHash)
    (expectedDigest : ExactStatementDigest)
    (identity : RegistryEntryIdentity) : Prop :=
  identity.entry_id ≠ "" ∧
    identity.artifact_hash = expectedHash ∧
    identity.statement_digest = expectedDigest

def ParentClosureComplete
    (parent : ParentClosureWitness) : Prop :=
  parent.parent_entry_id ≠ "" ∧
    parent.closure_digest ≠ ""

structure AppendOnlyVerifiedRegistryEvent
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
  parent_entries : List RegistryEntryIdentity
  identity : RegistryEntryIdentity
  verified_entry : VerifiedRegistryEntryInvariant
    oracle expectedHash expectedDigest
    expectedProjectCommit expectedToolchain expectedTheorem
    expectedKernelArtifactDigest finalRecord kernelRecord
  promotion_bundle : ExplicitVerifiedEvidenceBundle
    oracle expectedHash expectedDigest
    expectedProjectCommit expectedToolchain expectedTheorem
    expectedKernelArtifactDigest finalRecord kernelRecord
  evidence_eq_bundle : verified_entry.evidence = promotion_bundle
  parent_closure : ParentClosureWitness
  authorization : IndependentPromotionAuthorization
  identity_complete : RegistryEntryIdentityComplete expectedHash expectedDigest identity
  parent_closure_complete : ParentClosureComplete parent_closure
  authorization_complete :
    IndependentPromotionAuthorizationComplete authorization
  identity_artifact_hash_eq : identity.artifact_hash = expectedHash
  identity_statement_digest_eq : identity.statement_digest = expectedDigest
  authorization_eq_bundle : authorization = promotion_bundle.promotion_authorization
  fresh_entry_id : ∀ old ∈ parent_entries, old.entry_id ≠ identity.entry_id

def appendOnlyNextIdentities
    {taggedSource taggedChecker : TaggedFinalStatement}
    {canonicalCandidate canonicalTarget : CanonicalStatementForm}
    {canonicalTargetProp : Prop}
    {oracle : CanonicalDigestOracle}
    {expectedHash : ByteHash}
    {expectedDigest : ExactStatementDigest}
    {expectedProjectCommit expectedToolchain expectedTheorem : String}
    {expectedKernelArtifactDigest : KernelArtifactDigest}
    {finalRecord : FinalAdmissionRecord taggedSource taggedChecker
      canonicalCandidate canonicalTarget canonicalTargetProp}
    {kernelRecord : PinnedKernelReceiptAuditRecord}
    (before : List RegistryEntryIdentity)
    (event : AppendOnlyVerifiedRegistryEvent oracle expectedHash expectedDigest
      expectedProjectCommit expectedToolchain expectedTheorem
      expectedKernelArtifactDigest finalRecord kernelRecord) :
    List RegistryEntryIdentity :=
  before ++ [event.identity]

def AppendOnlyTransitionRelation
    {taggedSource taggedChecker : TaggedFinalStatement}
    {canonicalCandidate canonicalTarget : CanonicalStatementForm}
    {canonicalTargetProp : Prop}
    {oracle : CanonicalDigestOracle}
    {expectedHash : ByteHash}
    {expectedDigest : ExactStatementDigest}
    {expectedProjectCommit expectedToolchain expectedTheorem : String}
    {expectedKernelArtifactDigest : KernelArtifactDigest}
    {finalRecord : FinalAdmissionRecord taggedSource taggedChecker
      canonicalCandidate canonicalTarget canonicalTargetProp}
    {kernelRecord : PinnedKernelReceiptAuditRecord}
    (before after : List RegistryEntryIdentity)
    (event : AppendOnlyVerifiedRegistryEvent oracle expectedHash expectedDigest
      expectedProjectCommit expectedToolchain expectedTheorem
      expectedKernelArtifactDigest finalRecord kernelRecord) : Prop :=
  event.parent_entries = before ∧ after = appendOnlyNextIdentities before event

inductive AppendOnlyRegistryTransitionRequest (event : Type) where
  | append (event : event)
  | compiledOnly (candidate : CompiledCandidateOnly)
  | pending (reason : String)
  | rejected (reason : String)
  | overwrite (entry_id : String)
  | delete (entry_id : String)

def appendOnlyTransitionDecision {event : Type} :
    AppendOnlyRegistryTransitionRequest event → Option event
  | .append event => some event
  | .compiledOnly _ => none
  | .pending _ => none
  | .rejected _ => none
  | .overwrite _ => none
  | .delete _ => none

theorem compiled_only_transition_is_fail_closed
    {event : Type} (candidate : CompiledCandidateOnly) :
    appendOnlyTransitionDecision
      (AppendOnlyRegistryTransitionRequest.compiledOnly (event := event) candidate) = none := by
  rfl

theorem pending_transition_is_fail_closed
    {event : Type} (reason : String) :
    appendOnlyTransitionDecision
      (AppendOnlyRegistryTransitionRequest.pending (event := event) reason) = none := by
  rfl

theorem rejected_transition_is_fail_closed
    {event : Type} (reason : String) :
    appendOnlyTransitionDecision
      (AppendOnlyRegistryTransitionRequest.rejected (event := event) reason) = none := by
  rfl

theorem overwrite_transition_is_fail_closed
    {event : Type} (entryId : String) :
    appendOnlyTransitionDecision
      (AppendOnlyRegistryTransitionRequest.overwrite (event := event) entryId) = none := by
  rfl

theorem delete_transition_is_fail_closed
    {event : Type} (entryId : String) :
    appendOnlyTransitionDecision
      (AppendOnlyRegistryTransitionRequest.delete (event := event) entryId) = none := by
  rfl

/- Admission boundary: this is an append-event relation only.  No real
   registry state is read or modified, and no VERIFIED status is inferred. -/

#print axioms compiled_only_transition_is_fail_closed
#print axioms pending_transition_is_fail_closed
#print axioms rejected_transition_is_fail_closed
#print axioms overwrite_transition_is_fail_closed
#print axioms delete_transition_is_fail_closed

end
end RouteBFixedLambdaAppendOnlyRegistryTransition

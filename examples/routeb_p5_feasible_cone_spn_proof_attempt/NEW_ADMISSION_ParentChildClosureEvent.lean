import NEW_FIXED_LAMBDA_ADMISSIBILITY_APPEND_ONLY_REGISTRY_TRANSITION20260907

/-!
OPEN_UNCOMPILED. Additional parent/child closure gate around the EXISTING
append event, retaining all its verified-evidence and authorization fields.
No registry IO, runtime receipt validation, Lean execution or promotion.
-/

set_option autoImplicit false

namespace RouteBAdmissionParentChildClosureEvent

open RouteBFixedLambdaExactStatementBoundary
open RouteBFixedLambdaTypedReceiptAudit
open RouteBFixedLambdaCanonicalDigestNormalization
open RouteBFixedLambdaFinalAdmissionContract
open RouteBFixedLambdaPinnedKernelReceiptFailClosed
open RouteBFixedLambdaAppendOnlyRegistryTransition

noncomputable section

/-- Only packages the old event's dependent parameters; no evidence is
created by packaging them. -/
structure EventContext where
  taggedSource : TaggedFinalStatement
  taggedChecker : TaggedFinalStatement
  canonicalCandidate : CanonicalStatementForm
  canonicalTarget : CanonicalStatementForm
  canonicalTargetProp : Prop
  oracle : CanonicalDigestOracle
  expectedHash : ByteHash
  expectedDigest : ExactStatementDigest
  projectCommit : String
  toolchain : String
  theoremName : String
  kernelArtifact : KernelArtifactDigest
  finalRecord : FinalAdmissionRecord taggedSource taggedChecker
    canonicalCandidate canonicalTarget canonicalTargetProp
  kernelRecord : PinnedKernelReceiptAuditRecord

abbrev BaseEvent (c : EventContext) := AppendOnlyVerifiedRegistryEvent
  c.oracle c.expectedHash c.expectedDigest c.projectCommit c.toolchain c.theoremName
  c.kernelArtifact c.finalRecord c.kernelRecord

structure ChildReceipt where
  parentIdentity : RegistryEntryIdentity
  childIdentity : RegistryEntryIdentity
  snapshotDigest : String
  closureDigest : Option String
  kernelReceiptDigest : Option String
  comparatorReceiptDigest : Option String

def PresentDigest (digest : Option String) : Prop :=
  ∃ value : String, digest = some value ∧ value ≠ ""

def ReceiptFieldsComplete (r : ChildReceipt) : Prop :=
  r.snapshotDigest ≠ "" ∧ PresentDigest r.closureDigest ∧
    PresentDigest r.kernelReceiptDigest ∧ PresentDigest r.comparatorReceiptDigest

/-- Semantic authorities are EXTERNAL predicates. Nonempty digest strings
do not establish closure, hash validity, or binding to the old event bundle. -/
structure ClosurePolicy (c : EventContext) where
  parentClosed : RegistryEntryIdentity → String → Prop
  childClosed : RegistryEntryIdentity → String → Prop
  snapshotMatches : List RegistryEntryIdentity → String → Prop
  receiptValidForEvent : ChildReceipt → BaseEvent c → Prop

structure ParentReady {c : EventContext} (policy : ClosurePolicy c)
    (before : List RegistryEntryIdentity) (parent : RegistryEntryIdentity)
    (event : BaseEvent c) : Prop where
  same_snapshot : event.parent_entries = before
  parent_in_snapshot : parent ∈ before
  id_matches : event.parent_closure.parent_entry_id = parent.entry_id
  artifact_matches : event.parent_closure.parent_artifact_hash = parent.artifact_hash
  statement_matches : event.parent_closure.parent_statement_digest = parent.statement_digest
  closed : policy.parentClosed parent event.parent_closure.closure_digest

structure BoundChildReceipt {c : EventContext} (policy : ClosurePolicy c)
    (before : List RegistryEntryIdentity) (parent : RegistryEntryIdentity)
    (event : BaseEvent c) (r : ChildReceipt) : Prop where
  parent_matches : r.parentIdentity = parent
  child_matches : r.childIdentity = event.identity
  complete : ReceiptFieldsComplete r
  snapshot_bound : policy.snapshotMatches before r.snapshotDigest
  child_closed : ∀ digest, r.closureDigest = some digest →
    policy.childClosed event.identity digest
  receipt_bound : policy.receiptValidForEvent r event

def ChildReady {c : EventContext} (policy : ClosurePolicy c)
    (before : List RegistryEntryIdentity) (parent : RegistryEntryIdentity)
    (event : BaseEvent c) (receipt : Option ChildReceipt) : Prop :=
  ∃ r : ChildReceipt, receipt = some r ∧ BoundChildReceipt policy before parent event r

structure ClosureApproved {c : EventContext} (policy : ClosurePolicy c)
    (before : List RegistryEntryIdentity) (parent : RegistryEntryIdentity)
    (event : BaseEvent c) (receipt : Option ChildReceipt) : Prop where
  parentProof : ParentReady policy before parent event
  childProof : ChildReady policy before parent event receipt

/-- Missing PROOF inputs fail closed, without deciding external predicates
or fabricating evidence. This is a pure option constructor, not a validator. -/
def closureDecision {c : EventContext} (policy : ClosurePolicy c)
    (before : List RegistryEntryIdentity) (parent : RegistryEntryIdentity)
    (event : BaseEvent c) (receipt : Option ChildReceipt)
    (hp : Option (ParentReady policy before parent event))
    (hc : Option (ChildReady policy before parent event receipt)) :
    Option (ClosureApproved policy before parent event receipt) :=
  match hp, hc with
  | some p, some child => some ⟨p, child⟩
  | _, _ => none

def approvedAppendRequest {c : EventContext} {policy : ClosurePolicy c}
    {before : List RegistryEntryIdentity} {parent : RegistryEntryIdentity}
    {event : BaseEvent c} {receipt : Option ChildReceipt}
    (_ : ClosureApproved policy before parent event receipt) :
    AppendOnlyRegistryTransitionRequest (BaseEvent c) := .append event

theorem approved_append_relation {c : EventContext} {policy : ClosurePolicy c}
    {before : List RegistryEntryIdentity} {parent : RegistryEntryIdentity}
    {event : BaseEvent c} {receipt : Option ChildReceipt}
    (approved : ClosureApproved policy before parent event receipt) :
    AppendOnlyTransitionRelation before (before ++ [event.identity]) event :=
  ⟨approved.parentProof.same_snapshot, rfl⟩

section FailureCases

variable {c : EventContext} (policy : ClosurePolicy c)
  (before : List RegistryEntryIdentity) (parent : RegistryEntryIdentity)
  (event : BaseEvent c) (receipt : Option ChildReceipt)

theorem missing_parent_proof
    (hc : Option (ChildReady policy before parent event receipt)) :
    closureDecision policy before parent event receipt none hc = none := by
  cases hc <;> rfl

theorem missing_child_proof
    (hp : Option (ParentReady policy before parent event)) :
    closureDecision policy before parent event receipt hp none = none := by
  cases hp <;> rfl

theorem unclosed_parent_fail_closed
    (hnot : ¬ policy.parentClosed parent event.parent_closure.closure_digest)
    (hp : Option (ParentReady policy before parent event))
    (hc : Option (ChildReady policy before parent event receipt)) :
    closureDecision policy before parent event receipt hp hc = none := by
  cases hp with
  | none => exact missing_parent_proof policy before parent event receipt hc
  | some p => exact False.elim (hnot p.closed)

theorem absent_receipt_not_ready : ¬ ChildReady policy before parent event none := by
  rintro ⟨r, h, _⟩
  cases h

theorem incomplete_receipt_not_ready (r : ChildReceipt) (hbad : ¬ ReceiptFieldsComplete r) :
    ¬ ChildReady policy before parent event (some r) := by
  rintro ⟨actual, heq, hready⟩
  have hid : r = actual := Option.some.inj heq
  subst actual
  exact hbad hready.complete

theorem child_not_ready_fail_closed
    (hnot : ¬ ChildReady policy before parent event receipt)
    (hp : Option (ParentReady policy before parent event))
    (hc : Option (ChildReady policy before parent event receipt)) :
    closureDecision policy before parent event receipt hp hc = none := by
  cases hc with
  | none => exact missing_child_proof policy before parent event receipt hp
  | some child => exact False.elim (hnot child)

theorem incomplete_child_receipt_fail_closed (r : ChildReceipt)
    (hbad : ¬ ReceiptFieldsComplete r)
    (hp : Option (ParentReady policy before parent event))
    (hc : Option (ChildReady policy before parent event (some r))) :
    closureDecision policy before parent event (some r) hp hc = none :=
  child_not_ready_fail_closed policy before parent event (some r)
    (incomplete_receipt_not_ready policy before parent event r hbad) hp hc

theorem stale_snapshot_fail_closed (hbad : event.parent_entries ≠ before)
    (hp : Option (ParentReady policy before parent event))
    (hc : Option (ChildReady policy before parent event receipt)) :
    closureDecision policy before parent event receipt hp hc = none := by
  cases hp with
  | none => exact missing_parent_proof policy before parent event receipt hc
  | some p => exact False.elim (hbad p.same_snapshot)

end FailureCases

theorem missing_kernel_digest_incomplete (r : ChildReceipt) (h : r.kernelReceiptDigest = none) :
    ¬ ReceiptFieldsComplete r := by
  intro hc
  obtain ⟨digest, hp, _⟩ := hc.2.2.1
  rw [h] at hp
  cases hp

end

-- Future audit commands only; NOT executed in this round.
#print axioms approved_append_relation
#print axioms missing_parent_proof
#print axioms missing_child_proof
#print axioms unclosed_parent_fail_closed
#print axioms incomplete_child_receipt_fail_closed
#print axioms stale_snapshot_fail_closed
#print axioms missing_kernel_digest_incomplete

end RouteBAdmissionParentChildClosureEvent

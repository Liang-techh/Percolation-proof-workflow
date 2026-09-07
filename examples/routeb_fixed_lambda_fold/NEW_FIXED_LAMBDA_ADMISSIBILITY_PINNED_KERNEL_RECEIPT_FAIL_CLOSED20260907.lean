import NEW_FIXED_LAMBDA_ADMISSIBILITY_EXPLICIT_REGISTRY_PROMOTION_GATE20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaPinnedKernelReceiptFailClosed

noncomputable section

/-!
This sidecar isolates the pinned Lean-kernel receipt gate.  Project commit,
toolchain, theorem identity, artifact digest, exit code, and the zero
sorry/admit/nonstandard-axiom audit are independent receipt fields.
-/

structure KernelArtifactDigest where
  value : String

structure PinnedKernelReceiptAuditRecord where
  project_commit : Option String
  toolchain_identity : Option String
  theorem_identity : Option String
  artifact_digest : Option KernelArtifactDigest
  exit_code : Option Int
  sorry_count : Option Nat
  admit_count : Option Nat
  nonstandard_axiom_count : Option Nat

def PinnedKernelReceiptPending
    (record : PinnedKernelReceiptAuditRecord) : Prop :=
  record.project_commit = none ∨
    record.toolchain_identity = none ∨
    record.theorem_identity = none ∨
    record.artifact_digest = none ∨
    record.exit_code = none ∨
    record.sorry_count = none ∨
    record.admit_count = none ∨
    record.nonstandard_axiom_count = none

def PinnedKernelReceiptRejected
    (expectedProjectCommit expectedToolchain expectedTheorem : String)
    (expectedArtifactDigest : KernelArtifactDigest)
    (record : PinnedKernelReceiptAuditRecord) : Prop :=
  (∃ value,
    record.project_commit = some value ∧ value ≠ expectedProjectCommit) ∨
  (∃ value,
    record.toolchain_identity = some value ∧ value ≠ expectedToolchain) ∨
  (∃ value,
    record.theorem_identity = some value ∧ value ≠ expectedTheorem) ∨
  (∃ value,
    record.artifact_digest = some value ∧ value ≠ expectedArtifactDigest) ∨
  (∃ value,
    record.exit_code = some value ∧ value ≠ 0) ∨
  (∃ value,
    record.sorry_count = some value ∧ value ≠ 0) ∨
  (∃ value,
    record.admit_count = some value ∧ value ≠ 0) ∨
  (∃ value,
    record.nonstandard_axiom_count = some value ∧ value ≠ 0)

def PinnedKernelReceiptComplete
    (expectedProjectCommit expectedToolchain expectedTheorem : String)
    (expectedArtifactDigest : KernelArtifactDigest)
    (record : PinnedKernelReceiptAuditRecord) : Prop :=
  record.project_commit = some expectedProjectCommit ∧
    record.toolchain_identity = some expectedToolchain ∧
    record.theorem_identity = some expectedTheorem ∧
    record.artifact_digest = some expectedArtifactDigest ∧
    record.exit_code = some 0 ∧
    record.sorry_count = some 0 ∧
    record.admit_count = some 0 ∧
    record.nonstandard_axiom_count = some 0

structure PinnedKernelReceiptAdmissionContract
    (expectedProjectCommit expectedToolchain expectedTheorem : String)
    (expectedArtifactDigest : KernelArtifactDigest)
    (record : PinnedKernelReceiptAuditRecord) where
  complete : PinnedKernelReceiptComplete
    expectedProjectCommit expectedToolchain expectedTheorem
    expectedArtifactDigest record
  pending_absent : ¬ PinnedKernelReceiptPending record
  rejected_absent :
    ¬ PinnedKernelReceiptRejected
      expectedProjectCommit expectedToolchain expectedTheorem
      expectedArtifactDigest record

/-!
This gate is only a prerequisite object for a later promotion workflow.  It
contains no VERIFIED field and performs no registry action.
-/
structure PinnedKernelReceiptPromotionGate
    (expectedProjectCommit expectedToolchain expectedTheorem : String)
    (expectedArtifactDigest : KernelArtifactDigest)
    (record : PinnedKernelReceiptAuditRecord) where
  admission : PinnedKernelReceiptAdmissionContract
    expectedProjectCommit expectedToolchain expectedTheorem
    expectedArtifactDigest record
  pending_absent : ¬ PinnedKernelReceiptPending record
  rejected_absent :
    ¬ PinnedKernelReceiptRejected
      expectedProjectCommit expectedToolchain expectedTheorem
      expectedArtifactDigest record

theorem pending_kernel_receipt_blocks_promotion
    {expectedProjectCommit expectedToolchain expectedTheorem : String}
    {expectedArtifactDigest : KernelArtifactDigest}
    {record : PinnedKernelReceiptAuditRecord}
    (pending : PinnedKernelReceiptPending record) :
    ¬ Nonempty (PinnedKernelReceiptPromotionGate
      expectedProjectCommit expectedToolchain expectedTheorem
      expectedArtifactDigest record) := by
  intro gate
  rcases gate with ⟨gate⟩
  exact gate.pending_absent pending

theorem rejected_kernel_receipt_blocks_promotion
    {expectedProjectCommit expectedToolchain expectedTheorem : String}
    {expectedArtifactDigest : KernelArtifactDigest}
    {record : PinnedKernelReceiptAuditRecord}
    (rejected : PinnedKernelReceiptRejected
      expectedProjectCommit expectedToolchain expectedTheorem
      expectedArtifactDigest record) :
    ¬ Nonempty (PinnedKernelReceiptPromotionGate
      expectedProjectCommit expectedToolchain expectedTheorem
      expectedArtifactDigest record) := by
  intro gate
  rcases gate with ⟨gate⟩
  exact gate.rejected_absent rejected

/- Admission boundary: this receipt gate does not assert that Lean was run,
   that the artifact digest was computed correctly, that zero counts came from
   an authoritative report, or that any candidate is VERIFIED or registry-ready. -/

#print axioms pending_kernel_receipt_blocks_promotion
#print axioms rejected_kernel_receipt_blocks_promotion

end
end RouteBFixedLambdaPinnedKernelReceiptFailClosed

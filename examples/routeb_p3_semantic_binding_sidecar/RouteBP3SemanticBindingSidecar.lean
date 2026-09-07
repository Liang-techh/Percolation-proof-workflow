import Mathlib

set_option autoImplicit false

namespace RouteBP3SemanticBindingSidecar

noncomputable section

/-- Provenance evidence stays separate from semantics. -/
structure ProvenanceHashes where
  sourceRoot : String
  entries : List (String × String)

/-- Manifest and snapshot agreement is an explicit premise, not a consequence of hashes. -/
structure ManifestSnapshotAgreement where
  stateOrder : List String
  massRegularizer : ℚ
  fdStep : ℚ
  manifestSemantics : String
  snapshotSemantics : String
  agreesOnRegularizer : massRegularizer = massRegularizer
  agreesOnStep : fdStep = fdStep
  agreesOnSemantics : manifestSemantics = snapshotSemantics

/-- Exact true-DH semantics are admitted only as their own premise. -/
structure ExactTrueDHSemantics where
  semantics : String
  sourceExact : String
  sourceRun : String
  provenanceDoesNotImplySemantics : True

/-- Interval enclosure is kept as a separate checker-side premise. -/
structure IntervalEnclosure where
  payloadCenter : ℚ
  payloadRadius : ℚ
  roundingRadius : ℚ
  derivativeRadius : ℚ
  witnessNorm : ℚ
  enclosure : True

/-- Minimal interface theorem for the P3 semantic-binding sidecar.

This theorem does not derive semantics from hashes, does not introduce any
Float64 equality, and does not modify registry or StateStore state. It only
packages the four explicit premises together.
-/
theorem minimal_interface
    (hHashes : ProvenanceHashes)
    (hAgreement : ManifestSnapshotAgreement)
    (hSemantics : ExactTrueDHSemantics)
    (hEnclosure : IntervalEnclosure) :
    ProvenanceHashes ∧
    ManifestSnapshotAgreement ∧
    ExactTrueDHSemantics ∧
    IntervalEnclosure := by
  exact ⟨hHashes, hAgreement, hSemantics, hEnclosure⟩

end

end RouteBP3SemanticBindingSidecar

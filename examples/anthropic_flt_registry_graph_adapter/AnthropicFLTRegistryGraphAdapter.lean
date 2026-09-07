import Mathlib.Data.List.Basic

/-!
# Anthropic FLT registry / graph adapter

This is a typed architecture adapter for the upstream extract -> graphdata ->
render -> selfcheck pipeline.  It records provenance and graph relations, but
does not create a local registry entry or treat rendered metadata as proof.
-/

set_option autoImplicit false

namespace AnthropicFLTRegistryGraphAdapter

inductive ReuseClass
  | directReuse
  | lightAdaptation
  | architectureOnly
  deriving DecidableEq, Repr

inductive RegistryState
  | pending
  | rejected
  | verified
  deriving DecidableEq, Repr

inductive EdgeKind
  | citation
  | statementHop
  | definitionHop
  deriving DecidableEq, Repr

structure Provenance where
  repository : String
  commit : String
  sourcePath : String
  license : String

structure GraphNode where
  id : String
  stage : Nat
  landmark : Bool

structure GraphEdge where
  source : String
  target : String
  kind : EdgeKind

structure GraphManifest where
  schemaVersion : Nat
  classification : ReuseClass
  provenance : Provenance
  nodes : List GraphNode
  edges : List GraphEdge
  sourceSnapshotSha256 : String
  graphSnapshotSha256 : String
  selfcheckInputSha256 : String
  registryState : RegistryState
  formalCertificateAllowed : Bool

def nodeIds (M : GraphManifest) : List String := M.nodes.map GraphNode.id

def edgeRefsValid (M : GraphManifest) : Prop :=
  ∀ e, e ∈ M.edges → e.source ∈ nodeIds M ∧ e.target ∈ nodeIds M

def graphMetadataComplete (M : GraphManifest) : Prop :=
  M.schemaVersion = 1 ∧
    M.provenance.repository ≠ "" ∧
    M.provenance.commit ≠ "" ∧
    M.provenance.sourcePath ≠ "" ∧
    M.sourceSnapshotSha256 ≠ "" ∧
    M.graphSnapshotSha256 ≠ "" ∧
    M.selfcheckInputSha256 ≠ ""

def admissionClosed (M : GraphManifest) : Prop :=
  M.registryState ≠ RegistryState.verified ∧
    M.formalCertificateAllowed = false

theorem pending_manifest_is_closed (M : GraphManifest)
    (hPending : M.registryState = RegistryState.pending)
    (hClosed : admissionClosed M) :
    M.formalCertificateAllowed = false := by
  exact hClosed.2

theorem metadata_does_not_validate_edges
    (M : GraphManifest) (hMeta : graphMetadataComplete M) :
    graphMetadataComplete M ∧
      (edgeRefsValid M ∨ ¬ edgeRefsValid M) := by
  exact ⟨hMeta, Classical.em (edgeRefsValid M)⟩

structure PromotionEvidence (M : GraphManifest) where
  sourceBound : Prop
  graphBound : Prop
  finalCheck : Prop
  comparatorAccepted : Prop
  sourceBound_proof : sourceBound
  graphBound_proof : graphBound
  finalCheck_proof : finalCheck
  comparatorAccepted_proof : comparatorAccepted
  state_verified : M.registryState = RegistryState.verified
  formal_allowed : M.formalCertificateAllowed = true

theorem promotion_requires_explicit_evidence
    (M : GraphManifest) (E : PromotionEvidence M) :
    M.registryState = RegistryState.verified ∧
      M.formalCertificateAllowed = true := by
  exact ⟨E.state_verified, E.formal_allowed⟩

end AnthropicFLTRegistryGraphAdapter

#print axioms AnthropicFLTRegistryGraphAdapter.pending_manifest_is_closed
#print axioms AnthropicFLTRegistryGraphAdapter.metadata_does_not_validate_edges
#print axioms AnthropicFLTRegistryGraphAdapter.promotion_requires_explicit_evidence

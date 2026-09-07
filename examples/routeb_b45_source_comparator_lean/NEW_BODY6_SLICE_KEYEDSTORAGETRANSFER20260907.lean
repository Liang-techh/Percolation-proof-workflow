import Mathlib

set_option autoImplicit false

namespace NEW_BODY6_SLICE_KEYEDSTORAGETRANSFER20260907
noncomputable section

/- OPEN_UNCOMPILED. Digests are receipt labels, never proofs of semantics. -/
structure Candidate (X : Type*) where
  V : X → ℝ
  candidateDigest : String
  parameterDigest : String

structure Scope (X : Type*) where
  initial : Set X
  domain : Set X
  initialDigest : String
  domainDigest : String

structure ReceiptKey where
  sourceCandidate : String
  sourceParameters : String
  targetCandidate : String
  targetParameters : String
  initialSet : String
  domain : String

def keyOf {X : Type*} (src dst : Candidate X) (scope : Scope X) : ReceiptKey :=
  ⟨src.candidateDigest, src.parameterDigest, dst.candidateDigest,
    dst.parameterDigest, scope.initialDigest, scope.domainDigest⟩

def SameStorageIdentity {X : Type*} (src dst : Candidate X) (scope : Scope X) : Prop :=
  ∀ x ∈ scope.domain, dst.V x = src.V x

def OneSidedComparison {X : Type*} (src dst : Candidate X)
    (scope : Scope X) (delta : ℝ) : Prop :=
  ∀ x ∈ scope.domain, dst.V x ≤ src.V x + delta

theorem identity_supplies_comparison_attempt {X : Type*}
    (src dst : Candidate X) (scope : Scope X) (h : SameStorageIdentity src dst scope) :
    OneSidedComparison src dst scope 0 := by
  intro x hx
  rw [h x hx]
  simp

/- Hash equality and the actual function inequality are distinct fields.
   Initial and path points must belong to the same comparison domain. -/
structure TransferContract {X : Type*} (src dst : Candidate X)
    (scope : Scope X) (receipt : ReceiptKey) (delta : ℝ) : Prop where
  keyMatches : receipt = keyOf src dst scope
  initialInDomain : scope.initial ⊆ scope.domain
  comparison : OneSidedComparison src dst scope delta

theorem initial_bound_transfer_attempt {X : Type*}
    (src dst : Candidate X) (scope : Scope X) (receipt : ReceiptKey)
    (delta upper : ℝ) (h : TransferContract src dst scope receipt delta)
    (hInitial : ∀ x ∈ scope.initial, src.V x ≤ upper) :
    ∀ x ∈ scope.initial, dst.V x ≤ upper + delta := by
  intro x hx
  exact (h.comparison x (h.initialInDomain hx)).trans
    (add_le_add_right (hInitial x hx) delta)

theorem barrier_transfer_attempt {X : Type*}
    (src dst : Candidate X) (scope : Scope X) (receipt : ReceiptKey)
    (delta cap bar : ℝ) (h : TransferContract src dst scope receipt delta)
    (path : ℝ → X)
    (hDomain : ∀ t ∈ Set.Icc (0 : ℝ) 1, path t ∈ scope.domain)
    (hSource : ∀ t ∈ Set.Icc (0 : ℝ) 1, src.V (path t) ≤ cap)
    (hBudget : cap + delta ≤ bar) :
    ∀ t ∈ Set.Icc (0 : ℝ) 1, dst.V (path t) ≤ bar := by
  intro t ht
  exact ((h.comparison (path t) (hDomain t ht)).trans
    (add_le_add_right (hSource t ht) delta)).trans hBudget

/- For time-dependent storage, use X = Real x PhysicalState and bind the
   time/state embedding in candidate/domain receipts. No path is invented. -/
def ledgerV0 : ℝ := 492033745203 / 25600000000000

/- Exact scalar V0 matches even as the actual initial VALUE for both
   functions. This is an abstract transfer counterexample, not DH dynamics. -/
theorem exact_v0_match_no_barrier_transfer_attempt :
    ∃ V W : ℝ → ℝ,
      V 0 = ledgerV0 ∧ W 0 = ledgerV0 ∧
      (∀ t ∈ Set.Icc (0 : ℝ) 1, V t ≤ 1) ∧
      ¬ (∀ t ∈ Set.Icc (0 : ℝ) 1, W t ≤ 1) := by
  refine ⟨(fun _ => ledgerV0), (fun t => ledgerV0 + 2*t), rfl, ?_, ?_, ?_⟩
  · simp
  · intro t ht
    norm_num [ledgerV0]
  · intro h
    have hb := h 1 (by norm_num)
    norm_num [ledgerV0] at hb

/- No actual src/dst/scope/digest instance, source envelope, trajectory,
   first-exit theorem or source-to-Float64 equivalence is asserted. -/
end
end NEW_BODY6_SLICE_KEYEDSTORAGETRANSFER20260907

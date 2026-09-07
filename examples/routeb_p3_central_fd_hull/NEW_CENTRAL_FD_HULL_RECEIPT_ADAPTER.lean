import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

/-!
# P3 receipt to interval-enclosure adapter

The receipt stores optional metadata.  A separate mathematical evidence record
must match those fields and prove endpoint order, gap/cap inequalities,
rounding soundness, and coverage before an interval-enclosure certificate can
be constructed.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullReceiptAdapter

noncomputable section

structure IntervalReceiptPayload (D B : Type*) [DecidableEq B] where
  domain : D → Prop
  boxes : Finset B
  region : B → D → Prop
  weightedLoad : D → ℝ
  capLoad : D → ℝ
  capLoadUpper : B → ℝ
  capMaxLoad : D → ℝ
  boxSource : B → Option String
  lowerEndpoint : B → Option ℝ
  upperEndpoint : B → Option ℝ
  roundingSoundnessClaim : B → Option Bool
  artifactHash : B → Option String
  checkerExitCode : B → Option Nat
  checkerOutput : B → Option String
  coverageMapping : D → Option B

structure MathEnclosureEvidence
    {D B : Type*} [DecidableEq B]
    (R : IntervalReceiptPayload D B) where
  source : B → String
  lowerEndpoint : B → ℝ
  upperEndpoint : B → ℝ
  roundingSound : B → Prop
  artifactHash : B → String
  checkerExitCode : B → Nat
  checkerOutput : B → String
  coverageBox : D → B
  source_match : ∀ b, R.boxSource b = some (source b)
  lower_match : ∀ b, R.lowerEndpoint b = some (lowerEndpoint b)
  upper_match : ∀ b, R.upperEndpoint b = some (upperEndpoint b)
  rounding_match : ∀ b, R.roundingSoundnessClaim b = some true
  hash_match : ∀ b, R.artifactHash b = some (artifactHash b)
  checker_exit_match : ∀ b, R.checkerExitCode b = some (checkerExitCode b)
  checker_output_match : ∀ b, R.checkerOutput b = some (checkerOutput b)
  coverage_match : ∀ x, R.coverageMapping x = some (coverageBox x)
  endpoint_order : ∀ b, b ∈ R.boxes → lowerEndpoint b ≤ upperEndpoint b
  rounding_sound : ∀ b, b ∈ R.boxes → roundingSound b
  gapLower : B → ℝ
  capLoadUpper : B → ℝ
  gap_lower_positive : ∀ b, b ∈ R.boxes → 0 < gapLower b
  gap_lower_sound : ∀ b, b ∈ R.boxes → ∀ x, R.region b x →
    gapLower b ≤ R.capLoad x - R.weightedLoad x
  cap_load_upper_sound : ∀ b, b ∈ R.boxes → ∀ x, R.region b x →
    R.capLoad x ≤ capLoadUpper b
  cap_upper_to_capMax : ∀ b, b ∈ R.boxes → ∀ x, R.region b x →
    capLoadUpper b ≤ R.capMaxLoad x
  coverage : ∀ x, R.domain x →
    coverageBox x ∈ R.boxes ∧ R.region (coverageBox x) x

structure IntervalEnclosureCertificate
    {D B : Type*} [DecidableEq B]
    (R : IntervalReceiptPayload D B)
    (M : MathEnclosureEvidence R) where
  source : B → String
  lowerEndpoint : B → ℝ
  upperEndpoint : B → ℝ
  roundingSound : B → Prop
  artifactHash : B → String
  checkerExitCode : B → Nat
  checkerOutput : B → String
  coverageMapping : D → B
  gapLower : B → ℝ
  capLoadUpper : B → ℝ
  endpoint_order : ∀ b, b ∈ R.boxes → lowerEndpoint b ≤ upperEndpoint b
  rounding_interval_sound : ∀ b, b ∈ R.boxes → roundingSound b
  gap_lower_positive : ∀ b, b ∈ R.boxes → 0 < gapLower b
  gap_lower_sound : ∀ b, b ∈ R.boxes → ∀ x, R.region b x →
    gapLower b ≤ R.capLoad x - R.weightedLoad x
  cap_load_upper_sound : ∀ b, b ∈ R.boxes → ∀ x, R.region b x →
    R.capLoad x ≤ capLoadUpper b
  cap_upper_to_capMax : ∀ b, b ∈ R.boxes → ∀ x, R.region b x →
    capLoadUpper b ≤ R.capMaxLoad x
  coverage : ∀ x, R.domain x →
    coverageMapping x ∈ R.boxes ∧ R.region (coverageMapping x) x

def adaptReceipt
    {D B : Type*} [DecidableEq B]
    (R : IntervalReceiptPayload D B) (M : MathEnclosureEvidence R) :
    IntervalEnclosureCertificate R M where
  source := M.source
  lowerEndpoint := M.lowerEndpoint
  upperEndpoint := M.upperEndpoint
  roundingSound := M.roundingSound
  artifactHash := M.artifactHash
  checkerExitCode := M.checkerExitCode
  checkerOutput := M.checkerOutput
  coverageMapping := M.coverageBox
  gapLower := M.gapLower
  capLoadUpper := M.capLoadUpper
  endpoint_order := M.endpoint_order
  rounding_interval_sound := M.rounding_sound
  gap_lower_positive := M.gap_lower_positive
  gap_lower_sound := M.gap_lower_sound
  cap_load_upper_sound := M.cap_load_upper_sound
  cap_upper_to_capMax := M.cap_upper_to_capMax
  coverage := M.coverage

theorem adapter_requires_mathematical_evidence
    {D B : Type*} [DecidableEq B]
    (R : IntervalReceiptPayload D B) :
    (∃ M : MathEnclosureEvidence R, True) →
      ∃ M : MathEnclosureEvidence R, ∃ C : IntervalEnclosureCertificate R M, True := by
  rintro ⟨M, hM⟩
  exact ⟨M, adaptReceipt R M, trivial⟩

theorem missing_receipt_field_blocks_adapter
    {D B : Type*} [DecidableEq B]
    (R : IntervalReceiptPayload D B) (b : B)
    (hMissing : R.boxSource b = none ∨
      R.lowerEndpoint b = none ∨
      R.upperEndpoint b = none ∨
      R.roundingSoundnessClaim b = none ∨
      R.artifactHash b = none ∨
      R.checkerExitCode b = none ∨
      R.checkerOutput b = none) :
    ¬ ∃ M : MathEnclosureEvidence R, True := by
  intro hEvidence
  rcases hEvidence with ⟨M, hM⟩
  rcases hMissing with h | h | h | h | h | h | h
  · simp [h] at M.source_match
  · simp [h] at M.lower_match
  · simp [h] at M.upper_match
  · simp [h] at M.rounding_match
  · simp [h] at M.hash_match
  · simp [h] at M.checker_exit_match
  · simp [h] at M.checker_output_match

theorem missing_coverage_mapping_blocks_adapter
    {D B : Type*} [DecidableEq B]
    (R : IntervalReceiptPayload D B) (x : D)
    (hMissing : R.coverageMapping x = none) :
    ¬ ∃ M : MathEnclosureEvidence R, True := by
  intro hEvidence
  rcases hEvidence with ⟨M, hM⟩
  simp [hMissing] at M.coverage_match

/-! Complete metadata with invalid exact endpoints still cannot be adapted. -/

def forgedReceipt : IntervalReceiptPayload Bool Bool where
  domain := fun _ => True
  boxes := {false}
  region := fun b x => b = false ∧ x = false
  weightedLoad := fun _ => 0
  capLoad := fun _ => 1
  capLoadUpper := fun _ => 1
  capMaxLoad := fun _ => 2
  boxSource := fun _ => some "solver-output"
  lowerEndpoint := fun _ => some 1
  upperEndpoint := fun _ => some 0
  roundingSoundnessClaim := fun _ => some true
  artifactHash := fun _ => some "deadbeef"
  checkerExitCode := fun _ => some 0
  checkerOutput := fun _ => some "Your solution is okay!"
  coverageMapping := fun x => if x = false then some false else none

theorem forged_metadata_not_adaptable :
    (∃ M : MathEnclosureEvidence forgedReceipt, True) → False := by
  rintro ⟨M, hM⟩
  have hOrder := M.endpoint_order false (by simp [forgedReceipt])
  have hLower := M.lower_match false
  have hUpper := M.upper_match false
  have hLowerValue : M.lowerEndpoint false = 1 := by
    simpa [forgedReceipt] using (Option.some.inj hLower).symm
  have hUpperValue : M.upperEndpoint false = 0 := by
    simpa [forgedReceipt] using (Option.some.inj hUpper).symm
  rw [hLowerValue, hUpperValue] at hOrder
  norm_num at hOrder

end

end RouteBP3CentralFDHullReceiptAdapter

#print axioms RouteBP3CentralFDHullReceiptAdapter.adaptReceipt
#print axioms RouteBP3CentralFDHullReceiptAdapter.missing_receipt_field_blocks_adapter
#print axioms RouteBP3CentralFDHullReceiptAdapter.forged_metadata_not_adaptable

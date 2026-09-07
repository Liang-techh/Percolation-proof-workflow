import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

/-!
# P3 interval payload / receipt boundary

Receipt metadata is typed separately from mathematical enclosure.  Completeness
and checker acceptance are necessary bookkeeping conditions, but the theorem
does not treat them as a proof that endpoint inequalities or rounding are
sound.  Missing receipt fields are fail-closed.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullIntervalReceipt

noncomputable section

structure IntervalPayloadReceipt (D B : Type*) [DecidableEq B] where
  domain : D → Prop
  boxes : Finset B
  region : B → D → Prop
  boxSource : B → Option String
  lowerEndpoint : B → Option ℝ
  upperEndpoint : B → Option ℝ
  roundingSoundness : B → Option Bool
  artifactHash : B → Option String
  checkerExitCode : B → Option Nat
  checkerOutput : B → Option String
  coverageMapping : D → Option B

def receiptReadyAt
    {D B : Type*} [DecidableEq B]
    (R : IntervalPayloadReceipt D B) (b : B) : Prop :=
  (∃ source, R.boxSource b = some source) ∧
    (∃ lower, R.lowerEndpoint b = some lower) ∧
    (∃ upper, R.upperEndpoint b = some upper) ∧
    R.roundingSoundness b = some true ∧
    (∃ hash, R.artifactHash b = some hash) ∧
    R.checkerExitCode b = some 0 ∧
    R.checkerOutput b = some "Your solution is okay!"

def coverageWitnessAt
    {D B : Type*} [DecidableEq B]
    (R : IntervalPayloadReceipt D B) (x : D) : Prop :=
  ∃ b, R.coverageMapping x = some b ∧ b ∈ R.boxes ∧ R.region b x

theorem missing_required_field_fail_closed
    {D B : Type*} [DecidableEq B]
    (R : IntervalPayloadReceipt D B) (b : B)
    (hMissing : R.boxSource b = none ∨
      R.lowerEndpoint b = none ∨
      R.upperEndpoint b = none ∨
      R.roundingSoundness b = none ∨
      R.artifactHash b = none ∨
      R.checkerExitCode b = none ∨
      R.checkerOutput b = none) :
    ¬ receiptReadyAt R b := by
  intro hReady
  rcases hMissing with h | h | h | h | h | h | h <;>
    simp [receiptReadyAt, h] at hReady

theorem missing_coverage_mapping_fail_closed
    {D B : Type*} [DecidableEq B]
    (R : IntervalPayloadReceipt D B) (x : D)
    (hMissing : R.coverageMapping x = none) :
    ¬ coverageWitnessAt R x := by
  intro hCoverage
  rcases hCoverage with ⟨b, hMap, hb, hRegion⟩
  simp [hMissing] at hMap

/-! Metadata can be complete while the endpoint relation is mathematically false. -/

def forgedReceipt : IntervalPayloadReceipt Bool Bool where
  domain := fun _ => True
  boxes := {false}
  region := fun b x => b = false ∧ x = false
  boxSource := fun _ => some "solver-output"
  lowerEndpoint := fun _ => some 1
  upperEndpoint := fun _ => some 0
  roundingSoundness := fun _ => some true
  artifactHash := fun _ => some "deadbeef"
  checkerExitCode := fun _ => some 0
  checkerOutput := fun _ => some "Your solution is okay!"
  coverageMapping := fun x => if x = false then some false else none

theorem forged_receipt_metadata_complete :
    receiptReadyAt forgedReceipt false := by
  simp [receiptReadyAt, forgedReceipt]

theorem forged_receipt_not_mathematical_enclosure :
    ∃ lower upper : ℝ,
      forgedReceipt.lowerEndpoint false = some lower ∧
      forgedReceipt.upperEndpoint false = some upper ∧
      ¬ lower ≤ upper := by
  exact ⟨1, 0, by simp [forgedReceipt], by simp [forgedReceipt], by norm_num⟩

theorem receipt_metadata_does_not_imply_enclosure :
    receiptReadyAt forgedReceipt false ∧
      (∃ lower upper : ℝ,
        forgedReceipt.lowerEndpoint false = some lower ∧
        forgedReceipt.upperEndpoint false = some upper ∧
        ¬ lower ≤ upper) := by
  constructor
  · exact forged_receipt_metadata_complete
  · exact forged_receipt_not_mathematical_enclosure

end

end RouteBP3CentralFDHullIntervalReceipt

#print axioms RouteBP3CentralFDHullIntervalReceipt.missing_required_field_fail_closed
#print axioms RouteBP3CentralFDHullIntervalReceipt.missing_coverage_mapping_fail_closed
#print axioms RouteBP3CentralFDHullIntervalReceipt.receipt_metadata_does_not_imply_enclosure

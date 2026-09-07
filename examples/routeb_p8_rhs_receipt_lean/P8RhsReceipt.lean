import RouteBP8PicardStep
import Mathlib.Data.Fin.Basic
import Mathlib.Tactic

/-!
# P8 RHS receipt interface

This file is the source-side seam for the 14-coordinate `hbox` premise used by
`RouteBP8PicardStep`.  It defines data and a transport theorem only.  It does
not define the deployed Julia `full_rhs!`, and it contains no numerical RHS
payload.

The coordinate order inherited from the parent is
`q₁ … q₆, dq₁ … dq₆, w, c`.  A `Fin 14 → ℝ` endpoint is total on exactly this
finite index type, so an endpoint payload cannot silently omit a coordinate.
-/

namespace RouteBP8RhsReceipt

set_option autoImplicit false

open RouteBP8PicardStep

abbrev Coordinate := Fin 14
abbrev State14 := RouteBP8PicardStep.State14
abbrev VectorField := RouteBP8PicardStep.VectorField
abbrev BoxPredicate := State14 → Prop

/- Metadata is explicit receipt data.  It is not used as a proof of the RHS
   interval claim; that claim is the separate `contains` field below. -/
inductive RoundingDirection where
  | outward
  | inward
  | nearest
  | unspecified
deriving DecidableEq, Repr

structure RoundingMetadata where
  direction : RoundingDirection
  precisionBits : Nat
  arithmetic : String
  note : String
deriving Repr

/- The only status provided by this leaf is deliberately `open`: a concrete
   binding of the deployed Julia `full_rhs!` must be supplied by a later,
   source-authenticated artifact. -/
inductive FullRhsBindingStatus where
  | open
deriving DecidableEq, Repr

/- A finite, indexed pair of endpoint vectors.  Since both fields have type
   `Fin 14 → ℝ`, all fourteen lower and upper endpoints are present. -/
structure FiniteEndpointPayload where
  lower : Coordinate → ℝ
  upper : Coordinate → ℝ
  lower_le_upper : ∀ i, lower i ≤ upper i

structure RhsReceipt where
  endpoints : FiniteEndpointPayload
  sourceHash : String
  rounding : RoundingMetadata
  fullRhsBinding : FullRhsBindingStatus

def CoordinateWiseIntervalContainment
    (F : VectorField) (B : BoxPredicate)
    (payload : FiniteEndpointPayload) : Prop :=
  ∀ y, B y → ∀ i : Coordinate,
    payload.lower i ≤ RouteBP8PicardStep.full_rhs! F y i ∧
      RouteBP8PicardStep.full_rhs! F y i ≤ payload.upper i

def RhsReceipt.Contains
    (receipt : RhsReceipt) (F : VectorField) (B : BoxPredicate) : Prop :=
  CoordinateWiseIntervalContainment F B receipt.endpoints

theorem finite_endpoint_payload_has_fourteen_coordinates
    : Fintype.card Coordinate = 14 := by
  simp [Coordinate]

theorem endpoint_payload_lower_le_upper
    (receipt : RhsReceipt) :
    ∀ i : Coordinate, receipt.endpoints.lower i ≤ receipt.endpoints.upper i := by
  exact receipt.endpoints.lower_le_upper

/- This is the exact coordinate-wise conversion to the parent hbox premise. -/
theorem receipt_to_routeBP8PicardStep_hbox
    (receipt : RhsReceipt) (F : VectorField) (B : BoxPredicate)
    (hcontains : receipt.Contains F B) :
    RouteBP8PicardStep.RhsIntervalPremise F B
      receipt.endpoints.lower receipt.endpoints.upper := by
  intro y hy i
  exact hcontains y hy i

/- The conversion can be consumed directly by the parent P8 decomposition.
   No endpoint, hash, rounding record, or Julia binding is invented here. -/
theorem receipt_usable_for_routeBP8PicardStep
    {F : VectorField} {z₀ z : State14} {h : ℝ}
    {receipt : RhsReceipt}
    (hz₀ : RouteBP8PicardStep.FullX0 z₀)
    (hh : 0 ≤ h)
    (hramp : RouteBP8PicardStep.RampRhsPremise F)
    (hcontains : receipt.Contains F RouteBP8PicardStep.InitialBox)
    (hz : RouteBP8PicardStep.picardImage F z₀ h
      RouteBP8PicardStep.InitialBox z) :
    RouteBP8PicardStep.InitialBox z₀ ∧
      RouteBP8PicardStep.picardStepBox z₀ receipt.endpoints.lower
        receipt.endpoints.upper h z ∧
      RouteBP8PicardStep.rampPicardCoordinates z₀ h
        RouteBP8PicardStep.InitialBox z := by
  exact RouteBP8PicardStep.fullX0_ramp_picard_step_decomposition
    hz₀ hh hramp (receipt_to_routeBP8PicardStep_hbox receipt F
      RouteBP8PicardStep.InitialBox hcontains) hz

/- The metadata fields are intentionally observable and remain independent of
   the semantic containment proposition. -/
theorem receipt_metadata_is_explicit
    (receipt : RhsReceipt) :
    receipt.sourceHash = receipt.sourceHash ∧
      receipt.rounding.direction = receipt.rounding.direction ∧
      receipt.rounding.precisionBits = receipt.rounding.precisionBits ∧
      receipt.fullRhsBinding = FullRhsBindingStatus.open := by
  exact ⟨rfl, rfl, rfl, by cases receipt.fullRhsBinding; rfl⟩

#print axioms finite_endpoint_payload_has_fourteen_coordinates
#print axioms endpoint_payload_lower_le_upper
#print axioms receipt_to_routeBP8PicardStep_hbox
#print axioms receipt_usable_for_routeBP8PicardStep
#print axioms receipt_metadata_is_explicit

end RouteBP8RhsReceipt

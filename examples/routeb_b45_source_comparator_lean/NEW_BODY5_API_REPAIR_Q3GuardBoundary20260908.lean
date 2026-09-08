import BodyTraceEvaluator
import NEW_BODY5_API_REPAIR_SliceBoundaryCore20260908

set_option autoImplicit false

namespace NEW_BODY5_API_REPAIR_Q3GuardBoundary20260908

/-! OPEN_UNCOMPILED. No Lean/Lake execution, closed data decision, or admission.
Imports the frozen evaluator, not the shared adapter, targets, or skeletons.
BodyTraceEvaluator itself imports Mathlib; this is NOT a minimal Mathlib closure.
Any encoding (function-frequency or tuple-frequency) must supply its own left inverse. -/

open RouteBO1PerBodyTraceGenerated
open NEW_BODY5_API_REPAIR_SliceBoundaryCore20260908

def keepQ3 (r : BodyTraceRow) : Bool := decide (r.frequency 3 ≠ 0)

noncomputable section

def q3Rows : List BodyTraceRow := bodyTraceRows5.filter keepQ3

/-- Only the source-row decoder law and coded slice binding are consumed.
For paired representatives use blocks r = [r, body5Conjugate r] downstream.
No whole-list Perm, conjugate identity, or real-valued evaluation is manufactured. -/
theorem q3_blocks_from_codes {Code : Type*}
    (enc : BodyTraceRow → Code) (dec : Code → BodyTraceRow)
    (hinv : ∀ r, dec (enc r) = r) (keepCode : Code → Bool)
    (hkeep : ∀ r, keepCode (enc r) = keepQ3 r)
    (reps : List BodyTraceRow) (blocks : BodyTraceRow → List BodyTraceRow)
    (hcodes : List.Perm ((bodyTraceRows5.map enc).filter keepCode)
      ((reps.flatMap blocks).map enc))
    (q : Fin 6 → ℝ) (i j : Fin 6) (seed : ℝ) :
    q3Rows.foldl (fun acc r => acc + traceRowContribution 4 i j q r) seed =
      seed + (reps.map (fun r =>
        ((blocks r).map (traceRowContribution 4 i j q)).sum)).sum := by
  exact encoded_slice_blocks enc dec hinv keepQ3 keepCode hkeep
    bodyTraceRows5 reps blocks hcodes (traceRowContribution 4 i j q) seed

/-- This leaf never unfolds traceAtom, tracePhase, or rational coefficients. -/
theorem contribution_off_entry (r : BodyTraceRow) (body i j : Fin 6)
    (q : Fin 6 → ℝ) (h : r.row ≠ i ∨ r.col ≠ j) :
    traceRowContribution body i j q r = 0 := by
  have hg : ¬(r.body = body ∧ r.row = i ∧ r.col = j) := by
    intro he
    rcases h with hr | hc
    · exact hr he.2.1
    · exact hc he.2.2
  exact if_neg hg

/-- The directed-entry support packet remains an explicit obligation.
Frequency nonzero alone does not imply that an arbitrary entry is off support. -/
theorem q3_off_support (q : Fin 6 → ℝ) (i j : Fin 6) (seed : ℝ)
    (hsupport : ∀ r ∈ q3Rows, r.row ≠ i ∨ r.col ≠ j) :
    q3Rows.foldl (fun acc r => acc + traceRowContribution 4 i j q r) seed = seed := by
  apply fold_zero_on
  intro r hr
  exact contribution_off_entry r 4 i j q (hsupport r hr)

end
end NEW_BODY5_API_REPAIR_Q3GuardBoundary20260908

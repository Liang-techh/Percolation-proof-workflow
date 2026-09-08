import RouteBO1Body5SourceTraceTargets
import NEW_BODY5_API_REPAIR_SliceCore20260908

set_option autoImplicit false

namespace NEW_BODY5_API_REPAIR_Q3FromFull20260908

/-! OPEN_UNCOMPILED. All data bindings remain explicit premises.
No old NEW_BODY5 module is imported. No source row is replaced or deduplicated. -/

open RouteBO1PerBodyTraceGenerated RouteBO1PerBodyExactSource
open RouteBO1Body5SourceTraceTargets NEW_BODY5_API_REPAIR_SliceCore20260908

abbrev RowCode := Fin 6 × Fin 6 × Fin 6 × (Fin 6 → ℤ) × ℤ × ℤ × ℤ × ℤ

def encode (r : BodyTraceRow) : RowCode :=
  (r.body, r.row, r.col, r.frequency, r.realCoeff.numerator,
    r.realCoeff.denominator, r.imagCoeff.numerator, r.imagCoeff.denominator)

def decode (c : RowCode) : BodyTraceRow :=
  let (b, i, j, nu, rn, rd, an, ad) := c
  ⟨b, i, j, nu, ⟨rn, rd⟩, ⟨an, ad⟩⟩

theorem decode_encode (r : BodyTraceRow) : decode (encode r) = r := by
  cases r with
  | mk b i j nu re im =>
      cases re
      cases im
      rfl

def keepQ3 (r : BodyTraceRow) : Bool := decide (r.frequency 3 ≠ 0)

noncomputable section

theorem keep_conjugate (r : BodyTraceRow) :
    keepQ3 (body5Conjugate r) = keepQ3 r := by
  simp [keepQ3, body5Conjugate]

/-- Full raw-label Perm plus constant exclusion suffices for the q3 slice. -/
theorem q3_binding_from_full (constants reps : List BodyTraceRow)
    (hc : constants.filter keepQ3 = [])
    (hCodes : List.Perm (bodyTraceRows5.map encode)
      ((constants ++ reps.flatMap (fun r => [r, body5Conjugate r])).map encode)) :
    List.Perm (bodyTraceRows5.filter keepQ3)
      ((reps.filter keepQ3).flatMap (fun r => [r, body5Conjugate r])) := by
  exact slice_from_full keepQ3 body5Conjugate keep_conjugate
    bodyTraceRows5 constants reps hc (decode_perm encode decode decode_encode hCodes)

/-- Conjugate collapse, eight-row evaluation and support are NOT assumed silently. -/
theorem q3_fold_from_full (constants reps : List BodyTraceRow)
    (hc : constants.filter keepQ3 = [])
    (hCodes : List.Perm (bodyTraceRows5.map encode)
      ((constants ++ reps.flatMap (fun r => [r, body5Conjugate r])).map encode))
    (q : Q6) (i j : Fin 6) (seed : ℝ) :
    body5Fold (bodyTraceRows5.filter keepQ3) q i j seed = seed +
      ((reps.filter keepQ3).map (fun r =>
        traceRowContribution body5Index i j q r +
        traceRowContribution body5Index i j q (body5Conjugate r))).sum := by
  have hp := q3_binding_from_full constants reps hc hCodes
  unfold body5Fold
  rw [seeded_fold, sum_under_perm (traceRowContribution body5Index i j q) hp, pair_sum]

end
end NEW_BODY5_API_REPAIR_Q3FromFull20260908

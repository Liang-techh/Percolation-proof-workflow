import RouteBO1Body5SourceTraceTargets
import Mathlib.Tactic.FinCases
import NEW_BODY5_API_REPAIR_CodedFilterCore20260908

set_option autoImplicit false

namespace NEW_BODY5_API_REPAIR_TupleQ3Join20260908

/-! OPEN_UNCOMPILED. No Lean/Lake run, finite decision run, or admission.
The new code filter is not the old classical representative filter.
All source-list permutations and collapsed values remain explicit premises. -/

open RouteBO1PerBodyTraceGenerated RouteBO1PerBodyExactSource
open RouteBO1Body5SourceTraceTargets
open NEW_BODY5_API_REPAIR_CodedFilterCore20260908

abbrev FrequencyCode := ℤ × ℤ × ℤ × ℤ × ℤ × ℤ
abbrev RowCode := Fin 6 × Fin 6 × Fin 6 × FrequencyCode × ℤ × ℤ × ℤ × ℤ

def encode (r : BodyTraceRow) : RowCode :=
  (r.body, r.row, r.col,
    (r.frequency 0, r.frequency 1, r.frequency 2,
      r.frequency 3, r.frequency 4, r.frequency 5),
    r.realCoeff.numerator, r.realCoeff.denominator,
    r.imagCoeff.numerator, r.imagCoeff.denominator)

def decode (c : RowCode) : BodyTraceRow :=
  let (b, i, j, (n0, n1, n2, n3, n4, n5), rn, rd, an, ad) := c
  ⟨b, i, j, ![n0, n1, n2, n3, n4, n5], ⟨rn, rd⟩, ⟨an, ad⟩⟩

theorem frequency_eta (nu : Fin 6 → ℤ) :
    ![nu 0, nu 1, nu 2, nu 3, nu 4, nu 5] = nu := by
  funext k
  fin_cases k <;> rfl

theorem decode_encode (r : BodyTraceRow) : decode (encode r) = r := by
  cases r with
  | mk b i j nu re im =>
      cases re
      cases im
      simp only [encode, decode, frequency_eta]

def keepRowQ3 (r : BodyTraceRow) : Bool := decide (r.frequency 3 ≠ 0)

def keepCodeQ3 (c : RowCode) : Bool :=
  let (_, _, _, (_, _, _, n3, _, _), _, _, _, _) := c
  decide (n3 ≠ 0)

theorem keep_encode (r : BodyTraceRow) : keepCodeQ3 (encode r) = keepRowQ3 r := by
  rfl

theorem decode_source_slice :
    ((bodyTraceRows5.map encode).filter keepCodeQ3).map decode =
      bodyTraceRows5.filter keepRowQ3 := by
  exact decode_filtered_map encode decode decode_encode
    keepRowQ3 keepCodeQ3 keep_encode bodyTraceRows5

/-- A smaller coded slice obligation can be derived from an already supplied full Perm.
The canonical code filter equality is still a separate data obligation. -/
theorem slice_codes_from_full (canonical : List BodyTraceRow) (slice : List RowCode)
    (hfull : List.Perm (bodyTraceRows5.map encode) (canonical.map encode))
    (hfilter : (canonical.map encode).filter keepCodeQ3 = slice) :
    List.Perm ((bodyTraceRows5.map encode).filter keepCodeQ3) slice := by
  have hp := List.Perm.filter keepCodeQ3 hfull
  rw [hfilter] at hp
  exact hp

noncomputable section

/-- Whole-vector conjugation is retained; transpose is not a partner operation. -/
theorem q3_rows_perm (reps : List BodyTraceRow)
    (hCodes : List.Perm ((bodyTraceRows5.map encode).filter keepCodeQ3)
      ((reps.flatMap (fun r => [r, body5Conjugate r])).map encode)) :
    List.Perm (bodyTraceRows5.filter keepRowQ3)
      (reps.flatMap (fun r => [r, body5Conjugate r])) := by
  exact rows_perm_of_filtered_codes encode decode decode_encode
    keepRowQ3 keepCodeQ3 keep_encode bodyTraceRows5 _ hCodes

theorem q3_seeded_pairs (reps : List BodyTraceRow)
    (hCodes : List.Perm ((bodyTraceRows5.map encode).filter keepCodeQ3)
      ((reps.flatMap (fun r => [r, body5Conjugate r])).map encode))
    (q : Q6) (i j : Fin 6) (seed : ℝ) :
    body5Fold (bodyTraceRows5.filter keepRowQ3) q i j seed = seed +
      (reps.map (fun r => traceRowContribution body5Index i j q r +
        traceRowContribution body5Index i j q (body5Conjugate r))).sum := by
  have hp := q3_rows_perm reps hCodes
  unfold body5Fold
  rw [seeded_sum, perm_sum (traceRowContribution body5Index i j q) hp, flatMap_sum]
  simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil, add_zero]

/-- Evaluation is a distinct premise, not a consequence of code comparison alone. -/
theorem q3_seeded_value (reps : List BodyTraceRow)
    (hCodes : List.Perm ((bodyTraceRows5.map encode).filter keepCodeQ3)
      ((reps.flatMap (fun r => [r, body5Conjugate r])).map encode))
    (q : Q6) (i j : Fin 6) (seed value : ℝ)
    (hValue : (reps.map (fun r => traceRowContribution body5Index i j q r +
      traceRowContribution body5Index i j q (body5Conjugate r))).sum = value) :
    body5Fold (bodyTraceRows5.filter keepRowQ3) q i j seed = seed + value := by
  rw [q3_seeded_pairs reps hCodes q i j seed, hValue]

end
end NEW_BODY5_API_REPAIR_TupleQ3Join20260908

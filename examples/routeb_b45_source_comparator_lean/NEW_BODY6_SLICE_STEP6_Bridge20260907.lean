import NEW_BODY6_SLICE_STEP6_Core20260907
import NEW_BODY6_SLICE_20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_STEP6_Bridge20260907

noncomputable section

open RouteBO1PerBodyExactSource RouteBO1Body6CanonicalExportTargets
open RouteBBodySemanticCore RouteBSourceContractAdapter
open RouteBFrameOriginAxis RouteBFrameSlotAccessor RouteBRealDHStep
open RouteBB45Fourier RouteBB45FrameRecursion
open NEW_BODY6_SLICE_20260907 NEW_BODY6_SLICE_20260907Data

open NEW_BODY6_SLICE_STEP6_Core20260907

/- UNCOMPILED source attachment. All source references below are the actual
   existing definitions; the independent Core imports none of them.
   No Python check, row count or CSV hash is a premise of these theorems. -/

theorem step6_last_column_attempt (t : ℝ) (k : Fin 4) :
    routeBRealStepMatrix (5 : Fin 6) t k 3 =
      (![0, 0, (7 / 100 : ℝ), 1] : Fin 4 → ℝ) k := by
  fin_cases k <;>
    norm_num [routeBRealStepMatrix, realDHStep, routeBRealCos, routeBRealSin,
      routeBCosAlpha, routeBSinAlpha, routeBA, routeBD]

theorem slot6_recursion_attempt (q : Q6) :
    routeBFrameSlot q (6 : Fin 7) =
      routeBFrameSlot q (5 : Fin 7) * routeBRealStepMatrix (5 : Fin 6) (q 5) := by
  rfl

theorem source_endpoint_attempt : Body6EndpointTarget := by
  intro q a
  have ho6 := congrFun (congrFun (source_origin_function_eq_frame_contract q)
    (6 : Fin 7)) a
  have ho5 := congrFun (congrFun (source_origin_function_eq_frame_contract q)
    (5 : Fin 7)) a
  have hz5 := congrFun (congrFun (source_axis_function_eq_frame_contract q)
    (5 : Fin 6)) a
  rw [ho6, ho5, hz5]
  change (routeBFrameSlot q (6 : Fin 7)) (embed3 a) 3 =
    (routeBFrameSlot q (5 : Fin 7)) (embed3 a) 3 +
      (7 / 100 : ℝ) * (routeBFrameSlot q (5 : Fin 7)) (embed3 a) 2
  rw [slot6_recursion_attempt]
  exact product_endpoint_attempt _ _ (7 / 100)
    (step6_last_column_attempt (q 5)) (embed3 a)

theorem source_center_attempt : Body6CenterTarget :=
  endpoint_to_center_attempt source_endpoint_attempt

theorem source_sixth_linear_zero_attempt (q : Q6) (a : Fin 3) :
    bodyJv (sourceContract q).origins (sourceContract q).axes (5 : Fin 6) a
      (5 : Fin 6) = 0 := by
  rw [source_linear_column_attempt source_center_attempt]
  exact sixth_velocity_attempt q a

theorem source_gram_attempt : Body6SourceGramTarget :=
  center_to_source_gram_attempt source_center_attempt

def liftRow (r : Row) : CanonicalRow :=
  { row := r.row, col := ⟨5, by decide⟩,
    frequency := ![0, r.nx, r.nx, r.ny, r.nz, 0],
    realCoeff := r.coeff, imagCoeff := 0 }

def localCanonicalRows : List CanonicalRow := rows23.map liftRow

theorem lift_atom_attempt (r : Row) (q : Q6) :
    canonicalAtom (liftRow r) q = atom3 r (q 1 + q 2) (q 3) (q 4) := by
  have hp : phase (liftRow r).frequency q =
      phase3 r (q 1 + q 2) (q 3) (q 4) := by
    norm_num [phase, liftRow, phase3, Fin.sum_univ_succ] <;> ring
  change realFourierAtom (liftRow r).frequency r.coeff 0 q = _
  unfold realFourierAtom
  rw [hp]
  simp [atom3]

theorem lift_rows_attempt (rs : List Row) (q : Q6) (i : Fin 6) :
    body6CanonicalEvaluator (rs.map liftRow) q i (5 : Fin 6) =
      evalRows rs (q 1 + q 2) (q 3) (q 4) i := by
  unfold body6CanonicalEvaluator evalRows
  rw [List.map_map]
  have hf : (fun r : Row =>
      if (liftRow r).row = i ∧ (liftRow r).col = (5 : Fin 6)
      then canonicalAtom (liftRow r) q else 0) =
    (fun r : Row => if r.row = i
      then atom3 r (q 1 + q 2) (q 3) (q 4) else 0) := by
    funext r
    change (if r.row = i ∧ (5 : Fin 6) = 5
      then canonicalAtom (liftRow r) q else 0) = _
    simp only [eq_self_iff_true, and_true]
    by_cases hi : r.row = i
    · simp only [hi, if_true, lift_atom_attempt]
    · simp only [hi, if_false]
  change (rs.map (fun r : Row =>
    if (liftRow r).row = i ∧ (liftRow r).col = (5 : Fin 6)
    then canonicalAtom (liftRow r) q else 0)).sum = _
  rw [hf]

theorem local_column_fold_attempt (q : Q6) (i : Fin 6) :
    body6CanonicalEvaluator localCanonicalRows q i (5 : Fin 6) =
      sixthColumnFormula q i := by
  rw [show localCanonicalRows = rows23.map liftRow from rfl, lift_rows_attempt]
  rw [rows23_fold_attempt]
  rfl

/- This generic filtering lemma retains the entire list and its zero entries.
   It needs neither source semantics nor a row-count assumption. -/
theorem filter_column_attempt (rs : List CanonicalRow) (q : Q6) (i j : Fin 6) :
    body6CanonicalEvaluator (rs.filter (fun r => decide (r.col = j))) q i j =
      body6CanonicalEvaluator rs q i j := by
  induction rs with
  | nil => rfl
  | cons r rs ih =>
      by_cases hc : r.col = j
      · simpa [body6CanonicalEvaluator, hc] using
          congrArg (fun t : ℝ =>
            (if r.row = i ∧ r.col = j then canonicalAtom r q else 0) + t) ih
      · simpa [body6CanonicalEvaluator, hc] using ih

theorem full_filter_attempt : SixthColumnFilterTarget := by
  intro q i
  exact filter_column_attempt canonicalRows q i (5 : Fin 6)

/- Isolate the literal-data computation. Equality of the concrete lists,
   including every frequency and rational coefficient, is required. -/
def LiteralColumnBindingTarget : Prop := sixthColumnRows = localCanonicalRows

theorem sixth_fourier_of_literal_attempt (hd : LiteralColumnBindingTarget) :
    SixthColumnFourierTarget := by
  intro q i
  calc
    sliceEvaluator q i (5 : Fin 6) =
        body6CanonicalEvaluator sixthColumnRows q i (5 : Fin 6) :=
      (full_filter_attempt q i).symm
    _ = body6CanonicalEvaluator localCanonicalRows q i (5 : Fin 6) := by rw [hd]
    _ = sixthColumnFormula q i := local_column_fold_attempt q i

/- Source axis dot products remain a real mathematical obligation.
   Endpoint and the independent Fourier fold do not establish this premise. -/
theorem endpoint_to_sixth_column_seam_attempt
    (ha : SourceAxisDotTarget) (hd : LiteralColumnBindingTarget) :
    ∀ q i, sourceBodyMass q (5 : Fin 6) i (5 : Fin 6) =
      sliceEvaluator q i (5 : Fin 6) := by
  exact sixth_slice_seam_attempt source_gram_attempt ha
    (sixth_fourier_of_literal_attempt hd)

/- Preserve all 36 entries and the explicit four-entry zero complement.
   The sixth-column result is deliberately insufficient to invoke this seam. -/
theorem global_source_and_zero_seam_attempt
    (hall : AllEntriesGramFourierTarget) (hzero : EmptyFourierTarget) :
    SourceBindingTarget ∧
      (∀ q i j, EmptyEntry i j → sourceBodyMass q (5 : Fin 6) i j = 0) := by
  have hs : SourceBindingTarget := source_binding_seam_attempt source_gram_attempt hall
  refine ⟨hs, ?_⟩
  intro q i j he
  exact source_zero_complement_attempt hs hzero q i j he

end
end NEW_BODY6_SLICE_STEP6_Bridge20260907

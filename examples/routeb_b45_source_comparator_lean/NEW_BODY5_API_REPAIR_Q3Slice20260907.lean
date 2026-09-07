import RouteBO1Body5SourceTraceTargets
import NEW_BODY5_API_REPAIR_RowCode20260907

set_option autoImplicit false

namespace NEW_BODY5_API_REPAIR_Q3Slice20260907

noncomputable section

open RouteBO1PerBodyExactSource RouteBO1PerBodyTraceGenerated
open RouteBO1Body5SourceTraceTargets
open NEW_BODY5_API_REPAIR_ListFinset20260907
open NEW_BODY5_API_REPAIR_RowCode20260907

/-!
OPEN / UNCOMPILED. Independent q3 slice API; no import of either skeleton.
q3 means zero-based q 3. No old classical-filter target is discharged here.
The source-row binding and conjugate-atom identity remain explicit premises.
Only the separate DataLeaf module attempts the closed source permutation.
-/

def q3Keep (r : BodyTraceRow) : Bool := decide (r.frequency 3 ≠ 0)

def sourceQ3Rows : List BodyTraceRow := bodyTraceRows5.filter q3Keep

def q3Representatives : List BodyTraceRow :=
  [body5RealRow 0 4 1 1 (-1) 1 120,
   body5RealRow 0 4 1 1 1 (-1) 120,
   body5RealRow 4 0 1 1 (-1) 1 120,
   body5RealRow 4 0 1 1 1 (-1) 120,
   body5RealRow 1 4 0 0 1 1 60,
   body5RealRow 4 1 0 0 1 1 60,
   body5RealRow 2 4 0 0 1 1 60,
   body5RealRow 4 2 0 0 1 1 60]

def q3PairedRows : List BodyTraceRow :=
  q3Representatives.flatMap (fun r => [r, body5Conjugate r])

theorem q3_filter_perm (xs ys : List BodyTraceRow) (h : List.Perm xs ys) :
    List.Perm (xs.filter q3Keep) (ys.filter q3Keep) := by
  exact List.Perm.filter q3Keep h

theorem q3_conjugate_keep (r : BodyTraceRow) :
    q3Keep (body5Conjugate r) = q3Keep r := by
  simp only [q3Keep, body5Conjugate, neg_ne_zero]

theorem source_q3_frequency (r : BodyTraceRow) (h : r ∈ sourceQ3Rows) :
    r.frequency 3 ≠ 0 := by
  change r ∈ bodyTraceRows5.filter q3Keep at h
  have hp : q3Keep r = true := (List.mem_filter.mp h).2
  simpa only [q3Keep, decide_eq_true_eq] using hp

theorem phase_frequency (u v w : ℤ) (q : Q6) :
    tracePhase (body5Frequency u v w) q =
      (u : ℝ) * q 1 + (v : ℝ) * q 2 + (w : ℝ) * q 3 := by
  unfold tracePhase
  rw [fin6_sum]
  norm_num [body5Frequency]

def pairValue (q : Q6) (i j : Fin 6) (r : BodyTraceRow) : ℝ :=
  if r.body = body5Index ∧ r.row = i ∧ r.col = j then 2 * traceAtom r q else 0

theorem contribution_pair (hAtom : Body5ConjugateAtomTarget)
    (q : Q6) (i j : Fin 6) (r : BodyTraceRow) :
    traceRowContribution body5Index i j q r +
      traceRowContribution body5Index i j q (body5Conjugate r) =
        pairValue q i j r := by
  by_cases h : r.body = body5Index ∧ r.row = i ∧ r.col = j
  · simpa only [traceRowContribution, pairValue, body5Conjugate, if_pos h,
      traceAtom] using hAtom r q
  · simp only [traceRowContribution, pairValue, body5Conjugate, if_neg h, add_zero]

def q3Entry (i j : Fin 6) : Prop :=
  ((i = 0 ∧ j = 4) ∨ (i = 4 ∧ j = 0)) ∨
    ((i = 1 ∧ j = 4) ∨ (i = 4 ∧ j = 1) ∨
      (i = 2 ∧ j = 4) ∨ (i = 4 ∧ j = 2))

def q3Value (q : Q6) (i j : Fin 6) : ℝ :=
  if (i = 0 ∧ j = 4) ∨ (i = 4 ∧ j = 0) then
    (1 / 60) * (Real.cos (body5Phi q - q 3) - Real.cos (body5Phi q + q 3))
  else if (i = 1 ∧ j = 4) ∨ (i = 4 ∧ j = 1) ∨
      (i = 2 ∧ j = 4) ∨ (i = 4 ∧ j = 2) then (1 / 30) * Real.cos (q 3)
  else 0

/-- Only eight representative rows; the generic phase lemma is used first. -/
theorem q3_pairs_value (q : Q6) (i j : Fin 6) :
    (q3Representatives.map (pairValue q i j)).sum = q3Value q i j := by
  fin_cases i <;> fin_cases j <;>
    norm_num [q3Representatives, pairValue, traceAtom, body5RealRow, body5Index,
      rationalReal, rationalImag, RationalTag.toRat, phase_frequency,
      q3Value, body5Phi, sub_eq_add_neg] <;> ring

/-- No 36-case enumeration or trigonometric simplification off support. -/
theorem q3_value_off_support (q : Q6) (i j : Fin 6) (h : ¬q3Entry i j) :
    q3Value q i j = 0 := by
  have hm : ¬((i = 0 ∧ j = 4) ∨ (i = 4 ∧ j = 0)) :=
    fun hm => h (Or.inl hm)
  have hc : ¬((i = 1 ∧ j = 4) ∨ (i = 4 ∧ j = 1) ∨
      (i = 2 ∧ j = 4) ∨ (i = 4 ∧ j = 2)) := fun hc => h (Or.inr hc)
  simp only [q3Value, if_neg hm, if_neg hc]

/-- Exact uncollapsed handoff, usable before the atom/trig leaves. -/
theorem q3_source_fold_pairs
    (hCodes : List.Perm (sourceQ3Rows.map tupleRowCode) (q3PairedRows.map tupleRowCode))
    (q : Q6) (i j : Fin 6) (seed : ℝ) :
    body5Fold sourceQ3Rows q i j seed = seed +
      (q3Representatives.map (fun r =>
        traceRowContribution body5Index i j q r +
          traceRowContribution body5Index i j q (body5Conjugate r))).sum := by
  have hp := perm_of_tupleRowCodes sourceQ3Rows q3PairedRows hCodes
  unfold body5Fold
  rw [fold_add_perm (traceRowContribution body5Index i j q) hp seed]
  exact fold_pairs body5Conjugate (traceRowContribution body5Index i j q)
    q3Representatives seed

theorem q3_source_fold_conditional
    (hCodes : List.Perm (sourceQ3Rows.map tupleRowCode) (q3PairedRows.map tupleRowCode))
    (hAtom : Body5ConjugateAtomTarget) (q : Q6) (i j : Fin 6) (seed : ℝ) :
    body5Fold sourceQ3Rows q i j seed = seed + q3Value q i j := by
  rw [q3_source_fold_pairs hCodes]
  simp only [contribution_pair hAtom, q3_pairs_value]

theorem q3_source_off_support_conditional
    (hCodes : List.Perm (sourceQ3Rows.map tupleRowCode) (q3PairedRows.map tupleRowCode))
    (hAtom : Body5ConjugateAtomTarget) (q : Q6) (i j : Fin 6)
    (h : ¬q3Entry i j) (seed : ℝ) : body5Fold sourceQ3Rows q i j seed = seed := by
  rw [q3_source_fold_conditional hCodes hAtom, q3_value_off_support q i j h, add_zero]

end
end NEW_BODY5_API_REPAIR_Q3Slice20260907

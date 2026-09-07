import NEW_BODY5_GramTraceSkeleton20260907

set_option autoImplicit false

namespace NEW_BODY5_FiniteTraceSkeleton20260907

noncomputable section

open RouteBO1PerBodyExactSource RouteBO1PerBodyTraceAdapter
open RouteBO1PerBodyTraceGenerated RouteBO1Body5SourceTraceTargets
open NEW_BODY5_GramTraceSkeleton20260907

/-!
OPEN / UNCOMPILED. All proof bodies below are attempts, including `decide`.
No local Lean/Lake run, dependency check or admission is represented here.

The new literal lists are proposed reorganizations of the frozen source,
not replacement source data. Their whole-record Perm binding is essential.
The old classical filters are not fed to an executable decision procedure.
-/

def imagRow (i j : Fin 6) (u v w n d : ℤ) : BodyTraceRow where
  body := body5Index
  row := i
  col := j
  frequency := body5Frequency u v w
  realCoeff := ⟨0, 1⟩
  imagCoeff := ⟨n, d⟩

def constants : List BodyTraceRow :=
  [body5RealRow 0 0 0 0 0 1441 30000,
   body5RealRow 1 1 0 0 0 8609 150000,
   body5RealRow 1 2 0 0 0 13249 300000,
   body5RealRow 2 1 0 0 0 13249 300000,
   body5RealRow 2 2 0 0 0 13249 300000,
   body5RealRow 3 3 0 0 0 1 30,
   body5RealRow 4 4 0 0 0 1 30]

def reps17 : List BodyTraceRow :=
  [body5RealRow 0 0 0 1 0 1197 200000,
   imagRow 0 0 1 0 0 (-63) 12500,
   imagRow 0 0 1 1 0 (-57) 12500,
   body5RealRow 0 0 2 0 0 (-1323) 400000,
   body5RealRow 0 0 2 1 0 (-1197) 200000,
   body5RealRow 0 0 2 2 0 (-1083) 400000,
   body5RealRow 0 1 1 0 0 (-63) 40000,
   body5RealRow 0 1 1 1 0 (-57) 40000,
   body5RealRow 1 0 1 0 0 (-63) 40000,
   body5RealRow 1 0 1 1 0 (-57) 40000,
   body5RealRow 0 2 1 1 0 (-57) 40000,
   body5RealRow 2 0 1 1 0 (-57) 40000,
   body5RealRow 0 3 1 1 0 1 60,
   body5RealRow 3 0 1 1 0 1 60,
   body5RealRow 1 1 0 1 0 1197 100000,
   body5RealRow 1 2 0 1 0 1197 200000,
   body5RealRow 2 1 0 1 0 1197 200000]

def repsQ3 : List BodyTraceRow :=
  [body5RealRow 0 4 1 1 (-1) 1 120,
   body5RealRow 0 4 1 1 1 (-1) 120,
   body5RealRow 4 0 1 1 (-1) 1 120,
   body5RealRow 4 0 1 1 1 (-1) 120,
   body5RealRow 1 4 0 0 1 1 60,
   body5RealRow 4 1 0 0 1 1 60,
   body5RealRow 2 4 0 0 1 1 60,
   body5RealRow 4 2 0 0 1 1 60]

def reps : List BodyTraceRow := reps17 ++ repsQ3

def pairedRows (rs : List BodyTraceRow) : List BodyTraceRow :=
  rs.flatMap (fun r => [r, body5Conjugate r])

def canonicalRows : List BodyTraceRow := constants ++ pairedRows reps

/- Preserve raw rational labels: do NOT replace numerator/denominator with
   a normalized rational. Frequencies remain full six-coordinate functions.
   RowCode has computable equality; BodyTraceRow need not gain an instance. -/
abbrev RowCode := Fin 6 × Fin 6 × Fin 6 × (Fin 6 → ℤ) × ℤ × ℤ × ℤ × ℤ

def rowCode (r : BodyTraceRow) : RowCode :=
  (r.body, r.row, r.col, r.frequency, r.realCoeff.numerator,
    r.realCoeff.denominator, r.imagCoeff.numerator, r.imagCoeff.denominator)

def decodeRow (c : RowCode) : BodyTraceRow :=
  let (b, i, j, nu, rn, rd, imn, imd) := c
  ⟨b, i, j, nu, ⟨rn, rd⟩, ⟨imn, imd⟩⟩

theorem decode_code_attempt (r : BodyTraceRow) : decodeRow (rowCode r) = r := by
  rcases r with ⟨b, i, j, nu, ⟨rn, rd⟩, ⟨imn, imd⟩⟩
  rfl

theorem perm_of_codes_attempt (xs ys : List BodyTraceRow)
    (h : List.Perm (xs.map rowCode) (ys.map rowCode)) : List.Perm xs ys := by
  have hd := h.map decodeRow
  simpa only [List.map_map, Function.comp_def, decode_code_attempt, List.map_id] using hd

/- This is the source-data leaf: 57 literal records, not real arithmetic.
   If reduction hits limits, split the same coded lists by entry and use
   Perm.append; do not replace it by partner existence or coefficient sums. -/
set_option maxRecDepth 4096 in
set_option maxHeartbeats 800000 in
theorem canonical_codes_attempt :
    List.Perm (bodyTraceRows5.map rowCode) (canonicalRows.map rowCode) := by
  decide

theorem canonical_binding_attempt : List.Perm bodyTraceRows5 canonicalRows := by
  exact perm_of_codes_attempt _ _ canonical_codes_attempt

theorem counts_attempt : constants.length = 7 ∧ reps17.length = 17 ∧
    repsQ3.length = 8 ∧ canonicalRows.length = 57 := by
  decide

/- Generic fold lemmas retain arbitrary seeds, so prefixes/suffixes compose. -/
theorem fold_add_sum_attempt {α : Type} (rs : List α) (f : α → ℝ) (seed : ℝ) :
    rs.foldl (fun acc r => acc + f r) seed = seed + (rs.map f).sum := by
  induction rs generalizing seed with
  | nil => simp
  | cons r rs ih => simp [List.foldl_cons, ih, add_assoc]

theorem fold_perm_attempt (xs ys : List BodyTraceRow) (h : List.Perm xs ys)
    (q : Q6) (i j : Fin 6) (seed : ℝ) :
    body5Fold xs q i j seed = body5Fold ys q i j seed := by
  unfold body5Fold
  rw [fold_add_sum_attempt, fold_add_sum_attempt]
  exact congrArg (fun t => seed + t) ((h.map (traceRowContribution body5Index i j q)).sum_eq)

theorem pair_sum_attempt (rs : List BodyTraceRow) (f : BodyTraceRow → ℝ) :
    ((pairedRows rs).map f).sum = (rs.map (fun r => f r + f (body5Conjugate r))).sum := by
  induction rs with
  | nil => simp [pairedRows]
  | cons r rs ih =>
      simpa [pairedRows, List.map_append, List.sum_append, add_assoc] using
        congrArg (fun t => (f r + f (body5Conjugate r)) + t) ih

/- This consumes precisely the Perm component of the old F1 target.
   Counts/Nodup/nonzero denominators remain separate source audit properties. -/
theorem regroup_from_partition_attempt (h : Body5ExactPartitionTarget) : Body5RegroupTarget := by
  rcases h with ⟨_, _, _, _, _, _, hp⟩
  intro q i j seed
  rw [fold_perm_attempt _ _ hp]
  unfold body5Fold
  rw [fold_add_sum_attempt]
  change seed + ((body5ConstantRows ++ pairedRows body5RepresentativeRows).map
    (traceRowContribution body5Index i j q)).sum = _
  rw [List.map_append, List.sum_append, pair_sum_attempt]
  rfl

def prefixRows : List BodyTraceRow :=
  ((bodyTraceRows1 ++ bodyTraceRows2) ++ bodyTraceRows3) ++ bodyTraceRows4

/- Closed tag checks touch no other-body trigonometry. -/
set_option maxRecDepth 4096 in
set_option maxHeartbeats 800000 in
theorem off_body_tags_attempt :
    (∀ b ∈ prefixRows.map (fun r => r.body), b ≠ body5Index) ∧
    (∀ b ∈ bodyTraceRows6.map (fun r => r.body), b ≠ body5Index) := by
  decide

theorem off_body_fold_attempt (rs : List BodyTraceRow)
    (h : ∀ r ∈ rs, r.body ≠ body5Index) (q : Q6) (i j : Fin 6) (seed : ℝ) :
    body5Fold rs q i j seed = seed := by
  induction rs generalizing seed with
  | nil => rfl
  | cons r rs ih =>
      have hr := h r (by simp)
      have ht : ∀ s ∈ rs, s.body ≠ body5Index := fun s hs => h s (by simp [hs])
      simpa [body5Fold, List.foldl_cons, traceRowContribution, hr] using ih ht seed

theorem full_to_block_attempt : Body5FullToBlockFoldTarget := by
  intro q i j seed
  have hp : ∀ r ∈ prefixRows, r.body ≠ body5Index := by
    intro r hr
    exact off_body_tags_attempt.1 r.body (List.mem_map.mpr ⟨r, hr, rfl⟩)
  have hs : ∀ r ∈ bodyTraceRows6, r.body ≠ body5Index := by
    intro r hr
    exact off_body_tags_attempt.2 r.body (List.mem_map.mpr ⟨r, hr, rfl⟩)
  change body5Fold ((prefixRows ++ bodyTraceRows5) ++ bodyTraceRows6) q i j seed = _
  simp only [body5Fold, List.foldl_append]
  change body5Fold bodyTraceRows6 q i j
    (body5Fold bodyTraceRows5 q i j (body5Fold prefixRows q i j seed)) = _
  rw [off_body_fold_attempt _ hp, off_body_fold_attempt _ hs]

theorem phase_attempt : Body5PhaseTarget := by
  intro u v w q
  simp [tracePhase, body5Frequency, Fin.sum_univ_succ]

theorem phase_neg_attempt (nu : Fin 6 → ℤ) (q : Q6) :
    tracePhase (fun k => -nu k) q = -tracePhase nu q := by
  simp [tracePhase, Finset.sum_neg_distrib, neg_mul]

theorem conjugate_atom_attempt : Body5ConjugateAtomTarget := by
  intro r q
  have him : rationalImag (body5Conjugate r).imagCoeff = -rationalImag r.imagCoeff := by
    simp [rationalImag, RationalTag.toRat, body5Conjugate, neg_div]
  change rationalReal r.realCoeff * Real.cos (tracePhase r.frequency q) -
    rationalImag r.imagCoeff * Real.sin (tracePhase r.frequency q) +
    (rationalReal r.realCoeff * Real.cos (tracePhase (fun k => -r.frequency k) q) -
      rationalImag (body5Conjugate r).imagCoeff *
        Real.sin (tracePhase (fun k => -r.frequency k) q)) = _
  rw [phase_neg_attempt, him, Real.cos_neg, Real.sin_neg]
  ring

def pairValue (q : Q6) (i j : Fin 6) (r : BodyTraceRow) : ℝ :=
  if r.body = body5Index ∧ r.row = i ∧ r.col = j then
    2 * (rationalReal r.realCoeff * Real.cos (tracePhase r.frequency q) -
      rationalImag r.imagCoeff * Real.sin (tracePhase r.frequency q))
  else 0

theorem contribution_pair_attempt (q : Q6) (i j : Fin 6) (r : BodyTraceRow) :
    traceRowContribution body5Index i j q r +
      traceRowContribution body5Index i j q (body5Conjugate r) = pairValue q i j r := by
  by_cases h : r.body = body5Index ∧ r.row = i ∧ r.col = j
  · simpa only [traceRowContribution, pairValue, body5Conjugate, if_pos h] using
      conjugate_atom_attempt r q
  · simp [traceRowContribution, pairValue, body5Conjugate, h]

def canonicalValue (q : Q6) (i j : Fin 6) : ℝ :=
  (constants.map (traceRowContribution body5Index i j q)).sum +
    (reps17.map (pairValue q i j)).sum + (repsQ3.map (pairValue q i j)).sum

theorem block_to_canonical_attempt (q : Q6) (i j : Fin 6) (seed : ℝ) :
    body5Fold bodyTraceRows5 q i j seed = seed + canonicalValue q i j := by
  rw [fold_perm_attempt _ _ canonical_binding_attempt]
  unfold body5Fold
  rw [fold_add_sum_attempt]
  simp only [canonicalRows, List.map_append, List.sum_append, pair_sum_attempt,
    contribution_pair_attempt, reps, canonicalValue]
  simp [List.map_append, List.sum_append, add_assoc]

/- q3 occupies six directed entries; transposes are independent records.
   The (1,1,-1) and (1,1,1) frequencies use correlated whole-vector negatives. -/
def q3Entry (i j : Fin 6) : Prop :=
  (i = 0 ∧ j = 4) ∨ (i = 4 ∧ j = 0) ∨
  (i = 1 ∧ j = 4) ∨ (i = 4 ∧ j = 1) ∨
  (i = 2 ∧ j = 4) ∨ (i = 4 ∧ j = 2)

def q3Value (q : Q6) (i j : Fin 6) : ℝ :=
  if (i = 0 ∧ j = 4) ∨ (i = 4 ∧ j = 0) then
    (1 / 60) * (Real.cos (body5Phi q - q 3) - Real.cos (body5Phi q + q 3))
  else if (i = 1 ∧ j = 4) ∨ (i = 4 ∧ j = 1) ∨
      (i = 2 ∧ j = 4) ∨ (i = 4 ∧ j = 2) then (1 / 30) * Real.cos (q 3)
  else 0

theorem q3_pairs_value_attempt (q : Q6) (i j : Fin 6) :
    (repsQ3.map (pairValue q i j)).sum = q3Value q i j := by
  fin_cases i <;> fin_cases j <;>
    norm_num [repsQ3, pairValue, body5RealRow, body5Index, rationalReal,
      rationalImag, RationalTag.toRat, tracePhase, body5Frequency,
      Fin.sum_univ_succ, q3Value, body5Phi, sub_eq_add_neg] <;> ring

theorem q3_off_support_attempt (q : Q6) (i j : Fin 6) (h : ¬q3Entry i j) :
    (repsQ3.map (pairValue q i j)).sum = 0 := by
  rw [q3_pairs_value_attempt]
  fin_cases i <;> fin_cases j <;> simp_all [q3Entry, q3Value]

/- A new COMPUTABLE filter on the original generated rows binds all sixteen
   actual q3 records. It does not compute the old classical representative
   filter and does not identify row/column transposes. -/
def sourceQ3Rows : List BodyTraceRow :=
  bodyTraceRows5.filter (fun r => decide (r.frequency 3 ≠ 0))

set_option maxRecDepth 4096 in
set_option maxHeartbeats 800000 in
theorem q3_source_codes_attempt :
    List.Perm (sourceQ3Rows.map rowCode) ((pairedRows repsQ3).map rowCode) := by
  decide

theorem q3_source_fold_attempt (q : Q6) (i j : Fin 6) (seed : ℝ) :
    body5Fold sourceQ3Rows q i j seed = seed + q3Value q i j := by
  have hp := perm_of_codes_attempt _ _ q3_source_codes_attempt
  rw [fold_perm_attempt _ _ hp]
  unfold body5Fold
  rw [fold_add_sum_attempt, pair_sum_attempt]
  simp only [contribution_pair_attempt]
  rw [q3_pairs_value_attempt]

theorem q3_source_off_support_attempt (q : Q6) (i j : Fin 6)
    (h : ¬q3Entry i j) (seed : ℝ) : body5Fold sourceQ3Rows q i j seed = seed := by
  rw [q3_source_fold_attempt, ← q3_pairs_value_attempt, q3_off_support_attempt q i j h, add_zero]

/- Finite rational normalization, after collapsing conjugate atoms.
   No DH, trig-addition expansion or full 727-row real fold is used here. -/
theorem canonical_to_piecewise_attempt (q : Q6) (i j : Fin 6) :
    canonicalValue q i j = body_5_piecewise q i j := by
  unfold canonicalValue
  rw [q3_pairs_value_attempt]
  fin_cases i <;> fin_cases j <;>
    norm_num [constants, reps17, pairValue, traceRowContribution,
      traceAtom, body5RealRow, imagRow, body5Index, rationalReal, rationalImag,
      RationalTag.toRat, tracePhase, body5Frequency, Fin.sum_univ_succ,
      q3Value, body5Phi, body_5_piecewise, sub_eq_add_neg] <;> ring

/- Compatibility with the original F4 target. These two old-filter bindings
   are explicit data premises, not supplied by this compatibility lemma.
   The direct canonical trace route above/below does not require them. -/
theorem old_paired_to_piecewise_conditional_attempt
    (hc : List.Perm body5ConstantRows constants)
    (hr : List.Perm body5RepresentativeRows reps) : Body5PairedToPiecewiseTarget := by
  intro q i j
  have hcs := (hc.map (traceRowContribution body5Index i j q)).sum_eq
  have hrs := (hr.map (pairValue q i j)).sum_eq
  have hv : body5PairedValue q i j = canonicalValue q i j := by
    unfold body5PairedValue
    simp only [contribution_pair_attempt]
    rw [hcs, hrs]
    simp [canonicalValue, reps, List.map_append, List.sum_append, add_assoc]
  exact hv.trans (canonical_to_piecewise_attempt q i j)

/- Transpose changes only entry tags; it is NOT frequency conjugation. -/
def transposeRow (r : BodyTraceRow) : BodyTraceRow := { r with row := r.col, col := r.row }

theorem transpose_contribution_attempt (q : Q6) (i j : Fin 6) (r : BodyTraceRow) :
    traceRowContribution body5Index i j q (transposeRow r) =
      traceRowContribution body5Index j i q r := by
  simp [traceRowContribution, transposeRow, traceAtom, and_comm, and_left_comm, and_assoc]

set_option maxRecDepth 4096 in
set_option maxHeartbeats 800000 in
theorem transpose_codes_attempt :
    List.Perm ((bodyTraceRows5.map transposeRow).map rowCode) (bodyTraceRows5.map rowCode) := by
  decide

theorem trace_transpose_attempt (q : Q6) (i j : Fin 6) (seed : ℝ) :
    body5Fold bodyTraceRows5 q i j seed = body5Fold bodyTraceRows5 q j i seed := by
  have hp := perm_of_codes_attempt _ _ transpose_codes_attempt
  rw [fold_perm_attempt _ _ hp.symm]
  unfold body5Fold
  rw [fold_add_sum_attempt, fold_add_sum_attempt]
  simp only [List.map_map, Function.comp_def, transpose_contribution_attempt]

theorem trace_piecewise_attempt : h_body_5_trace_fold_target := by
  intro q i j
  change body_5_piecewise q i j = body5Fold bodyTraceRows q i j 0
  rw [full_to_block_attempt, block_to_canonical_attempt, zero_add,
    canonical_to_piecewise_attempt]

/- Final composition retains the only geometric premises. The trace branch
   has its own literal-data binding attempts above. All remain UNCOMPILED. -/
theorem source_trace_conditional_attempt
    (hcols : Body5ColumnsTarget) (hiso : Body5LiftIsometryTarget) : h_body_5 := by
  exact h_body_5_of_entry_targets
    (source_piecewise_conditional_attempt hcols hiso) trace_piecewise_attempt

end
end NEW_BODY5_FiniteTraceSkeleton20260907

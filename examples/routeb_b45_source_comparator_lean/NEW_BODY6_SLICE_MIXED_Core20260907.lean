import NEW_BODY6_SLICE_LEVER_Core20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_MIXED_Core20260907

noncomputable section

open NEW_BODY6_SLICE_AXIS_Core20260907 NEW_BODY6_SLICE_VGRAM_Core20260907
open NEW_BODY6_SLICE_LEVER_Core20260907

/- UNCOMPILED pure finite 3x2 mixed block. No source/DH/Fourier imports. -/
def tailJoint (t : Fin 2) : Fin 6 := ⟨t.val + 3, by omega⟩
def tailAxis (q : LQ) (t : Fin 2) : AVec :=
  localAxis (angleSum q) (q 3) (q 4) (tailJoint t)
def lastAxis (q : LQ) : AVec := localAxis (angleSum q) (q 3) (q 4) 5
def frontColumn (q : LQ) (h : ℝ) (i : Fin 3) : AVec :=
  fun a => baseLocal q i a + h * crossV (firstAxis i) (lastAxis q) a
def tailColumn (q : LQ) (h : ℝ) (t : Fin 2) : AVec :=
  fun a => h * crossV (tailAxis q t) (lastAxis q) a

def axisEntry (q : LQ) (i : Fin 3) (t : Fin 2) : ℝ :=
  (![![Real.cos (angleSum q), Real.sin (angleSum q) * Real.sin (q 3)],
     ![0, Real.cos (q 3)], ![0, Real.cos (q 3)]] : Fin 3 → Fin 2 → ℝ) i t

def frontLastDot (q : LQ) (i : Fin 3) : ℝ :=
  (![Real.cos (angleSum q) * Real.cos (q 4) -
       Real.sin (angleSum q) * Real.cos (q 3) * Real.sin (q 4),
     Real.sin (q 3) * Real.sin (q 4), Real.sin (q 3) * Real.sin (q 4)] : Fin 3 → ℝ) i

def tailLastDot (q : LQ) (t : Fin 2) : ℝ := (![Real.cos (q 4), 0] : Fin 2 → ℝ) t
def projAlong (q : LQ) : ℝ := height q * Real.cos (angleSum q) + reach q * Real.sin (angleSum q)
def projAcross (q : LQ) : ℝ := reach q * Real.cos (angleSum q) - height q * Real.sin (angleSum q)

/- B_i dot (T_t cross S). Full six scalar entries, no Fourier reification. -/
def tripleEntry (q : LQ) (i : Fin 3) (t : Fin 2) : ℝ :=
  (![![Real.sin (q 4) * (radial q * Real.cos (q 3) +
          Real.cos (angleSum q) * Real.sin (q 3) / 20),
        Real.cos (q 4) * (radial q * Real.sin (q 3) -
          Real.cos (angleSum q) * Real.cos (q 3) / 20) +
          Real.sin (angleSum q) * Real.sin (q 4) / 20],
     ![-projAlong q * Real.sin (q 3) * Real.sin (q 4),
        projAlong q * Real.cos (q 3) * Real.cos (q 4) + projAcross q * Real.sin (q 4)],
     ![-(19 / 100) * Real.sin (q 3) * Real.sin (q 4),
        (19 / 100) * Real.cos (q 3) * Real.cos (q 4)]] : Fin 3 → Fin 2 → ℝ) i t

def velocityEntry (q : LQ) (h : ℝ) (i : Fin 3) (t : Fin 2) : ℝ :=
  h * tripleEntry q i t + h ^ 2 *
    (axisEntry q i t - frontLastDot q i * tailLastDot q t)

theorem mixed_cross_identity_attempt (B W T S : AVec) (h : ℝ)
    (hs : dot3 S S = 1) :
    dot3 (fun a => B a + h * crossV W S a) (fun a => h * crossV T S a) =
      h * dot3 B (crossV T S) + h ^ 2 * (dot3 W T - dot3 W S * dot3 T S) := by
  have hd : dot3 (fun a => B a + h * crossV W S a) (fun a => h * crossV T S a) =
      h * dot3 B (crossV T S) + h ^ 2 * dot3 (crossV W S) (crossV T S) := by
    norm_num [dot3, Fin.sum_univ_succ] <;> ring
  rw [hd, cross_gram_attempt, dot_swap_attempt S T, hs]
  ring

theorem axis_entries_attempt (q : LQ) (i : Fin 3) (t : Fin 2) :
    dot3 (firstAxis i) (tailAxis q t) = axisEntry q i t := by
  fin_cases i <;> fin_cases t <;>
    norm_num [dot3, firstAxis, tailAxis, tailJoint, localAxis, pitchLift,
      axisEntry, Fin.sum_univ_succ] <;> ring

theorem front_last_dot_attempt (q : LQ) (i : Fin 3) :
    dot3 (firstAxis i) (lastAxis q) = frontLastDot q i := by
  fin_cases i <;>
    norm_num [dot3, firstAxis, lastAxis, localAxis, pitchLift, frontLastDot,
      Fin.sum_univ_succ] <;> ring

theorem tail_last_dot_attempt (q : LQ) (t : Fin 2) :
    dot3 (tailAxis q t) (lastAxis q) = tailLastDot q t := by
  fin_cases t
  · exact local_dot_three_five_attempt (angleSum q) (q 3) (q 4)
  · exact local_dot_four_five_attempt (angleSum q) (q 3) (q 4)

theorem last_unit_attempt (q : LQ) : dot3 (lastAxis q) (lastAxis q) = 1 :=
  local_dot_five_five_attempt (angleSum q) (q 3) (q 4)

theorem pitch_cross_attempt (x : ℝ) (u v : AVec) :
    crossV (pitchLift x u) (pitchLift x v) = pitchLift x (crossV u v) := by
  have hx := Real.sin_sq_add_cos_sq x
  funext a
  fin_cases a <;> simp [pitchLift, crossV] <;>
    first | ring | linear_combination (u 2 * v 0 - u 0 * v 2) * hx

def tailCross (q : LQ) (t : Fin 2) : AVec :=
  pitchLift (angleSum q)
    (if t = 0 then ![-Real.sin (q 3) * Real.sin (q 4), Real.cos (q 3) * Real.sin (q 4), 0]
     else ![Real.cos (q 3) * Real.cos (q 4), Real.sin (q 3) * Real.cos (q 4), -Real.sin (q 4)])

theorem tail_cross_attempt (q : LQ) (t : Fin 2) :
    crossV (tailAxis q t) (lastAxis q) = tailCross q t := by
  fin_cases t
  · change crossV (pitchLift (angleSum q) ![0, 0, 1])
      (pitchLift (angleSum q) ![Real.cos (q 3) * Real.sin (q 4),
        Real.sin (q 3) * Real.sin (q 4), Real.cos (q 4)]) = _
    rw [pitch_cross_attempt]
    apply congrArg (pitchLift (angleSum q))
    funext a
    fin_cases a <;> norm_num [crossV, tailCross]
  · change crossV (pitchLift (angleSum q) ![-Real.sin (q 3), Real.cos (q 3), 0])
      (pitchLift (angleSum q) ![Real.cos (q 3) * Real.sin (q 4),
        Real.sin (q 3) * Real.sin (q 4), Real.cos (q 4)]) = _
    rw [pitch_cross_attempt]
    apply congrArg (pitchLift (angleSum q))
    have hy := Real.sin_sq_add_cos_sq (q 3)
    funext a
    fin_cases a <;> norm_num [crossV, tailCross] <;>
      first | ring | linear_combination (-Real.sin (q 4)) * hy

theorem triple_entries_attempt (q : LQ) (i : Fin 3) (t : Fin 2) :
    dot3 (baseLocal q i) (crossV (tailAxis q t) (lastAxis q)) = tripleEntry q i t := by
  rw [tail_cross_attempt]
  have hx := Real.sin_sq_add_cos_sq (angleSum q)
  fin_cases i <;> fin_cases t <;>
    norm_num [dot3, baseLocal, tailCross, pitchLift, tripleEntry,
      projAlong, projAcross, Fin.sum_univ_succ] <;>
    first
    | ring
    | linear_combination (-(19 / 100 : ℝ) * Real.sin (q 3) * Real.sin (q 4)) * hx
    | linear_combination ((19 / 100 : ℝ) * Real.cos (q 3) * Real.cos (q 4)) * hx

theorem mixed_velocity_entries_attempt (q : LQ) (h : ℝ) (i : Fin 3) (t : Fin 2) :
    dot3 (frontColumn q h i) (tailColumn q h t) = velocityEntry q h i t := by
  unfold frontColumn tailColumn
  rw [mixed_cross_identity_attempt _ _ _ _ _ (last_unit_attempt q),
    triple_entries_attempt, axis_entries_attempt, front_last_dot_attempt, tail_last_dot_attempt]
  rfl

end
end NEW_BODY6_SLICE_MIXED_Core20260907

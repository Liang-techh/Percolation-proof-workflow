import NEW_BODY6_SLICE_VGRAM_Core20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_LEVER_Core20260907

noncomputable section

open NEW_BODY6_SLICE_AXIS_Core20260907 NEW_BODY6_SLICE_VGRAM_Core20260907

/- UNCOMPILED source-independent local vectors. No DH source or Fourier import. -/
abbrev LQ := Fin 6 → ℝ
def angleSum (q : LQ) : ℝ := q 1 + q 2
def reach (q : LQ) : ℝ := (21 / 100) * Real.sin (q 1) + (19 / 100) * Real.sin (angleSum q)
def height (q : LQ) : ℝ := (21 / 100) * Real.cos (q 1) + (19 / 100) * Real.cos (angleSum q)
def radial (q : LQ) : ℝ := 2 / 25 + reach q

def originLocal (q : LQ) (k : Fin 4) : AVec :=
  match k.val with
  | 0 => ![0, 0, 0]
  | 1 => ![2 / 25, 0, 1 / 10]
  | 2 => ![2 / 25 + (21 / 100) * Real.sin (q 1), 0,
             1 / 10 + (21 / 100) * Real.cos (q 1)]
  | 3 => ![2 / 25 + (21 / 100) * Real.sin (q 1), 1 / 20,
             1 / 10 + (21 / 100) * Real.cos (q 1)]
  | _ => 0

def endLocal (q : LQ) : AVec := ![radial q, 1 / 20, 1 / 10 + height q]
def parentLocalSlot (i : Fin 3) : Fin 4 := ⟨i.val, by omega⟩
def firstAxis (i : Fin 3) : AVec := if i = 0 then ![0, 0, 1] else ![0, 1, 0]

def baseLocal (q : LQ) (i : Fin 3) : AVec :=
  match i.val with
  | 0 => ![-1 / 20, radial q, 0]
  | 1 => ![height q, 0, -reach q]
  | 2 => ![(19 / 100) * Real.cos (angleSum q), 0,
             -(19 / 100) * Real.sin (angleSum q)]
  | _ => 0

theorem yaw_sub_attempt (t : ℝ) (u v : AVec) :
    (fun a => yawLift t u a - yawLift t v a) = yawLift t (fun a => u a - v a) := by
  funext a
  fin_cases a <;> simp [yawLift] <;> ring

theorem yaw_affine_attempt (t h : ℝ) (u v : AVec) :
    (fun a => yawLift t u a + h * yawLift t v a) =
      yawLift t (fun a => u a + h * v a) := by
  funext a
  fin_cases a <;> simp [yawLift] <;> ring

/- Cross covariance uses orientation as well as metric preservation. -/
theorem yaw_cross_attempt (t : ℝ) (u v : AVec) :
    crossV (yawLift t u) (yawLift t v) = yawLift t (crossV u v) := by
  have ht := Real.sin_sq_add_cos_sq t
  funext a
  fin_cases a <;> simp [yawLift, crossV] <;>
    first | ring | linear_combination (u 0 * v 1 - u 1 * v 0) * ht

theorem end_from_slot3_attempt (q : LQ) :
    (fun a => originLocal q 3 a + (19 / 100 : ℝ) *
      pitchLift (angleSum q) ![0, 0, 1] a) = endLocal q := by
  funext a
  fin_cases a <;> norm_num [originLocal, endLocal, radial, reach, height, pitchLift] <;> ring

theorem local_lever_cross_attempt (q : LQ) (i : Fin 3) :
    crossV (firstAxis i) (fun a => endLocal q a - originLocal q (parentLocalSlot i) a) =
      baseLocal q i := by
  fin_cases i <;> funext a <;> fin_cases a <;>
    norm_num [firstAxis, endLocal, originLocal, parentLocalSlot, baseLocal,
      radial, reach, height, crossV] <;> ring

theorem base0_nonzero_attempt (q : LQ) : baseLocal q (0 : Fin 3) ≠ 0 := by
  intro h
  have h0 := congrFun h (0 : Fin 3)
  norm_num [baseLocal] at h0

theorem base2_norm_attempt (q : LQ) :
    dot3 (baseLocal q (2 : Fin 3)) (baseLocal q (2 : Fin 3)) = (361 / 10000 : ℝ) := by
  have hx := Real.sin_sq_add_cos_sq (angleSum q)
  norm_num [dot3, baseLocal, Fin.sum_univ_succ]
  linear_combination (361 / 10000 : ℝ) * hx

end
end NEW_BODY6_SLICE_LEVER_Core20260907

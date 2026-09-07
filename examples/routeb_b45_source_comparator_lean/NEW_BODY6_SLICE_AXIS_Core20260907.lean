import Mathlib

set_option autoImplicit false

namespace NEW_BODY6_SLICE_AXIS_Core20260907

noncomputable section

/- Pure rotation algebra, UNCOMPILED. No source, Fourier rows or receipt imports. -/
abbrev AVec := Fin 3 → ℝ

def dot3 (u v : AVec) : ℝ := ∑ a : Fin 3, u a * v a

def yawLift (t : ℝ) (u : AVec) : AVec :=
  ![u 0 * Real.cos t - u 1 * Real.sin t,
    u 0 * Real.sin t + u 1 * Real.cos t, u 2]

def pitchLift (x : ℝ) (u : AVec) : AVec :=
  ![Real.cos x * u 0 + Real.sin x * u 2,
    u 1, -Real.sin x * u 0 + Real.cos x * u 2]

theorem yaw_isometry_attempt (t : ℝ) (u v : AVec) :
    dot3 (yawLift t u) (yawLift t v) = dot3 u v := by
  have ht := Real.sin_sq_add_cos_sq t
  norm_num [dot3, yawLift, Fin.sum_univ_succ]
  linear_combination (u 0 * v 0 + u 1 * v 1) * ht

theorem pitch_isometry_attempt (x : ℝ) (u v : AVec) :
    dot3 (pitchLift x u) (pitchLift x v) = dot3 u v := by
  have hx := Real.sin_sq_add_cos_sq x
  norm_num [dot3, pitchLift, Fin.sum_univ_succ]
  linear_combination (u 0 * v 0 + u 2 * v 2) * hx

/- x=q2+q3, y=q4, z=q5 in human angle notation. Parent axes are indexed 0..5.
   The fifth parent axis is obtained before applying the sixth DH step. -/
def localAxis (x y z : ℝ) (i : Fin 6) : AVec :=
  match i.val with
  | 0 => ![0, 0, 1]
  | 1 => pitchLift x ![0, 1, 0]
  | 2 => pitchLift x ![0, 1, 0]
  | 3 => pitchLift x ![0, 0, 1]
  | 4 => pitchLift x ![-Real.sin y, Real.cos y, 0]
  | 5 => pitchLift x ![Real.cos y * Real.sin z, Real.sin y * Real.sin z, Real.cos z]
  | _ => 0

def dotResult (x y z : ℝ) : Fin 6 → ℝ :=
  ![Real.cos x * Real.cos z - Real.sin x * Real.cos y * Real.sin z,
    Real.sin y * Real.sin z, Real.sin y * Real.sin z,
    Real.cos z, 0, 1]

theorem local_dot_zero_five_attempt (x y z : ℝ) :
    dot3 (localAxis x y z 0) (localAxis x y z 5) = dotResult x y z 0 := by
  norm_num [dot3, localAxis, pitchLift, dotResult, Fin.sum_univ_succ] <;> ring

theorem local_dot_one_five_attempt (x y z : ℝ) :
    dot3 (localAxis x y z 1) (localAxis x y z 5) = dotResult x y z 1 := by
  change dot3 (pitchLift x ![0, 1, 0])
    (pitchLift x ![Real.cos y * Real.sin z, Real.sin y * Real.sin z, Real.cos z]) = _
  rw [pitch_isometry_attempt]
  norm_num [dot3, dotResult, Fin.sum_univ_succ]

theorem local_dot_two_five_attempt (x y z : ℝ) :
    dot3 (localAxis x y z 2) (localAxis x y z 5) = dotResult x y z 2 := by
  exact local_dot_one_five_attempt x y z

theorem local_dot_three_five_attempt (x y z : ℝ) :
    dot3 (localAxis x y z 3) (localAxis x y z 5) = dotResult x y z 3 := by
  change dot3 (pitchLift x ![0, 0, 1])
    (pitchLift x ![Real.cos y * Real.sin z, Real.sin y * Real.sin z, Real.cos z]) = _
  rw [pitch_isometry_attempt]
  norm_num [dot3, dotResult, Fin.sum_univ_succ]

theorem local_dot_four_five_attempt (x y z : ℝ) :
    dot3 (localAxis x y z 4) (localAxis x y z 5) = dotResult x y z 4 := by
  change dot3 (pitchLift x ![-Real.sin y, Real.cos y, 0])
    (pitchLift x ![Real.cos y * Real.sin z, Real.sin y * Real.sin z, Real.cos z]) = _
  rw [pitch_isometry_attempt]
  norm_num [dot3, dotResult, Fin.sum_univ_succ] <;> ring

theorem local_dot_five_five_attempt (x y z : ℝ) :
    dot3 (localAxis x y z 5) (localAxis x y z 5) = dotResult x y z 5 := by
  change dot3
    (pitchLift x ![Real.cos y * Real.sin z, Real.sin y * Real.sin z, Real.cos z])
    (pitchLift x ![Real.cos y * Real.sin z, Real.sin y * Real.sin z, Real.cos z]) = _
  rw [pitch_isometry_attempt]
  have hy := Real.sin_sq_add_cos_sq y
  have hz := Real.sin_sq_add_cos_sq z
  norm_num [dot3, dotResult, Fin.sum_univ_succ]
  linear_combination (Real.sin z ^ 2) * hy + hz

theorem local_dot_all_attempt (x y z : ℝ) (i : Fin 6) :
    dot3 (localAxis x y z i) (localAxis x y z 5) = dotResult x y z i := by
  fin_cases i
  · exact local_dot_zero_five_attempt x y z
  · exact local_dot_one_five_attempt x y z
  · exact local_dot_two_five_attempt x y z
  · exact local_dot_three_five_attempt x y z
  · exact local_dot_four_five_attempt x y z
  · exact local_dot_five_five_attempt x y z

end
end NEW_BODY6_SLICE_AXIS_Core20260907

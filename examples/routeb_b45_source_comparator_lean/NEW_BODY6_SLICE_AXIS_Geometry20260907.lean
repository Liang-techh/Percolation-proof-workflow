import NEW_BODY6_SLICE_AXIS_Core20260907
import FrameSlotHomogeneousPrefixV2
import SourceContractAdapter

set_option autoImplicit false

namespace NEW_BODY6_SLICE_AXIS_Geometry20260907

noncomputable section

open NEW_BODY6_SLICE_AXIS_Core20260907
open RouteBConcreteStepHomogeneous RouteBHomogeneousPrefixProjection
open RouteBRotationPrefixOrthogonality RouteBFrameSlotAccessor
open RouteBFrameSlotHomogeneousPrefixV2 RouteBRealDHStep
open RouteBSourceContractAdapter RouteBBodySemanticCore RouteBB45Fourier

/- UNCOMPILED real-source geometry. No Fourier slice/evaluator is imported.
   Axis i : Fin 6 uses slot prevOrigin i : Fin 7, NOT nextOrigin i.
   Rotation columns and their scalar coordinates both use Fin 3. -/
abbrev AQ := Fin 6 → ℝ
abbrev ARot := Matrix (Fin 3) (Fin 3) ℝ

def column (R : ARot) (k : Fin 3) : AVec := fun a => R a k

def rotationAt (q : AQ) (slot : Fin 7) : ARot :=
  rotationPrefix (fun k => stepRotation k (q k)) slot

def phi (q : AQ) : ℝ := q 1 + q 2

theorem rotation_projection_attempt (q : AQ) (s : Fin 7) :
    RouteBHomogeneousRotationProjection.rotationBlock (routeBFrameSlot q s) =
      rotationAt q s := by
  rw [routeBFrameSlot_eq_routeBHomogeneousPrefix]
  exact homogeneousPrefix_rotationBlock_eq _ _ _

theorem source_axis_rotation_column_attempt (q : AQ) (i : Fin 6) :
    (sourceContract q).axes i = column (rotationAt q (prevOrigin i)) (2 : Fin 3) := by
  have hs := congrFun (source_axis_function_eq_frame_contract q) i
  change (sourceContract q).axes i =
    RouteBFrameOriginAxis.zAxis (routeBFrameSlot q (prevOrigin i)) at hs
  rw [hs]
  funext a
  have h := congrFun (congrFun (rotation_projection_attempt q (prevOrigin i)) a)
    (2 : Fin 3)
  exact h

theorem rotation_slot4_attempt (q : AQ) :
    rotationAt q (4 : Fin 7) = rotationAt q (3 : Fin 7) * stepRotation 3 (q 3) := by
  rfl

theorem rotation_slot5_attempt (q : AQ) :
    rotationAt q (5 : Fin 7) = rotationAt q (4 : Fin 7) * stepRotation 4 (q 4) := by
  rfl

/- Each leaf expands a SINGLE 3x3 multiplication, with the prefix R abstract. -/
macro "axis_single_step" : tactic =>
  `(tactic|
    (funext a; fin_cases a <;>
      norm_num [column, stepRotation, RouteBHomogeneousRotationProjection.embed3,
        routeBRealStepMatrix, realDHStep, routeBRealCos, routeBRealSin,
        routeBCosAlpha, routeBSinAlpha, routeBA, routeBD,
        Matrix.mul_apply, Fin.sum_univ_succ] <;> ring))

theorem step3_column0_attempt (R : ARot) (t : ℝ) :
    column (R * stepRotation 3 t) 0 =
      (fun a => Real.cos t * column R 0 a + Real.sin t * column R 1 a) := by
  axis_single_step

theorem step3_column1_attempt (R : ARot) (t : ℝ) :
    column (R * stepRotation 3 t) 1 = (fun a => -column R 2 a) := by
  axis_single_step

theorem step3_column2_attempt (R : ARot) (t : ℝ) :
    column (R * stepRotation 3 t) 2 =
      (fun a => -Real.sin t * column R 0 a + Real.cos t * column R 1 a) := by
  axis_single_step

theorem step4_column2_attempt (R : ARot) (t : ℝ) :
    column (R * stepRotation 4 t) 2 =
      (fun a => Real.sin t * column R 0 a - Real.cos t * column R 1 a) := by
  axis_single_step

/- Bounded prefix 0..3 only. The q2 offset -pi/2 and q3 offset +pi/2
   are read from routeBRealCos/Sin, not guessed from an unshifted Rz chain. -/
macro "axis_prefix_scalar" : tactic =>
  `(tactic|
    (norm_num [rotationAt, rotationPrefix, prefixAt, stepRotation,
      RouteBHomogeneousRotationProjection.embed3,
      routeBRealStepMatrix, realDHStep, routeBRealCos, routeBRealSin,
      routeBCosAlpha, routeBSinAlpha, routeBA, routeBD,
      column, prevOrigin, Matrix.mul_apply, Matrix.one_apply, Fin.sum_univ_succ,
      yawLift, pitchLift, localAxis, phi, Real.sin_add, Real.cos_add] <;> ring))

theorem prefix3_column0_attempt (q : AQ) :
    column (rotationAt q 3) 0 = yawLift (q 0) (pitchLift (phi q) ![1, 0, 0]) := by
  funext a
  fin_cases a <;> axis_prefix_scalar

theorem prefix3_column1_attempt (q : AQ) :
    column (rotationAt q 3) 1 = yawLift (q 0) (pitchLift (phi q) ![0, 1, 0]) := by
  funext a
  fin_cases a <;> axis_prefix_scalar

theorem prefix3_column2_attempt (q : AQ) :
    column (rotationAt q 3) 2 = yawLift (q 0) (pitchLift (phi q) ![0, 0, 1]) := by
  funext a
  fin_cases a <;> axis_prefix_scalar

theorem rotation_axis_local_attempt (q : AQ) (i : Fin 6) :
    column (rotationAt q (prevOrigin i)) 2 =
      yawLift (q 0) (localAxis (phi q) (q 3) (q 4) i) := by
  fin_cases i
  · funext a
    fin_cases a <;> axis_prefix_scalar
  · funext a
    fin_cases a <;> axis_prefix_scalar
  · funext a
    fin_cases a <;> axis_prefix_scalar
  · exact prefix3_column2_attempt q
  · change column (rotationAt q 4) 2 = _
    rw [rotation_slot4_attempt, step3_column2_attempt,
      prefix3_column0_attempt, prefix3_column1_attempt]
    funext a
    fin_cases a <;> norm_num [yawLift, pitchLift, localAxis] <;> ring
  · change column (rotationAt q 5) 2 = _
    rw [rotation_slot5_attempt, step4_column2_attempt]
    simp_rw [rotation_slot4_attempt]
    rw [step3_column0_attempt, step3_column1_attempt,
      prefix3_column0_attempt, prefix3_column1_attempt, prefix3_column2_attempt]
    funext a
    fin_cases a <;> norm_num [yawLift, pitchLift, localAxis] <;> ring

theorem source_axis_local_attempt (q : AQ) (i : Fin 6) :
    (sourceContract q).axes i =
      yawLift (q 0) (localAxis (phi q) (q 3) (q 4) i) := by
  rw [source_axis_rotation_column_attempt]
  exact rotation_axis_local_attempt q i

theorem source_dot_all_attempt (q : AQ) (i : Fin 6) :
    (∑ a : Fin 3, (sourceContract q).axes i a *
      (sourceContract q).axes (5 : Fin 6) a) =
      dotResult (phi q) (q 3) (q 4) i := by
  change dot3 ((sourceContract q).axes i) ((sourceContract q).axes 5) = _
  rw [source_axis_local_attempt q i, source_axis_local_attempt q 5,
    yaw_isometry_attempt]
  exact local_dot_all_attempt (phi q) (q 3) (q 4) i

/- Six explicit source seams. These are all-q statements, not samples or cell bounds. -/
theorem source_dot_0_5_attempt (q : AQ) :
    (∑ a : Fin 3, (sourceContract q).axes 0 a * (sourceContract q).axes 5 a) =
      Real.cos (q 1 + q 2) * Real.cos (q 4) -
        Real.sin (q 1 + q 2) * Real.cos (q 3) * Real.sin (q 4) := by
  simpa [dotResult, phi] using source_dot_all_attempt q 0

theorem source_dot_1_5_attempt (q : AQ) :
    (∑ a : Fin 3, (sourceContract q).axes 1 a * (sourceContract q).axes 5 a) =
      Real.sin (q 3) * Real.sin (q 4) := by
  simpa [dotResult] using source_dot_all_attempt q 1

theorem source_dot_2_5_attempt (q : AQ) :
    (∑ a : Fin 3, (sourceContract q).axes 2 a * (sourceContract q).axes 5 a) =
      Real.sin (q 3) * Real.sin (q 4) := by
  simpa [dotResult] using source_dot_all_attempt q 2

theorem source_dot_3_5_attempt (q : AQ) :
    (∑ a : Fin 3, (sourceContract q).axes 3 a * (sourceContract q).axes 5 a) =
      Real.cos (q 4) := by
  simpa [dotResult] using source_dot_all_attempt q 3

theorem source_dot_4_5_attempt (q : AQ) :
    (∑ a : Fin 3, (sourceContract q).axes 4 a * (sourceContract q).axes 5 a) = 0 := by
  simpa [dotResult] using source_dot_all_attempt q 4

theorem source_dot_5_5_attempt (q : AQ) :
    (∑ a : Fin 3, (sourceContract q).axes 5 a * (sourceContract q).axes 5 a) = 1 := by
  simpa [dotResult] using source_dot_all_attempt q 5

end
end NEW_BODY6_SLICE_AXIS_Geometry20260907

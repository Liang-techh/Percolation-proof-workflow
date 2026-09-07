import NEW_BODY6_SLICE_LEVER_Core20260907
import NEW_BODY6_SLICE_VGRAM_Source20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_LEVER_Source20260907

noncomputable section

open NEW_BODY6_SLICE_AXIS_Core20260907 NEW_BODY6_SLICE_AXIS_Geometry20260907
open NEW_BODY6_SLICE_VGRAM_Core20260907 NEW_BODY6_SLICE_VGRAM_Source20260907
open NEW_BODY6_SLICE_LEVER_Core20260907
open RouteBO1PerBodyExactSource RouteBBodySemanticCore RouteBSourceContractAdapter
open RouteBFrameOriginAxis RouteBFrameSlotAccessor RouteBRealDHStep RouteBB45Fourier

/- UNCOMPILED true-source seam for b0,b1,b2 only. No tail/Fourier recomputation.
   Source origins/axes are retained; v remains b + h (z cross z5). -/
def firstJoint (i : Fin 3) : Fin 6 := ⟨i.val, by omega⟩
def localOriginSlot (k : Fin 4) : Fin 7 := ⟨k.val, by omega⟩

theorem first_parent_slot_attempt (i : Fin 3) :
    prevOrigin (firstJoint i) = localOriginSlot (parentLocalSlot i) := by
  rfl

/- Only slots 0..3 are expanded. o5 is supplied through the existing source
   terminal_origin3_attempt; neither slots 4/5 nor velocity tail are rederived. -/
macro "lever_origin_scalar" : tactic =>
  `(tactic|
    (norm_num [routeBFrameSlot, prefixFrame, routeBStepFunction,
      routeBRealStepMatrix, realDHStep, routeBRealCos, routeBRealSin,
      routeBCosAlpha, routeBSinAlpha, routeBA, routeBD,
      origin, RouteBFrameOriginAxis.embed3, Matrix.mul_apply, Matrix.one_apply,
      Fin.sum_univ_succ, localOriginSlot, originLocal, yawLift] <;> ring))

theorem prefix_origin_local_attempt (q : Q6) (k : Fin 4) :
    origin (routeBFrameSlot q (localOriginSlot k)) = yawLift (q 0) (originLocal q k) := by
  fin_cases k <;> funext a <;> fin_cases a <;> lever_origin_scalar

theorem source_origin_local_attempt (q : Q6) (k : Fin 4) :
    (sourceContract q).origins (localOriginSlot k) = yawLift (q 0) (originLocal q k) := by
  rw [source_origin_slot_attempt]
  exact prefix_origin_local_attempt q k

theorem source_first_parent_local_attempt (q : Q6) (i : Fin 3) :
    parentO q (firstJoint i) = yawLift (q 0) (originLocal q (parentLocalSlot i)) := by
  unfold parentO
  rw [first_parent_slot_attempt]
  exact source_origin_local_attempt q (parentLocalSlot i)

theorem source_end_local_attempt (q : Q6) : terminalO q = yawLift (q 0) (endLocal q) := by
  have hp : parentO q (3 : Fin 6) = yawLift (q 0) (originLocal q 3) :=
    source_origin_local_attempt q 3
  have hz : sourceZ q (3 : Fin 6) = yawLift (q 0) (pitchLift (angleSum q) ![0, 0, 1]) := by
    exact source_axis_local_attempt q 3
  have he : terminalO q = fun a => parentO q 3 a + (19 / 100 : ℝ) * sourceZ q 3 a := by
    funext a
    exact terminal_origin3_attempt q a
  rw [he, hp, hz, yaw_affine_attempt, end_from_slot3_attempt]

theorem source_first_axis_local_attempt (q : Q6) (i : Fin 3) :
    sourceZ q (firstJoint i) = yawLift (q 0) (firstAxis i) := by
  change (sourceContract q).axes (firstJoint i) = _
  rw [source_axis_local_attempt]
  fin_cases i <;> funext a <;> fin_cases a <;>
    norm_num [firstJoint, firstAxis, localAxis, pitchLift, yawLift]

theorem source_first_base_local_attempt (q : Q6) (i : Fin 3) :
    baseV q (firstJoint i) = yawLift (q 0) (baseLocal q i) := by
  unfold baseV
  rw [source_first_axis_local_attempt, source_end_local_attempt,
    source_first_parent_local_attempt, yaw_sub_attempt, yaw_cross_attempt,
    local_lever_cross_attempt]

/- Inhabit the earlier interface with concrete local vectors, not baseV itself. -/
theorem first_three_lever_target_attempt :
    FirstThreeLeverTarget (fun q i => yawLift (q 0) (baseLocal q i)) := by
  intro q i
  exact source_first_base_local_attempt q i

theorem source_base0_norm_attempt (q : Q6) :
    dot3 (baseV q (0 : Fin 6)) (baseV q (0 : Fin 6)) =
      (1 / 400 : ℝ) + radial q ^ 2 := by
  have hv := source_first_base_local_attempt q (0 : Fin 3)
  change baseV q (0 : Fin 6) = _ at hv
  simp_rw [hv]
  rw [yaw_isometry_attempt]
  norm_num [dot3, baseLocal, Fin.sum_univ_succ] <;> ring

theorem source_base0_nonzero_attempt (q : Q6) : baseV q (0 : Fin 6) ≠ 0 := by
  intro hz
  have hn := source_base0_norm_attempt q
  rw [hz] at hn
  norm_num [dot3] at hn
  nlinarith [sq_nonneg (radial q)]

theorem source_first_base_gram_attempt (q : Q6) (i j : Fin 3) :
    dot3 (baseV q (firstJoint i)) (baseV q (firstJoint j)) =
      dot3 (baseLocal q i) (baseLocal q j) := by
  rw [source_first_base_local_attempt q i, source_first_base_local_attempt q j]
  exact yaw_isometry_attempt _ _ _

def velocityLocal (q : Q6) (i : Fin 3) : AVec :=
  fun a => baseLocal q i a + offset *
    crossV (firstAxis i) (localAxis (angleSum q) (q 3) (q 4) 5) a

theorem source_first_velocity_local_attempt (hc : CenterOffsetTarget) (q : Q6) (i : Fin 3) :
    sourceV q (firstJoint i) = yawLift (q 0) (velocityLocal q i) := by
  have hz5 : sourceZ q (5 : Fin 6) =
      yawLift (q 0) (localAxis (angleSum q) (q 3) (q 4) 5) :=
    source_axis_local_attempt q 5
  rw [source_velocity_decomposition_attempt hc, source_first_base_local_attempt,
    source_first_axis_local_attempt, hz5, yaw_cross_attempt, yaw_affine_attempt]
  rfl

theorem source_first_velocity_gram_attempt (hc : CenterOffsetTarget) (q : Q6) (i j : Fin 3) :
    dot3 (sourceV q (firstJoint i)) (sourceV q (firstJoint j)) =
      dot3 (velocityLocal q i) (velocityLocal q j) := by
  rw [source_first_velocity_local_attempt hc q i, source_first_velocity_local_attempt hc q j]
  exact yaw_isometry_attempt _ _ _

/- No mass/Fourier/coverage/registry witness. CenterOffsetTarget remains explicit
   for full v columns; the b_i source identities need no center premise. -/

end
end NEW_BODY6_SLICE_LEVER_Source20260907

import NEW_BODY6_SLICE_MIXED_Core20260907
import NEW_BODY6_SLICE_LEVER_Source20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_MIXED_Source20260907

noncomputable section

open NEW_BODY6_SLICE_AXIS_Core20260907 NEW_BODY6_SLICE_AXIS_Geometry20260907
open NEW_BODY6_SLICE_VGRAM_Core20260907 NEW_BODY6_SLICE_VGRAM_Source20260907
open NEW_BODY6_SLICE_LEVER_Core20260907 NEW_BODY6_SLICE_LEVER_Source20260907
open NEW_BODY6_SLICE_MIXED_Core20260907 RouteBO1PerBodyExactSource

/- UNCOMPILED source attachment. Fin 3 rows are source indices 0..2;
   Fin 2 tail columns map to source indices 3,4. CenterOffsetTarget is never
   discharged here. No origins, tail norms or Fourier folds are recomputed. -/

theorem tail_joint_value_attempt (t : Fin 2) : (tailJoint t).val = t.val + 3 := rfl

theorem source_tail_axis_local_attempt (q : Q6) (t : Fin 2) :
    sourceZ q (tailJoint t) = yawLift (q 0) (tailAxis q t) :=
  source_axis_local_attempt q (tailJoint t)

theorem source_tail_velocity_local_attempt (hc : CenterOffsetTarget) (q : Q6) (t : Fin 2) :
    sourceV q (tailJoint t) = yawLift (q 0) (tailColumn q offset t) := by
  have hv : sourceV q (tailJoint t) =
      fun a => offset * crossV (sourceZ q (tailJoint t)) (sourceZ q 5) a := by
    fin_cases t
    · exact source_velocity3_attempt hc q
    · exact source_velocity4_attempt hc q
  have hs : sourceZ q (5 : Fin 6) = yawLift (q 0) (lastAxis q) :=
    source_axis_local_attempt q 5
  rw [hv, source_tail_axis_local_attempt, hs, yaw_cross_attempt]
  funext a
  fin_cases a <;> simp [tailColumn, yawLift] <;> ring

theorem source_front_column_local_attempt (hc : CenterOffsetTarget) (q : Q6) (i : Fin 3) :
    sourceV q (firstJoint i) = yawLift (q 0) (frontColumn q offset i) :=
  source_first_velocity_local_attempt hc q i

def MixedAxisTarget : Prop :=
  ∀ q (i : Fin 3) (t : Fin 2),
    dot3 (sourceZ q (firstJoint i)) (sourceZ q (tailJoint t)) = axisEntry q i t

def MixedVelocityTarget : Prop :=
  ∀ q (i : Fin 3) (t : Fin 2),
    dot3 (sourceV q (firstJoint i)) (sourceV q (tailJoint t)) = velocityEntry q offset i t

theorem source_mixed_axis_attempt : MixedAxisTarget := by
  intro q i t
  rw [source_first_axis_local_attempt, source_tail_axis_local_attempt, yaw_isometry_attempt]
  exact axis_entries_attempt q i t

theorem source_mixed_velocity_attempt (hc : CenterOffsetTarget) : MixedVelocityTarget := by
  intro q i t
  rw [source_front_column_local_attempt hc, source_tail_velocity_local_attempt hc, yaw_isometry_attempt]
  exact mixed_velocity_entries_attempt q offset i t

theorem source_mixed_gram_interface_attempt (hc : CenterOffsetTarget) :
    MixedAxisTarget ∧ MixedVelocityTarget :=
  ⟨source_mixed_axis_attempt, source_mixed_velocity_attempt hc⟩

theorem source_reverse_mixed_velocity_attempt (hc : CenterOffsetTarget)
    (q : Q6) (i : Fin 3) (t : Fin 2) :
    dot3 (sourceV q (tailJoint t)) (sourceV q (firstJoint i)) = velocityEntry q offset i t := by
  rw [dot_swap_attempt]
  exact source_mixed_velocity_attempt hc q i t

/- Six forward velocity and six axis entries only, with an optional transpose.
   No mass/Fourier/5x5/36-entry coverage or registry witness is produced. -/

end
end NEW_BODY6_SLICE_MIXED_Source20260907

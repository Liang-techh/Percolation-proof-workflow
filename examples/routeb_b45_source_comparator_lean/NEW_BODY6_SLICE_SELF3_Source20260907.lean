import NEW_BODY6_SLICE_SELF3_Core20260907
import NEW_BODY6_SLICE_LEVER_Source20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_SELF3_Source20260907

noncomputable section

open NEW_BODY6_SLICE_AXIS_Core20260907 NEW_BODY6_SLICE_VGRAM_Source20260907
open NEW_BODY6_SLICE_LEVER_Core20260907 NEW_BODY6_SLICE_LEVER_Source20260907
open NEW_BODY6_SLICE_SELF3_Core20260907 RouteBO1PerBodyExactSource

/- UNCOMPILED source seam. Both Fin 3 indices map through firstJoint to source
   indices 0..2. CenterOffsetTarget remains explicit for every velocity result.
   No source column is set to zero; only its known coordinate sparsity is used. -/

def SelfAxisTarget : Prop :=
  ∀ q (i j : Fin 3), dot3 (sourceZ q (firstJoint i)) (sourceZ q (firstJoint j)) =
    selfAxisEntry i j

def SelfVelocityTarget : Prop :=
  ∀ q (i j : Fin 3), dot3 (sourceV q (firstJoint i)) (sourceV q (firstJoint j)) =
    selfVelocityEntry q offset i j

theorem source_self_axis_attempt : SelfAxisTarget := by
  intro q i j
  rw [source_first_axis_local_attempt q i, source_first_axis_local_attempt q j,
    yaw_isometry_attempt]
  exact self_axis_entries_attempt i j

theorem source_first_template_attempt (hc : CenterOffsetTarget) (q : Q6) (i : Fin 3) :
    sourceV q (firstJoint i) = yawLift (q 0)
      (templateColumns (coeffA q offset) (coeffB q offset) (coeffP q offset)
        (coeffR q offset) (coeffU q offset) (coeffV q offset) i) := by
  rw [source_first_velocity_local_attempt hc]
  change yawLift (q 0) (offsetColumn q offset i) = _
  rw [velocity_template_attempt]

theorem source_self_velocity_attempt (hc : CenterOffsetTarget) : SelfVelocityTarget := by
  intro q i j
  rw [source_first_template_attempt hc q i, source_first_template_attempt hc q j]
  exact yaw_template_gram_attempt _ _ _ _ _ _ _ i j

theorem source_self_gram_interface_attempt (hc : CenterOffsetTarget) :
    SelfAxisTarget ∧ SelfVelocityTarget :=
  ⟨source_self_axis_attempt, source_self_velocity_attempt hc⟩

theorem source_self_velocity_transpose_attempt (hc : CenterOffsetTarget)
    (q : Q6) (i j : Fin 3) :
    dot3 (sourceV q (firstJoint j)) (sourceV q (firstJoint i)) =
      selfVelocityEntry q offset i j := by
  rw [source_self_velocity_attempt hc q j i]
  exact self_velocity_symmetric_attempt q offset j i

/- Nine entries of this self block, six independent by symmetry. No mixed,
   tail, weighted mass, Fourier, full coverage or registry theorem is supplied. -/

end
end NEW_BODY6_SLICE_SELF3_Source20260907

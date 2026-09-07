import NEW_BODY6_SLICE_MASSTAIL_Core20260907
import NEW_BODY6_SLICE_VGRAM_Tail20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_MASSTAIL_Source20260907

noncomputable section

open NEW_BODY6_SLICE_AXIS_Core20260907 NEW_BODY6_SLICE_VGRAM_Core20260907
open NEW_BODY6_SLICE_VGRAM_Source20260907 NEW_BODY6_SLICE_VGRAM_Tail20260907
open NEW_BODY6_SLICE_MASSTAIL_Core20260907 RouteBO1PerBodyExactSource

/- UNCOMPILED. Reuse actual tail Gram leaves without repeating DH geometry.
   This independent weight target avoids importing the mixed block. -/
def SourceWeightsTarget (m kappa : ℝ) : Prop :=
  routeBMass (5 : Fin 6) = m ∧ routeBInertiaScalar (5 : Fin 6) = kappa

def TailAxisTarget : Prop :=
  ∀ q (i j : Fin 2),
    dot3 (sourceZ q (tailJoint i)) (sourceZ q (tailJoint j)) = axisTable i j

def TailVelocityTarget : Prop :=
  ∀ q (i j : Fin 2),
    dot3 (sourceV q (tailJoint i)) (sourceV q (tailJoint j)) =
      velocityTable (q 4) offset i j

def TailMassTarget (m kappa : ℝ) : Prop :=
  ∀ q (i j : Fin 2),
    sourceBodyMass q (5 : Fin 6) (tailJoint i) (tailJoint j) =
      explicitTail (q 4) offset m kappa i j

theorem source_tail_axis_attempt : TailAxisTarget := by
  intro q i j
  fin_cases i <;> fin_cases j
  · simpa [tailJoint, axisTable] using source_axis33_attempt q
  · simpa [tailJoint, axisTable] using source_axis34_attempt q
  · change dot3 (sourceZ q 4) (sourceZ q 3) = 0
    rw [dot_swap_attempt]
    exact source_axis34_attempt q
  · simpa [tailJoint, axisTable] using source_axis44_attempt q

theorem source_tail_velocity_attempt (hc : CenterOffsetTarget) : TailVelocityTarget := by
  intro q i j
  fin_cases i <;> fin_cases j
  · simpa [tailJoint, velocityTable] using velocity_gram33_attempt hc q
  · simpa [tailJoint, velocityTable] using velocity_gram34_zero_attempt hc q
  · change dot3 (sourceV q 4) (sourceV q 3) = 0
    rw [dot_swap_attempt]
    exact velocity_gram34_zero_attempt hc q
  · simpa [tailJoint, velocityTable] using velocity_gram44_attempt hc q

/- Gram proof premises must be Lean terms, not symbolic check receipts. -/
theorem tail_mass_from_gram_attempt (m kappa : ℝ)
    (hw : SourceWeightsTarget m kappa)
    (hv : TailVelocityTarget) (ha : TailAxisTarget) : TailMassTarget m kappa := by
  have hm : (3 / 20 : ℝ) = m := by simpa [routeBMass] using hw.1
  have hk : (1 / 60 : ℝ) = kappa := by simpa [routeBInertiaScalar] using hw.2
  intro q i j
  rw [source_mass_gram_attempt, hm, hk, hv q i j, ha q i j]
  exact weighted_table_attempt (q 4) offset m kappa i j

theorem source_weighted_tail_attempt (hc : CenterOffsetTarget)
    (m kappa : ℝ) (hw : SourceWeightsTarget m kappa) : TailMassTarget m kappa :=
  tail_mass_from_gram_attempt m kappa hw (source_tail_velocity_attempt hc)
    source_tail_axis_attempt

/- The physical specialization deliberately retains both explicit premises. -/
theorem source_routeB_tail_table_attempt (hc : CenterOffsetTarget)
    (hw : SourceWeightsTarget (3 / 20 : ℝ) (1 / 60 : ℝ)) :
    ∀ q (i j : Fin 2),
      sourceBodyMass q (5 : Fin 6) (tailJoint i) (tailJoint j) =
        routeBTailTable (q 4) i j := by
  intro q i j
  calc
    sourceBodyMass q (5 : Fin 6) (tailJoint i) (tailJoint j) =
        explicitTail (q 4) offset (3 / 20) (1 / 60) i j :=
      source_weighted_tail_attempt hc (3 / 20) (1 / 60) hw q i j
    _ = routeBTailTable (q 4) i j := routeB_table_attempt (q 4) i j

/- No complete matrix, Fourier, coverage, comparator or registry witness. -/
end
end NEW_BODY6_SLICE_MASSTAIL_Source20260907

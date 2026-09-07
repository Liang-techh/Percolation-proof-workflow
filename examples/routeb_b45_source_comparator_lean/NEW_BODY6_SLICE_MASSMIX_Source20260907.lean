import NEW_BODY6_SLICE_MASSMIX_Core20260907
import NEW_BODY6_SLICE_MIXED_Source20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_MASSMIX_Source20260907

noncomputable section

open NEW_BODY6_SLICE_VGRAM_Source20260907 NEW_BODY6_SLICE_LEVER_Source20260907
open NEW_BODY6_SLICE_MIXED_Core20260907 NEW_BODY6_SLICE_MIXED_Source20260907
open NEW_BODY6_SLICE_MASSMIX_Core20260907 RouteBO1PerBodyExactSource

/- UNCOMPILED source seam. The typed row/column indices are 0..2 and 3..4.
   Both center and weight-binding premises remain explicit, including the
   fixed-weight specialization. No automatic source/comparator admission. -/

def SourceWeightsTarget (m kappa : ℝ) : Prop :=
  routeBMass (5 : Fin 6) = m ∧ routeBInertiaScalar (5 : Fin 6) = kappa

def MixedMassTarget (m kappa : ℝ) : Prop :=
  ∀ q (i : Fin 3) (t : Fin 2),
    sourceBodyMass q (5 : Fin 6) (firstJoint i) (tailJoint t) =
      explicitMixed q offset m kappa i t

/- Consumes actual body-6 constants, including already-divided inertia.
   A weight hypothesis cannot relabel body 5, add regularization or change q. -/
theorem source_weight_values_attempt (m kappa : ℝ) (hw : SourceWeightsTarget m kappa) :
    (3 / 20 : ℝ) = m ∧ (1 / 60 : ℝ) = kappa := by
  constructor
  · simpa [routeBMass] using hw.1
  · simpa [routeBInertiaScalar] using hw.2

/- Keep mixed Gram premises independently usable as a mathematical interface.
   They must be proof terms, never Python checks or CSV coefficient equalities. -/
theorem mixed_mass_from_gram_attempt (m kappa : ℝ)
    (hw : SourceWeightsTarget m kappa)
    (hv : MixedVelocityTarget) (ha : MixedAxisTarget) : MixedMassTarget m kappa := by
  rcases source_weight_values_attempt m kappa hw with ⟨hm, hk⟩
  intro q i t
  rw [source_mass_gram_attempt, hm, hk, hv q i t, ha q i t]
  exact weighted_table_attempt q offset m kappa i t

theorem source_weighted_mixed_attempt (hc : CenterOffsetTarget)
    (m kappa : ℝ) (hw : SourceWeightsTarget m kappa) : MixedMassTarget m kappa :=
  mixed_mass_from_gram_attempt m kappa hw
    (source_mixed_velocity_attempt hc) source_mixed_axis_attempt

/- Exact fixed body-6 table; hw is deliberately still an explicit premise. -/
theorem source_routeB_mixed_table_attempt (hc : CenterOffsetTarget)
    (hw : SourceWeightsTarget (3 / 20 : ℝ) (1 / 60 : ℝ)) :
    ∀ q (i : Fin 3) (t : Fin 2),
      sourceBodyMass q (5 : Fin 6) (firstJoint i) (tailJoint t) = routeBMixedTable q i t := by
  intro q i t
  exact source_weighted_mixed_attempt hc (3 / 20) (1 / 60) hw q i t

/- No self3/tail entries are assembled here. No full-matrix, Fourier, coverage,
   source-registry or comparator witness is constructed. -/

end
end NEW_BODY6_SLICE_MASSMIX_Source20260907

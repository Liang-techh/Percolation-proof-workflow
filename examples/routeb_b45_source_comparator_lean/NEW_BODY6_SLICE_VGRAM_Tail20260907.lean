import NEW_BODY6_SLICE_VGRAM_Source20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_VGRAM_Tail20260907

noncomputable section

open NEW_BODY6_SLICE_AXIS_Core20260907 NEW_BODY6_SLICE_AXIS_Geometry20260907
open NEW_BODY6_SLICE_VGRAM_Core20260907 NEW_BODY6_SLICE_VGRAM_Source20260907
open RouteBO1PerBodyExactSource RouteBSourceContractAdapter

/- UNCOMPILED minimal tail of the FRONT 5x5 block: indices 3,4, not index 5.
   Both corresponding velocity columns are generally nonzero. -/

theorem source_axis33_attempt (q : Q6) : dot3 (sourceZ q 3) (sourceZ q 3) = 1 := by
  change dot3 ((sourceContract q).axes 3) ((sourceContract q).axes 3) = _
  simp_rw [source_axis_local_attempt]
  rw [yaw_isometry_attempt]
  change dot3 (pitchLift (phi q) ![0, 0, 1]) (pitchLift (phi q) ![0, 0, 1]) = _
  rw [pitch_isometry_attempt]
  norm_num [dot3, Fin.sum_univ_succ]

theorem source_axis44_attempt (q : Q6) : dot3 (sourceZ q 4) (sourceZ q 4) = 1 := by
  change dot3 ((sourceContract q).axes 4) ((sourceContract q).axes 4) = _
  simp_rw [source_axis_local_attempt]
  rw [yaw_isometry_attempt]
  change dot3 (pitchLift (phi q) ![-Real.sin (q 3), Real.cos (q 3), 0])
    (pitchLift (phi q) ![-Real.sin (q 3), Real.cos (q 3), 0]) = _
  rw [pitch_isometry_attempt]
  have hy := Real.sin_sq_add_cos_sq (q 3)
  norm_num [dot3, Fin.sum_univ_succ]
  nlinarith [hy]

theorem source_axis34_attempt (q : Q6) : dot3 (sourceZ q 3) (sourceZ q 4) = 0 := by
  change dot3 ((sourceContract q).axes 3) ((sourceContract q).axes 4) = _
  simp_rw [source_axis_local_attempt]
  rw [yaw_isometry_attempt]
  change dot3 (pitchLift (phi q) ![0, 0, 1])
    (pitchLift (phi q) ![-Real.sin (q 3), Real.cos (q 3), 0]) = _
  rw [pitch_isometry_attempt]
  norm_num [dot3, Fin.sum_univ_succ]

theorem source_axis55_attempt (q : Q6) : dot3 (sourceZ q 5) (sourceZ q 5) = 1 :=
  source_dot_5_5_attempt q

theorem source_axis35_attempt (q : Q6) :
    dot3 (sourceZ q 3) (sourceZ q 5) = Real.cos (q 4) := source_dot_3_5_attempt q

theorem source_axis45_attempt (q : Q6) : dot3 (sourceZ q 4) (sourceZ q 5) = 0 :=
  source_dot_4_5_attempt q

theorem velocity_gram33_attempt (hc : CenterOffsetTarget) (q : Q6) :
    dot3 (sourceV q 3) (sourceV q 3) = offset ^ 2 * Real.sin (q 4) ^ 2 := by
  simp_rw [source_velocity3_attempt hc]
  rw [common_axis_gram_attempt, source_axis33_attempt, source_axis55_attempt,
    source_axis35_attempt]
  have hz := Real.sin_sq_add_cos_sq (q 4)
  linear_combination -(offset ^ 2) * hz

theorem velocity_gram44_attempt (hc : CenterOffsetTarget) (q : Q6) :
    dot3 (sourceV q 4) (sourceV q 4) = offset ^ 2 := by
  simp_rw [source_velocity4_attempt hc]
  rw [common_axis_gram_attempt, source_axis44_attempt, source_axis55_attempt,
    source_axis45_attempt]
  ring

theorem velocity_gram34_zero_attempt (hc : CenterOffsetTarget) (q : Q6) :
    dot3 (sourceV q 3) (sourceV q 4) = 0 := by
  rw [source_velocity3_attempt hc, source_velocity4_attempt hc,
    common_axis_gram_attempt, source_axis34_attempt, source_axis55_attempt,
    source_axis35_attempt, source_axis45_attempt]
  ring

theorem velocity4_nonzero_attempt (hc : CenterOffsetTarget) (q : Q6) :
    sourceV q (4 : Fin 6) ≠ 0 := by
  intro hv
  have hh := velocity_gram44_attempt hc q
  rw [hv] at hh
  norm_num [dot3, offset] at hh

theorem source_mass33_attempt (hc : CenterOffsetTarget) (q : Q6) :
    sourceBodyMass q (5 : Fin 6) (3 : Fin 6) (3 : Fin 6) =
      (1 / 60 : ℝ) + (147 / 800000 : ℝ) * Real.sin (q 4) ^ 2 := by
  rw [source_mass_gram_attempt, velocity_gram33_attempt hc, source_axis33_attempt]
  norm_num [offset] <;> ring

theorem source_mass44_attempt (hc : CenterOffsetTarget) (q : Q6) :
    sourceBodyMass q (5 : Fin 6) (4 : Fin 6) (4 : Fin 6) = (40441 / 2400000 : ℝ) := by
  rw [source_mass_gram_attempt, velocity_gram44_attempt hc, source_axis44_attempt]
  norm_num [offset]

theorem source_mass34_zero_attempt (hc : CenterOffsetTarget) (q : Q6) :
    sourceBodyMass q (5 : Fin 6) (3 : Fin 6) (4 : Fin 6) = 0 := by
  rw [source_mass_gram_attempt, velocity_gram34_zero_attempt hc, source_axis34_attempt]
  ring

theorem source_mass43_zero_attempt (hc : CenterOffsetTarget) (q : Q6) :
    sourceBodyMass q (5 : Fin 6) (4 : Fin 6) (3 : Fin 6) = 0 := by
  rw [source_mass_symmetric_attempt]
  exact source_mass34_zero_attempt hc q

end
end NEW_BODY6_SLICE_VGRAM_Tail20260907

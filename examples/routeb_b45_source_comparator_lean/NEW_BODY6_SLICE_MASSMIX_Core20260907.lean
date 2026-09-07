import NEW_BODY6_SLICE_MIXED_Core20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_MASSMIX_Core20260907

noncomputable section

open NEW_BODY6_SLICE_LEVER_Core20260907 NEW_BODY6_SLICE_MIXED_Core20260907

/- UNCOMPILED algebraic weighting of the existing 3x2 mixed block only.
   m and kappa are arbitrary real weights here, not asserted source constants. -/

def combinedWeight (h m kappa : ℝ) : ℝ := m * h ^ 2 + kappa

def weightedMixed (q : LQ) (h m kappa : ℝ) (i : Fin 3) (t : Fin 2) : ℝ :=
  m * velocityEntry q h i t + kappa * axisEntry q i t

/- Explicit six-entry table. The h^2 axial correction is retained. -/
def explicitMixed (q : LQ) (h m kappa : ℝ) : Fin 3 → Fin 2 → ℝ :=
  ![![m * h * Real.sin (q 4) * (radial q * Real.cos (q 3) +
          Real.cos (angleSum q) * Real.sin (q 3) / 20) +
        combinedWeight h m kappa * Real.cos (angleSum q) -
        m * h ^ 2 * (Real.cos (angleSum q) * Real.cos (q 4) -
          Real.sin (angleSum q) * Real.cos (q 3) * Real.sin (q 4)) * Real.cos (q 4),
      m * h * (Real.cos (q 4) * (radial q * Real.sin (q 3) -
          Real.cos (angleSum q) * Real.cos (q 3) / 20) +
          Real.sin (angleSum q) * Real.sin (q 4) / 20) +
        combinedWeight h m kappa * Real.sin (angleSum q) * Real.sin (q 3)],
    ![-m * h * Real.sin (q 3) * Real.sin (q 4) * (projAlong q + h * Real.cos (q 4)),
      m * h * (projAlong q * Real.cos (q 3) * Real.cos (q 4) +
          projAcross q * Real.sin (q 4)) + combinedWeight h m kappa * Real.cos (q 3)],
    ![-m * h * Real.sin (q 3) * Real.sin (q 4) * ((19 / 100 : ℝ) + h * Real.cos (q 4)),
      (m * h * (19 / 100 : ℝ) * Real.cos (q 4) + combinedWeight h m kappa) * Real.cos (q 3)]]

theorem weighted_table_attempt (q : LQ) (h m kappa : ℝ) (i : Fin 3) (t : Fin 2) :
    weightedMixed q h m kappa i t = explicitMixed q h m kappa i t := by
  fin_cases i <;> fin_cases t <;>
    norm_num [weightedMixed, velocityEntry, tripleEntry, axisEntry,
      frontLastDot, tailLastDot, explicitMixed, combinedWeight] <;> ring

/- Pure source-independent scalar specialization; no weight witness is issued. -/
def routeBMixedTable (q : LQ) : Fin 3 → Fin 2 → ℝ :=
  explicitMixed q (7 / 200) (3 / 20) (1 / 60)

theorem routeB_weight_arithmetic_attempt :
    (3 / 20 : ℝ) * (7 / 200 : ℝ) = (21 / 4000 : ℝ) ∧
    (3 / 20 : ℝ) * (7 / 200 : ℝ) ^ 2 = (147 / 800000 : ℝ) ∧
    combinedWeight (7 / 200) (3 / 20) (1 / 60) = (40441 / 2400000 : ℝ) := by
  norm_num [combinedWeight]

theorem routeB_table_weighted_attempt (q : LQ) (i : Fin 3) (t : Fin 2) :
    (3 / 20 : ℝ) * velocityEntry q (7 / 200) i t +
      (1 / 60 : ℝ) * axisEntry q i t = routeBMixedTable q i t :=
  weighted_table_attempt q (7 / 200) (3 / 20) (1 / 60) i t

end
end NEW_BODY6_SLICE_MASSMIX_Core20260907

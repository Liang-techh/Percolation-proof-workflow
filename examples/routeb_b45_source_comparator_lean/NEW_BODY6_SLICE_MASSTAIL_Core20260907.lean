import NEW_BODY6_SLICE_VGRAM_Core20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_MASSTAIL_Core20260907

noncomputable section

/- UNCOMPILED scalar weighting leaf. Ordered source columns are exactly 3,4.
   Generic real h,m,kappa do not assert physical source bindings. -/
def tailJoint (i : Fin 2) : Fin 6 := ⟨i.val + 3, by omega⟩

theorem tail_joint_order_attempt : tailJoint 0 = 3 ∧ tailJoint 1 = 4 := by
  constructor <;> rfl

def axisTable : Fin 2 → Fin 2 → ℝ := ![![1, 0], ![0, 1]]

def lastProjection (z : ℝ) : Fin 2 → ℝ := ![Real.cos z, 0]

/- The common terminal axis has unit norm. Retain its rank-one correction. -/
def correctedVelocity (z h : ℝ) (i j : Fin 2) : ℝ :=
  h ^ 2 * (axisTable i j - lastProjection z i * lastProjection z j)

def velocityTable (z h : ℝ) : Fin 2 → Fin 2 → ℝ :=
  ![![h ^ 2 * Real.sin z ^ 2, 0], ![0, h ^ 2]]

theorem velocity_correction_table_attempt (z h : ℝ) (i j : Fin 2) :
    correctedVelocity z h i j = velocityTable z h i j := by
  fin_cases i <;> fin_cases j <;>
    norm_num [correctedVelocity, axisTable, lastProjection, velocityTable] <;>
    linear_combination -(h ^ 2) * (Real.sin_sq_add_cos_sq z)

def weightedTail (z h m kappa : ℝ) (i j : Fin 2) : ℝ :=
  m * velocityTable z h i j + kappa * axisTable i j

def explicitTail (z h m kappa : ℝ) : Fin 2 → Fin 2 → ℝ :=
  ![![kappa + m * h ^ 2 * Real.sin z ^ 2, 0], ![0, kappa + m * h ^ 2]]

theorem weighted_table_attempt (z h m kappa : ℝ) (i j : Fin 2) :
    weightedTail z h m kappa i j = explicitTail z h m kappa i j := by
  fin_cases i <;> fin_cases j <;>
    norm_num [weightedTail, velocityTable, axisTable, explicitTail] <;> ring

theorem corrected_weighted_table_attempt (z h m kappa : ℝ) (i j : Fin 2) :
    m * correctedVelocity z h i j + kappa * axisTable i j =
      explicitTail z h m kappa i j := by
  rw [velocity_correction_table_attempt]
  exact weighted_table_attempt z h m kappa i j

theorem table_symmetric_attempt (z h m kappa : ℝ) (i j : Fin 2) :
    explicitTail z h m kappa i j = explicitTail z h m kappa j i := by
  fin_cases i <;> fin_cases j <;> rfl

/- Scalar specialization only; the source seam still requires weight binding. -/
def routeBTailTable (z : ℝ) : Fin 2 → Fin 2 → ℝ :=
  ![![(1 / 60 : ℝ) + (147 / 800000 : ℝ) * Real.sin z ^ 2, 0],
    ![0, (40441 / 2400000 : ℝ)]]

theorem routeB_table_attempt (z : ℝ) (i j : Fin 2) :
    explicitTail z (7 / 200) (3 / 20) (1 / 60) i j = routeBTailTable z i j := by
  fin_cases i <;> fin_cases j <;> norm_num [explicitTail, routeBTailTable] <;> ring

end
end NEW_BODY6_SLICE_MASSTAIL_Core20260907

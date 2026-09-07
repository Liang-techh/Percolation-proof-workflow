import NEW_BODY6_SLICE_LEVER_Core20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_SELF3_Core20260907

noncomputable section

open NEW_BODY6_SLICE_AXIS_Core20260907 NEW_BODY6_SLICE_VGRAM_Core20260907
open NEW_BODY6_SLICE_LEVER_Core20260907

/- UNCOMPILED source-independent first-three self Gram.
   No mixed/tail/Fourier imports; no unit-norm assumption for the last axis. -/

def templateColumns (a b p r u v : ℝ) : Fin 3 → AVec :=
  ![![-a, b, 0], ![p, 0, -r], ![u, 0, -v]]

def templateGram (a b p r u v : ℝ) : Fin 3 → Fin 3 → ℝ :=
  ![![a ^ 2 + b ^ 2, -a * p, -a * u],
    ![-a * p, p ^ 2 + r ^ 2, p * u + r * v],
    ![-a * u, p * u + r * v, u ^ 2 + v ^ 2]]

theorem template_gram_attempt (a b p r u v : ℝ) (i j : Fin 3) :
    dot3 (templateColumns a b p r u v i) (templateColumns a b p r u v j) =
      templateGram a b p r u v i j := by
  fin_cases i <;> fin_cases j <;>
    norm_num [dot3, templateColumns, templateGram, Fin.sum_univ_succ] <;> ring

theorem yaw_template_gram_attempt (t a b p r u v : ℝ) (i j : Fin 3) :
    dot3 (yawLift t (templateColumns a b p r u v i))
      (yawLift t (templateColumns a b p r u v j)) = templateGram a b p r u v i j := by
  rw [yaw_isometry_attempt]
  exact template_gram_attempt a b p r u v i j

theorem template_symmetric_attempt (a b p r u v : ℝ) (i j : Fin 3) :
    templateGram a b p r u v i j = templateGram a b p r u v j i := by
  fin_cases i <;> fin_cases j <;> rfl

def selfAxisEntry : Fin 3 → Fin 3 → ℝ := ![![1, 0, 0], ![0, 1, 1], ![0, 1, 1]]

theorem self_axis_entries_attempt (i j : Fin 3) :
    dot3 (firstAxis i) (firstAxis j) = selfAxisEntry i j := by
  fin_cases i <;> fin_cases j <;>
    norm_num [dot3, firstAxis, selfAxisEntry, Fin.sum_univ_succ]

def lastX (q : LQ) : ℝ :=
  Real.cos (angleSum q) * Real.cos (q 3) * Real.sin (q 4) +
    Real.sin (angleSum q) * Real.cos (q 4)
def lastY (q : LQ) : ℝ := Real.sin (q 3) * Real.sin (q 4)
def lastZ (q : LQ) : ℝ :=
  Real.cos (angleSum q) * Real.cos (q 4) -
    Real.sin (angleSum q) * Real.cos (q 3) * Real.sin (q 4)

theorem last_coordinates_attempt (q : LQ) :
    localAxis (angleSum q) (q 3) (q 4) 5 = ![lastX q, lastY q, lastZ q] := by
  funext a
  fin_cases a <;> norm_num [localAxis, pitchLift, lastX, lastY, lastZ] <;> ring

/- All six scalar slots retain h. In Source, h is the fixed offset 7/200. -/
def coeffA (q : LQ) (h : ℝ) : ℝ := 1 / 20 + h * lastY q
def coeffB (q : LQ) (h : ℝ) : ℝ := radial q + h * lastX q
def coeffP (q : LQ) (h : ℝ) : ℝ := height q + h * lastZ q
def coeffR (q : LQ) (h : ℝ) : ℝ := reach q + h * lastX q
def coeffU (q : LQ) (h : ℝ) : ℝ := (19 / 100) * Real.cos (angleSum q) + h * lastZ q
def coeffV (q : LQ) (h : ℝ) : ℝ := (19 / 100) * Real.sin (angleSum q) + h * lastX q

def offsetColumn (q : LQ) (h : ℝ) (i : Fin 3) : AVec :=
  fun a => baseLocal q i a + h *
    crossV (firstAxis i) (localAxis (angleSum q) (q 3) (q 4) 5) a

def selfVelocityEntry (q : LQ) (h : ℝ) : Fin 3 → Fin 3 → ℝ :=
  templateGram (coeffA q h) (coeffB q h) (coeffP q h) (coeffR q h) (coeffU q h) (coeffV q h)

theorem velocity_template_attempt (q : LQ) (h : ℝ) (i : Fin 3) :
    offsetColumn q h i =
      templateColumns (coeffA q h) (coeffB q h) (coeffP q h) (coeffR q h)
        (coeffU q h) (coeffV q h) i := by
  unfold offsetColumn
  rw [last_coordinates_attempt]
  fin_cases i <;> funext a <;> fin_cases a <;>
    norm_num [baseLocal, firstAxis, crossV, templateColumns,
      coeffA, coeffB, coeffP, coeffR, coeffU, coeffV] <;> ring

theorem local_self_velocity_gram_attempt (q : LQ) (h : ℝ) (i j : Fin 3) :
    dot3 (offsetColumn q h i) (offsetColumn q h j) = selfVelocityEntry q h i j := by
  rw [velocity_template_attempt q h i, velocity_template_attempt q h j]
  exact template_gram_attempt _ _ _ _ _ _ i j

theorem self_velocity_symmetric_attempt (q : LQ) (h : ℝ) (i j : Fin 3) :
    selfVelocityEntry q h i j = selfVelocityEntry q h j i :=
  template_symmetric_attempt _ _ _ _ _ _ i j

end
end NEW_BODY6_SLICE_SELF3_Core20260907

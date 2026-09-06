import Mathlib.Data.Real.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBQProjection
noncomputable section

/-!
Exact physical-side Q projection for the `(e₄+e₅)` velocity/source
direction.  Lean uses zero-based indices, so the two selected coordinates
are `3` and `4`.  The expanded quadratic form is the current exact Q:

  diag Q = (3, 8, 95/7, 165/7, 45, 90),
  Q[1,2] = Q[2,1] = -5.

The cross term is therefore `-10 * eta 1 * eta 2`.
-/

abbrev Vec6 := Fin 6 → ℝ

def qEnergy (eta : Vec6) : ℝ :=
  3 * (eta 0)^2 + 8 * (eta 1)^2 + (95 / 7) * (eta 2)^2
    + (165 / 7) * (eta 3)^2 + 45 * (eta 4)^2 + 90 * (eta 5)^2
    - 10 * eta 1 * eta 2

def etaU (eta : Vec6) : ℝ := eta 3 + eta 4

theorem qEnergy_dominates_selected (eta : Vec6) :
    (165 / 7) * (eta 3)^2 + 45 * (eta 4)^2 ≤ qEnergy eta := by
  have h0 : 0 ≤ 3 * (eta 0)^2 := by positivity
  have hblock1 : 0 ≤ 8 * (eta 1 - (5 / 8) * eta 2)^2 := by positivity
  have hblock2 : 0 ≤ (585 / 56) * (eta 2)^2 := by positivity
  have h5 : 0 ≤ 90 * (eta 5)^2 := by positivity
  unfold qEnergy
  nlinarith

/-! Exact two-variable weighted Cauchy inequality.  The slack is the
    rational square `(11*x - 21*y)^2 / 231`. -/

theorem weighted_projection_square (x y : ℝ) :
    (x + y)^2 ≤ (32 / 495) * ((165 / 7) * x^2 + 45 * y^2) := by
  have hsquare : 0 ≤ (11 * x - 21 * y)^2 := sq_nonneg _
  nlinarith

theorem projection_square
    (eta : Vec6) (epsilonQ : ℝ)
    (hQ : qEnergy eta ≤ epsilonQ^2) :
    (etaU eta)^2 ≤ (32 / 495) * epsilonQ^2 := by
  have hdom := qEnergy_dominates_selected eta
  have hw := weighted_projection_square (eta 3) (eta 4)
  unfold etaU at *
  nlinarith

theorem projection_abs
    (eta : Vec6) (epsilonQ : ℝ)
    (hepsilon : 0 ≤ epsilonQ)
    (hQ : qEnergy eta ≤ epsilonQ^2) :
    |etaU eta| ≤ Real.sqrt (32 / 495) * epsilonQ := by
  have hsq := projection_square eta epsilonQ hQ
  have hc : (0 : ℝ) ≤ 32 / 495 := by norm_num
  have hroot : (Real.sqrt (32 / 495 : ℝ))^2 = 32 / 495 := by
    exact Real.sq_sqrt hc
  have hroot_nonneg : 0 ≤ Real.sqrt (32 / 495 : ℝ) := Real.sqrt_nonneg _
  have hprod : 0 ≤ Real.sqrt (32 / 495 : ℝ) * epsilonQ :=
    mul_nonneg hroot_nonneg hepsilon
  have hsq' : (etaU eta)^2 ≤
      (Real.sqrt (32 / 495 : ℝ) * epsilonQ)^2 := by
    nlinarith [hsq, hroot]
  by_cases hsign : 0 ≤ etaU eta
  · rw [abs_of_nonneg hsign]
    nlinarith
  · have hnonpos : etaU eta ≤ 0 := le_of_not_ge hsign
    rw [abs_of_nonpos hnonpos]
    nlinarith

/-! The constant is exact for the selected two-coordinate subspace. -/

def sharpEta (s : ℝ) : Vec6 := ![0, 0, 0, 21 * s, 11 * s, 0]

theorem sharp_projection (s : ℝ) :
    qEnergy (sharpEta s) = 15840 * s^2 ∧
      etaU (sharpEta s) = 32 * s ∧
      (etaU (sharpEta s))^2 = (32 / 495) * qEnergy (sharpEta s) := by
  unfold qEnergy etaU sharpEta
  simp [Fin.sum_univ_succ]
  norm_num
  ring_nf

#print axioms qEnergy_dominates_selected
#print axioms weighted_projection_square
#print axioms projection_square
#print axioms projection_abs
#print axioms sharp_projection

end
end RouteBQProjection

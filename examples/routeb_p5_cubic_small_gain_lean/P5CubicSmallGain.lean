import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P5 cubic-power small-gain sidecar

This file formalizes source-independent consequences of
`review-T-P5-010-youhunmozun-20260907T0026.md`:

* a division-free scaled Young inequality for quadratic absorption;
* the power-level composition of cubic and relative residual gains;
* strict dissipation when the retained damping margin is positive;
* a squared energy-sublevel adapter that avoids square roots; and
* a one-ray scaling obstruction showing that a nonzero cubic coefficient
  cannot be globally absorbed by a quadratic budget on unbounded velocity.

It does not bind the central-FD tensor to deployed DH source, prove a P8
velocity/sublevel domain, or establish P5/M4 admission.
-/

set_option autoImplicit false

namespace RouteBP5CubicSmallGain

noncomputable section

/-- Division-free form of the scaled Young inequality.  Positive weights can
later be divided out by an adapter, but the reusable kernel needs no divisions. -/
theorem scaled_young_division_free (ai aj x y : ℝ) :
    2 * ai * aj * x * y ≤ aj ^ 2 * x ^ 2 + ai ^ 2 * y ^ 2 := by
  nlinarith [sq_nonneg (aj * x - ai * y)]

/-- Additive power-level small gain: two separately bounded error-power lanes
consume additive fractions of the same damping quadratic. -/
theorem cubic_relative_small_gain
    (A PC PR PB dE kC kR : ℝ)
    (hE : dE ≤ -A + PC + PR + PB)
    (hPC : PC ≤ kC * A)
    (hPR : PR ≤ kR * A) :
    dE ≤ -(1 - kC - kR) * A + PB := by
  nlinarith

/-- If the retained damping factor is positive and there is no positive bias,
the small-gain consumer yields strict decay whenever `A > 0`. -/
theorem cubic_relative_small_gain_strict
    (A PC PR PB dE kC kR : ℝ)
    (hA : 0 < A)
    (hgain : kC + kR < 1)
    (hPB : PB ≤ 0)
    (hE : dE ≤ -A + PC + PR + PB)
    (hPC : PC ≤ kC * A)
    (hPR : PR ≤ kR * A) :
    dE < 0 := by
  have hret : 0 < (1 - kC - kR) * A := by
    apply mul_pos
    · linarith
    · exact hA
  have hbound := cubic_relative_small_gain A PC PR PB dE kC kR hE hPC hPR
  nlinarith

/-- Nonnegative square domination gives an absolute-value bound. -/
theorem abs_le_of_sq_le_sq_nonneg
    (x y : ℝ) (hy : 0 ≤ y) (hxy : x ^ 2 ≤ y ^ 2) :
    |x| ≤ y := by
  rw [abs_le]
  constructor <;> nlinarith [sq_nonneg (x + y), sq_nonneg (x - y)]

/-- Squared energy-sublevel adapter from the mathematical review.  It consumes
`PC^2 ≤ Lambda*A^3`, `A ≤ R^2`, and `Lambda*R^2 ≤ kappa^2`, and returns the
power-level estimate without introducing square roots. -/
theorem cubic_absorption_of_energy_sublevel
    (A PC Lambda R kappa : ℝ)
    (hA : 0 ≤ A)
    (hLambda : 0 ≤ Lambda)
    (hkappa : 0 ≤ kappa)
    (hPCsq : PC ^ 2 ≤ Lambda * A ^ 3)
    (hAupper : A ≤ R ^ 2)
    (hgainSq : Lambda * R ^ 2 ≤ kappa ^ 2) :
    |PC| ≤ kappa * A := by
  have hA2 : 0 ≤ A ^ 2 := sq_nonneg A
  have hprod : 0 ≤ (R ^ 2 - A) * A ^ 2 := by
    exact mul_nonneg (by linarith) hA2
  have hA3 : A ^ 3 ≤ R ^ 2 * A ^ 2 := by
    nlinarith
  have hLambdaA : Lambda * A ^ 3 ≤ Lambda * (R ^ 2 * A ^ 2) :=
    mul_le_mul_of_nonneg_left hA3 hLambda
  have hgainA : (Lambda * R ^ 2) * A ^ 2 ≤ kappa ^ 2 * A ^ 2 :=
    mul_le_mul_of_nonneg_right hgainSq hA2
  have hsq : PC ^ 2 ≤ (kappa * A) ^ 2 := by
    nlinarith
  exact abs_le_of_sq_le_sq_nonneg PC (kappa * A) (mul_nonneg hkappa hA) hsq

/-- One-dimensional ray obstruction behind the global-cubic impossibility.
For any nonzero cubic coefficient and positive quadratic coefficient, no finite
real `kappa` can dominate `|c| t^3` by `kappa*a*t^2` for every `t ≥ 0`. -/
theorem nonzero_cubic_ray_not_globally_quadratic_absorbable
    (c a kappa : ℝ) (hc : c ≠ 0) (ha : 0 < a) :
    ¬ (∀ t : ℝ, 0 ≤ t → |c| * t ^ 3 ≤ kappa * a * t ^ 2) := by
  intro hglobal
  have hcabs : 0 < |c| := abs_pos.mpr hc
  let t : ℝ := |kappa| * a / |c| + 1
  have ht : 0 < t := by
    dsimp [t]
    have hnum : 0 ≤ |kappa| * a :=
      mul_nonneg (abs_nonneg kappa) (le_of_lt ha)
    have hquot : 0 ≤ |kappa| * a / |c| :=
      div_nonneg hnum (le_of_lt hcabs)
    linarith
  have hraw := hglobal t (le_of_lt ht)
  have ht2 : 0 < t ^ 2 := sq_pos_of_pos ht
  have hfactored : (|c| * t) * t ^ 2 ≤ (kappa * a) * t ^ 2 := by
    nlinarith
  have hlinear : |c| * t ≤ kappa * a := by
    by_contra hnot
    have hgt : kappa * a < |c| * t := lt_of_not_ge hnot
    have hmulgt : (kappa * a) * t ^ 2 < (|c| * t) * t ^ 2 :=
      mul_lt_mul_of_pos_right hgt ht2
    exact (not_lt_of_ge hfactored) hmulgt
  have hkappa_abs : kappa * a ≤ |kappa| * a := by
    exact mul_le_mul_of_nonneg_right (le_abs_self kappa) (le_of_lt ha)
  have hcne : |c| ≠ 0 := ne_of_gt hcabs
  have ht_identity : |c| * t = |kappa| * a + |c| := by
    dsimp [t]
    field_simp [hcne]
    <;> ring
  nlinarith

#print axioms scaled_young_division_free
#print axioms cubic_relative_small_gain
#print axioms cubic_relative_small_gain_strict
#print axioms abs_le_of_sq_le_sq_nonneg
#print axioms cubic_absorption_of_energy_sublevel
#print axioms nonzero_cubic_ray_not_globally_quadratic_absorbable

end

end RouteBP5CubicSmallGain

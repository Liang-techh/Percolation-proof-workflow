import Mathlib

noncomputable section

namespace RouteBP4O2SignedRectangleEnergy

/-- Retained two-channel quadratic energy/dissipation block. -/
def energyQuadratic (p q s x y : ℝ) : ℝ :=
  p * x ^ 2 + 2 * q * x * y + s * y ^ 2

/-- Adjugate quadratic that prices an affine residual error. -/
def dualQuadratic (p q s e4 e5 : ℝ) : ℝ :=
  s * e4 ^ 2 - 2 * q * e4 * e5 + p * e5 ^ 2

/-- The error must already be in the force/residual coordinates paired with `(x,y)`. -/
def errorPower (e4 e5 x y : ℝ) : ℝ :=
  -(e4 * x + e5 * y)

/-- Distinct wrappers prevent silently treating solve/acceleration error as force residual error. -/
structure AccelerationError2 where
  ch4 : ℝ
  ch5 : ℝ

/-- This is the only error type consumed by the energy gate below. -/
structure ForceResidualError2 where
  ch4 : ℝ
  ch5 : ℝ

/-- Positive definiteness forces the second diagonal entry positive. -/
theorem second_diagonal_pos
    (p q s : ℝ)
    (hp : 0 < p)
    (hdelta : 0 < p * s - q ^ 2) :
    0 < s := by
  by_contra hnot
  have hs : s ≤ 0 := le_of_not_gt hnot
  have hps : p * s ≤ 0 :=
    mul_nonpos_of_nonneg_of_nonpos (le_of_lt hp) hs
  nlinarith [sq_nonneg q]

/-- Division-free SOS identity for the retained quadratic. -/
theorem energy_sos_identity
    (p q s x y : ℝ) :
    p * energyQuadratic p q s x y =
      (p * x + q * y) ^ 2 + (p * s - q ^ 2) * y ^ 2 := by
  simp only [energyQuadratic]
  ring

/-- A positive-definite 2x2 block is nonnegative without invoking eigenvalues. -/
theorem energy_quadratic_nonnegative
    (p q s x y : ℝ)
    (hp : 0 < p)
    (hdelta : 0 < p * s - q ^ 2) :
    0 ≤ energyQuadratic p q s x y := by
  have hsos :
      0 ≤ (p * x + q * y) ^ 2 + (p * s - q ^ 2) * y ^ 2 := by
    exact add_nonneg (sq_nonneg _) (mul_nonneg (le_of_lt hdelta) (sq_nonneg y))
  by_contra hnot
  have hneg : energyQuadratic p q s x y < 0 := lt_of_not_ge hnot
  have hprod : p * energyQuadratic p q s x y < 0 :=
    mul_neg_of_pos_of_neg hp hneg
  rw [energy_sos_identity] at hprod
  exact (not_lt_of_ge hsos) hprod

/-- Division-free SOS identity for the adjugate/dual quadratic. -/
theorem dual_sos_identity
    (p q s z1 z2 : ℝ) :
    p * dualQuadratic p q s z1 z2 =
      (p * z2 - q * z1) ^ 2 + (p * s - q ^ 2) * z1 ^ 2 := by
  simp only [dualQuadratic]
  ring

/-- The dual quadratic is nonnegative on a positive-definite block. -/
theorem dual_quadratic_nonnegative
    (p q s z1 z2 : ℝ)
    (hp : 0 < p)
    (hdelta : 0 < p * s - q ^ 2) :
    0 ≤ dualQuadratic p q s z1 z2 := by
  have hsos :
      0 ≤ (p * z2 - q * z1) ^ 2 + (p * s - q ^ 2) * z1 ^ 2 := by
    exact add_nonneg (sq_nonneg _) (mul_nonneg (le_of_lt hdelta) (sq_nonneg z1))
  by_contra hnot
  have hneg : dualQuadratic p q s z1 z2 < 0 := lt_of_not_ge hnot
  have hprod : p * dualQuadratic p q s z1 z2 < 0 :=
    mul_neg_of_pos_of_neg hp hneg
  rw [dual_sos_identity] at hprod
  exact (not_lt_of_ge hsos) hprod

/-- Exact polynomial completion behind the O2 energy charge. -/
theorem retained_dissipation_completion_identity
    (p q s theta x y e4 e5 : ℝ) :
    dualQuadratic p q s
        (2 * theta * (p * x + q * y) + e4)
        (2 * theta * (q * x + s * y) + e5) =
      4 * theta * (p * s - q ^ 2) *
          (theta * energyQuadratic p q s x y + e4 * x + e5 * y) +
        dualQuadratic p q s e4 e5 := by
  simp only [dualQuadratic, energyQuadratic]
  ring

/--
Division-free retained-dissipation completion.  No inverse, square root, or
floating-point semantics enters this theorem.
-/
theorem o2_error_power_retained_dissipation_completion_2x2
    (p q s theta x y e4 e5 : ℝ)
    (hp : 0 < p)
    (hdelta : 0 < p * s - q ^ 2) :
    4 * theta * (p * s - q ^ 2) *
        (-theta * energyQuadratic p q s x y - (e4 * x + e5 * y)) ≤
      dualQuadratic p q s e4 e5 := by
  have hnonneg := dual_quadratic_nonnegative p q s
    (2 * theta * (p * x + q * y) + e4)
    (2 * theta * (q * x + s * y) + e5) hp hdelta
  have hid := retained_dissipation_completion_identity p q s theta x y e4 e5
  nlinarith

/-- A convex scalar quadratic is bounded by endpoint bounds on an interval. -/
theorem quadratic_interval_le_endpoints
    (A B C a b r K : ℝ)
    (hA : 0 ≤ A)
    (har : a ≤ r)
    (hrb : r ≤ b)
    (haK : A * a ^ 2 + B * a + C ≤ K)
    (hbK : A * b ^ 2 + B * b + C ≤ K) :
    A * r ^ 2 + B * r + C ≤ K := by
  by_cases hab : a = b
  · have hr : r = a := by nlinarith
    subst r
    exact haK
  · have hablt : a < b := lt_of_le_of_ne (le_trans har hrb) hab
    have hwa : 0 ≤ b - r := by linarith
    have hwb : 0 ≤ r - a := by linarith
    have hba : 0 ≤ b - a := by linarith
    have hleft := mul_le_mul_of_nonneg_left haK hwa
    have hright := mul_le_mul_of_nonneg_left hbK hwb
    have hweighted :
        (b - r) * (A * a ^ 2 + B * a + C) +
            (r - a) * (A * b ^ 2 + B * b + C) ≤
          (b - r) * K + (r - a) * K :=
      add_le_add hleft hright
    have hconv : 0 ≤ A * (r - a) * (b - r) * (b - a) :=
      mul_nonneg (mul_nonneg (mul_nonneg hA hwb) hwa) hba
    have hid :
        (b - r) * (A * a ^ 2 + B * a + C) +
              (r - a) * (A * b ^ 2 + B * b + C) -
            (b - a) * (A * r ^ 2 + B * r + C) =
          A * (r - a) * (b - r) * (b - a) := by
      ring
    have hbridge :
        (b - a) * (A * r ^ 2 + B * r + C) ≤
          (b - r) * (A * a ^ 2 + B * a + C) +
            (r - a) * (A * b ^ 2 + B * b + C) := by
      nlinarith
    have hscaled :
        (b - a) * (A * r ^ 2 + B * r + C) ≤ (b - a) * K := by
      calc
        (b - a) * (A * r ^ 2 + B * r + C) ≤
            (b - r) * (A * a ^ 2 + B * a + C) +
              (r - a) * (A * b ^ 2 + B * b + C) := hbridge
        _ ≤ (b - r) * K + (r - a) * K := hweighted
        _ = (b - a) * K := by ring
    by_contra hnot
    have hlt : K < A * r ^ 2 + B * r + C := lt_of_not_ge hnot
    have hmul : (b - a) * K < (b - a) * (A * r ^ 2 + B * r + C) :=
      mul_lt_mul_of_pos_left hlt (sub_pos.mpr hablt)
    exact (not_lt_of_ge hscaled) hmul

/--
For the dual quadratic, four signed rectangle corners are sufficient.  This
retains correlation from one-sided intervals instead of replacing them by
absolute component maxima.
-/
theorem dual_quadratic_rectangle_le_corners
    (p q s L4 U4 L5 U5 e4 e5 K : ℝ)
    (hp : 0 ≤ p)
    (hs : 0 ≤ s)
    (he4L : L4 ≤ e4)
    (he4U : e4 ≤ U4)
    (he5L : L5 ≤ e5)
    (he5U : e5 ≤ U5)
    (hLL : dualQuadratic p q s L4 L5 ≤ K)
    (hLU : dualQuadratic p q s L4 U5 ≤ K)
    (hUL : dualQuadratic p q s U4 L5 ≤ K)
    (hUU : dualQuadratic p q s U4 U5 ≤ K) :
    dualQuadratic p q s e4 e5 ≤ K := by
  have hleft : dualQuadratic p q s L4 e5 ≤ K := by
    apply quadratic_interval_le_endpoints p (-2 * q * L4) (s * L4 ^ 2)
      L5 U5 e5 K hp he5L he5U
    · nlinarith [hLL]
    · nlinarith [hLU]
  have hright : dualQuadratic p q s U4 e5 ≤ K := by
    apply quadratic_interval_le_endpoints p (-2 * q * U4) (s * U4 ^ 2)
      L5 U5 e5 K hp he5L he5U
    · nlinarith [hUL]
    · nlinarith [hUU]
  apply quadratic_interval_le_endpoints s (-2 * q * e5) (p * e5 ^ 2)
    L4 U4 e4 K hs he4L he4U
  · nlinarith [hleft]
  · nlinarith [hright]

/--
Portable exact-real O2 consumer.  The four corner obligations are deliberately
division-free and can be discharged by exact rational arithmetic.
-/
theorem o2_signed_rectangle_energy_consumer
    (p q s theta kappa L4 U4 L5 U5 e4 e5 x y : ℝ)
    (hp : 0 < p)
    (hdelta : 0 < p * s - q ^ 2)
    (htheta : 0 < theta)
    (he4L : L4 ≤ e4)
    (he4U : e4 ≤ U4)
    (he5L : L5 ≤ e5)
    (he5U : e5 ≤ U5)
    (hLL : dualQuadratic p q s L4 L5 ≤
      4 * theta * (p * s - q ^ 2) * kappa)
    (hLU : dualQuadratic p q s L4 U5 ≤
      4 * theta * (p * s - q ^ 2) * kappa)
    (hUL : dualQuadratic p q s U4 L5 ≤
      4 * theta * (p * s - q ^ 2) * kappa)
    (hUU : dualQuadratic p q s U4 U5 ≤
      4 * theta * (p * s - q ^ 2) * kappa) :
    -energyQuadratic p q s x y + errorPower e4 e5 x y ≤
      -(1 - theta) * energyQuadratic p q s x y + kappa := by
  have hs : 0 < s := second_diagonal_pos p q s hp hdelta
  have hN := dual_quadratic_rectangle_le_corners p q s
    L4 U4 L5 U5 e4 e5
    (4 * theta * (p * s - q ^ 2) * kappa)
    (le_of_lt hp) (le_of_lt hs) he4L he4U he5L he5U hLL hLU hUL hUU
  have hcomp := o2_error_power_retained_dissipation_completion_2x2
    p q s theta x y e4 e5 hp hdelta
  have hscaled :
      4 * theta * (p * s - q ^ 2) *
          (-theta * energyQuadratic p q s x y - (e4 * x + e5 * y)) ≤
        4 * theta * (p * s - q ^ 2) * kappa :=
    le_trans hcomp hN
  have hfac : 0 < 4 * theta * (p * s - q ^ 2) := by positivity
  have hcore :
      -theta * energyQuadratic p q s x y - (e4 * x + e5 * y) ≤ kappa := by
    by_contra hnot
    have hlt : kappa <
        -theta * energyQuadratic p q s x y - (e4 * x + e5 * y) :=
      lt_of_not_ge hnot
    have hmul := mul_lt_mul_of_pos_left hlt hfac
    exact (not_lt_of_ge hscaled) hmul
  simp only [errorPower]
  nlinarith

/--
First-exit seam with an explicit additive reserve.  The source lane still has
to export the actual signed force-residual rectangle on the same box.
-/
theorem o2_signed_rectangle_first_exit_with_reserve
    (p q s theta kappa L4 U4 L5 U5 e4 e5 x y c V Vstar beta Vdot : ℝ)
    (hp : 0 < p)
    (hdelta : 0 < p * s - q ^ 2)
    (htheta : 0 < theta)
    (htheta1 : theta ≤ 1)
    (he4L : L4 ≤ e4)
    (he4U : e4 ≤ U4)
    (he5L : L5 ≤ e5)
    (he5U : e5 ≤ U5)
    (hLL : dualQuadratic p q s L4 L5 ≤
      4 * theta * (p * s - q ^ 2) * kappa)
    (hLU : dualQuadratic p q s L4 U5 ≤
      4 * theta * (p * s - q ^ 2) * kappa)
    (hUL : dualQuadratic p q s U4 L5 ≤
      4 * theta * (p * s - q ^ 2) * kappa)
    (hUU : dualQuadratic p q s U4 U5 ≤
      4 * theta * (p * s - q ^ 2) * kappa)
    (hV : V = Vstar)
    (hledger : Vdot ≤ -c * V - energyQuadratic p q s x y +
      errorPower e4 e5 x y + beta)
    (hreserve : kappa < c * Vstar - beta) :
    Vdot < 0 := by
  have hconsumer := o2_signed_rectangle_energy_consumer
    p q s theta kappa L4 U4 L5 U5 e4 e5 x y hp hdelta htheta
    he4L he4U he5L he5U hLL hLU hUL hUU
  have hD : 0 ≤ energyQuadratic p q s x y :=
    energy_quadratic_nonnegative p q s x y hp hdelta
  have hret : 0 ≤ (1 - theta) * energyQuadratic p q s x y :=
    mul_nonneg (by linarith) hD
  rw [hV] at hledger
  nlinarith

/-- Global port/gain sign transport leaves the final dual charge unchanged. -/
theorem global_sign_dual_invariant
    (p q s e4 e5 : ℝ) :
    dualQuadratic p q s (-e4) (-e5) = dualQuadratic p q s e4 e5 := by
  simp only [dualQuadratic]
  ring

/-- A signed interval transports under the global residual sign flip. -/
theorem global_sign_rectangle_transport
    (L U e : ℝ)
    (hL : L ≤ e)
    (hU : e ≤ U) :
    -U ≤ -e ∧ -e ≤ -L := by
  constructor <;> linarith

/-- Exact small-scale identity exposing the absolute-bias obstruction. -/
theorem absolute_bias_small_scale_identity
    (p q s e4 e5 t : ℝ) :
    -energyQuadratic p q s (-t * e4) (-t * e5) +
        errorPower e4 e5 (-t * e4) (-t * e5) =
      -(t ^ 2) * energyQuadratic p q s e4 e5 +
        t * (e4 ^ 2 + e5 ^ 2) := by
  simp only [energyQuadratic, errorPower]
  ring

/--
If a fixed nonzero bias is allowed and `t*D_H(e) < |e|^2`, the affine power
beats quadratic dissipation at the scaled state `u=-t e`.
-/
theorem absolute_evaluator_bias_blocks_homogeneous_decay
    (p q s e4 e5 t : ℝ)
    (hD : 0 < energyQuadratic p q s e4 e5)
    (hnorm : 0 < e4 ^ 2 + e5 ^ 2)
    (ht : 0 < t)
    (hsmall : t * energyQuadratic p q s e4 e5 < e4 ^ 2 + e5 ^ 2) :
    0 < -energyQuadratic p q s (-t * e4) (-t * e5) +
      errorPower e4 e5 (-t * e4) (-t * e5) := by
  rw [absolute_bias_small_scale_identity]
  have hgap : 0 < e4 ^ 2 + e5 ^ 2 - t * energyQuadratic p q s e4 e5 := by
    linarith
  have hprod : 0 < t *
      (e4 ^ 2 + e5 ^ 2 - t * energyQuadratic p q s e4 e5) :=
    mul_pos ht hgap
  nlinarith

#print axioms second_diagonal_pos
#print axioms energy_sos_identity
#print axioms energy_quadratic_nonnegative
#print axioms dual_sos_identity
#print axioms dual_quadratic_nonnegative
#print axioms retained_dissipation_completion_identity
#print axioms o2_error_power_retained_dissipation_completion_2x2
#print axioms quadratic_interval_le_endpoints
#print axioms dual_quadratic_rectangle_le_corners
#print axioms o2_signed_rectangle_energy_consumer
#print axioms o2_signed_rectangle_first_exit_with_reserve
#print axioms global_sign_dual_invariant
#print axioms global_sign_rectangle_transport
#print axioms absolute_bias_small_scale_identity
#print axioms absolute_evaluator_bias_blocks_homogeneous_decay

end RouteBP4O2SignedRectangleEnergy

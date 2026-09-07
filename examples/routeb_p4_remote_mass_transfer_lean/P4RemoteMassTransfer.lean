import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P4 remote mass-metric transfer sidecar

This file formalizes the source-independent arithmetic core of
`review-T-P4-012-youhunmozun-20260907T0130.md`.

It proves:

* the division-free scaled PSD cross-term bound;
* direct Schur/PMI absorption from a positive-block comparison and one distal
  quadratic-energy bound;
* a square-to-absolute component reserve adapter; and
* the exact rational constants for the corrected channel-4/channel-5 reserve.

It does not identify the abstract quadratic forms with deployed Float64 DH,
prove P8 distal-acceleration coverage, or close P4/M4.
-/

set_option autoImplicit false

namespace RouteBP4RemoteMassTransfer

noncomputable section

/-- If a scaled local/distal block quadratic is nonnegative, then its cross
term obeys the corresponding division-free lower bound.  This is the exact
algebraic form obtained by evaluating a PSD block matrix on `(theta*x, a)`. -/
theorem remote_scaled_cross_bound_division_free
    (theta QB C QD : ℝ)
    (hpsd : 0 ≤ theta ^ 2 * QB + 2 * theta * C + QD) :
    -(theta ^ 2) * QB - QD ≤ 2 * theta * C := by
  linarith

/-- Direct source-independent consumer for the remote action.  If the P4
positive quadratic dominates `theta*QB`, and the distal quadratic energy fits
inside `theta*d*y^2`, then the remote cross term is fully absorbed.

The hypothesis `hpsd` is exactly the scaled block-PSD evaluation; no matrix
inverse or entrywise `M_BD` bound appears. -/
theorem remote_schur_absorption
    (theta QB C QD P d y : ℝ)
    (htheta : 0 < theta)
    (hpsd : 0 ≤ theta ^ 2 * QB + 2 * theta * C + QD)
    (hP : theta * QB ≤ P)
    (hQD : QD ≤ theta * d * y ^ 2) :
    0 ≤ P + 2 * C + d * y ^ 2 := by
  have hPscaled : theta ^ 2 * QB ≤ theta * P := by
    nlinarith
  have hscaled : 0 ≤ theta * (P + 2 * C + d * y ^ 2) := by
    nlinarith
  nlinarith

/-- Nonnegative square domination gives an absolute-value bound. -/
theorem abs_le_of_sq_le_sq_nonneg
    (x y : ℝ) (hy : 0 ≤ y) (hxy : x ^ 2 ≤ y ^ 2) :
    |x| ≤ y := by
  rw [abs_le]
  constructor <;> nlinarith [sq_nonneg (x + y), sq_nonneg (x - y)]

/-- Convert a distal-energy square bound into a linear coefficient reserve.
This is deliberately source-independent and square-root-free. -/
theorem remote_component_reserve
    (U gamma c E r y : ℝ)
    (hU : 0 ≤ U)
    (hc : 0 ≤ c)
    (hr : r ^ 2 ≤ U * E)
    (hE : E ≤ gamma * y ^ 2)
    (hUg : U * gamma = c ^ 2) :
    |r| ≤ c * |y| := by
  have hUE : U * E ≤ U * (gamma * y ^ 2) :=
    mul_le_mul_of_nonneg_left hE hU
  have hsq : r ^ 2 ≤ (c * |y|) ^ 2 := by
    calc
      r ^ 2 ≤ U * E := hr
      _ ≤ U * (gamma * y ^ 2) := hUE
      _ = (c * |y|) ^ 2 := by
        calc
          U * (gamma * y ^ 2) = (U * gamma) * y ^ 2 := by ring
          _ = c ^ 2 * y ^ 2 := by rw [hUg]
          _ = c ^ 2 * |y| ^ 2 := by rw [sq_abs]
          _ = (c * |y|) ^ 2 := by ring
  exact abs_le_of_sq_le_sq_nonneg r (c * |y|)
    (mul_nonneg hc (abs_nonneg y)) hsq

/-- Exact global upper coefficient for the unregularized block-4 mass entry. -/
def U4 : ℝ := 280441 / 2400000

/-- Exact global upper coefficient for the unregularized block-5 mass entry. -/
def U5 : ℝ := 40147 / 800000

/-- Distal-energy coefficient sufficient to leave a `6/25` remote reserve in
channel 4 after the corrected `1/100` force-coordinate `kc` term. -/
def gamma4 : ℝ := 138240 / 280441

/-- Distal-energy coefficient sufficient to leave a `49/200` remote reserve in
channel 5 after the corrected `1/200` force-coordinate `kc` term. -/
def gamma5 : ℝ := 48020 / 40147

theorem U4_pos : 0 < U4 := by
  norm_num [U4]

theorem U5_pos : 0 < U5 := by
  norm_num [U5]

theorem gamma4_pos : 0 < gamma4 := by
  norm_num [gamma4]

theorem gamma5_pos : 0 < gamma5 := by
  norm_num [gamma5]

/-- Exact square identity behind the channel-4 distal-energy target. -/
theorem channel4_remote_square_identity :
    U4 * gamma4 = (6 / 25 : ℝ) ^ 2 := by
  norm_num [U4, gamma4]

/-- Exact square identity behind the channel-5 distal-energy target. -/
theorem channel5_remote_square_identity :
    U5 * gamma5 = (49 / 200 : ℝ) ^ 2 := by
  norm_num [U5, gamma5]

/-- Corrected force-coordinate `kc` plus the channel-4 remote reserve exactly
fills the quarter residual coefficient. -/
theorem channel4_quarter_reserve_identity :
    (1 / 100 : ℝ) + 6 / 25 = 1 / 4 := by
  norm_num

/-- Corrected force-coordinate `kc` plus the channel-5 remote reserve exactly
fills the quarter residual coefficient. -/
theorem channel5_quarter_reserve_identity :
    (1 / 200 : ℝ) + 49 / 200 = 1 / 4 := by
  norm_num

/-- Concrete channel-4 remote component consequence, still conditional on the
abstract distal quadratic energy premise. -/
theorem channel4_remote_component
    (E r q5 : ℝ)
    (hr : r ^ 2 ≤ U4 * E)
    (hE : E ≤ gamma4 * q5 ^ 2) :
    |r| ≤ (6 / 25 : ℝ) * |q5| := by
  exact remote_component_reserve U4 gamma4 (6 / 25) E r q5
    (le_of_lt U4_pos) (by norm_num) hr hE channel4_remote_square_identity

/-- Concrete channel-5 remote component consequence, still conditional on the
abstract distal quadratic energy premise. -/
theorem channel5_remote_component
    (E r q4 : ℝ)
    (hr : r ^ 2 ≤ U5 * E)
    (hE : E ≤ gamma5 * q4 ^ 2) :
    |r| ≤ (49 / 200 : ℝ) * |q4| := by
  exact remote_component_reserve U5 gamma5 (49 / 200) E r q4
    (le_of_lt U5_pos) (by norm_num) hr hE channel5_remote_square_identity

#print axioms remote_scaled_cross_bound_division_free
#print axioms remote_schur_absorption
#print axioms abs_le_of_sq_le_sq_nonneg
#print axioms remote_component_reserve
#print axioms U4_pos
#print axioms U5_pos
#print axioms gamma4_pos
#print axioms gamma5_pos
#print axioms channel4_remote_square_identity
#print axioms channel5_remote_square_identity
#print axioms channel4_quarter_reserve_identity
#print axioms channel5_quarter_reserve_identity
#print axioms channel4_remote_component
#print axioms channel5_remote_component

end

end RouteBP4RemoteMassTransfer

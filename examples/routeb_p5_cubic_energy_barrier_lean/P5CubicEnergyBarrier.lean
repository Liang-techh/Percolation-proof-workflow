import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P5 cubic-energy self-bootstrap sidecar

This file formalizes the source-independent algebra from
`review-T-P5-011-honglianmozun-20260907T0155.md`.

It proves:
* square-only absorption of a cubic power term from an energy barrier;
* the strict version at positive damping energy;
* the scalar Lyapunov-ledger consumer;
* the regularizer-to-damping coercivity constant `K = 2600000`; and
* the exact Fourier scalar reduction
  `Lambda*K = 13*S_F / 72000000000000000`.

It deliberately does not formalize first-exit/ODE existence, source binding,
Float64 execution error, a physical lower bound for the non-kinetic storage,
or P5/M4 admission.
-/

set_option autoImplicit false

namespace RouteBP5CubicEnergyBarrier

noncomputable section

/-- Nonnegative square domination gives an absolute-value bound. -/
theorem abs_le_of_sq_le_sq_nonneg
    (x y : ℝ) (hy : 0 ≤ y) (hxy : x ^ 2 ≤ y ^ 2) :
    |x| ≤ y := by
  rw [abs_le]
  constructor <;> nlinarith [sq_nonneg (x + y), sq_nonneg (x - y)]

/-- Core square-only bootstrap: cubic power is absorbed by the remaining
quadratic damping whenever storage controls the damping energy and the
energy-dependent gain stays below `g^2`. -/
theorem cubic_square_absorption_from_energy_barrier
    (A Z PC Lambda K g : ℝ)
    (hA : 0 ≤ A) (hLambda : 0 ≤ Lambda) (hg : 0 ≤ g)
    (hcoerce : A ≤ K * Z)
    (hcubic : PC ^ 2 ≤ Lambda * A ^ 3)
    (hbarrier : Lambda * K * Z ≤ g ^ 2) :
    |PC| ≤ g * A := by
  have hA2 : 0 ≤ A ^ 2 := sq_nonneg A
  have hLambdaA : Lambda * A ≤ g ^ 2 := by
    calc
      Lambda * A ≤ Lambda * (K * Z) :=
        mul_le_mul_of_nonneg_left hcoerce hLambda
      _ = Lambda * K * Z := by ring
      _ ≤ g ^ 2 := hbarrier
  have hscaled : (Lambda * A) * A ^ 2 ≤ g ^ 2 * A ^ 2 :=
    mul_le_mul_of_nonneg_right hLambdaA hA2
  have hsq : PC ^ 2 ≤ (g * A) ^ 2 := by
    calc
      PC ^ 2 ≤ Lambda * A ^ 3 := hcubic
      _ = (Lambda * A) * A ^ 2 := by ring
      _ ≤ g ^ 2 * A ^ 2 := hscaled
      _ = (g * A) ^ 2 := by ring
  exact abs_le_of_sq_le_sq_nonneg PC (g * A) (mul_nonneg hg hA) hsq

/-- Strict square-only bootstrap.  Strict barrier margin and positive damping
energy imply strict power absorption. -/
theorem cubic_square_strict_absorption_from_energy_barrier
    (A Z PC Lambda K g : ℝ)
    (hA : 0 < A) (hLambda : 0 ≤ Lambda) (hg : 0 < g)
    (hcoerce : A ≤ K * Z)
    (hcubic : PC ^ 2 ≤ Lambda * A ^ 3)
    (hbarrier : Lambda * K * Z < g ^ 2) :
    |PC| < g * A := by
  have hA2pos : 0 < A ^ 2 := sq_pos_of_pos hA
  have hLambdaA : Lambda * A < g ^ 2 := by
    calc
      Lambda * A ≤ Lambda * (K * Z) :=
        mul_le_mul_of_nonneg_left hcoerce hLambda
      _ = Lambda * K * Z := by ring
      _ < g ^ 2 := hbarrier
  have hscaled : (Lambda * A) * A ^ 2 < g ^ 2 * A ^ 2 :=
    mul_lt_mul_of_pos_right hLambdaA hA2pos
  have hsq : PC ^ 2 < (g * A) ^ 2 := by
    calc
      PC ^ 2 ≤ Lambda * A ^ 3 := hcubic
      _ = (Lambda * A) * A ^ 2 := by ring
      _ < g ^ 2 * A ^ 2 := hscaled
      _ = (g * A) ^ 2 := by ring
  rw [abs_lt]
  constructor
  · by_contra hnot
    have hle : PC ≤ -(g * A) := le_of_not_gt hnot
    have hsqge : (g * A) ^ 2 ≤ PC ^ 2 := by
      nlinarith [sq_nonneg (PC + g * A)]
    linarith
  · by_contra hnot
    have hge : g * A ≤ PC := le_of_not_gt hnot
    have hsqge : (g * A) ^ 2 ≤ PC ^ 2 := by
      nlinarith [sq_nonneg (PC - g * A)]
    linarith

/-- The algebraic Lyapunov-ledger consumer.  It keeps the positive-bias lane
explicit and only concludes nonincrease when that lane is nonpositive. -/
theorem cubic_energy_barrier_dissipation
    (A Z Zdot PC PR PB Lambda K kappaR : ℝ)
    (hA : 0 ≤ A) (hLambda : 0 ≤ Lambda)
    (hkappa1 : kappaR ≤ 1)
    (hledger : Zdot ≤ -A + PC + PR + PB)
    (hrel : PR ≤ kappaR * A)
    (hbias : PB ≤ 0)
    (hcoerce : A ≤ K * Z)
    (hcubic : PC ^ 2 ≤ Lambda * A ^ 3)
    (hbarrier : Lambda * K * Z ≤ (1 - kappaR) ^ 2) :
    Zdot ≤ 0 := by
  have hg : 0 ≤ 1 - kappaR := by linarith
  have habs := cubic_square_absorption_from_energy_barrier
    A Z PC Lambda K (1 - kappaR)
    hA hLambda hg hcoerce hcubic hbarrier
  have hPC : PC ≤ (1 - kappaR) * A := le_trans (le_abs_self PC) habs
  nlinarith

/-- Strict ledger version: inside a strict barrier, nonzero damping energy
forces strict decrease if the bias lane is nonpositive. -/
theorem cubic_energy_barrier_strict_dissipation
    (A Z Zdot PC PR PB Lambda K kappaR : ℝ)
    (hA : 0 < A) (hLambda : 0 ≤ Lambda)
    (hkappa1 : kappaR < 1)
    (hledger : Zdot ≤ -A + PC + PR + PB)
    (hrel : PR ≤ kappaR * A)
    (hbias : PB ≤ 0)
    (hcoerce : A ≤ K * Z)
    (hcubic : PC ^ 2 ≤ Lambda * A ^ 3)
    (hbarrier : Lambda * K * Z < (1 - kappaR) ^ 2) :
    Zdot < 0 := by
  have hg : 0 < 1 - kappaR := by linarith
  have habs := cubic_square_strict_absorption_from_energy_barrier
    A Z PC Lambda K (1 - kappaR)
    hA hLambda hg hcoerce hcubic hbarrier
  have hPC : PC ≤ |PC| := le_abs_self PC
  nlinarith

/-- Scalar coercivity bridge behind the review's `K = 2600000` value.  The
premise `(1/2000000) * normSq ≤ Z` is the regularizer kinetic lower bound, and
`A ≤ (13/10) * normSq` uses the largest current damping coefficient. -/
theorem regularizer_to_damping_coercivity
    (normSq A Z : ℝ)
    (hA : A ≤ (13 / 10 : ℝ) * normSq)
    (hkinetic : (1 / 2000000 : ℝ) * normSq ≤ Z) :
    A ≤ 2600000 * Z := by
  nlinarith

/-- Exact-real Fourier cubic coefficient from `h = 1/100000`. -/
def fdLambda (SF : ℝ) : ℝ :=
  SF / (144 * (100000 : ℝ) ^ 4)

/-- Exact simplification of `Lambda*K` for `K = 2600000`. -/
theorem fdLambda_mul_K_exact (SF : ℝ) :
    fdLambda SF * 2600000 = 13 * SF / 72000000000000000 := by
  norm_num [fdLambda]
  ring

/-- The review's division-free Fourier barrier implies the normalized
`Lambda*K*Z ≤ g^2` hypothesis consumed by the generic bootstrap theorem. -/
theorem fourier_barrier_from_division_free
    (SF Z g : ℝ)
    (hbarrier :
      13 * SF * Z ≤ 72000000000000000 * g ^ 2) :
    fdLambda SF * 2600000 * Z ≤ g ^ 2 := by
  rw [fdLambda_mul_K_exact]
  have hD : (0 : ℝ) < 72000000000000000 := by norm_num
  calc
    (13 * SF / 72000000000000000) * Z =
        (13 * SF * Z) / 72000000000000000 := by ring
    _ ≤ g ^ 2 := by
      apply (div_le_iff₀ hD).2
      simpa [mul_comm, mul_left_comm, mul_assoc] using hbarrier

/-- Final exact-real consumer for the one-scalar Fourier interface. -/
theorem fourier_cubic_absorption_from_division_free_barrier
    (A Z PC SF g : ℝ)
    (hA : 0 ≤ A) (hSF : 0 ≤ SF) (hg : 0 ≤ g)
    (hcoerce : A ≤ 2600000 * Z)
    (hcubic : PC ^ 2 ≤ fdLambda SF * A ^ 3)
    (hbarrier :
      13 * SF * Z ≤ 72000000000000000 * g ^ 2) :
    |PC| ≤ g * A := by
  have hLambda : 0 ≤ fdLambda SF := by
    dsimp [fdLambda]
    positivity
  apply cubic_square_absorption_from_energy_barrier
      A Z PC (fdLambda SF) 2600000 g
      hA hLambda hg hcoerce hcubic
  exact fourier_barrier_from_division_free SF Z g hbarrier

#print axioms abs_le_of_sq_le_sq_nonneg
#print axioms cubic_square_absorption_from_energy_barrier
#print axioms cubic_square_strict_absorption_from_energy_barrier
#print axioms cubic_energy_barrier_dissipation
#print axioms cubic_energy_barrier_strict_dissipation
#print axioms regularizer_to_damping_coercivity
#print axioms fdLambda_mul_K_exact
#print axioms fourier_barrier_from_division_free
#print axioms fourier_cubic_absorption_from_division_free_barrier

end

end RouteBP5CubicEnergyBarrier

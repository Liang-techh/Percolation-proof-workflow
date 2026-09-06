import Mathlib

set_option autoImplicit false
open scoped BigOperators

namespace RouteBTerminalGate
noncomputable section

/-- A bounded nonnegative polynomial family with powers 1 through 8.

The index `j` stores the coefficient of `(1 - t)^(j.val + 1)`, so
`a 0` is the coefficient called `a₁` and `a 7` is the coefficient called
`a₈`.  There is deliberately no constant term in this bounded family. -/
def decayPolynomial (a : Fin 8 → ℝ) (t : ℝ) : ℝ :=
  ∑ j, a j * (1 - t)^(j.val + 1)

def tailPolynomial (a : Fin 8 → ℝ) (t : ℝ) : ℝ :=
  ∑ j : Fin 7, a j.succ * (1 - t)^j.val

def NonnegativeCoefficients (a : Fin 8 → ℝ) : Prop :=
  ∀ j, 0 ≤ a j

def FirstCoefficientZero (a : Fin 8 → ℝ) : Prop :=
  a 0 = 0

theorem decayPolynomial_nonneg (a : Fin 8 → ℝ) (t : ℝ)
    (ha : NonnegativeCoefficients a) (ht : t ≤ 1) :
    0 ≤ decayPolynomial a t := by
  unfold decayPolynomial NonnegativeCoefficients at *
  exact Finset.sum_nonneg (fun j _ =>
    mul_nonneg (ha j) (pow_nonneg (sub_nonneg.mpr ht) _))

theorem decayPolynomial_terminal (a : Fin 8 → ℝ) :
    decayPolynomial a 1 = 0 := by
  simp [decayPolynomial]

/-- The `a₁ = 0` hypothesis has the exact finite algebraic consequence
`f(t) = (1-t)^2 * tailPolynomial(a,t)`.  This is the bounded substitute for
the analytic statement `f = o(1-t)`. -/
theorem decayPolynomial_factor (a : Fin 8 → ℝ) (t : ℝ)
    (ha1 : FirstCoefficientZero a) :
    decayPolynomial a t = (1 - t)^2 * tailPolynomial a t := by
  unfold decayPolynomial tailPolynomial FirstCoefficientZero at *
  simp only [Fin.sum_univ_succ, ha1, zero_mul, zero_add]
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j hj
  change a j.succ * (1 - t)^(j.val + 2) =
    (1 - t)^2 * (a j.succ * (1 - t)^j.val)
  rw [pow_add]
  ring

/-- The correction carried by the eighth terminal mode. -/
def terminalCorrection (a8 W0 Vd tau : ℝ) : ℝ :=
  a8 * (8 * tau^7 * W0 + tau^8 * Vd)

def terminalResidual (E a8 W0 Vd tau : ℝ) : ℝ :=
  E - terminalCorrection a8 W0 Vd tau

/-- A `b = 0` terminal gate is the nonpositive-residual requirement. -/
def bZeroGate (E a8 W0 Vd tau : ℝ) : Prop :=
  terminalResidual E a8 W0 Vd tau ≤ 0

def correctionFunction (a8 W0 Vd : ℝ) (t : ℝ) : ℝ :=
  terminalCorrection a8 W0 Vd (1 - t)

/-- Uniformity over a terminal neighborhood, with every interval hypothesis
made explicit. -/
def UniformBZeroGate (E : ℝ → ℝ) (a8 W0 Vd T : ℝ) : Prop :=
  ∀ t, T ≤ t → t ≤ 1 → E t ≤ correctionFunction a8 W0 Vd t

/-- A pointwise gate necessarily pays at least the eighth-mode correction. -/
theorem gate_implies_terminal_lower_bound
    (E a8 W0 Vd tau : ℝ) (hgate : bZeroGate E a8 W0 Vd tau) :
    E ≤ a8 * (8 * tau^7 * W0 + tau^8 * Vd) := by
  unfold bZeroGate terminalResidual terminalCorrection at hgate
  linarith

/-- Exact fixed-parameter obstruction requested in the prompt.

The polynomial hypotheses record the bounded nonnegative family and its
`a₁ = 0` terminal shape.  The conclusion is purely algebraic: a strict
positive residual excludes the `b = 0` gate. -/
theorem fixed_terminal_gate_failure
    (a : Fin 8 → ℝ) (E W0 Vd tau rho c : ℝ)
    (ha : NonnegativeCoefficients a)
    (ha1 : FirstCoefficientZero a)
    (htau : 0 ≤ tau) (htau_one : tau ≤ 1)
    (hrho : 0 < rho) (hc : 0 < c)
    (hE_floor : c * rho^4 ≤ E)
    (hgap : 0 < terminalResidual E (a 7) W0 Vd tau) :
    0 < E ∧ ¬ bZeroGate E (a 7) W0 Vd tau := by
  have hEpos : 0 < E := by
    exact lt_of_lt_of_le (mul_pos hc (pow_pos hrho 4)) hE_floor
  constructor
  · exact hEpos
  · intro hgate
    have hnecessary := gate_implies_terminal_lower_bound E (a 7) W0 Vd tau hgate
    unfold terminalResidual terminalCorrection at hgap
    linarith

def SourceQuarticFloor (E : ℝ → ℝ) (rho c T : ℝ) : Prop :=
  ∀ t, T ≤ t → t ≤ 1 → c * rho^4 ≤ E t

def SeventhOrderBound (C : ℝ → ℝ) (K T : ℝ) : Prop :=
  ∀ t, T ≤ t → t ≤ 1 → |C t| ≤ K * (1 - t)^7

/-- The order-aware fixed-neighborhood version.  `SourceQuarticFloor` and
`SeventhOrderBound` are hypotheses, so no unproved analytic asymptotic claim
is hidden in this theorem. -/
theorem no_uniform_bZero_gate_of_quartic_floor_and_seventh_order
    (a : Fin 8 → ℝ) (E : ℝ → ℝ) (W0 Vd rho c K T t0 : ℝ)
    (ha : NonnegativeCoefficients a)
    (ha1 : FirstCoefficientZero a)
    (hrho : 0 < rho) (hc : 0 < c)
    (hfloor : SourceQuarticFloor E rho c T)
    (horder : SeventhOrderBound (correctionFunction (a 7) W0 Vd) K T)
    (hT : T ≤ t0) (ht0 : t0 ≤ 1)
    (hsmall : K * (1 - t0)^7 < c * rho^4) :
    ¬ UniformBZeroGate E (a 7) W0 Vd T := by
  have hEfloor := hfloor t0 hT ht0
  have hcorrAbs := horder t0 hT ht0
  have hcorr : correctionFunction (a 7) W0 Vd t0 ≤
      K * (1 - t0)^7 := by
    exact le_trans (le_abs_self _) hcorrAbs
  intro huniform
  have hgate := huniform t0 hT ht0
  unfold correctionFunction terminalCorrection at hgate hcorr
  linarith

/-- The order-aware theorem exposes the exact residual gap at the selected
parameter, making the fixed algebraic obstruction reusable downstream. -/
theorem no_uniform_bZero_gate_of_strict_residual
    (a : Fin 8 → ℝ) (E : ℝ → ℝ) (W0 Vd T t0 : ℝ)
    (ha : NonnegativeCoefficients a)
    (ha1 : FirstCoefficientZero a)
    (hT : T ≤ t0) (ht0 : t0 ≤ 1)
    (hgap : 0 < E t0 -
      (a 7) * (8 * (1 - t0)^7 * W0 + (1 - t0)^8 * Vd)) :
    ¬ UniformBZeroGate E (a 7) W0 Vd T := by
  intro huniform
  have hgate := huniform t0 hT ht0
  unfold UniformBZeroGate correctionFunction terminalCorrection at hgate
  linarith

#print axioms decayPolynomial_nonneg
#print axioms decayPolynomial_terminal
#print axioms decayPolynomial_factor
#print axioms gate_implies_terminal_lower_bound
#print axioms fixed_terminal_gate_failure
#print axioms no_uniform_bZero_gate_of_quartic_floor_and_seventh_order
#print axioms no_uniform_bZero_gate_of_strict_residual

end
end RouteBTerminalGate

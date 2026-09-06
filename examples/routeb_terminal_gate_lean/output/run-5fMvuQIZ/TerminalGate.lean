import Mathlib.Data.Real.Basic
import Mathlib.Tactic

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

/-- The correction carried by the eighth terminal mode. -/
def terminalCorrection (a8 W0 Vd tau : ℝ) : ℝ :=
  a8 * (8 * tau^7 * W0 + tau^8 * Vd)

def terminalResidual (E a8 W0 Vd tau : ℝ) : ℝ :=
  E - terminalCorrection a8 W0 Vd tau

def terminalVdot (a8 W0 Vd tau : ℝ) : ℝ :=
  -terminalCorrection a8 W0 Vd tau

def terminalSupply (E a8 W0 Vd tau : ℝ) : ℝ :=
  E + terminalVdot a8 W0 Vd tau

def QuadNonnegative (x : ℝ) : Prop :=
  0 ≤ x

/-- A `b = 0` terminal gate is nonnegative available supply, equivalently
the nonpositive-residual requirement. -/
def zeroSupplyGate (E a8 W0 Vd tau : ℝ) : Prop :=
  QuadNonnegative (-terminalSupply E a8 W0 Vd tau)

def bZeroGate (E a8 W0 Vd tau : ℝ) : Prop :=
  zeroSupplyGate E a8 W0 Vd tau

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
  unfold bZeroGate zeroSupplyGate QuadNonnegative terminalSupply terminalVdot
    terminalCorrection at hgate
  linarith

/-- Exact fixed-parameter obstruction requested in the prompt.

The polynomial hypotheses record the bounded nonnegative family and its
`a₁ = 0` terminal shape.  The conclusion is purely algebraic: a strict
positive residual excludes the `b = 0` gate. -/
theorem fixed_terminal_gate_failure
    (a : Fin 8 → ℝ) (E W0 Vd tau rho c : ℝ)
    (_ha : NonnegativeCoefficients a)
    (_ha1 : FirstCoefficientZero a)
    (_htau : 0 ≤ tau) (_htau_one : tau ≤ 1)
    (hrho : 0 < rho) (hc : 0 < c)
    (hE_floor : c * rho^4 ≤ E)
    (hgap : 0 < terminalResidual E (a 7) W0 Vd tau) :
    0 < E ∧
      ¬ QuadNonnegative (-terminalSupply E (a 7) W0 Vd tau) ∧
      ¬ bZeroGate E (a 7) W0 Vd tau := by
  have hEpos : 0 < E := by
    exact lt_of_lt_of_le (mul_pos hc (pow_pos hrho 4)) hE_floor
  constructor
  · exact hEpos
  · constructor
    · intro hq
      unfold QuadNonnegative terminalSupply terminalVdot at hq
      unfold terminalResidual terminalCorrection at hgap
      linarith
    · intro hgate
      have hnecessary := gate_implies_terminal_lower_bound E (a 7) W0 Vd tau hgate
      unfold terminalResidual terminalCorrection at hgap
      linarith

/-- The order-aware theorem exposes the exact residual gap at the selected
parameter, making the fixed algebraic obstruction reusable downstream. -/
theorem no_uniform_bZero_gate_of_strict_residual
    (a : Fin 8 → ℝ) (E : ℝ → ℝ) (W0 Vd T t0 : ℝ)
    (_ha : NonnegativeCoefficients a)
    (_ha1 : FirstCoefficientZero a)
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
#print axioms gate_implies_terminal_lower_bound
#print axioms fixed_terminal_gate_failure
#print axioms no_uniform_bZero_gate_of_strict_residual

end
end RouteBTerminalGate

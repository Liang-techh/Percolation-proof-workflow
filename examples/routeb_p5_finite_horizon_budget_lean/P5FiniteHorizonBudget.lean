import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P5 finite-horizon mixed energy-budget sidecar

This file formalizes the source-independent pointwise algebra from
`review-T-P5-013-honglianmozun-20260907T0358.md`.

It deliberately stops before the calculus/ODE first-exit argument.  In
particular it does not prove source binding, Float64/IEEE bounds, P8 graph-domain
coverage, ODE existence/continuation, or P5/M4 admission.
-/

set_option autoImplicit false

namespace RouteBP5FiniteHorizonBudget

noncomputable section

/-- Nonnegative square domination gives an absolute-value bound. -/
theorem abs_le_of_sq_le_sq_nonneg
    (x y : ℝ) (hy : 0 ≤ y) (hxy : x ^ 2 ≤ y ^ 2) :
    |x| ≤ y := by
  rw [abs_le]
  constructor <;> nlinarith [sq_nonneg (x + y), sq_nonneg (x - y)]

/-- The square-only cubic absorption used by the mixed finite-horizon ledger.
This is the same source-independent algebraic interface as T-P5-011, repeated
here so this sidecar remains portable and does not depend on a sibling example
module being on `LEAN_PATH`. -/
theorem cubic_absorption_from_energy_barrier
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

/-- Division-free weighted-dual work charging.  The premise
`P^2 ≤ R*A` is the inverse-free consumer form of weighted Cauchy, while
`R ≤ 4*gR*BR` charges the nonconservative remainder to the chosen energy-rate
budget `BR`. -/
theorem dual_work_budget
    (A P R gR BR : ℝ)
    (hA : 0 ≤ A) (hgR : 0 < gR) (hBR : 0 ≤ BR)
    (hP : P ^ 2 ≤ R * A)
    (hcap : R ≤ 4 * gR * BR) :
    P ≤ gR * A + BR := by
  have hgR0 : 0 ≤ gR := le_of_lt hgR
  have hRA : R * A ≤ (4 * gR * BR) * A :=
    mul_le_mul_of_nonneg_right hcap hA
  have hyoung : 4 * gR * BR * A ≤ (gR * A + BR) ^ 2 := by
    nlinarith [sq_nonneg (gR * A - BR)]
  have hsq : P ^ 2 ≤ (gR * A + BR) ^ 2 := by
    calc
      P ^ 2 ≤ R * A := hP
      _ ≤ (4 * gR * BR) * A := hRA
      _ = 4 * gR * BR * A := by ring
      _ ≤ (gR * A + BR) ^ 2 := hyoung
  have htarget : 0 ≤ gR * A + BR :=
    add_nonneg (mul_nonneg hgR0 hA) hBR
  exact le_trans (le_abs_self P)
    (abs_le_of_sq_le_sq_nonneg P (gR * A + BR) htarget hsq)

/-- Pointwise mixed P5 ledger.  The damping margin is split into `gC` for the
central-FD cubic power and `gR` for a genuine nonconservative remainder.  A
one-sided ramp-work cap is sufficient. -/
theorem mixed_energy_rate
    (A Z Zdot PC PR hRamp Lambda K gC gR R BR Hbar : ℝ)
    (hA : 0 ≤ A) (hLambda : 0 ≤ Lambda) (hgC : 0 ≤ gC)
    (hgR : 0 < gR) (hBR : 0 ≤ BR)
    (hcoerce : A ≤ K * Z)
    (hcubic : PC ^ 2 ≤ Lambda * A ^ 3)
    (hbarrier : Lambda * K * Z ≤ gC ^ 2)
    (hdual : PR ^ 2 ≤ R * A)
    (hRcap : R ≤ 4 * gR * BR)
    (hramp : hRamp ≤ Hbar)
    (hledger :
      Zdot ≤ -(gC + gR) * A + PC + PR + hRamp) :
    Zdot ≤ Hbar + BR := by
  have hPCabs := cubic_absorption_from_energy_barrier
    A Z PC Lambda K gC hA hLambda hgC hcoerce hcubic hbarrier
  have hPC : PC ≤ gC * A := le_trans (le_abs_self PC) hPCabs
  have hPR := dual_work_budget A PR R gR BR hA hgR hBR hdual hRcap
  linarith

/-- Once a calculus layer has established linear growth, strict headroom at the
horizon immediately implies strict sublevel retention at every earlier time. -/
theorem linear_growth_stays_below_barrier
    (t T Zt Z0 B Zstar : ℝ)
    (ht0 : 0 ≤ t) (htT : t ≤ T) (hB : 0 ≤ B)
    (hgrowth : Zt ≤ Z0 + t * B)
    (hheadroom : Z0 + T * B < Zstar) :
    Zt < Zstar := by
  have htime : t * B ≤ T * B :=
    mul_le_mul_of_nonneg_right htT hB
  linarith

/-- Exact `T=1`, 50/50 damping-split checker-facing rational criterion from
T-P5-013.  No square root is introduced.  Positivity of `SF` and `g0` is made
explicit because the displayed headroom formula divides by both. -/
theorem t1_fifty_fifty_headroom_from_rational
    (SF g0 Z0 Hbar Rbar : ℝ)
    (hSF : 0 < SF) (hg0 : 0 < g0)
    (hcrit :
      26 * SF * g0 * (Z0 + Hbar) + 13 * SF * Rbar <
        36000000000000000 * g0 ^ 3) :
    Z0 + Hbar + Rbar / (2 * g0) <
      (18000000000000000 * g0 ^ 2) / (13 * SF) := by
  have hdenSF : 0 < 13 * SF := by positivity
  have hdenG : 0 < 2 * g0 := by positivity
  apply (lt_div_iff₀ hdenSF).2
  have hscaled :
      (2 * g0) *
          ((Z0 + Hbar + Rbar / (2 * g0)) * (13 * SF)) <
        (2 * g0) * (18000000000000000 * g0 ^ 2) := by
    calc
      (2 * g0) *
          ((Z0 + Hbar + Rbar / (2 * g0)) * (13 * SF)) =
          26 * SF * g0 * (Z0 + Hbar) + 13 * SF * Rbar := by
            field_simp [ne_of_gt hg0]
            <;> ring
      _ < 36000000000000000 * g0 ^ 3 := hcrit
      _ = (2 * g0) * (18000000000000000 * g0 ^ 2) := by ring
  exact (mul_lt_mul_left hdenG).mp hscaled

/-- The available one-sided storage coercivity `A ≤ K*Z` cannot by itself be
turned into a negative multiple of positive storage.  This concrete witness is
kept as a kernel-checked failure boundary for asymptotic overclaims. -/
theorem upper_storage_coercivity_counterexample :
    ∃ (A Z K : ℝ),
      0 ≤ A ∧ 0 < Z ∧ A ≤ K * Z ∧
      ∀ alpha : ℝ, 0 < alpha → ¬ (-A ≤ -alpha * Z) := by
  refine ⟨0, 1, 1, by norm_num, by norm_num, by norm_num, ?_⟩
  intro alpha halpha hfalse
  norm_num at hfalse
  linarith

#print axioms abs_le_of_sq_le_sq_nonneg
#print axioms cubic_absorption_from_energy_barrier
#print axioms dual_work_budget
#print axioms mixed_energy_rate
#print axioms linear_growth_stays_below_barrier
#print axioms t1_fifty_fifty_headroom_from_rational
#print axioms upper_storage_coercivity_counterexample

end

end RouteBP5FiniteHorizonBudget

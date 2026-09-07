import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P5 block-(4,5) exact 15/16 SOS sidecar

Source-independent Lean decomposition of
`agent_review_inbox/review-T-P5-034-honglianmozun-20260907T1701.md`.

This file freezes the same exact block-(4,5) storage `V45` and dissipation
`Q45` used by T-P5-019/T-P5-033, proves the weighted nine-square identity
`Q45 - (15/16) * V45 = SOS`, derives `Q45 >= (15/16) * V45`, records the
exact rational counterexample forbidding the rounded-up `47/50` claim, and
checks only the downstream scalar arithmetic consumers whose constants change.

It does not prove any source residual bound, Float64/true-DH semantics,
trajectory/ODE coverage, first-exit packaging, provenance/admission, or final
P5/M4 integration.
-/

set_option autoImplicit false

namespace RouteBP5Block45FifteenSixteenSOS

noncomputable section

/-- Exact block-(4,5) storage from T-P5-019/T-P5-033/T-P5-034. -/
def V45 (x4 x5 y4 y5 : ℝ) : ℝ :=
  (1 / 2 : ℝ) *
      ((350003 / 3000000 : ℝ) * y4^2 + (200739 / 4000000 : ℝ) * y5^2) +
    (1 / 2 : ℝ) *
      ((3 / 4 : ℝ) * x4^2 - (3 / 200 : ℝ) * x4 * x5 +
        (29 / 50 : ℝ) * x5^2) +
    (350003 / 3000000 : ℝ) * x4 * y4 +
    (200739 / 4000000 : ℝ) * x5 * y5 +
    (1 / 2 : ℝ) *
      ((4 / 5 : ℝ) * x4^2 + (13 / 20 : ℝ) * x5^2)

/-- Exact block-(4,5) dissipation from T-P5-019/T-P5-033/T-P5-034. -/
def Q45 (x4 x5 y4 y5 : ℝ) : ℝ :=
  ((4 / 5 : ℝ) - (350003 / 3000000 : ℝ)) * y4^2 +
    ((13 / 20 : ℝ) - (200739 / 4000000 : ℝ)) * y5^2 +
    (3 / 4 : ℝ) * x4^2 - (3 / 200 : ℝ) * x4 * x5 +
    (29 / 50 : ℝ) * x5^2 -
    (1 / 400 : ℝ) * y4 * x5 + (1 / 400 : ℝ) * y5 * x4

/-- Exact weighted nine-square identity supplied by T-P5-034. -/
theorem block45_Q_minus_15_16_V_sos
    (x4 x5 y4 y5 : ℝ) :
    Q45 x4 x5 y4 y5 - (15 / 16 : ℝ) * V45 x4 x5 y4 y5 =
        (270997 / 64000000 : ℝ) * x4^2
      + (2073349 / 1740800000 : ℝ) * x5^2
      + (3769409 / 96000000 : ℝ) * y4^2
      + (13342021 / 384000000 : ℝ) * y5^2
      + (867 / 64000 : ℝ) * (x4 - (5 / 17 : ℝ) * x5)^2
      + (350003 / 64000000 : ℝ) * (x4 - 10 * y4)^2
      + (3 / 16000 : ℝ) * (x4 + (20 / 3 : ℝ) * y5)^2
      + (1 / 27200 : ℝ) * (x5 - 34 * y4)^2
      + (1806651 / 1740800000 : ℝ) * (x5 - (68 / 3 : ℝ) * y5)^2 := by
  simp [Q45, V45]
  ring

/-- The weighted SOS identity yields `Q45 >= (15/16) V45`. -/
theorem block45_Q_ge_15_16_V
    (x4 x5 y4 y5 : ℝ) :
    (15 / 16 : ℝ) * V45 x4 x5 y4 y5 ≤ Q45 x4 x5 y4 y5 := by
  have hsos :
      0 ≤ Q45 x4 x5 y4 y5 - (15 / 16 : ℝ) * V45 x4 x5 y4 y5 := by
    rw [block45_Q_minus_15_16_V_sos]
    positivity
  linarith

/-- Exact rational nearby obstruction recorded by T-P5-034. -/
theorem block45_47_50_gap_at_z0 :
    Q45 1 (25 / 6 : ℝ) (1 / 10 : ℝ) (1 / 6 : ℝ) -
        (47 / 50 : ℝ) * V45 1 (25 / 6 : ℝ) (1 / 10 : ℝ) (1 / 6 : ℝ) =
      -(83857069 / 120000000000 : ℝ) := by
  norm_num [Q45, V45]

/-- Therefore the tempting rounded-up coercivity `Q >= (47/50)V` is false
for the frozen block, already at the exact rational witness `z0`. -/
theorem block45_not_ge_47_50_V_at_z0 :
    ¬ ((47 / 50 : ℝ) * V45 1 (25 / 6 : ℝ) (1 / 10 : ℝ) (1 / 6 : ℝ) ≤
      Q45 1 (25 / 6 : ℝ) (1 / 10 : ℝ) (1 / 6 : ℝ)) := by
  norm_num [Q45, V45]

/-- Abstract downstream ledger replacement: once the unchanged residual Young
step has produced `Vdot <= -Q/2 + 17 L2/10`, the new coercivity replaces only
the `Q -> V` constant. -/
theorem lyapunov_ledger_of_15_16_coercivity
    (Vdot V Q L2 : ℝ)
    (hQV : (15 / 16 : ℝ) * V ≤ Q)
    (hledger : Vdot ≤ -(1 / 2 : ℝ) * Q + (17 / 10 : ℝ) * L2) :
    Vdot ≤ -(15 / 32 : ℝ) * V + (17 / 10 : ℝ) * L2 := by
  linarith

/-- Concrete block-(4,5) specialization of the improved residual-coupled
Lyapunov ledger. -/
theorem block45_lyapunov_ledger
    (x4 x5 y4 y5 Vdot L2 : ℝ)
    (hledger :
      Vdot ≤ -(1 / 2 : ℝ) * Q45 x4 x5 y4 y5 + (17 / 10 : ℝ) * L2) :
    Vdot ≤
      -(15 / 32 : ℝ) * V45 x4 x5 y4 y5 + (17 / 10 : ℝ) * L2 := by
  exact lyapunov_ledger_of_15_16_coercivity
    Vdot (V45 x4 x5 y4 y5) (Q45 x4 x5 y4 y5) L2
    (block45_Q_ge_15_16_V x4 x5 y4 y5) hledger

/-- Division-free `Vstar=1/4` checker gate from T-P5-034. -/
theorem quarter_barrier_gate
    (L2 : ℝ) (hgate : 1088 * L2 < 75) :
    (17 / 10 : ℝ) * L2 < (15 / 32 : ℝ) * (1 / 4 : ℝ) := by
  norm_num at hgate ⊢
  linarith

/-- Division-free `Kc=1/12` incremental-tube checker gate from T-P5-034. -/
theorem incremental_Kc_one_twelfth_gate
    (mu nu : ℝ) (hgate : 272 * mu + 3264 * nu < 75) :
    (17 / 10 : ℝ) * (mu * (1 / 12 : ℝ) + nu) <
      (15 / 32 : ℝ) * (1 / 12 : ℝ) := by
  norm_num at hgate ⊢
  linarith

/-- Exact capacity improvement factor relative to T-P5-033. -/
theorem exact_capacity_improvement_over_93_100 :
    ((15 / 32 : ℝ) / (93 / 200 : ℝ)) = 125 / 124 := by
  norm_num

/-- Exact constant-residual ultimate coefficient for the new ledger. -/
theorem ultimate_residual_coefficient :
    ((17 / 10 : ℝ) / (15 / 32 : ℝ)) = 272 / 75 := by
  norm_num

#print axioms block45_Q_minus_15_16_V_sos
#print axioms block45_Q_ge_15_16_V
#print axioms block45_47_50_gap_at_z0
#print axioms block45_not_ge_47_50_V_at_z0
#print axioms lyapunov_ledger_of_15_16_coercivity
#print axioms block45_lyapunov_ledger
#print axioms quarter_barrier_gate
#print axioms incremental_Kc_one_twelfth_gate
#print axioms exact_capacity_improvement_over_93_100
#print axioms ultimate_residual_coefficient

end

end RouteBP5Block45FifteenSixteenSOS

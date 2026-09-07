import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P5 block-(4,5) exact 93/100 SOS sidecar

Source-independent Lean decomposition of
`agent_review_inbox/review-T-P5-033-honglianmozun-20260907T1604.md`.

This file freezes the exact block-(4,5) storage `V45` and dissipation `Q45`,
proves the weighted nine-square identity
`Q45 - (93/100) * V45 = SOS`, derives `Q45 >= (93/100) * V45`, and records
only the downstream scalar arithmetic consumers whose constants change.

It does not prove any source residual bound, Float64/true-DH semantics,
trajectory/ODE coverage, first-exit packaging, provenance/admission, or final
P5/M4 integration.
-/

set_option autoImplicit false

namespace RouteBP5Block45NinetyThreeSOS

noncomputable section

/-- Exact block-(4,5) storage from T-P5-019/T-P5-032/T-P5-033. -/
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

/-- Exact block-(4,5) dissipation from T-P5-019/T-P5-032/T-P5-033. -/
def Q45 (x4 x5 y4 y5 : ℝ) : ℝ :=
  ((4 / 5 : ℝ) - (350003 / 3000000 : ℝ)) * y4^2 +
    ((13 / 20 : ℝ) - (200739 / 4000000 : ℝ)) * y5^2 +
    (3 / 4 : ℝ) * x4^2 - (3 / 200 : ℝ) * x4 * x5 +
    (29 / 50 : ℝ) * x5^2 -
    (1 / 400 : ℝ) * y4 * x5 + (1 / 400 : ℝ) * y5 * x4

/-- Exact weighted nine-square identity supplied by T-P5-033. -/
theorem block45_Q_minus_93_100_V_sos
    (x4 x5 y4 y5 : ℝ) :
    Q45 x4 x5 y4 y5 - (93 / 100 : ℝ) * V45 x4 x5 y4 y5 =
        (3542407 / 600000000 : ℝ) * x4^2
      + (155697 / 800000000 : ℝ) * x5^2
      + (69762071 / 150000000 : ℝ) * y4^2
      + (29216493 / 80000000 : ℝ) * y5^2
      + (321 / 80000 : ℝ) * (x4 - x5)^2
      + (10850093 / 600000000 : ℝ) * (x4 - 3 * y4)^2
      + (1 / 800 : ℝ) * (x4 + y5)^2
      + (1 / 800 : ℝ) * (x5 - y4)^2
      + (18668727 / 7200000000 : ℝ) * (x5 - 9 * y5)^2 := by
  simp [Q45, V45]
  ring

/-- The nine-square identity yields the strengthened coercivity
`Q45 >= (93/100) V45` with no matrix-positivity API. -/
theorem block45_Q_ge_93_100_V
    (x4 x5 y4 y5 : ℝ) :
    (93 / 100 : ℝ) * V45 x4 x5 y4 y5 ≤ Q45 x4 x5 y4 y5 := by
  have hsos :
      0 ≤ Q45 x4 x5 y4 y5 - (93 / 100 : ℝ) * V45 x4 x5 y4 y5 := by
    rw [block45_Q_minus_93_100_V_sos]
    positivity
  linarith

/-- Abstract downstream ledger replacement: once the unchanged residual Young
step has produced `Vdot <= -Q/2 + 17 L2/10`, the new coercivity replaces only
the `Q -> V` constant. -/
theorem lyapunov_ledger_of_93_100_coercivity
    (Vdot V Q L2 : ℝ)
    (hQV : (93 / 100 : ℝ) * V ≤ Q)
    (hledger : Vdot ≤ -(1 / 2 : ℝ) * Q + (17 / 10 : ℝ) * L2) :
    Vdot ≤ -(93 / 200 : ℝ) * V + (17 / 10 : ℝ) * L2 := by
  linarith

/-- Concrete block-(4,5) specialization of the improved residual-coupled
Lyapunov ledger. -/
theorem block45_lyapunov_ledger
    (x4 x5 y4 y5 Vdot L2 : ℝ)
    (hledger :
      Vdot ≤ -(1 / 2 : ℝ) * Q45 x4 x5 y4 y5 + (17 / 10 : ℝ) * L2) :
    Vdot ≤
      -(93 / 200 : ℝ) * V45 x4 x5 y4 y5 + (17 / 10 : ℝ) * L2 := by
  exact lyapunov_ledger_of_93_100_coercivity
    Vdot (V45 x4 x5 y4 y5) (Q45 x4 x5 y4 y5) L2
    (block45_Q_ge_93_100_V x4 x5 y4 y5) hledger

/-- Division-free quarter-barrier checker gate from T-P5-033. -/
theorem quarter_barrier_gate
    (L2 : ℝ) (hgate : 1360 * L2 < 93) :
    (17 / 10 : ℝ) * L2 < (93 / 200 : ℝ) * (1 / 4 : ℝ) := by
  norm_num at hgate ⊢
  linarith

/-- Division-free `Kc=1/12` incremental-tube checker gate from T-P5-033. -/
theorem incremental_Kc_one_twelfth_gate
    (mu nu : ℝ) (hgate : 340 * mu + 4080 * nu < 93) :
    (17 / 10 : ℝ) * (mu * (1 / 12 : ℝ) + nu) <
      (93 / 200 : ℝ) * (1 / 12 : ℝ) := by
  norm_num at hgate ⊢
  linarith

/-- Exact improvement factor relative to the previous `8/9` consumer. -/
theorem exact_capacity_improvement_ratio :
    ((93 / 200 : ℝ) / (4 / 9 : ℝ)) = 837 / 800 := by
  norm_num

/-- Exact ultimate residual coefficient and the strict comparison recorded by
T-P5-033. -/
theorem ultimate_residual_coefficient :
    ((17 / 10 : ℝ) / (93 / 200 : ℝ)) = 340 / 93 ∧
    (340 / 93 : ℝ) < 153 / 40 := by
  norm_num

#print axioms block45_Q_minus_93_100_V_sos
#print axioms block45_Q_ge_93_100_V
#print axioms lyapunov_ledger_of_93_100_coercivity
#print axioms block45_lyapunov_ledger
#print axioms quarter_barrier_gate
#print axioms incremental_Kc_one_twelfth_gate
#print axioms exact_capacity_improvement_ratio
#print axioms ultimate_residual_coefficient

end

end RouteBP5Block45NinetyThreeSOS

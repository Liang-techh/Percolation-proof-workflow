import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
T-P5-030 -- UNCOMPILED SOURCE-INDEPENDENT ALGEBRA SKELETON.
No Lean/Lake execution or kernel-verification claim for this file.
Only initial-energy arithmetic and pointwise boundary algebra; no ODE,
first-exit, continuation, physical source, residual, or coverage instance.
-/

set_option autoImplicit false

namespace RouteBP5030ISSBoundary

def C0 : ℚ := 474733828336525417 / 5726342542105201000

theorem initial_coefficient_rational :
    0 < C0 ∧ C0 < (1 / 12 : ℚ) := by norm_num [C0]

theorem initial_margin_rational :
    (1 / 12 : ℚ) - C0 = 7384150516723999 / 17179027626315603000 := by
  norm_num [C0]

noncomputable section

def h4 : ℝ := 2340 / 8699
def h5 : ℝ := 1520 / 8699
def r4 : ℝ := -21912800 / 75672601
def r5 : ℝ := -15007200 / 75672601

/-- Declared T-P5-030 storage polynomial, in order X4,X5,Y4,Y5.
This definition does not identify any deployed trajectory's physical storage. -/
def storage (X4 X5 Y4 Y5 : ℝ) : ℝ :=
  (1 / 2 : ℝ) * ((350003 / 3000000 : ℝ) * Y4^2 +
    (200739 / 4000000 : ℝ) * Y5^2) +
  (1 / 2 : ℝ) * ((3 / 4 : ℝ) * X4^2 -
    (3 / 200 : ℝ) * X4 * X5 + (29 / 50 : ℝ) * X5^2) +
  (350003 / 3000000 : ℝ) * X4 * Y4 +
  (200739 / 4000000 : ℝ) * X5 * Y5 +
  (1 / 2 : ℝ) * ((4 / 5 : ℝ) * X4^2 + (13 / 20 : ℝ) * X5^2)

/-- Exact substitution only. Equal-physical-state initialization and each
trajectory's own moving-frame identities remain external premises. -/
theorem initial_energy_identity (dc : ℝ) :
    storage (-r4 * dc) (-r5 * dc) (-h4 * dc) (-h5 * dc) = (C0 : ℝ) * dc^2 := by
  norm_num [storage, r4, r5, h4, h5, C0]
  <;> ring

theorem initial_strict_of_identity (dc V0 : ℝ) (hdc : dc ≠ 0)
    (hinit : V0 = (C0 : ℝ) * dc^2) : V0 < dc^2 / 12 := by
  have hc : (C0 : ℝ) < (1 / 12 : ℝ) := by norm_num [C0]
  have hs : 0 < dc^2 := sq_pos_of_ne_zero hdc
  calc
    V0 = (C0 : ℝ) * dc^2 := hinit
    _ < (1 / 12 : ℝ) * dc^2 := mul_lt_mul_of_pos_right hc hs
    _ = dc^2 / 12 := by ring

theorem initialized_storage_strict (dc : ℝ) (hdc : dc ≠ 0) :
    storage (-r4 * dc) (-r5 * dc) (-h4 * dc) (-h5 * dc) < dc^2 / 12 :=
  initial_strict_of_identity dc _ hdc (initial_energy_identity dc)

def damping (mu : ℝ) : ℝ := (457 / 1344 : ℝ) - (17 / 10 : ℝ) * mu
def budgetMargin (mu nu : ℝ) : ℝ := 2285 - 11424 * mu - 137088 * nu

structure ParameterGate (mu nu : ℝ) : Prop where
  mu_nonnegative : 0 ≤ mu
  nu_nonnegative : 0 ≤ nu
  strict_budget : 11424 * mu + 137088 * nu < 2285

/-- dc2 is an abstract squared-width input. It must be strictly positive in
the boundary theorem. dV is a scalar with an externally supplied derivative meaning. -/
def ISSAt (mu nu dc2 V dV : ℝ) : Prop :=
  dV ≤ -damping mu * V + (17 / 10 : ℝ) * nu * dc2

/-- L2 stands for an actual incremental residual square only after external
source identification; neither an absolute residual cap nor a JSON flag suffices. -/
theorem incremental_residual_ledger (mu nu dc2 V dV L2 : ℝ)
    (hiss : dV ≤ -(457 / 1344 : ℝ) * V + (17 / 10 : ℝ) * L2)
    (hres : L2 ≤ mu * V + nu * dc2) : ISSAt mu nu dc2 V dV := by
  unfold ISSAt damping
  nlinarith

theorem margin_positive {mu nu : ℝ} (gate : ParameterGate mu nu) :
    0 < budgetMargin mu nu := by
  unfold budgetMargin
  linarith [gate.strict_budget]

/-- nu>=0 makes the single gate imply positive homogeneous damping as well. -/
theorem damping_positive {mu nu : ℝ} (gate : ParameterGate mu nu) :
    0 < damping mu := by
  unfold damping
  linarith [gate.strict_budget, gate.nu_nonnegative]

/-- Exact cleared-denominator identity at the tube BOUNDARY, not in its interior. -/
theorem boundary_rhs_identity (mu nu dc2 : ℝ) :
    -damping mu * (dc2 / 12) + (17 / 10 : ℝ) * nu * dc2 =
      -(budgetMargin mu nu * dc2) / 80640 := by
  unfold damping budgetMargin
  ring

theorem boundary_derivative_bound (mu nu dc2 V dV : ℝ)
    (hledger : ISSAt mu nu dc2 V dV) (hboundary : V = dc2 / 12) :
    dV ≤ -(budgetMargin mu nu * dc2) / 80640 := by
  calc
    dV ≤ -damping mu * (dc2 / 12) + (17 / 10 : ℝ) * nu * dc2 := by
      simpa only [ISSAt, hboundary] using hledger
    _ = _ := boundary_rhs_identity mu nu dc2

theorem twelfth_boundary_strict {mu nu dc2 V dV : ℝ}
    (gate : ParameterGate mu nu) (hwidth : 0 < dc2)
    (hledger : ISSAt mu nu dc2 V dV) (hboundary : V = dc2 / 12) : dV < 0 := by
  have hp : 0 < budgetMargin mu nu * dc2 := mul_pos (margin_positive gate) hwidth
  have hnegative : -(budgetMargin mu nu * dc2) / 80640 < 0 :=
    div_neg_of_neg_of_pos (neg_neg_of_pos hp) (by norm_num)
  exact lt_of_le_of_lt (boundary_derivative_bound mu nu dc2 V dV hledger hboundary) hnegative

/-- Final algebraic consumer: strict initialization plus strict inward boundary
derivative. The conjunction is NOT a theorem of trajectory/tube invariance. -/
theorem initial_and_boundary {mu nu dc V0 V dV L2 : ℝ}
    (gate : ParameterGate mu nu) (hdc : dc ≠ 0)
    (hinit : V0 = (C0 : ℝ) * dc^2)
    (hiss : dV ≤ -(457 / 1344 : ℝ) * V + (17 / 10 : ℝ) * L2)
    (hres : L2 ≤ mu * V + nu * dc^2)
    (hboundary : V = dc^2 / 12) : V0 < dc^2 / 12 ∧ dV < 0 := by
  constructor
  · exact initial_strict_of_identity dc V0 hdc hinit
  · exact twelfth_boundary_strict gate (sq_pos_of_ne_zero hdc)
      (incremental_residual_ledger mu nu (dc^2) V dV L2 hiss hres) hboundary

/-- At zero width the hypotheses permit a zero derivative. Strict negativity
cannot be extended to dc=0 from this algebra alone, even with an admissible gate. -/
theorem zero_width_boundary (mu nu : ℝ) :
    ISSAt mu nu 0 0 0 ∧ ¬ ((0 : ℝ) < 0) := by
  simp [ISSAt]

end

-- Future audit commands only; NOT executed in this round.
#print axioms initial_coefficient_rational
#print axioms initial_margin_rational
#print axioms initial_energy_identity
#print axioms initialized_storage_strict
#print axioms incremental_residual_ledger
#print axioms damping_positive
#print axioms boundary_rhs_identity
#print axioms twelfth_boundary_strict
#print axioms initial_and_boundary
#print axioms zero_width_boundary

end RouteBP5030ISSBoundary

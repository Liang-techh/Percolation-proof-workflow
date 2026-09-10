import Mathlib.Data.Real.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBM4CrossBranchBudget

/-!
Pure arithmetic child for T-M4-007.  It transfers a conditional P7 tail
charge into the improved M4 residual window.  The hypotheses are deliberately
typed inputs: this file does not prove the P7 integral estimate, the P8 ramp
identity, physical source binding, coverage, or terminal semantics.
-/

noncomputable def D_old : ℝ := 4483 / 2000
noncomputable def D_new : ℝ := 1401 / 625

theorem exact_gate_gap : D_new - D_old = (1 / 10000 : ℝ) := by
  norm_num [D_old, D_new]

theorem old_gate_tail_transfer
    (D_base rho_bar D_tail D_total : ℝ)
    (hbase : D_base ≤ D_old)
    (_hrho_nonneg : 0 ≤ rho_bar)
    (hrho : rho_bar ≤ 16)
    (htail : D_tail ≤ rho_bar / 160000)
    (htotal : D_total ≤ D_base + D_tail) :
    D_total ≤ D_new := by
  norm_num [D_old, D_new] at hbase hrho htail htotal ⊢
  linarith

theorem slack_tail_transfer
    (D_base rho_bar D_tail D_total : ℝ)
    (_hrho_nonneg : 0 ≤ rho_bar)
    (hslack : rho_bar ≤ 160000 * (D_new - D_base))
    (htail : D_tail ≤ rho_bar / 160000)
    (htotal : D_total ≤ D_base + D_tail) :
    D_total ≤ D_new := by
  have htail_budget : D_tail ≤ D_new - D_base := by
    have hscale : rho_bar / 160000 ≤ D_new - D_base := by
      nlinarith
    linarith
  linarith

#print axioms exact_gate_gap
#print axioms old_gate_tail_transfer
#print axioms slack_tail_transfer

end RouteBM4CrossBranchBudget

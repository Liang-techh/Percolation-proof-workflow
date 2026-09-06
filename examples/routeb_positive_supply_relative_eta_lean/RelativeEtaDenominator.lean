import Mathlib.Data.Real.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBPositiveSupplyRelativeEta
noncomputable section

/-! Exact constants for the frozen `(e₄+e₅)` scalar slice. -/

def A : ℝ := 2002229 / 24000000

def D : ℝ := 29 / 20

def K : ℝ := 36802229 / 24000000

theorem K_eq_A_add_D : K = A + D := by
  norm_num [K, A, D]

theorem A_pos : 0 < A := by
  norm_num [A]

theorem D_pos : 0 < D := by
  norm_num [D]

/-! The endpoint value `K=A+D` gives a positive affine margin on the
    whole interval `0 ≤ tau ≤ 1`.  The proof uses the convex decomposition
    `(1-tau) A + tau (A+D-kappa)`, so it does not rely on nonlinear
    automation to infer a product-sign fact. -/

theorem affine_margin_pos
    (tau kappa : ℝ)
    (htau0 : 0 ≤ tau)
    (htau1 : tau ≤ 1)
    (hkappa : kappa < K) :
    0 < A + tau * D - tau * kappa := by
  have hA : 0 < A := A_pos
  have hendpoint : 0 < A + D - kappa := by
    rw [← K_eq_A_add_D]
    linarith
  by_cases htau : tau = 0
  · subst tau
    simpa using hA
  · have htau_pos : 0 < tau := by
      exact lt_of_le_of_ne htau0 (by
        intro hzero
        exact htau hzero.symm)
    have hleft : 0 ≤ (1 - tau) * A := by
      exact mul_nonneg (by linarith) (le_of_lt hA)
    have hright : 0 < tau * (A + D - kappa) :=
      mul_pos htau_pos hendpoint
    have hsplit :
        A + tau * D - tau * kappa =
          (1 - tau) * A + tau * (A + D - kappa) := by
      ring
    rw [hsplit]
    exact add_pos_of_nonneg_of_pos hleft hright

/-! The denominator in the first-order lower-bound route, written without
    division. -/

def etaDenominator (rho tau etaU : ℝ) : ℝ :=
  rho * (rho * (A + tau * D) - tau * etaU)

theorem etaDenominator_expanded (rho tau etaU : ℝ) :
    etaDenominator rho tau etaU =
      A * rho ^ 2 + tau * (D * rho ^ 2 - rho * etaU) := by
  unfold etaDenominator
  ring

/-! Relative projected eta error is enough for strict positivity, including
    the endpoint `tau=1`, provided `kappa < A+D`. -/

theorem relative_eta_denominator_pos
    (rho tau etaU kappa : ℝ)
    (hrho : 0 < rho)
    (htau0 : 0 ≤ tau)
    (htau1 : tau ≤ 1)
    (heta : |etaU| ≤ kappa * rho)
    (hkappa : kappa < K) :
    0 < etaDenominator rho tau etaU := by
  have heta_le : etaU ≤ kappa * rho :=
    le_trans (le_abs_self etaU) heta
  have hmargin : 0 < A + tau * D - tau * kappa :=
    affine_margin_pos tau kappa htau0 htau1 hkappa
  have hmargin' : 0 < A + tau * D - kappa * tau := by
    simpa [mul_comm] using hmargin
  have hbase : 0 < rho * (A + tau * D - kappa * tau) :=
    mul_pos hrho hmargin'
  have heta_term : tau * etaU ≤ tau * (kappa * rho) :=
    mul_le_mul_of_nonneg_left heta_le htau0
  have hbracket : 0 < rho * (A + tau * D) - tau * etaU := by
    have hcomparison :
        rho * (A + tau * D - kappa * tau) ≤
          rho * (A + tau * D) - tau * etaU := by
      calc
        rho * (A + tau * D - kappa * tau) =
            rho * (A + tau * D) - tau * (kappa * rho) := by ring
        _ ≤ rho * (A + tau * D) - tau * etaU := by
          linarith
    exact lt_of_lt_of_le hbase hcomparison
  unfold etaDenominator
  exact mul_pos hrho hbracket

/-! A direct gate keeps the scalar inequality in multiplicative form and
    therefore remains meaningful even when no denominator sign has been
    established. -/

def firstOrderResidual
    (E a1 rho tau etaU : ℝ) : ℝ :=
  E - a1 * etaDenominator rho tau etaU

def directGate
    (E b a1 rho tau etaU : ℝ) : Prop :=
  firstOrderResidual E a1 rho tau etaU ≤ b

theorem direct_gate_iff_no_division
    (E b a1 rho tau etaU : ℝ) :
    directGate E b a1 rho tau etaU ↔
      E ≤ b + a1 * etaDenominator rho tau etaU := by
  unfold directGate firstOrderResidual
  exact sub_le_iff_le_add

theorem direct_gate_consequence_no_division
    (E b a1 rho tau etaU : ℝ)
    (hgate : directGate E b a1 rho tau etaU) :
    E ≤ b + a1 * etaDenominator rho tau etaU := by
  exact (direct_gate_iff_no_division E b a1 rho tau etaU).1 hgate

/-! This is the intended two-route interface: positivity supplies the
    division-free denominator fact, while the direct gate itself requires no
    division or positivity assumption. -/

theorem relative_eta_direct_gate_interface
    (E b a1 rho tau etaU kappa : ℝ)
    (hrho : 0 < rho)
    (htau0 : 0 ≤ tau)
    (htau1 : tau ≤ 1)
    (heta : |etaU| ≤ kappa * rho)
    (hkappa : kappa < K)
    (hgate : directGate E b a1 rho tau etaU) :
    E ≤ b + a1 * etaDenominator rho tau etaU ∧
      0 < etaDenominator rho tau etaU := by
  constructor
  · exact direct_gate_consequence_no_division E b a1 rho tau etaU hgate
  · exact relative_eta_denominator_pos rho tau etaU kappa
      hrho htau0 htau1 heta hkappa

#print axioms K_eq_A_add_D
#print axioms affine_margin_pos
#print axioms etaDenominator_expanded
#print axioms relative_eta_denominator_pos
#print axioms direct_gate_iff_no_division
#print axioms direct_gate_consequence_no_division
#print axioms relative_eta_direct_gate_interface

end
end RouteBPositiveSupplyRelativeEta

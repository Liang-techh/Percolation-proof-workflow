import Mathlib.Data.Real.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBPositiveSupplyFrontier
noncomputable section

/-- The scalar denominator used by the first-order terminal estimate. -/
def terminalDen (A D rho eta tau : ℝ) : ℝ :=
  A * rho ^ 2 + tau * (D * rho ^ 2 - rho * eta)

/-- With zero projected defect, the terminal denominator is positive on every
    nonzero velocity slice.  This is the no-division-at-equilibrium split. -/
theorem terminalDen_pos_of_eta_zero
    (A D rho tau : ℝ)
    (hA : 0 < A) (hD : 0 < D) (hrho : 0 < rho)
    (htau : 0 ≤ tau) :
    0 < terminalDen A D rho 0 tau := by
  unfold terminalDen
  have hrho2 : 0 < rho ^ 2 := sq_pos_of_pos hrho
  have hdrag : 0 ≤ tau * (D * rho ^ 2) := by
    positivity
  nlinarith

/-- A state-relative projected error is sufficient for a uniform denominator.
    The threshold is sharp for the scalar worst-case estimate because the
    adverse sign is attained at tau=1 and eta=kappa*rho. -/
theorem terminalDen_pos_of_relative_eta
    (A D rho eta tau kappa : ℝ)
    (hA : 0 < A) (hD : 0 < D) (hrho : 0 < rho)
    (htau0 : 0 ≤ tau) (htau1 : tau ≤ 1)
    (hk : kappa < A + D)
    (heta : |eta| ≤ kappa * rho) :
    0 < terminalDen A D rho eta tau := by
  unfold terminalDen
  have heta_upper : eta ≤ kappa * rho := (abs_le.mp heta).2
  have hnonneg : 0 ≤ tau * rho * (kappa * rho - eta) := by
    have htr : 0 ≤ tau * rho := mul_nonneg htau0 (le_of_lt hrho)
    exact mul_nonneg htr (sub_nonneg.mpr heta_upper)
  have hsum : 0 < A + D - kappa := by linarith
  have hconv : 0 < (1 - tau) * A + tau * (A + D - kappa) := by
    by_cases htau0' : tau = 0
    · simp [htau0', hA]
    by_cases htau1' : tau < 1
    · have hleft : 0 < (1 - tau) * A :=
        mul_pos (sub_pos.mpr htau1') hA
      have hright : 0 ≤ tau * (A + D - kappa) :=
        mul_nonneg htau0 (le_of_lt hsum)
      exact add_pos_of_pos_of_nonneg hleft hright
    · have htau_eq : tau = 1 := by
        apply le_antisymm
        · exact le_of_not_gt htau1'
        · exact htau1
      simp [htau_eq, hsum]
  have hbase : 0 < rho ^ 2 * (A + tau * (D - kappa)) := by
    have hrewrite : A + tau * (D - kappa) =
        (1 - tau) * A + tau * (A + D - kappa) := by ring
    rw [hrewrite]
    exact mul_pos (sq_pos_of_pos hrho) hconv
  have hcompare : rho ^ 2 * (A + tau * (D - kappa)) ≤
      A * rho ^ 2 + tau * (D * rho ^ 2 - rho * eta) := by
    nlinarith [hnonneg]
  exact lt_of_lt_of_le hbase hcompare

/-- The concrete B45 slice uses A=2002229/24000000 and D=29/20.  The
    relative-error threshold is 36802229/24000000. -/
theorem b45_terminalDen_pos_of_relative_eta
    (rho eta tau kappa : ℝ)
    (hrho : 0 < rho) (htau0 : 0 ≤ tau) (htau1 : tau ≤ 1)
    (hk : kappa < (36802229 : ℝ) / 24000000)
    (heta : |eta| ≤ kappa * rho) :
    0 < terminalDen ((2002229 : ℝ) / 24000000) (29 / 20)
        rho eta tau := by
  apply terminalDen_pos_of_relative_eta
    ((2002229 : ℝ) / 24000000) (29 / 20) rho eta tau kappa
  · norm_num
  · norm_num
  · exact hrho
  · exact htau0
  · exact htau1
  · norm_num at hk ⊢
    exact hk
  · exact heta

/-- A direct equilibrium gate does not divide by the terminal denominator. -/
theorem equilibrium_floor_le_beta0
    (floor beta0 rate : ℝ)
    (hrate : rate = 0)
    (hgate : floor + rate ≤ beta0) :
    floor ≤ beta0 := by
  linarith

/-- Once the equilibrium floor is paid by beta0, the remaining finite supply
    budget can be checked by ordinary exact arithmetic. -/
theorem equilibrium_floor_budget
    (v0 floor beta0 tail : ℝ)
    (hfloor : floor ≤ beta0)
    (hbudget : v0 + beta0 + tail < 1) :
    v0 + floor + tail < 1 := by
  linarith

#print axioms terminalDen_pos_of_eta_zero
#print axioms terminalDen_pos_of_relative_eta
#print axioms b45_terminalDen_pos_of_relative_eta
#print axioms equilibrium_floor_le_beta0
#print axioms equilibrium_floor_budget

end
end RouteBPositiveSupplyFrontier

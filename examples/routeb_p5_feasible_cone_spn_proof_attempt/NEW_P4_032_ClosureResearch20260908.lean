import NEW_P4_032_SchurPMIAbsorption

/-!
UNCOMPILED independent research sidecar. No local Lean/Lake execution.
Exact scalar/vector composition only: no physical instance, matrix PSD,
Float64 enclosure, domain coverage, or registry admission is asserted.
This file does not import or modify another agent's BudgetClosureAudit.
-/
set_option autoImplicit false

namespace RouteBP4032ClosureResearch20260908

open RouteBP4032RelativeAdditive RouteBP4032SchurPMIAbsorption

noncomputable section

abbrev Vec2 := Fin 2 → ℝ

def sq2 (v : Vec2) : ℝ := v 0 ^ 2 + v 1 ^ 2

theorem sq2_nonnegative (v : Vec2) : 0 ≤ sq2 v :=
  add_nonneg (sq_nonneg _) (sq_nonneg _)

/-- Division-free numerator of the combined Schur floor for lambda > 1.
W is an upper bound on the PORT squared norm, not the total residual. -/
def schurNumerator (base target lam W : ℝ) (ell : Vec2) : ℝ :=
  (lam - 1) * (base - target - lam * W) - lam * sq2 ell

/-- Retains the total residual cross term. The completed square and the
port allowance each occur once, with the forced lambda coefficient. -/
theorem combined_remainder_identity (base target lam W : ℝ) (ell r : Vec2) :
    (lam - 1) * (base - target - sq2 (fun i => ell i + r i)) =
      schurNumerator base target lam W ell +
        sq2 (fun i => ell i - (lam - 1) * r i) +
        lam * (lam - 1) * (W - sq2 r) := by
  simp only [sq2, schurNumerator]
  ring

/-- Pointwise scalar consumer; matrix interpretation is a separate theorem. -/
theorem combined_of_port_budget (base target lam W : ℝ) (ell r : Vec2)
    (hlam : 1 < lam) (hport : sq2 r ≤ W)
    (halloc : 0 ≤ schurNumerator base target lam W ell) :
    target ≤ base - sq2 (fun i => ell i + r i) := by
  have hd : 0 < lam - 1 := by linarith
  have hl : 0 ≤ lam := by linarith
  have hs : 0 ≤ (lam - 1) * (base - target - sq2 (fun i => ell i + r i)) := by
    rw [combined_remainder_identity]
    exact add_nonneg (add_nonneg halloc (sq2_nonnegative _))
      (mul_nonneg (mul_nonneg hl hd.le) (sub_nonneg.mpr hport))
  have hc := (mul_nonneg_iff_of_pos_left hd).mp hs
  linarith

/-- Compatibility with the existing port absorption packet. A caller from
force_absorption must additionally identify norm2(r)^2 with sq2(r).
No source object or that norm identity is manufactured by this theorem. -/
theorem combined_of_absorbed_port (p : Parameters)
    (energy delta base target lam margin : ℝ) (ell r : Vec2)
    (budget : AbsorbedAt p energy (sq2 r) delta)
    (hlam : 1 < lam)
    (halloc : 0 ≤ schurNumerator base target lam
      (rhoEff p * energy + biasEff p) ell)
    (binding : base - sq2 (fun i => ell i + r i) ≤ margin) :
    target ≤ margin :=
  (combined_of_port_budget base target lam (rhoEff p * energy + biasEff p)
    ell r hlam budget.relative halloc).trans binding

/-- A non-unit scalar comparison changes BOTH the relative coefficient and
the bias charge. gain can incorporate an already justified scalar scale. -/
theorem scaled_margin_floor (energy q rho bias alpha gain offset margin : ℝ)
    (hg : 0 ≤ gain) (hrel : q ≤ rho * energy + bias)
    (binding : alpha * energy + offset - gain * q ≤ margin) :
    (alpha - gain * rho) * energy + offset - gain * bias ≤ margin := by
  have h := mul_le_mul_of_nonneg_left hrel hg
  nlinarith

/-- General feedback gain c: the residual numerator contains bias ONCE,
whereas the energy numerator contains c*bias. No quotients are used. -/
theorem scaled_feedback (energy q base rho bias c : ℝ)
    (hr : 0 ≤ rho) (hc : 0 ≤ c)
    (hrel : q ≤ rho * energy + bias) (hfb : energy ≤ base + c * q) :
    (1 - c * rho) * energy ≤ base + c * bias ∧
      (1 - c * rho) * q ≤ rho * base + bias := by
  constructor
  · have h := mul_le_mul_of_nonneg_left hrel hc
    nlinarith
  · have h := mul_le_mul_of_nonneg_left hfb hr
    nlinarith

/-- Port=0 does not imply total residual=0. This is an abstract two-vector
interface counterexample, not a reachable robot state. -/
theorem port_only_replacement_fails :
    let ell : Vec2 := ![1, 0]
    let r : Vec2 := ![0, 0]
    sq2 r ≤ 0 ∧
      0 ≤ (1 / 2 : ℝ) - sq2 r ∧
      (1 / 2 : ℝ) - sq2 (fun i => ell i + r i) < 0 := by
  norm_num [sq2]

/-- rho<1 cannot replace the scaled gate alpha-gain*rho>0. -/
theorem ignored_gain_counterexample :
    (3 / 4 : ℝ) < 1 ∧ (3 / 4 : ℝ) ≤ (3 / 4 : ℝ) * 1 + 0 ∧
      1 - 2 * (3 / 4 : ℝ) < 0 := by
  norm_num

/-- Robust zero-radius boundary: ell=(1,0), base=1, target=0, r=0
has true margin zero, but no finite lambda>1 certifies this Schur form. -/
theorem fixed_lambda_zero_radius_obstruction (lam : ℝ) :
    schurNumerator 1 0 lam 0 ![1, 0] = -1 := by
  norm_num [schurNumerator, sq2]
  ring

theorem zero_radius_true_margin :
    (1 : ℝ) - sq2 (fun i => (![1, 0] : Vec2) i + (![0, 0] : Vec2) i) = 0 := by
  norm_num [sq2]

-- Future axiom inspections only; none has been run in this task.
#print axioms sq2_nonnegative
#print axioms combined_remainder_identity
#print axioms combined_of_port_budget
#print axioms combined_of_absorbed_port
#print axioms scaled_margin_floor
#print axioms scaled_feedback
#print axioms port_only_replacement_fails
#print axioms ignored_gain_counterexample
#print axioms fixed_lambda_zero_radius_obstruction
#print axioms zero_radius_true_margin

end
end RouteBP4032ClosureResearch20260908

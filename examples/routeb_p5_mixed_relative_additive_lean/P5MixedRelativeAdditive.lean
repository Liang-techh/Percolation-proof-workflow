import Mathlib

noncomputable section

namespace RouteBP5MixedRelativeAdditive

/-- Exact Pareto decay coefficient from T-P5-040. -/
def decayRate (r : ℝ) : ℝ := (109 - r) / 200

/-- Exact fourth-channel quadratic reserve before relative residual charging. -/
def a4 (r : ℝ) : ℝ := (250 + 53 * r) / 1500

/-- Exact fifth-channel quadratic reserve before relative residual charging. -/
def a5 : ℝ := 1 / 6

/-- Remaining fourth-channel reserve after charging `rho4`. -/
def reserve4 (r rho4 : ℝ) : ℝ := a4 r - rho4

/-- Remaining fifth-channel reserve after charging `rho5`. -/
def reserve5 (rho5 : ℝ) : ℝ := a5 - rho5

/-- Division-free fourth-channel reserve numerator used by the checker gate. -/
def A4 (r rho4 : ℝ) : ℝ := 250 + 53 * r - 1500 * rho4

/-- Division-free fifth-channel reserve numerator used by the checker gate. -/
def A5 (rho5 : ℝ) : ℝ := 1 - 6 * rho5

/-- Absolute value preserves squares over the reals. -/
theorem abs_sq_eq (x : ℝ) : |x| ^ 2 = x ^ 2 := by
  calc
    |x| ^ 2 = |x| * |x| := by ring
    _ = |x * x| := by rw [abs_mul]
    _ = x * x := abs_of_nonneg (mul_self_nonneg x)
    _ = x ^ 2 := by ring

/-- Convert a mixed componentwise residual bound into the corresponding power bound. -/
theorem residual_power_bound
    (u l rho b : ℝ)
    (hres : |l| ≤ rho * |u| + b) :
    -u * l ≤ rho * u ^ 2 + b * |u| := by
  have hsign : -(u * l) ≤ |u * l| := neg_le_abs (u * l)
  rw [abs_mul] at hsign
  have hscale : |u| * |l| ≤ |u| * (rho * |u| + b) :=
    mul_le_mul_of_nonneg_left hres (abs_nonneg u)
  have hrewrite : |u| * (rho * |u| + b) = rho * u ^ 2 + b * |u| := by
    rw [← abs_sq_eq u]
    ring
  calc
    -u * l ≤ |u| * |l| := hsign
    _ ≤ |u| * (rho * |u| + b) := hscale
    _ = rho * u ^ 2 + b * |u| := hrewrite

/--
Division-free sharp square completion.  This identity-derived inequality is valid
without assuming `t > 0`; positivity is needed only when dividing by `4*t`.
-/
theorem mixed_square_completion_cleared (t u b : ℝ) :
    4 * t * (-t * u ^ 2 + b * |u|) ≤ b ^ 2 := by
  have hid :
      4 * t * (-t * u ^ 2 + b * |u|)
          + (2 * t * |u| - b) ^ 2 = b ^ 2 := by
    rw [← abs_sq_eq u]
    ring
  have hsquare : 0 ≤ (2 * t * |u| - b) ^ 2 := sq_nonneg (2 * t * |u| - b)
  linarith

/-- Sharp one-channel additive-bias charge for a strictly positive reserve. -/
theorem mixed_square_completion
    (t u b : ℝ) (ht : 0 < t) :
    -t * u ^ 2 + b * |u| ≤ b ^ 2 / (4 * t) := by
  have hclear := mixed_square_completion_cleared t u b
  have h4t : 0 < 4 * t := by nlinarith
  apply (le_div_iff₀ h4t).2
  nlinarith

/-- Exact equivalence between checker numerator positivity and positive fourth reserve. -/
theorem reserve4_pos_iff (r rho4 : ℝ) :
    0 < reserve4 r rho4 ↔ 0 < A4 r rho4 := by
  dsimp [reserve4, a4, A4]
  constructor <;> intro h <;> nlinarith

/-- Exact equivalence between checker numerator positivity and positive fifth reserve. -/
theorem reserve5_pos_iff (rho5 : ℝ) :
    0 < reserve5 rho5 ↔ 0 < A5 rho5 := by
  dsimp [reserve5, a5, A5]
  constructor <;> intro h <;> nlinarith

/--
Source-independent mixed relative-plus-additive decay theorem.  It consumes the
frozen Pareto coercivity inequality and moving-frame derivative identity, but
makes no claim that deployed residuals satisfy the component contracts.
-/
theorem block45_pareto_mixed_residual_decay
    (r V Q Vdot u4 u5 l4 l5 rho4 rho5 b4 b5 : ℝ)
    (hQ : decayRate r * V + a4 r * u4 ^ 2 + a5 * u5 ^ 2 ≤ Q)
    (hVdot : Vdot = -Q - u4 * l4 - u5 * l5)
    (hres4 : |l4| ≤ rho4 * |u4| + b4)
    (hres5 : |l5| ≤ rho5 * |u5| + b5)
    (ht4 : 0 < reserve4 r rho4)
    (ht5 : 0 < reserve5 rho5) :
    Vdot ≤ -decayRate r * V
      + b4 ^ 2 / (4 * reserve4 r rho4)
      + b5 ^ 2 / (4 * reserve5 rho5) := by
  have hp4 := residual_power_bound u4 l4 rho4 b4 hres4
  have hp5 := residual_power_bound u5 l5 rho5 b5 hres5
  have hraw :
      Vdot ≤ -decayRate r * V
        + (-reserve4 r rho4 * u4 ^ 2 + b4 * |u4|)
        + (-reserve5 rho5 * u5 ^ 2 + b5 * |u5|) := by
    rw [hVdot]
    dsimp [reserve4, reserve5]
    nlinarith [hQ, hp4, hp5]
  have hc4 := mixed_square_completion (reserve4 r rho4) u4 b4 ht4
  have hc5 := mixed_square_completion (reserve5 rho5) u5 b5 ht5
  linarith

/--
The T-P5-040 polynomial quarter-barrier gate is exactly the cross-multiplied
charge inequality in the reserve variables; no square roots or state-dependent
Young parameters are introduced.  Positivity is needed only by consumers that
subsequently divide by the reserves.
-/
theorem block45_pareto_quarter_gate_cross
    (r rho4 rho5 B4 B5 : ℝ)
    (hgate :
      300000 * B4 * A5 rho5 + 1200 * B5 * A4 r rho4
        < (109 - r) * A4 r rho4 * A5 rho5) :
    B4 * reserve5 rho5 + B5 * reserve4 r rho4
      < decayRate r * reserve4 r rho4 * reserve5 rho5 := by
  dsimp [A4, A5, reserve4, reserve5, a4, a5, decayRate] at hgate ⊢
  nlinarith

/--
Division-free quarter-barrier first-exit theorem.  The only residual information
used is the mixed componentwise contract plus uniform square budgets on the
additive witnesses.
-/
theorem block45_pareto_bias_first_exit_gate
    (r V Q Vdot u4 u5 l4 l5 rho4 rho5 b4 b5 B4 B5 : ℝ)
    (hQ : decayRate r * V + a4 r * u4 ^ 2 + a5 * u5 ^ 2 ≤ Q)
    (hVdot : Vdot = -Q - u4 * l4 - u5 * l5)
    (hres4 : |l4| ≤ rho4 * |u4| + b4)
    (hres5 : |l5| ≤ rho5 * |u5| + b5)
    (hB4 : b4 ^ 2 ≤ B4)
    (hB5 : b5 ^ 2 ≤ B5)
    (hVstar : V = 1 / 4)
    (hA4 : 0 < A4 r rho4)
    (hA5 : 0 < A5 rho5)
    (hgate :
      300000 * B4 * A5 rho5 + 1200 * B5 * A4 r rho4
        < (109 - r) * A4 r rho4 * A5 rho5) :
    Vdot < 0 := by
  have ht4 : 0 < reserve4 r rho4 := (reserve4_pos_iff r rho4).2 hA4
  have ht5 : 0 < reserve5 rho5 := (reserve5_pos_iff rho5).2 hA5
  have hp4 := residual_power_bound u4 l4 rho4 b4 hres4
  have hp5 := residual_power_bound u5 l5 rho5 b5 hres5
  have hraw :
      Vdot ≤ -decayRate r * V
        + (-reserve4 r rho4 * u4 ^ 2 + b4 * |u4|)
        + (-reserve5 rho5 * u5 ^ 2 + b5 * |u5|) := by
    rw [hVdot]
    dsimp [reserve4, reserve5]
    nlinarith [hQ, hp4, hp5]
  have hc4 := mixed_square_completion_cleared (reserve4 r rho4) u4 b4
  have hc5 := mixed_square_completion_cleared (reserve5 rho5) u5 b5
  have hc4B :
      4 * reserve4 r rho4 *
          (-reserve4 r rho4 * u4 ^ 2 + b4 * |u4|) ≤ B4 :=
    le_trans hc4 hB4
  have hc5B :
      4 * reserve5 rho5 *
          (-reserve5 rho5 * u5 ^ 2 + b5 * |u5|) ≤ B5 :=
    le_trans hc5 hB5
  have hm4 := mul_le_mul_of_nonneg_right hc4B (le_of_lt ht5)
  have hm5 := mul_le_mul_of_nonneg_right hc5B (le_of_lt ht4)
  have hsum :
      4 * (reserve4 r rho4 * reserve5 rho5) *
          ((-reserve4 r rho4 * u4 ^ 2 + b4 * |u4|)
            + (-reserve5 rho5 * u5 ^ 2 + b5 * |u5|))
        ≤ B4 * reserve5 rho5 + B5 * reserve4 r rho4 := by
    nlinarith [hm4, hm5]
  have hcross := block45_pareto_quarter_gate_cross r rho4 rho5 B4 B5 hgate
  have hscaled :
      4 * (reserve4 r rho4 * reserve5 rho5) *
          ((-reserve4 r rho4 * u4 ^ 2 + b4 * |u4|)
            + (-reserve5 rho5 * u5 ^ 2 + b5 * |u5|))
        < 4 * (reserve4 r rho4 * reserve5 rho5) * (decayRate r / 4) := by
    nlinarith [hsum, hcross]
  have hden : 0 < 4 * (reserve4 r rho4 * reserve5 rho5) := by positivity
  have hcharge :
      (-reserve4 r rho4 * u4 ^ 2 + b4 * |u4|)
          + (-reserve5 rho5 * u5 ^ 2 + b5 * |u5|)
        < decayRate r / 4 := by
    by_contra hnot
    have hge :
        decayRate r / 4 ≤
          (-reserve4 r rho4 * u4 ^ 2 + b4 * |u4|)
            + (-reserve5 rho5 * u5 ^ 2 + b5 * |u5|) := le_of_not_gt hnot
    have hm := mul_le_mul_of_nonneg_left hge (le_of_lt hden)
    exact (not_le_of_gt hscaled) hm
  rw [hVstar] at hraw
  have hcancel : -decayRate r * (1 / 4 : ℝ) + decayRate r / 4 = 0 := by ring
  linarith

/-- The zero-relative specialization is exactly the earlier T-P5-039 additive gate. -/
theorem block45_zero_relative_gate_reduces (r B4 B5 : ℝ) :
    (300000 * B4 * A5 0 + 1200 * B5 * A4 r 0
        < (109 - r) * A4 r 0 * A5 0) ↔
      300000 * B4 + 1200 * (250 + 53 * r) * B5
        < (109 - r) * (250 + 53 * r) := by
  constructor <;> intro h
  · dsimp [A4, A5] at h
    nlinarith
  · dsimp [A4, A5]
    nlinarith

/--
Pure arithmetic form of the incremental `dc^2` tube gate.  This is the exact
cross-multiplied statement corresponding to
`G4/(4*t4)+G5/(4*t5) < decayRate(r)/12`.
-/
theorem block45_pareto_incremental_gate_cross
    (r rho4 rho5 G4 G5 : ℝ)
    (hgate :
      900000 * G4 * A5 rho5 + 3600 * G5 * A4 r rho4
        < (109 - r) * A4 r rho4 * A5 rho5) :
    3 * (G4 * reserve5 rho5 + G5 * reserve4 r rho4)
      < decayRate r * reserve4 r rho4 * reserve5 rho5 := by
  dsimp [A4, A5, reserve4, reserve5, a4, a5, decayRate] at hgate ⊢
  nlinarith

#print axioms abs_sq_eq
#print axioms residual_power_bound
#print axioms mixed_square_completion_cleared
#print axioms mixed_square_completion
#print axioms reserve4_pos_iff
#print axioms reserve5_pos_iff
#print axioms block45_pareto_mixed_residual_decay
#print axioms block45_pareto_quarter_gate_cross
#print axioms block45_pareto_bias_first_exit_gate
#print axioms block45_zero_relative_gate_reduces
#print axioms block45_pareto_incremental_gate_cross

end RouteBP5MixedRelativeAdditive

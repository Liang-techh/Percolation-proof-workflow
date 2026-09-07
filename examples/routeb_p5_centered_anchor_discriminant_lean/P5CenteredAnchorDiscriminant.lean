import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P5 centered/anchor discriminant sidecar

This file formalizes the exact-real algebra from
`review-T-P5-021-honglianmozun-20260907T0800.md`.

The core result eliminates the auxiliary dissipation split search.  A positive
linear headroom together with a strict polynomial discriminant produces an
explicit rational balanced split.  Thin corollaries instantiate the current P5
centered/anchor ledger, the quarter barrier, and the common physical-margin
barrier.

This sidecar deliberately does not source-bind `ell2`, `B2`, `Vstar`, or
`sigma`; it does not certify IEEE/Float64/solve semantics, ODE continuation,
P8 coverage, P5/M4 closure, or registry admission.
-/

set_option autoImplicit false

namespace RouteBP5CenteredAnchorDiscriminant

noncomputable section

/-- Canonical rational balanced split. -/
def balancedMu (D X Y : ℝ) : ℝ :=
  (D + X - Y) / (2 * D)

/-- The centered square slack has exactly the discriminant remainder. -/
theorem centered_discriminant_identity (D X Y : ℝ) :
    (D + X - Y) ^ 2 - 4 * D * X =
      (D - X - Y) ^ 2 - 4 * X * Y := by
  ring

/-- The anchor square slack has the same discriminant remainder. -/
theorem anchor_discriminant_identity (D X Y : ℝ) :
    (D - X + Y) ^ 2 - 4 * D * Y =
      (D - X - Y) ^ 2 - 4 * X * Y := by
  ring

/-- Strict polynomial feasibility constructs an explicit balanced split with
strict room in both square budgets.  No square root or density argument is
used. -/
theorem balanced_square_split
    (D X Y : ℝ)
    (hD : 0 < D)
    (hX : 0 ≤ X)
    (hY : 0 ≤ Y)
    (hC : 0 < D - X - Y)
    (hDelta : 4 * X * Y < (D - X - Y) ^ 2) :
    0 < balancedMu D X Y ∧
      balancedMu D X Y < 1 ∧
      X < D * (balancedMu D X Y) ^ 2 ∧
      Y < D * (1 - balancedMu D X Y) ^ 2 := by
  have hD2 : 0 < 2 * D := by positivity
  have hD4 : 0 < 4 * D := by positivity
  have hDne : D ≠ 0 := ne_of_gt hD
  have hnumPos : 0 < D + X - Y := by
    nlinarith
  have hotherPos : 0 < D - X + Y := by
    nlinarith
  have hnumLt : D + X - Y < 2 * D := by
    nlinarith
  have hmu0 : 0 < balancedMu D X Y := by
    rw [balancedMu]
    exact div_pos hnumPos hD2
  have hmu1 : balancedMu D X Y < 1 := by
    rw [balancedMu]
    exact (div_lt_one hD2).2 hnumLt
  have hslackX : 4 * D * X < (D + X - Y) ^ 2 := by
    have hid := centered_discriminant_identity D X Y
    nlinarith
  have hslackY : 4 * D * Y < (D - X + Y) ^ 2 := by
    have hid := anchor_discriminant_identity D X Y
    nlinarith
  have hmuSq :
      D * (balancedMu D X Y) ^ 2 =
        (D + X - Y) ^ 2 / (4 * D) := by
    rw [balancedMu]
    field_simp [hDne]
    <;> ring
  have hOneMu :
      1 - balancedMu D X Y = (D - X + Y) / (2 * D) := by
    rw [balancedMu]
    field_simp [hDne]
    <;> ring
  have hOneMuSq :
      D * (1 - balancedMu D X Y) ^ 2 =
        (D - X + Y) ^ 2 / (4 * D) := by
    rw [hOneMu]
    field_simp [hDne]
    <;> ring
  have hx : X < D * (balancedMu D X Y) ^ 2 := by
    rw [hmuSq]
    apply (lt_div_iff₀ hD4).2
    nlinarith
  have hy : Y < D * (1 - balancedMu D X Y) ^ 2 := by
    rw [hOneMuSq]
    apply (lt_div_iff₀ hD4).2
    nlinarith
  exact ⟨hmu0, hmu1, hx, hy⟩

/-- P5 route-specific linear headroom. -/
def p5Headroom (ell2 B2 Vstar : ℝ) : ℝ :=
  2285 * Vstar - 13600 * ell2 * Vstar - 11424 * B2

/-- P5 route-specific balanced witness from T-P5-021. -/
def p5BalancedMu (ell2 B2 Vstar : ℝ) : ℝ :=
  (2285 * Vstar + 13600 * ell2 * Vstar - 11424 * B2) /
    (4570 * Vstar)

/-- Exact checker frontend for the centered-plus-anchor P5 barrier. -/
theorem p5_centered_anchor_balanced_mu
    (ell2 B2 Vstar : ℝ)
    (hEll : 0 ≤ ell2)
    (hB : 0 ≤ B2)
    (hV : 0 < Vstar)
    (hC : 0 < p5Headroom ell2 B2 Vstar)
    (hDelta :
      621465600 * ell2 * Vstar * B2 <
        (p5Headroom ell2 B2 Vstar) ^ 2) :
    0 < p5BalancedMu ell2 B2 Vstar ∧
      p5BalancedMu ell2 B2 Vstar < 1 ∧
      2720 * ell2 < 457 * (p5BalancedMu ell2 B2 Vstar) ^ 2 ∧
      11424 * B2 <
        2285 * (1 - p5BalancedMu ell2 B2 Vstar) ^ 2 * Vstar := by
  have hD : 0 < 2285 * Vstar := by positivity
  have hX : 0 ≤ 13600 * ell2 * Vstar := by positivity
  have hY : 0 ≤ 11424 * B2 := by positivity
  have hC' :
      0 < 2285 * Vstar - 13600 * ell2 * Vstar - 11424 * B2 := by
    simpa [p5Headroom] using hC
  have hDelta' :
      4 * (13600 * ell2 * Vstar) * (11424 * B2) <
        (2285 * Vstar - 13600 * ell2 * Vstar - 11424 * B2) ^ 2 := by
    convert hDelta using 1 <;> simp [p5Headroom] <;> ring
  have hs := balanced_square_split
    (2285 * Vstar) (13600 * ell2 * Vstar) (11424 * B2)
    hD hX hY hC' hDelta'
  have hmuEq :
      balancedMu (2285 * Vstar) (13600 * ell2 * Vstar) (11424 * B2) =
        p5BalancedMu ell2 B2 Vstar := by
    simp [balancedMu, p5BalancedMu]
    ring
  rw [hmuEq] at hs
  rcases hs with ⟨hmu0, hmu1, hx, hy⟩
  have hxCancel :
      13600 * ell2 < 2285 * (p5BalancedMu ell2 B2 Vstar) ^ 2 := by
    apply (mul_lt_mul_left hV).mp
    simpa [mul_assoc, mul_left_comm, mul_comm] using hx
  have hxFinal :
      2720 * ell2 < 457 * (p5BalancedMu ell2 B2 Vstar) ^ 2 := by
    nlinarith
  have hyFinal :
      11424 * B2 <
        2285 * (1 - p5BalancedMu ell2 B2 Vstar) ^ 2 * Vstar := by
    simpa [mul_assoc, mul_left_comm, mul_comm] using hy
  exact ⟨hmu0, hmu1, hxFinal, hyFinal⟩

/-- Quarter-barrier linear headroom with all denominators cleared. -/
def quarterHeadroom (ell2 B2 : ℝ) : ℝ :=
  2285 - 13600 * ell2 - 45696 * B2

/-- Canonical quarter-barrier balanced witness. -/
def quarterBalancedMu (ell2 B2 : ℝ) : ℝ :=
  (2285 + 13600 * ell2 - 45696 * B2) / 4570

/-- Exact `Vstar = 1/4` discriminant checker. -/
theorem p5_quarter_discriminant_barrier
    (ell2 B2 : ℝ)
    (hEll : 0 ≤ ell2)
    (hB : 0 ≤ B2)
    (hC : 0 < quarterHeadroom ell2 B2)
    (hDelta :
      2485862400 * ell2 * B2 < (quarterHeadroom ell2 B2) ^ 2) :
    0 < quarterBalancedMu ell2 B2 ∧
      quarterBalancedMu ell2 B2 < 1 ∧
      2720 * ell2 < 457 * (quarterBalancedMu ell2 B2) ^ 2 ∧
      45696 * B2 < 2285 * (1 - quarterBalancedMu ell2 B2) ^ 2 := by
  have hC' : 0 < 2285 - 13600 * ell2 - 45696 * B2 := by
    simpa [quarterHeadroom] using hC
  have hDelta' :
      4 * (13600 * ell2) * (45696 * B2) <
        (2285 - 13600 * ell2 - 45696 * B2) ^ 2 := by
    convert hDelta using 1 <;> simp [quarterHeadroom] <;> ring
  have hs := balanced_square_split
    2285 (13600 * ell2) (45696 * B2)
    (by norm_num) (by positivity) (by positivity) hC' hDelta'
  have hmuEq :
      balancedMu 2285 (13600 * ell2) (45696 * B2) =
        quarterBalancedMu ell2 B2 := by
    norm_num [balancedMu, quarterBalancedMu]
  rw [hmuEq] at hs
  rcases hs with ⟨hmu0, hmu1, hx, hy⟩
  have hxFinal :
      2720 * ell2 < 457 * (quarterBalancedMu ell2 B2) ^ 2 := by
    nlinarith
  exact ⟨hmu0, hmu1, hxFinal, hy⟩

/-- Common position/velocity-margin headroom. -/
def commonMarginHeadroom (ell2 B2 sigma : ℝ) : ℝ :=
  17823 * sigma ^ 2 - 106080 * ell2 * sigma ^ 2 - 3716608 * B2

/-- Canonical common-margin balanced witness. -/
def commonMarginBalancedMu (ell2 B2 sigma : ℝ) : ℝ :=
  (17823 * sigma ^ 2 + 106080 * ell2 * sigma ^ 2 - 3716608 * B2) /
    (35646 * sigma ^ 2)

/-- Exact discriminant checker for the common position/velocity margin. -/
theorem p5_common_margin_discriminant_barrier
    (ell2 B2 sigma : ℝ)
    (hEll : 0 ≤ ell2)
    (hB : 0 ≤ B2)
    (hSigmaSq : 0 < sigma ^ 2)
    (hC : 0 < commonMarginHeadroom ell2 B2 sigma)
    (hDelta :
      1577031106560 * ell2 * sigma ^ 2 * B2 <
        (commonMarginHeadroom ell2 B2 sigma) ^ 2) :
    0 < commonMarginBalancedMu ell2 B2 sigma ∧
      commonMarginBalancedMu ell2 B2 sigma < 1 ∧
      2720 * ell2 < 457 * (commonMarginBalancedMu ell2 B2 sigma) ^ 2 ∧
      3716608 * B2 <
        17823 * (1 - commonMarginBalancedMu ell2 B2 sigma) ^ 2 * sigma ^ 2 := by
  have hD : 0 < 17823 * sigma ^ 2 := by positivity
  have hX : 0 ≤ 106080 * ell2 * sigma ^ 2 := by positivity
  have hY : 0 ≤ 3716608 * B2 := by positivity
  have hC' :
      0 < 17823 * sigma ^ 2 - 106080 * ell2 * sigma ^ 2 - 3716608 * B2 := by
    simpa [commonMarginHeadroom] using hC
  have hDelta' :
      4 * (106080 * ell2 * sigma ^ 2) * (3716608 * B2) <
        (17823 * sigma ^ 2 - 106080 * ell2 * sigma ^ 2 - 3716608 * B2) ^ 2 := by
    convert hDelta using 1 <;> simp [commonMarginHeadroom] <;> ring
  have hs := balanced_square_split
    (17823 * sigma ^ 2) (106080 * ell2 * sigma ^ 2) (3716608 * B2)
    hD hX hY hC' hDelta'
  have hmuEq :
      balancedMu (17823 * sigma ^ 2)
          (106080 * ell2 * sigma ^ 2) (3716608 * B2) =
        commonMarginBalancedMu ell2 B2 sigma := by
    simp [balancedMu, commonMarginBalancedMu]
    ring
  rw [hmuEq] at hs
  rcases hs with ⟨hmu0, hmu1, hx, hy⟩
  have hxCancel :
      106080 * ell2 <
        17823 * (commonMarginBalancedMu ell2 B2 sigma) ^ 2 := by
    apply (mul_lt_mul_left hSigmaSq).mp
    simpa [mul_assoc, mul_left_comm, mul_comm] using hx
  have hxFinal :
      2720 * ell2 < 457 * (commonMarginBalancedMu ell2 B2 sigma) ^ 2 := by
    nlinarith
  have hyFinal :
      3716608 * B2 <
        17823 * (1 - commonMarginBalancedMu ell2 B2 sigma) ^ 2 * sigma ^ 2 := by
    simpa [mul_assoc, mul_left_comm, mul_comm] using hy
  exact ⟨hmu0, hmu1, hxFinal, hyFinal⟩

#print axioms centered_discriminant_identity
#print axioms anchor_discriminant_identity
#print axioms balanced_square_split
#print axioms p5_centered_anchor_balanced_mu
#print axioms p5_quarter_discriminant_barrier
#print axioms p5_common_margin_discriminant_barrier

end

end RouteBP5CenteredAnchorDiscriminant

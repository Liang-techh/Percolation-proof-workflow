import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P5 same-curvature shared-r optimizer seam

Source-independent Lean decomposition for
`agent_review_inbox/review-T-P5-047-shared-r-kuangmanmozun-20260907T2148.md`.

This sidecar freezes the algebraic candidate seams used by the exact five-candidate
shared-`r` checker: same-curvature affine difference, vertex identities and active
vertex witnesses, strict-interior crossover transport and scaled crossover value,
the P5 determinant-term cancellation, and a regression family showing that two
independent one-gate PASS results do not imply one shared witness.

It intentionally does not claim the full five-candidate necessity/completeness
proof, source binding, Float64/controller semantics, P8 coverage, or registry
admission.
-/

set_option autoImplicit false

namespace RouteBP5SharedROptimizer

noncomputable section

/-- One concave gate with common curvature parameter `d`. -/
def gate (A B d r : ℝ) : ℝ := A + B * r - d * r^2

/-- Two gates with the same curvature differ by an affine function. -/
theorem same_curvature_difference_affine
    (A1 B1 A2 B2 d r : ℝ) :
    gate A1 B1 d r - gate A2 B2 d r =
      (A1 - A2) + (B1 - B2) * r := by
  unfold gate
  ring

/-- Pure ring completion-of-square identity at the formal vertex `B/(2d)`. -/
theorem same_curvature_vertex_square
    (A B d r : ℝ) (hd : d ≠ 0) :
    4 * d * (gate A B d (B / (2 * d)) - gate A B d r) =
      (2 * d * r - B)^2 := by
  unfold gate
  field_simp [hd]
  ring

/-- The value at the formal vertex has the square-root-free numerator
`4*d*A+B^2`. -/
theorem scaled_vertex_value
    (A B d : ℝ) (hd : d ≠ 0) :
    4 * d * gate A B d (B / (2 * d)) = 4 * d * A + B^2 := by
  unfold gate
  field_simp [hd]
  ring

/-- The affine gate difference evaluated at gate 1's formal vertex, scaled by
`2d`, is division-free. -/
theorem scaled_difference_at_vertex_one
    (A1 B1 A2 B2 d : ℝ) (hd : d ≠ 0) :
    (2 * d) *
        (gate A1 B1 d (B1 / (2 * d)) -
          gate A2 B2 d (B1 / (2 * d))) =
      2 * d * (A1 - A2) + (B1 - B2) * B1 := by
  rw [same_curvature_difference_affine]
  field_simp [hd]

/-- Symmetric division-free difference formula at gate 2's formal vertex. -/
theorem scaled_difference_at_vertex_two
    (A1 B1 A2 B2 d : ℝ) (hd : d ≠ 0) :
    (2 * d) *
        (gate A1 B1 d (B2 / (2 * d)) -
          gate A2 B2 d (B2 / (2 * d))) =
      2 * d * (A1 - A2) + (B1 - B2) * B2 := by
  rw [same_curvature_difference_affine]
  field_simp [hd]

/-- Active interior vertex of gate 1 is a valid shared strict witness. -/
theorem shared_positive_of_active_vertex_one
    (A1 B1 A2 B2 d : ℝ)
    (hd : 0 < d)
    (hBpos : 0 < B1)
    (hBlt : B1 < 2 * d)
    (hnum : 0 < 4 * d * A1 + B1^2)
    (hactive : 2 * d * (A1 - A2) + (B1 - B2) * B1 ≤ 0) :
    ∃ r : ℝ,
      0 ≤ r ∧ r ≤ 1 ∧
      0 < gate A1 B1 d r ∧ 0 < gate A2 B2 d r := by
  let r : ℝ := B1 / (2 * d)
  have h2d : 0 < 2 * d := by positivity
  have hscale : (2 * d) * r = B1 := by
    dsimp [r]
    field_simp
  have hrpos : 0 < r := by
    nlinarith
  have hrlt : r < 1 := by
    nlinarith
  have hv : 4 * d * gate A1 B1 d r = 4 * d * A1 + B1^2 := by
    dsimp [r]
    exact scaled_vertex_value A1 B1 d (ne_of_gt hd)
  have hg1 : 0 < gate A1 B1 d r := by
    nlinarith
  have hdiffScaled :
      (2 * d) * (gate A1 B1 d r - gate A2 B2 d r) =
        2 * d * (A1 - A2) + (B1 - B2) * B1 := by
    dsimp [r]
    exact scaled_difference_at_vertex_one A1 B1 A2 B2 d (ne_of_gt hd)
  have hdiff : gate A1 B1 d r ≤ gate A2 B2 d r := by
    nlinarith
  refine ⟨r, ?_, ?_, hg1, ?_⟩
  · exact le_of_lt hrpos
  · exact le_of_lt hrlt
  · nlinarith

/-- Active interior vertex of gate 2 is a valid shared strict witness. -/
theorem shared_positive_of_active_vertex_two
    (A1 B1 A2 B2 d : ℝ)
    (hd : 0 < d)
    (hBpos : 0 < B2)
    (hBlt : B2 < 2 * d)
    (hnum : 0 < 4 * d * A2 + B2^2)
    (hactive : 0 ≤ 2 * d * (A1 - A2) + (B1 - B2) * B2) :
    ∃ r : ℝ,
      0 ≤ r ∧ r ≤ 1 ∧
      0 < gate A1 B1 d r ∧ 0 < gate A2 B2 d r := by
  let r : ℝ := B2 / (2 * d)
  have h2d : 0 < 2 * d := by positivity
  have hscale : (2 * d) * r = B2 := by
    dsimp [r]
    field_simp
  have hrpos : 0 < r := by
    nlinarith
  have hrlt : r < 1 := by
    nlinarith
  have hv : 4 * d * gate A2 B2 d r = 4 * d * A2 + B2^2 := by
    dsimp [r]
    exact scaled_vertex_value A2 B2 d (ne_of_gt hd)
  have hg2 : 0 < gate A2 B2 d r := by
    nlinarith
  have hdiffScaled :
      (2 * d) * (gate A1 B1 d r - gate A2 B2 d r) =
        2 * d * (A1 - A2) + (B1 - B2) * B2 := by
    dsimp [r]
    exact scaled_difference_at_vertex_two A1 B1 A2 B2 d (ne_of_gt hd)
  have hdiff : gate A2 B2 d r ≤ gate A1 B1 d r := by
    nlinarith
  refine ⟨r, ?_, ?_, ?_, hg2⟩
  · exact le_of_lt hrpos
  · exact le_of_lt hrlt
  · nlinarith

/-- Opposite signs of the affine difference at `0` and `1` force its unique
crossover `-c/q` strictly into `(0,1)`. -/
theorem crossover_inside_of_endpoint_sign_change
    (c q : ℝ)
    (hsign : c * (c + q) < 0) :
    0 < -c / q ∧ -c / q < 1 := by
  have hq : q ≠ 0 := by
    intro hq0
    subst q
    have hsquare : 0 ≤ c^2 := sq_nonneg c
    nlinarith
  have hc : c ≠ 0 := by
    intro hc0
    subst c
    norm_num at hsign
  have hscale : q * (-c / q) = -c := by
    field_simp [hq]
  rcases lt_or_gt_of_ne hc with hcneg | hcpos
  · have hcpq : 0 < c + q := by
      nlinarith
    have hqpos : 0 < q := by
      nlinarith
    constructor <;> nlinarith
  · have hcpq : c + q < 0 := by
      nlinarith
    have hqneg : q < 0 := by
      nlinarith
    constructor <;> nlinarith

/-- The common crossover value has a division-free scaled numerator. -/
theorem crossover_value_scaled
    (A1 B1 d c q : ℝ)
    (hq : q ≠ 0) :
    q^2 * gate A1 B1 d (-c / q) =
      A1 * q^2 - B1 * c * q - d * c^2 := by
  unfold gate
  field_simp [hq]
  ring

/-- At `c=A1-A2`, `q=B1-B2`, the crossover makes the two gates equal. -/
theorem crossover_gate_equality
    (A1 B1 A2 B2 d : ℝ)
    (hq : B1 - B2 ≠ 0) :
    gate A1 B1 d (-(A1 - A2) / (B1 - B2)) =
      gate A2 B2 d (-(A1 - A2) / (B1 - B2)) := by
  have hdiff := same_curvature_difference_affine
    A1 B1 A2 B2 d (-(A1 - A2) / (B1 - B2))
  have hzero :
      (A1 - A2) + (B1 - B2) * (-(A1 - A2) / (B1 - B2)) = 0 := by
    field_simp [hq]
    ring
  nlinarith

/-- The exact crossover candidate is a valid shared strict witness whenever the
endpoint sign-change and the scaled crossover numerator are both strict. -/
theorem shared_positive_of_crossover
    (A1 B1 A2 B2 d : ℝ)
    (hsign :
      (A1 - A2) * ((A1 - A2) + (B1 - B2)) < 0)
    (hnum :
      0 < A1 * (B1 - B2)^2 -
        B1 * (A1 - A2) * (B1 - B2) - d * (A1 - A2)^2) :
    ∃ r : ℝ,
      0 ≤ r ∧ r ≤ 1 ∧
      0 < gate A1 B1 d r ∧ 0 < gate A2 B2 d r := by
  let c : ℝ := A1 - A2
  let q : ℝ := B1 - B2
  have hq : q ≠ 0 := by
    intro hq0
    have hsign' : c * (c + q) < 0 := by
      simpa [c, q] using hsign
    rw [hq0] at hsign'
    have hsquare : 0 ≤ c^2 := sq_nonneg c
    nlinarith
  have hrange : 0 < -c / q ∧ -c / q < 1 := by
    apply crossover_inside_of_endpoint_sign_change c q
    simpa [c, q] using hsign
  have hscaled :
      q^2 * gate A1 B1 d (-c / q) =
        A1 * q^2 - B1 * c * q - d * c^2 :=
    crossover_value_scaled A1 B1 d c q hq
  have hq2 : 0 < q^2 := sq_pos_of_ne_zero hq
  have hg1 : 0 < gate A1 B1 d (-c / q) := by
    have hnum' : 0 < A1 * q^2 - B1 * c * q - d * c^2 := by
      simpa [c, q] using hnum
    nlinarith
  have heq : gate A1 B1 d (-c / q) = gate A2 B2 d (-c / q) := by
    simpa [c, q] using crossover_gate_equality A1 B1 A2 B2 d hq
  refine ⟨-c / q, le_of_lt hrange.1, le_of_lt hrange.2, hg1, ?_⟩
  nlinarith

/-- In the P5 specialization the common determinant term cancels exactly from
`Fb-Fg`; only the two affine bias envelopes choose the bottleneck. -/
theorem p5_barrier_parameter_difference_cancels
    (r D Eb0 eb Eg0 eg : ℝ) :
    ((109 - r) * D - 800 * (Eb0 + eb * r)) -
        ((109 - r) * D - 2400 * (Eg0 + eg * r)) =
      800 * ((3 * Eg0 - Eb0) + (3 * eg - eb) * r) := by
  ring

/-- Each separated regression gate is individually strictly feasible whenever
`eps>0`. -/
theorem separated_regression_each_passes
    (eps : ℝ) (heps : 0 < eps) :
    (0 < eps - (((1 : ℝ) / 4) - (1 / 4))^2) ∧
    (0 < eps - (((3 : ℝ) / 4) - (3 / 4))^2) := by
  simpa using And.intro heps heps

/-- If both shifted-square regression gates are strictly positive at one shared
`r`, then necessarily `eps > 1/16`. -/
theorem shared_regression_positive_implies_eps_gt_sixteenth
    (eps r : ℝ)
    (h1 : 0 < eps - (r - (1 : ℝ) / 4)^2)
    (h2 : 0 < eps - (r - (3 : ℝ) / 4)^2) :
    (1 : ℝ) / 16 < eps := by
  have hsquare : 0 ≤ (r - (1 : ℝ) / 2)^2 := sq_nonneg (r - (1 : ℝ) / 2)
  nlinarith

/-- Concrete strict obstruction: `eps=1/100` makes both gates separately PASS,
but no single shared `r` can make both strict. -/
theorem eps_one_hundred_no_shared_witness :
    ¬ ∃ r : ℝ,
      0 < (1 : ℝ) / 100 - (r - (1 : ℝ) / 4)^2 ∧
      0 < (1 : ℝ) / 100 - (r - (3 : ℝ) / 4)^2 := by
  rintro ⟨r, h1, h2⟩
  have h := shared_regression_positive_implies_eps_gt_sixteenth
    ((1 : ℝ) / 100) r h1 h2
  norm_num at h

/-- Boundary-only regression at `eps=1/16`, `r=1/2`. -/
theorem eps_one_sixteenth_boundary :
    (1 : ℝ) / 16 - ((1 : ℝ) / 2 - (1 : ℝ) / 4)^2 = 0 ∧
    (1 : ℝ) / 16 - ((1 : ℝ) / 2 - (3 : ℝ) / 4)^2 = 0 := by
  norm_num

/-- Positive crossover regression at `eps=1/10`, `r=1/2`: both margins are
exactly `3/80`. -/
theorem eps_one_tenth_crossover_margin :
    (1 : ℝ) / 10 - ((1 : ℝ) / 2 - (1 : ℝ) / 4)^2 = (3 : ℝ) / 80 ∧
    (1 : ℝ) / 10 - ((1 : ℝ) / 2 - (3 : ℝ) / 4)^2 = (3 : ℝ) / 80 := by
  norm_num

#print axioms same_curvature_difference_affine
#print axioms same_curvature_vertex_square
#print axioms scaled_vertex_value
#print axioms scaled_difference_at_vertex_one
#print axioms scaled_difference_at_vertex_two
#print axioms shared_positive_of_active_vertex_one
#print axioms shared_positive_of_active_vertex_two
#print axioms crossover_inside_of_endpoint_sign_change
#print axioms crossover_value_scaled
#print axioms crossover_gate_equality
#print axioms shared_positive_of_crossover
#print axioms p5_barrier_parameter_difference_cancels
#print axioms separated_regression_each_passes
#print axioms shared_regression_positive_implies_eps_gt_sixteenth
#print axioms eps_one_hundred_no_shared_witness
#print axioms eps_one_sixteenth_boundary
#print axioms eps_one_tenth_crossover_margin

end

end RouteBP5SharedROptimizer

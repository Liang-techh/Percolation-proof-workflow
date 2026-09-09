import Mathlib

namespace RouteBP5SameCellAnchorBudget

noncomputable section

/-- Pure lower-gain transport for the second implicit graph jet.  The actual
physical identity `M a'' = J2` and the correlated cap remain source-facing
hypotheses; this theorem does not materialize `M⁻¹`. -/
theorem second_jet_energy_le_of_lower_gain
    {A R : Type*}
    (QA : A → ℝ) (QR : R → ℝ) (M : A → R)
    (a2 : A) (J2 : R) (gamma H2 : ℝ)
    (hjet : M a2 = J2)
    (hlower : gamma * QA a2 ≤ QR (M a2))
    (hcap : QR J2 ≤ H2) :
    gamma * QA a2 ≤ H2 := by
  calc
    gamma * QA a2 ≤ QR (M a2) := hlower
    _ = QR J2 := by rw [hjet]
    _ ≤ H2 := hcap

/-- Division-free final consumer of the analytic Taylor/Jensen remainder bound
`4 * gamma * q ≤ H2`.  Here `q` is the fixed acceleration quadratic energy of
the affine-anchor remainder. -/
theorem same_cell_graph_affine_anchor_budget_of_four_mul
    (q Danchor gamma H2 : ℝ)
    (hgamma : 0 < gamma)
    (hremainder : 4 * gamma * q ≤ H2)
    (hgate : H2 ≤ 4 * gamma * Danchor) :
    q ≤ Danchor := by
  have hscaled : 4 * gamma * q ≤ 4 * gamma * Danchor :=
    le_trans hremainder hgate
  have hscale : 0 < 4 * gamma := by positivity
  exact (mul_le_mul_left hscale).mp hscaled

/-- Cell-radius specialization of the same trusted consumer.  A source/geometry
producer may supply `4*gamma*q ≤ K2*S²`; the checker needs only the final
polynomial gate `K2*S² ≤ 4*gamma*Danchor`. -/
theorem cell_radius_anchor_budget
    (q Danchor gamma K2 S : ℝ)
    (hgamma : 0 < gamma)
    (hremainder : 4 * gamma * q ≤ K2 * S ^ 2)
    (hgate : K2 * S ^ 2 ≤ 4 * gamma * Danchor) :
    q ≤ Danchor := by
  exact same_cell_graph_affine_anchor_budget_of_four_mul
    q Danchor gamma (K2 * S ^ 2) hgamma hremainder hgate

/-- Scalar triangle-inequality leaf behind the approximate-left-inverse route.
It deliberately exposes the transformed value `xm`; a later typed source seam
may instantiate it as `X (M v)` in the chosen normed space. -/
theorem abs_lower_of_approx_left_inverse
    (v xm kappa : ℝ)
    (herr : |v - xm| ≤ kappa * |v|) :
    (1 - kappa) * |v| ≤ |xm| := by
  have hsum : (v - xm) + xm = v := by ring
  have htri : |v| ≤ |v - xm| + |xm| := by
    calc
      |v| = |(v - xm) + xm| := by rw [hsum]
      _ ≤ |v - xm| + |xm| := abs_add _ _
  linarith

/-- Squared lower-gain leaf for the scalar approximate-left-inverse model.
Together with an exact bound on the `X`-image (`hX`) this yields the
source-friendly squared coefficient `(1-kappa)^2` without division or square
roots. -/
theorem scalar_lower_gain_sq_of_approx_left_inverse
    (v xm kappa chi qR : ℝ)
    (hkappa : kappa < 1)
    (herr : |v - xm| ≤ kappa * |v|)
    (hX : |xm| ^ 2 ≤ chi * qR) :
    (1 - kappa) ^ 2 * |v| ^ 2 ≤ chi * qR := by
  have habs : (1 - kappa) * |v| ≤ |xm| :=
    abs_lower_of_approx_left_inverse v xm kappa herr
  have hleft : 0 ≤ (1 - kappa) * |v| := by
    exact mul_nonneg (le_of_lt (sub_pos.mpr hkappa)) (abs_nonneg v)
  have hright : 0 ≤ |xm| := abs_nonneg xm
  have hprod :
      0 ≤ (|xm| - (1 - kappa) * |v|) *
        (|xm| + (1 - kappa) * |v|) := by
    exact mul_nonneg (sub_nonneg.mpr habs) (add_nonneg hright hleft)
  have hsq : ((1 - kappa) * |v|) ^ 2 ≤ |xm| ^ 2 := by
    nlinarith [hprod]
  calc
    (1 - kappa) ^ 2 * |v| ^ 2 = ((1 - kappa) * |v|) ^ 2 := by ring
    _ ≤ |xm| ^ 2 := hsq
    _ ≤ chi * qR := hX

/-- Final division-free anchor-budget consumer for the preconditioner route from
the mathematical handoff: if the analytic/source layer has established
`4(1-kappa)^2 q ≤ chi H2`, the rational checker gate is
`chi H2 ≤ 4(1-kappa)^2 Danchor`. -/
theorem preconditioned_anchor_budget
    (q Danchor kappa chi H2 : ℝ)
    (hkappa : kappa < 1)
    (hremainder : 4 * (1 - kappa) ^ 2 * q ≤ chi * H2)
    (hgate : chi * H2 ≤ 4 * (1 - kappa) ^ 2 * Danchor) :
    q ≤ Danchor := by
  have hpos : 0 < 1 - kappa := sub_pos.mpr hkappa
  have hscale : 0 < 4 * (1 - kappa) ^ 2 := by positivity
  have hscaled :
      4 * (1 - kappa) ^ 2 * q ≤ 4 * (1 - kappa) ^ 2 * Danchor :=
    le_trans hremainder hgate
  exact (mul_le_mul_left hscale).mp hscaled

/-- Scalar regression used to keep the whole-segment second-jet premise honest. -/
def cubicGraph (x : ℝ) : ℝ := x ^ 3

def cubicFirst (x : ℝ) : ℝ := 3 * x ^ 2

def cubicSecond (x : ℝ) : ℝ := 6 * x

def affineRemainder (f df : ℝ → ℝ) (x0 x1 : ℝ) : ℝ :=
  f x1 - f x0 - df x0 * (x1 - x0)

theorem cubic_anchor_second_zero : cubicSecond 0 = 0 := by
  norm_num [cubicSecond]

theorem cubic_anchor_affine_remainder_one :
    affineRemainder cubicGraph cubicFirst 0 1 = 1 := by
  norm_num [affineRemainder, cubicGraph, cubicFirst]

/-- Anchor-only curvature is therefore not a finite-segment certificate. -/
theorem anchor_only_second_jet_is_insufficient_regression :
    cubicSecond 0 = 0 ∧ affineRemainder cubicGraph cubicFirst 0 1 = 1 := by
  exact ⟨cubic_anchor_second_zero, cubic_anchor_affine_remainder_one⟩

/-- Scalar nonsingularity regression from the mathematical review.  For
`M=eps` and `R=x²/2`, the graph is `x²/(2 eps)`. -/
def scalarEpsGraph (eps x : ℝ) : ℝ := x ^ 2 / (2 * eps)

def scalarEpsFirst (eps x : ℝ) : ℝ := x / eps

theorem scalar_eps_anchor_affine_remainder_exact (eps : ℝ) :
    affineRemainder (scalarEpsGraph eps) (scalarEpsFirst eps) 0 1 =
      1 / (2 * eps) := by
  simp [affineRemainder, scalarEpsGraph, scalarEpsFirst]

/-- For every proposed positive uniform budget, a positive (hence nonsingular)
scalar mass `eps` exists whose anchor remainder is larger.  Thus nonsingularity
alone cannot replace a quantitative lower-gain premise. -/
theorem nonsingularity_alone_no_uniform_anchor_budget
    (B : ℝ) (hB : 0 < B) :
    ∃ eps : ℝ, 0 < eps ∧ B < scalarEpsGraph eps 1 := by
  refine ⟨1 / (4 * B), ?_, ?_⟩
  · positivity
  · have hBne : B ≠ 0 := ne_of_gt hB
    have heq : scalarEpsGraph (1 / (4 * B)) 1 = 2 * B := by
      field_simp [scalarEpsGraph, hBne]
      <;> ring
    rw [heq]
    linarith

#print axioms second_jet_energy_le_of_lower_gain
#print axioms same_cell_graph_affine_anchor_budget_of_four_mul
#print axioms cell_radius_anchor_budget
#print axioms abs_lower_of_approx_left_inverse
#print axioms scalar_lower_gain_sq_of_approx_left_inverse
#print axioms preconditioned_anchor_budget
#print axioms cubic_anchor_second_zero
#print axioms cubic_anchor_affine_remainder_one
#print axioms anchor_only_second_jet_is_insufficient_regression
#print axioms scalar_eps_anchor_affine_remainder_exact
#print axioms nonsingularity_alone_no_uniform_anchor_budget

end

end RouteBP5SameCellAnchorBudget

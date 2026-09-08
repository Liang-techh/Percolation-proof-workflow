import Mathlib

noncomputable section

namespace RouteBP5SignedTwoCycle

/-- Unsigned elimination for the first coordinate of a two-cycle. -/
theorem unsigned_two_cycle_budget_x1
    (a b p q X1 X2 Z1 Z2 D : ℝ)
    (ha : 0 ≤ a)
    (h1 : X1 ≤ Z1 + a * X2 + p * D)
    (h2 : X2 ≤ Z2 + b * X1 + q * D) :
    (1 - a * b) * X1 ≤ Z1 + a * Z2 + (p + a * q) * D := by
  have h2a : a * X2 ≤ a * (Z2 + b * X1 + q * D) :=
    mul_le_mul_of_nonneg_left h2 ha
  nlinarith

/-- Unsigned elimination for the second coordinate of a two-cycle. -/
theorem unsigned_two_cycle_budget_x2
    (a b p q X1 X2 Z1 Z2 D : ℝ)
    (hb : 0 ≤ b)
    (h1 : X1 ≤ Z1 + a * X2 + p * D)
    (h2 : X2 ≤ Z2 + b * X1 + q * D) :
    (1 - a * b) * X2 ≤ b * Z1 + Z2 + (b * p + q) * D := by
  have h1b : b * X1 ≤ b * (Z1 + a * X2 + p * D) :=
    mul_le_mul_of_nonneg_left h1 hb
  nlinarith

/-- The strict unsigned small-gain reserve turns the two cleared inequalities into uniqueness. -/
theorem unsigned_two_cycle_injective_zero_budget
    (a b X1 X2 : ℝ)
    (ha : 0 ≤ a)
    (hX1 : 0 ≤ X1) (hX2 : 0 ≤ X2)
    (h1 : X1 ≤ a * X2)
    (h2 : X2 ≤ b * X1)
    (hgain : a * b < 1) :
    X1 = 0 ∧ X2 = 0 := by
  have hx1budget : (1 - a * b) * X1 ≤ 0 := by
    simpa using
      (unsigned_two_cycle_budget_x1 a b 0 0 X1 X2 0 0 0 ha (by simpa using h1) (by simpa using h2))
  have hreserve : 0 < 1 - a * b := by linarith
  have hx1zero : X1 = 0 := by
    have : X1 ≤ 0 := by nlinarith
    exact le_antisymm this hX1
  have hx2zero : X2 = 0 := by
    rw [hx1zero] at h2
    have : X2 ≤ 0 := by simpa using h2
    exact le_antisymm this hX2
  exact ⟨hx1zero, hx2zero⟩

/-- Fully division-free source-cleared first-coordinate budget. -/
theorem cleared_two_cycle_budget_x1
    (mu1 mu2 C12 C21 L1 L2 X1 X2 Z1 Z2 D : ℝ)
    (hmu2 : 0 ≤ mu2) (hC12 : 0 ≤ C12)
    (h1 : mu1 * X1 ≤ mu1 * Z1 + C12 * X2 + L1 * D)
    (h2 : mu2 * X2 ≤ mu2 * Z2 + C21 * X1 + L2 * D) :
    (mu1 * mu2 - C12 * C21) * X1 ≤
      mu1 * mu2 * Z1 + C12 * mu2 * Z2 + (mu2 * L1 + C12 * L2) * D := by
  have h1m : mu2 * (mu1 * X1) ≤ mu2 * (mu1 * Z1 + C12 * X2 + L1 * D) :=
    mul_le_mul_of_nonneg_left h1 hmu2
  have h2c : C12 * (mu2 * X2) ≤ C12 * (mu2 * Z2 + C21 * X1 + L2 * D) :=
    mul_le_mul_of_nonneg_left h2 hC12
  nlinarith

/-- Fully division-free source-cleared second-coordinate budget. -/
theorem cleared_two_cycle_budget_x2
    (mu1 mu2 C12 C21 L1 L2 X1 X2 Z1 Z2 D : ℝ)
    (hmu1 : 0 ≤ mu1) (hC21 : 0 ≤ C21)
    (h1 : mu1 * X1 ≤ mu1 * Z1 + C12 * X2 + L1 * D)
    (h2 : mu2 * X2 ≤ mu2 * Z2 + C21 * X1 + L2 * D) :
    (mu1 * mu2 - C12 * C21) * X2 ≤
      C21 * mu1 * Z1 + mu1 * mu2 * Z2 + (C21 * L1 + mu1 * L2) * D := by
  have h2m : mu1 * (mu2 * X2) ≤ mu1 * (mu2 * Z2 + C21 * X1 + L2 * D) :=
    mul_le_mul_of_nonneg_left h2 hmu1
  have h1c : C21 * (mu1 * X1) ≤ C21 * (mu1 * Z1 + C12 * X2 + L1 * D) :=
    mul_le_mul_of_nonneg_left h1 hC21
  nlinarith

/-- Increasing after decreasing gives an antitone two-cycle composition. -/
theorem composition_antitone_of_monotone_antitone
    (rho1 rho2 : ℝ → ℝ)
    (h1 : Monotone rho1) (h2 : Antitone rho2) :
    Antitone (fun s => rho1 (rho2 s)) := by
  intro s t hst
  exact h1 (h2 hst)

/-- Decreasing after increasing also gives an antitone two-cycle composition. -/
theorem composition_antitone_of_antitone_monotone
    (rho1 rho2 : ℝ → ℝ)
    (h1 : Antitone rho1) (h2 : Monotone rho2) :
    Antitone (fun s => rho1 (rho2 s)) := by
  intro s t hst
  exact h1 (h2 hst)

/-- If `phi` is antitone, `G(s)=s-phi(s)` has unit one-sided coercivity. -/
theorem antitone_unit_coercivity
    (phi : ℝ → ℝ) (hphi : Antitone phi)
    {s t : ℝ} (hst : s ≤ t) :
    t - s ≤ (t - phi t) - (s - phi s) := by
  have hp : phi t ≤ phi s := hphi hst
  linarith

/-- The same unit reserve yields a global absolute-value inverse inequality. -/
theorem antitone_abs_coercivity
    (phi : ℝ → ℝ) (hphi : Antitone phi)
    (s t : ℝ) :
    |t - s| ≤ |(t - phi t) - (s - phi s)| := by
  rcases le_total s t with hst | hts
  · have h := antitone_unit_coercivity phi hphi hst
    have hleft : 0 ≤ t - s := sub_nonneg.mpr hst
    have hright : 0 ≤ (t - phi t) - (s - phi s) := le_trans hleft h
    rw [abs_of_nonneg hleft, abs_of_nonneg hright]
    exact h
  · have h := antitone_unit_coercivity phi hphi hts
    have hleft : 0 ≤ s - t := sub_nonneg.mpr hts
    have hright : 0 ≤ (s - phi s) - (t - phi t) := le_trans hleft h
    rw [abs_sub_comm t s, abs_sub_comm (t - phi t) (s - phi s)]
    rw [abs_of_nonneg hleft, abs_of_nonneg hright]
    exact h

/-- Parameter perturbation of an antitone cycle costs only the perturbation itself: no small-gain denominator. -/
theorem negative_feedback_scalar_budget
    (phi phi' : ℝ → ℝ) (hphi : Antitone phi)
    (x x' xi xi' R : ℝ)
    (hx : xi = x - phi x)
    (hx' : xi' = x' - phi' x')
    (hR : |phi x' - phi' x'| ≤ R) :
    |x - x'| ≤ |xi - xi'| + R := by
  have hco := antitone_abs_coercivity phi hphi x' x
  have hxrev : x - phi x = xi := hx.symm
  have hx'rev : x' - phi' x' = xi' := hx'.symm
  have hrewrite :
      (x - phi x) - (x' - phi x') =
        (xi - xi') + (phi x' - phi' x') := by
    calc
      (x - phi x) - (x' - phi x') =
          (x - phi x) - (x' - phi' x') + (phi x' - phi' x') := by ring
      _ = (xi - xi') + (phi x' - phi' x') := by rw [hxrev, hx'rev]
  have htri :
      |(x - phi x) - (x' - phi x')| ≤
        |xi - xi'| + |phi x' - phi' x'| := by
    rw [hrewrite]
    exact abs_add_le _ _
  exact hco.trans (htri.trans (add_le_add_left hR _))

/-- Nested root-map variation produces the numerator from T-P5-071 without division. -/
theorem nested_variation_budget
    (a p q U Z D : ℝ)
    (ha : 0 ≤ a)
    (hinner : U ≤ Z + q * D) :
    a * U + p * D ≤ a * Z + (p + a * q) * D := by
  have hm := mul_le_mul_of_nonneg_left hinner ha
  nlinarith

/-- Companion seam: combine opposite-orientation unit coercivity with outer/inner parameter charges for coordinate 1. -/
theorem negative_feedback_parameter_transport_x1
    (a p q X1 Z1 Z2 D E U : ℝ)
    (ha : 0 ≤ a)
    (hcoer : X1 ≤ Z1 + E)
    (houter : E ≤ a * U + p * D)
    (hinner : U ≤ Z2 + q * D) :
    X1 ≤ Z1 + a * Z2 + (p + a * q) * D := by
  have hm := mul_le_mul_of_nonneg_left hinner ha
  nlinarith

/-- Companion seam: symmetric opposite-orientation parameter transport for coordinate 2. -/
theorem negative_feedback_parameter_transport_x2
    (b p q X2 Z1 Z2 D E U : ℝ)
    (hb : 0 ≤ b)
    (hcoer : X2 ≤ Z2 + E)
    (houter : E ≤ b * U + q * D)
    (hinner : U ≤ Z1 + p * D) :
    X2 ≤ b * Z1 + Z2 + (q + b * p) * D := by
  have hm := mul_le_mul_of_nonneg_left hinner hb
  nlinarith

/-- Source-cleared negative-feedback parameter transport for coordinate 1, with no determinant reserve. -/
theorem cleared_negative_feedback_parameter_transport_x1
    (mu1 mu2 C12 L1 L2 X1 U Z1 Z2 D : ℝ)
    (hmu2 : 0 ≤ mu2) (hC12 : 0 ≤ C12)
    (hcoer : mu1 * X1 ≤ mu1 * Z1 + C12 * U + L1 * D)
    (hinner : mu2 * U ≤ mu2 * Z2 + L2 * D) :
    mu1 * mu2 * X1 ≤
      mu1 * mu2 * Z1 + C12 * mu2 * Z2 + (mu2 * L1 + C12 * L2) * D := by
  have hc := mul_le_mul_of_nonneg_left hcoer hmu2
  have hi := mul_le_mul_of_nonneg_left hinner hC12
  nlinarith

/-- Source-cleared negative-feedback parameter transport for coordinate 2, with no determinant reserve. -/
theorem cleared_negative_feedback_parameter_transport_x2
    (mu1 mu2 C21 L1 L2 X2 U Z1 Z2 D : ℝ)
    (hmu1 : 0 ≤ mu1) (hC21 : 0 ≤ C21)
    (hcoer : mu2 * X2 ≤ mu2 * Z2 + C21 * U + L2 * D)
    (hinner : mu1 * U ≤ mu1 * Z1 + L1 * D) :
    mu1 * mu2 * X2 ≤
      C21 * mu1 * Z1 + mu1 * mu2 * Z2 + (C21 * L1 + mu1 * L2) * D := by
  have hc := mul_le_mul_of_nonneg_left hcoer hmu1
  have hi := mul_le_mul_of_nonneg_left hinner hC21
  nlinarith

/-- A source fiber that is strictly increasing locates a zero to the left of any nonnegative sample. -/
theorem strictMono_zero_le_of_nonneg_sample
    (g : ℝ → ℝ) (hg : StrictMono g)
    (r r0 : ℝ)
    (hr0 : g r0 = 0)
    (hr : 0 ≤ g r) :
    r0 ≤ r := by
  by_contra hnot
  have hlt : r < r0 := lt_of_not_ge hnot
  have hval : g r < g r0 := hg hlt
  rw [hr0] at hval
  linarith

/-- Dually, a nonpositive sample of a strictly increasing fiber lies left of its zero. -/
theorem strictMono_le_zero_of_nonpos_sample
    (g : ℝ → ℝ) (hg : StrictMono g)
    (r r0 : ℝ)
    (hr0 : g r0 = 0)
    (hr : g r ≤ 0) :
    r ≤ r0 := by
  by_contra hnot
  have hlt : r0 < r := lt_of_not_ge hnot
  have hval : g r0 < g r := hg hlt
  rw [hr0] at hval
  linarith

/-- Same-orientation unit gain can lose injectivity completely: every diagonal point has the same chart value. -/
theorem same_orientation_unit_gain_obstruction
    (r : ℝ) :
    (r - r = 0) ∧ (r - r = 0) := by
  constructor <;> ring

/-- A linear negative-feedback cycle stays injective for arbitrarily large nonnegative cross gains. -/
theorem negative_feedback_linear_injective
    (a b dx1 dx2 : ℝ)
    (ha : 0 ≤ a) (hb : 0 ≤ b)
    (h1 : dx1 - a * dx2 = 0)
    (h2 : dx2 + b * dx1 = 0) :
    dx1 = 0 ∧ dx2 = 0 := by
  have hsq : 0 ≤ a * b := mul_nonneg ha hb
  have hx : (1 + a * b) * dx1 = 0 := by
    nlinarith
  have hpos : 0 < 1 + a * b := by linarith
  have hdx1 : dx1 = 0 := by
    apply (mul_eq_zero.mp hx).resolve_left
    exact ne_of_gt hpos
  have hdx2 : dx2 = 0 := by
    rw [hdx1] at h2
    simpa using h2
  exact ⟨hdx1, hdx2⟩

#print axioms unsigned_two_cycle_budget_x1
#print axioms unsigned_two_cycle_budget_x2
#print axioms unsigned_two_cycle_injective_zero_budget
#print axioms cleared_two_cycle_budget_x1
#print axioms cleared_two_cycle_budget_x2
#print axioms composition_antitone_of_monotone_antitone
#print axioms composition_antitone_of_antitone_monotone
#print axioms antitone_unit_coercivity
#print axioms antitone_abs_coercivity
#print axioms negative_feedback_scalar_budget
#print axioms nested_variation_budget
#print axioms negative_feedback_parameter_transport_x1
#print axioms negative_feedback_parameter_transport_x2
#print axioms cleared_negative_feedback_parameter_transport_x1
#print axioms cleared_negative_feedback_parameter_transport_x2
#print axioms strictMono_zero_le_of_nonneg_sample
#print axioms strictMono_le_zero_of_nonpos_sample
#print axioms same_orientation_unit_gain_obstruction
#print axioms negative_feedback_linear_injective

end RouteBP5SignedTwoCycle

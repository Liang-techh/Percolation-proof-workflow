import Mathlib

noncomputable section

namespace RouteBP4ShiftedCommonReserve

/-- Exact interpolation identity for a quadratic row `A*t^2 - G*t + P`. -/
theorem quadratic_chord_identity
    (A G P a b t : ℝ) :
    (b - a) * (A * t ^ 2 - G * t + P)
      = (b - t) * (A * a ^ 2 - G * a + P)
        + (t - a) * (A * b ^ 2 - G * b + P)
        - A * (b - a) * (t - a) * (b - t) := by
  ring

/--
If a quadratic row is nonpositive at both ends of `[a,b]`, then inside the
interval it lies below the universal parabola determined by any lower
curvature bound `A0 ≤ A`.
-/
theorem quadratic_below_endpoint_chord
    (A G P A0 a b t : ℝ)
    (hab : a < b)
    (hta : a ≤ t)
    (htb : t ≤ b)
    (hA : A0 ≤ A)
    (hqa : A * a ^ 2 - G * a + P ≤ 0)
    (hqb : A * b ^ 2 - G * b + P ≤ 0) :
    A * t ^ 2 - G * t + P ≤ -A0 * (t - a) * (b - t) := by
  have hwidth : 0 < b - a := sub_pos.mpr hab
  have hta0 : 0 ≤ t - a := sub_nonneg.mpr hta
  have hbt0 : 0 ≤ b - t := sub_nonneg.mpr htb
  have hgap : 0 ≤ (t - a) * (b - t) := mul_nonneg hta0 hbt0
  have hleft :
      (b - t) * (A * a ^ 2 - G * a + P) ≤ 0 :=
    mul_nonpos_of_nonneg_of_nonpos hbt0 hqa
  have hright :
      (t - a) * (A * b ^ 2 - G * b + P) ≤ 0 :=
    mul_nonpos_of_nonneg_of_nonpos hta0 hqb
  have hcurv :
      A0 * ((b - a) * ((t - a) * (b - t)))
        ≤ A * ((b - a) * ((t - a) * (b - t))) := by
    exact mul_le_mul_of_nonneg_right hA (mul_nonneg (le_of_lt hwidth) hgap)
  have hid := quadratic_chord_identity A G P a b t
  have hscaled :
      (b - a) * (A * t ^ 2 - G * t + P)
        ≤ (b - a) * (-A0 * (t - a) * (b - t)) := by
    nlinarith
  exact (mul_le_mul_left hwidth).mp hscaled

/-- Exact square-completion identity for the theta-weighted reserve. -/
theorem shifted_charge_complete_square
    (A0 a b m t : ℝ) :
    ((A0 * (a + b) - m) ^ 2 - 4 * A0 ^ 2 * a * b)
        - (2 * A0 * t - (A0 * (a + b) - m)) ^ 2
      = 4 * A0 * (A0 * (t - a) * (b - t) - m * t) := by
  ring

/--
Division-free common-interval consumer.  The supplied rational witness `t`
need only satisfy the affine center equation; no square root or row root is
used by the semantic theorem.
-/
theorem common_interval_shifted_reserve_mul
    (A G P A0 a b m t : ℝ)
    (hA0 : 0 < A0)
    (hab : a < b)
    (hta : a ≤ t)
    (htb : t ≤ b)
    (hA : A0 ≤ A)
    (hqa : A * a ^ 2 - G * a + P ≤ 0)
    (hqb : A * b ^ 2 - G * b + P ≤ 0)
    (hcenter : 2 * A0 * t = A0 * (a + b) - m) :
    4 * A0 * (A * t ^ 2 - G * t + P + m * t)
      ≤ -((A0 * (a + b) - m) ^ 2 - 4 * A0 ^ 2 * a * b) := by
  have hbelow :=
    quadratic_below_endpoint_chord A G P A0 a b t hab hta htb hA hqa hqb
  have hcost :
      A * t ^ 2 - G * t + P + m * t
        ≤ -(A0 * (t - a) * (b - t) - m * t) := by
    nlinarith
  have hscale :
      4 * A0 * (A * t ^ 2 - G * t + P + m * t)
        ≤ 4 * A0 * (-(A0 * (t - a) * (b - t) - m * t)) := by
    exact mul_le_mul_of_nonneg_left hcost (by nlinarith)
  have hcomp := shifted_charge_complete_square A0 a b m t
  have hcenter0 : 2 * A0 * t - (A0 * (a + b) - m) = 0 := by
    linarith
  rw [hcenter0] at hcomp
  norm_num at hcomp
  nlinarith

/-- Nonnegative discriminant gives weak charged feasibility at the shifted witness. -/
theorem common_interval_shifted_feasible
    (A G P A0 a b m t : ℝ)
    (hA0 : 0 < A0)
    (hab : a < b)
    (hta : a ≤ t)
    (htb : t ≤ b)
    (hA : A0 ≤ A)
    (hqa : A * a ^ 2 - G * a + P ≤ 0)
    (hqb : A * b ^ 2 - G * b + P ≤ 0)
    (hcenter : 2 * A0 * t = A0 * (a + b) - m)
    (hD : 0 ≤ (A0 * (a + b) - m) ^ 2 - 4 * A0 ^ 2 * a * b) :
    A * t ^ 2 - G * t + P + m * t ≤ 0 := by
  have hreserve := common_interval_shifted_reserve_mul
    A G P A0 a b m t hA0 hab hta htb hA hqa hqb hcenter
  nlinarith

/-- Positive discriminant gives strict charged feasibility at the shifted witness. -/
theorem common_interval_shifted_strict
    (A G P A0 a b m t : ℝ)
    (hA0 : 0 < A0)
    (hab : a < b)
    (hta : a ≤ t)
    (htb : t ≤ b)
    (hA : A0 ≤ A)
    (hqa : A * a ^ 2 - G * a + P ≤ 0)
    (hqb : A * b ^ 2 - G * b + P ≤ 0)
    (hcenter : 2 * A0 * t = A0 * (a + b) - m)
    (hD : 0 < (A0 * (a + b) - m) ^ 2 - 4 * A0 ^ 2 * a * b) :
    A * t ^ 2 - G * t + P + m * t < 0 := by
  have hreserve := common_interval_shifted_reserve_mul
    A G P A0 a b m t hA0 hab hta htb hA hqa hqb hcenter
  nlinarith

/-- The same shifted witness/reserve applies simultaneously to an arbitrary row family. -/
theorem common_interval_shifted_reserve_family
    {ι : Type*}
    (A G P : ι → ℝ)
    (A0 a b m t : ℝ)
    (hA0 : 0 < A0)
    (hab : a < b)
    (hta : a ≤ t)
    (htb : t ≤ b)
    (hA : ∀ i, A0 ≤ A i)
    (hqa : ∀ i, A i * a ^ 2 - G i * a + P i ≤ 0)
    (hqb : ∀ i, A i * b ^ 2 - G i * b + P i ≤ 0)
    (hcenter : 2 * A0 * t = A0 * (a + b) - m) :
    ∀ i,
      4 * A0 * (A i * t ^ 2 - G i * t + P i + m * t)
        ≤ -((A0 * (a + b) - m) ^ 2 - 4 * A0 ^ 2 * a * b) := by
  intro i
  exact common_interval_shifted_reserve_mul
    (A i) (G i) (P i) A0 a b m t hA0 hab hta htb (hA i) (hqa i) (hqb i) hcenter

/--
Small-charge branch: an affine-center witness automatically lies in the
positive common interval.  This is the division-free semantic companion to a
rational checker constructing `t = (A0*(a+b)-m)/(2*A0)`.
-/
theorem shifted_witness_mem_interval
    (a b A0 m t : ℝ)
    (ha : 0 < a)
    (hab : a < b)
    (hA0 : 0 < A0)
    (hm0 : 0 ≤ m)
    (hm : m ≤ A0 * (b - a))
    (hcenter : 2 * A0 * t = A0 * (a + b) - m) :
    0 < t ∧ a ≤ t ∧ t < b := by
  have h2A : 0 < 2 * A0 := by nlinarith
  have hleftScaled : (2 * A0) * a ≤ (2 * A0) * t := by
    nlinarith
  have hta : a ≤ t := (mul_le_mul_left h2A).mp hleftScaled
  have hrightScaled : (2 * A0) * t ≤ (2 * A0) * ((a + b) / 2) := by
    nlinarith
  have htMid : t ≤ (a + b) / 2 := (mul_le_mul_left h2A).mp hrightScaled
  have hmidb : (a + b) / 2 < b := by nlinarith
  exact ⟨lt_of_lt_of_le ha hta, hta, lt_of_le_of_lt htMid hmidb⟩

/-- Exact regression: the midpoint fails while the shifted rational witness passes. -/
theorem midpoint_fails_shifted_passes_1_4_19_20 :
    (((5 : ℝ) / 2 - 1) * ((5 : ℝ) / 2 - 4)
        + ((19 : ℝ) / 20) * ((5 : ℝ) / 2) = (1 : ℝ) / 8)
    ∧ (2 * (1 : ℝ) * ((81 : ℝ) / 40)
        = (1 : ℝ) * (1 + 4) - (19 : ℝ) / 20)
    ∧ (((1 : ℝ) * (1 + 4) - (19 : ℝ) / 20) ^ 2
        - 4 * (1 : ℝ) ^ 2 * 1 * 4 = (161 : ℝ) / 400)
    ∧ (((81 : ℝ) / 40 - 1) * ((81 : ℝ) / 40 - 4)
        + ((19 : ℝ) / 20) * ((81 : ℝ) / 40) = -(161 : ℝ) / 1600) := by
  norm_num

/-- `D > 0` alone is unsound: the large-charge branch puts the vertex outside `[1,4]`. -/
theorem large_discriminant_wrong_branch_counterexample :
    (((1 : ℝ) * (1 + 4) - 10) ^ 2 - 4 * (1 : ℝ) ^ 2 * 1 * 4 = 9)
    ∧ (2 * (1 : ℝ) * (-(5 : ℝ) / 2) = (1 : ℝ) * (1 + 4) - 10)
    ∧ (-(5 : ℝ) / 2 < 1)
    ∧ ∀ t : ℝ, 1 ≤ t → t ≤ 4 →
        0 < (t - 1) * (t - 4) + 10 * t := by
  constructor
  · norm_num
  constructor
  · norm_num
  constructor
  · norm_num
  · intro t ht _htb
    have h1 : 0 < t + 1 := by nlinarith
    have h4 : 0 < t + 4 := by nlinarith
    have hp : 0 < (t + 1) * (t + 4) := mul_pos h1 h4
    nlinarith

/-- Exact boundary row at the sharp charge `m=1`. -/
theorem shifted_boundary_1_4_1 (t : ℝ) :
    (t - 1) * (t - 4) + t = (t - 2) ^ 2 := by
  ring

/-- Above the sharp charge, the extremal row has no positive witness. -/
theorem charge_above_one_impossible_1_4
    (m t : ℝ) (hm : 1 < m) (ht : 0 < t) :
    0 < (t - 1) * (t - 4) + m * t := by
  have hprod : 0 < (m - 1) * t := mul_pos (sub_pos.mpr hm) ht
  have hsq : 0 ≤ (t - 2) ^ 2 := sq_nonneg (t - 2)
  nlinarith

#print axioms quadratic_chord_identity
#print axioms quadratic_below_endpoint_chord
#print axioms shifted_charge_complete_square
#print axioms common_interval_shifted_reserve_mul
#print axioms common_interval_shifted_feasible
#print axioms common_interval_shifted_strict
#print axioms common_interval_shifted_reserve_family
#print axioms shifted_witness_mem_interval
#print axioms midpoint_fails_shifted_passes_1_4_19_20
#print axioms large_discriminant_wrong_branch_counterexample
#print axioms shifted_boundary_1_4_1
#print axioms charge_above_one_impossible_1_4

end RouteBP4ShiftedCommonReserve

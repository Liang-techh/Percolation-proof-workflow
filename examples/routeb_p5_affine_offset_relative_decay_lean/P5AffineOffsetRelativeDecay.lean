import Mathlib

noncomputable section

namespace RouteBP5AffineOffsetRelativeDecay

/-- A pure componentwise relative envelope forces exact vanishing on every zero-coordinate slice. -/
theorem componentwise_relative_implies_zero_slice
    {α : Type*} (R coord : α → ℝ) (κ : ℝ) (x : α)
    (hrel : |R x| ≤ κ * |coord x|)
    (hzero : coord x = 0) :
    R x = 0 := by
  have hz : |R x| ≤ 0 := by
    simpa [hzero] using hrel
  have habs : |R x| = 0 := le_antisymm hz (abs_nonneg _)
  exact abs_eq_zero.mp habs

/-- Exact bias-plus-factor decomposition gives the affine absolute-value envelope. -/
theorem affine_envelope_from_bias_factor
    (R b v q β κ : ℝ)
    (hdef : R = b + v * q)
    (hb : |b| ≤ β)
    (hq : |q| ≤ κ) :
    |R| ≤ β + κ * |v| := by
  calc
    |R| = |b + v * q| := by rw [hdef]
    _ ≤ |b| + |v * q| := abs_add _ _
    _ = |b| + |v| * |q| := by rw [abs_mul]
    _ ≤ β + |v| * κ :=
      add_le_add hb (mul_le_mul_of_nonneg_left hq (abs_nonneg v))
    _ = β + κ * |v| := by ring

/-- Division-free absorption into a requested relative factor on a gap cell. -/
theorem affine_offset_gap_absorption
    (R β κ q δ v : ℝ)
    (hqk : κ ≤ q)
    (hδ : 0 ≤ δ)
    (hgap : δ ≤ |v|)
    (henv : |R| ≤ β + κ * |v|)
    (hbudget : β ≤ (q - κ) * δ) :
    |R| ≤ q * |v| := by
  have hscale : (q - κ) * δ ≤ (q - κ) * |v| :=
    mul_le_mul_of_nonneg_left hgap (sub_nonneg.mpr hqk)
  have hb : β ≤ (q - κ) * |v| := le_trans hbudget hscale
  calc
    |R| ≤ β + κ * |v| := henv
    _ ≤ (q - κ) * |v| + κ * |v| := add_le_add_right hb (κ * |v|)
    _ = q * |v| := by ring

/-- The sharp strict gate `β < (1-κ)δ` yields strict decay on `|v| ≥ δ`. -/
theorem affine_offset_gap_strict_decay
    (R β κ δ v : ℝ)
    (hκ : κ < 1)
    (hδ : 0 < δ)
    (hgap : δ ≤ |v|)
    (henv : |R| ≤ β + κ * |v|)
    (hbudget : β < (1 - κ) * δ) :
    |R| < |v| := by
  have hpos : 0 < 1 - κ := sub_pos.mpr hκ
  have hscale : (1 - κ) * δ ≤ (1 - κ) * |v| :=
    mul_le_mul_of_nonneg_left hgap (le_of_lt hpos)
  have hb : β < (1 - κ) * |v| := lt_of_lt_of_le hbudget hscale
  calc
    |R| ≤ β + κ * |v| := henv
    _ < (1 - κ) * |v| + κ * |v| := add_lt_add_right hb (κ * |v|)
    _ = |v| := by ring

/-- Componentwise nonnegative matrix envelope plus a strict radius budget closes a finite box. -/
theorem box_envelope_strict_invariant
    {n : ℕ}
    (β r : Fin n → ℝ)
    (A : Fin n → Fin n → ℝ)
    (v R : Fin n → ℝ)
    (hA : ∀ i j, 0 ≤ A i j)
    (hv : ∀ j, |v j| ≤ r j)
    (henv : ∀ i, |R i| ≤ β i + ∑ j, A i j * |v j|)
    (hgate : ∀ i, β i + ∑ j, A i j * r j < r i) :
    ∀ i, |R i| < r i := by
  intro i
  have hsum : (∑ j, A i j * |v j|) ≤ ∑ j, A i j * r j := by
    apply Finset.sum_le_sum
    intro j _
    exact mul_le_mul_of_nonneg_left (hv j) (hA i j)
  exact lt_of_le_of_lt
    (le_trans (henv i) (add_le_add_left hsum (β i)))
    (hgate i)

/-- The scalar strict-box consumer is the one-dimensional form of the matrix budget. -/
theorem scalar_affine_box_strict_invariant
    (R β κ r v : ℝ)
    (hκ : 0 ≤ κ)
    (hv : |v| ≤ r)
    (henv : |R| ≤ β + κ * |v|)
    (hgate : β + κ * r < r) :
    |R| < r := by
  have hscale : κ * |v| ≤ κ * r := mul_le_mul_of_nonneg_left hv hκ
  exact lt_of_le_of_lt
    (le_trans henv (add_le_add_left hscale β))
    hgate

/-- A strict box budget is exactly positivity of its division-free reserve. -/
theorem box_budget_iff_positive_reserve
    (β S r : ℝ) :
    β + S < r ↔ 0 < r - β - S := by
  constructor <;> intro h <;> linarith

/-- Equality at the box budget boundary has zero strict reserve. -/
theorem box_budget_equality_zero_reserve
    (β S r : ℝ)
    (h : β + S = r) :
    r - β - S = 0 := by
  linarith

/-- Equality at the gap threshold likewise has zero strict reserve. -/
theorem gap_budget_equality_zero_reserve
    (β κ δ : ℝ)
    (h : β = (1 - κ) * δ) :
    (1 - κ) * δ - β = 0 := by
  linarith

/-- Origin-only vanishing cannot certify a transverse zero slice: `(0,1/2)` fails every finite factor. -/
theorem transverse_slice_counterexample
    (κ : ℝ) :
    ¬ |(1 / 2 : ℝ)| ≤ κ * |(0 : ℝ)| := by
  norm_num

/-- A positive coarse additive allowance is not by itself a nonzero-source obstruction. -/
theorem coarse_beta_is_not_nonzero_witness
    (β κ v : ℝ)
    (hβ : 0 ≤ β) :
    κ * |v| ≤ β + κ * |v| := by
  linarith

#print axioms componentwise_relative_implies_zero_slice
#print axioms affine_envelope_from_bias_factor
#print axioms affine_offset_gap_absorption
#print axioms affine_offset_gap_strict_decay
#print axioms box_envelope_strict_invariant
#print axioms scalar_affine_box_strict_invariant
#print axioms box_budget_iff_positive_reserve
#print axioms box_budget_equality_zero_reserve
#print axioms gap_budget_equality_zero_reserve
#print axioms transverse_slice_counterexample
#print axioms coarse_beta_is_not_nonzero_witness

end RouteBP5AffineOffsetRelativeDecay

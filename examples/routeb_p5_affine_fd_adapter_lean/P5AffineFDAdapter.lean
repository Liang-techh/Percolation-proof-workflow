import Mathlib.Data.Fin.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# Route-B P5 affine FD-envelope adapters

This focused sidecar formalizes the source-independent interface mathematics in
`review-T-P5-009-liuguanyi-20260907T0606.md`.

The input is an affine component envelope `|e| ≤ s*cap+b`.  The file proves:

* the exact division-free punctured-domain route to a homogeneous relative gain;
* the equilibrium-safe centered-increment route;
* a six-channel weighted-dual mixed relative-plus-additive square charge;
* an explicit anchored counterexample showing that `err 0 = 0` plus a positive
  static offset envelope does not by itself imply any finite relative gain.

No source/DH/Float64 binding, same-domain P8 coverage, or P5/M4 admission is
asserted here.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP5AffineFDAdapter

noncomputable section

abbrev Vec6 := Fin 6 → ℝ

/-- The division-free form of the punctured-domain affine-envelope adapter.
The state floor converts the positive offset `b` into a homogeneous charge. -/
theorem affine_envelope_division_free
    (s b cap K nu x e : ℝ)
    (hs : 0 ≤ s) (hb : 0 ≤ b) (hnu : 0 < nu)
    (henv : |e| ≤ s * cap + b)
    (hcap : cap ≤ K * |x|)
    (hfloor : nu ≤ |x|) :
    nu * |e| ≤ (s * K * nu + b) * |x| := by
  have hcapScaled : s * cap ≤ s * (K * |x|) :=
    mul_le_mul_of_nonneg_left hcap hs
  have henv' : |e| ≤ s * K * |x| + b := by
    nlinarith
  have hnu0 : 0 ≤ nu := le_of_lt hnu
  have hmul : nu * |e| ≤ nu * (s * K * |x| + b) :=
    mul_le_mul_of_nonneg_left henv' hnu0
  have hbFloor : b * nu ≤ b * |x| :=
    mul_le_mul_of_nonneg_left hfloor hb
  nlinarith

/-- If the downstream coefficient `rho` pays the division-free budget
`s*K*nu+b ≤ rho*nu`, the affine envelope becomes homogeneous on a domain with
`|x| ≥ nu > 0`. -/
theorem affine_envelope_relative_of_floor
    (s b cap K nu x e rho : ℝ)
    (hs : 0 ≤ s) (hb : 0 ≤ b) (hnu : 0 < nu)
    (henv : |e| ≤ s * cap + b)
    (hcap : cap ≤ K * |x|)
    (hfloor : nu ≤ |x|)
    (hbudget : s * K * nu + b ≤ rho * nu) :
    |e| ≤ rho * |x| := by
  have hdiv := affine_envelope_division_free
    s b cap K nu x e hs hb hnu henv hcap hfloor
  have hbudgetMul :
      (s * K * nu + b) * |x| ≤ (rho * nu) * |x| :=
    mul_le_mul_of_nonneg_right hbudget (abs_nonneg x)
  have hscaled : nu * |e| ≤ nu * (rho * |x|) := by
    calc
      nu * |e| ≤ (s * K * nu + b) * |x| := hdiv
      _ ≤ (rho * nu) * |x| := hbudgetMul
      _ = nu * (rho * |x|) := by ring
  nlinarith

/-- The correct equilibrium-containing bridge uses a centered increment of the
actual error map, rather than reinterpreting a static affine offset. -/
theorem centered_increment_relative
    {X : Type*}
    (err : X → ℝ) (z z0 : X) (g : X → ℝ) (L : ℝ)
    (h0 : err z0 = 0)
    (hinc : |err z - err z0| ≤ L * g z) :
    |err z| ≤ L * g z := by
  simpa [h0] using hinc

/-- A structured version of the centered adapter.  The source must provide the
split itself; the old affine numerical envelope does not construct it. -/
theorem split_centered_increment_relative
    {X : Type*}
    (err slopePart remPart cap g : X → ℝ)
    (z z0 : X) (s K Lrem : ℝ)
    (hs : 0 ≤ s)
    (hcap : cap z ≤ K * g z)
    (hslope : |slopePart z| ≤ s * cap z)
    (hsplit : err z = slopePart z + remPart z)
    (hrem0 : remPart z0 = 0)
    (hremInc : |remPart z - remPart z0| ≤ Lrem * g z) :
    |err z| ≤ (s * K + Lrem) * g z := by
  have hscaledCap : s * cap z ≤ s * (K * g z) :=
    mul_le_mul_of_nonneg_left hcap hs
  have hslope' : |slopePart z| ≤ s * K * g z := by
    nlinarith
  have hrem : |remPart z| ≤ Lrem * g z := by
    simpa [hrem0] using hremInc
  have htri : |slopePart z + remPart z| ≤ |slopePart z| + |remPart z| :=
    abs_add_le (slopePart z) (remPart z)
  rw [hsplit]
  nlinarith

/-- Diagonal weighted-dual square used by the P5 finite-horizon consumer. -/
def weightedDual (d e : Vec6) : ℝ :=
  ∑ i, e i ^ 2 / d i

/-- Squared-slope coefficient in the affine mixed charge. -/
def slopeDual (d s : Vec6) : ℝ :=
  ∑ i, s i ^ 2 / d i

/-- Squared-offset coefficient in the affine mixed charge. -/
def offsetDual (d b : Vec6) : ℝ :=
  ∑ i, b i ^ 2 / d i

/-- A six-channel affine component box yields a legal mixed weighted-dual
relative-plus-additive charge.  Positive offsets are retained explicitly as
`2*offsetDual`; they are not silently converted into a homogeneous gain. -/
theorem affine_box_to_weighted_dual_mixed
    (d s b e : Vec6) (cap : ℝ)
    (hd : ∀ i, 0 < d i)
    (hs : ∀ i, 0 ≤ s i)
    (hb : ∀ i, 0 ≤ b i)
    (hcap : 0 ≤ cap)
    (he : ∀ i, |e i| ≤ s i * cap + b i) :
    weightedDual d e ≤
      2 * slopeDual d s * cap ^ 2 + 2 * offsetDual d b := by
  unfold weightedDual slopeDual offsetDual
  calc
    (∑ i, e i ^ 2 / d i) ≤
        ∑ i, (2 * (s i ^ 2 / d i) * cap ^ 2 + 2 * (b i ^ 2 / d i)) := by
      apply Finset.sum_le_sum
      intro i hi
      have hbounds :
          -(s i * cap + b i) ≤ e i ∧ e i ≤ s i * cap + b i :=
        (abs_le).mp (he i)
      have hesq : e i ^ 2 ≤ (s i * cap + b i) ^ 2 := by
        nlinarith [sq_nonneg ((s i * cap + b i) - e i),
          sq_nonneg ((s i * cap + b i) + e i)]
      have hyoung :
          (s i * cap + b i) ^ 2 ≤
            2 * (s i * cap) ^ 2 + 2 * b i ^ 2 := by
        nlinarith [sq_nonneg (s i * cap - b i)]
      have hnum : e i ^ 2 ≤ 2 * (s i * cap) ^ 2 + 2 * b i ^ 2 :=
        le_trans hesq hyoung
      have hdiv :
          e i ^ 2 / d i ≤
            (2 * (s i * cap) ^ 2 + 2 * b i ^ 2) / d i :=
        (div_le_div_iff_of_pos_right (hd i)).2 hnum
      calc
        e i ^ 2 / d i ≤
            (2 * (s i * cap) ^ 2 + 2 * b i ^ 2) / d i := hdiv
        _ = 2 * (s i ^ 2 / d i) * cap ^ 2 + 2 * (b i ^ 2 / d i) := by
          field_simp [ne_of_gt (hd i)]
          ring
    _ = 2 * (∑ i, s i ^ 2 / d i) * cap ^ 2 +
        2 * (∑ i, b i ^ 2 / d i) := by
      rw [Finset.sum_add_distrib]
      rw [← Finset.sum_mul]
      rw [← Finset.mul_sum]
      rw [← Finset.mul_sum]

/-- The affine mixed charge composes with a same-domain state bridge
`cap^2 ≤ K^2*A` without introducing any square root. -/
theorem affine_box_to_weighted_dual_state_mixed
    (d s b e : Vec6) (cap K A : ℝ)
    (hd : ∀ i, 0 < d i)
    (hs : ∀ i, 0 ≤ s i)
    (hb : ∀ i, 0 ≤ b i)
    (hcap0 : 0 ≤ cap)
    (he : ∀ i, |e i| ≤ s i * cap + b i)
    (hS : 0 ≤ slopeDual d s)
    (hcapA : cap ^ 2 ≤ K ^ 2 * A) :
    weightedDual d e ≤
      2 * slopeDual d s * K ^ 2 * A + 2 * offsetDual d b := by
  have hmixed := affine_box_to_weighted_dual_mixed d s b e cap hd hs hb hcap0 he
  have hscale :
      2 * slopeDual d s * cap ^ 2 ≤
        2 * slopeDual d s * (K ^ 2 * A) := by
    exact mul_le_mul_of_nonneg_left hcapA (mul_nonneg (by norm_num) hS)
  nlinarith

/-- An explicit error map which vanishes at the equilibrium but retains a
positive jump everywhere else. -/
def anchoredOffset (b x : ℝ) : ℝ :=
  if x = 0 then 0 else b / 2

theorem anchoredOffset_zero (b : ℝ) :
    anchoredOffset b 0 = 0 := by
  simp [anchoredOffset]

/-- The anchored jump map stays under the static positive-offset envelope. -/
theorem anchoredOffset_le_offset
    (b x : ℝ) (hb : 0 ≤ b) :
    |anchoredOffset b x| ≤ b := by
  by_cases hx : x = 0
  · simp [anchoredOffset, hx, hb]
  · rw [anchoredOffset, if_neg hx]
    rw [abs_of_nonneg (by positivity : 0 ≤ b / 2)]
    linarith

/-- Even after exact equilibrium anchoring, a positive static affine offset does
not imply any finite homogeneous relative gain near zero. -/
theorem anchored_offset_not_uniformly_relative
    (b rho : ℝ) (hb : 0 < b) (hrho : 0 ≤ rho) :
    ∃ x : ℝ, x ≠ 0 ∧ rho * |x| < |anchoredOffset b x| := by
  let t : ℝ := 1 / (rho + 1)
  let x : ℝ := t * b / 2
  have hden : 0 < rho + 1 := by linarith
  have ht : 0 < t := by
    dsimp [t]
    positivity
  have hxpos : 0 < x := by
    dsimp [x]
    positivity
  have hfrac : rho / (rho + 1) < 1 :=
    (div_lt_one hden).2 (by linarith)
  have hrt : rho * t < 1 := by
    simpa [t, div_eq_mul_inv] using hfrac
  have hb2 : 0 < b / 2 := by positivity
  have hmain := mul_lt_mul_of_pos_right hrt hb2
  refine ⟨x, ne_of_gt hxpos, ?_⟩
  rw [abs_of_pos hxpos]
  have hx0 : x ≠ 0 := ne_of_gt hxpos
  rw [anchoredOffset, if_neg hx0, abs_of_pos hb2]
  dsimp [x]
  nlinarith

#print axioms affine_envelope_division_free
#print axioms affine_envelope_relative_of_floor
#print axioms centered_increment_relative
#print axioms split_centered_increment_relative
#print axioms affine_box_to_weighted_dual_mixed
#print axioms affine_box_to_weighted_dual_state_mixed
#print axioms anchoredOffset_zero
#print axioms anchoredOffset_le_offset
#print axioms anchored_offset_not_uniformly_relative

end

end RouteBP5AffineFDAdapter

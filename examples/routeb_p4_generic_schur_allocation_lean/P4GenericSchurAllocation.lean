import Mathlib

/-!
Standalone finite-dimensional Euclidean Schur/Young allocation sidecar.
This file is intentionally source-independent: it does not bind `ell` or `r`
to deployed DH expressions, a dense matrix metric, coverage, flowpipe, or registry.
-/
set_option autoImplicit false

namespace RouteBP4GenericSchurAllocation

open scoped BigOperators

noncomputable section

abbrev Vec (n : ℕ) := Fin n → ℝ

def sq {n : ℕ} (x : Vec n) : ℝ := ∑ i, x i ^ 2

def dot {n : ℕ} (x y : Vec n) : ℝ := ∑ i, x i * y i

def schurNumerator (base target lam W : ℝ) {n : ℕ} (ell : Vec n) : ℝ :=
  (lam - 1) * (base - target - lam * W) - lam * sq ell

theorem sq_nonnegative {n : ℕ} (x : Vec n) : 0 ≤ sq x := by
  exact Finset.sum_nonneg (fun i _ => sq_nonneg (x i))

theorem sq_add {n : ℕ} (x y : Vec n) :
    sq (fun i => x i + y i) = sq x + 2 * dot x y + sq y := by
  unfold sq dot
  calc
    (∑ i, (x i + y i) ^ 2) =
        ∑ i, (x i ^ 2 + 2 * (x i * y i) + y i ^ 2) := by
          apply Finset.sum_congr rfl
          intro i _
          ring
    _ = (∑ i, x i ^ 2) + 2 * (∑ i, x i * y i) + (∑ i, y i ^ 2) := by
          rw [Finset.sum_add_distrib, Finset.sum_add_distrib]
          rw [← Finset.mul_sum]

theorem sq_sub_smul {n : ℕ} (x y : Vec n) (a : ℝ) :
    sq (fun i => x i - a * y i) =
      sq x - 2 * a * dot x y + a ^ 2 * sq y := by
  unfold sq dot
  calc
    (∑ i, (x i - a * y i) ^ 2) =
        ∑ i, (x i ^ 2 - 2 * a * (x i * y i) + a ^ 2 * y i ^ 2) := by
          apply Finset.sum_congr rfl
          intro i _
          ring
    _ = (∑ i, x i ^ 2) - 2 * a * (∑ i, x i * y i) +
          a ^ 2 * (∑ i, y i ^ 2) := by
          rw [Finset.sum_sub_distrib, Finset.sum_add_distrib]
          rw [← Finset.mul_sum, ← Finset.mul_sum]

/-- Exact completed-square identity. `W` is only a cap for `sq r`; it is not
substituted for the exact total square of `ell+r`. -/
theorem combined_remainder_identity
    (base target lam W : ℝ) {n : ℕ} (ell r : Vec n) :
    (lam - 1) * (base - target - sq (fun i => ell i + r i)) =
      schurNumerator base target lam W ell +
        sq (fun i => ell i - (lam - 1) * r i) +
        lam * (lam - 1) * (W - sq r) := by
  rw [sq_add, sq_sub_smul]
  unfold schurNumerator
  ring

/-- Generic finite-dimensional consumer of the relaxed Schur allocation. -/
theorem combined_of_port_budget
    (base target lam W : ℝ) {n : ℕ} (ell r : Vec n)
    (hlam : 1 < lam) (hport : sq r ≤ W)
    (halloc : 0 ≤ schurNumerator base target lam W ell) :
    target ≤ base - sq (fun i => ell i + r i) := by
  have hd : 0 < lam - 1 := by linarith
  have hl : 0 ≤ lam := by linarith
  have hs : 0 ≤ (lam - 1) *
      (base - target - sq (fun i => ell i + r i)) := by
    rw [combined_remainder_identity]
    exact add_nonneg (add_nonneg halloc (sq_nonnegative _))
      (mul_nonneg (mul_nonneg hl hd.le) (sub_nonneg.mpr hport))
  have hc := (mul_nonneg_iff_of_pos_left hd).mp hs
  linarith

/-- Exact total residual dominates the single relaxed Schur charge; this is the
no-double-charge comparison. -/
theorem relaxed_target_le_exact_total
    (beta lam W : ℝ) {n : ℕ} (ell r : Vec n)
    (hlam : 1 < lam) (hport : sq r ≤ W) :
    beta - lam * W - lam / (lam - 1) * sq ell ≤
      beta - sq (fun i => ell i + r i) := by
  have hden : lam - 1 ≠ 0 := ne_of_gt (by linarith : 0 < lam - 1)
  have hzero : schurNumerator
      beta (beta - lam * W - lam / (lam - 1) * sq ell) lam W ell = 0 := by
    unfold schurNumerator
    field_simp [hden]
    ring
  have halloc : 0 ≤ schurNumerator
      beta (beta - lam * W - lam / (lam - 1) * sq ell) lam W ell :=
    le_of_eq hzero.symm
  exact combined_of_port_budget beta
    (beta - lam * W - lam / (lam - 1) * sq ell) lam W ell r hlam hport
    halloc

/-- A nonnegative relaxed allocation also supplies the exact total-residual floor. -/
theorem exact_total_floor_of_relaxed_nonnegative
    (beta target lam W : ℝ) {n : ℕ} (ell r : Vec n)
    (hlam : 1 < lam) (hport : sq r ≤ W)
    (hrelaxed : 0 ≤ beta - target - lam * W -
      lam / (lam - 1) * sq ell) :
    target ≤ beta - sq (fun i => ell i + r i) := by
  have h := relaxed_target_le_exact_total beta lam W ell r hlam hport
  linarith

/-- Exact regression showing zero radius does not make a nonzero port finite. -/
theorem zero_radius_boundary_not_finite_witness (lam : ℝ) :
    schurNumerator 1 0 lam 0 (![1, 0] : Vec 2) = -1 := by
  norm_num [schurNumerator, sq]
  ring

#print axioms sq_nonnegative
#print axioms sq_add
#print axioms sq_sub_smul
#print axioms combined_remainder_identity
#print axioms combined_of_port_budget
#print axioms relaxed_target_le_exact_total
#print axioms exact_total_floor_of_relaxed_nonnegative
#print axioms zero_radius_boundary_not_finite_witness

end
end RouteBP4GenericSchurAllocation

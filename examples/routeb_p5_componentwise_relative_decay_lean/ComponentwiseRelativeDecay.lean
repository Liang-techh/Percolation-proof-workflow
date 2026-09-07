import Mathlib.Data.Real.Basic
import Mathlib.Tactic

set_option autoImplicit false

open scoped BigOperators

namespace RouteBP5ComponentwiseRelativeDecay

/-!
Source-independent componentwise residual closure.  The premise is the exact
same-coordinate interface that a true-DH/FD/solve adapter must later provide;
this file does not derive it from numerical data or source code.
-/

theorem componentwise_relative_decay
    {ι : Type*} [Fintype ι]
    (d rho r v : ι → ℝ) (dE : ℝ)
    (hd : ∀ i, 0 < d i)
    (hrho : ∀ i, 0 ≤ rho i)
    (hstrict : ∀ i, rho i < d i)
    (hrel : ∀ i, |r i| ≤ rho i * |v i|)
    (henergy : dE ≤ -(∑ i, d i * v i ^ 2) + ∑ i, r i * v i) :
    dE ≤ -(∑ i, (d i - rho i) * v i ^ 2) := by
  have hpoint : ∀ i, r i * v i ≤ rho i * v i ^ 2 := by
    intro i
    calc
      r i * v i ≤ |r i * v i| := le_abs_self _
      _ = |r i| * |v i| := by simp [abs_mul]
      _ ≤ (rho i * |v i|) * |v i| := by
        exact mul_le_mul_of_nonneg_right (hrel i) (abs_nonneg _)
      _ = rho i * v i ^ 2 := by
        rw [sq_abs]
        ring
  have hsum : (∑ i, r i * v i) ≤ ∑ i, rho i * v i ^ 2 := by
    exact Finset.sum_le_sum (fun i _ => hpoint i)
  calc
    dE ≤ -(∑ i, d i * v i ^ 2) + ∑ i, rho i * v i ^ 2 := by linarith
    _ = -(∑ i, (d i - rho i) * v i ^ 2) := by
      rw [Finset.sum_sub_distrib]
      simp only [sub_mul]
      ring

theorem componentwise_relative_decay_uniform
    {ι : Type*} [Fintype ι]
    (d rho r v : ι → ℝ) (dE lambda : ℝ)
    (hd : ∀ i, 0 < d i)
    (hrho : ∀ i, 0 ≤ rho i)
    (hstrict : ∀ i, rho i < d i)
    (hlambda : ∀ i, lambda ≤ d i - rho i)
    (hrel : ∀ i, |r i| ≤ rho i * |v i|)
    (henergy : dE ≤ -(∑ i, d i * v i ^ 2) + ∑ i, r i * v i) :
    dE ≤ -lambda * (∑ i, v i ^ 2) := by
  have hcomponent := componentwise_relative_decay d rho r v dE
    hd hrho hstrict hrel henergy
  have hweighted : lambda * (∑ i, v i ^ 2) ≤
      ∑ i, (d i - rho i) * v i ^ 2 := by
    apply Finset.sum_le_sum
    intro i _
    have hsq : 0 ≤ v i ^ 2 := sq_nonneg _
    exact mul_le_mul_of_nonneg_right (hlambda i) hsq
  linarith

#print axioms componentwise_relative_decay
#print axioms componentwise_relative_decay_uniform

end RouteBP5ComponentwiseRelativeDecay

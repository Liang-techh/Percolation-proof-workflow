import Mathlib.Data.Real.Basic
import Mathlib.Data.Fin.VecNotation
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# Route-B P5 component-wise relative residual decay sidecar

This file formalizes the source-independent finite-sum algebra requested by
`T-P5-006`, consuming the mathematical derivation in
`review-T-P5-005-kuangmanmozun-20260906T2307.md`.

The main statement keeps the six diagonal damping channels separate: a
component-wise force residual bound `|r i| ≤ rho i * |v i|` retains exactly the
margin `d i - rho i` in that channel.  A second statement packages the physical
admissibility assumptions `0 ≤ rho i` and `rho i < d i` and records that every
retained diagonal margin is strictly positive.

The concrete Route-B damping vector is repeated as exact rationals only to give
an interface corollary matching `RouteBSupplyCore.damping`; this sidecar does
not derive any residual bound from source samples, FD envelopes, controller
code, Float64 execution, or a flowpipe.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP5ComponentRelativeDecay

noncomputable section

/-- Exact diagonal damping vector used by `RouteBSupplyCore`.  Keeping a local
copy makes this sidecar portable in the pinned Mathlib Lake environment. -/
def routeBDamping : Fin 6 → ℝ :=
  ![13 / 10, 11 / 10, 19 / 20, 4 / 5, 13 / 20, 1 / 2]

/-- Each exact Route-B damping coefficient is positive. -/
theorem routeB_damping_pos (i : Fin 6) : 0 < routeBDamping i := by
  fin_cases i <;> norm_num [routeBDamping]

/-- A component-wise absolute residual estimate gives the corresponding
component-wise power estimate.  No sign assumption on `rho` is needed for this
pure implication; source-facing admissibility is imposed separately below. -/
theorem component_power_le
    (rho v r : Fin 6 → ℝ)
    (hrel : ∀ i, |r i| ≤ rho i * |v i|)
    (i : Fin 6) :
    r i * v i ≤ rho i * v i ^ 2 := by
  have hrv : r i * v i ≤ |r i| * |v i| := by
    calc
      r i * v i ≤ |r i * v i| := le_abs_self (r i * v i)
      _ = |r i| * |v i| := abs_mul (r i) (v i)
  have hmul : |r i| * |v i| ≤ (rho i * |v i|) * |v i| :=
    mul_le_mul_of_nonneg_right (hrel i) (abs_nonneg (v i))
  have habs_sq : |v i| * |v i| = v i ^ 2 := by
    calc
      |v i| * |v i| = |v i * v i| := by rw [abs_mul]
      _ = v i * v i := abs_of_nonneg (mul_self_nonneg (v i))
      _ = v i ^ 2 := by ring
  calc
    r i * v i ≤ |r i| * |v i| := hrv
    _ ≤ (rho i * |v i|) * |v i| := hmul
    _ = rho i * (|v i| * |v i|) := by ring
    _ = rho i * v i ^ 2 := by rw [habs_sq]

/-- Source-independent finite-sum closure: the residual power can consume at
most `rho i` of diagonal damping in channel `i`, leaving the exact retained
coefficient `d i - rho i`. -/
theorem component_relative_decay_raw
    (d rho v r : Fin 6 → ℝ)
    (hrel : ∀ i, |r i| ≤ rho i * |v i|) :
    -(∑ i, d i * v i ^ 2) + ∑ i, r i * v i ≤
      -(∑ i, (d i - rho i) * v i ^ 2) := by
  have hsum :
      (∑ i, r i * v i) ≤ ∑ i, rho i * v i ^ 2 := by
    exact Finset.sum_le_sum fun i _ => component_power_le rho v r hrel i
  have hsplit :
      (∑ i, (d i - rho i) * v i ^ 2) =
        (∑ i, d i * v i ^ 2) - ∑ i, rho i * v i ^ 2 := by
    calc
      (∑ i, (d i - rho i) * v i ^ 2) =
          ∑ i, (d i * v i ^ 2 - rho i * v i ^ 2) := by
            apply Finset.sum_congr rfl
            intro i _
            ring
      _ = (∑ i, d i * v i ^ 2) - ∑ i, rho i * v i ^ 2 := by
        simpa using
          (Finset.sum_sub_distrib
            (s := (Finset.univ : Finset (Fin 6)))
            (fun i => d i * v i ^ 2)
            (fun i => rho i * v i ^ 2))
  rw [hsplit]
  linarith

/-- The exact source-facing positivity package.  The hypotheses used in the
mathematical review imply a nonnegative relative gain and a strictly positive
retained damping margin in every channel. -/
theorem admissible_relative_margin
    (d rho : Fin 6 → ℝ)
    (hadm : ∀ i, 0 ≤ rho i ∧ rho i < d i) :
    ∀ i, 0 ≤ rho i ∧ 0 < d i - rho i := by
  intro i
  constructor
  · exact (hadm i).1
  · linarith [(hadm i).2]

/-- Main `T-P5-006` theorem.  It combines the finite-sum decay closure with the
strict positivity of every retained diagonal damping coefficient. -/
theorem component_relative_residual_decay
    (d rho v r : Fin 6 → ℝ)
    (hadm : ∀ i, 0 ≤ rho i ∧ rho i < d i)
    (hrel : ∀ i, |r i| ≤ rho i * |v i|) :
    (-(∑ i, d i * v i ^ 2) + ∑ i, r i * v i ≤
        -(∑ i, (d i - rho i) * v i ^ 2)) ∧
      (∀ i, 0 ≤ rho i ∧ 0 < d i - rho i) := by
  constructor
  · exact component_relative_decay_raw d rho v r hrel
  · exact admissible_relative_margin d rho hadm

/-- Concrete portable corollary for the exact rational damping coefficients in
`RouteBSupplyCore`.  The premise remains abstract: no deployed residual/source
binding is claimed here. -/
theorem routeB_component_relative_residual_decay
    (rho v r : Fin 6 → ℝ)
    (hadm : ∀ i, 0 ≤ rho i ∧ rho i < routeBDamping i)
    (hrel : ∀ i, |r i| ≤ rho i * |v i|) :
    (-(∑ i, routeBDamping i * v i ^ 2) + ∑ i, r i * v i ≤
        -(∑ i, (routeBDamping i - rho i) * v i ^ 2)) ∧
      (∀ i, 0 ≤ rho i ∧ 0 < routeBDamping i - rho i) := by
  exact component_relative_residual_decay routeBDamping rho v r hadm hrel

#print axioms routeB_damping_pos
#print axioms component_power_le
#print axioms component_relative_decay_raw
#print axioms admissible_relative_margin
#print axioms component_relative_residual_decay
#print axioms routeB_component_relative_residual_decay

end

end RouteBP5ComponentRelativeDecay

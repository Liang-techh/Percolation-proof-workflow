import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P4 strict common-lambda boundary

Source-independent Lean decomposition of
`agent_review_inbox/review-T-P4-041-strict-common-lambda-boundary-kuangmanmozun-20260907T1742.md`.

This sidecar kernelizes the square-root-free weak/strict/boundary pair predicates,
the exact weak-but-not-strict boundary classification, the two-row touching
counterexample, and the rational one-parameter perturbation transition.  It is
intentionally an algebraic child only: it does not prove concrete P4 source
coefficients, Float64 realization, P8 coverage, P4/M4 closure, or registry
admission.
-/

set_option autoImplicit false

namespace RouteBP4StrictLambdaBoundary

noncomputable section

/-- Square-root-free weak pair gate from the common-Young-row reduction. -/
def weakPair (C U V : ℝ) : Prop :=
  C ≤ U + V ∨ (C - U - V)^2 ≤ 4 * U * V

/-- Square-root-free strict pair gate.  This is the checker-facing predicate
that distinguishes positive-width overlap from mere touching. -/
def strictPair (C U V : ℝ) : Prop :=
  C < U + V ∨ (C - U - V)^2 < 4 * U * V

/-- Exact touching boundary: the first branch is no longer strict and the
second branch is saturated exactly. -/
def boundaryPair (C U V : ℝ) : Prop :=
  U + V ≤ C ∧ (C - U - V)^2 = 4 * U * V

/-- Strict pair feasibility always implies weak pair feasibility. -/
theorem strictPair_implies_weakPair
    (C U V : ℝ) (h : strictPair C U V) : weakPair C U V := by
  rcases h with hfirst | hsecond
  · exact Or.inl (le_of_lt hfirst)
  · exact Or.inr (le_of_lt hsecond)

/-- Every exact touching boundary passes the weak gate. -/
theorem boundaryPair_implies_weakPair
    (C U V : ℝ) (h : boundaryPair C U V) : weakPair C U V := by
  exact Or.inr (le_of_eq h.2)

/-- Exact touching cannot pass the strict gate. -/
theorem boundaryPair_not_strict
    (C U V : ℝ) (h : boundaryPair C U V) : ¬ strictPair C U V := by
  intro hs
  rcases hs with hfirst | hsecond
  · linarith [h.1]
  · linarith [h.2]

/-- Under the nonnegative `U,V` semantics of squared discriminant terms, a
weak PASS together with strict FAIL is *exactly* the polynomial touching
boundary.  This is the fail-closed seam needed before any positive-reserve or
rounding consumer. -/
theorem weak_not_strict_iff_boundary
    (C U V : ℝ) (hU : 0 ≤ U) (hV : 0 ≤ V) :
    weakPair C U V ∧ ¬ strictPair C U V ↔ boundaryPair C U V := by
  constructor
  · rintro ⟨hw, hns⟩
    have hnotFirst : ¬ C < U + V := by
      intro hfirst
      exact hns (Or.inl hfirst)
    have hge : U + V ≤ C := le_of_not_gt hnotFirst
    have hnotSecond : ¬ (C - U - V)^2 < 4 * U * V := by
      intro hsecond
      exact hns (Or.inr hsecond)
    have hrev : 4 * U * V ≤ (C - U - V)^2 := le_of_not_gt hnotSecond
    refine ⟨hge, ?_⟩
    rcases hw with hfirst | hsecond
    · have hEq : C = U + V := le_antisymm hfirst hge
      have hs0 : (C - U - V)^2 = 0 := by
        rw [hEq]
        ring
      have hprod0 : 0 ≤ 4 * U * V := by
        positivity
      nlinarith
    · exact le_antisymm hsecond hrev
  · intro hb
    exact ⟨boundaryPair_implies_weakPair C U V hb,
      boundaryPair_not_strict C U V hb⟩

/-- The exact pair data of the rational touching example are on the boundary. -/
theorem touching_pair_is_boundary : boundaryPair 4 1 1 := by
  norm_num [boundaryPair]

/-- Therefore the exact pair data pass weak feasibility but fail strict
feasibility. -/
theorem touching_pair_weak_not_strict :
    weakPair 4 1 1 ∧ ¬ strictPair 4 1 1 := by
  norm_num [weakPair, strictPair]

/-- Young-row quadratic in the `theta` coordinate used by T-P4-041. -/
def thetaQuadratic (A G P t : ℝ) : ℝ :=
  A * t^2 - G * t + P

/-- If both touching rows are weakly feasible, their only common witness is
`t = 2`.  The proof uses the exact factorizations rather than numerical root
computation. -/
theorem touching_rows_common_weak_forces_two
    (t : ℝ)
    (h1 : thetaQuadratic 1 3 2 t ≤ 0)
    (h2 : thetaQuadratic 1 5 6 t ≤ 0) :
    t = 2 := by
  have hfact1 : thetaQuadratic 1 3 2 t = (t - 1) * (t - 2) := by
    unfold thetaQuadratic
    ring
  have hfact2 : thetaQuadratic 1 5 6 t = (t - 2) * (t - 3) := by
    unfold thetaQuadratic
    ring
  rw [hfact1] at h1
  rw [hfact2] at h2
  have ht_le : t ≤ 2 := by
    by_contra hnot
    have ht : 2 < t := lt_of_not_ge hnot
    have hp : 0 < (t - 1) * (t - 2) :=
      mul_pos (by linarith) (by linarith)
    linarith
  have ht_ge : 2 ≤ t := by
    by_contra hnot
    have ht : t < 2 := lt_of_not_ge hnot
    have hp : 0 < (t - 2) * (t - 3) :=
      mul_pos_of_neg_of_neg (by linarith) (by linarith)
    linarith
  exact le_antisymm ht_le ht_ge

/-- Both touching rows saturate at their unique common weak witness. -/
theorem touching_rows_at_two :
    thetaQuadratic 1 3 2 2 = 0 ∧ thetaQuadratic 1 5 6 2 = 0 := by
  norm_num [thetaQuadratic]

/-- The touching witness cannot carry any positive common reserve. -/
theorem touching_rows_no_positive_common_reserve
    (m : ℝ) (hm : 0 < m) :
    ¬ (thetaQuadratic 1 3 2 2 ≤ -m ∧ thetaQuadratic 1 5 6 2 ≤ -m) := by
  intro h
  have hfirst := h.1
  norm_num [thetaQuadratic] at hfirst
  linarith

/-- Square-free pair data for the one-parameter perturbation in T-P4-041. -/
def perturbC (e : ℝ) : ℝ := (2 - e)^2
def perturbU : ℝ := 1
def perturbV (e : ℝ) : ℝ := (1 + e)^2

/-- Exact phase-transition identity. -/
theorem perturb_gap_identity (e : ℝ) :
    4 * perturbU * perturbV e -
      (perturbC e - perturbU - perturbV e)^2 =
    32 * e * (1 - e) := by
  unfold perturbC perturbU perturbV
  ring

/-- Positive perturbations strictly inside `(0,1)` pass the strict algebraic
pair gate. -/
theorem positive_perturbation_strict
    (e : ℝ) (he0 : 0 < e) (he1 : e < 1) :
    strictPair (perturbC e) perturbU (perturbV e) := by
  unfold strictPair
  right
  have hgap : 0 < 32 * e * (1 - e) := by
    positivity
  have hid := perturb_gap_identity e
  nlinarith

/-- At `e = 0` the perturbation is exactly the boundary-only pair. -/
theorem zero_perturbation_boundary :
    boundaryPair (perturbC 0) perturbU (perturbV 0) := by
  norm_num [boundaryPair, perturbC, perturbU, perturbV]

/-- Any negative perturbation lies on the disjoint side of the weak gate. -/
theorem negative_perturbation_not_weak
    (e : ℝ) (he : e < 0) :
    ¬ weakPair (perturbC e) perturbU (perturbV e) := by
  intro hw
  have hdiff :
      perturbC e - (perturbU + perturbV e) = 2 - 6 * e := by
    unfold perturbC perturbU perturbV
    ring
  have hsep : perturbU + perturbV e < perturbC e := by
    linarith
  have h1me : 0 < 1 - e := by
    linarith
  have h32e : 32 * e < 0 := by
    nlinarith
  have hgap : 32 * e * (1 - e) < 0 :=
    mul_neg_of_neg_of_pos h32e h1me
  have hid := perturb_gap_identity e
  have hsquare :
      4 * perturbU * perturbV e <
        (perturbC e - perturbU - perturbV e)^2 := by
    nlinarith
  rcases hw with hfirst | hsecond
  · linarith
  · linarith

/-- The perturbed second-row discriminant is exactly `(1+e)^2`. -/
theorem perturbation_discriminant_identity (e : ℝ) :
    (5 - e)^2 - 4 * (6 - 3 * e) = (1 + e)^2 := by
  ring

/-- Rational interior witness from the review: at `e=1/10`, `t=39/20`
leaves common reserve at least `19/400`. -/
theorem positive_tenth_exact_reserve :
    thetaQuadratic 1 3 2 (39 / 20 : ℝ) = -(19 / 400 : ℝ) ∧
    thetaQuadratic 1 (5 - (1 / 10 : ℝ)) (6 - 3 * (1 / 10 : ℝ))
      (39 / 20 : ℝ) = -(21 / 400 : ℝ) := by
  norm_num [thetaQuadratic]

#print axioms strictPair_implies_weakPair
#print axioms boundaryPair_implies_weakPair
#print axioms boundaryPair_not_strict
#print axioms weak_not_strict_iff_boundary
#print axioms touching_pair_is_boundary
#print axioms touching_pair_weak_not_strict
#print axioms touching_rows_common_weak_forces_two
#print axioms touching_rows_at_two
#print axioms touching_rows_no_positive_common_reserve
#print axioms perturb_gap_identity
#print axioms positive_perturbation_strict
#print axioms zero_perturbation_boundary
#print axioms negative_perturbation_not_weak
#print axioms perturbation_discriminant_identity
#print axioms positive_tenth_exact_reserve

end

end RouteBP4StrictLambdaBoundary

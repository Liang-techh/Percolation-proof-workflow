import NEW_P4_032_SplitAllocationObstruction

/-!
OPEN_UNCOMPILED. Exact feasibility for the chosen split budget records.
Canonical target is their maximal allocated scalar, not an optimized
physical margin or a guarantee for an independently prescribed target.
No Lean/Lake run, registry mutation, source/coverage or PSD claim.
-/

set_option autoImplicit false

namespace RouteBP4032PositiveTargetFeasibility

open RouteBP4032UniformParameterBridge
open RouteBP4032ResidualMarginConsumer
open RouteBP4032Body6SchurScalarAdapter
open RouteBP4032DualScaleComposition
open RouteBP4032SplitAllocationObstruction

noncomputable section

variable {X : Type*} {f : ParameterField X} {d : RemainderField X}
  {m : MarginField X} {s : ScaleFields X}

def frontCredit (front : FrontFloors f d s) : ℝ :=
  front.offsetFloor + front.alphaFloor * front.frontFloor

def residualLoss (caps : ResidualCaps f m s) : ℝ :=
  caps.gainCap * (caps.betaCap * caps.qCap)

theorem residualLoss_nonnegative (caps : ResidualCaps f m s) : 0 ≤ residualLoss caps :=
  mul_nonneg caps.gain_nonnegative (mul_nonneg caps.beta_nonnegative caps.cap_nonnegative)

/-- Exact condition for EVERY prescribed target, regardless of its sign. -/
theorem target_budget_iff (front : FrontFloors f d s) (caps : ResidualCaps f m s)
    (target : ℝ) : TargetBudget front caps target ↔ target ≤ canonicalTarget front caps := by
  constructor
  · intro h
    have ha := h.allocation
    unfold canonicalTarget
    linarith
  · intro h
    refine ⟨?_⟩
    unfold canonicalTarget at h
    linarith

structure PositiveTargetBudget (front : FrontFloors f d s)
    (caps : ResidualCaps f m s) (target : ℝ) : Prop where
  positive : 0 < target
  budget : TargetBudget front caps target

theorem positive_target_iff (front : FrontFloors f d s) (caps : ResidualCaps f m s)
    (target : ℝ) : PositiveTargetBudget front caps target ↔
      0 < target ∧ target ≤ canonicalTarget front caps := by
  constructor
  · intro h
    exact ⟨h.positive, (target_budget_iff front caps target).mp h.budget⟩
  · rintro ⟨hpos, hle⟩
    exact ⟨hpos, (target_budget_iff front caps target).mpr hle⟩

/-- Existence of SOME positive target, not feasibility of an arbitrary one. -/
theorem positive_target_exists_iff (front : FrontFloors f d s) (caps : ResidualCaps f m s) :
    (∃ target : ℝ, PositiveTargetBudget front caps target) ↔
      residualLoss caps < frontCredit front := by
  constructor
  · rintro ⟨target, h⟩
    have ha := h.budget.allocation
    have ht := h.positive
    unfold residualLoss frontCredit
    linarith
  · intro h
    refine ⟨canonicalTarget front caps, ?_, canonicalTargetBudget front caps⟩
    unfold canonicalTarget
    unfold residualLoss frontCredit at h
    linarith

theorem zero_target_iff (front : FrontFloors f d s) (caps : ResidualCaps f m s) :
    TargetBudget front caps 0 ↔ residualLoss caps ≤ frontCredit front := by
  constructor
  · intro h
    simpa only [zero_add, residualLoss, frontCredit] using h.allocation
  · intro h
    exact ⟨by simpa only [zero_add, residualLoss, frontCredit] using h⟩

/-- A prescribed negative target still has to satisfy the same inequality. -/
theorem negative_target_iff (front : FrontFloors f d s) (caps : ResidualCaps f m s)
    (target : ℝ) :
    (target < 0 ∧ TargetBudget front caps target) ↔
      target < 0 ∧ target ≤ canonicalTarget front caps := by
  rw [target_budget_iff]

/-- Some negative target always exists for finite real records. This does
not say every negative target works, or that the resulting margin is positive. -/
theorem negative_target_exists (front : FrontFloors f d s) (caps : ResidualCaps f m s) :
    ∃ target : ℝ, target < 0 ∧ TargetBudget front caps target := by
  let target := min (canonicalTarget front caps) 0 - 1
  have h0 := min_le_right (canonicalTarget front caps) (0 : ℝ)
  have hc := min_le_left (canonicalTarget front caps) (0 : ℝ)
  refine ⟨target, ?_, (target_budget_iff front caps target).mpr ?_⟩
  · dsimp [target]
    linarith
  · dsimp [target]
    linarith

/-- Budget feasibility reaches a positive scalar margin only after the
independent same-domain composition/normalization and nominal lower proofs. -/
theorem positive_margin_of_budget (front : FrontFloors f d s) (caps : ResidualCaps f m s)
    (b : CompositionContract f d m s) (nominal : NominalRealization f d m s)
    (target : ℝ) (h : PositiveTargetBudget front caps target) :
    ∀ x, f.domain x → 0 < m.margin x := by
  intro x hx
  exact h.positive.trans_le
    (split_conditional_margin f d m s b front caps nominal target h.budget x hx)

theorem nonnegative_margin_of_zero_budget (front : FrontFloors f d s)
    (caps : ResidualCaps f m s) (b : CompositionContract f d m s)
    (nominal : NominalRealization f d m s) (h : TargetBudget front caps 0) :
    ∀ x, f.domain x → 0 ≤ m.margin x :=
  split_conditional_margin f d m s b front caps nominal 0 h

/-- Credit=1, gain=beta=1, qCap=2: the canonical target -1 is allocated,
yet the independently prescribed positive target 1 is not. -/
theorem canonical_existence_not_positive :
    ((-1 : ℝ) + 1 * (1 * 2) ≤ 1) ∧ ¬ ((1 : ℝ) + 1 * (1 * 2) ≤ 1) := by
  norm_num

/-- Even a positive canonical target 1 does not allocate prescribed target 2. -/
theorem positive_canonical_not_arbitrary_target :
    (0 : ℝ) < 2 - 1 * (1 * 1) ∧ ¬ ((2 : ℝ) + 1 * (1 * 1) ≤ 2) := by
  norm_num

/-- Canonical target -2: target -1 is negative but still infeasible. -/
theorem negative_target_not_automatic :
    (-1 : ℝ) < 0 ∧ ¬ ((-1 : ℝ) + 1 * (1 * 2) ≤ 0) := by
  norm_num

/-- A seemingly positive allocation does not replace q<=qCap. With correct
nominal=credit=2 but q=3>qCap=1, the actual margin is -1, below target 1. -/
theorem missing_qCap_positive_counterexample :
    ∃ credit gain beta q qCap target margin : ℝ,
      0 ≤ credit ∧ 0 ≤ gain ∧ 0 ≤ beta ∧ 0 ≤ q ∧ 0 ≤ qCap ∧ 0 < target ∧
      target + gain * (beta * qCap) ≤ credit ∧ credit - gain * (beta * q) ≤ margin ∧
      qCap < q ∧ margin < target := by
  refine ⟨2, 1, 1, 3, 1, 1, -1, ?_⟩
  norm_num

end

-- Future audit commands only; NOT executed in this round.
#print axioms target_budget_iff
#print axioms positive_target_iff
#print axioms positive_target_exists_iff
#print axioms zero_target_iff
#print axioms negative_target_iff
#print axioms negative_target_exists
#print axioms positive_margin_of_budget
#print axioms nonnegative_margin_of_zero_budget
#print axioms canonical_existence_not_positive
#print axioms positive_canonical_not_arbitrary_target
#print axioms negative_target_not_automatic
#print axioms missing_qCap_positive_counterexample

end RouteBP4032PositiveTargetFeasibility

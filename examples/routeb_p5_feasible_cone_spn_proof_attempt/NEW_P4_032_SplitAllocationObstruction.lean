import NEW_P4_032_NominalDirectionAudit

/-!
OPEN_UNCOMPILED. Independent uniform evidence records and allocation
obstructions. Reuses existing composition and finite/dyadic lemmas.
No Lean/Lake run, registry mutation, source/coverage or PSD claim.
-/

set_option autoImplicit false

namespace RouteBP4032SplitAllocationObstruction

open RouteBP4032UniformParameterBridge
open RouteBP4032ResidualMarginConsumer
open RouteBP4032Body6SchurScalarAdapter
open RouteBP4032DualScaleComposition
open RouteBP4032DualScaleUniformization
open RouteBP4032NominalDirectionAudit
open RouteBP4032DomainUniformContraction
open scoped BigOperators

noncomputable section

structure FrontFloors {X : Type*} (f : ParameterField X)
    (d : RemainderField X) (s : ScaleFields X) where
  alphaFloor : ℝ
  frontFloor : ℝ
  offsetFloor : ℝ
  alpha_nonnegative : 0 ≤ alphaFloor
  front_nonnegative : 0 ≤ frontFloor
  alpha_bound : ∀ x, f.domain x → alphaFloor ≤ (s.front x).value
  front_bound : ∀ x, f.domain x → frontFloor ≤ d.mu x * frontEnergy (d.front x)
  offset_bound : ∀ x, f.domain x → offsetFloor ≤ d.offset x

structure ResidualCaps {X : Type*} (f : ParameterField X)
    (m : MarginField X) (s : ScaleFields X) where
  betaCap : ℝ
  gainCap : ℝ
  qCap : ℝ
  beta_nonnegative : 0 ≤ betaCap
  gain_nonnegative : 0 ≤ gainCap
  cap_nonnegative : 0 ≤ qCap
  beta_bound : ∀ x, f.domain x → (s.residual x).value ≤ betaCap
  gain_bound : ∀ x, f.domain x → m.gain x ≤ gainCap
  q_nonnegative : ∀ x, f.domain x → 0 ≤ f.residual x
  q_bound : ∀ x, f.domain x → f.residual x ≤ qCap

/-- Direction is encoded by the previously distinct NominalLower type. -/
structure NominalRealization {X : Type*} (f : ParameterField X)
    (d : RemainderField X) (m : MarginField X) (s : ScaleFields X) : Prop where
  lower : NominalLower f m (bodyExpression d s)

/-- Independent allocation proposition; finite bounds do not fill it. -/
structure TargetBudget {X : Type*} {f : ParameterField X} {d : RemainderField X}
    {m : MarginField X} {s : ScaleFields X}
    (front : FrontFloors f d s) (caps : ResidualCaps f m s) (target : ℝ) : Prop where
  allocation : target + caps.gainCap * (caps.betaCap * caps.qCap) ≤
    front.offsetFloor + front.alphaFloor * front.frontFloor

def assembleUniform {X : Type*} (f : ParameterField X)
    (d : RemainderField X) (m : MarginField X) (s : ScaleFields X)
    (front : FrontFloors f d s) (caps : ResidualCaps f m s)
    (nominal : NominalRealization f d m s) : UniformData f d m s where
  alphaFloor := front.alphaFloor
  frontFloor := front.frontFloor
  offsetFloor := front.offsetFloor
  betaCap := caps.betaCap
  gainCap := caps.gainCap
  qCap := caps.qCap
  alphaFloor_nonnegative := front.alpha_nonnegative
  frontFloor_nonnegative := front.front_nonnegative
  betaCap_nonnegative := caps.beta_nonnegative
  gainCap_nonnegative := caps.gain_nonnegative
  qCap_nonnegative := caps.cap_nonnegative
  alpha_bound := front.alpha_bound
  front_bound := front.front_bound
  offset_bound := front.offset_bound
  beta_bound := caps.beta_bound
  gain_bound := caps.gain_bound
  q_nonnegative := caps.q_nonnegative
  q_bound := caps.q_bound
  nominal_realization := nominal.lower.bound

theorem split_conditional_margin {X : Type*} (f : ParameterField X)
    (d : RemainderField X) (m : MarginField X) (s : ScaleFields X)
    (b : CompositionContract f d m s)
    (front : FrontFloors f d s) (caps : ResidualCaps f m s)
    (nominal : NominalRealization f d m s) (target : ℝ)
    (allocation : TargetBudget front caps target) :
    ∀ x, f.domain x → target ≤ m.margin x :=
  uniformized_scalar_margin f d m s b (assembleUniform f d m s front caps nominal)
    target allocation.allocation

/-- A finite covering set supplies residual caps, provided the residual
is nonnegative on the actual domain. Uses old finite_upper three times. -/
theorem finite_residual_caps {X : Type*} (f : ParameterField X)
    (m : MarginField X) (s : ScaleFields X) (cells : Finset X)
    (cover : ∀ x, f.domain x → x ∈ cells)
    (hq0 : ∀ x, f.domain x → 0 ≤ f.residual x) : Nonempty (ResidualCaps f m s) := by
  obtain ⟨bc, hb0, hb⟩ := finite_upper cells (fun x => (s.residual x).value)
  obtain ⟨gc, hg0, hg⟩ := finite_upper cells m.gain
  obtain ⟨qc, hqcap0, hq⟩ := finite_upper cells f.residual
  exact ⟨⟨bc, gc, qc, hb0, hg0, hqcap0,
    fun x hx => hb x (cover x hx), fun x hx => hg x (cover x hx),
    hq0, fun x hx => hq x (cover x hx)⟩⟩

/-- A conservative finite front record: alphaFloor=frontFloor=0. Positive
floors need extra evidence; this existence lemma promises no positive target. -/
theorem finite_front_floors {X : Type*} (f : ParameterField X)
    (d : RemainderField X) (m : MarginField X) (s : ScaleFields X)
    (b : CompositionContract f d m s) (cells : Finset X)
    (cover : ∀ x, f.domain x → x ∈ cells) : Nonempty (FrontFloors f d s) := by
  obtain ⟨lo, hi, hb⟩ := finite_lower_upper cells d.offset
  refine ⟨⟨0, 0, lo, le_rfl, le_rfl, b.front_nonnegative, ?_, ?_⟩⟩
  · intro x hx
    have henergy : 0 ≤ frontEnergy (d.front x) := by
      unfold frontEnergy
      exact Finset.sum_nonneg (fun i _ => sq_nonneg _)
    exact mul_nonneg (b.remainder_margin x hx).2.1 henergy
  · intro x hx
    exact (hb x (cover x hx)).1

/-- Every selected pair of finite real records has an exact allocated
floor, possibly NEGATIVE. This does not allocate a prescribed target. -/
def canonicalTarget {X : Type*} {f : ParameterField X} {d : RemainderField X}
    {m : MarginField X} {s : ScaleFields X}
    (front : FrontFloors f d s) (caps : ResidualCaps f m s) : ℝ :=
  front.offsetFloor + front.alphaFloor * front.frontFloor -
    caps.gainCap * (caps.betaCap * caps.qCap)

def canonicalTargetBudget {X : Type*} {f : ParameterField X} {d : RemainderField X}
    {m : MarginField X} {s : ScaleFields X}
    (front : FrontFloors f d s) (caps : ResidualCaps f m s) :
    TargetBudget front caps (canonicalTarget front caps) where
  allocation := by unfold canonicalTarget; linarith

/-- Finite-domain sufficient conclusion, still explicitly conditional on
normalization and the correct nominal direction. The target may be negative. -/
theorem finite_conditional_floor {X : Type*} (f : ParameterField X)
    (d : RemainderField X) (m : MarginField X) (s : ScaleFields X)
    (b : CompositionContract f d m s) (nominal : NominalRealization f d m s)
    (cells : Finset X) (cover : ∀ x, f.domain x → x ∈ cells)
    (hq0 : ∀ x, f.domain x → 0 ≤ f.residual x) :
    ∃ target : ℝ, ∀ x, f.domain x → target ≤ m.margin x := by
  obtain ⟨front⟩ := finite_front_floors f d m s b cells cover
  obtain ⟨caps⟩ := finite_residual_caps f m s cells cover hq0
  exact ⟨canonicalTarget front caps,
    split_conditional_margin f d m s b front caps nominal _ (canonicalTargetBudget front caps)⟩

/-- beta_n=2^n, gain=q=qCap=1, nominal=expression=1. Exact normalized
margin 1-beta_n defeats every common target: nominal direction is correct. -/
theorem infinite_loss_allocation_obstruction (target : ℝ) :
    ∃ n : ℕ, 0 ≤ dyadicEnergy n ∧
      ¬ (target + dyadicEnergy n ≤ 1) ∧ 1 - dyadicEnergy n < target := by
  obtain ⟨n, hn⟩ := dyadic_exceeds (1 - target)
  refine ⟨n, (dyadic_point n).1, ?_, ?_⟩
  · intro h
    linarith
  · linarith

/-- Wrong nominal direction blocks the NOMINAL allocation even with zero
loss and bounded residual. expression=0, nominal_n=-2^n. Normalized BODY6
margin=0 is still compatible: this is not an impossibility of all margin proofs. -/
theorem infinite_nominal_direction_obstruction (target : ℝ) (ht : target ≤ 0) :
    ∃ n : ℕ, -dyadicEnergy n ≤ 0 ∧ target + 0 ≤ 0 ∧
      ¬ (target + 0 ≤ -dyadicEnergy n) ∧ (0 : ℝ) - 0 ≤ 0 := by
  obtain ⟨n, hn⟩ := dyadic_exceeds (-target)
  have hE := (dyadic_point n).1
  refine ⟨n, ?_, ?_, ?_, by norm_num⟩
  · linarith
  · linarith
  · intro h
    linarith

end

-- Future audit commands only; NOT executed in this round.
#print axioms assembleUniform
#print axioms split_conditional_margin
#print axioms finite_residual_caps
#print axioms finite_front_floors
#print axioms finite_conditional_floor
#print axioms infinite_loss_allocation_obstruction
#print axioms infinite_nominal_direction_obstruction

end RouteBP4032SplitAllocationObstruction

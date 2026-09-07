import NEW_P4_032_PositiveTargetFeasibility

/-!
OPEN_UNCOMPILED. Same-domain source-view binding for a prescribed positive
target. An abstract SourceView is NOT itself a verified true-DH model.
No Lean/Lake run, concrete source parameters, coverage or registry upgrade.
-/

set_option autoImplicit false

namespace RouteBP4032SourcePositiveTargetBinding

open RouteBP4032BlockDefects
open RouteBP4032DefectNormBudget
open NEW_BODY6_SLICE_SCHURMARGIN20260907
open RouteBP4032UniformParameterBridge
open RouteBP4032ResidualMarginConsumer
open RouteBP4032Body6SchurScalarAdapter
open RouteBP4032DualScaleComposition
open RouteBP4032SplitAllocationObstruction
open RouteBP4032PositiveTargetFeasibility

noncomputable section

/-- Explicit modeled source functions. A caller must identify these with
the intended true-DH equations/provenance; names do not certify that step. -/
structure SourceView (Y : Type*) where
  domain : Y → Prop
  energy : Y → ℝ
  forceResidual : Y → PortGeneralizedForce
  remainder : Y → FrontBlock
  front : Y → Front
  mu : Y → ℝ
  alpha : Y → ℝ
  beta : Y → ℝ
  gain : Y → ℝ
  offset : Y → ℝ
  nominal : Y → ℝ
  scalarMargin : Y → ℝ

/-- A single mapping binds all fields at the same source state. residual
is EXACTLY the squared generalized-force norm here; no acceleration or
unproved inertia conversion is silently permitted. -/
structure SameDomainBinding {X Y : Type*} (src : SourceView Y)
    (f : ParameterField X) (d : RemainderField X) (m : MarginField X)
    (s : ScaleFields X) (embed : Y → X) : Prop where
  covered : ∀ y, src.domain y → f.domain (embed y)
  energy_eq : ∀ y, src.domain y → f.energy (embed y) = src.energy y
  residual_eq : ∀ y, src.domain y →
    f.residual (embed y) = (norm2 (src.forceResidual y).value)^2
  remainder_eq : ∀ y, src.domain y → d.remainder (embed y) = src.remainder y
  front_eq : ∀ y, src.domain y → d.front (embed y) = src.front y
  mu_eq : ∀ y, src.domain y → d.mu (embed y) = src.mu y
  alpha_eq : ∀ y, src.domain y → (s.front (embed y)).value = src.alpha y
  beta_eq : ∀ y, src.domain y → (s.residual (embed y)).value = src.beta y
  gain_eq : ∀ y, src.domain y → m.gain (embed y) = src.gain y
  offset_eq : ∀ y, src.domain y → d.offset (embed y) = src.offset y
  nominal_eq : ∀ y, src.domain y → m.nominal (embed y) = src.nominal y
  margin_eq : ∀ y, src.domain y → m.margin (embed y) = src.scalarMargin y

/-- Retains the actual residual cap obligation after source binding. -/
theorem source_residual_cap {X Y : Type*} (src : SourceView Y)
    (f : ParameterField X) (d : RemainderField X) (m : MarginField X)
    (s : ScaleFields X) (embed : Y → X)
    (binding : SameDomainBinding src f d m s embed) (caps : ResidualCaps f m s) :
    ∀ y, src.domain y → (norm2 (src.forceResidual y).value)^2 ≤ caps.qCap := by
  intro y hy
  rw [← binding.residual_eq y hy]
  exact caps.q_bound (embed y) (binding.covered y hy)

/-- The exact positive budget is a separate input. The scalar source-view
conclusion is conditional on ALL same-domain/normalization evidence. -/
theorem source_prescribed_positive_margin {X Y : Type*} (src : SourceView Y)
    (f : ParameterField X) (d : RemainderField X) (m : MarginField X)
    (s : ScaleFields X) (embed : Y → X)
    (binding : SameDomainBinding src f d m s embed)
    (front : FrontFloors f d s) (caps : ResidualCaps f m s)
    (composition : CompositionContract f d m s) (nominal : NominalRealization f d m s)
    (target : ℝ) (budget : PositiveTargetBudget front caps target) :
    ∀ y, src.domain y → 0 < target ∧ target ≤ src.scalarMargin y := by
  intro y hy
  refine ⟨budget.positive, ?_⟩
  calc
    target ≤ m.margin (embed y) :=
      split_conditional_margin f d m s composition front caps nominal target budget.budget
        (embed y) (binding.covered y hy)
    _ = src.scalarMargin y := binding.margin_eq y hy

/-- Exact arithmetic obstruction for these fixed records only. -/
theorem credit_not_exceeding_loss_blocks_positive {X : Type*} {f : ParameterField X}
    {d : RemainderField X} {m : MarginField X} {s : ScaleFields X}
    (front : FrontFloors f d s) (caps : ResidualCaps f m s)
    (h : frontCredit front ≤ residualLoss caps) :
    ¬ ∃ target : ℝ, PositiveTargetBudget front caps target := by
  intro hp
  exact (not_lt_of_ge h) ((positive_target_exists_iff front caps).mp hp)

/-- Nonnegative/zero floors alone do not supply a strictly positive credit. -/
theorem zero_floor_blocks_positive {X : Type*} {f : ParameterField X}
    {d : RemainderField X} {m : MarginField X} {s : ScaleFields X}
    (front : FrontFloors f d s) (caps : ResidualCaps f m s)
    (hzero : front.alphaFloor = 0 ∨ front.frontFloor = 0)
    (hoffset : front.offsetFloor ≤ 0) :
    ¬ ∃ target : ℝ, PositiveTargetBudget front caps target := by
  have hcredit : frontCredit front ≤ 0 := by
    rcases hzero with ha | hf
    · simpa [frontCredit, ha] using hoffset
    · simpa [frontCredit, hf] using hoffset
  exact credit_not_exceeding_loss_blocks_positive front caps
    (hcredit.trans (residualLoss_nonnegative caps))

/-- If the domain includes a zero front test vector, its homogeneous front
energy prevents any positive uniform frontFloor, even with positive mu. -/
theorem zero_front_test_forces_zero_floor {X : Type*} {f : ParameterField X}
    {d : RemainderField X} {s : ScaleFields X} (front : FrontFloors f d s)
    (x : X) (hx : f.domain x) (hv : d.front x = fun _ => 0) : front.frontFloor = 0 := by
  have hb := front.front_bound x hx
  have hle : front.frontFloor ≤ 0 := by simpa [hv, frontEnergy] using hb
  exact le_antisymm hle front.front_nonnegative

/-- All scalar cap/gain/front numbers can be positive and STILL exhaust
the credit exactly: F=L=1, so no positive target is allocated. -/
theorem positive_signs_not_positive_budget :
    (0 : ℝ) < 1 ∧ (∀ target : ℝ, 0 < target → ¬ (target + 1 * (1 * 1) ≤ 1)) := by
  refine ⟨by norm_num, ?_⟩
  intro target ht halloc
  linarith

end

-- Future audit commands only; NOT executed in this round.
#print axioms source_residual_cap
#print axioms source_prescribed_positive_margin
#print axioms credit_not_exceeding_loss_blocks_positive
#print axioms zero_floor_blocks_positive
#print axioms zero_front_test_forces_zero_floor
#print axioms positive_signs_not_positive_budget

end RouteBP4032SourcePositiveTargetBinding

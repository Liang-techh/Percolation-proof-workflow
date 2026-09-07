import NEW_P4_032_SourcePositiveTargetBinding

/-!
OPEN_UNCOMPILED. Same-row exact budget gate; no concrete packet is admitted.
Metadata equality is not source authentication or unit/normalization proof.
No Lean/Lake execution, numerical rerun, source mutation or registry change.
-/
set_option autoImplicit false

namespace RouteBP4032SameRowBudgetAudit

open RouteBP4032UniformParameterBridge RouteBP4032ResidualMarginConsumer
open RouteBP4032Body6SchurScalarAdapter RouteBP4032DualScaleComposition
open RouteBP4032SplitAllocationObstruction RouteBP4032PositiveTargetFeasibility
open RouteBP4032SourcePositiveTargetBinding

noncomputable section

inductive Slot where
  | frontFloor | offsetFloor | alphaFloor | gainCap | betaCap | qCap | target
  deriving DecidableEq

/-- One instance key. Strings are declarations, not verified identities.
unitContract identifies a conversion contract, not a claim that all slots
have the same dimension. eta/sf require exact reification before this layer. -/
structure Context where
  manifestDigest : String
  artifactDigest : String
  rowId : String
  stage : String
  domainId : String
  objectContract : String
  unitContract : String
  eta : ℚ
  sf : ℚ
  deriving DecidableEq

structure ObservedRow where
  context : Context
  value : Slot → Option ℚ
  origin : Slot → Option Context

/-- Must be supplied by an external, audited extraction/reification step. -/
structure CompleteRow (r : ObservedRow) where
  exactValue : Slot → ℚ
  present : ∀ k, r.value k = some (exactValue k)
  same_origin : ∀ k, r.origin k = some r.context

theorem missing_slot_blocks_completion (r : ObservedRow) (k : Slot)
    (h : r.value k = none) : ¬ Nonempty (CompleteRow r) := by
  rintro ⟨c⟩
  have hc := c.present k
  rw [h] at hc
  cases hc

theorem mixed_origin_blocks_completion (r : ObservedRow) (k : Slot)
    (other : Context) (h : r.origin k = some other) (hne : other ≠ r.context) :
    ¬ Nonempty (CompleteRow r) := by
  rintro ⟨c⟩
  have hc := c.same_origin k
  rw [h] at hc
  exact hne (Option.some.inj hc)

def credit (v : Slot → ℚ) : ℚ :=
  v .offsetFloor + v .alphaFloor * v .frontFloor

def loss (v : Slot → ℚ) : ℚ :=
  v .gainCap * (v .betaCap * v .qCap)

def PositiveAllocation (v : Slot → ℚ) : Prop :=
  0 < v .target ∧ v .target + loss v ≤ credit v

theorem prescribed_target_iff (v : Slot → ℚ) :
    PositiveAllocation v ↔ 0 < v .target ∧ v .target ≤ credit v - loss v := by
  unfold PositiveAllocation
  constructor <;> rintro ⟨hp, hb⟩ <;> exact ⟨hp, by linarith⟩

theorem credit_le_loss_blocks_positive (v : Slot → ℚ) (h : credit v ≤ loss v) :
    ¬ PositiveAllocation v := by
  rintro ⟨hp, hb⟩
  linarith

/-- F>L supplies SOME positive target; a prescribed target still needs t≤F-L. -/
theorem positive_target_exists_iff_exact (v : Slot → ℚ) :
    (∃ t : ℚ, 0 < t ∧ t + loss v ≤ credit v) ↔ loss v < credit v := by
  constructor
  · rintro ⟨t, hp, hb⟩
    linarith
  · intro h
    exact ⟨credit v - loss v, by linarith, by linarith⟩

/-- Same-domain semantic bounds are separate from the metadata gate. -/
structure BoundRow {X : Type*} (r : ObservedRow) (f : ParameterField X)
    (d : RemainderField X) (m : MarginField X) (s : ScaleFields X) where
  complete : CompleteRow r
  front : FrontFloors f d s
  caps : ResidualCaps f m s
  front_eq : front.frontFloor = (complete.exactValue .frontFloor : ℝ)
  offset_eq : front.offsetFloor = (complete.exactValue .offsetFloor : ℝ)
  alpha_eq : front.alphaFloor = (complete.exactValue .alphaFloor : ℝ)
  gain_eq : caps.gainCap = (complete.exactValue .gainCap : ℝ)
  beta_eq : caps.betaCap = (complete.exactValue .betaCap : ℝ)
  q_eq : caps.qCap = (complete.exactValue .qCap : ℝ)

theorem bound_row_allocation {X : Type*} {r : ObservedRow}
    {f : ParameterField X} {d : RemainderField X} {m : MarginField X} {s : ScaleFields X}
    (b : BoundRow r f d m s) (h : PositiveAllocation b.complete.exactValue) :
    PositiveTargetBudget b.front b.caps (b.complete.exactValue .target : ℝ) := by
  rcases h with ⟨hp, hb⟩
  refine ⟨by exact_mod_cast hp, ⟨?_⟩⟩
  rw [b.gain_eq, b.beta_eq, b.q_eq, b.offset_eq, b.alpha_eq, b.front_eq]
  dsimp [loss, credit] at hb
  exact_mod_cast hb

/-- All nine object groups, both scales, mu and coverage use one embed.
Even this conclusion is about the modeled SourceView, not authenticated DH. -/
theorem same_row_source_margin {X Y : Type*} {r : ObservedRow}
    (src : SourceView Y) (f : ParameterField X) (d : RemainderField X)
    (m : MarginField X) (s : ScaleFields X) (embed : Y → X)
    (binding : SameDomainBinding src f d m s embed) (b : BoundRow r f d m s)
    (composition : CompositionContract f d m s) (nominal : NominalRealization f d m s)
    (h : PositiveAllocation b.complete.exactValue) :
    ∀ y, src.domain y → 0 < (b.complete.exactValue .target : ℝ) ∧
      (b.complete.exactValue .target : ℝ) ≤ src.scalarMargin y :=
  source_prescribed_positive_margin src f d m s embed binding b.front b.caps
    composition nominal _ (bound_row_allocation b h)

/-- Exact synthetic rows: A has F=4,L=5; B has F=1,L=2. -/
def rowA : Slot → ℚ
  | .frontFloor => 4
  | .qCap => 5
  | .offsetFloor => 0
  | _ => 1

def rowB : Slot → ℚ
  | .qCap => 2
  | .offsetFloor => 0
  | _ => 1

/-- Illegally borrowing only A's frontFloor makes B appear feasible. -/
def mixedRow : Slot → ℚ
  | .frontFloor => rowA .frontFloor
  | k => rowB k

theorem mixed_row_false_positive :
    ¬ PositiveAllocation rowA ∧ ¬ PositiveAllocation rowB ∧ PositiveAllocation mixedRow := by
  norm_num [PositiveAllocation, credit, loss, rowA, rowB, mixedRow]

/-- A SINGLE unrecorded qCap suffices to leave both outcomes possible. -/
def missingCapCompletion (q : ℚ) : Slot → ℚ
  | .frontFloor => 2
  | .offsetFloor => 0
  | .qCap => q
  | _ => 1

theorem same_other_six (q₁ q₂ : ℚ) (k : Slot) (hk : k ≠ .qCap) :
    missingCapCompletion q₁ k = missingCapCompletion q₂ k := by
  cases k <;> simp_all [missingCapCompletion]

theorem missing_cap_underdetermines_sign :
    PositiveAllocation (missingCapCompletion 1) ∧
    credit (missingCapCompletion 3) < loss (missingCapCompletion 3) := by
  norm_num [PositiveAllocation, credit, loss, missingCapCompletion]

end
end RouteBP4032SameRowBudgetAudit

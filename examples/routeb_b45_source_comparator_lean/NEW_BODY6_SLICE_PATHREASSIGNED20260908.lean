import NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_PATHREASSIGNED20260908
noncomputable section
open NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907

/- OPEN_UNCOMPILED. Explicit packaging of the unchanged repaired contract.
   D is the caller's fixed full-state domain, not a domain chosen by this record. -/
structure TransferInputs {X C : Type*} (project : X → C)
    (D : ℝ → Set X) (Q : Set C) (path : ℝ → X)
    (F G : ℝ → X → ℝ) (B cap bar : ℝ) : Prop where
  projection : DomainProjection project D Q
  wholePath : WholePathMembership D path
  value : ShiftIdentityOnQ project Q F G B
  sourceCap : ∀ t ∈ Set.Icc (0 : ℝ) 1, F t (path t) ≤ cap
  budget : cap + B ≤ bar

theorem repaired_contract_adapter_attempt {X C : Type*} (project : X → C)
    (D : ℝ → Set X) (Q : Set C) (path : ℝ → X)
    (F G : ℝ → X → ℝ) (B cap bar : ℝ)
    (h : TransferInputs project D Q path F G B cap bar) :
    ∀ t ∈ Set.Icc (0 : ℝ) 1, G t (path t) ≤ bar :=
  projected_shift_cap_transfer_attempt project D Q path F G B cap bar
    h.projection h.wholePath h.value h.sourceCap h.budget

/- A canonical pullback expresses only projected membership. It need not
   equal the physical domain, which may constrain velocities and other state. -/
def pullbackDomain {X C : Type*} (project : X → C) (Q : Set C) : ℝ → Set X :=
  fun _ => {x | project x ∈ Q}

theorem pullback_projection_attempt {X C : Type*} (project : X → C) (Q : Set C) :
    DomainProjection project (pullbackDomain project Q) Q := by
  intro t ht x hx
  exact hx

theorem pullback_membership_iff_attempt {X C : Type*} (project : X → C)
    (Q : Set C) (path : ℝ → X) :
    WholePathMembership (pullbackDomain project Q) path ↔
      ∀ t ∈ Set.Icc (0 : ℝ) 1, project (path t) ∈ Q := by
  rfl

theorem fixed_domain_supplies_pullback_attempt {X C : Type*} (project : X → C)
    (D : ℝ → Set X) (Q : Set C) (path : ℝ → X)
    (hProjection : DomainProjection project D Q) (hPath : WholePathMembership D path) :
    WholePathMembership (pullbackDomain project Q) path :=
  (pullback_membership_iff_attempt project Q path).mpr
    (project_whole_path_attempt project D Q path hProjection hPath)

/- Projected membership alone does not certify membership in a specified D. -/
theorem projected_membership_does_not_certify_fixed_domain_attempt :
    (∀ t ∈ Set.Icc (0 : ℝ) 1, (id : ℝ → ℝ) t ∈ (Set.univ : Set ℝ)) ∧
    ¬ WholePathMembership (fun _ : ℝ => Set.Iic (0 : ℝ)) (fun t : ℝ => t) := by
  constructor
  · intro t ht
    exact Set.mem_univ t
  · exact initial_does_not_give_whole_path_attempt.2

/- No concrete projection, whole-path membership, DH binding, integrated
   growth, ODE/continuation or admission witness is constructed here. -/
end
end NEW_BODY6_SLICE_PATHREASSIGNED20260908

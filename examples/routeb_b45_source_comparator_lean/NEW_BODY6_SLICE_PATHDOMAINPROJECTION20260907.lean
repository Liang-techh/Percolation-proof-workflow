import Mathlib

set_option autoImplicit false

namespace NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907
noncomputable section

/- OPEN_UNCOMPILED. X is the full state, C the configuration type.
   project must be the actual source coordinate map, supplied explicitly. -/
def WholePathMembership {X : Type*} (D : ℝ → Set X) (path : ℝ → X) : Prop :=
  ∀ t ∈ Set.Icc (0 : ℝ) 1, path t ∈ D t

def InitialMembership {X : Type*} (D : ℝ → Set X) (path : ℝ → X) : Prop :=
  path 0 ∈ D 0

def DomainProjection {X C : Type*} (project : X → C)
    (D : ℝ → Set X) (Q : Set C) : Prop :=
  ∀ t ∈ Set.Icc (0 : ℝ) 1, ∀ x ∈ D t, project x ∈ Q

theorem whole_path_has_initial_attempt {X : Type*} (D : ℝ → Set X) (path : ℝ → X)
    (hPath : WholePathMembership D path) : InitialMembership D path :=
  hPath 0 (by norm_num)

theorem project_whole_path_attempt {X C : Type*} (project : X → C)
    (D : ℝ → Set X) (Q : Set C) (path : ℝ → X)
    (hProjection : DomainProjection project D Q) (hPath : WholePathMembership D path) :
    ∀ t ∈ Set.Icc (0 : ℝ) 1, project (path t) ∈ Q := by
  intro t ht
  exact hProjection t ht (path t) (hPath t ht)

theorem project_initial_only_attempt {X C : Type*} (project : X → C)
    (D : ℝ → Set X) (Q : Set C) (path : ℝ → X)
    (hProjection : DomainProjection project D Q) (hInitial : InitialMembership D path) :
    project (path 0) ∈ Q :=
  hProjection 0 (by norm_num) (path 0) hInitial

/- This is an INPUT produced by the separate storage-alignment lane.
   The present file does not prove Alignment or bind a physical source. -/
def ShiftIdentityOnQ {X C : Type*} (project : X → C) (Q : Set C)
    (F G : ℝ → X → ℝ) (B : ℝ) : Prop :=
  ∀ t ∈ Set.Icc (0 : ℝ) 1, ∀ x, project x ∈ Q → G t x = F t x + B

theorem projected_shift_cap_transfer_attempt {X C : Type*} (project : X → C)
    (D : ℝ → Set X) (Q : Set C) (path : ℝ → X)
    (F G : ℝ → X → ℝ) (B cap bar : ℝ)
    (hProjection : DomainProjection project D Q) (hPath : WholePathMembership D path)
    (hIdentity : ShiftIdentityOnQ project Q F G B)
    (hCap : ∀ t ∈ Set.Icc (0 : ℝ) 1, F t (path t) ≤ cap)
    (hBudget : cap + B ≤ bar) :
    ∀ t ∈ Set.Icc (0 : ℝ) 1, G t (path t) ≤ bar := by
  intro t ht
  rw [hIdentity t ht (path t) (project_whole_path_attempt project D Q path hProjection hPath t ht)]
  have hBudget' : B + cap ≤ bar := by simpa [add_comm] using hBudget
  exact (add_le_add_right (hCap t ht) B).trans hBudget'

/- If the supplied cap ALREADY bounds F+B, no second shift is charged. -/
theorem already_shifted_cap_transfer_attempt {X C : Type*} (project : X → C)
    (D : ℝ → Set X) (Q : Set C) (path : ℝ → X)
    (F G : ℝ → X → ℝ) (B cap : ℝ)
    (hProjection : DomainProjection project D Q) (hPath : WholePathMembership D path)
    (hIdentity : ShiftIdentityOnQ project Q F G B)
    (hCap : ∀ t ∈ Set.Icc (0 : ℝ) 1, F t (path t) + B ≤ cap) :
    ∀ t ∈ Set.Icc (0 : ℝ) 1, G t (path t) ≤ cap := by
  intro t ht
  rw [hIdentity t ht (path t) (project_whole_path_attempt project D Q path hProjection hPath t ht)]
  exact hCap t ht

/- Exact smooth path with an initial point in D, but no whole-path inclusion.
   This is a logical domain counterexample, not a DH trajectory claim. -/
theorem initial_does_not_give_whole_path_attempt :
    InitialMembership (fun _ : ℝ => Set.Iic (0 : ℝ)) (fun t : ℝ => t) ∧
    ¬ WholePathMembership (fun _ : ℝ => Set.Iic (0 : ℝ)) (fun t : ℝ => t) := by
  constructor
  · norm_num [InitialMembership]
  · intro h
    have hb := h 1 (by norm_num)
    norm_num at hb

def routeBShift : ℝ := 4079979/400000

/- F=0, G=B, cap=B. Correct already-shifted cap holds; charging B again
   rejects it. Conversely dropping B at fixed bar=1 gives a false claim. -/
theorem shift_accounting_counterexample_attempt :
    (0 : ℝ) + routeBShift ≤ routeBShift ∧
    ¬ ((0 : ℝ) + routeBShift + routeBShift ≤ routeBShift) ∧
    (0 : ℝ) ≤ 1 ∧ ¬ routeBShift ≤ 1 := by
  norm_num [routeBShift]

/- No ODE existence, continuation, invariance, path inclusion, domain
   projection or same-source shifted-identity instance is asserted here. -/
end
end NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907

import NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_INITIALPATHCAPS20260907
noncomputable section
open NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907

/- OPEN_UNCOMPILED. Separate statements indexed by the SAME storage/path. -/
def InitialSetCap {X : Type*} (X0 : Set X) (F : ℝ → X → ℝ) (a : ℝ) : Prop :=
  ∀ x ∈ X0, F 0 x ≤ a

def InitialPathCap {X : Type*} (F : ℝ → X → ℝ) (path : ℝ → X) (a : ℝ) : Prop :=
  F 0 (path 0) ≤ a

def FullPathCap {X : Type*} (F : ℝ → X → ℝ) (path : ℝ → X) (cap : ℝ) : Prop :=
  ∀ t ∈ Set.Icc (0 : ℝ) 1, F t (path t) ≤ cap

/- This is the missing integrated growth input, NOT an integration theorem.
   A derivative identity or a numeric ledger does not construct this field. -/
def IntegratedGrowth {X : Type*} (F : ℝ → X → ℝ)
    (path : ℝ → X) (b : ℝ → ℝ) : Prop :=
  ∀ t ∈ Set.Icc (0 : ℝ) 1, F t (path t) ≤ F 0 (path 0) + b t

def ShiftBudget (cap B bar : ℝ) : Prop := cap + B ≤ bar

theorem initial_set_to_path_attempt {X : Type*} (X0 : Set X)
    (F : ℝ → X → ℝ) (path : ℝ → X) (a : ℝ)
    (hInitial : InitialSetCap X0 F a) (hStart : path 0 ∈ X0) :
    InitialPathCap F path a := hInitial (path 0) hStart

theorem growth_supplies_full_cap_attempt {X : Type*} (F : ℝ → X → ℝ)
    (path : ℝ → X) (a beta : ℝ) (b : ℝ → ℝ)
    (hInitial : InitialPathCap F path a) (hGrowth : IntegratedGrowth F path b)
    (hUniform : ∀ t ∈ Set.Icc (0 : ℝ) 1, b t ≤ beta) :
    FullPathCap F path (a + beta) := by
  intro t ht
  exact (hGrowth t ht).trans (add_le_add hInitial (hUniform t ht))

theorem initial_growth_shifted_barrier_attempt {X C : Type*}
    (project : X → C) (X0 : Set X) (D : ℝ → Set X) (Q : Set C)
    (F G : ℝ → X → ℝ) (path : ℝ → X) (a beta B bar : ℝ) (b : ℝ → ℝ)
    (hInitial : InitialSetCap X0 F a) (hStart : path 0 ∈ X0)
    (hGrowth : IntegratedGrowth F path b)
    (hUniform : ∀ t ∈ Set.Icc (0 : ℝ) 1, b t ≤ beta)
    (hProjection : DomainProjection project D Q) (hPath : WholePathMembership D path)
    (hIdentity : ShiftIdentityOnQ project Q F G B)
    (hBudget : ShiftBudget (a + beta) B bar) : FullPathCap G path bar :=
  projected_shift_cap_transfer_attempt project D Q path F G B (a + beta) bar
    hProjection hPath hIdentity
    (growth_supplies_full_cap_attempt F path a beta b
      (initial_set_to_path_attempt X0 F path a hInitial hStart) hGrowth hUniform) hBudget

/- Initial upper bound, global-in-time nonnegativity and terminal zero do
   not themselves supply an upper tube: the exact smooth hump reaches 2. -/
def hump (t : ℝ) (_ : Unit) : ℝ := 8*t*(1-t)

theorem initial_and_terminal_do_not_bound_path_attempt :
    InitialSetCap (Set.univ : Set Unit) hump 0 ∧
    (∀ t ∈ Set.Icc (0 : ℝ) 1, 0 ≤ hump t ()) ∧
    hump 1 () = 0 ∧
    ¬ FullPathCap hump (fun _ => ()) 1 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro x hx
    norm_num [hump]
  · intro t ht
    exact mul_nonneg (mul_nonneg (by norm_num) ht.1) (sub_nonneg.mpr ht.2)
  · norm_num [hump]
  · intro h
    have hb := h (1/2) (by norm_num)
    norm_num [hump] at hb

/- For the ActualShift constant, a nonnegative unshifted cap cannot meet
   bar=1. This is a budget obstruction, not a controller failure theorem. -/
theorem nonnegative_cap_cannot_pay_shift_attempt (cap : ℝ) (hc : 0 ≤ cap) :
    ¬ ShiftBudget cap routeBShift 1 := by
  unfold ShiftBudget routeBShift
  linarith

theorem zero_origin_full_cap_cannot_pay_shift_attempt {X : Type*}
    (F : ℝ → X → ℝ) (path : ℝ → X) (cap : ℝ)
    (hZero : F 0 (path 0) = 0) (hFull : FullPathCap F path cap) :
    ¬ ShiftBudget cap routeBShift 1 := by
  have hStart := hFull 0 (by norm_num)
  rw [hZero] at hStart
  exact nonnegative_cap_cannot_pay_shift_attempt cap hStart

/- An already-shifted full cap is consumed by the separate existing
   already_shifted_cap_transfer_attempt, WITHOUT charging B again.
   No source, path, growth or current ledger instantiation is asserted. -/
end
end NEW_BODY6_SLICE_INITIALPATHCAPS20260907

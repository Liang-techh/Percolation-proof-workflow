import NEW_BODY6_SLICE_INITIALPATHCAPS20260907
import NEW_BODY6_SLICE_ACTUALSTORAGEALIGN20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908
noncomputable section
open NEW_BODY6_SLICE_INITIALPATHCAPS20260907
open NEW_BODY6_SLICE_ACTUALSTORAGEALIGN20260907
open NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907

/- OPEN_UNCOMPILED. One consumer for the existing f=1,h=0 branch, with
   explicit full mechanical state (q,v). No active candidate is selected. -/
abbrev State := Vec × Vec
structure Model where
  H : Mat
  Ma : Vec → Mat
  Me : Vec → Mat
  U : Vec → ℝ
  Uzero : ℝ
  p : Vec

def source (m : Model) (_ : ℝ) (x : State) : ℝ :=
  actualBase m.H m.Ma m.U m.Uzero m.p x.1 x.2

def target (m : Model) (_ : ℝ) (x : State) : ℝ :=
  encodedShifted m.Me x.1 x.2

structure ConsumerPremises (m : Model) (Q : Set Vec) (X0 : Set State)
    (D : ℝ → Set State) (path : ℝ → State) (a beta bar : ℝ) (b : ℝ → ℝ) : Prop where
  alignment : Alignment Q m.H m.Ma m.Me m.U m.Uzero m.p
  initial : InitialSetCap X0 (source m) a
  startsInInitial : path 0 ∈ X0
  growth : IntegratedGrowth (source m) path b
  uniformGrowth : ∀ t ∈ Set.Icc (0 : ℝ) 1, b t ≤ beta
  projection : DomainProjection Prod.fst D Q
  wholePath : WholePathMembership D path
  shiftedBudget : ShiftBudget (a + beta) shiftB bar

/- Alignment supplies the value identity. INITIALPATHCAPS supplies the
   initial -> integrated growth -> full cap composition; B is charged once. -/
theorem consume_aligned_path_cap_attempt (m : Model) (Q : Set Vec) (X0 : Set State)
    (D : ℝ → Set State) (path : ℝ → State) (a beta bar : ℝ) (b : ℝ → ℝ)
    (h : ConsumerPremises m Q X0 D path a beta bar b) :
    FullPathCap (target m) path bar := by
  have hIdentity : ShiftIdentityOnQ Prod.fst Q (source m) (target m) shiftB := by
    intro t ht x hx
    exact (aligned_shifted_identity_attempt Q m.H m.Ma m.Me m.U m.Uzero m.p
      h.alignment x.1 x.2 hx).symm
  exact initial_growth_shifted_barrier_attempt Prod.fst X0 D Q (source m) (target m)
    path a beta shiftB bar b h.initial h.startsInInitial h.growth h.uniformGrowth
    h.projection h.wholePath hIdentity h.shiftedBudget

def normalizedOriginModel (H : Mat) (M : Vec → Mat) (p : Vec) : Model :=
  ⟨H, M, M, RouteBPotentialSlice.potential, RouteBPotentialSlice.potential 0, p⟩

def originPath : ℝ → State := fun _ => (0,0)

/- Exact actual-definition counterexample: even a source full cap of zero
   does not give a target cap of one when B is unpaid. No ODE is asserted. -/
theorem source_full_cap_does_not_pay_shift_attempt (H : Mat) (M : Vec → Mat) (p : Vec) :
    FullPathCap (source (normalizedOriginModel H M p)) originPath 0 ∧
    ¬ FullPathCap (target (normalizedOriginModel H M p)) originPath 1 := by
  constructor
  · intro t ht
    exact le_of_eq (actual_origin_value_attempt H M p)
  · intro h
    have hb := h 0 (by norm_num)
    exact (actual_origin_fixed_bar_counterexample_attempt H M p).2 hb

/- No initial/growth/domain/alignment instance for Route-B, no path ODE,
   positivity, first-exit proof, source admission or compiled receipt. -/
end
end NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908

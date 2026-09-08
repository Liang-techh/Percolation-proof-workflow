import NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908

set_option autoImplicit false

namespace NEW_BODY6_SLICE_PATHCONTRACT20260908
noncomputable section
open NEW_BODY6_SLICE_INITIALPATHCAPS20260907
open NEW_BODY6_SLICE_ACTUALSTORAGEALIGN20260907
open NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908

/- OPEN_UNCOMPILED. A sufficient path interface, not an irredundancy claim.
   Every field refers to the same source F, target G and full-state path. -/
structure PathContract {X : Type*} (F G : ℝ → X → ℝ) (path : ℝ → X)
    (a B bar : ℝ) (b : ℝ → ℝ) : Prop where
  initial : InitialPathCap F path a
  growth : IntegratedGrowth F path b
  value : ∀ t ∈ Set.Icc (0 : ℝ) 1, G t (path t) = F t (path t) + B
  budget : ∀ t ∈ Set.Icc (0 : ℝ) 1, (a + b t) + B ≤ bar

theorem consume_path_contract_attempt {X : Type*} (F G : ℝ → X → ℝ)
    (path : ℝ → X) (a B bar : ℝ) (b : ℝ → ℝ)
    (h : PathContract F G path a B bar b) : FullPathCap G path bar := by
  intro t ht
  have hi : F 0 (path 0) ≤ a := h.initial
  have hg := h.growth t ht
  have hb := h.budget t ht
  rw [h.value t ht]
  linarith

/- The existing domain and alignment fields PRODUCE the on-path identity;
   the contract does not infer path inclusion from an initial condition. -/
theorem aligned_premises_to_path_contract_attempt
    (m : Model) (Q : Set Vec) (X0 : Set State) (D : ℝ → Set State)
    (path : ℝ → State) (a beta bar : ℝ) (b : ℝ → ℝ)
    (h : ConsumerPremises m Q X0 D path a beta bar b) :
    PathContract (source m) (target m) path a shiftB bar b := by
  refine ⟨h.initial (path 0) h.startsInInitial, h.growth, ?_, ?_⟩
  · intro t ht
    have hq : (path t).1 ∈ Q := h.projection t ht (path t) (h.wholePath t ht)
    exact (aligned_shifted_identity_attempt Q m.H m.Ma m.Me m.U m.Uzero m.p
      h.alignment (path t).1 (path t).2 hq).symm
  · intro t ht
    have hu := h.uniformGrowth t ht
    have hb : (a + beta) + shiftB ≤ bar := h.shiftedBudget
    linarith

theorem consume_aligned_via_path_contract_attempt
    (m : Model) (Q : Set Vec) (X0 : Set State) (D : ℝ → Set State)
    (path : ℝ → State) (a beta bar : ℝ) (b : ℝ → ℝ)
    (h : ConsumerPremises m Q X0 D path a beta bar b) :
    FullPathCap (target m) path bar :=
  consume_path_contract_attempt (source m) (target m) path a shiftB bar b
    (aligned_premises_to_path_contract_attempt m Q X0 D path a beta bar b h)

/- No concrete initial/growth/alignment/domain instance or ODE is supplied.
   B occurs once in the target identity and once in its matching budget. -/
end
end NEW_BODY6_SLICE_PATHCONTRACT20260908

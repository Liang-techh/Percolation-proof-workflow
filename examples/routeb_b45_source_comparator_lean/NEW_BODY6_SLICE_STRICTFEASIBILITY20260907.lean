import NEW_BODY6_SLICE_DOMAINREPAIR20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_STRICTFEASIBILITY20260907

noncomputable section

open NEW_BODY6_SLICE_DOMAINREPAIR20260907 NEW_BODY6_SLICE_ENTRYMARGIN20260907
open NEW_BODY6_SLICE_MARGINUNIFORM20260907 NEW_BODY6_SLICE_SCHURMARGIN20260907
open NEW_BODY6_SLICE_VGRAM_Source20260907 NEW_BODY6_SLICE_MASSTAIL_Source20260907

/- OPEN_UNCOMPILED. Feasibility is a proof of existence, not a domain label. -/
def StrictMarginFeasible (D : Set Config) (R : Config → FrontBlock) : Prop :=
  ∃ mu : ℝ, 0 < mu ∧ UniformMargin D R mu

def NonstrictPSD (D : Set Config) (R : Config → FrontBlock) : Prop := UniformMargin D R 0

theorem same_domain_nine_entries_feasible_attempt (D : Set Config) (R : Config → FrontBlock)
    (mu : ℝ) (hp : 0 < mu) (beta : Config → ℝ)
    (he : ∀ q ∈ D, NineEntryLowerBound (R q) mu (beta q)) : StrictMarginFeasible D R := by
  refine ⟨mu, hp, ?_⟩
  intro q hq
  exact nine_entries_to_margin_attempt (R q) mu (beta q) (he q hq)

/- K supplies finitely many labels, not a sample-to-domain inference. Each
   selected cell has a margin over ALL of its points in the same target D. -/
structure FiniteCellMarginCover (D : Set Config) (R : Config → FrontBlock)
    (K : Finset Config) (cells : Config → Set Config) (rho : Config → ℝ) : Prop where
  cover : ∀ q ∈ D, ∃ k ∈ K, q ∈ cells k
  positive : ∀ k ∈ K, 0 < rho k
  cellMargin : ∀ k ∈ K, ∀ q ∈ D, q ∈ cells k → RemainderMargin (R q) (rho k)

theorem finite_cells_feasible_attempt (D : Set Config) (R : Config → FrontBlock)
    (K : Finset Config) (cells : Config → Set Config) (rho : Config → ℝ)
    (hc : FiniteCellMarginCover D R K cells rho) : StrictMarginFeasible D R := by
  obtain ⟨mu, hp, hfloor⟩ := finite_positive_floor_attempt K rho hc.positive
  refine ⟨mu, hp, ?_⟩
  intro q hq
  obtain ⟨k, hk, hcell⟩ := hc.cover q hq
  exact margin_lowering_attempt (R q) (rho k) mu (hc.cellMargin k hk q hq hcell)
    (le_of_lt hp) (hfloor k hk)

/- Nine-entry bounds are one way to discharge per-cell margins. Any other
   rigorous RemainderMargin proof can fill the same cellMargin field. -/
theorem finite_cell_cover_from_entries_attempt (D : Set Config) (R : Config → FrontBlock)
    (K : Finset Config) (cells : Config → Set Config) (rho : Config → ℝ)
    (beta : Config → Config → ℝ)
    (hcover : ∀ q ∈ D, ∃ k ∈ K, q ∈ cells k) (hp : ∀ k ∈ K, 0 < rho k)
    (he : ∀ k ∈ K, ∀ q ∈ D, q ∈ cells k → NineEntryLowerBound (R q) (rho k) (beta k q)) :
    FiniteCellMarginCover D R K cells rho := by
  refine ⟨hcover, hp, ?_⟩
  intro k hk q hq hcell
  exact nine_entries_to_margin_attempt (R q) (rho k) (beta k q) (he k hk q hq hcell)

theorem strict_implies_nonstrict_attempt (D : Set Config) (R : Config → FrontBlock)
    (hf : StrictMarginFeasible D R) : NonstrictPSD D R := by
  obtain ⟨mu, hp, hu⟩ := hf
  intro q hq
  exact margin_lowering_attempt (R q) mu 0 (hu q hq) (by norm_num) (le_of_lt hp)

/- Source binding and the inherited zero-null obstruction remain explicit.
   Exclusion is necessary, whereas feasibility requires a separate witness. -/
structure SourceStrictFeasibilityContract (D : Set Config) (R : Config → FrontBlock) : Prop where
  center : CenterOffsetTarget
  weights : SourceWeightsTarget (3 / 20 : ℝ) (1 / 60 : ℝ)
  sourceEntries : ExactPhysicalFamily D R
  excludesZero : (0 : Config) ∉ D
  feasible : StrictMarginFeasible D R

theorem source_feasibility_excludes_zero_attempt (hc : CenterOffsetTarget)
    (hw : SourceWeightsTarget (3 / 20 : ℝ) (1 / 60 : ℝ))
    (D : Set Config) (R : Config → FrontBlock) (he : ExactPhysicalFamily D R)
    (hf : StrictMarginFeasible D R) : (0 : Config) ∉ D := by
  obtain ⟨mu, hp, hu⟩ := hf
  exact positive_uniform_excludes_zero_attempt hc hw D R mu hp he hu

theorem source_feasibility_contract_attempt (hc : CenterOffsetTarget)
    (hw : SourceWeightsTarget (3 / 20 : ℝ) (1 / 60 : ℝ))
    (D : Set Config) (R : Config → FrontBlock) (he : ExactPhysicalFamily D R)
    (hx : (0 : Config) ∉ D) (hf : StrictMarginFeasible D R) : SourceStrictFeasibilityContract D R :=
  ⟨hc, hw, he, hx, hf⟩

theorem feasible_source_certificate_consumer_attempt (D : Set Config) (R : Config → FrontBlock)
    (hc : SourceStrictFeasibilityContract D R) :
    ∃ mu : ℝ, 0 < mu ∧ SourceDomainMarginCertificate D R mu := by
  obtain ⟨mu, hp, hu⟩ := hc.feasible
  exact ⟨mu, hp, strict_domain_certificate_attempt hc.center hc.weights D R mu hp
    hc.excludesZero hc.sourceEntries hu⟩

/- Reuse the exact abstract counterexample. This domain is separated from
   zero in its first coordinate, not merely missing the single zero point. -/
theorem away_counter_coordinate_gap_attempt : ∀ q ∈ awayCounterDomain, (1 : ℝ) ≤ q 0 := by
  intro q hq
  rcases hq with ⟨n, rfl⟩
  have hn : (0 : ℝ) ≤ (n : ℝ) := Nat.cast_nonneg n
  norm_num [counterConfig, Nat.cast_add, Nat.cast_one] <;> linarith

theorem away_nonstrict_not_strict_attempt :
    (0 : Config) ∉ awayCounterDomain ∧ NonstrictPSD awayCounterDomain counterR ∧
      ¬ StrictMarginFeasible awayCounterDomain counterR := by
  refine ⟨away_counter_excludes_zero_attempt, ?_, away_counter_no_uniform_positive_attempt⟩
  intro q hq
  obtain ⟨rho, hp, hm⟩ := away_counter_pointwise_positive_attempt q hq
  exact margin_lowering_attempt (counterR q) rho 0 hm (by norm_num) (le_of_lt hp)

/- Domain labels, sample PSD and finite collections of sample margins cannot
   fill cover/cellMargin. No actual domain feasibility, full PSD or admission. -/
end
end NEW_BODY6_SLICE_STRICTFEASIBILITY20260907

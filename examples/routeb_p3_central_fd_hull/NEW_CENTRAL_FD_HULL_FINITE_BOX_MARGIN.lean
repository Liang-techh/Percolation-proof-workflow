import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Finset.Lattice
import Mathlib.Tactic

/-!
# P3 finite-box common uniform margin

An explicit nonempty finite box family supplies a common exact-real margin via
`Finset.inf'`.  The result is global only because every domain point is mapped
to a listed box and its region.  Empty boxes and broken continuous coverage are
kept as separate obstructions.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullFiniteBoxMargin

noncomputable section

structure FiniteBoxUniformMargin (D B : Type*) [DecidableEq B] where
  domain : D → Prop
  boxes : Finset B
  boxes_nonempty : boxes.Nonempty
  boxOf : D → B
  region : B → D → Prop
  gapLower : B → ℝ
  weightedLoad : D → ℝ
  capMaxLoad : D → ℝ
  gap_positive : ∀ b, b ∈ boxes → 0 < gapLower b
  mapping_in_boxes : ∀ x, domain x → boxOf x ∈ boxes
  mapping_in_region : ∀ x, domain x → region (boxOf x) x
  box_margin : ∀ b, b ∈ boxes → ∀ x, region b x →
    weightedLoad x + gapLower b ≤ capMaxLoad x

def commonMu
    {D B : Type*} [DecidableEq B]
    (C : FiniteBoxUniformMargin D B) : ℝ :=
  C.boxes.inf' C.boxes_nonempty C.gapLower

theorem common_mu_positive
    {D B : Type*} [DecidableEq B]
    (C : FiniteBoxUniformMargin D B) : 0 < commonMu C := by
  have hMem : commonMu C ∈ C.boxes.image C.gapLower := by
    exact Finset.inf'_mem C.boxes C.boxes_nonempty C.gapLower
  rcases hMem with ⟨b, hb, hValue⟩
  rw [← hValue]
  exact C.gap_positive b hb

theorem common_mu_lower_at
    {D B : Type*} [DecidableEq B]
    (C : FiniteBoxUniformMargin D B) (b : B) (hb : b ∈ C.boxes) :
    commonMu C ≤ C.gapLower b := by
  exact Finset.inf'_le C.boxes C.boxes_nonempty C.gapLower hb

theorem finite_box_global_uniform_margin
    {D B : Type*} [DecidableEq B]
    (C : FiniteBoxUniformMargin D B) :
    ∀ x, C.domain x →
      0 < commonMu C ∧
        commonMu C ≤ C.gapLower (C.boxOf x) ∧
        C.weightedLoad x + commonMu C ≤ C.capMaxLoad x ∧
        C.weightedLoad x < C.capMaxLoad x := by
  intro x hx
  have hb : C.boxOf x ∈ C.boxes := C.mapping_in_boxes x hx
  have hRegion : C.region (C.boxOf x) x := C.mapping_in_region x hx
  have hMuPos : 0 < commonMu C := common_mu_positive C
  have hMuLower : commonMu C ≤ C.gapLower (C.boxOf x) :=
    common_mu_lower_at C (C.boxOf x) hb
  have hBoxMargin :
      C.weightedLoad x + C.gapLower (C.boxOf x) ≤ C.capMaxLoad x :=
    C.box_margin (C.boxOf x) hb x hRegion
  have hUniformMargin :
      C.weightedLoad x + commonMu C ≤ C.capMaxLoad x := by
    linarith
  refine ⟨hMuPos, hMuLower, hUniformMargin, ?_⟩
  linarith

theorem finite_box_consumer_strict
    {D B : Type*} [DecidableEq B]
    (C : FiniteBoxUniformMargin D B)
    (consumer : D → ℝ)
    (hConsumer : ∀ x, C.domain x → consumer x ≤ C.weightedLoad x) :
    ∀ x, C.domain x → consumer x < C.capMaxLoad x := by
  intro x hx
  exact lt_of_le_of_lt (hConsumer x hx)
    (finite_box_global_uniform_margin C x hx).2.2.2

/-! An empty box family has no finite infimum witness. -/

theorem empty_box_obstruction :
    ¬ (∅ : Finset Bool).Nonempty := by
  simp

/-! A listed box and map can leave a domain point outside every region. -/

def brokenBoxes : Finset Bool := {false}

def brokenBoxOf (_ : Bool) : Bool := false

def brokenRegion (b x : Bool) : Prop := b = false ∧ x = false

theorem broken_coverage_obstruction :
    ∃ x : Bool, ¬ (brokenBoxOf x ∈ brokenBoxes ∧
      brokenRegion (brokenBoxOf x) x) := by
  refine ⟨true, ?_⟩
  simp [brokenBoxOf, brokenBoxes, brokenRegion]

/-! Pointwise positive gaps on an unbounded continuous parameter need not be uniform. -/

def continuousGap (x : ℝ) : ℝ := 1 / (x + 1)

theorem continuous_gap_pointwise_positive
    (x : ℝ) (hx : 0 ≤ x) : 0 < continuousGap x := by
  unfold continuousGap
  have hden : 0 < x + 1 := by linarith
  positivity

theorem continuous_gap_no_uniform_positive_lower_bound
    (ε : ℝ) (hε : 0 < ε) :
    ∃ x : ℝ, 0 ≤ x ∧ continuousGap x < ε := by
  refine ⟨1 / ε, ?_, ?_⟩
  · positivity
  · unfold continuousGap
    have hεne : ε ≠ 0 := ne_of_gt hε
    have hden : 0 < 1 + ε := by linarith
    calc
      1 / (1 / ε + 1) = ε / (1 + ε) := by
        field_simp [hεne, ne_of_gt hden]
      _ < ε := by
        apply (div_lt_iff₀ hden).2
        nlinarith [sq_nonneg ε]

end

end RouteBP3CentralFDHullFiniteBoxMargin

#print axioms RouteBP3CentralFDHullFiniteBoxMargin.common_mu_positive
#print axioms RouteBP3CentralFDHullFiniteBoxMargin.finite_box_global_uniform_margin
#print axioms RouteBP3CentralFDHullFiniteBoxMargin.empty_box_obstruction
#print axioms RouteBP3CentralFDHullFiniteBoxMargin.continuous_gap_no_uniform_positive_lower_bound

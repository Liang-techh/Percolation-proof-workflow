import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

/-!
# P3 finite box coverage bridge

This sidecar turns per-box uniform gap certificates into a pointwise strict
capMax conclusion only through an explicit finite-box coverage premise.  It
does not identify boxes with intervals, Taylor cells, samples, or physical
domains.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullBoxCoverage

noncomputable section

structure BoxCoverageCertificate (D B : Type*) [DecidableEq B] where
  domain : D → Prop
  boxes : Finset B
  region : B → D → Prop
  weightedLoad : D → ℝ
  capLoad : D → ℝ
  capMaxLoad : D → ℝ
  uniformGap : B → ℝ
  box_gap_positive : ∀ b, b ∈ boxes → 0 < uniformGap b
  box_gap_lower : ∀ b, b ∈ boxes → ∀ x, region b x →
    uniformGap b ≤ capLoad x - weightedLoad x
  cap_load_upper : ∀ x, domain x → capLoad x ≤ capMaxLoad x
  coverage : ∀ x, domain x → ∃ b, b ∈ boxes ∧ region b x

theorem box_coverage_strict_slack
    {D B : Type*} [DecidableEq B]
    (C : BoxCoverageCertificate D B) :
    ∀ x, C.domain x →
      ∃ b, b ∈ C.boxes ∧ C.region b x ∧
        C.weightedLoad x + C.uniformGap b ≤ C.capMaxLoad x ∧
        C.weightedLoad x < C.capMaxLoad x := by
  intro x hx
  rcases C.coverage x hx with ⟨b, hb, hRegion⟩
  have hGapPos : 0 < C.uniformGap b := C.box_gap_positive b hb
  have hGapLower :
      C.uniformGap b ≤ C.capLoad x - C.weightedLoad x :=
    C.box_gap_lower b hb x hRegion
  have hGapToCap :
      C.weightedLoad x + C.uniformGap b ≤ C.capLoad x := by
    linarith
  have hMargin :
      C.weightedLoad x + C.uniformGap b ≤ C.capMaxLoad x :=
    hGapToCap.trans (C.cap_load_upper x hx)
  refine ⟨b, hb, hRegion, hMargin, ?_⟩
  linarith [hGapPos]

theorem box_coverage_consumer_strict
    {D B : Type*} [DecidableEq B]
    (C : BoxCoverageCertificate D B) (consumer : D → ℝ)
    (hConsumer : ∀ x, C.domain x → consumer x ≤ C.weightedLoad x) :
    ∀ x, C.domain x → consumer x < C.capMaxLoad x := by
  intro x hx
  rcases box_coverage_strict_slack C x hx with
    ⟨b, hb, hRegion, hMargin, hStrict⟩
  exact lt_of_le_of_lt (hConsumer x hx) hStrict

/-! Grid membership alone is not a coverage predicate. -/

def singletonGrid : Finset Bool := {false}

theorem grid_membership_not_global_coverage :
    (∀ x, x ∈ singletonGrid → (0 : ℝ) ≤ 1) ∧
      (∃ y, y ∉ singletonGrid) := by
  constructor
  · intro x hx
    norm_num
  · exact ⟨true, by simp [singletonGrid]⟩

/-! A box family that covers only false leaves true explicitly uncovered. -/

def singletonBoxRegion (b x : Bool) : Prop := b = false ∧ x = false

theorem uncovered_box_not_global :
    ∃ x : Bool, ¬ ∃ b, b ∈ singletonGrid ∧ singletonBoxRegion b x := by
  refine ⟨true, ?_⟩
  simp [singletonGrid, singletonBoxRegion]

end

end RouteBP3CentralFDHullBoxCoverage

#print axioms RouteBP3CentralFDHullBoxCoverage.box_coverage_strict_slack
#print axioms RouteBP3CentralFDHullBoxCoverage.box_coverage_consumer_strict
#print axioms RouteBP3CentralFDHullBoxCoverage.uncovered_box_not_global

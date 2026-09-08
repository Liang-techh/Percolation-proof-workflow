import Mathlib

noncomputable section

namespace RouteBP5ParetoOptimizer

/-- Concave quadratic margin obtained after clearing the T-P5-038 quarter-barrier gate. -/
def margin (A B r : ℝ) : ℝ := A + B * r - 53 * r ^ 2

/-- Exact source-facing expansion of the T-P5-038 gate margin. -/
theorem pareto_margin_expand (E4 E5 r : ℝ) :
    (109 - r) * (250 + 53 * r)
        - 300000 * E4
        - 1200 * (250 + 53 * r) * E5
      = (27250 - 300000 * (E4 + E5))
        + (5527 - 63600 * E5) * r
        - 53 * r ^ 2 := by
  ring

/-- If `B ≤ 0`, the left endpoint `r = 0` maximizes the quadratic on `r ≥ 0`. -/
theorem pareto_margin_left_max
    (A B r : ℝ) (hr0 : 0 ≤ r) (hB : B ≤ 0) :
    margin A B r ≤ A := by
  have hBr : B * r ≤ 0 := mul_nonpos_of_nonpos_of_nonneg hB hr0
  have hrsq : 0 ≤ r ^ 2 := sq_nonneg r
  dsimp [margin]
  nlinarith

/-- If `B ≥ 106`, the right endpoint `r = 1` maximizes on `r ≤ 1`. -/
theorem pareto_margin_right_max
    (A B r : ℝ) (hr1 : r ≤ 1) (hB : 106 ≤ B) :
    margin A B r ≤ A + B - 53 := by
  have hfirst : 0 ≤ 1 - r := sub_nonneg.mpr hr1
  have hsecond : 0 ≤ B - 53 * (1 + r) := by
    nlinarith
  have hprod : 0 ≤ (1 - r) * (B - 53 * (1 + r)) :=
    mul_nonneg hfirst hsecond
  dsimp [margin]
  nlinarith

/-- Exact square-completion gap at the unconstrained vertex `B/106`. -/
theorem pareto_margin_vertex_gap (A B r : ℝ) :
    margin A B (B / 106) - margin A B r
      = 53 * (r - B / 106) ^ 2 := by
  dsimp [margin]
  ring

/-- The unconstrained vertex globally maximizes the concave quadratic. -/
theorem pareto_margin_vertex_max (A B r : ℝ) :
    margin A B r ≤ margin A B (B / 106) := by
  have hgap := pareto_margin_vertex_gap A B r
  have hsquare : 0 ≤ (r - B / 106) ^ 2 := sq_nonneg (r - B / 106)
  nlinarith

/-- Exact value at the vertex; denominator `212 = 4*53` is constant. -/
theorem pareto_margin_vertex_value (A B : ℝ) :
    margin A B (B / 106) = A + B ^ 2 / 212 := by
  dsimp [margin]
  ring

/-- In the interior branch the rational vertex lies strictly inside `[0,1]`. -/
theorem pareto_vertex_mem_Ioo
    (B : ℝ) (hB0 : 0 < B) (hB1 : B < 106) :
    0 < B / 106 ∧ B / 106 < 1 := by
  constructor <;> nlinarith

/-- Piecewise exact optimizer for the entire T-P5-038 convex family. -/
def paretoOpt (B : ℝ) : ℝ :=
  if B ≤ 0 then 0 else if 106 ≤ B then 1 else B / 106

/-- The exact optimizer always belongs to the admissible interpolation interval. -/
theorem paretoOpt_mem_Icc (B : ℝ) :
    0 ≤ paretoOpt B ∧ paretoOpt B ≤ 1 := by
  by_cases h0 : B ≤ 0
  · simp [paretoOpt, h0]
  · have hpos : 0 < B := lt_of_not_ge h0
    by_cases h106 : 106 ≤ B
    · simp [paretoOpt, h0, h106]
    · have hlt : B < 106 := lt_of_not_ge h106
      have hv := pareto_vertex_mem_Ioo B hpos hlt
      simp [paretoOpt, h0, h106, le_of_lt hv.1, le_of_lt hv.2]

/-- Every admissible parameter has margin at most the piecewise exact optimizer. -/
theorem pareto_optimal_selector
    (A B r : ℝ) (hr0 : 0 ≤ r) (hr1 : r ≤ 1) :
    margin A B r ≤ margin A B (paretoOpt B) := by
  by_cases h0 : B ≤ 0
  · have h := pareto_margin_left_max A B r hr0 h0
    simpa [paretoOpt, h0, margin] using h
  · by_cases h106 : 106 ≤ B
    · have h := pareto_margin_right_max A B r hr1 h106
      simpa [paretoOpt, h0, h106, margin] using h
    · have h := pareto_margin_vertex_max A B r
      simpa [paretoOpt, h0, h106] using h

/-- Interior positivity is equivalent to the division-free discriminant check. -/
theorem pareto_vertex_positive_iff (A B : ℝ) :
    0 < margin A B (B / 106) ↔ 0 < 212 * A + B ^ 2 := by
  rw [pareto_margin_vertex_value]
  constructor <;> intro h <;> nlinarith

/--
Exact necessary-and-sufficient feasibility test for the whole one-parameter
T-P5-038 certificate family. Boundary cases `B=0` and `B=106` are assigned to
the endpoint branches, while the open middle branch uses a division-free test.
-/
theorem pareto_gate_exists_iff (A B : ℝ) :
    (∃ r : ℝ, 0 ≤ r ∧ r ≤ 1 ∧ 0 < margin A B r) ↔
      (B ≤ 0 ∧ 0 < A) ∨
      (106 ≤ B ∧ 0 < A + B - 53) ∨
      (0 < B ∧ B < 106 ∧ 0 < 212 * A + B ^ 2) := by
  constructor
  · rintro ⟨r, hr0, hr1, hpos⟩
    by_cases hleft : B ≤ 0
    · have hmax := pareto_margin_left_max A B r hr0 hleft
      exact Or.inl ⟨hleft, lt_of_lt_of_le hpos hmax⟩
    · have hBpos : 0 < B := lt_of_not_ge hleft
      by_cases hright : 106 ≤ B
      · have hmax := pareto_margin_right_max A B r hr1 hright
        exact Or.inr (Or.inl ⟨hright, lt_of_lt_of_le hpos hmax⟩)
      · have hBlt : B < 106 := lt_of_not_ge hright
        have hmax := pareto_margin_vertex_max A B r
        have hvertex : 0 < margin A B (B / 106) := lt_of_lt_of_le hpos hmax
        have hcrit : 0 < 212 * A + B ^ 2 :=
          (pareto_vertex_positive_iff A B).mp hvertex
        exact Or.inr (Or.inr ⟨hBpos, hBlt, hcrit⟩)
  · intro hbranches
    rcases hbranches with hleft | hrest
    · rcases hleft with ⟨_hB, hA⟩
      refine ⟨0, by norm_num, by norm_num, ?_⟩
      simpa [margin] using hA
    · rcases hrest with hright | hinterior
      · rcases hright with ⟨_hB, hA⟩
        refine ⟨1, by norm_num, by norm_num, ?_⟩
        dsimp [margin]
        nlinarith
      · rcases hinterior with ⟨hB0, hB1, hcrit⟩
        have hv := pareto_vertex_mem_Ioo B hB0 hB1
        refine ⟨B / 106, le_of_lt hv.1, le_of_lt hv.2, ?_⟩
        exact (pareto_vertex_positive_iff A B).mpr hcrit

/-- Branch-wise nonpositive maxima rule out every parameter in the convex family. -/
theorem pareto_gate_impossible_of_branch_nonpositive
    (A B : ℝ)
    (hleft : B ≤ 0 → A ≤ 0)
    (hright : 106 ≤ B → A + B - 53 ≤ 0)
    (hinterior : 0 < B → B < 106 → 212 * A + B ^ 2 ≤ 0) :
    ¬ ∃ r : ℝ, 0 ≤ r ∧ r ≤ 1 ∧ 0 < margin A B r := by
  intro hex
  rcases (pareto_gate_exists_iff A B).mp hex with hL | hR | hI
  · exact (not_lt_of_ge (hleft hL.1)) hL.2
  · exact (not_lt_of_ge (hright hR.1)) hR.2
  · exact (not_lt_of_ge (hinterior hI.1 hI.2.1)) hI.2.2

/-- In the interior branch, the vertex strictly improves on the `r=0` endpoint. -/
theorem pareto_interior_strict_gain_over_left
    (A B : ℝ) (hB0 : 0 < B) :
    0 < margin A B (B / 106) - margin A B 0 := by
  rw [pareto_margin_vertex_value]
  have hsq : 0 < B ^ 2 := by positivity
  dsimp [margin]
  nlinarith

/-- In the interior branch, the vertex strictly improves on the `r=1` endpoint. -/
theorem pareto_interior_strict_gain_over_right
    (A B : ℝ) (hB1 : B < 106) :
    0 < margin A B (B / 106) - margin A B 1 := by
  rw [pareto_margin_vertex_value]
  have hsq : 0 < (106 - B) ^ 2 := by positivity
  dsimp [margin]
  nlinarith

/-- Source-facing threshold selecting the anisotropic/right endpoint branch. -/
theorem pareto_selector_right_threshold (E5 : ℝ) :
    106 ≤ 5527 - 63600 * E5 ↔ E5 ≤ (1807 / 21200 : ℝ) := by
  constructor <;> intro h <;> nlinarith

/-- Source-facing threshold selecting the scalar/left endpoint branch. -/
theorem pareto_selector_left_threshold (E5 : ℝ) :
    5527 - 63600 * E5 ≤ 0 ↔ (5527 / 63600 : ℝ) ≤ E5 := by
  constructor <;> intro h <;> nlinarith

/--
Exact regression witness from T-P5-039: both endpoint margins are negative,
while the interior optimizer `r=1/2` has positive margin `49/4`.
-/
theorem pareto_interior_endpoint_failure_witness :
    let E5 : ℝ := 2737 / 31800
    let E4 : ℝ := 75803 / 15900000
    let A : ℝ := 27250 - 300000 * (E4 + E5)
    let B : ℝ := 5527 - 63600 * E5
    margin A B 0 = -1 ∧
      margin A B 1 = -1 ∧
      margin A B (1 / 2) = 49 / 4 := by
  norm_num [margin]

#print axioms pareto_margin_expand
#print axioms pareto_margin_left_max
#print axioms pareto_margin_right_max
#print axioms pareto_margin_vertex_gap
#print axioms pareto_margin_vertex_max
#print axioms pareto_margin_vertex_value
#print axioms pareto_vertex_mem_Ioo
#print axioms paretoOpt_mem_Icc
#print axioms pareto_optimal_selector
#print axioms pareto_vertex_positive_iff
#print axioms pareto_gate_exists_iff
#print axioms pareto_gate_impossible_of_branch_nonpositive
#print axioms pareto_interior_strict_gain_over_left
#print axioms pareto_interior_strict_gain_over_right
#print axioms pareto_selector_right_threshold
#print axioms pareto_selector_left_threshold
#print axioms pareto_interior_endpoint_failure_witness

end RouteBP5ParetoOptimizer

import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic

/-!
# Route-B P4 robust exact-real phase cells

Source-independent Lean decomposition of
`agent_review_inbox/review-T-P4-036.2-guyuefangyuan-robust-phase-cells-20260907T1434.md`.

This sidecar proves the exact-real trigonometric consumer only: a base cell from
`|r| <= b`, transport of an upstream formed-angle error to a reduced radius,
quarter-turn phase transport, the finite six-link theta/alpha phase tables, and
robust source-facing seams.  It deliberately contains no Float64/libm/runtime,
source-execution, coverage, receipt/provenance, admission, or final-integration
claim.
-/

set_option autoImplicit false

namespace RouteBP4RobustPhaseCells

noncomputable section

/-- Three source phases occurring in the six-link DH table. -/
inductive QuarterPhase
  | neg
  | zero
  | pos
  deriving DecidableEq, Repr

open QuarterPhase

/-- Exact quarter-turn center associated with a finite source phase. -/
def phaseShift : QuarterPhase → ℝ
  | neg => -(Real.pi / 2)
  | zero => 0
  | pos => Real.pi / 2

/-- Exact angle obtained from a reduced coordinate and a quarter-turn phase. -/
def phaseAngle (p : QuarterPhase) (r : ℝ) : ℝ := r + phaseShift p

/-- Lower sine endpoint of the robust phase cell with radius `b`. -/
def phaseSinLower (p : QuarterPhase) (b : ℝ) : ℝ :=
  match p with
  | neg => -1
  | zero => -b
  | pos => 1 - b^2 / 2

/-- Upper sine endpoint of the robust phase cell with radius `b`. -/
def phaseSinUpper (p : QuarterPhase) (b : ℝ) : ℝ :=
  match p with
  | neg => -(1 - b^2 / 2)
  | zero => b
  | pos => 1

/-- Lower cosine endpoint of the robust phase cell with radius `b`. -/
def phaseCosLower (p : QuarterPhase) (b : ℝ) : ℝ :=
  match p with
  | neg => -b
  | zero => 1 - b^2 / 2
  | pos => -b

/-- Upper cosine endpoint of the robust phase cell with radius `b`. -/
def phaseCosUpper (p : QuarterPhase) (b : ℝ) : ℝ :=
  match p with
  | neg => b
  | zero => 1
  | pos => b

/-- The base exact-real cell.  No small-angle assumption is needed. -/
theorem base_trig_cell_of_abs_le
    (r b : ℝ) (hb : 0 ≤ b) (hr : |r| ≤ b) :
    -b ≤ Real.sin r ∧ Real.sin r ≤ b ∧
      1 - b^2 / 2 ≤ Real.cos r ∧ Real.cos r ≤ 1 := by
  have hSinAbs : |Real.sin r| ≤ b := Real.abs_sin_le_abs.trans hr
  have hSin := abs_le.mp hSinAbs
  have hBounds := abs_le.mp hr
  have hSq : r^2 ≤ b^2 := sq_le_sq' hBounds.1 hBounds.2
  have hCosBase : 1 - r^2 / 2 ≤ Real.cos r := Real.one_sub_sq_div_two_le_cos
  refine ⟨hSin.1, hSin.2, ?_, Real.cos_le_one r⟩
  linarith

/-- Formed-angle error transports directly to a reduced-radius bound.  The
center is abstract here; the quarter-turn specialization is source-facing. -/
theorem formed_angle_error_to_reduced_radius
    (q xhat center eps a : ℝ)
    (hform : |xhat - (q + center)| ≤ eps)
    (hq : |q| ≤ a) :
    |xhat - center| ≤ a + eps := by
  have hRewrite : xhat - center = (xhat - (q + center)) + q := by ring
  rw [hRewrite]
  calc
    |xhat - (q + center) + q| ≤ |xhat - (q + center)| + |q| := abs_add _ _
    _ ≤ eps + a := add_le_add hform hq
    _ = a + eps := by ring

/-- Negative-quarter-turn transport of the base cell. -/
theorem phase_neg_quarter_cell
    (r b : ℝ) (hb : 0 ≤ b) (hr : |r| ≤ b) :
    -1 ≤ Real.sin (r - Real.pi / 2) ∧
      Real.sin (r - Real.pi / 2) ≤ -(1 - b^2 / 2) ∧
      -b ≤ Real.cos (r - Real.pi / 2) ∧
      Real.cos (r - Real.pi / 2) ≤ b := by
  rcases base_trig_cell_of_abs_le r b hb hr with ⟨hsL, hsU, hcL, hcU⟩
  rw [Real.sin_sub_pi_div_two, Real.cos_sub_pi_div_two]
  constructor
  · linarith
  constructor
  · linarith
  constructor
  · exact hsL
  · exact hsU

/-- Zero-phase transport is exactly the base cell. -/
theorem phase_zero_cell
    (r b : ℝ) (hb : 0 ≤ b) (hr : |r| ≤ b) :
    -b ≤ Real.sin r ∧ Real.sin r ≤ b ∧
      1 - b^2 / 2 ≤ Real.cos r ∧ Real.cos r ≤ 1 :=
  base_trig_cell_of_abs_le r b hb hr

/-- Positive-quarter-turn transport of the base cell. -/
theorem phase_pos_quarter_cell
    (r b : ℝ) (hb : 0 ≤ b) (hr : |r| ≤ b) :
    1 - b^2 / 2 ≤ Real.sin (r + Real.pi / 2) ∧
      Real.sin (r + Real.pi / 2) ≤ 1 ∧
      -b ≤ Real.cos (r + Real.pi / 2) ∧
      Real.cos (r + Real.pi / 2) ≤ b := by
  rcases base_trig_cell_of_abs_le r b hb hr with ⟨hsL, hsU, hcL, hcU⟩
  rw [Real.sin_add_pi_div_two, Real.cos_add_pi_div_two]
  constructor
  · exact hcL
  constructor
  · exact hcU
  constructor
  · linarith
  · linarith

/-- Uniform finite-phase cell, avoiding a generic integer range-reduction
statement because the source table contains only `-1, 0, +1`. -/
theorem quarter_phase_cell
    (p : QuarterPhase) (r b : ℝ) (hb : 0 ≤ b) (hr : |r| ≤ b) :
    phaseSinLower p b ≤ Real.sin (phaseAngle p r) ∧
      Real.sin (phaseAngle p r) ≤ phaseSinUpper p b ∧
      phaseCosLower p b ≤ Real.cos (phaseAngle p r) ∧
      Real.cos (phaseAngle p r) ≤ phaseCosUpper p b := by
  cases p with
  | neg =>
      simpa [phaseSinLower, phaseSinUpper, phaseCosLower, phaseCosUpper,
        phaseAngle, phaseShift, sub_eq_add_neg] using
        phase_neg_quarter_cell r b hb hr
  | zero =>
      simpa [phaseSinLower, phaseSinUpper, phaseCosLower, phaseCosUpper,
        phaseAngle, phaseShift] using phase_zero_cell r b hb hr
  | pos =>
      simpa [phaseSinLower, phaseSinUpper, phaseCosLower, phaseCosUpper,
        phaseAngle, phaseShift] using phase_pos_quarter_cell r b hb hr

/-- Canonical theta phase table `(0,-1,+1,0,0,0)`. -/
def phaseTheta : Fin 6 → QuarterPhase :=
  ![zero, neg, pos, zero, zero, zero]

/-- Canonical alpha phase table `(-1,0,+1,-1,+1,0)`. -/
def phaseAlpha : Fin 6 → QuarterPhase :=
  ![neg, zero, pos, neg, pos, zero]

/-- Exact rational identity for the declared theta q-box radius. -/
theorem theta_cos_lower_constant :
    (1 : ℝ) - ((3 : ℝ) / 20)^2 / 2 = 791 / 800 := by
  norm_num

/-- All six exact-real theta rows follow from the single q-box radius and the
finite source phase table. -/
theorem theta_all6_exact_cells_from_qbox
    (q : Fin 6 → ℝ) (hq : ∀ i, |q i| ≤ (3 : ℝ) / 20) (i : Fin 6) :
    phaseSinLower (phaseTheta i) ((3 : ℝ) / 20) ≤
        Real.sin (phaseAngle (phaseTheta i) (q i)) ∧
      Real.sin (phaseAngle (phaseTheta i) (q i)) ≤
        phaseSinUpper (phaseTheta i) ((3 : ℝ) / 20) ∧
      phaseCosLower (phaseTheta i) ((3 : ℝ) / 20) ≤
        Real.cos (phaseAngle (phaseTheta i) (q i)) ∧
      Real.cos (phaseAngle (phaseTheta i) (q i)) ≤
        phaseCosUpper (phaseTheta i) ((3 : ℝ) / 20) := by
  exact quarter_phase_cell (phaseTheta i) (q i) ((3 : ℝ) / 20) (by norm_num) (hq i)

/-- All six exact-real alpha rows collapse to radius zero and the finite source
phase table. -/
theorem alpha_all6_exact_cells (i : Fin 6) :
    phaseSinLower (phaseAlpha i) 0 ≤ Real.sin (phaseAngle (phaseAlpha i) 0) ∧
      Real.sin (phaseAngle (phaseAlpha i) 0) ≤ phaseSinUpper (phaseAlpha i) 0 ∧
      phaseCosLower (phaseAlpha i) 0 ≤ Real.cos (phaseAngle (phaseAlpha i) 0) ∧
      Real.cos (phaseAngle (phaseAlpha i) 0) ≤ phaseCosUpper (phaseAlpha i) 0 := by
  exact quarter_phase_cell (phaseAlpha i) 0 0 (by norm_num) (by norm_num)

/-- Robust exact-real seam: an upstream absolute error on a formed angle widens
only the scalar reduced radius from `a` to `a + eps`. -/
theorem robust_phase_cell_of_formed_angle_error
    (p : QuarterPhase) (q xhat a eps : ℝ)
    (ha : 0 ≤ a) (heps : 0 ≤ eps)
    (hq : |q| ≤ a)
    (hform : |xhat - phaseAngle p q| ≤ eps) :
    phaseSinLower p (a + eps) ≤ Real.sin xhat ∧
      Real.sin xhat ≤ phaseSinUpper p (a + eps) ∧
      phaseCosLower p (a + eps) ≤ Real.cos xhat ∧
      Real.cos xhat ≤ phaseCosUpper p (a + eps) := by
  have hReduced : |xhat - phaseShift p| ≤ a + eps := by
    exact formed_angle_error_to_reduced_radius q xhat (phaseShift p) eps a hform hq
  have hCell := quarter_phase_cell p (xhat - phaseShift p) (a + eps)
    (add_nonneg ha heps) hReduced
  have hRecover : phaseAngle p (xhat - phaseShift p) = xhat := by
    simp [phaseAngle]
  rwa [hRecover] at hCell

/-- Source-facing robust theta seam. -/
theorem robust_theta_cell_of_formed_angle_error
    (i : Fin 6) (q xhat eps : ℝ)
    (heps : 0 ≤ eps) (hq : |q| ≤ (3 : ℝ) / 20)
    (hform : |xhat - phaseAngle (phaseTheta i) q| ≤ eps) :
    phaseSinLower (phaseTheta i) ((3 : ℝ) / 20 + eps) ≤ Real.sin xhat ∧
      Real.sin xhat ≤ phaseSinUpper (phaseTheta i) ((3 : ℝ) / 20 + eps) ∧
      phaseCosLower (phaseTheta i) ((3 : ℝ) / 20 + eps) ≤ Real.cos xhat ∧
      Real.cos xhat ≤ phaseCosUpper (phaseTheta i) ((3 : ℝ) / 20 + eps) := by
  exact robust_phase_cell_of_formed_angle_error
    (phaseTheta i) q xhat ((3 : ℝ) / 20) eps (by norm_num) heps hq hform

/-- Source-facing robust alpha seam. -/
theorem robust_alpha_cell_of_formed_angle_error
    (i : Fin 6) (xhat eps : ℝ)
    (heps : 0 ≤ eps)
    (hform : |xhat - phaseAngle (phaseAlpha i) 0| ≤ eps) :
    phaseSinLower (phaseAlpha i) eps ≤ Real.sin xhat ∧
      Real.sin xhat ≤ phaseSinUpper (phaseAlpha i) eps ∧
      phaseCosLower (phaseAlpha i) eps ≤ Real.cos xhat ∧
      Real.cos xhat ≤ phaseCosUpper (phaseAlpha i) eps := by
  simpa using robust_phase_cell_of_formed_angle_error
    (phaseAlpha i) 0 xhat 0 eps (by norm_num) heps (by norm_num) hform

#print axioms base_trig_cell_of_abs_le
#print axioms formed_angle_error_to_reduced_radius
#print axioms phase_neg_quarter_cell
#print axioms phase_zero_cell
#print axioms phase_pos_quarter_cell
#print axioms quarter_phase_cell
#print axioms theta_cos_lower_constant
#print axioms theta_all6_exact_cells_from_qbox
#print axioms alpha_all6_exact_cells
#print axioms robust_phase_cell_of_formed_angle_error
#print axioms robust_theta_cell_of_formed_angle_error
#print axioms robust_alpha_cell_of_formed_angle_error

end

end RouteBP4RobustPhaseCells

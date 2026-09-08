import NEW_CENTRAL_FD_HULL_C2C3_SOURCE_BINDING
import Mathlib.Tactic

/-!
# P3 central-FD remainder to exact-real DH derivative

This bounded contract consumes the existing C2/C3 source binding.  It keeps
the central-FD evaluator, the exact source function, the step, and the box
region tied together, then exposes the independent C3 remainder theorem and
residual budget needed for absorption.

The remainder theorem is intentionally a premise: endpoint values and a
pointwise third-derivative hull do not by themselves prove a central-FD error
bound on the whole segment.  Status: OPEN_UNCOMPILED.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullC2C3CentralFDRemainder

noncomputable section

open RouteBP3CentralFDHullC2C3SourceBinding

structure CentralFDSourceContract (D B : Type*) [DecidableEq B]
    [AddCommGroup D] [Module ℝ D] where
  source : C2C3SourceBinding D B
  dhFirstDerivative : D → ℝ
  centralFDEvaluator : D → ℝ
  plusPoint : B → D → D
  minusPoint : B → D → D
  direction : B → D
  step : B → ℝ
  residualBudget : B → ℝ
  c3Regularity : B → Prop
  regularity_sound : ∀ b, b ∈ source.boxes → c3Regularity b

  /- The concrete DH derivative is the same source derivative on each box. -/
  dh_first_binding : ∀ b, b ∈ source.boxes → ∀ x, source.region b x →
    source.taylorFirstDerivative x = dhFirstDerivative x

  step_pos : ∀ b, b ∈ source.boxes → 0 < step b

  shift_step_semantics : ∀ b, b ∈ source.boxes → ∀ x,
    plusPoint b x = x + step b • direction b ∧
      minusPoint b x = x - step b • direction b

  /- Both shifted evaluations stay in the same source box. -/
  shifted_points_same_box : ∀ b, b ∈ source.boxes → ∀ x, source.region b x →
    source.region b (plusPoint b x) ∧ source.region b (minusPoint b x)

  /- The evaluator is the central difference of this exact source function. -/
  central_fd_source_identity : ∀ b, b ∈ source.boxes → ∀ x, source.region b x →
    centralFDEvaluator x =
      (source.sourceFunction (plusPoint b x) -
        source.sourceFunction (minusPoint b x)) / (2 * step b)

  /- This is the analytic C3/Taylor remainder obligation on the same box. -/
  central_fd_remainder_sound : ∀ b, b ∈ source.boxes → c3Regularity b →
    ∀ x, source.region b x →
    |centralFDEvaluator x - source.sourceFirstDerivative x| ≤
      step b ^ 2 * source.thirdDerivativeHull b / 6

  /- This is the separate residual-absorption budget. -/
  residual_absorption_budget : ∀ b, b ∈ source.boxes →
    step b ^ 2 * source.thirdDerivativeHull b / 6 ≤ residualBudget b

theorem central_fd_error_to_dh_derivative_at_covered_point
    {D B : Type*} [DecidableEq B] [AddCommGroup D] [Module ℝ D]
    (C : CentralFDSourceContract D B) (x : D) (hx : C.source.domain x) :
      C.centralFDEvaluator x =
        (C.source.sourceFunction (C.plusPoint (C.source.boxOf x) x) -
          C.source.sourceFunction (C.minusPoint (C.source.boxOf x) x)) /
          (2 * C.step (C.source.boxOf x)) ∧
      C.plusPoint (C.source.boxOf x) x =
          x + C.step (C.source.boxOf x) • C.direction (C.source.boxOf x) ∧
      C.minusPoint (C.source.boxOf x) x =
          x - C.step (C.source.boxOf x) • C.direction (C.source.boxOf x) ∧
      C.source.region (C.source.boxOf x) (C.plusPoint (C.source.boxOf x) x) ∧
      C.source.region (C.source.boxOf x) (C.minusPoint (C.source.boxOf x) x) ∧
      |C.centralFDEvaluator x - C.dhFirstDerivative x| ≤
        C.residualBudget (C.source.boxOf x) := by
  have hCoverage := C.source.coverage x hx
  have hb : C.source.boxOf x ∈ C.source.boxes := hCoverage.1
  have hRegion : C.source.region (C.source.boxOf x) x := hCoverage.2
  have hStep := C.shift_step_semantics (C.source.boxOf x) hb x
  have hShift := C.shifted_points_same_box (C.source.boxOf x) hb x hRegion
  have hEvaluator := C.central_fd_source_identity
    (C.source.boxOf x) hb x hRegion
  have hTaylorDerivative := C.dh_first_binding
    (C.source.boxOf x) hb x hRegion
  have hRegularity := C.regularity_sound (C.source.boxOf x) hb
  have hSourceDerivative :
      C.source.sourceFirstDerivative x = C.dhFirstDerivative x :=
    (C.source.same_first_derivative (C.source.boxOf x) hb x hRegion).symm.trans
      hTaylorDerivative
  have hRemainder := C.central_fd_remainder_sound
    (C.source.boxOf x) hb hRegularity x hRegion
  have hBudget := C.residual_absorption_budget (C.source.boxOf x) hb
  have hDhRemainder :
      |C.centralFDEvaluator x - C.dhFirstDerivative x| ≤
        C.step (C.source.boxOf x) ^ 2 *
          C.source.thirdDerivativeHull (C.source.boxOf x) / 6 := by
    rw [hSourceDerivative] at hRemainder
    exact hRemainder
  refine ⟨hEvaluator, hStep.1, hStep.2, hShift.1, hShift.2, ?_⟩
  exact le_trans hDhRemainder hBudget

/-! Exact cubic obstruction to a zero central-FD remainder bound. -/

def cubic : ℝ → ℝ := fun x => x ^ 3

def cubicCentralFDAtZero : ℝ :=
  (cubic 1 - cubic (-1)) / (2 : ℝ)

def cubicDerivativeAtZero : ℝ := 0

theorem cubic_zero_remainder_bound_obstruction :
    ¬ |cubicCentralFDAtZero - cubicDerivativeAtZero| ≤ 0 := by
  norm_num [cubicCentralFDAtZero, cubicDerivativeAtZero, cubic]

end

end RouteBP3CentralFDHullC2C3CentralFDRemainder

#print axioms RouteBP3CentralFDHullC2C3CentralFDRemainder.central_fd_error_to_dh_derivative_at_covered_point
#print axioms RouteBP3CentralFDHullC2C3CentralFDRemainder.cubic_zero_remainder_bound_obstruction

import NEW_CENTRAL_FD_HULL_C2C3_SOURCE_BINDING
import Mathlib.Tactic

/-!
# P3 minimal C2/C3 derivative-level DH binding

This companion does not redefine the source binding and does not repeat the
endpoint consumer.  It adds only the same-box equalities between the Taylor
derivative fields and supplied concrete DH evaluator derivative functions.
Together with the existing Taylor-to-source equalities, these premises yield
source-derivative equality at one covered point.

The supplied derivative functions are still abstract exact-real inputs.  No
claim is made that they are derivatives of the deployed Float64 evaluator.
Status: OPEN_UNCOMPILED.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullC2C3DerivativeBinding

noncomputable section

open RouteBP3CentralFDHullC2C3SourceBinding

theorem source_derivatives_eq_concrete_dh_derivatives_at_covered_point
    {D B : Type*} [DecidableEq B]
    (E : C2C3SourceBinding D B)
    (dhFirst dhSecond dhThird : D → ℝ)
    (hFirst : ∀ b, b ∈ E.boxes → ∀ x, E.region b x →
      E.taylorFirstDerivative x = dhFirst x)
    (hSecond : ∀ b, b ∈ E.boxes → ∀ x, E.region b x →
      E.taylorSecondDerivative x = dhSecond x)
    (hThird : ∀ b, b ∈ E.boxes → ∀ x, E.region b x →
      E.taylorThirdDerivative x = dhThird x)
    (x : D) (hx : E.domain x) :
    E.sourceFirstDerivative x = dhFirst x ∧
      E.sourceSecondDerivative x = dhSecond x ∧
      E.sourceThirdDerivative x = dhThird x := by
  have hCoverage := E.coverage x hx
  have hb : E.boxOf x ∈ E.boxes := hCoverage.1
  have hRegion : E.region (E.boxOf x) x := hCoverage.2
  have hFirstSame := E.same_first_derivative (E.boxOf x) hb x hRegion
  have hSecondSame := E.same_second_derivative (E.boxOf x) hb x hRegion
  have hThirdSame := E.same_third_derivative (E.boxOf x) hb x hRegion
  have hFirstConcrete := hFirst (E.boxOf x) hb x hRegion
  have hSecondConcrete := hSecond (E.boxOf x) hb x hRegion
  have hThirdConcrete := hThird (E.boxOf x) hb x hRegion
  exact ⟨hFirstSame.symm.trans hFirstConcrete,
    hSecondSame.symm.trans hSecondConcrete,
    hThirdSame.symm.trans hThirdConcrete⟩

/-! Value identity alone does not determine derivative fields. -/

def obstructionValue : Bool → ℝ := fun _ => 0

def obstructionSourceDerivative : Bool → ℝ := fun _ => 0

def obstructionEvaluatorDerivative : Bool → ℝ := fun _ => 1

theorem value_identity_does_not_force_derivative_identity :
    (∀ x, obstructionValue x = obstructionValue x) ∧
      ¬ (∀ x, obstructionSourceDerivative x = obstructionEvaluatorDerivative x) := by
  constructor
  · intro x
    rfl
  · intro h
    have hFalse := h false
    norm_num [obstructionSourceDerivative, obstructionEvaluatorDerivative] at hFalse

end

end RouteBP3CentralFDHullC2C3DerivativeBinding

#print axioms RouteBP3CentralFDHullC2C3DerivativeBinding.source_derivatives_eq_concrete_dh_derivatives_at_covered_point
#print axioms RouteBP3CentralFDHullC2C3DerivativeBinding.value_identity_does_not_force_derivative_identity

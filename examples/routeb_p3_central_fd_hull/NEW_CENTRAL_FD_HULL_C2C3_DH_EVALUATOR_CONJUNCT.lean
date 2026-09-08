import NEW_CENTRAL_FD_HULL_C2C3_ENDPOINT_UNIFORM_CONSUMER
import Mathlib.Tactic

/-!
# P3 minimal C2/C3 to DH-evaluator conjunct

This companion adds one value-level source seam without redefining either the
source binding or the endpoint consumer.  If an exact-real DH evaluator is
identified with the existing `sourceM + sourceC + sourceG` expression on the
domain, the existing source identity binds the Taylor/source function to that
evaluator at the same covered point.  The endpoint-uniform margin is then
reused as a separate consumer result.

This does not infer derivatives of the DH evaluator from value equality.  The
derivative-level evaluator binding, concrete Float64/source proof, flowpipe,
and residual obligations remain open.  Status: OPEN_UNCOMPILED.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullC2C3DHEvaluatorConjunct

noncomputable section

open RouteBP3CentralFDHullC2C3SourceBinding
open RouteBP3CentralFDHullC2C3EndpointUniformConsumer

theorem source_function_eq_dh_evaluator_at_covered_point
    {D B : Type*} [DecidableEq B]
    (C : EndpointUniformConsumer D B)
    (dhEvaluator : D → ℝ)
    (hEvaluator : ∀ x, C.source.domain x →
      dhEvaluator x =
        C.source.sourceM x + C.source.sourceC x + C.source.sourceG x)
    (x : D) (hx : C.source.domain x) :
    C.source.sourceFunction x = dhEvaluator x := by
  calc
    C.source.sourceFunction x =
        C.source.sourceM x + C.source.sourceC x + C.source.sourceG x :=
      source_dh_identity_at_covered_point C.source x hx
    _ = dhEvaluator x := (hEvaluator x hx).symm

theorem dh_evaluator_at_same_covered_point_has_uniform_margin
    {D B : Type*} [DecidableEq B]
    (C : EndpointUniformConsumer D B)
    (dhEvaluator : D → ℝ)
    (hEvaluator : ∀ x, C.source.domain x →
      dhEvaluator x =
        C.source.sourceM x + C.source.sourceC x + C.source.sourceG x)
    (x : D) (hx : C.source.domain x) :
    C.source.sourceFunction x = dhEvaluator x ∧
      0 < commonMu C ∧
      C.weightedLoad x + commonMu C ≤ C.capMaxLoad x := by
  have hSource := source_function_eq_dh_evaluator_at_covered_point
    C dhEvaluator hEvaluator x hx
  have hMargin := source_endpoint_to_common_uniform_margin C x hx
  have hPositive : 0 < commonMu C := hMargin.2.2.2.2.2
  have hUniform :
      C.weightedLoad x + commonMu C ≤ C.capMaxLoad x :=
    hMargin.2.2.2.2.2.2
  exact ⟨hSource, hPositive, hUniform⟩

end

end RouteBP3CentralFDHullC2C3DHEvaluatorConjunct

#print axioms RouteBP3CentralFDHullC2C3DHEvaluatorConjunct.source_function_eq_dh_evaluator_at_covered_point
#print axioms RouteBP3CentralFDHullC2C3DHEvaluatorConjunct.dh_evaluator_at_same_covered_point_has_uniform_margin

import RouteBO1PerBodyExactSource
import BodyTraceEvaluator

set_option autoImplicit false

namespace RouteBO1PerBodyTraceAdapter

noncomputable section

open RouteBO1PerBodyExactSource
open RouteBO1PerBodyTraceGenerated
open RouteBBodySemanticCore
open RouteBBodyContractCore
open RouteBSourceContractAdapter

/-- The generated evaluator at the type expected by the O1 source comparator. -/
def fourierBodyFromTrace : FourierBody :=
  bodyTraceEvaluator

/-- Concrete targets; these are propositions only, not proofs. -/
def h_body_1 : Prop :=
  ∀ q i j, sourceBodyMass q (0 : Body) i j = fourierBodyFromTrace 0 q i j

def h_body_2 : Prop :=
  ∀ q i j, sourceBodyMass q (1 : Body) i j = fourierBodyFromTrace 1 q i j

def h_body_3 : Prop :=
  ∀ q i j, sourceBodyMass q (2 : Body) i j = fourierBodyFromTrace 2 q i j

def h_body_4 : Prop :=
  ∀ q i j, sourceBodyMass q (3 : Body) i j = fourierBodyFromTrace 3 q i j

def h_body_5 : Prop :=
  ∀ q i j, sourceBodyMass q (4 : Body) i j = fourierBodyFromTrace 4 q i j

def h_body_6 : Prop :=
  ∀ q i j, sourceBodyMass q (5 : Body) i j = fourierBodyFromTrace 5 q i j

def h_body_all : Prop :=
  h_body_1 ∧ h_body_2 ∧ h_body_3 ∧ h_body_4 ∧ h_body_5 ∧ h_body_6

/- Body 1 is the smallest source theorem instance.  These are deliberately
   separate targets so a Lean agent can close the source expansion and the
   generated-trace reduction independently, then compose them into h_body_1. -/
def h_body_1_source_entry_target : Prop :=
  ∀ q i j,
    bodyMass (sourceContract q).origins (sourceContract q).axes
        (0 : Body) (routeBMass 0) (routeBInertia 0) i j =
      bodyTraceEvaluator 0 q i j

def h_body_1_expected_entry_target : Prop :=
  ∀ q i j,
    sourceBodyMass q (0 : Body) i j =
      if i = (0 : Joint) ∧ j = (0 : Joint) then
        (628 / 1875 : ℝ)
      else 0

def h_body_1_trace_entry_target : Prop :=
  ∀ q i j,
    (if i = (0 : Joint) ∧ j = (0 : Joint) then
        (628 / 1875 : ℝ)
      else 0) = bodyTraceEvaluator 0 q i j

theorem h_body_1_of_entry_targets
    (h_source : h_body_1_expected_entry_target)
    (h_trace : h_body_1_trace_entry_target) : h_body_1 := by
  intro q i j
  change sourceBodyMass q (0 : Body) i j = bodyTraceEvaluator 0 q i j
  calc
    sourceBodyMass q (0 : Body) i j =
        (if i = (0 : Joint) ∧ j = (0 : Joint) then
          (628 / 1875 : ℝ)
        else 0) := h_source q i j
    _ = bodyTraceEvaluator 0 q i j := h_trace q i j

/- Intended composition, still unproved:
   h_body_1_expected_entry_target ∧ h_body_1_trace_entry_target
   implies h_body_1.  The source proof needs explicit slot-0/slot-1 origin,
   world-z parent-axis, diagonal inertia, and sin_sq_add_cos_sq expansion;
   the trace proof needs a finite-fold reduction of the body-1 tagged slice. -/

/- Compilation status: intentionally uncompiled.  No theorem below asserts any
   h_body_i; each name is a concrete target for the next Lean agent. -/

end
end RouteBO1PerBodyTraceAdapter

import RouteBO1PerBodyExactSource
import BodyTraceEvaluator

set_option autoImplicit false

namespace RouteBO1PerBodyTraceAdapter

noncomputable section

open RouteBO1PerBodyExactSource
open RouteBO1PerBodyTraceGenerated

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

/- Compilation status: intentionally uncompiled.  No theorem below asserts any
   h_body_i; each name is a concrete target for the next Lean agent. -/

end
end RouteBO1PerBodyTraceAdapter

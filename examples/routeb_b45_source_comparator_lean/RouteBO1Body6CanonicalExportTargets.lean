import RouteBO1PerBodyExactSource
import BodyTraceEvaluator

set_option autoImplicit false

namespace RouteBO1Body6CanonicalExportTargets

noncomputable section

open RouteBO1PerBodyExactSource
open RouteBBodySemanticCore
open RouteBSourceContractAdapter
open RouteBO1PerBodyTraceGenerated

/- Body-6-only targets, UNCOMPILED. No source theorem or receipt inhabitant.
   Rows are an explicit parameter until the separately hashed canonical CSV
   is reified. The main adapter and its existing evaluator are not changed. -/
structure CanonicalRow where
  row : Fin 6
  col : Fin 6
  frequency : Fin 6 → ℤ
  realCoeff : ℚ
  imagCoeff : ℚ

def canonicalAtom (r : CanonicalRow) (q : Q6) : ℝ :=
  realFourierAtom r.frequency r.realCoeff r.imagCoeff q

def body6CanonicalEvaluator (rows : List CanonicalRow) (q : Q6)
    (i j : Fin 6) : ℝ :=
  (rows.map (fun r => if r.row = i ∧ r.col = j then canonicalAtom r q else 0)).sum

def body6Center (q : Q6) : Fin 3 → ℝ :=
  fun a => (sourceContract q).origins (5 : Fin 7) a +
    (7 / 200 : ℝ) * (sourceContract q).axes (5 : Fin 6) a

def body6Velocity (q : Q6) (i : Fin 6) : Fin 3 → ℝ :=
  cross3 ((sourceContract q).axes i)
    (fun a => body6Center q a - (sourceContract q).origins (prevOrigin i) a)

def body6Gram (q : Q6) (i j : Fin 6) : ℝ :=
  (3 / 20 : ℝ) * (∑ a : Fin 3, body6Velocity q i a * body6Velocity q j a) +
    (1 / 60 : ℝ) * (∑ a : Fin 3,
      (sourceContract q).axes i a * (sourceContract q).axes j a)

/- G0: sixth DH translation is along the parent z-axis, a6=0, d6=7/100. -/
def Body6EndpointTarget : Prop :=
  ∀ q a, (sourceContract q).origins (6 : Fin 7) a =
    (sourceContract q).origins (5 : Fin 7) a +
      (7 / 100 : ℝ) * (sourceContract q).axes (5 : Fin 6) a

def Body6CenterTarget : Prop :=
  ∀ q, bodyCom (sourceContract q).origins (5 : Fin 6) = body6Center q

/- G1: expand the actual source term with its fixed mass and isotropic inertia. -/
def Body6SourceGramTarget : Prop :=
  ∀ q i j, sourceBodyMass q (5 : Fin 6) i j = body6Gram q i j

/- G2: all 36 entries, including the four zero-complement entries. -/
def Body6GramFourierTarget (rows : List CanonicalRow) : Prop :=
  ∀ q i j, body6Gram q i j = body6CanonicalEvaluator rows q i j

def Body6CanonicalSourceTarget (rows : List CanonicalRow) : Prop :=
  ∀ q i j, sourceBodyMass q (5 : Fin 6) i j = body6CanonicalEvaluator rows q i j

/- G3: this is an additional target, not a consequence of equal CSV hashes.
   Its RHS is the immutable evaluator used by the existing adapter h_body_6. -/
def Body6LegacyTraceTarget (rows : List CanonicalRow) : Prop :=
  ∀ q i j, body6CanonicalEvaluator rows q i j = bodyTraceEvaluator 5 q i j

/- Small structural leaves that do not depend on 610-row expansion. -/
def Body6SixthVelocityTarget : Prop :=
  ∀ q a, body6Velocity q (5 : Fin 6) a = 0

def Body6SixthColumnTarget : Prop :=
  ∀ q i, sourceBodyMass q (5 : Fin 6) i (5 : Fin 6) =
    (1 / 60 : ℝ) * (∑ a : Fin 3,
      (sourceContract q).axes i a * (sourceContract q).axes (5 : Fin 6) a)

def Body6SixthDiagonalTarget : Prop :=
  ∀ q, sourceBodyMass q (5 : Fin 6) (5 : Fin 6) (5 : Fin 6) = (1 / 60 : ℝ)

def Body6LastAngleIndependentTarget : Prop :=
  ∀ (q q' : Q6), (∀ k : Fin 6, k ≠ (5 : Fin 6) → q k = q' k) →
    ∀ i j, sourceBodyMass q (5 : Fin 6) i j = sourceBodyMass q' (5 : Fin 6) i j

end
end RouteBO1Body6CanonicalExportTargets

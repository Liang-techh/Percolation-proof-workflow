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

/- Body 2 source expansion and trace-fold targets.  The index 1 is the second
   body and q 1 is its only nonconstant frequency coordinate in the trace. -/
def h_body_2_source_expanded_target : Prop :=
  ∀ q i j,
    (routeBMass 1) *
        (∑ a : Axis,
          bodyJv (sourceContract q).origins (sourceContract q).axes
            (1 : Body) a i *
          bodyJv (sourceContract q).origins (sourceContract q).axes
            (1 : Body) a j) +
      (∑ a : Axis, ∑ b : Axis,
        bodyJw (sourceContract q).axes (1 : Body) a i *
          routeBInertia 1 a b *
        bodyJw (sourceContract q).axes (1 : Body) b j) =
      if i = (0 : Joint) ∧ j = (0 : Joint) then
        (20953 / 100000 : ℝ) +
            (42 / 3125 : ℝ) * Real.sin (q (1 : Joint)) -
            (441 / 100000 : ℝ) * Real.cos (2 * q (1 : Joint))
      else if i = (1 : Joint) ∧ j = (1 : Joint) then
        (10441 / 50000 : ℝ)
      else 0

def h_body_2_source_entry_target : Prop :=
  ∀ q i j,
    sourceBodyMass q (1 : Body) i j =
      bodyTraceEvaluator 1 q i j

def h_body_2_expected_entry_target : Prop :=
  ∀ q i j,
    sourceBodyMass q (1 : Body) i j =
      if i = (0 : Joint) ∧ j = (0 : Joint) then
        (20953 / 100000 : ℝ) +
            (42 / 3125 : ℝ) * Real.sin (q (1 : Joint)) -
            (441 / 100000 : ℝ) * Real.cos (2 * q (1 : Joint))
      else if i = (1 : Joint) ∧ j = (1 : Joint) then
        (10441 / 50000 : ℝ)
      else 0

def h_body_2_trace_fold_target : Prop :=
  ∀ q i j,
    (if i = (0 : Joint) ∧ j = (0 : Joint) then
        (20953 / 100000 : ℝ) +
            (42 / 3125 : ℝ) * Real.sin (q (1 : Joint)) -
            (441 / 100000 : ℝ) * Real.cos (2 * q (1 : Joint))
      else if i = (1 : Joint) ∧ j = (1 : Joint) then
        (10441 / 50000 : ℝ)
      else 0) = bodyTraceEvaluator 1 q i j

theorem h_body_2_of_entry_targets
    (h_source : h_body_2_expected_entry_target)
    (h_trace : h_body_2_trace_fold_target) : h_body_2 := by
  intro q i j
  change sourceBodyMass q (1 : Body) i j = bodyTraceEvaluator 1 q i j
  calc
    sourceBodyMass q (1 : Body) i j =
        (if i = (0 : Joint) ∧ j = (0 : Joint) then
          (20953 / 100000 : ℝ) +
              (42 / 3125 : ℝ) * Real.sin (q (1 : Joint)) -
              (441 / 100000 : ℝ) * Real.cos (2 * q (1 : Joint))
        else if i = (1 : Joint) ∧ j = (1 : Joint) then
          (10441 / 50000 : ℝ)
        else 0) := h_source q i j
    _ = bodyTraceEvaluator 1 q i j := h_trace q i j

/- Human body 3 is zero-based body 2.  Its trace depends only on the second
   joint coordinate q 1.  Keep source expansion and trace reduction separate. -/
def h_body_3_source_expanded_target : Prop :=
  ∀ q i j,
    (routeBMass 2) *
        (∑ a : Axis,
          bodyJv (sourceContract q).origins (sourceContract q).axes
            (2 : Body) a i *
          bodyJv (sourceContract q).origins (sourceContract q).axes
            (2 : Body) a j) +
      (∑ a : Axis, ∑ b : Axis,
        bodyJw (sourceContract q).axes (2 : Body) a i *
          routeBInertia 2 a b *
        bodyJw (sourceContract q).axes (2 : Body) b j) =
      if i = (0 : Joint) ∧ j = (0 : Joint) then
        (80467 / 600000 : ℝ) +
            (63 / 3125 : ℝ) * Real.sin (q (1 : Joint)) -
            (1323 / 100000 : ℝ) * Real.cos (2 * q (1 : Joint))
      else if i = (0 : Joint) ∧ j = (1 : Joint) then
        (-63 / 20000 : ℝ) * Real.cos (q (1 : Joint))
      else if i = (1 : Joint) ∧ j = (0 : Joint) then
        (-63 / 20000 : ℝ) * Real.cos (q (1 : Joint))
      else if i = (1 : Joint) ∧ j = (1 : Joint) then
        (21469 / 150000 : ℝ)
      else if i = (1 : Joint) ∧ j = (2 : Joint) then
        (7 / 60 : ℝ)
      else if i = (2 : Joint) ∧ j = (1 : Joint) then
        (7 / 60 : ℝ)
      else if i = (2 : Joint) ∧ j = (2 : Joint) then
        (7 / 60 : ℝ)
      else 0

def h_body_3_source_entry_target : Prop :=
  ∀ q i j,
    sourceBodyMass q (2 : Body) i j =
      bodyTraceEvaluator 2 q i j

def h_body_3_expected_entry_target : Prop :=
  ∀ q i j,
    sourceBodyMass q (2 : Body) i j =
      if i = (0 : Joint) ∧ j = (0 : Joint) then
        (80467 / 600000 : ℝ) +
            (63 / 3125 : ℝ) * Real.sin (q (1 : Joint)) -
            (1323 / 100000 : ℝ) * Real.cos (2 * q (1 : Joint))
      else if i = (0 : Joint) ∧ j = (1 : Joint) then
        (-63 / 20000 : ℝ) * Real.cos (q (1 : Joint))
      else if i = (1 : Joint) ∧ j = (0 : Joint) then
        (-63 / 20000 : ℝ) * Real.cos (q (1 : Joint))
      else if i = (1 : Joint) ∧ j = (1 : Joint) then
        (21469 / 150000 : ℝ)
      else if i = (1 : Joint) ∧ j = (2 : Joint) then
        (7 / 60 : ℝ)
      else if i = (2 : Joint) ∧ j = (1 : Joint) then
        (7 / 60 : ℝ)
      else if i = (2 : Joint) ∧ j = (2 : Joint) then
        (7 / 60 : ℝ)
      else 0

def h_body_3_trace_fold_target : Prop :=
  ∀ q i j,
    (if i = (0 : Joint) ∧ j = (0 : Joint) then
        (80467 / 600000 : ℝ) +
            (63 / 3125 : ℝ) * Real.sin (q (1 : Joint)) -
            (1323 / 100000 : ℝ) * Real.cos (2 * q (1 : Joint))
      else if i = (0 : Joint) ∧ j = (1 : Joint) then
        (-63 / 20000 : ℝ) * Real.cos (q (1 : Joint))
      else if i = (1 : Joint) ∧ j = (0 : Joint) then
        (-63 / 20000 : ℝ) * Real.cos (q (1 : Joint))
      else if i = (1 : Joint) ∧ j = (1 : Joint) then
        (21469 / 150000 : ℝ)
      else if i = (1 : Joint) ∧ j = (2 : Joint) then
        (7 / 60 : ℝ)
      else if i = (2 : Joint) ∧ j = (1 : Joint) then
        (7 / 60 : ℝ)
      else if i = (2 : Joint) ∧ j = (2 : Joint) then
        (7 / 60 : ℝ)
      else 0) = bodyTraceEvaluator 2 q i j

theorem h_body_3_of_entry_targets
    (h_source : h_body_3_expected_entry_target)
    (h_trace : h_body_3_trace_fold_target) : h_body_3 := by
  intro q i j
  change sourceBodyMass q (2 : Body) i j = bodyTraceEvaluator 2 q i j
  calc
    sourceBodyMass q (2 : Body) i j =
        (if i = (0 : Joint) ∧ j = (0 : Joint) then
          (80467 / 600000 : ℝ) +
              (63 / 3125 : ℝ) * Real.sin (q (1 : Joint)) -
              (1323 / 100000 : ℝ) * Real.cos (2 * q (1 : Joint))
        else if i = (0 : Joint) ∧ j = (1 : Joint) then
          (-63 / 20000 : ℝ) * Real.cos (q (1 : Joint))
        else if i = (1 : Joint) ∧ j = (0 : Joint) then
          (-63 / 20000 : ℝ) * Real.cos (q (1 : Joint))
        else if i = (1 : Joint) ∧ j = (1 : Joint) then
          (21469 / 150000 : ℝ)
        else if i = (1 : Joint) ∧ j = (2 : Joint) then
          (7 / 60 : ℝ)
        else if i = (2 : Joint) ∧ j = (1 : Joint) then
          (7 / 60 : ℝ)
        else if i = (2 : Joint) ∧ j = (2 : Joint) then
          (7 / 60 : ℝ)
        else 0) := h_source q i j
    _ = bodyTraceEvaluator 2 q i j := h_trace q i j

/- Body-3 source-side decomposition.  These are typed propositions only: they
   expose the exact prefix/axis, active Jacobian, Gram, and trigonometric
   seams needed by a later source proof, but do not assert that any seam is
   already proved. -/
def h_body_3_prefix_slots_target : Prop :=
  ∀ q,
    (sourceContract q).origins (0 : Slot) =
        ![(0 : ℝ), 0, 0] ∧
    (sourceContract q).origins (1 : Slot) =
        ![(2 / 25 : ℝ) * Real.cos (q (0 : Joint)),
          (2 / 25 : ℝ) * Real.sin (q (0 : Joint)), 1 / 10] ∧
    (fun a => (sourceContract q).origins (2 : Slot) a -
        (sourceContract q).origins (1 : Slot) a) =
        ![(21 / 100 : ℝ) * Real.sin (q (1 : Joint)) *
            Real.cos (q (0 : Joint)),
          (21 / 100 : ℝ) * Real.sin (q (1 : Joint)) *
            Real.sin (q (0 : Joint)),
          (21 / 100 : ℝ) * Real.cos (q (1 : Joint))] ∧
    (fun a => (sourceContract q).origins (3 : Slot) a -
        (sourceContract q).origins (2 : Slot) a) =
        ![(-1 / 20 : ℝ) * Real.sin (q (0 : Joint)),
          (1 / 20 : ℝ) * Real.cos (q (0 : Joint)), 0]

def h_body_3_axes_target : Prop :=
  ∀ q,
    (sourceContract q).axes (0 : Joint) =
        ![(0 : ℝ), 0, 1] ∧
    (sourceContract q).axes (1 : Joint) =
        ![-Real.sin (q (0 : Joint)),
          Real.cos (q (0 : Joint)), 0] ∧
    (sourceContract q).axes (2 : Joint) =
        ![-Real.sin (q (0 : Joint)),
          Real.cos (q (0 : Joint)), 0]

def h_body_3_active_jacobian_target : Prop :=
  ∀ q a,
    bodyJv (sourceContract q).origins (sourceContract q).axes
        (2 : Body) a (0 : Joint) =
      cross3 ((sourceContract q).axes (0 : Joint)) (fun b =>
        bodyCom (sourceContract q).origins (2 : Body) b -
          (sourceContract q).origins (prevOrigin (0 : Joint)) b) a ∧
    bodyJv (sourceContract q).origins (sourceContract q).axes
        (2 : Body) a (1 : Joint) =
      cross3 ((sourceContract q).axes (1 : Joint)) (fun b =>
        bodyCom (sourceContract q).origins (2 : Body) b -
          (sourceContract q).origins (prevOrigin (1 : Joint)) b) a ∧
    bodyJv (sourceContract q).origins (sourceContract q).axes
        (2 : Body) a (2 : Joint) =
      cross3 ((sourceContract q).axes (2 : Joint)) (fun b =>
        bodyCom (sourceContract q).origins (2 : Body) b -
          (sourceContract q).origins (prevOrigin (2 : Joint)) b) a ∧
    bodyJv (sourceContract q).origins (sourceContract q).axes
        (2 : Body) a (3 : Joint) = 0 ∧
    bodyJv (sourceContract q).origins (sourceContract q).axes
        (2 : Body) a (4 : Joint) = 0 ∧
    bodyJv (sourceContract q).origins (sourceContract q).axes
        (2 : Body) a (5 : Joint) = 0 ∧
    bodyJw (sourceContract q).axes (2 : Body) a (0 : Joint) =
      (sourceContract q).axes (0 : Joint) a ∧
    bodyJw (sourceContract q).axes (2 : Body) a (1 : Joint) =
      (sourceContract q).axes (1 : Joint) a ∧
    bodyJw (sourceContract q).axes (2 : Body) a (2 : Joint) =
      (sourceContract q).axes (2 : Joint) a ∧
    bodyJw (sourceContract q).axes (2 : Body) a (3 : Joint) = 0 ∧
    bodyJw (sourceContract q).axes (2 : Body) a (4 : Joint) = 0 ∧
    bodyJw (sourceContract q).axes (2 : Body) a (5 : Joint) = 0

def body_3_translational_gram (q : Q6) (i j : Joint) : ℝ :=
  ∑ a : Axis,
    bodyJv (sourceContract q).origins (sourceContract q).axes
      (2 : Body) a i *
    bodyJv (sourceContract q).origins (sourceContract q).axes
      (2 : Body) a j

def body_3_angular_gram (q : Q6) (i j : Joint) : ℝ :=
  ∑ a : Axis, ∑ b : Axis,
    bodyJw (sourceContract q).axes (2 : Body) a i *
      routeBInertia 2 a b *
    bodyJw (sourceContract q).axes (2 : Body) b j

def body_3_unexpanded_gram (q : Q6) (i j : Joint) : ℝ :=
  routeBMass 2 * body_3_translational_gram q i j +
    body_3_angular_gram q i j

def h_body_3_bodyMass_to_unexpanded_gram_target : Prop :=
  ∀ q i j,
    sourceBodyMass q (2 : Body) i j = body_3_unexpanded_gram q i j

def body_3_piecewise (q : Q6) (i j : Joint) : ℝ :=
  if i = (0 : Joint) ∧ j = (0 : Joint) then
    (80467 / 600000 : ℝ) +
        (63 / 3125 : ℝ) * Real.sin (q (1 : Joint)) -
        (1323 / 100000 : ℝ) * Real.cos (2 * q (1 : Joint))
  else if i = (0 : Joint) ∧ j = (1 : Joint) then
    (-63 / 20000 : ℝ) * Real.cos (q (1 : Joint))
  else if i = (1 : Joint) ∧ j = (0 : Joint) then
    (-63 / 20000 : ℝ) * Real.cos (q (1 : Joint))
  else if i = (1 : Joint) ∧ j = (1 : Joint) then
    (21469 / 150000 : ℝ)
  else if i = (1 : Joint) ∧ j = (2 : Joint) then
    (7 / 60 : ℝ)
  else if i = (2 : Joint) ∧ j = (1 : Joint) then
    (7 / 60 : ℝ)
  else if i = (2 : Joint) ∧ j = (2 : Joint) then
    (7 / 60 : ℝ)
  else 0

def h_body_3_unexpanded_gram_to_piecewise_target : Prop :=
  ∀ q i j, body_3_unexpanded_gram q i j = body_3_piecewise q i j

def h_body_3_minimal_trig_target : Prop :=
  ∀ x : ℝ,
    Real.sin x * Real.sin x + Real.cos x * Real.cos x = 1 ∧
    Real.cos (2 * x) = 2 * Real.cos x * Real.cos x - 1

/- Human body 4 is zero-based body 3.  Its exact trace uses q 1 and q 2. -/
def body_4_piecewise (q : Q6) (i j : Joint) : ℝ :=
  if i = (0 : Joint) ∧ j = (0 : Joint) then
    (48511 / 600000 : ℝ) +
        (42 / 3125 : ℝ) * Real.sin (q (1 : Joint)) +
        (19 / 3125 : ℝ) * Real.sin (q (1 : Joint) + q (2 : Joint)) -
        (441 / 50000 : ℝ) * Real.cos (2 * q (1 : Joint)) +
        (399 / 50000 : ℝ) * Real.cos (q (2 : Joint)) -
        (399 / 50000 : ℝ) * Real.cos (2 * q (1 : Joint) + q (2 : Joint)) -
        (361 / 200000 : ℝ) * Real.cos (2 * q (1 : Joint) + 2 * q (2 : Joint))
  else if i = (0 : Joint) ∧ j = (1 : Joint) then
    (-19 / 10000 : ℝ) * Real.cos (q (1 : Joint) + q (2 : Joint)) -
        (21 / 5000 : ℝ) * Real.cos (q (1 : Joint))
  else if i = (1 : Joint) ∧ j = (0 : Joint) then
    (-19 / 10000 : ℝ) * Real.cos (q (1 : Joint) + q (2 : Joint)) -
        (21 / 5000 : ℝ) * Real.cos (q (1 : Joint))
  else if i = (0 : Joint) ∧ j = (2 : Joint) then
    (-19 / 10000 : ℝ) * Real.cos (q (1 : Joint) + q (2 : Joint))
  else if i = (2 : Joint) ∧ j = (0 : Joint) then
    (-19 / 10000 : ℝ) * Real.cos (q (1 : Joint) + q (2 : Joint))
  else if i = (0 : Joint) ∧ j = (3 : Joint) then
    (1 / 15 : ℝ) * Real.cos (q (1 : Joint) + q (2 : Joint))
  else if i = (3 : Joint) ∧ j = (0 : Joint) then
    (1 / 15 : ℝ) * Real.cos (q (1 : Joint) + q (2 : Joint))
  else if i = (1 : Joint) ∧ j = (1 : Joint) then
    (211 / 2400 : ℝ) +
        (399 / 25000 : ℝ) * Real.cos (q (2 : Joint))
  else if i = (1 : Joint) ∧ j = (2 : Joint) then
    (21083 / 300000 : ℝ) +
        (399 / 50000 : ℝ) * Real.cos (q (2 : Joint))
  else if i = (2 : Joint) ∧ j = (1 : Joint) then
    (21083 / 300000 : ℝ) +
        (399 / 50000 : ℝ) * Real.cos (q (2 : Joint))
  else if i = (2 : Joint) ∧ j = (2 : Joint) then
    (21083 / 300000 : ℝ)
  else if i = (3 : Joint) ∧ j = (3 : Joint) then
    (1 / 15 : ℝ)
  else 0

def h_body_4_source_expanded_target : Prop :=
  ∀ q i j,
    (routeBMass 3) *
        (∑ a : Axis,
          bodyJv (sourceContract q).origins (sourceContract q).axes
            (3 : Body) a i *
          bodyJv (sourceContract q).origins (sourceContract q).axes
            (3 : Body) a j) +
      (∑ a : Axis, ∑ b : Axis,
        bodyJw (sourceContract q).axes (3 : Body) a i *
          routeBInertia 3 a b *
        bodyJw (sourceContract q).axes (3 : Body) b j) =
      body_4_piecewise q i j

def h_body_4_source_entry_target : Prop :=
  ∀ q i j,
    sourceBodyMass q (3 : Body) i j =
      bodyTraceEvaluator 3 q i j

def h_body_4_expected_entry_target : Prop :=
  ∀ q i j,
    sourceBodyMass q (3 : Body) i j = body_4_piecewise q i j

def h_body_4_trace_fold_target : Prop :=
  ∀ q i j,
    body_4_piecewise q i j = bodyTraceEvaluator 3 q i j

theorem h_body_4_of_entry_targets
    (h_source : h_body_4_expected_entry_target)
    (h_trace : h_body_4_trace_fold_target) : h_body_4 := by
  intro q i j
  change sourceBodyMass q (3 : Body) i j = bodyTraceEvaluator 3 q i j
  calc
    sourceBodyMass q (3 : Body) i j = body_4_piecewise q i j := h_source q i j
    _ = bodyTraceEvaluator 3 q i j := h_trace q i j

/- Human body 5 is zero-based body 4.  Its exact trace uses q 1, q 2, q 3. -/
def body_5_piecewise (q : Q6) (i j : Joint) : ℝ :=
  if i = (0 : Joint) ∧ j = (0 : Joint) then
    (1441 / 30000 : ℝ) +
        (63 / 6250 : ℝ) * Real.sin (q (1 : Joint)) +
        (57 / 6250 : ℝ) * Real.sin (q (1 : Joint) + q (2 : Joint)) -
        (1323 / 200000 : ℝ) * Real.cos (2 * q (1 : Joint)) +
        (1197 / 100000 : ℝ) * Real.cos (q (2 : Joint)) -
        (1197 / 100000 : ℝ) * Real.cos (2 * q (1 : Joint) + q (2 : Joint)) -
        (1083 / 200000 : ℝ) * Real.cos (2 * q (1 : Joint) + 2 * q (2 : Joint))
  else if i = (0 : Joint) ∧ j = (1 : Joint) then
    (-57 / 20000 : ℝ) * Real.cos (q (1 : Joint) + q (2 : Joint)) -
        (63 / 20000 : ℝ) * Real.cos (q (1 : Joint))
  else if i = (1 : Joint) ∧ j = (0 : Joint) then
    (-57 / 20000 : ℝ) * Real.cos (q (1 : Joint) + q (2 : Joint)) -
        (63 / 20000 : ℝ) * Real.cos (q (1 : Joint))
  else if i = (0 : Joint) ∧ j = (2 : Joint) then
    (-57 / 20000 : ℝ) * Real.cos (q (1 : Joint) + q (2 : Joint))
  else if i = (2 : Joint) ∧ j = (0 : Joint) then
    (-57 / 20000 : ℝ) * Real.cos (q (1 : Joint) + q (2 : Joint))
  else if i = (0 : Joint) ∧ j = (3 : Joint) then
    (1 / 30 : ℝ) * Real.cos (q (1 : Joint) + q (2 : Joint))
  else if i = (3 : Joint) ∧ j = (0 : Joint) then
    (1 / 30 : ℝ) * Real.cos (q (1 : Joint) + q (2 : Joint))
  else if i = (0 : Joint) ∧ j = (4 : Joint) then
    (1 / 60 : ℝ) *
        (Real.cos (q (1 : Joint) + q (2 : Joint) - q (3 : Joint)) -
          Real.cos (q (1 : Joint) + q (2 : Joint) + q (3 : Joint)))
  else if i = (4 : Joint) ∧ j = (0 : Joint) then
    (1 / 60 : ℝ) *
        (Real.cos (q (1 : Joint) + q (2 : Joint) - q (3 : Joint)) -
          Real.cos (q (1 : Joint) + q (2 : Joint) + q (3 : Joint)))
  else if i = (1 : Joint) ∧ j = (1 : Joint) then
    (8609 / 150000 : ℝ) +
        (1197 / 50000 : ℝ) * Real.cos (q (2 : Joint))
  else if i = (1 : Joint) ∧ j = (2 : Joint) then
    (13249 / 300000 : ℝ) +
        (1197 / 100000 : ℝ) * Real.cos (q (2 : Joint))
  else if i = (2 : Joint) ∧ j = (1 : Joint) then
    (13249 / 300000 : ℝ) +
        (1197 / 100000 : ℝ) * Real.cos (q (2 : Joint))
  else if i = (1 : Joint) ∧ j = (4 : Joint) then
    (1 / 30 : ℝ) * Real.cos (q (3 : Joint))
  else if i = (4 : Joint) ∧ j = (1 : Joint) then
    (1 / 30 : ℝ) * Real.cos (q (3 : Joint))
  else if i = (2 : Joint) ∧ j = (2 : Joint) then
    (13249 / 300000 : ℝ)
  else if i = (2 : Joint) ∧ j = (4 : Joint) then
    (1 / 30 : ℝ) * Real.cos (q (3 : Joint))
  else if i = (4 : Joint) ∧ j = (2 : Joint) then
    (1 / 30 : ℝ) * Real.cos (q (3 : Joint))
  else if i = (3 : Joint) ∧ j = (3 : Joint) then
    (1 / 30 : ℝ)
  else if i = (4 : Joint) ∧ j = (4 : Joint) then
    (1 / 30 : ℝ)
  else 0

def h_body_5_source_expanded_target : Prop :=
  ∀ q i j,
    (routeBMass 4) *
        (∑ a : Axis,
          bodyJv (sourceContract q).origins (sourceContract q).axes
            (4 : Body) a i *
          bodyJv (sourceContract q).origins (sourceContract q).axes
            (4 : Body) a j) +
      (∑ a : Axis, ∑ b : Axis,
        bodyJw (sourceContract q).axes (4 : Body) a i *
          routeBInertia 4 a b *
        bodyJw (sourceContract q).axes (4 : Body) b j) =
      body_5_piecewise q i j

def h_body_5_source_entry_target : Prop :=
  ∀ q i j,
    sourceBodyMass q (4 : Body) i j =
      bodyTraceEvaluator 4 q i j

def h_body_5_expected_entry_target : Prop :=
  ∀ q i j,
    sourceBodyMass q (4 : Body) i j = body_5_piecewise q i j

def h_body_5_trace_fold_target : Prop :=
  ∀ q i j,
    body_5_piecewise q i j = bodyTraceEvaluator 4 q i j

theorem h_body_5_of_entry_targets
    (h_source : h_body_5_expected_entry_target)
    (h_trace : h_body_5_trace_fold_target) : h_body_5 := by
  intro q i j
  change sourceBodyMass q (4 : Body) i j = bodyTraceEvaluator 4 q i j
  calc
    sourceBodyMass q (4 : Body) i j = body_5_piecewise q i j := h_source q i j
    _ = bodyTraceEvaluator 4 q i j := h_trace q i j

/- Intended composition, still unproved:
   h_body_1_expected_entry_target ∧ h_body_1_trace_entry_target
   implies h_body_1.  The source proof needs explicit slot-0/slot-1 origin,
   world-z parent-axis, diagonal inertia, and sin_sq_add_cos_sq expansion;
   the trace proof needs a finite-fold reduction of the body-1 tagged slice. -/

/- Compilation status: intentionally uncompiled.  The two *_of_entry_targets
   theorems are only conditional compositions; no source or trace premise is
   asserted here. -/

end
end RouteBO1PerBodyTraceAdapter

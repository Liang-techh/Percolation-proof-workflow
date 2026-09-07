import P8First12Adapter
import Mathlib.Tactic

/-!
# P8 ramp-tube transport and pullback-domain bridge

Formalization follow-up for `T-P8-011` (mathematics by 古月方源).

This file stays source-independent.  It records the exact graph lift from a
12-state explicit-time mechanical tube to the existing 14-state ramp
representation, the corresponding pulled-back 13-state source domain, a
square-only ramp-tail cap, the rational obstruction to reusing the current
`|w| <= 1/100` box through `T = 1`, and the elementary anisotropic Lipschitz
substitution.  It does not prove Julia source semantics, ODE existence,
continuation, interval enclosure, flowpipe coverage, admission, or registry
mutation.
-/

namespace RouteBP8RampTubeTransport

set_option autoImplicit false

open RouteBP8PicardStep RouteBP8ContractAdapter RouteBP8First12Adapter

/-- Projecting an exact ramp lift recovers its twelve mechanical coordinates. -/
theorem proj12_rampLift (m : State12) (c t : ℝ) :
    proj12_14 (rampLift m c t) = m := by
  funext i
  fin_cases i <;> rfl

/-- For fixed time, the exact ramp graph is injective in the mechanical state
    and external ramp coefficient.  The `w = c*t` slot is redundant because the
    final slot stores `c` itself. -/
theorem rampLift_injective_mc
    {m1 m2 : State12} {c1 c2 t : ℝ}
    (h : rampLift m1 c1 t = rampLift m2 c2 t) :
    m1 = m2 ∧ c1 = c2 := by
  constructor
  · have hproj := congrArg proj12_14 h
    simpa only [proj12_rampLift] using hproj
  · have hc := congrFun h cSlot
    simpa only [rampLift_c] using hc

/-- Exact graph lift of an arbitrary mechanical tube `B` and parameter
    admissibility predicate `C`. -/
def RampTube
    (B : ℝ → ℝ → State12 → Prop) (C : ℝ → Prop)
    (t : ℝ) (z : State14) : Prop :=
  ∃ m c, C c ∧ B t c m ∧ z = rampLift m c t

/-- Membership of a state already known to be on the ramp graph reduces exactly
    to the mechanical tube and parameter predicates. -/
theorem rampTube_on_ramp_iff
    (B : ℝ → ℝ → State12 → Prop) (C : ℝ → Prop)
    (t c : ℝ) (m : State12) :
    RampTube B C t (rampLift m c t) ↔ C c ∧ B t c m := by
  constructor
  · rintro ⟨m', c', hc', hB', hEq⟩
    rcases rampLift_injective_mc hEq with ⟨hm, hc⟩
    subst m'
    subst c'
    exact ⟨hc', hB'⟩
  · rintro ⟨hc, hB⟩
    exact ⟨m, c, hc, hB, rfl⟩

/-- Pointwise mechanical coverage lifts to the exact 14-state ramp graph
    without independently enclosing the two tail coordinates. -/
theorem mechanical_coverage_lifts
    (B : ℝ → ℝ → State12 → Prop) (C I : ℝ → Prop)
    (m : ℝ → State12) (c : ℝ)
    (hc : C c)
    (hB : ∀ t, I t → B t c (m t)) :
    ∀ t, I t → RampTube B C t (rampLift (m t) c t) := by
  intro t ht
  exact (rampTube_on_ramp_iff B C t c (m t)).2 ⟨hc, hB t ht⟩

/-- The source domain for the explicit-time field is the exact pullback of the
    13-state source domain along `w = c*t`. -/
def PullbackDomain
    (D13 : State13 → Prop) (c t : ℝ) (m : State12) : Prop :=
  D13 (pack13 m (c * t))

/-- Unfolding the pullback-domain contract is exact and introduces no extra
    Cartesian `w,c` domain obligation. -/
theorem pullbackDomain_iff
    (D13 : State13 → Prop) (c t : ℝ) (m : State12) :
    PullbackDomain D13 c t m ↔ D13 (pack13 m (c * t)) := by
  rfl

/-- Square-only ramp-tail cap.  It avoids square roots and is suitable for a
    rational downstream consumer. -/
theorem ramp_tail_sq_cap
    {c t T W : ℝ}
    (hc : c ^ 2 ≤ 3)
    (ht0 : 0 ≤ t) (htT : t ≤ T) (hT : 0 ≤ T)
    (hcap : 3 * T ^ 2 ≤ W ^ 2) :
    (c * t) ^ 2 ≤ W ^ 2 := by
  have htSq : t ^ 2 ≤ T ^ 2 := by
    calc
      t ^ 2 = t * t := by ring
      _ ≤ t * T := mul_le_mul_of_nonneg_left htT ht0
      _ ≤ T * T := mul_le_mul_of_nonneg_right htT hT
      _ = T ^ 2 := by ring
  have hct : c ^ 2 * t ^ 2 ≤ 3 * t ^ 2 :=
    mul_le_mul_of_nonneg_right hc (sq_nonneg t)
  have htime : 3 * t ^ 2 ≤ 3 * T ^ 2 :=
    mul_le_mul_of_nonneg_left htSq (by norm_num)
  calc
    (c * t) ^ 2 = c ^ 2 * t ^ 2 := by ring
    _ ≤ 3 * t ^ 2 := hct
    _ ≤ 3 * T ^ 2 := htime
    _ ≤ W ^ 2 := hcap

/-- Fully rational witness that the documented local source box
    `|w| <= 1/100` cannot cover the full ramp family through `T = 1`. -/
theorem current_w_box_not_T1 :
    ∃ c t : ℝ,
      c ^ 2 ≤ 3 ∧ 0 ≤ t ∧ t ≤ 1 ∧ |c * t| > (1 : ℝ) / 100 := by
  refine ⟨1, 1, ?_, ?_, ?_, ?_⟩ <;> norm_num

/-- Exact tail-distance identity used when transporting source regularity through
    the substitution `w = c*t`. -/
theorem ramp_tail_distance (c t1 t2 : ℝ) :
    |c * t1 - c * t2| = |c| * |t1 - t2| := by
  rw [← mul_sub, abs_mul]

/-- An anisotropic source Lipschitz premise transports to the explicit-time
    mechanical field by pure substitution.  This theorem does not assert that
    the deployed Float64 source satisfies the premise. -/
theorem explicitMechanical_lipschitz_transport
    (S : VectorField13) (Lm Lw c t1 t2 : ℝ) (m1 m2 : State12)
    (hsrc :
      ∀ (x1 x2 : State12) (w1 w2 : ℝ),
        ‖sourceMechanical S (pack13 x1 w1) -
            sourceMechanical S (pack13 x2 w2)‖ ≤
          Lm * ‖x1 - x2‖ + Lw * |w1 - w2|) :
    ‖explicitMechanical S c t1 m1 - explicitMechanical S c t2 m2‖ ≤
      Lm * ‖m1 - m2‖ + Lw * |c| * |t1 - t2| := by
  have h := hsrc m1 m2 (c * t1) (c * t2)
  rw [ramp_tail_distance] at h
  simpa [explicitMechanical, mul_assoc] using h

#print axioms proj12_rampLift
#print axioms rampLift_injective_mc
#print axioms rampTube_on_ramp_iff
#print axioms mechanical_coverage_lifts
#print axioms pullbackDomain_iff
#print axioms ramp_tail_sq_cap
#print axioms current_w_box_not_T1
#print axioms ramp_tail_distance
#print axioms explicitMechanical_lipschitz_transport

end RouteBP8RampTubeTransport

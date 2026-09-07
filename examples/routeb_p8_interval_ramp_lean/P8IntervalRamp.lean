import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Tactic

/-!
# Route-B P8 interval-local ramp reconstruction

This sidecar refines the already compiled all-real ramp reconstruction theorem.
It only assumes continuity on `[0,1]` and right-derivative witnesses on `[0,1)`.
That is enough for the endpoint transfer `w(1)=c0` and avoids assuming any
behavior outside the proof horizon.

It does not prove source binding, ODE existence/uniqueness, flowpipe coverage,
first-exit closure, or Route-B admission.
-/

namespace RouteBP8IntervalRamp

set_option autoImplicit false

/-- A scalar tail coefficient with zero right derivative on `[0,1)` is constant
on `[0,1]`, including the endpoint. -/
theorem ramp_c_constant_on_Icc
    (c : ℝ → ℝ) (c0 : ℝ)
    (hc0 : c 0 = c0)
    (hcont : ContinuousOn c (Set.Icc (0 : ℝ) 1))
    (hc : ∀ t ∈ Set.Ico (0 : ℝ) 1,
      HasDerivWithinAt c 0 (Set.Ici t) t) :
    ∀ t ∈ Set.Icc (0 : ℝ) 1, c t = c0 := by
  intro t ht
  calc
    c t = c 0 := constant_of_has_deriv_right_zero hcont hc t ht
    _ = c0 := hc0

/-- On `[0,1]`, if `w' = c`, `c = c0`, and `w(0)=0`, then `w(t)=c0*t`.
Only right derivatives on `[0,1)` and endpoint continuity are required. -/
theorem ramp_w_eq_mul_on_Icc
    (w c : ℝ → ℝ) (c0 : ℝ)
    (hw0 : w 0 = 0)
    (hcconst : ∀ t ∈ Set.Icc (0 : ℝ) 1, c t = c0)
    (hwcont : ContinuousOn w (Set.Icc (0 : ℝ) 1))
    (hw : ∀ t ∈ Set.Ico (0 : ℝ) 1,
      HasDerivWithinAt w (c t) (Set.Ici t) t) :
    ∀ t ∈ Set.Icc (0 : ℝ) 1, w t = c0 * t := by
  let lin : ℝ → ℝ := fun s => c0 * s
  have hlincont : ContinuousOn lin (Set.Icc (0 : ℝ) 1) := by
    fun_prop
  have hw' : ∀ t ∈ Set.Ico (0 : ℝ) 1,
      HasDerivWithinAt w c0 (Set.Ici t) t := by
    intro t ht
    have htIcc : t ∈ Set.Icc (0 : ℝ) 1 := ⟨ht.1, le_of_lt ht.2⟩
    simpa [hcconst t htIcc] using hw t ht
  have hlin : ∀ t ∈ Set.Ico (0 : ℝ) 1,
      HasDerivWithinAt lin c0 (Set.Ici t) t := by
    intro t _
    simpa [lin] using ((hasDerivAt_id t).const_mul c0).hasDerivWithinAt
  have hinit : w 0 = lin 0 := by
    simp [lin, hw0]
  intro t ht
  have hEq : w t = lin t :=
    eq_of_has_deriv_right_eq hw' hlin hwcont hlincont hinit t ht
  simpa [lin] using hEq

/-- Combined interval-local scalar ramp reconstruction. -/
theorem ramp_reconstruction_on_Icc
    (w c : ℝ → ℝ) (c0 : ℝ)
    (hw0 : w 0 = 0)
    (hc0 : c 0 = c0)
    (hccont : ContinuousOn c (Set.Icc (0 : ℝ) 1))
    (hwcont : ContinuousOn w (Set.Icc (0 : ℝ) 1))
    (hc : ∀ t ∈ Set.Ico (0 : ℝ) 1,
      HasDerivWithinAt c 0 (Set.Ici t) t)
    (hw : ∀ t ∈ Set.Ico (0 : ℝ) 1,
      HasDerivWithinAt w (c t) (Set.Ici t) t) :
    ∀ t ∈ Set.Icc (0 : ℝ) 1, c t = c0 ∧ w t = c0 * t := by
  have hcconst := ramp_c_constant_on_Icc c c0 hc0 hccont hc
  have hwform := ramp_w_eq_mul_on_Icc w c c0 hw0 hcconst hwcont hw
  intro t ht
  exact ⟨hcconst t ht, hwform t ht⟩

/-- Minimal typed state matching the existing P8 14-state ramp adapter. -/
abbrev State14 := Fin 14 → ℝ

def wSlot : Fin 14 := ⟨12, by omega⟩
def cSlot : Fin 14 := ⟨13, by omega⟩

/-- Typed interval-local tail reconstruction for a 14-state trajectory. -/
theorem state_tail_reconstruction_on_Icc
    (z : ℝ → State14) (c0 : ℝ)
    (hw0 : z 0 wSlot = 0)
    (hc0 : z 0 cSlot = c0)
    (hccont : ContinuousOn (fun t => z t cSlot) (Set.Icc (0 : ℝ) 1))
    (hwcont : ContinuousOn (fun t => z t wSlot) (Set.Icc (0 : ℝ) 1))
    (hc : ∀ t ∈ Set.Ico (0 : ℝ) 1,
      HasDerivWithinAt (fun s => z s cSlot) 0 (Set.Ici t) t)
    (hw : ∀ t ∈ Set.Ico (0 : ℝ) 1,
      HasDerivWithinAt (fun s => z s wSlot) (z t cSlot) (Set.Ici t) t) :
    ∀ t ∈ Set.Icc (0 : ℝ) 1,
      z t cSlot = c0 ∧ z t wSlot = c0 * t := by
  exact ramp_reconstruction_on_Icc
    (fun s => z s wSlot) (fun s => z s cSlot) c0
    hw0 hc0 hccont hwcont hc hw

/-- Endpoint transfer at the proof horizon using only interval-local calculus. -/
theorem state_terminal_one_interval
    (z : ℝ → State14) (c0 : ℝ)
    (hw0 : z 0 wSlot = 0)
    (hc0 : z 0 cSlot = c0)
    (hccont : ContinuousOn (fun t => z t cSlot) (Set.Icc (0 : ℝ) 1))
    (hwcont : ContinuousOn (fun t => z t wSlot) (Set.Icc (0 : ℝ) 1))
    (hc : ∀ t ∈ Set.Ico (0 : ℝ) 1,
      HasDerivWithinAt (fun s => z s cSlot) 0 (Set.Ici t) t)
    (hw : ∀ t ∈ Set.Ico (0 : ℝ) 1,
      HasDerivWithinAt (fun s => z s wSlot) (z t cSlot) (Set.Ici t) t) :
    z 1 wSlot = c0 := by
  have h := (state_tail_reconstruction_on_Icc
    z c0 hw0 hc0 hccont hwcont hc hw 1 (by norm_num)).2
  simpa using h

#print axioms ramp_c_constant_on_Icc
#print axioms ramp_w_eq_mul_on_Icc
#print axioms ramp_reconstruction_on_Icc
#print axioms state_tail_reconstruction_on_Icc
#print axioms state_terminal_one_interval

end RouteBP8IntervalRamp

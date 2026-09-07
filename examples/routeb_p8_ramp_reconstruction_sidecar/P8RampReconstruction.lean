import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Tactic

/-!
# P8 ramp-tail reconstruction sidecar

This file formalizes the calculus core from `T-P8-006` under a deliberately
strong first implementation hypothesis: the scalar coordinate functions are
differentiable on all of `ℝ` via `HasDerivAt` assumptions at every time.

It proves:

* `c' = 0` and `c(0)=c0` imply `c(t)=c0`;
* `w' = c`, `w(0)=0`, and the previous constancy imply `w(t)=c0*t`;
* the same facts for typed `Fin 14 → ℝ` trajectories;
* the terminal identity `w(1)=c0`.

This does not prove source binding, ODE existence, interval enclosure,
flowpipe coverage, or Route-B admission.  The weaker interval-local endpoint
hypotheses requested by the mathematical review remain a later refinement.
-/

namespace RouteBP8RampReconstruction

set_option autoImplicit false

/-- A scalar function with zero derivative everywhere is fixed by its value at zero. -/
theorem ramp_c_constant
    (c : ℝ → ℝ) (c0 : ℝ)
    (hc0 : c 0 = c0)
    (hc : ∀ t : ℝ, HasDerivAt c 0 t) :
    ∀ t : ℝ, c t = c0 := by
  have hdiff : Differentiable ℝ c := fun t => (hc t).differentiableAt
  have hzero : ∀ t : ℝ, deriv c t = 0 := fun t => (hc t).deriv
  intro t
  calc
    c t = c 0 := is_const_of_deriv_eq_zero hdiff hzero t 0
    _ = c0 := hc0

/-- If `w' = c`, the tail coefficient is constant, and `w(0)=0`, then `w(t)=c0*t`. -/
theorem ramp_w_eq_mul
    (w c : ℝ → ℝ) (c0 : ℝ)
    (hw0 : w 0 = 0)
    (hc : ∀ t : ℝ, c t = c0)
    (hw : ∀ t : ℝ, HasDerivAt w (c t) t) :
    ∀ t : ℝ, w t = c0 * t := by
  let lin : ℝ → ℝ := fun s => c0 * s
  let h : ℝ → ℝ := w - lin
  have hh : ∀ t : ℝ, HasDerivAt h 0 t := by
    intro t
    have hw' : HasDerivAt w c0 t := by
      simpa [hc t] using hw t
    have hlin : HasDerivAt lin c0 t := by
      simpa [lin] using (hasDerivAt_id t).const_mul c0
    have hsub := hw'.sub hlin
    simpa [h] using hsub
  have hdiff : Differentiable ℝ h := fun t => (hh t).differentiableAt
  have hzero : ∀ t : ℝ, deriv h t = 0 := fun t => (hh t).deriv
  intro t
  have hconst : h t = h 0 := is_const_of_deriv_eq_zero hdiff hzero t 0
  simp only [h, lin, Pi.sub_apply, hw0, mul_zero, sub_zero] at hconst
  exact hconst

/-- Combined scalar ramp reconstruction. -/
theorem ramp_reconstruction
    (w c : ℝ → ℝ) (c0 : ℝ)
    (hw0 : w 0 = 0)
    (hc0 : c 0 = c0)
    (hc : ∀ t : ℝ, HasDerivAt c 0 t)
    (hw : ∀ t : ℝ, HasDerivAt w (c t) t) :
    ∀ t : ℝ, c t = c0 ∧ w t = c0 * t := by
  have hcconst : ∀ t : ℝ, c t = c0 := ramp_c_constant c c0 hc0 hc
  have hwform : ∀ t : ℝ, w t = c0 * t := ramp_w_eq_mul w c c0 hw0 hcconst hw
  intro t
  exact ⟨hcconst t, hwform t⟩

/-- Minimal typed state matching the P8 coordinate count. -/
abbrev State14 := Fin 14 → ℝ

def wSlot : Fin 14 := ⟨12, by omega⟩

def cSlot : Fin 14 := ⟨13, by omega⟩

/-- Typed tail reconstruction for a 14-state trajectory. -/
theorem state_tail_reconstruction
    (z : ℝ → State14) (c0 : ℝ)
    (hw0 : z 0 wSlot = 0)
    (hc0 : z 0 cSlot = c0)
    (hc : ∀ t : ℝ, HasDerivAt (fun s => z s cSlot) 0 t)
    (hw : ∀ t : ℝ, HasDerivAt (fun s => z s wSlot) (z t cSlot) t) :
    ∀ t : ℝ, z t cSlot = c0 ∧ z t wSlot = c0 * t := by
  exact ramp_reconstruction
    (fun s => z s wSlot) (fun s => z s cSlot) c0 hw0 hc0 hc hw

/-- At horizon `T=1`, the ramp coordinate equals the initial constant coefficient. -/
theorem state_terminal_one
    (z : ℝ → State14) (c0 : ℝ)
    (hw0 : z 0 wSlot = 0)
    (hc0 : z 0 cSlot = c0)
    (hc : ∀ t : ℝ, HasDerivAt (fun s => z s cSlot) 0 t)
    (hw : ∀ t : ℝ, HasDerivAt (fun s => z s wSlot) (z t cSlot) t) :
    z 1 wSlot = c0 := by
  have h := (state_tail_reconstruction z c0 hw0 hc0 hc hw 1).2
  simpa using h

#print axioms ramp_c_constant
#print axioms ramp_w_eq_mul
#print axioms ramp_reconstruction
#print axioms state_tail_reconstruction
#print axioms state_terminal_one

end RouteBP8RampReconstruction

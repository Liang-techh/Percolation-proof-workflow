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
  linarith

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

/-! ### Interval-local endpoint seam

The global `HasDerivAt` hypotheses above are convenient for the abstract
candidate, but they are stronger than the deployed P8 obligation.  The next
lemmas expose the exact interval-local seam needed by the eventual source
binding: continuity on a closed interval, derivative data on its interior,
and integrability of the derivative.  They deliberately leave the interval
integral identity as an explicit premise, so this child does not smuggle in
ODE existence, coverage, or a source-specific regularity theorem.
-/

/-- A zero derivative on an interval transfers the endpoint value. -/
theorem endpoint_eq_of_zero_derivative_on_interval
    (f : ℝ → ℝ) (a b : ℝ)
    (hab : a ≤ b)
    (hcont : ContinuousOn f (Set.Icc a b))
    (hderiv : ∀ t ∈ Set.Ioo a b, HasDerivAt f 0 t)
    (hzero : IntervalIntegrable (fun _ : ℝ => (0 : ℝ)) volume a b) :
    f b = f a := by
  have hfund := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le
    hab hcont hderiv hzero
  have hzero_int : (∫ t in a..b, (0 : ℝ)) = 0 := by
    simp
  rw [hzero_int] at hfund
  linarith

/--
Interval-local ramp transfer.  The two integral identities are the explicit
frontier assumptions to be discharged by the deployed P8 source/flowpipe
agent; no global differentiability is inferred from them.
-/
theorem ramp_endpoint_on_interval
    (w c : ℝ → ℝ) (c0 a b : ℝ)
    (hab : a ≤ b)
    (hc_a : c a = c0)
    (hc_cont : ContinuousOn c (Set.Icc a b))
    (hc_deriv : ∀ t ∈ Set.Ioo a b, HasDerivAt c 0 t)
    (hzero : IntervalIntegrable (fun _ : ℝ => (0 : ℝ)) volume a b)
    (hw_cont : ContinuousOn w (Set.Icc a b))
    (hw_deriv : ∀ t ∈ Set.Ioo a b, HasDerivAt w (c t) t)
    (hc_int : IntervalIntegrable c volume a b)
    (hc_integral : (∫ t in a..b, c t) = c0 * (b - a)) :
    c b = c0 ∧ w b = w a + c0 * (b - a) := by
  have hc_b := endpoint_eq_of_zero_derivative_on_interval c a b hab
    hc_cont hc_deriv hzero
  have hw_fund := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le
    hab hw_cont hw_deriv hc_int
  rw [hc_integral] at hw_fund
  constructor
  · calc
      c b = c a := hc_b
      _ = c0 := hc_a
  · linarith

#print axioms ramp_c_constant
#print axioms ramp_w_eq_mul
#print axioms ramp_reconstruction
#print axioms state_tail_reconstruction
#print axioms state_terminal_one
#print axioms endpoint_eq_of_zero_derivative_on_interval
#print axioms ramp_endpoint_on_interval

end RouteBP8RampReconstruction

import Mathlib

/-!
  Route-B P8: exact reconstruction of the auxiliary ramp tail.

  This child uses an all-real `HasDerivAt` interface.  It proves only the
  calculus identity for the tail; ODE existence, source semantics, interval
  coverage, and flowpipe admission remain separate obligations.
-/

set_option autoImplicit false

namespace RouteBP8RampReconstruction

theorem constant_of_zero_derivative
    {c : ℝ → ℝ} {c0 : ℝ}
    (hc0 : c 0 = c0)
    (hc : ∀ t, HasDerivAt c 0 t) :
    ∀ t, c t = c0 := by
  have hdiff : Differentiable ℝ c := fun t => (hc t).differentiableAt
  have hderiv : ∀ t, deriv c t = 0 := by
    intro t
    rw [(hc t).deriv]
  intro t
  have hconst : c t = c 0 :=
    is_const_of_deriv_eq_zero hdiff hderiv t 0
  simpa [hc0] using hconst

theorem ramp_reconstruction
    {w c : ℝ → ℝ} {c0 : ℝ}
    (hw0 : w 0 = 0)
    (hc0 : c 0 = c0)
    (hc : ∀ t, HasDerivAt c 0 t)
    (hw : ∀ t, HasDerivAt w (c t) t) :
    ∀ t, c t = c0 ∧ w t = c0 * t := by
  have hcconst : ∀ t, c t = c0 :=
    constant_of_zero_derivative hc0 hc
  let h : ℝ → ℝ := fun s => w s - c0 * s
  have hdiff : Differentiable ℝ h := by
    dsimp [h]
    exact (fun t => (hw t).differentiableAt).sub
      (differentiable_id.const_mul c0)
  have hderiv : ∀ t, deriv h t = 0 := by
    intro t
    have h_at : HasDerivAt h (c t - c0) t := by
      dsimp [h]
      simpa using (hw t).sub ((hasDerivAt_id t).const_mul c0)
    rw [h_at.deriv]
    rw [hcconst t]
    ring
  have hconst : ∀ t, h t = h 0 := by
    intro t
    exact is_const_of_deriv_eq_zero hdiff hderiv t 0
  intro t
  constructor
  · exact hcconst t
  · have ht := hconst t
    dsimp [h] at ht
    rw [hw0] at ht
    simpa using ht

theorem terminal_transfer_one
    {w c : ℝ → ℝ} {c0 : ℝ}
    (hw0 : w 0 = 0)
    (hc0 : c 0 = c0)
    (hc : ∀ t, HasDerivAt c 0 t)
    (hw : ∀ t, HasDerivAt w (c t) t) :
    w 1 = c0 := by
  have h := ramp_reconstruction hw0 hc0 hc hw 1
  simpa using h.2

#print axioms constant_of_zero_derivative
#print axioms ramp_reconstruction
#print axioms terminal_transfer_one

end RouteBP8RampReconstruction

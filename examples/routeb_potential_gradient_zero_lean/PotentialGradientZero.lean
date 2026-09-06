import PotentialSlice

set_option autoImplicit false

namespace RouteBPotentialGradientZero

noncomputable section

open RouteBPotentialSlice

def potentialGradient (q : Fin 6 → ℝ) (j : Fin 6) : ℝ :=
  ∑ row : Fin 17,
    -(coefficient (rows row)) * ((rows row).frequency j : ℝ) *
      Real.sin (phase (rows row) q)

def zeroConfiguration : Fin 6 → ℝ := ![0, 0, 0, 0, 0, 0]

theorem phase_zero (row : Fin 17) : phase (rows row) zeroConfiguration = 0 := by
  simp [phase, zeroConfiguration]

theorem potentialGradient_zero (j : Fin 6) :
    potentialGradient zeroConfiguration j = 0 := by
  unfold potentialGradient
  apply Finset.sum_eq_zero
  intro row hrow
  rw [phase_zero]
  simp

theorem potentialGradient_zero_all :
    ∀ j : Fin 6, potentialGradient zeroConfiguration j = 0 := by
  intro j
  exact potentialGradient_zero j

/- The exact Fourier payload therefore has no linear term at the origin.  This
   remains a payload theorem until the deployed Julia potential is functionally
   identified with `RouteBPotentialSlice.potential`. -/
theorem origin_gradient_payload_zero :
    (fun j => potentialGradient zeroConfiguration j) = fun _ => 0 := by
  funext j
  exact potentialGradient_zero j

#print axioms phase_zero
#print axioms potentialGradient_zero
#print axioms potentialGradient_zero_all
#print axioms origin_gradient_payload_zero

end
end RouteBPotentialGradientZero

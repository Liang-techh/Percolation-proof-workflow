import Mathlib

set_option autoImplicit false

namespace RouteBFourierGradient

noncomputable section

abbrev Vec (n : ℕ) := Fin n → ℝ

def phase {r n : ℕ} (frequency : Fin r → Fin n → ℤ)
    (row : Fin r) (q : Vec n) : ℝ :=
  ∑ k : Fin n, (frequency row k : ℝ) * q k

def lineValue {n : ℕ} (q : Vec n) (j : Fin n) (t : ℝ) (k : Fin n) : ℝ :=
  Function.update q j t k

def phaseLine {r n : ℕ} (frequency : Fin r → Fin n → ℤ)
    (row : Fin r) (q : Vec n) (j : Fin n) (t : ℝ) : ℝ :=
  ∑ k : Fin n, (frequency row k : ℝ) * lineValue q j t k

def fourierPotential {r n : ℕ} (coefficient : Fin r → ℝ)
    (frequency : Fin r → Fin n → ℤ) (q : Vec n) : ℝ :=
  ∑ row : Fin r, coefficient row * Real.cos (phase frequency row q)

def fourierGradient {r n : ℕ} (coefficient : Fin r → ℝ)
    (frequency : Fin r → Fin n → ℤ) (q : Vec n) : Vec n :=
  fun j => ∑ row : Fin r,
    -(coefficient row) * (frequency row j : ℝ) *
      Real.sin (phase frequency row q)

theorem phaseLine_at
    {r n : ℕ} (frequency : Fin r → Fin n → ℤ)
    (row : Fin r) (q : Vec n) (j : Fin n) :
    phaseLine frequency row q j (q j) = phase frequency row q := by
  simp [phaseLine, phase, lineValue]

theorem hasDerivAt_phaseLine
    {r n : ℕ} (frequency : Fin r → Fin n → ℤ)
    (row : Fin r) (q : Vec n) (j : Fin n) :
    HasDerivAt (phaseLine frequency row q j)
      (frequency row j : ℝ) (q j) := by
  have h :
      HasDerivAt
        (fun t => ∑ k : Fin n,
          (frequency row k : ℝ) * lineValue q j t k)
        (∑ k : Fin n, if k = j then (frequency row j : ℝ) else 0)
        (q j) := by
    apply HasDerivAt.fun_sum (u := Finset.univ)
    intro k hk
    by_cases hkj : k = j
    · subst k
      simpa [lineValue] using
        (hasDerivAt_id (q j)).const_mul (frequency row j : ℝ)
    · have hc := hasDerivAt_const (q j)
        ((frequency row k : ℝ) * q k)
      convert hc using 1 <;> simp [lineValue, hkj]
  simpa [phaseLine, Finset.sum_ite_irrel] using h

theorem hasDerivAt_fourier_row
    {r n : ℕ} (coefficient : Fin r → ℝ)
    (frequency : Fin r → Fin n → ℤ)
    (row : Fin r) (q : Vec n) (j : Fin n) :
    HasDerivAt
      (fun t => coefficient row *
        Real.cos (phaseLine frequency row q j t))
      (-(coefficient row) * (frequency row j : ℝ) *
        Real.sin (phase frequency row q)) (q j) := by
  have hphase := hasDerivAt_phaseLine frequency row q j
  have hrow := hphase.cos
  have hconst := hrow.const_mul (coefficient row)
  rw [phaseLine_at] at hconst
  convert hconst using 1 <;> ring

theorem hasDerivAt_fourierPotential_coordinate
    {r n : ℕ} (coefficient : Fin r → ℝ)
    (frequency : Fin r → Fin n → ℤ)
    (q : Vec n) (j : Fin n) :
    HasDerivAt
      (fun t => fourierPotential coefficient frequency
        (Function.update q j t))
      (fourierGradient coefficient frequency q j) (q j) := by
  change HasDerivAt
    (fun t => ∑ row : Fin r, coefficient row *
      Real.cos (phaseLine frequency row q j t))
    (fourierGradient coefficient frequency q j) (q j)
  have h := HasDerivAt.fun_sum (u := Finset.univ) (fun row _ =>
    hasDerivAt_fourier_row coefficient frequency row q j)
  simpa [fourierGradient] using h

/-- The source adapter needed by B45-2: if a deployed potential is equal to
    this finite Fourier evaluator as a function, its coordinate derivative is
    the exact Fourier gradient above.  The theorem intentionally says nothing
    about finite-difference approximations or Float64 rounding. -/
theorem deployed_gradient_of_functional_identity
    {r n : ℕ} (deployedPotential : Vec n → ℝ)
    (coefficient : Fin r → ℝ)
    (frequency : Fin r → Fin n → ℤ)
    (q : Vec n) (j : Fin n)
    (hidentity : ∀ x, deployedPotential x =
      fourierPotential coefficient frequency x)
    (hderiv : HasDerivAt (fun t => deployedPotential
      (Function.update q j t)) (0 : ℝ) (q j)) :
    (fourierGradient coefficient frequency q j) = 0 := by
  have h := hasDerivAt_fourierPotential_coordinate coefficient frequency q j
  have hzero := hderiv
  have heq : (fun t => deployedPotential (Function.update q j t)) =
      (fun t => fourierPotential coefficient frequency
        (Function.update q j t)) := by
    funext t
    exact hidentity _
  rw [heq] at hzero
  exact (hzero.unique h).symm

end
end RouteBFourierGradient

#print axioms RouteBFourierGradient.phaseLine_at
#print axioms RouteBFourierGradient.hasDerivAt_phaseLine
#print axioms RouteBFourierGradient.hasDerivAt_fourier_row
#print axioms RouteBFourierGradient.hasDerivAt_fourierPotential_coordinate
#print axioms RouteBFourierGradient.deployed_gradient_of_functional_identity

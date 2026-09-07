import LocalEnergyBudget

set_option autoImplicit false

namespace RouteBBlockLocalComparison

noncomputable section

open RouteBLocalEnergyBudget

/-!
Minimal local storage-comparison leaf for block `(4,5)`.

The comparison is a pure algebraic consequence of the already compiled
reference storage `VB` and carries no dynamics or domain premise.  The
separate `blockEquation` interface keeps the actual block equations and the
total residual components explicit when a downstream derivative theorem uses
them.  No residual bound or physical DH identification is asserted here.
-/

abbrev p45 (q4 q5 v4 v5 : ℝ) : ℝ :=
  RouteBLocalEnergyBudget.p q4 q5 v4 v5

abbrev VB45 (q4 q5 v4 v5 : ℝ) : ℝ :=
  RouteBLocalEnergyBudget.VB q4 q5 v4 v5

def Lambda : ℝ := 6400000 / 200739

/-- The exact comparison constant inherited from `RouteBLocalEnergyBudget.p_le_VB`. -/
theorem p45_le_Lambda_mul_VB (q4 q5 v4 v5 : ℝ) :
    p45 q4 q5 v4 v5 ≤ Lambda * VB45 q4 q5 v4 v5 := by
  simpa [p45, VB45, Lambda] using
    (RouteBLocalEnergyBudget.p_le_VB q4 q5 v4 v5)

/-- A downstream certificate may use any larger comparison constant. -/
theorem p45_le_mul_VB_of_Lambda_ge
    (q4 q5 v4 v5 Lambda' : ℝ)
    (hLambda : Lambda ≤ Lambda') :
    p45 q4 q5 v4 v5 ≤ Lambda' * VB45 q4 q5 v4 v5 := by
  have hcore := p45_le_Lambda_mul_VB q4 q5 v4 v5
  have hVB : 0 ≤ VB45 q4 q5 v4 v5 :=
    RouteBLocalEnergyBudget.VB_nonneg q4 q5 v4 v5
  have hscale :
      Lambda * VB45 q4 q5 v4 v5 ≤ Lambda' * VB45 q4 q5 v4 v5 :=
    mul_le_mul_of_nonneg_right hLambda hVB
  exact hcore.trans hscale

/-!
This is the nominal block equation with an explicit total force residual.
The residuals `e4` and `e5` are unconstrained real variables here.  In
particular, this definition does not claim that they are small, bounded, or
equal to any Float64/finite-difference implementation residual.
-/
def blockEquation
    (q4 q5 v4 v5 a4 a5 w e4 e5 : ℝ) : Prop :=
  (m44 * a4 = -(3 / 5) * q4 - (4 / 5) * v4 + (1 / 5) * w + e4) ∧
  (m55 * a5 = -(1 / 2) * q5 - (13 / 20) * v5 + (1 / 10) * w + e5)

/--
Downstream adapter: explicit block dynamics plus an explicit derivative value
give the algebraic derivative budget, while the storage comparison remains the
independent pure-algebra leaf above.
-/
theorem derivative_budget_and_storage_comparison
    (q4 q5 v4 v5 a4 a5 w e4 e5 dVB : ℝ)
    (hd : dVB = derivativeExpr q4 q5 v4 v5 a4 a5)
    (hblock : blockEquation q4 q5 v4 v5 a4 a5 w e4 e5) :
    dVB ≤ (17 / 520) * w^2 + e4^2 / (8 / 5) + e5^2 / (13 / 10) ∧
      p45 q4 q5 v4 v5 ≤ Lambda * VB45 q4 q5 v4 v5 := by
  rcases hblock with ⟨h4, h5⟩
  constructor
  · exact derivative_budget q4 q5 v4 v5 a4 a5 w e4 e5 dVB hd h4 h5
  · exact p45_le_Lambda_mul_VB q4 q5 v4 v5

#print axioms p45_le_Lambda_mul_VB
#print axioms p45_le_mul_VB_of_Lambda_ge
#print axioms derivative_budget_and_storage_comparison

end
end RouteBBlockLocalComparison

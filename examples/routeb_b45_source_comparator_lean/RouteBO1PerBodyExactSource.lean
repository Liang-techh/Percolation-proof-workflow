import SourceBodyMassExtensionalProbe
import SourceContractIndexAdapter
import Mathlib

set_option autoImplicit false

namespace RouteBO1PerBodyExactSource

noncomputable section

open RouteBB45SourceComparator
open RouteBBodySemanticCore
open RouteBBodyContractCore
open RouteBSourceContractAdapter

abbrev Body := Fin 6
abbrev Joint := Fin 6
abbrev Axis := Fin 3
abbrev Q6 := Joint → ℝ
abbrev Mat6 := Matrix Joint Joint ℝ
abbrev FourierBody := Body → Q6 → Joint → Joint → ℝ

/- Exact source constants copied into the source-side definition.  The
   inertia matrix is diagonal; its diagonal entries are the already divided
   I_val/3 coefficients used by the deployed body Gram formula. -/
def routeBMass : Body → ℝ :=
  ![1, 4 / 5, 3 / 5, 2 / 5, 3 / 10, 3 / 20]

def routeBInertiaScalar : Body → ℝ :=
  ![1 / 3, 1 / 5, 7 / 60, 1 / 15, 1 / 30, 1 / 60]

def routeBInertia (body : Body) : IMat :=
  fun a b => if a = b then routeBInertiaScalar body else 0

/- This is the concrete exact-real source body evaluator.  It is a genuine
   bodyMass expansion through the existing sourceContract, not an abstract
   Fourier placeholder. -/
def sourceBodyMass (q : Q6) (body : Body) : Mat6 :=
  contractMass (sourceContract q) body (routeBMass body) (routeBInertia body)

theorem sourceBodyMass_eq_bodyMass (q : Q6) (body : Body) :
    sourceBodyMass q body =
      bodyMass (sourceContract q).origins (sourceContract q).axes body
        (routeBMass body) (routeBInertia body) := by
  rfl

theorem sourceBodyMass_eq_juliaExactBodyMass (q : Q6) (body : Body) :
    sourceBodyMass q body =
      contractMass (juliaExactContract q) body (routeBMass body)
        (routeBInertia body) := by
  symm
  exact source_body_mass_extensional_bridge q body (routeBMass body)
    (routeBInertia body)

theorem six_per_body_source_expansion (q : Q6) :
    ∀ body : Body,
      sourceBodyMass q body =
        bodyMass (sourceContract q).origins (sourceContract q).axes body
          (routeBMass body) (routeBInertia body) := by
  intro body
  exact sourceBodyMass_eq_bodyMass q body

/- The only missing per-body source comparator object is a body-labelled
   Fourier evaluator with the equality below. -/
def h_body_target (fourierBody : FourierBody) : Prop :=
  ∀ body q i j, sourceBodyMass q body i j = fourierBody body q i j

structure TypedFourierBodyExport where
  fourierBody : FourierBody
  h_body : h_body_target fourierBody

/- Minimal real function-lift seam for a Gaussian-rational Fourier atom. -/
def phase (nu : Joint → ℤ) (q : Q6) : ℝ :=
  ∑ k : Joint, (nu k : ℝ) * q k

def realFourierAtom (nu : Joint → ℤ) (a b : ℚ) (q : Q6) : ℝ :=
  (a : ℝ) * Real.cos (phase nu q) -
    (b : ℝ) * Real.sin (phase nu q)

theorem realFourierAtom_add
    (nu : Joint → ℤ) (a₁ b₁ a₂ b₂ : ℚ) (q : Q6) :
    realFourierAtom nu (a₁ + a₂) (b₁ + b₂) q =
      realFourierAtom nu a₁ b₁ q + realFourierAtom nu a₂ b₂ q := by
  simp [realFourierAtom]
  ring

/- This is the minimal coefficient-to-function lemma needed to lift a
   keywise rational equality into h_aggregate.  It is intentionally kept
   independent of the six-body expansion. -/
theorem realFourierAtom_complex_re_target
    (nu : Joint → ℤ) (a b : ℚ) (q : Q6) :
    Complex.re (((a : ℂ) + (b : ℂ) * Complex.I) *
      Complex.exp (Complex.I * (phase nu q : ℂ))) =
      realFourierAtom nu a b q := by
  let theta : ℝ := phase nu q
  have h_exp : Complex.exp (Complex.I * (theta : ℂ)) =
      (Real.cos theta : ℂ) + (Real.sin theta : ℂ) * Complex.I := by
    rw [show Complex.I * (theta : ℂ) = (theta : ℂ) * Complex.I by ring]
    exact Complex.exp_ofReal_mul_I theta
  change Complex.re (((a : ℂ) + (b : ℂ) * Complex.I) *
      Complex.exp (Complex.I * (theta : ℂ))) = _
  rw [h_exp]
  simp [realFourierAtom, Complex.mul_re, Complex.add_re]
  ring

#print axioms sourceBodyMass_eq_bodyMass
#print axioms sourceBodyMass_eq_juliaExactBodyMass
#print axioms six_per_body_source_expansion
#print axioms realFourierAtom_add
#print axioms realFourierAtom_complex_re_target

end
end RouteBO1PerBodyExactSource

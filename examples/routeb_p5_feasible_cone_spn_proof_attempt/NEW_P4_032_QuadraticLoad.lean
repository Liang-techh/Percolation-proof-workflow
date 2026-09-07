import NEW_P4_032_DefectNormBudget

/-!
UNCOMPILED source-independent quadratic residual-load skeleton.
No PSD assumption on SBB, numerical eigenvalue certificate, Schur inversion,
deployed source instance, or Lean/Lake verification. No new triangle proof.
All vector norms use the imported explicit Euclidean norm2.
-/

set_option autoImplicit false

namespace RouteBP4032QuadraticLoad

open scoped BigOperators
open RouteBP4032BlockDefects
open RouteBP4032DefectNormBudget

noncomputable section

/-- rB^T SBB rB. SBB is an arbitrary real 2x2 matrix, possibly nonsymmetric
or indefinite. This definition does not assert a physical load identity. -/
def quadratic (SBB : BB) (rB : BVec) : ℝ :=
  ∑ i, ∑ j, rB i * SBB i j * rB j

/-- Optional uniform quadratic UPPER bound. This is proof-valued evidence;
it is not obtained from a numerical eigenvalue, and gives no PSD lower bound. -/
structure QuadraticUpperBound (SBB : BB) (k : ℝ) : Prop where
  bound : ∀ rB : BVec, quadratic SBB rB ≤ k * (norm2 rB)^2

/-- Local bound is enough; a global matrix property is not required.
k>=0 is needed to replace the norm square by its upper cap without reversing order. -/
theorem quadratic_cap (SBB : BB) (rB : BVec) (k rB_cap : ℝ)
    (hcap : 0 ≤ rB_cap) (hk : 0 ≤ k)
    (hNorm : norm2 rB ≤ rB_cap)
    (hQuadratic : quadratic SBB rB ≤ k * (norm2 rB)^2) :
    quadratic SBB rB ≤ k * rB_cap^2 := by
  have hsq : (norm2 rB)^2 ≤ rB_cap^2 := by
    simpa only [pow_two] using mul_le_mul hNorm hNorm (norm2_nonnegative rB) hcap
  exact hQuadratic.trans (mul_le_mul_of_nonneg_left hsq hk)

theorem quadratic_cap_of_uniform (SBB : BB) (rB : BVec) (k rB_cap : ℝ)
    (hcap : 0 ≤ rB_cap) (hk : 0 ≤ k)
    (hNorm : norm2 rB ≤ rB_cap) (hUpper : QuadraticUpperBound SBB k) :
    quadratic SBB rB ≤ k * rB_cap^2 :=
  quadratic_cap SBB rB k rB_cap hcap hk hNorm (hUpper.bound rB)

/-- The Schur/PMI consumer must supply this exact load comparison for the
same rB,SBB,normalization and domain. Cross terms or other residual pieces
must already be accounted for here; they are not silently discarded. -/
structure LoadBinding (SBB : BB) (rB : BVec) (residualLoad baseLoad weight : ℝ) : Prop where
  upper : residualLoad ≤ baseLoad + weight * quadratic SBB rB

theorem residual_load_cap (SBB : BB) (rB : BVec)
    (k rB_cap residualLoad baseLoad weight : ℝ)
    (hcap : 0 ≤ rB_cap) (hk : 0 ≤ k) (hweight : 0 ≤ weight)
    (hNorm : norm2 rB ≤ rB_cap)
    (hQuadratic : quadratic SBB rB ≤ k * (norm2 rB)^2)
    (binding : LoadBinding SBB rB residualLoad baseLoad weight) :
    residualLoad ≤ baseLoad + (weight * k) * rB_cap^2 := by
  have hq := quadratic_cap SBB rB k rB_cap hcap hk hNorm hQuadratic
  calc
    residualLoad ≤ baseLoad + weight * quadratic SBB rB := binding.upper
    _ ≤ baseLoad + weight * (k * rB_cap^2) :=
      add_le_add_left (mul_le_mul_of_nonneg_left hq hweight) baseLoad
    _ = baseLoad + (weight * k) * rB_cap^2 := by ring

/-- Directly consume the EXISTING defect norm budget. For the O1 instance use
R=Rport MBD MDDinv DeltaMDB and T=MBD*MDDinv with its proved defect identity.
All defects and cross terms in the squared total cap remain present. -/
theorem defect_quadratic_load (R : BB) (T : BD) (SBB : BB)
    (aB rB eB : BVec) (eD : DVec)
    (rho tau alpha deltaD deltaB k residualLoad baseLoad weight : ℝ)
    (identity : rB = R *ᵥ aB + T *ᵥ eD + eB)
    (hR : ActionBound R rho) (hT : ActionBound T tau)
    (hA : norm2 aB ≤ alpha) (hD : norm2 eD ≤ deltaD) (hB : norm2 eB ≤ deltaB)
    (hcap : 0 ≤ rho * alpha + tau * deltaD + deltaB)
    (hk : 0 ≤ k) (hweight : 0 ≤ weight)
    (hUpper : QuadraticUpperBound SBB k)
    (binding : LoadBinding SBB rB residualLoad baseLoad weight) :
    residualLoad ≤ baseLoad + (weight * k) * (rho * alpha + tau * deltaD + deltaB)^2 := by
  have hn := operator_budget R T aB rB eB eD rho tau alpha deltaD deltaB
    identity hR hT hA hD hB
  exact residual_load_cap SBB rB k (rho * alpha + tau * deltaD + deltaB)
    residualLoad baseLoad weight hcap hk hweight hn (hUpper.bound rB) binding

/-- Allocation is another explicit inequality, not a claim that a Schur/PMI
condition has been discharged simply because a residual load is bounded. -/
theorem allocated_load (residualLoad baseLoad weight k rB_cap available : ℝ)
    (hLoad : residualLoad ≤ baseLoad + (weight * k) * rB_cap^2)
    (hAllocation : baseLoad + (weight * k) * rB_cap^2 ≤ available) :
    residualLoad ≤ available := hLoad.trans hAllocation

/-- Same-domain pointwise seam. Uniform k/cap/load parameters are supplied,
not inferred from samples or from membership of a different source state. -/
theorem on_domain_load {X : Type*} (D : X → Prop) (SBB : X → BB)
    (rB : X → BVec) (residualLoad : X → ℝ)
    (k rB_cap baseLoad weight : ℝ)
    (hcap : 0 ≤ rB_cap) (hk : 0 ≤ k) (hweight : 0 ≤ weight)
    (hNorm : ∀ x, D x → norm2 (rB x) ≤ rB_cap)
    (hQuadratic : ∀ x, D x → quadratic (SBB x) (rB x) ≤ k * (norm2 (rB x))^2)
    (binding : ∀ x, D x → LoadBinding (SBB x) (rB x) (residualLoad x) baseLoad weight) :
    ∀ x, D x → residualLoad x ≤ baseLoad + (weight * k) * rB_cap^2 := by
  intro x hx
  exact residual_load_cap (SBB x) (rB x) k rB_cap (residualLoad x) baseLoad weight
    hcap hk hweight (hNorm x hx) (hQuadratic x hx) (binding x hx)

end

-- Future audit commands only; NOT executed in this round.
#print axioms quadratic_cap
#print axioms quadratic_cap_of_uniform
#print axioms residual_load_cap
#print axioms defect_quadratic_load
#print axioms allocated_load
#print axioms on_domain_load

end RouteBP4032QuadraticLoad

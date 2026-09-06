import Percolation.Literature.PercolationEvents

set_option autoImplicit false
set_option relaxedAutoImplicit false

universe u

namespace Percolation.Literature.LocalFKG

/-- The finite Boolean cube; only its coordinate type will carry `Fintype`. -/
abbrev Cube (ι : Type u) := ι → Bool

/-- Coordinatewise order, written without relying on a particular Bool order instance. -/
def CubeLE {ι : Type u} (x y : Cube ι) : Prop :=
  ∀ i, x i = true → y i = true

def Increasing {ι : Type u} (f : Cube ι → ℝ) : Prop :=
  ∀ x y, CubeLE x y → f x ≤ f y

/-- Independent Bernoulli weights, allowing different parameters and endpoints. -/
noncomputable def cubeWeight {ι : Type u} [Fintype ι]
    (q : ι → unitInterval) (x : Cube ι) : ℝ :=
  ∏ i, if x i = true then (q i : ℝ) else 1 - (q i : ℝ)

noncomputable def cubeExpectation {ι : Type u} [Fintype ι]
    (q : ι → unitInterval) (f : Cube ι → ℝ) : ℝ := by
  classical
  exact ∑ x, cubeWeight q x * f x

/-- Extend by closed coordinates outside F and close all nonedges of G.
The bits indexed by nonedges in F are dummy coordinates, still summed over. -/
def cubeConfig {V : Type u} (G : SimpleGraph V) (F : Finset (Sym2 V))
    (x : Cube {e // e ∈ F}) : BondConfig V :=
  {e | ∃ h : e ∈ F, x ⟨e, h⟩ = true ∧ e ∈ G.edgeSet}

noncomputable def eventIndicator {V : Type u} (G : SimpleGraph V)
    (F : Finset (Sym2 V)) (A : Set (BondConfig V))
    (x : Cube {e // e ∈ F}) : ℝ := by
  classical
  exact if cubeConfig G F x ∈ A then 1 else 0

end Percolation.Literature.LocalFKG

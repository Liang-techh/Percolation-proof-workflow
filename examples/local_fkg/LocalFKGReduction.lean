import LocalFKGDefinitions

set_option autoImplicit false
set_option relaxedAutoImplicit false

universe u

namespace Percolation.Literature.LocalFKG

theorem cubeConfig_mono {V : Type u} (G : SimpleGraph V) (F : Finset (Sym2 V))
    {x y : Cube {e // e ∈ F}} (hxy : CubeLE x y) :
    cubeConfig G F x ⊆ cubeConfig G F y := by
  rintro e ⟨he, hx, hG⟩
  exact ⟨he, hxy ⟨e, he⟩ hx, hG⟩

theorem eventIndicator_nonneg {V : Type u} (G : SimpleGraph V)
    (F : Finset (Sym2 V)) (A : Set (BondConfig V))
    (x : Cube {e // e ∈ F}) : 0 ≤ eventIndicator G F A x := by
  classical
  by_cases h : cubeConfig G F x ∈ A <;> simp [eventIndicator, h]

theorem eventIndicator_increasing {V : Type u} (G : SimpleGraph V)
    (F : Finset (Sym2 V)) {A : Set (BondConfig V)} (hA : IsUpperSet A) :
    Increasing (eventIndicator G F A) := by
  classical
  intro x y hxy
  by_cases hx : cubeConfig G F x ∈ A
  · have hy : cubeConfig G F y ∈ A := hA (cubeConfig_mono G F hxy) hx
    simp [eventIndicator, hx, hy]
  · simpa [eventIndicator, hx] using eventIndicator_nonneg G F A y

theorem eventIndicator_inter {V : Type u} (G : SimpleGraph V)
    (F : Finset (Sym2 V)) (A B : Set (BondConfig V)) :
    eventIndicator G F (A ∩ B) =
      fun x => eventIndicator G F A x * eventIndicator G F B x := by
  classical
  funext x
  by_cases hA : cubeConfig G F x ∈ A <;>
    by_cases hB : cubeConfig G F x ∈ B <;>
      simp [eventIndicator, hA, hB]

/-- Conditional reduction only. Both child statements are explicit universal hypotheses;
this module does not import the obligation placeholders or the Challenge. -/
theorem harris_fkg_local_of_children
    (hfinite : ∀ (ι : Type u) [Fintype ι] (q : ι → unitInterval)
      (f g : Cube ι → ℝ),
      (∀ x, 0 ≤ f x) → (∀ x, 0 ≤ g x) →
      Increasing f → Increasing g →
      cubeExpectation q f * cubeExpectation q g ≤
        cubeExpectation q (fun x => f x * g x))
    (hlocal : ∀ {V : Type u} (G : SimpleGraph V) (p : unitInterval)
      (F : Finset (Sym2 V)) (A : Set (BondConfig V)),
      DeterminedBy A (↑F : Set (Sym2 V)) →
      (bondPercolation G p).real A =
        cubeExpectation (fun _ : {e // e ∈ F} => p) (eventIndicator G F A))
    {V : Type u} (G : SimpleGraph V) (p : unitInterval)
    {A B : Set (BondConfig V)}
    (hA : IsUpperSet A) (hB : IsUpperSet B)
    (hAl : IsLocalEvent A) (hBl : IsLocalEvent B) :
    (bondPercolation G p).real A * (bondPercolation G p).real B ≤
      (bondPercolation G p).real (A ∩ B) := by
  classical
  rcases hAl with ⟨FA, hFA⟩
  rcases hBl with ⟨FB, hFB⟩
  let F := FA ∪ FB
  have hAF : DeterminedBy A (↑F : Set (Sym2 V)) :=
    hFA.mono (by intro e he; exact Finset.mem_union.mpr (Or.inl he))
  have hBF : DeterminedBy B (↑F : Set (Sym2 V)) :=
    hFB.mono (by intro e he; exact Finset.mem_union.mpr (Or.inr he))
  rw [hlocal G p F A hAF, hlocal G p F B hBF,
    hlocal G p F (A ∩ B) (hAF.inter hBF), eventIndicator_inter]
  exact hfinite {e // e ∈ F} (fun _ => p)
    (eventIndicator G F A) (eventIndicator G F B)
    (eventIndicator_nonneg G F A) (eventIndicator_nonneg G F B)
    (eventIndicator_increasing G F hA) (eventIndicator_increasing G F hB)

end Percolation.Literature.LocalFKG

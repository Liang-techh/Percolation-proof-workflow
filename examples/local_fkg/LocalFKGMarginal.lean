import LocalFKGDefinitions
import Mathlib.Probability.Distributions.Bernoulli

set_option autoImplicit false
set_option relaxedAutoImplicit false

universe u

namespace Percolation.Literature.LocalFKG

open MeasureTheory ProbabilityTheory

private theorem marginal_map_mask {V : Type u} (G : SimpleGraph V) (p : unitInterval) :
    (Measure.infinitePi (fun _ : Sym2 V => bernoulliMeasure true false p)).map
      (fun x => {e | x e = true ∧ e ∈ G.edgeSet}) = bondPercolation G p := by
  classical
  let f : Sym2 V → Bool → Prop := fun e b => b = true ∧ e ∈ G.edgeSet
  have hf : ∀ e, Measurable (f e) := fun _ => measurable_from_top
  have hm := Measure.infinitePi_map_pi
    (fun _ : Sym2 V => bernoulliMeasure true false p) hf
  have hc : ∀ e, (bernoulliMeasure true false p).map (f e) =
      unitInterval.toNNReal p • Measure.dirac (e ∈ G.edgeSet) +
        unitInterval.toNNReal (unitInterval.symm p) • Measure.dirac False := by
    intro e
    rw [map_bernoulliMeasure' true false (hf e)]
    simp [f, bernoulliMeasure_def]
  simp_rw [hc] at hm
  rw [bondPercolation, setBernoulli_eq_map, ← hm,
    Measure.map_map (by fun_prop) (by fun_prop)]
  rfl

private theorem marginal_preimage {V : Type u} (G : SimpleGraph V)
    (F : Finset (Sym2 V)) (A : Set (BondConfig V))
    (hA : DeterminedBy A (↑F : Set (Sym2 V))) :
    (fun x : Sym2 V → Bool => {e | x e = true ∧ e ∈ G.edgeSet}) ⁻¹' A =
      F.restrict ⁻¹' {x | cubeConfig G F x ∈ A} := by
  ext x
  apply (determinedBy_iff _ _).mp hA
  ext e
  simp only [Set.mem_inter_iff, Set.mem_setOf_eq, cubeConfig]
  constructor
  · rintro ⟨⟨hx, he⟩, hF⟩
    exact ⟨⟨hF, hx, he⟩, hF⟩
  · rintro ⟨⟨hF, hx, he⟩, _⟩
    exact ⟨⟨hx, he⟩, hF⟩

private theorem marginal_cube_singleton {ι : Type u} [Fintype ι]
    (p : unitInterval) (x : Cube ι) :
    (Measure.pi (fun _ : ι => bernoulliMeasure true false p)).real {x} =
      cubeWeight (fun _ => p) x := by
  classical
  simp only [measureReal_def, Measure.pi_singleton, ENNReal.toReal_prod, cubeWeight]
  apply Finset.prod_congr rfl
  intro i _
  change (bernoulliMeasure true false p).real {x i} = _
  cases x i <;> simp

theorem local_event_cube_expectation
    {V : Type u} (G : SimpleGraph V) (p : unitInterval)
    (F : Finset (Sym2 V)) (A : Set (BondConfig V))
    (hA : DeterminedBy A (↑F : Set (Sym2 V))) :
    (bondPercolation G p).real A =
      cubeExpectation (fun _ : {e // e ∈ F} => p) (eventIndicator G F A) := by
  classical
  have hmask : Measurable (fun x : Sym2 V → Bool =>
      {e | x e = true ∧ e ∈ G.edgeSet}) := by
    change Measurable (MeasurableEquiv.setOf ∘
      (fun x : Sym2 V → Bool => fun e => x e = true ∧ e ∈ G.edgeSet))
    exact MeasurableEquiv.setOf.measurable.comp
      (measurable_pi_lambda _ fun e =>
        (show Measurable (fun b : Bool => b = true ∧ e ∈ G.edgeSet) from
          measurable_from_top).comp (measurable_pi_apply e))
  have hfinite : MeasurableSet {x | cubeConfig G F x ∈ A} := .of_discrete
  have hm : (bondPercolation G p) A =
      (Measure.pi (fun _ : {e // e ∈ F} => bernoulliMeasure true false p))
        {x | cubeConfig G F x ∈ A} := by
    rw [← marginal_map_mask G p, Measure.map_apply hmask hA.measurableSet_of_finset,
      marginal_preimage G F A hA, ← Measure.map_apply (Finset.measurable_restrict F) hfinite,
      Measure.infinitePi_map_restrict]
  rw [measureReal_def, hm]
  let S : Finset (Cube {e // e ∈ F}) := Finset.univ.filter (fun x => cubeConfig G F x ∈ A)
  have hS : (↑S : Set (Cube {e // e ∈ F})) = {x | cubeConfig G F x ∈ A} := by
    ext x
    simp [S]
  rw [← hS, ← measureReal_def, ← sum_measureReal_singleton]
  simp only [marginal_cube_singleton]
  simp [S, Finset.sum_filter, cubeExpectation, eventIndicator, mul_ite]
  apply Finset.sum_congr
  · ext x
    simp
  · intro x _
    rfl

end Percolation.Literature.LocalFKG

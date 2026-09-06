import LocalFKGDefinitions
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

set_option autoImplicit false
set_option relaxedAutoImplicit false

universe u v
namespace Percolation.Literature.LocalFKG

private theorem finite_weight_nonneg {ι : Type u} [Fintype ι]
    (q : ι → unitInterval) (x : Cube ι) : 0 ≤ cubeWeight q x := by
  classical
  apply Finset.prod_nonneg
  intro i _
  split_ifs
  · exact (q i).property.1
  · exact sub_nonneg.mpr (q i).property.2

private theorem finite_expectation_mono {ι : Type u} [Fintype ι]
    (q : ι → unitInterval) (f g : Cube ι → ℝ) (h : ∀ x, f x ≤ g x) :
    cubeExpectation q f ≤ cubeExpectation q g := by
  classical
  exact Finset.sum_le_sum fun x _ => mul_le_mul_of_nonneg_left (h x)
    (finite_weight_nonneg q x)

private def finite_cube_equiv {ι : Type u} {κ : Type v} (e : ι ≃ κ) :
    Cube ι ≃ Cube κ where
  toFun x := fun j => x (e.symm j)
  invFun y := fun i => y (e i)
  left_inv x := by funext i; simp
  right_inv y := by funext j; simp

private theorem finite_expectation_equiv {ι : Type u} {κ : Type v}
    [Fintype ι] [Fintype κ] (e : ι ≃ κ)
    (q : κ → unitInterval) (f : Cube κ → ℝ) :
    cubeExpectation (fun i => q (e i)) (fun x => f (finite_cube_equiv e x)) =
      cubeExpectation q f := by
  classical
  apply Fintype.sum_equiv (finite_cube_equiv e)
  intro x
  congr 1
  apply Fintype.prod_equiv e
  intro i
  simp [finite_cube_equiv]

private def finite_split_equiv (n : ℕ) : Bool × Cube (Fin n) ≃ Cube (Fin (n+1)) where
  toFun z := Fin.cons z.1 z.2
  invFun x := (x 0, fun i => x i.succ)
  left_inv z := by cases z; rfl
  right_inv x := by funext i; exact Fin.cases rfl (fun _ => rfl) i

private theorem finite_expectation_split (n : ℕ) (q : Fin (n+1) → unitInterval)
    (f : Cube (Fin (n+1)) → ℝ) :
    cubeExpectation q f =
      (1 - (q 0 : ℝ)) * cubeExpectation (fun i => q i.succ) (fun x => f (Fin.cons false x)) +
      (q 0 : ℝ) * cubeExpectation (fun i => q i.succ) (fun x => f (Fin.cons true x)) := by
  classical
  letI : DecidableEq (Fin (n+1)) := Classical.decEq _
  letI : DecidableEq (Fin n) := Classical.decEq _
  unfold cubeExpectation
  calc
    _ = ∑ z : Bool × Cube (Fin n), cubeWeight q (Fin.cons z.1 z.2) * f (Fin.cons z.1 z.2) :=
      (Fintype.sum_equiv (finite_split_equiv n)
        (fun z => cubeWeight q (Fin.cons z.1 z.2) * f (Fin.cons z.1 z.2))
        (fun x => cubeWeight q x * f x) (fun _ => rfl)).symm
    _ = _ := by
      simp only [Fintype.sum_prod_type, Fintype.sum_bool]
      simp only [cubeWeight, Fin.prod_univ_succ, Fin.cons_zero, Fin.cons_succ,
        Bool.false_eq_true, if_false, if_true]
      simp only [mul_assoc, Finset.mul_sum]
      exact add_comm (G := ℝ) _ _

private theorem finite_cons_increasing (n : ℕ) (f : Cube (Fin (n+1)) → ℝ)
    (hf : Increasing f) (b : Bool) : Increasing (fun x => f (Fin.cons b x)) := by
  intro x y h
  apply hf
  intro i
  exact Fin.cases (fun hb => hb) (fun j => h j) i

private theorem finite_slice_order (n : ℕ) (f : Cube (Fin (n+1)) → ℝ)
    (hf : Increasing f) (x : Cube (Fin n)) : f (Fin.cons false x) ≤ f (Fin.cons true x) := by
  apply hf
  intro i
  exact Fin.cases (by simp) (fun _ h => h) i

private theorem finite_correlation_fin (n : ℕ) (q : Fin n → unitInterval)
    (f g : Cube (Fin n) → ℝ) (hf : Increasing f) (hg : Increasing g) :
    cubeExpectation q f * cubeExpectation q g ≤
      cubeExpectation q (fun x => f x * g x) := by
  induction n with
  | zero =>
      simp [cubeExpectation, cubeWeight, Finset.univ_unique]
  | succ n ih =>
      let q' : Fin n → unitInterval := fun i => q i.succ
      let f0 := fun x => f (Fin.cons false x)
      let f1 := fun x => f (Fin.cons true x)
      let g0 := fun x => g (Fin.cons false x)
      let g1 := fun x => g (Fin.cons true x)
      have h0 := ih q' f0 g0 (finite_cons_increasing n f hf false)
        (finite_cons_increasing n g hg false)
      have h1 := ih q' f1 g1 (finite_cons_increasing n f hf true)
        (finite_cons_increasing n g hg true)
      have hfm : cubeExpectation q' f0 ≤ cubeExpectation q' f1 :=
        finite_expectation_mono q' f0 f1 (finite_slice_order n f hf)
      have hgm : cubeExpectation q' g0 ≤ cubeExpectation q' g1 :=
        finite_expectation_mono q' g0 g1 (finite_slice_order n g hg)
      have hp : 0 ≤ (q 0 : ℝ) := (q 0).property.1
      have hpc : 0 ≤ 1 - (q 0 : ℝ) := sub_nonneg.mpr (q 0).property.2
      -- The remaining covariance is p * (1-p) * (E f1 - E f0) * (E g1 - E g0).
      have hc := mul_nonneg (mul_nonneg hp hpc)
        (mul_nonneg (sub_nonneg.mpr hfm) (sub_nonneg.mpr hgm))
      have ha := mul_le_mul_of_nonneg_left h0 hpc
      have hb := mul_le_mul_of_nonneg_left h1 hp
      rw [finite_expectation_split, finite_expectation_split, finite_expectation_split]
      change ((1 - (q 0 : ℝ)) * cubeExpectation q' f0 + (q 0 : ℝ) * cubeExpectation q' f1) *
        ((1 - (q 0 : ℝ)) * cubeExpectation q' g0 + (q 0 : ℝ) * cubeExpectation q' g1) ≤
        (1 - (q 0 : ℝ)) * cubeExpectation q' (fun x => f0 x * g0 x) +
        (q 0 : ℝ) * cubeExpectation q' (fun x => f1 x * g1 x)
      nlinarith only [hc, ha, hb]

/-- Finite Bernoulli positive correlation, including parameters zero and one. -/
theorem finite_bernoulli_positive_correlation
    (ι : Type u) [Fintype ι] (q : ι → unitInterval)
    (f g : Cube ι → ℝ)
    (hf0 : ∀ x, 0 ≤ f x) (hg0 : ∀ x, 0 ≤ g x)
    (hf : Increasing f) (hg : Increasing g) :
    cubeExpectation q f * cubeExpectation q g ≤
      cubeExpectation q (fun x => f x * g x) := by
  classical
  -- The finite argument proves the stronger real-valued statement.
  clear hf0 hg0
  let e : Fin (Fintype.card ι) ≃ ι := (Fintype.equivFin ι).symm
  have hf' : Increasing (fun x => f (finite_cube_equiv e x)) := by
    intro x y h
    exact hf _ _ (fun i => h (e.symm i))
  have hg' : Increasing (fun x => g (finite_cube_equiv e x)) := by
    intro x y h
    exact hg _ _ (fun i => h (e.symm i))
  have h := finite_correlation_fin (Fintype.card ι) (fun i => q (e i))
    (fun x => f (finite_cube_equiv e x)) (fun x => g (finite_cube_equiv e x)) hf' hg'
  rw [← finite_expectation_equiv e q f, ← finite_expectation_equiv e q g,
    ← finite_expectation_equiv e q (fun x => f x * g x)]
  exact h

end Percolation.Literature.LocalFKG

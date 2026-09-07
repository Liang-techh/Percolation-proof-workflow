import Mathlib

set_option autoImplicit false

namespace RouteBForceAccelNormalization

noncomputable section

/-!
This file is a deliberately small exact-real adapter.  It treats a residual
as a force vector `eF` and an acceleration residual as `eA`.  The source
binding `eF = M * eA`, and the lower operator bound used below, are explicit
premises.  No DH, Float64, trajectory, coverage, or D-row fact is inferred.
-/

abbrev Vec (n : ℕ) := Fin n → ℝ
abbrev Mat (n : ℕ) := Fin n → Fin n → ℝ

def matVec {n : ℕ} (M : Mat n) (x : Vec n) : Vec n :=
  fun i => ∑ j, M i j * x j

def sqNorm {n : ℕ} (x : Vec n) : ℝ := ∑ i, x i ^ 2

def forcePower {ι n : ℕ} [Fintype (Fin ι)]
    (D : ℝ) (eF : Fin ι → Vec n) : ℝ :=
  ∑ t, sqNorm (eF t) / (2 * D)

def accelerationBudget {ι n : ℕ} [Fintype (Fin ι)]
    (eA : Fin ι → Vec n) : ℝ :=
  ∑ t, sqNorm (eA t)

def OperatorLowerBound {n : ℕ} (M : Mat n) (κ : ℝ) : Prop :=
  ∀ x, κ * sqNorm x ≤ sqNorm (matVec M x)

def SingularLowerBound {n : ℕ} (M : Mat n) (m : ℝ) : Prop :=
  OperatorLowerBound M (m ^ 2)

theorem sqNorm_nonneg {n : ℕ} (x : Vec n) : 0 ≤ sqNorm x := by
  unfold sqNorm
  exact Finset.sum_nonneg (fun i _ => sq_nonneg (x i))

theorem singular_bound_is_operator_bound {n : ℕ} (M : Mat n) (m : ℝ)
    (h : SingularLowerBound M m) : OperatorLowerBound M (m ^ 2) :=
  h

theorem acceleration_sqNorm_le_of_force_factorization
    {n : ℕ} (M : Mat n) (eA eF : Vec n) (κ : ℝ)
    (hκ : 0 < κ) (hfactor : eF = matVec M eA)
    (hop : OperatorLowerBound M κ) :
    sqNorm eA ≤ sqNorm eF / κ := by
  have hbound := hop eA
  apply (le_div_iff₀ hκ).2
  calc
    sqNorm eA * κ = κ * sqNorm eA := by ring
    _ ≤ sqNorm (matVec M eA) := hbound
    _ = sqNorm eF := by rw [hfactor]

theorem acceleration_budget_le_of_factorization
    {ι n : ℕ} [Fintype (Fin ι)]
    (M : Mat n) (eA eF : Fin ι → Vec n) (κ : ℝ)
    (hκ : 0 < κ)
    (hfactor : ∀ t, eF t = matVec M (eA t))
    (hop : OperatorLowerBound M κ) :
    accelerationBudget eA ≤
      (∑ t, sqNorm (eF t)) / κ := by
  have hsum : κ * (∑ t, sqNorm (eA t)) ≤ ∑ t, sqNorm (eF t) := by
    calc
      κ * (∑ t, sqNorm (eA t)) = ∑ t, κ * sqNorm (eA t) := by
        rw [Finset.mul_sum]
      _ ≤ ∑ t, sqNorm (eF t) := by
        apply Finset.sum_le_sum
        intro t ht
        have h := hop (eA t)
        calc
          κ * sqNorm (eA t) ≤ sqNorm (matVec M (eA t)) := h
          _ = sqNorm (eF t) := by rw [hfactor t]
  apply (le_div_iff₀ hκ).2
  simpa [accelerationBudget, mul_comm] using hsum

theorem acceleration_budget_le_of_force_power_budget
    {ι n : ℕ} [Fintype (Fin ι)]
    (M : Mat n) (eA eF : Fin ι → Vec n) (D κ B : ℝ)
    (hD : 0 < D) (hκ : 0 < κ)
    (hfactor : ∀ t, eF t = matVec M (eA t))
    (hop : OperatorLowerBound M κ)
    (hpower : forcePower D eF ≤ B) :
    accelerationBudget eA ≤ 2 * D * B / κ := by
  have hforce : (∑ t, sqNorm (eF t)) ≤ 2 * D * B := by
    have hpower' : (∑ t, sqNorm (eF t)) / (2 * D) ≤ B := by
      simpa [forcePower, Finset.sum_div] using hpower
    have hden : 0 < 2 * D := by positivity
    have hforce' := (div_le_iff₀ hden).mp hpower'
    nlinarith [hforce']
  have hacc := acceleration_budget_le_of_factorization M eA eF κ hκ hfactor hop
  have hinv : 0 ≤ (1 / κ : ℝ) := by positivity
  have hscaled : (∑ t, sqNorm (eF t)) * (1 / κ) ≤
      (2 * D * B) * (1 / κ) :=
    mul_le_mul_of_nonneg_right hforce hinv
  calc
    accelerationBudget eA ≤ (∑ t, sqNorm (eF t)) / κ := hacc
    _ = (∑ t, sqNorm (eF t)) * (1 / κ) := by rw [div_eq_mul_inv, one_div]
    _ ≤ (2 * D * B) * (1 / κ) := hscaled
    _ = 2 * D * B / κ := by simp [div_eq_mul_inv]

theorem acceleration_budget_le_of_singular_lower_bound
    {ι n : ℕ} [Fintype (Fin ι)]
    (M : Mat n) (eA eF : Fin ι → Vec n) (m D B : ℝ)
    (hm : 0 < m) (hD : 0 < D)
    (hfactor : ∀ t, eF t = matVec M (eA t))
    (hM : SingularLowerBound M m)
    (hpower : forcePower D eF ≤ B) :
    accelerationBudget eA ≤ 2 * D * B / (m ^ 2) := by
  apply acceleration_budget_le_of_force_power_budget M eA eF D (m ^ 2) B
    hD (sq_pos_of_pos hm) hfactor hM hpower

/-! The exact 2-by-2 diagonal block used as a sanity-check normalization.
It is an illustrative rational operator, not the deployed DH `M(q)` or the
audit's distinct frozen `M0_BB`. -/

noncomputable def exactBlockMass : Mat 2 := fun i j =>
  if i = 0 ∧ j = 0 then (1 / 5 : ℝ)
  else if i = 1 ∧ j = 1 then (1 / 10 : ℝ)
  else 0

theorem exactBlockMass_apply (x : Vec 2) :
    matVec exactBlockMass x =
      fun i => if i = 0 then (1 / 5 : ℝ) * x 0
        else (1 / 10 : ℝ) * x 1 := by
  funext i
  fin_cases i <;> simp [matVec, exactBlockMass]

theorem exactBlockMass_operator_lower_bound :
    OperatorLowerBound exactBlockMass (1 / 100 : ℝ) := by
  intro x
  rw [exactBlockMass_apply]
  simp only [sqNorm, Fin.sum_univ_two]
  norm_num
  nlinarith [sq_nonneg (x 0), sq_nonneg (x 1)]

theorem exactBlockMass_acceleration_budget_conversion
    {ι : ℕ} [Fintype (Fin ι)]
    (eA eF : Fin ι → Vec 2) (D B : ℝ)
    (hD : 0 < D)
    (hfactor : ∀ t, eF t = matVec exactBlockMass (eA t))
    (hpower : forcePower D eF ≤ B) :
    accelerationBudget eA ≤ 200 * D * B := by
  have h := acceleration_budget_le_of_force_power_budget
    exactBlockMass eA eF D (1 / 100 : ℝ) B hD (by norm_num)
    hfactor exactBlockMass_operator_lower_bound hpower
  calc
    accelerationBudget eA ≤ 2 * D * B / (1 / 100 : ℝ) := h
    _ = 200 * D * B := by norm_num [div_eq_mul_inv]; ring

/-! A force-only budget has no acceleration consequence without a lower bound.
The zero operator is the minimal counterexample. -/

theorem no_force_only_acceleration_bound_without_lower_bound :
    ¬ (∀ C : ℝ, 0 ≤ C → ∀ a f : ℝ,
      f = (0 : ℝ) * a → a ^ 2 ≤ C * f ^ 2) := by
  intro h
  have hbad := h 0 (by norm_num) 1 0 (by norm_num)
  norm_num at hbad

theorem force_only_zero_budget_does_not_bound_acceleration :
    ¬ (∀ C : ℝ, 0 ≤ C → ∀ a : ℝ,
      forcePower 1 (fun _ : Fin 1 => fun _ : Fin 1 => 0) ≤ 0 →
        accelerationBudget (fun _ : Fin 1 => fun _ : Fin 1 => a) ≤ C) := by
  intro h
  have hbad := h 0 (by norm_num) 1
    (by norm_num [forcePower, accelerationBudget, sqNorm])
  norm_num [accelerationBudget, sqNorm] at hbad

#print axioms acceleration_budget_le_of_force_power_budget
#print axioms exactBlockMass_acceleration_budget_conversion
#print axioms no_force_only_acceleration_bound_without_lower_bound

end
end RouteBForceAccelNormalization

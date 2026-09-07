import NEW_P4_032_DivisionFreeContraction
import Mathlib.Algebra.Order.Archimedean.Basic

/-!
UNCOMPILED exact-real domain-uniform contraction interface.
No variable division, reciprocal, sqrt, or source identification.
0.5 is an exact real numeral, not a Float approximation.
A fixed finite domain is distinguished from a family of finite instances.
-/

set_option autoImplicit false

namespace RouteBP4032DomainUniformContraction

open RouteBP4032DivisionFreeContraction

noncomputable section

/-- One typed scalar field: all evidence refers to these SAME functions. -/
structure BudgetField (X : Type*) where
  domain : X → Prop
  energy : X → ℝ
  bias : X → ℝ
  rho : X → ℝ

structure PointwiseClosure {X : Type*} (f : BudgetField X) : Prop where
  energy_nonnegative : ∀ x, f.domain x → 0 ≤ f.energy x
  bias_nonnegative : ∀ x, f.domain x → 0 ≤ f.bias x
  rho_nonnegative : ∀ x, f.domain x → 0 ≤ f.rho x
  strict : ∀ x, f.domain x → f.rho x < 1
  closure : ∀ x, f.domain x → f.energy x ≤ f.bias x + f.rho x * f.energy x

/-- Proof-bearing uniform input; pointwise strictness alone does not
construct this packet. No optional evidence or default bound. -/
structure UniformBudget {X : Type*} (f : BudgetField X) where
  rhoBar : ℝ
  biasBar : ℝ
  cap : ℝ
  rhoBar_nonnegative : 0 ≤ rhoBar
  rhoBar_strict : rhoBar < 1
  biasBar_nonnegative : 0 ≤ biasBar
  cap_nonnegative : 0 ≤ cap
  rho_bound : ∀ x, f.domain x → f.rho x ≤ rhoBar
  bias_bound : ∀ x, f.domain x → f.bias x ≤ biasBar
  allocation : biasBar ≤ (1 - rhoBar) * cap

/-- Only monotone replacement by uniform parameters is new here. The
scalar cancellation is delegated to the preceding leaf. -/
theorem uniform_cap {X : Type*} (f : BudgetField X)
    (hp : PointwiseClosure f) (hu : UniformBudget f) :
    ∀ x, f.domain x → f.energy x ≤ hu.cap := by
  intro x hx
  have hmul := mul_le_mul_of_nonneg_right (hu.rho_bound x hx)
    (hp.energy_nonnegative x hx)
  have hclosure := hp.closure x hx
  have hb := hu.bias_bound x hx
  apply allocated_upper_bound (f.energy x) hu.biasBar hu.rhoBar hu.cap
    hu.rhoBar_strict _ hu.allocation
  linarith

/-- Fixed finite domains ALWAYS have a strict uniform majorant. Even an
empty domain is covered, using 0. This is not a theorem about a whole
parameterized family of finite domains at once. -/
theorem finite_strict_majorant {X : Type*} (s : Finset X) (rho : X → ℝ)
    (h : ∀ x ∈ s, rho x < 1) :
    ∃ rhoBar : ℝ, rhoBar < 1 ∧ ∀ x ∈ s, rho x ≤ rhoBar := by
  classical
  revert h
  induction s using Finset.induction_on with
  | empty =>
      intro h
      exact ⟨0, by norm_num, by simp⟩
  | @insert a s ha ih =>
      intro h
      have hs : ∀ x ∈ s, rho x < 1 := by
        intro x hx
        exact h x (Finset.mem_insert_of_mem hx)
      obtain ⟨r, hr, hbound⟩ := ih hs
      refine ⟨max (rho a) r, max_lt_iff.mpr ⟨h a (by simp), hr⟩, ?_⟩
      intro x hx
      rcases Finset.mem_insert.mp hx with hxa | hxs
      · subst x
        exact le_max_left _ _
      · exact (hbound x hxs).trans (le_max_right _ _)

def dyadicEnergy (n : ℕ) : ℝ := (2 : ℝ)^n
def dyadicGap (n : ℕ) : ℝ := (0.5 : ℝ)^n
def dyadicRho (n : ℕ) : ℝ := 1 - dyadicGap n

theorem dyadic_gap_le_one (n : ℕ) : dyadicGap n ≤ 1 := by
  induction n with
  | zero => norm_num [dyadicGap]
  | succ n ih =>
      have hrec : dyadicGap (n + 1) = dyadicGap n * 0.5 := by
        simp [dyadicGap, pow_succ]
      rw [hrec]
      linarith

theorem dyadic_point (n : ℕ) :
    0 ≤ dyadicEnergy n ∧ 0 ≤ dyadicRho n ∧ dyadicRho n < 1 ∧
      dyadicEnergy n = 1 + dyadicRho n * dyadicEnergy n := by
  have hE : 0 < dyadicEnergy n := pow_pos (by norm_num) n
  have hg : 0 < dyadicGap n := pow_pos (by norm_num) n
  have hgle := dyadic_gap_le_one n
  have hprod : dyadicGap n * dyadicEnergy n = 1 := by
    unfold dyadicGap dyadicEnergy
    rw [← mul_pow]
    norm_num
  refine ⟨hE.le, ?_, ?_, ?_⟩ <;> unfold dyadicRho <;> nlinarith

theorem dyadic_energy_growth (n : ℕ) : (n : ℝ) + 1 ≤ dyadicEnergy n := by
  induction n with
  | zero => norm_num [dyadicEnergy]
  | succ n ih =>
      have hrec : dyadicEnergy (n + 1) = 2 * dyadicEnergy n := by
        simp [dyadicEnergy, pow_succ, mul_comm]
      rw [hrec]
      push_cast
      have hn : (0 : ℝ) ≤ (n : ℝ) := Nat.cast_nonneg n
      linarith

theorem dyadic_exceeds (cap : ℝ) : ∃ n : ℕ, cap < dyadicEnergy n := by
  obtain ⟨n, hn⟩ := exists_nat_gt cap
  exact ⟨n, by linarith [dyadic_energy_growth n]⟩

/-- No common rhoBar<1 on the single infinite domain N. Archimedean
growth is used without constructing a quotient threshold. -/
theorem no_dyadic_uniform_rho :
    ¬ ∃ rhoBar : ℝ, rhoBar < 1 ∧ ∀ n : ℕ, dyadicRho n ≤ rhoBar := by
  rintro ⟨rhoBar, hr, hbound⟩
  have hdelta : 0 < 1 - rhoBar := sub_pos.mpr hr
  obtain ⟨n, hn⟩ := exists_nat_mul_gt hdelta (1 : ℝ)
  have hn' : 1 < (n : ℝ) * (1 - rhoBar) := by
    simpa only [nsmul_eq_mul] using hn
  have hp := dyadic_point n
  have hscaled := mul_le_mul_of_nonneg_right (hbound n) hp.1
  have hg := mul_le_mul_of_nonneg_left (dyadic_energy_growth n) hdelta.le
  have heq := hp.2.2.2
  nlinarith

/-- A two-point INSTANCE, with an anchor and a dyadic point. -/
def twoPoint (n : ℕ) : BudgetField (Fin 2) where
  domain := fun _ => True
  energy := fun i => if i = 0 then 1 else dyadicEnergy n
  bias := fun _ => 1
  rho := fun i => if i = 0 then 0 else dyadicRho n

theorem twoPoint_closed (n : ℕ) : PointwiseClosure (twoPoint n) := by
  have hp := dyadic_point n
  constructor
  · intro i hi
    by_cases h : i = 0
    · simp [twoPoint, h]
    · simpa [twoPoint, h] using hp.1
  · intro i hi
    norm_num [twoPoint]
  · intro i hi
    by_cases h : i = 0
    · simp [twoPoint, h]
    · simpa [twoPoint, h] using hp.2.1
  · intro i hi
    by_cases h : i = 0
    · simp [twoPoint, h]
    · simpa [twoPoint, h] using hp.2.2.1
  · intro i hi
    by_cases h : i = 0
    · simp [twoPoint, h]
    · simpa [twoPoint, h] using hp.2.2.2.le

/-- For every proposed family-wide cap there is a finite two-point
instance violating it, although BOTH points are strictly contractive. -/
theorem two_point_family_counterexample (cap : ℝ) :
    ∃ n : ℕ, PointwiseClosure (twoPoint n) ∧
      cap < (twoPoint n).energy (1 : Fin 2) := by
  obtain ⟨n, hn⟩ := dyadic_exceeds cap
  exact ⟨n, twoPoint_closed n, by simpa [twoPoint] using hn⟩

theorem no_family_uniform_rho :
    ¬ ∃ rhoBar : ℝ, rhoBar < 1 ∧
      ∀ (n : ℕ) (i : Fin 2), (twoPoint n).rho i ≤ rhoBar := by
  rintro ⟨rhoBar, hr, hb⟩
  apply no_dyadic_uniform_rho
  refine ⟨rhoBar, hr, ?_⟩
  intro n
  simpa [twoPoint] using hb n (1 : Fin 2)

end

-- Future audit commands only; NOT executed in this round.
#print axioms uniform_cap
#print axioms finite_strict_majorant
#print axioms dyadic_point
#print axioms dyadic_energy_growth
#print axioms dyadic_exceeds
#print axioms no_dyadic_uniform_rho
#print axioms twoPoint_closed
#print axioms two_point_family_counterexample
#print axioms no_family_uniform_rho

end RouteBP4032DomainUniformContraction

import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic

/-!
Structural origin-quadratic rejection lemmas.

The first theorem packages the only local fact needed from a quadratic
little-o statement: every quadratic direction has nonpositive coefficient.
The second theorem is the exact 2-by-2 obstruction used for a zero-diagonal
coupling block.  It is deliberately independent of the physical model.
-/

set_option autoImplicit false

namespace RouteBOriginQuadratic

abbrev Vec (n : ℕ) := Fin n → ℝ
abbrev Mat (n : ℕ) := Matrix (Fin n) (Fin n) ℝ

def Symmetric {n : ℕ} (N : Mat n) : Prop :=
  ∀ i j, N i j = N j i

def qform {n : ℕ} (N : Mat n) (x : Vec n) : ℝ :=
  ∑ i, x i * ∑ j, N i j * x j

def normSq {n : ℕ} (x : Vec n) : ℝ :=
  ∑ i, (x i) ^ 2

def QuadNonnegative {n : ℕ} (N : Mat n) : Prop :=
  ∀ x, 0 ≤ qform N x

def QuadNonpositive {n : ℕ} (N : Mat n) : Prop :=
  ∀ x, qform N x ≤ 0

def OriginQuadraticLittleO {n : ℕ} (N : Mat n) : Prop :=
  ∀ x ε, 0 < ε → qform N x ≤ ε * normSq x

def NegatedQuadraticPlusQuartic {n : ℕ} (N : Mat n)
    (quartic : Vec n → ℝ) : Prop :=
  ∀ x ε, 0 < ε → 0 ≤ -qform N x + ε * quartic x

theorem normSq_nonneg {n : ℕ} (x : Vec n) : 0 ≤ normSq x := by
  exact Finset.sum_nonneg (fun i _ => sq_nonneg (x i))

theorem negSemidefinite_of_originQuadraticLittleO {n : ℕ} (N : Mat n)
    (_hN : Symmetric N) (hsmall : OriginQuadraticLittleO N) :
    QuadNonpositive N := by
  intro x
  by_cases hx : normSq x = 0
  · simpa [hx] using hsmall x 1 (by norm_num)
  · have hnorm : 0 < normSq x :=
      lt_of_le_of_ne (normSq_nonneg x) (Ne.symm hx)
    by_contra hpositive
    have hq : 0 < qform N x := lt_of_not_ge hpositive
    let ε : ℝ := qform N x / (2 * normSq x)
    have hε : 0 < ε := by
      dsimp [ε]
      positivity
    have hbound := hsmall x ε hε
    have hcancel : ε * normSq x = qform N x / 2 := by
      dsimp [ε]
      field_simp [hx]
    rw [hcancel] at hbound
    linarith

theorem negSemidefinite_of_negatedQuadraticPlusQuartic {n : ℕ} (N : Mat n)
    (_hN : Symmetric N) (quartic : Vec n → ℝ)
    (hpoly : NegatedQuadraticPlusQuartic N quartic) :
    QuadNonpositive N := by
  intro x
  by_contra hpositive
  have hq : 0 < qform N x := lt_of_not_ge hpositive
  let c : ℝ := |quartic x| + 1
  have hc : 0 < c := by
    dsimp [c]
    linarith [abs_nonneg (quartic x)]
  let ε : ℝ := qform N x / (2 * c)
  have hε : 0 < ε := by
    dsimp [ε]
    positivity
  have hquartic : quartic x ≤ |quartic x| := le_abs_self (quartic x)
  have hcap : |quartic x| ≤ c := by
    dsimp [c]
    linarith [abs_nonneg (quartic x)]
  have hprod₁ : ε * quartic x ≤ ε * |quartic x| :=
    mul_le_mul_of_nonneg_left hquartic (le_of_lt hε)
  have hprod₂ : ε * |quartic x| ≤ ε * c :=
    mul_le_mul_of_nonneg_left hcap (le_of_lt hε)
  have hcancel : ε * c = qform N x / 2 := by
    dsimp [ε]
    field_simp [ne_of_gt hc]
  have hsmall : 0 ≤ -qform N x + ε * quartic x := hpoly x ε hε
  have hupper : ε * quartic x ≤ qform N x / 2 := by
    calc
      ε * quartic x ≤ ε * |quartic x| := hprod₁
      _ ≤ ε * c := hprod₂
      _ = qform N x / 2 := hcancel
  linarith

def negMat {n : ℕ} (N : Mat n) : Mat n :=
  fun i j => -N i j

def vPlus : Vec 2 := ![1, 1]

def vMinus : Vec 2 := ![1, -1]

theorem qform_neg {n : ℕ} (N : Mat n) (x : Vec n) :
    qform (negMat N) x = -qform N x := by
  simp [qform, negMat, Finset.mul_sum, Finset.sum_neg_distrib]

theorem qform_vPlus_zero_diag {B : Mat 2} (h00 : B 0 0 = 0)
    (h11 : B 1 1 = 0) :
    qform B vPlus = B 0 1 + B 1 0 := by
  simp [qform, vPlus, Fin.sum_univ_succ, h00, h11]

theorem qform_vMinus_zero_diag {B : Mat 2} (h00 : B 0 0 = 0)
    (h11 : B 1 1 = 0) :
    qform B vMinus = -(B 0 1 + B 1 0) := by
  simp [qform, vMinus, Fin.sum_univ_succ, h00, h11]
  ring

theorem neg_not_quadNonnegative_zero_diagonal_offdiag {B : Mat 2}
    (hB : Symmetric B) (h00 : B 0 0 = 0) (h11 : B 1 1 = 0)
    (hoff : B 0 1 ≠ 0) :
    ¬ QuadNonnegative (negMat B) := by
  intro hnonneg
  have hp := hnonneg vPlus
  have hm := hnonneg vMinus
  rw [qform_neg, qform_vPlus_zero_diag h00 h11] at hp
  rw [qform_neg, qform_vMinus_zero_diag h00 h11] at hm
  have hsym : B 1 0 = B 0 1 := hB 1 0
  rw [hsym] at hp hm
  have : B 0 1 = 0 := by linarith
  exact hoff this

theorem neg_not_quadNonnegative_q6_v6_block {b : ℝ} (hb : b ≠ 0) :
    ¬ QuadNonnegative (negMat (fun i j : Fin 2 =>
      if i = j then 0 else b)) := by
  apply neg_not_quadNonnegative_zero_diagonal_offdiag
  · intro i j
    fin_cases i <;> fin_cases j <;> simp
  · simp
  · simp
  · simpa using hb

end RouteBOriginQuadratic

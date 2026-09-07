import NEW_P4_032_QuadraticLoad

/-!
UNCOMPILED source-independent entrywise-to-quadratic upper-bound skeleton.
No PSD, symmetry, numerical eigenvalue, deployed source or coverage premise
is inferred. No Lean/Lake run. The output plugs into the existing load seam;
this file does not repeat residual_load_cap or any defect triangle inequality.
-/

set_option autoImplicit false

namespace RouteBP4032EntrywiseQuadratic

open scoped BigOperators
open RouteBP4032BlockDefects
open RouteBP4032DefectNormBudget
open RouteBP4032QuadraticLoad

noncomputable section

/-- Explicit Euclidean identification, not the norm of the default Pi space. -/
theorem norm2_sq_coordinates (r : BVec) :
    (norm2 r)^2 = (r 0)^2 + (r 1)^2 := by
  simpa [norm2, Fin.sum_univ_succ, PiLp.toLp_apply] using
    EuclideanSpace.real_norm_sq_eq (WithLp.toLp 2 r : EuclideanSpace ℝ (Fin 2))

theorem entry_term_upper (x y sij aij : ℝ) (h : |sij| ≤ aij) :
    x * sij * y ≤ aij * |x| * |y| := by
  calc
    x * sij * y ≤ |x * sij * y| := le_abs_self _
    _ = |sij| * (|x| * |y|) := by simp only [abs_mul]; ring
    _ ≤ aij * (|x| * |y|) :=
      mul_le_mul_of_nonneg_right h (mul_nonneg (abs_nonneg _) (abs_nonneg _))
    _ = aij * |x| * |y| := by ring

theorem diagonal_term_upper (x sii aii : ℝ) (h : |sii| ≤ aii) :
    x * sii * x ≤ aii * x^2 := by
  calc
    x * sii * x = sii * x^2 := by ring
    _ ≤ aii * x^2 := mul_le_mul_of_nonneg_right ((le_abs_self sii).trans h) (sq_nonneg x)

/-- The ordered off-diagonal bounds are both retained, even for nonsymmetric S. -/
theorem quadratic_absolute_majorant (S A : BB) (r : BVec)
    (hEntries : ∀ i j, |S i j| ≤ A i j) :
    quadratic S r ≤ A 0 0 * (r 0)^2 +
      (A 0 1 + A 1 0) * |r 0| * |r 1| + A 1 1 * (r 1)^2 := by
  have h00 := diagonal_term_upper (r 0) (S 0 0) (A 0 0) (hEntries 0 0)
  have h11 := diagonal_term_upper (r 1) (S 1 1) (A 1 1) (hEntries 1 1)
  have h01 := entry_term_upper (r 0) (r 1) (S 0 1) (A 0 1) (hEntries 0 1)
  have h10 := entry_term_upper (r 1) (r 0) (S 1 0) (A 1 0) (hEntries 1 0)
  simp [quadratic, Fin.sum_univ_succ]
  <;> nlinarith

/-- Row sums of sym(A); no symmetry of either S or A is assumed. -/
def rowBudget (A : BB) (i : Fin 2) : ℝ := A i i + (A 0 1 + A 1 0) / 2

theorem rowBudget_nonnegative (A : BB) (hA : ∀ i j, 0 ≤ A i j) (i : Fin 2) :
    0 ≤ rowBudget A i :=
  add_nonneg (hA i i) (div_nonneg (add_nonneg (hA 0 1) (hA 1 0)) (by norm_num))

/-- Young's scalar inequality charges half of the off-diagonal sum to each
coordinate square. This is an upper bound, never a positivity claim for S. -/
theorem quadratic_row_budget (S A : BB) (r : BVec)
    (hA : ∀ i j, 0 ≤ A i j) (hEntries : ∀ i j, |S i j| ≤ A i j) :
    quadratic S r ≤ rowBudget A 0 * (r 0)^2 + rowBudget A 1 * (r 1)^2 := by
  have hmajor := quadratic_absolute_majorant S A r hEntries
  have hYoung : 2 * |r 0| * |r 1| ≤ (r 0)^2 + (r 1)^2 := by
    nlinarith [sq_nonneg (|r 0| - |r 1|), sq_abs (r 0), sq_abs (r 1)]
  have hcross := mul_le_mul_of_nonneg_left hYoung (add_nonneg (hA 0 1) (hA 1 0))
  unfold rowBudget
  nlinarith

/-- Proof-valued upper bound for the EXISTING QuadraticLoad consumer.
Nonnegativity of the exported k is packaged explicitly by the constructors below. -/
theorem upper_of_row_budget (S A : BB) (k : ℝ)
    (hA : ∀ i j, 0 ≤ A i j) (hEntries : ∀ i j, |S i j| ≤ A i j)
    (h0 : rowBudget A 0 ≤ k) (h1 : rowBudget A 1 ≤ k) : QuadraticUpperBound S k where
  bound r := by
    calc
      quadratic S r ≤ rowBudget A 0 * (r 0)^2 + rowBudget A 1 * (r 1)^2 :=
        quadratic_row_budget S A r hA hEntries
      _ ≤ k * (r 0)^2 + k * (r 1)^2 :=
        add_le_add (mul_le_mul_of_nonneg_right h0 (sq_nonneg _))
          (mul_le_mul_of_nonneg_right h1 (sq_nonneg _))
      _ = k * (norm2 r)^2 := by rw [norm2_sq_coordinates]; ring

/-- Export both pieces required downstream: k>=0 and the matching upper proof.
There is deliberately no PSD or source-binding field. -/
structure NonnegativeUpperBound (S : BB) where
  k : ℝ
  nonnegative : 0 ≤ k
  upper : QuadraticUpperBound S k

def ofEntryBounds (S A : BB) (k : ℝ) (hk : 0 ≤ k)
    (hA : ∀ i j, 0 ≤ A i j) (hEntries : ∀ i j, |S i j| ≤ A i j)
    (h0 : rowBudget A 0 ≤ k) (h1 : rowBudget A 1 ≤ k) : NonnegativeUpperBound S where
  k := k
  nonnegative := hk
  upper := upper_of_row_budget S A k hA hEntries h0 h1

/-- Explicit anisotropic coefficient: max of the two symmetrized row budgets.
This finite formula does not call an eigensolver or assert sharpness. -/
def ofEntryMax (S A : BB) (hA : ∀ i j, 0 ≤ A i j)
    (hEntries : ∀ i j, |S i j| ≤ A i j) : NonnegativeUpperBound S :=
  ofEntryBounds S A (max (rowBudget A 0) (rowBudget A 1))
    ((rowBudget_nonnegative A hA 0).trans (le_max_left _ _)) hA hEntries
    (le_max_left _ _) (le_max_right _ _)

/-- Uniform |Sij|<=s gives k=2*s in dimension TWO, not a hidden norm switch. -/
def ofUniformBound (S : BB) (s : ℝ) (hs : 0 ≤ s)
    (hEntries : ∀ i j, |S i j| ≤ s) : NonnegativeUpperBound S :=
  ofEntryBounds S (fun _ _ => s) (2 * s) (mul_nonneg (by norm_num) hs)
    (fun _ _ => hs) hEntries (by simp [rowBudget]; linarith)
    (by simp [rowBudget]; linarith)

end

-- Future audit commands only; NOT executed in this round.
#print axioms norm2_sq_coordinates
#print axioms quadratic_absolute_majorant
#print axioms quadratic_row_budget
#print axioms upper_of_row_budget
#print axioms ofEntryBounds
#print axioms ofEntryMax
#print axioms ofUniformBound

end RouteBP4032EntrywiseQuadratic

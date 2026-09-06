import SignedGap

set_option autoImplicit false
open scoped BigOperators

namespace RouteBSignedGap
noncomputable section

def transpose {n : ℕ} (M : Mat n) : Mat n := fun i j => M j i
def mm {n : ℕ} (M N : Mat n) : Mat n := fun i j => ∑ k, M i k * N k j

theorem dot_comm {n : ℕ} (x y : Vec n) : dot x y = dot y x := by
  simp only [dot, mul_comm]

theorem dot_transpose {n : ℕ} (Z : Mat n) (x y : Vec n) :
    dot x (mv (transpose Z) y) = dot (mv Z x) y := by
  simp only [dot, mv, transpose, Finset.mul_sum, Finset.sum_mul]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  ring

theorem mv_mm {n : ℕ} (M N : Mat n) (x : Vec n) :
    mv (mm M N) x = mv M (mv N x) := by
  funext i
  simp only [mv, mm, Finset.sum_mul, Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro j _
  apply Finset.sum_congr rfl
  intro k _
  ring

/-- A genuine (n+1)-square matrix; n=6 gives the requested 7x7 block. -/
def block {n : ℕ} (top : ℝ) (off : Vec n) (bottom : Mat n) : Mat (n+1) :=
  Fin.cons (Fin.cons top off) (fun i => Fin.cons (off i) (bottom i))

theorem quad_block {n : ℕ} (top : ℝ) (off : Vec n) (bottom : Mat n) (x : Vec n) :
    quad (block top off bottom) (Fin.cons 1 x) =
      top + 2 * dot off x + quad bottom x := by
  simp only [quad, dot, mv, block, Fin.sum_univ_succ, Fin.cons_zero, Fin.cons_succ,
    one_mul, mul_one, mul_add, Finset.sum_add_distrib]
  have hcomm : (∑ i, x i * off i) = ∑ i, off i * x i := by
    apply Finset.sum_congr rfl
    intro i _
    ring
  rw [hcomm]
  ring

def multiplierBottom {n : ℕ} (M L Z : Mat n) : Mat n := fun i j =>
  mm (transpose Z) M i j + mm M Z i j - L i j

def affineMatrix {n : ℕ} (M L Z : Mat n) (g r z : Vec n) (b d : ℝ) : Mat (n+1) :=
  block (b - d - 2 * dot z r)
    (fun i => -(g i + mv (transpose Z) r i - mv M z i))
    (multiplierBottom M L Z)

/-- Explicit finite-vector nonnegativity; it asserts no source-cell certificate. -/
def QuadNonnegative {n : ℕ} (A : Mat n) : Prop := ∀ x, 0 ≤ quad A x

theorem quad_multiplierBottom {n : ℕ} (M L Z : Mat n) (x : Vec n)
    (hM : Symmetric M) :
    quad (multiplierBottom M L Z) x =
      2 * dot (mv Z x) (mv M x) - quad L x := by
  have hexpand : quad (multiplierBottom M L Z) x =
      dot x (mv (mm (transpose Z) M) x) + dot x (mv (mm M Z) x) - quad L x := by
    simp only [quad, dot, mv, multiplierBottom, add_mul, sub_mul,
      Finset.sum_add_distrib, Finset.sum_sub_distrib, mul_add, mul_sub]
  rw [hexpand, mv_mm, mv_mm, dot_transpose, dot_mv_symm M x (mv Z x) hM]
  ring

/-- Exact affine residual expansion, before imposing M delta = r. -/
theorem affine_quadratic_expansion {n : ℕ} (M L Z : Mat n) (g r z delta : Vec n)
    (b d : ℝ) (hM : Symmetric M) :
    quad (affineMatrix M L Z g r z b d) (Fin.cons 1 delta) =
      b - (d + 2 * dot g delta) - quad L delta +
        2 * dot (fun i => z i + mv Z delta i) (fun i => mv M delta i - r i) := by
  rw [affineMatrix, quad_block, quad_multiplierBottom M L Z delta hM]
  have hoff : dot (fun i => -(g i + mv (transpose Z) r i - mv M z i)) delta =
      -dot g delta - dot (mv Z delta) r + dot z (mv M delta) := by
    have he : dot (fun i => -(g i + mv (transpose Z) r i - mv M z i)) delta =
        -dot g delta - dot (mv (transpose Z) r) delta + dot (mv M z) delta := by
      simp only [dot, neg_mul, add_mul, sub_mul, Finset.sum_neg_distrib,
        Finset.sum_add_distrib, Finset.sum_sub_distrib]
      ring
    rw [he, dot_comm (mv (transpose Z) r) delta, dot_transpose,
      dot_comm (mv M z) delta, dot_mv_symm M delta z hM]
  rw [hoff]
  have hres : dot (fun i => z i + mv Z delta i) (fun i => mv M delta i - r i) =
      dot z (mv M delta) - dot z r + dot (mv Z delta) (mv M delta) -
        dot (mv Z delta) r := by
    simp only [dot, add_mul, mul_sub, Finset.sum_add_distrib, Finset.sum_sub_distrib]
    ring
  rw [hres]
  ring

/-- Scalar finite-sum cancellation for z+Z delta; no inverse or positivity of storage. -/
theorem affine_residual_cancellation {n : ℕ} (M Z : Mat n) (r z delta : Vec n)
    (balance : ∀ i, mv M delta i = r i) :
    dot (fun i => z i + mv Z delta i) (fun i => mv M delta i - r i) = 0 := by
  simp only [balance, sub_self, dot, mul_zero, Finset.sum_const_zero]

/-- Only nonnegativity at (1,delta) is needed; all-vector PSD is a sufficient premise. -/
theorem affine_dissipation_of_test_vector {n : ℕ} (M L Z : Mat n)
    (g r z delta : Vec n) (b d : ℝ) (hM : Symmetric M)
    (balance : ∀ i, mv M delta i = r i)
    (hQ : 0 ≤ quad (affineMatrix M L Z g r z b d) (Fin.cons 1 delta)) :
    quad L delta + (d + 2 * dot g delta) ≤ b := by
  rw [affine_quadratic_expansion M L Z g r z delta b d hM,
    affine_residual_cancellation M Z r z delta balance] at hQ
  linarith

theorem affine_dissipation {n : ℕ} (M L Z : Mat n)
    (g r z delta : Vec n) (b d : ℝ) (hM : Symmetric M)
    (balance : ∀ i, mv M delta i = r i)
    (hQ : QuadNonnegative (affineMatrix M L Z g r z b d)) :
    quad L delta + (d + 2 * dot g delta) ≤ b :=
  affine_dissipation_of_test_vector M L Z g r z delta b d hM balance (hQ _)

/-- Original homogeneous S6 is exactly the affine construction with z=0. -/
theorem homogeneous_matrix {n : ℕ} (M L Z : Mat n) (g r : Vec n) (b d : ℝ) :
    affineMatrix M L Z g r (fun _ => 0) b d =
      block (b-d) (fun i => -(g i + mv (transpose Z) r i)) (multiplierBottom M L Z) := by
  simp [affineMatrix, dot, mv]

theorem affine_dissipation_fin6 (M L Z : Mat 6) (g r z delta : Vec 6)
    (b d : ℝ) (hM : Symmetric M) (balance : ∀ i, mv M delta i = r i)
    (hQ : ∀ x : Vec 7, 0 ≤ quad (affineMatrix M L Z g r z b d) x) :
    quad L delta + (d + 2 * dot g delta) ≤ b :=
  affine_dissipation M L Z g r z delta b d hM balance hQ

#print axioms quad_block
#print axioms affine_quadratic_expansion
#print axioms affine_residual_cancellation
#print axioms affine_dissipation
#print axioms affine_dissipation_fin6
#print axioms homogeneous_matrix

end
end RouteBSignedGap

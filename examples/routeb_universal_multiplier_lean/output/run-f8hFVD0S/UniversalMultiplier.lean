import ResidualMultiplier

set_option autoImplicit false
open scoped BigOperators

namespace RouteBUniversalMultiplier
open RouteBSignedGap
noncomputable section

def identityMat (n : ℕ) : Mat n := fun i j => if i = j then 1 else 0
def D {n : ℕ} (M L : Mat n) : Mat n := fun i j => 2 * M i j - L i j
def Dominates {n : ℕ} (M L : Mat n) : Prop := ∀ x, quad L x ≤ quad M x
def CoerciveAt {n : ℕ} (L : Mat n) (c : ℝ) : Prop :=
  ∀ x, c * dot x x ≤ quad L x
def margin {n : ℕ} (L : Mat n) (g delta : Vec n) (b d : ℝ) : ℝ :=
  b - d - 2 * dot g delta - quad L delta

@[simp] theorem mv_identity {n : ℕ} (x : Vec n) : mv (identityMat n) x = x := by
  ext i
  simp [mv, identityMat]

@[simp] theorem transpose_identity (n : ℕ) : transpose (identityMat n) = identityMat n := by
  ext i j
  simp [transpose, identityMat, eq_comm]

theorem bottom_identity {n : ℕ} (M L : Mat n) :
    multiplierBottom M L (identityMat n) = D M L := by
  ext i j
  simp [multiplierBottom, mm, identityMat, transpose, D]
  ring

theorem D_symmetric {n : ℕ} (M L : Mat n) (hM : Symmetric M) (hL : Symmetric L) :
    Symmetric (D M L) := by
  intro i j
  simp only [D, hM i j, hL i j]

theorem mv_D {n : ℕ} (M L : Mat n) (x : Vec n) :
    mv (D M L) x = fun i => 2 * mv M x i - mv L x i := by
  ext i
  simp only [mv, D, sub_mul, mul_assoc, Finset.sum_sub_distrib, Finset.mul_sum]

theorem quad_D {n : ℕ} (M L : Mat n) (x : Vec n) :
    quad (D M L) x = 2 * quad M x - quad L x := by
  simp only [quad, mv_D, dot, mul_sub, Finset.sum_sub_distrib, Finset.mul_sum]
  congr 1
  apply Finset.sum_congr rfl
  intro i _
  ring

/-- The only mass-order hypothesis is the actual source-bound M >= L. -/
theorem D_dominates_L {n : ℕ} (M L : Mat n) (source_mass_lower_bound : Dominates M L) :
    Dominates (D M L) L := by
  intro x
  rw [quad_D]
  linarith [source_mass_lower_bound x]

theorem D_nonnegative {n : ℕ} (M L : Mat n)
    (source_mass_lower_bound : Dominates M L) (hL : QuadNonnegative L) :
    QuadNonnegative (D M L) :=
  fun x => le_trans (hL x) (D_dominates_L M L source_mass_lower_bound x)

/-- Quantitative coercivity is inherited with the SAME constant. -/
theorem finite_quadratic_coercivity {n : ℕ} (M L : Mat n) (c : ℝ)
    (source_mass_lower_bound : Dominates M L) (hL : CoerciveAt L c) :
    CoerciveAt (D M L) c :=
  fun x => le_trans (hL x) (D_dominates_L M L source_mass_lower_bound x)

theorem global_coercivity {α : Type*} {n : ℕ} (M : α → Mat n) (L : Mat n) (c : ℝ)
    (source_mass_lower_bound : ∀ q, Dominates (M q) L) (hL : CoerciveAt L c) :
    ∀ q, CoerciveAt (D (M q) L) c :=
  fun q => finite_quadratic_coercivity (M q) L c (source_mass_lower_bound q) hL

theorem dot_sub_left {n : ℕ} (x y z : Vec n) :
    dot (fun i => x i - y i) z = dot x z - dot y z := by
  simp [dot, sub_mul, Finset.sum_sub_distrib]

theorem dot_sub_right {n : ℕ} (x y z : Vec n) :
    dot x (fun i => y i - z i) = dot x y - dot x z := by
  simp [dot, mul_sub, Finset.sum_sub_distrib]

theorem dot_scale_left {n : ℕ} (s : ℝ) (x y : Vec n) :
    dot (fun i => s * x i) y = s * dot x y := by
  simp [dot, mul_assoc, Finset.mul_sum]

theorem dot_scale_right {n : ℕ} (s : ℝ) (x y : Vec n) :
    dot x (fun i => s * y i) = s * dot x y := by
  rw [dot_comm, dot_scale_left, dot_comm y x]

theorem mv_shift {n : ℕ} (A : Mat n) (v delta : Vec n) (s : ℝ) :
    mv A (fun i => v i - s * delta i) = fun i => mv A v i - s * mv A delta i := by
  ext i
  simp only [mv, mul_sub, Finset.sum_sub_distrib, Finset.mul_sum]
  congr 1
  apply Finset.sum_congr rfl
  intro j _
  ring

/-- Expansion of the actual finite quadratic sum using matrix symmetry. -/
theorem quad_shift {n : ℕ} (A : Mat n) (v delta : Vec n) (s : ℝ)
    (hA : Symmetric A) :
    quad A (fun i => v i - s * delta i) =
      quad A v - 2 * s * dot delta (mv A v) + s^2 * quad A delta := by
  simp only [quad, mv_shift, dot_sub_left, dot_sub_right,
    dot_scale_left, dot_scale_right]
  rw [dot_mv_symm A v delta hA]
  ring

/-- Homogeneous finite-vector identity, including s=0. -/
theorem quad_block_homogeneous {n : ℕ} (top : ℝ) (off : Vec n) (bottom : Mat n)
    (s : ℝ) (v : Vec n) :
    quad (block top off bottom) (Fin.cons s v) =
      top * s^2 + 2 * s * dot off v + quad bottom v := by
  simp only [quad, dot, mv, block, Fin.sum_univ_succ, Fin.cons_zero, Fin.cons_succ,
    mul_add, Finset.sum_add_distrib]
  have hc : (∑ i, v i * (off i * s)) = s * ∑ i, off i * v i := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i _
    ring
  rw [hc]
  ring

theorem optimal_off {n : ℕ} (M L : Mat n) (g r z delta : Vec n)
    (balance : ∀ i, mv M delta i = r i)
    (optimal : ∀ i, mv M z i = g i - r i + mv L delta i) :
    (fun i => -(g i + mv (transpose (identityMat n)) r i - mv M z i)) =
      fun i => -(mv (D M L) delta i) := by
  simp only [transpose_identity, mv_identity, mv_D]
  ext i
  rw [balance i, optimal i]
  ring

theorem optimal_top {n : ℕ} (M L : Mat n) (g r z delta : Vec n) (b d : ℝ)
    (hM : Symmetric M) (balance : ∀ i, mv M delta i = r i)
    (optimal : ∀ i, mv M z i = g i - r i + mv L delta i) :
    b - d - 2 * dot z r = margin L g delta b d + quad (D M L) delta := by
  have hb : mv M delta = r := funext balance
  have hz : mv M z = fun i => g i - r i + mv L delta i := funext optimal
  have hzr : dot z r = dot delta g - dot delta r + quad L delta := by
    rw [← hb, dot_mv_symm M z delta hM, hz]
    simp only [dot, quad, mul_add, mul_sub,
      Finset.sum_add_distrib, Finset.sum_sub_distrib]
    rw [hb]
  rw [hzr, quad_D, margin, dot_comm g delta]
  have hm : quad M delta = dot delta r := by rw [quad, hb]
  rw [hm]
  ring

/-- Derives the block entries; the congruence is a conclusion, never a premise. -/
theorem optimal_matrix {n : ℕ} (M L : Mat n) (g r z delta : Vec n) (b d : ℝ)
    (hM : Symmetric M) (balance : ∀ i, mv M delta i = r i)
    (optimal : ∀ i, mv M z i = g i - r i + mv L delta i) :
    affineMatrix M L (identityMat n) g r z b d =
      block (margin L g delta b d + quad (D M L) delta)
        (fun i => -(mv (D M L) delta i)) (D M L) := by
  rw [affineMatrix, optimal_top M L g r z delta b d hM balance optimal,
    optimal_off M L g r z delta balance optimal, bottom_identity]

theorem finite_vector_congruence {n : ℕ} (M L : Mat n) (g r z delta : Vec n)
    (b d s : ℝ) (v : Vec n) (hM : Symmetric M) (hL : Symmetric L)
    (balance : ∀ i, mv M delta i = r i)
    (optimal : ∀ i, mv M z i = g i - r i + mv L delta i) :
    quad (affineMatrix M L (identityMat n) g r z b d) (Fin.cons s v) =
      margin L g delta b d * s^2 + quad (D M L) (fun i => v i - s * delta i) := by
  rw [optimal_matrix M L g r z delta b d hM balance optimal, quad_block_homogeneous,
    quad_shift (D M L) v delta s (D_symmetric M L hM hL)]
  have hoff : dot (fun i => -(mv (D M L) delta i)) v = -dot delta (mv (D M L) v) := by
    rw [show (fun i => -(mv (D M L) delta i)) =
      (fun i => (-1 : ℝ) * mv (D M L) delta i) by ext i; ring]
    rw [dot_scale_left, dot_comm (mv (D M L) delta) v,
      dot_mv_symm (D M L) v delta (D_symmetric M L hM hL)]
    ring
  rw [hoff]
  ring

theorem psd_iff_margin {n : ℕ} (M L : Mat n) (g r z delta : Vec n) (b d : ℝ)
    (hM : Symmetric M) (hL : Symmetric L) (hD : QuadNonnegative (D M L))
    (balance : ∀ i, mv M delta i = r i)
    (optimal : ∀ i, mv M z i = g i - r i + mv L delta i) :
    QuadNonnegative (affineMatrix M L (identityMat n) g r z b d) ↔
      0 ≤ margin L g delta b d := by
  constructor
  · intro h
    have hh := h (Fin.cons 1 delta)
    rw [finite_vector_congruence M L g r z delta b d 1 delta hM hL balance optimal] at hh
    simpa [quad, dot, mv] using hh
  · intro hm x
    have hx : Fin.cons (x 0) (fun i => x i.succ) = x := by
      ext i
      exact Fin.cases rfl (fun _ => rfl) i
    rw [← hx, finite_vector_congruence M L g r z delta b d (x 0)
      (fun i => x i.succ) hM hL balance optimal]
    exact add_nonneg (mul_nonneg hm (sq_nonneg _)) (hD _)

/-- This formula uses an actual right inverse of M, not a frozen M0 inverse. -/
def optimalZ {n : ℕ} (R L : Mat n) (g delta : Vec n) : Vec n :=
  fun i => mv R g i - delta i + mv R (mv L delta) i

theorem optimalZ_balance {n : ℕ} (M L R : Mat n) (g r delta : Vec n)
    (right_inverse : ∀ x, mv M (mv R x) = x)
    (balance : ∀ i, mv M delta i = r i) :
    ∀ i, mv M (optimalZ R L g delta) i = g i - r i + mv L delta i := by
  intro i
  simp only [mv, optimalZ, mul_add, mul_sub, Finset.sum_add_distrib,
    Finset.sum_sub_distrib]
  change mv M (mv R g) i - mv M delta i + mv M (mv R (mv L delta)) i = _
  rw [right_inverse, right_inverse, balance]
  rfl

/-- Constructive losslessness for the fixed matrix multiplier Z=I. -/
theorem CONSTRUCTIVELOSSLESS {n : ℕ} (M L R : Mat n) (g r delta : Vec n) (b d : ℝ)
    (hM : Symmetric M) (hL : Symmetric L)
    (source_mass_lower_bound : Dominates M L) (L_nonnegative : QuadNonnegative L)
    (right_inverse : ∀ x, mv M (mv R x) = x)
    (balance : ∀ i, mv M delta i = r i) :
    QuadNonnegative (affineMatrix M L (identityMat n) g r (optimalZ R L g delta) b d) ↔
      quad L delta + (d + 2 * dot g delta) ≤ b := by
  rw [psd_iff_margin M L g r (optimalZ R L g delta) delta b d hM hL
    (D_nonnegative M L source_mass_lower_bound L_nonnegative) balance
    (optimalZ_balance M L R g r delta right_inverse balance)]
  unfold margin
  constructor <;> intro h <;> linarith

theorem affine7x7_lossless (M L : Mat 6) (g r z delta : Vec 6) (b d : ℝ)
    (hM : Symmetric M) (hL : Symmetric L)
    (source_mass_lower_bound : Dominates M L) (L_nonnegative : QuadNonnegative L)
    (balance : ∀ i, mv M delta i = r i)
    (optimal : ∀ i, mv M z i = g i - r i + mv L delta i) :
    (∀ x : Vec 7, 0 ≤ quad (affineMatrix M L (identityMat 6) g r z b d) x) ↔
      0 ≤ margin L g delta b d :=
  psd_iff_margin M L g r z delta b d hM hL
    (D_nonnegative M L source_mass_lower_bound L_nonnegative) balance optimal

def difference {n : ℕ} (A L : Mat n) : Mat n := fun i j => A i j - L i j

theorem quad_difference {n : ℕ} (A L : Mat n) (y : Vec n) :
    quad (difference A L) y = quad A y - quad L y := by
  simp only [quad, dot, mv, difference, sub_mul, mul_sub, Finset.sum_sub_distrib]

/-- Exact finite SOS completion of the centered matrix K. Only L is inverted. -/
theorem centered_dual_sos {n : ℕ} (A L Q : Mat n) (e y : Vec n) (m s : ℝ)
    (hL : Symmetric L) (dual_solve : mv L (mv Q e) = e) :
    quad (block m (fun i => -e i) A) (Fin.cons s y) =
      quad (difference A L) y + quad L (fun i => y i - s * mv Q e i) +
        s^2 * (m - dot e (mv Q e)) := by
  rw [quad_block_homogeneous, quad_difference, quad_shift L y (mv Q e) s hL]
  have hc : dot (mv Q e) (mv L y) = dot e y := by
    rw [dot_mv_symm L (mv Q e) y hL, dual_solve, dot_comm]
  have hq : quad L (mv Q e) = dot e (mv Q e) := by
    rw [quad, dual_solve, dot_comm]
  have hn : dot (fun i => -e i) y = -dot e y := by
    simp [dot, neg_mul, Finset.sum_neg_distrib]
  rw [hc, hq, hn]
  ring

/-- A single signed scalar source condition certifies ALL vectors of K. -/
theorem centered_dual_bound {n : ℕ} (A L Q : Mat n) (e : Vec n) (m : ℝ)
    (hL : Symmetric L) (hAL : Dominates A L) (hLpos : QuadNonnegative L)
    (dual_solve : mv L (mv Q e) = e) (scalar_source_condition : dot e (mv Q e) ≤ m) :
    QuadNonnegative (block m (fun i => -e i) A) := by
  intro x
  have hx : Fin.cons (x 0) (fun i => x i.succ) = x := by
    ext i
    exact Fin.cases rfl (fun _ => rfl) i
  rw [← hx, centered_dual_sos A L Q e (fun i => x i.succ) m (x 0) hL dual_solve]
  have hd : 0 ≤ quad (difference A L) (fun i => x i.succ) := by
    rw [quad_difference]
    exact sub_nonneg.mpr (hAL _)
  exact add_nonneg (add_nonneg hd (hLpos _))
    (mul_nonneg (sq_nonneg _) (sub_nonneg.mpr scalar_source_condition))

theorem fixed_identity_centered_dual_bound {n : ℕ} (M L Q : Mat n) (e : Vec n) (m : ℝ)
    (hL : Symmetric L) (source_mass_lower_bound : Dominates M L)
    (hLpos : QuadNonnegative L) (dual_solve : mv L (mv Q e) = e)
    (scalar_source_condition : dot e (mv Q e) ≤ m) :
    QuadNonnegative (block m (fun i => -e i) (D M L)) :=
  centered_dual_bound (D M L) L Q e m hL (D_dominates_L M L source_mass_lower_bound)
    hLpos dual_solve scalar_source_condition

#print axioms bottom_identity
#print axioms D_dominates_L
#print axioms finite_quadratic_coercivity
#print axioms global_coercivity
#print axioms quad_block_homogeneous
#print axioms optimal_matrix
#print axioms finite_vector_congruence
#print axioms psd_iff_margin
#print axioms optimalZ_balance
#print axioms CONSTRUCTIVELOSSLESS
#print axioms affine7x7_lossless
#print axioms centered_dual_sos
#print axioms centered_dual_bound
#print axioms fixed_identity_centered_dual_bound

end
end RouteBUniversalMultiplier

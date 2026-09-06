import PotentialSlice

namespace RouteBBlockPotential

noncomputable def factor (q : Fin 6 → ℝ) : ℝ :=
  (10791 / 4000 : ℝ) + (762237 / 200000 : ℝ) * Real.cos (q 1) +
  (242307 / 200000 : ℝ) * Real.cos (q 1 + q 2) +
  (20601 / 400000 : ℝ) *
    (Real.cos (q 1 + q 2) * Real.cos (q 4) -
      Real.sin (q 1 + q 2) * Real.cos (q 3) * Real.sin (q 4))

/- Equality to the previously audited 17-row cosine encoding only. -/
set_option maxRecDepth 8192 in
set_option maxHeartbeats 1200000 in
theorem potential_factor (q : Fin 6 → ℝ) :
    RouteBPotentialSlice.potential q = factor q := by
  norm_num [RouteBPotentialSlice.potential, RouteBPotentialSlice.rows,
    RouteBPotentialSlice.coefficient, RouteBPotentialSlice.phase,
    Fin.sum_univ_six, Fin.sum_univ_succ, Matrix.cons_val_two,
    Matrix.cons_val_three, Matrix.cons_val_four, Matrix.vecHead, Matrix.vecTail]
  have h3 : Fin.succ (2 : Fin 5) = (3 : Fin 6) := by decide
  have h4 : (Fin.succ (2 : Fin 4)).succ = (4 : Fin 6) := by decide
  simp only [h3, h4]
  simp only [factor, Real.cos_add, Real.sin_add, Real.cos_neg, Real.sin_neg]
  ring

noncomputable def blockPotential (s x y : ℝ) : ℝ :=
  (20601 / 400000 : ℝ) *
    (Real.cos s * (Real.cos y - 1) - Real.sin s * Real.cos x * Real.sin y) +
  (3 / 10 : ℝ) * x ^ 2 + (1 / 4 : ℝ) * y ^ 2

theorem centered_block_identity (r a b x y z : ℝ) :
    RouteBPotentialSlice.potential ![r, a, b, x, y, z] -
      RouteBPotentialSlice.potential ![r, a, b, 0, 0, z] +
      (3 / 10 : ℝ) * x ^ 2 + (1 / 4 : ℝ) * y ^ 2 =
    blockPotential (a + b) x y := by
  rw [potential_factor, potential_factor]
  simp [factor, blockPotential]
  ring

theorem remote_pi_half_slice (t : ℝ) :
    blockPotential (Real.pi / 2) 0 t =
      -(20601 / 400000 : ℝ) * Real.sin t + (1 / 4 : ℝ) * t ^ 2 := by
  simp [blockPotential]

#print axioms potential_factor
#print axioms centered_block_identity
#print axioms remote_pi_half_slice

end RouteBBlockPotential

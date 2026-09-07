import NEW_BODY6_SLICE_AXIS_Core20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_VGRAM_Core20260907

noncomputable section

open NEW_BODY6_SLICE_AXIS_Core20260907

/- UNCOMPILED source-independent cross/Gram leaves. No mass table or CSV import. -/
def crossV (u v : AVec) : AVec :=
  ![u 1 * v 2 - u 2 * v 1,
    u 2 * v 0 - u 0 * v 2,
    u 0 * v 1 - u 1 * v 0]

def displacedVelocity (o p z w : AVec) (h : ℝ) : AVec :=
  crossV z (fun a => p a + h * w a - o a)

theorem displaced_velocity_split_attempt (o p z w : AVec) (h : ℝ) :
    displacedVelocity o p z w h =
      (fun a => crossV z (fun b => p b - o b) a + h * crossV z w a) := by
  funext a
  fin_cases a <;> simp [displacedVelocity, crossV] <;> ring

theorem parallel_lever_zero_attempt (o p z : AVec) (d : ℝ)
    (hp : ∀ a, p a = o a + d * z a) :
    crossV z (fun a => p a - o a) = 0 := by
  funext a
  fin_cases a <;> simp [crossV, hp] <;> ring

theorem displaced_velocity_of_parallel_attempt (o p z w : AVec) (d h : ℝ)
    (hp : ∀ a, p a = o a + d * z a) :
    displacedVelocity o p z w h = fun a => h * crossV z w a := by
  rw [displaced_velocity_split_attempt, parallel_lever_zero_attempt o p z d hp]
  simp

theorem dot_swap_attempt (u v : AVec) : dot3 u v = dot3 v u := by
  unfold dot3
  apply Finset.sum_congr rfl
  intro a _
  exact mul_comm _ _

theorem dot_scaled_attempt (u v : AVec) (h : ℝ) :
    dot3 (fun a => h * u a) (fun a => h * v a) = h ^ 2 * dot3 u v := by
  norm_num [dot3, Fin.sum_univ_succ] <;> ring

/- General Lagrange identity, with distinct lever arms p/r if needed later. -/
theorem cross_gram_attempt (u p v r : AVec) :
    dot3 (crossV u p) (crossV v r) =
      dot3 u v * dot3 p r - dot3 u r * dot3 p v := by
  norm_num [dot3, crossV, Fin.sum_univ_succ] <;> ring

theorem common_axis_gram_attempt (u v w : AVec) (h : ℝ) :
    dot3 (fun a => h * crossV u w a) (fun a => h * crossV v w a) =
      h ^ 2 * (dot3 u v * dot3 w w - dot3 u w * dot3 v w) := by
  rw [dot_scaled_attempt, cross_gram_attempt]
  rw [dot_swap_attempt w v]

def linearGram5 (v : Fin 5 → AVec) (i j : Fin 5) : ℝ := dot3 (v i) (v j)

theorem linear_gram5_symmetric_attempt (v : Fin 5 → AVec) (i j : Fin 5) :
    linearGram5 v i j = linearGram5 v j i := dot_swap_attempt _ _

end
end NEW_BODY6_SLICE_VGRAM_Core20260907

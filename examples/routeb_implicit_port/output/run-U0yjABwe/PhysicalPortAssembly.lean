import ImplicitPort

open scoped BigOperators
set_option autoImplicit false

namespace RouteBPhysicalPortAssembly

open RouteBImplicitPort
variable {ι : Type*} [Fintype ι]

/- No acceleration variable is discarded: the force link determines it.
   The residual bracket and port bound are DIFFERENT explicit premises. -/
theorem linked_acceleration (I l r m a : ℝ) (hm : m ≠ 0)
    (hlink : m * a = I + r - l) : a = ((I - l) + r) / m := by
  apply (eq_div_iff hm).2
  nlinarith

theorem physical_port_absorption
    (Dcore beta0 s nu lambda rho : ℝ)
    (I rt l a r m B : ι → ℝ)
    (hm : ∀ i, m i ≠ 0)
    (hforce : ∀ i, m i * a i = I i + r i - l i)
    (hs : 0 ≤ s) (hnu : 0 ≤ nu)
    (hport : (∑ i, r i ^ 2) ≤ rho * (∑ i, B i * a i ^ 2))
    (hresidual : (∑ i, l i ^ 2) ≤ beta0 + lambda * (∑ i, a i ^ 2))
    (hh : ∀ i, 0 < H nu (s * lambda / m i ^ 2 + nu * rho * B i / m i ^ 2))
    (hg : ∀ i, 0 < G s nu (s * lambda / m i ^ 2 + nu * rho * B i / m i ^ 2))
    (hreduced : 0 ≤
      (Dcore + (∑ i, (rt i * I i + s * I i ^ 2)) - s * beta0) -
      ∑ i, (-(rt i + 2 * s * I i)) ^ 2 /
        (4 * G s nu (s * lambda / m i ^ 2 + nu * rho * B i / m i ^ 2))) :
    0 ≤ Dcore + ∑ i, rt i * l i := by
  let z : ι → ℝ := fun i => I i - l i
  let k : ι → ℝ := fun i => s * lambda / m i ^ 2 + nu * rho * B i / m i ^ 2
  let b : ι → ℝ := fun i => -(rt i + 2 * s * I i)
  let D0 := Dcore + (∑ i, (rt i * I i + s * I i ^ 2)) - s * beta0
  let Daug := Dcore + (∑ i, rt i * l i) + s * (∑ i, l i ^ 2) -
    s * (beta0 + lambda * (∑ i, a i ^ 2))
  let gap := rho * (∑ i, B i * a i ^ 2) - (∑ i, r i ^ 2)
  have hi (i : ι) := residual_link_channel (I i) (rt i) (l i) (a i)
    (z i) (r i) (m i) s nu lambda rho (B i) (hm i)
    (by dsimp [z]; ring) (linked_acceleration _ _ _ _ _ (hm i) (hforce i))
  have hsum := Finset.sum_congr (s₁ := Finset.univ) rfl (fun i _ => hi i)
  have hidentity : Daug - nu * gap =
      D0 + ∑ i, (s * z i ^ 2 + b i * z i + nu * r i ^ 2 - k i * (z i + r i) ^ 2) := by
    dsimp [Daug, gap, D0, k, b]
    simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib,
      ← Finset.mul_sum] at hsum ⊢
    linarith
  have hD : 0 ≤ Daug := absorption_of_reduced_bound Daug D0 s nu gap k b z r
    hnu (sub_nonneg.mpr hport) hh hg hidentity hreduced
  have hslack := mul_le_mul_of_nonneg_left hresidual hs
  dsimp [Daug] at hD
  linarith

#print axioms linked_acceleration
#print axioms physical_port_absorption

end RouteBPhysicalPortAssembly

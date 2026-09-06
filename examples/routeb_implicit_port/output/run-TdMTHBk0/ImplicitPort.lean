import Mathlib

open scoped BigOperators

namespace RouteBImplicitPort

theorem first_completion (s nu k z r : ℝ) (hh : nu - k ≠ 0) :
    s * z ^ 2 + nu * r ^ 2 - k * (z + r) ^ 2 =
      (nu - k) * (r - k * z / (nu - k)) ^ 2 +
      (s - k - k ^ 2 / (nu - k)) * z ^ 2 := by
  field_simp
  <;> ring

theorem second_completion (g b z : ℝ) (hg : g ≠ 0) :
    g * z ^ 2 + b * z = -b ^ 2 / (4 * g) + g * (z + b / (2 * g)) ^ 2 := by
  field_simp
  <;> ring

theorem channel_completion (s nu k b z r : ℝ) (hh : nu - k ≠ 0)
    (hg : s - k - k ^ 2 / (nu - k) ≠ 0) :
    s * z ^ 2 + b * z + nu * r ^ 2 - k * (z + r) ^ 2 =
      -b ^ 2 / (4 * (s - k - k ^ 2 / (nu - k))) +
      (nu - k) * (r - k * z / (nu - k)) ^ 2 +
      (s - k - k ^ 2 / (nu - k)) *
        (z + b / (2 * (s - k - k ^ 2 / (nu - k)))) ^ 2 := by
  have h1 := first_completion s nu k z r hh
  have h2 := second_completion (s - k - k ^ 2 / (nu - k)) b z hg
  linarith

noncomputable def H (nu k : ℝ) : ℝ := nu - k
noncomputable def G (s nu k : ℝ) : ℝ := s - k - k ^ 2 / (nu - k)

variable {ι : Type*} [Fintype ι]

/- Reduced quadratic after retaining the exact residual link. Unlike the old
   free-acceleration target, this accounts for z=I-l before eliminating r. -/
theorem diagonal_elimination (D0 s nu : ℝ) (k b z r : ι → ℝ)
    (hh : ∀ i, 0 < H nu (k i)) (hg : ∀ i, 0 < G s nu (k i)) :
    D0 + (∑ i, s * z i ^ 2 + b i * z i + nu * r i ^ 2 - k i * (z i + r i) ^ 2) =
      (D0 - ∑ i, b i ^ 2 / (4 * G s nu (k i))) +
      (∑ i, H nu (k i) * (r i - k i * z i / H nu (k i)) ^ 2) +
      (∑ i, G s nu (k i) * (z i + b i / (2 * G s nu (k i))) ^ 2) := by
  have hi (i : ι) := channel_completion s nu (k i) (b i) (z i) (r i)
    (ne_of_gt (hh i)) (ne_of_gt (hg i))
  have hs := Finset.sum_congr (s := Finset.univ) rfl (fun i _ => hi i)
  simp only [Finset.sum_add_distrib, Finset.sum_neg_distrib, neg_div] at hs
  unfold H G
  linarith

theorem absorption_of_reduced_bound (D D0 s nu portGap : ℝ) (k b z r : ι → ℝ)
    (hnu : 0 ≤ nu) (hport : 0 ≤ portGap)
    (hh : ∀ i, 0 < H nu (k i)) (hg : ∀ i, 0 < G s nu (k i))
    (hlink : D - nu * portGap =
      D0 + ∑ i, s * z i ^ 2 + b i * z i + nu * r i ^ 2 - k i * (z i + r i) ^ 2)
    (hreduced : 0 ≤ D0 - ∑ i, b i ^ 2 / (4 * G s nu (k i))) :
    0 ≤ D := by
  have hid := diagonal_elimination D0 s nu k b z r hh hg
  have hsq1 : 0 ≤ ∑ i, H nu (k i) * (r i - k i * z i / H nu (k i)) ^ 2 :=
    Finset.sum_nonneg (fun i _ => mul_nonneg (le_of_lt (hh i)) (sq_nonneg _))
  have hsq2 : 0 ≤ ∑ i, G s nu (k i) * (z i + b i / (2 * G s nu (k i))) ^ 2 :=
    Finset.sum_nonneg (fun i _ => mul_nonneg (le_of_lt (hg i)) (sq_nonneg _))
  have hp := mul_nonneg hnu hport
  linarith

/- This universal algebraic identity binds the ORIGINAL acceleration charge,
   not a lambda_A=0 replacement. Its l=I-z, a=(z+r)/m premises are explicit. -/
theorem residual_link_channel (I rt l a z r m s nu lambda rho B : ℝ)
    (hm : m ≠ 0) (hl : l = I - z) (ha : a = (z + r) / m) :
    rt * l + s * l ^ 2 - s * lambda * a ^ 2 -
      nu * (rho * B * a ^ 2 - r ^ 2) =
    rt * I + s * I ^ 2 +
      (s * z ^ 2 + (-(rt + 2 * s * I)) * z + nu * r ^ 2 -
        (s * lambda / m ^ 2 + nu * rho * B / m ^ 2) * (z + r) ^ 2) := by
  rw [hl, ha]
  field_simp
  <;> ring

#print axioms first_completion
#print axioms second_completion
#print axioms channel_completion
#print axioms diagonal_elimination
#print axioms absorption_of_reduced_bound
#print axioms residual_link_channel

end RouteBImplicitPort

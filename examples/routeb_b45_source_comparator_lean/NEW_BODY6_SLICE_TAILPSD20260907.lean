import NEW_BODY6_SLICE_MASSTAIL_Source20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_TAILPSD20260907

noncomputable section

open NEW_BODY6_SLICE_MASSTAIL_Core20260907 NEW_BODY6_SLICE_MASSTAIL_Source20260907
open NEW_BODY6_SLICE_VGRAM_Source20260907 RouteBO1PerBodyExactSource

/- UNCOMPILED bounded sidecar: only the ordered source columns {3,4}.
   PSD is stated explicitly as symmetry plus nonnegative real quadratic form. -/
def quadratic (B : Fin 2 → Fin 2 → ℝ) (x : Fin 2 → ℝ) : ℝ :=
  ∑ i : Fin 2, ∑ j : Fin 2, x i * B i j * x j

def normSq (x : Fin 2 → ℝ) : ℝ := x 0 ^ 2 + x 1 ^ 2

def TailPSD (B : Fin 2 → Fin 2 → ℝ) : Prop :=
  (∀ i j, B i j = B j i) ∧ ∀ x, 0 ≤ quadratic B x

def minDiagonal (B : Fin 2 → Fin 2 → ℝ) : ℝ := min (B 0 0) (B 1 1)

theorem quadratic_decomposition_attempt (z h m kappa : ℝ) (x : Fin 2 → ℝ) :
    quadratic (explicitTail z h m kappa) x =
      kappa * normSq x + m * h ^ 2 * (Real.sin z ^ 2 * x 0 ^ 2 + x 1 ^ 2) := by
  norm_num [quadratic, explicitTail, normSq, Fin.sum_univ_succ] <;> ring

/- Keep h^2 >= 0 explicit even though it follows from sq_nonneg h. -/
theorem quadratic_lower_attempt (z h m kappa : ℝ)
    (hm : 0 ≤ m) (hh : 0 ≤ h ^ 2) (x : Fin 2 → ℝ) :
    kappa * normSq x ≤ quadratic (explicitTail z h m kappa) x := by
  rw [quadratic_decomposition_attempt]
  have hr : 0 ≤ m * h ^ 2 * (Real.sin z ^ 2 * x 0 ^ 2 + x 1 ^ 2) :=
    mul_nonneg (mul_nonneg hm hh)
      (add_nonneg (mul_nonneg (sq_nonneg _) (sq_nonneg _)) (sq_nonneg _))
  exact le_add_of_nonneg_right hr

theorem tail_psd_attempt (z h m kappa : ℝ)
    (hk : 0 < kappa) (hm : 0 ≤ m) (hh : 0 ≤ h ^ 2) :
    TailPSD (explicitTail z h m kappa) := by
  constructor
  · exact table_symmetric_attempt z h m kappa
  · intro x
    exact le_trans (mul_nonneg (le_of_lt hk) (add_nonneg (sq_nonneg _) (sq_nonneg _)))
      (quadratic_lower_attempt z h m kappa hm hh x)

theorem min_diagonal_exact_attempt (z h m kappa : ℝ)
    (hm : 0 ≤ m) (hh : 0 ≤ h ^ 2) :
    minDiagonal (explicitTail z h m kappa) = kappa + m * h ^ 2 * Real.sin z ^ 2 := by
  have hs : Real.sin z ^ 2 ≤ 1 := by
    nlinarith [Real.sin_sq_add_cos_sq z, sq_nonneg (Real.cos z)]
  have hp : m * h ^ 2 * Real.sin z ^ 2 ≤ m * h ^ 2 := by
    simpa using mul_le_mul_of_nonneg_left hs (mul_nonneg hm hh)
  change min (kappa + m * h ^ 2 * Real.sin z ^ 2) (kappa + m * h ^ 2) = _
  exact min_eq_left (add_le_add_left hp kappa)

theorem min_diagonal_lower_attempt (z h m kappa : ℝ)
    (hm : 0 ≤ m) (hh : 0 ≤ h ^ 2) :
    kappa ≤ minDiagonal (explicitTail z h m kappa) := by
  rw [min_diagonal_exact_attempt z h m kappa hm hh]
  exact le_add_of_nonneg_right (mul_nonneg (mul_nonneg hm hh) (sq_nonneg _))

/- Source binding retains body index 5 and tailJoint order 0->3, 1->4. -/
def sourceTail (q : Fin 6 → ℝ) : Fin 2 → Fin 2 → ℝ :=
  fun i j => sourceBodyMass q (5 : Fin 6) (tailJoint i) (tailJoint j)

theorem source_tail_eq_attempt (hc : CenterOffsetTarget)
    (m kappa : ℝ) (hw : SourceWeightsTarget m kappa) (q : Fin 6 → ℝ) :
    sourceTail q = explicitTail (q 4) offset m kappa := by
  funext i j
  exact source_weighted_tail_attempt hc m kappa hw q i j

/- All source conclusions keep center, weight, and sign premises together.
   This is a conditional theorem attempt, not a registry witness. -/
theorem source_tail_psd_bounds_attempt (hc : CenterOffsetTarget)
    (m kappa : ℝ) (hw : SourceWeightsTarget m kappa)
    (hk : 0 < kappa) (hm : 0 ≤ m) (hh : 0 ≤ offset ^ 2) (q : Fin 6 → ℝ) :
    TailPSD (sourceTail q) ∧
    (∀ x, kappa * normSq x ≤ quadratic (sourceTail q) x) ∧
    kappa ≤ minDiagonal (sourceTail q) ∧
    minDiagonal (sourceTail q) = kappa + m * offset ^ 2 * Real.sin (q 4) ^ 2 := by
  rw [source_tail_eq_attempt hc m kappa hw q]
  exact ⟨tail_psd_attempt (q 4) offset m kappa hk hm hh,
    quadratic_lower_attempt (q 4) offset m kappa hm hh,
    min_diagonal_lower_attempt (q 4) offset m kappa hm hh,
    min_diagonal_exact_attempt (q 4) offset m kappa hm hh⟩

/- No claim about other columns, the complete mass matrix, Fourier or coverage.
   No Lean execution or source/registry admission is provided by this file. -/
end
end NEW_BODY6_SLICE_TAILPSD20260907

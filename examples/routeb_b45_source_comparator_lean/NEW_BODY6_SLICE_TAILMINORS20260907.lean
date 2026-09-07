import NEW_BODY6_SLICE_TAILPSD20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_TAILMINORS20260907

noncomputable section

open NEW_BODY6_SLICE_MASSTAIL_Core20260907 NEW_BODY6_SLICE_MASSTAIL_Source20260907
open NEW_BODY6_SLICE_VGRAM_Source20260907 NEW_BODY6_SLICE_TAILPSD20260907

/- UNCOMPILED: the three nonempty principal minors of an ordered real 2x2.
   det2 is the explicit scalar determinant formula, not a Matrix.det adapter. -/
def det2 (B : Fin 2 → Fin 2 → ℝ) : ℝ := B 0 0 * B 1 1 - B 0 1 * B 1 0

def StrictPrincipalMinors (B : Fin 2 → Fin 2 → ℝ) : Prop :=
  0 < B 0 0 ∧ 0 < B 1 1 ∧ 0 < det2 B

def PrincipalMinorCriterion (B : Fin 2 → Fin 2 → ℝ) : Prop :=
  0 ≤ B 0 0 ∧ 0 ≤ B 1 1 ∧ 0 ≤ det2 B

theorem tail_principal_formulas_attempt (z h m kappa : ℝ) :
    (explicitTail z h m kappa) 0 0 = kappa + m * h ^ 2 * Real.sin z ^ 2 ∧
    (explicitTail z h m kappa) 1 1 = kappa + m * h ^ 2 ∧
    det2 (explicitTail z h m kappa) =
      (kappa + m * h ^ 2 * Real.sin z ^ 2) * (kappa + m * h ^ 2) := by
  norm_num [det2, explicitTail]

theorem tail_principal_positive_attempt (z h m kappa : ℝ)
    (hk : 0 < kappa) (hm : 0 ≤ m) (hh : 0 ≤ h ^ 2) :
    StrictPrincipalMinors (explicitTail z h m kappa) := by
  have ha : 0 ≤ m * h ^ 2 := mul_nonneg hm hh
  have h0 : 0 < kappa + m * h ^ 2 * Real.sin z ^ 2 :=
    lt_of_lt_of_le hk (le_add_of_nonneg_right (mul_nonneg ha (sq_nonneg _)))
  have h1 : 0 < kappa + m * h ^ 2 :=
    lt_of_lt_of_le hk (le_add_of_nonneg_right ha)
  rcases tail_principal_formulas_attempt z h m kappa with ⟨e0, e1, ed⟩
  unfold StrictPrincipalMinors
  rw [e0, e1, ed]
  exact ⟨h0, h1, mul_pos h0 h1⟩

theorem strict_to_nonnegative_attempt (B : Fin 2 → Fin 2 → ℝ)
    (hp : StrictPrincipalMinors B) : PrincipalMinorCriterion B :=
  ⟨le_of_lt hp.1, le_of_lt hp.2.1, le_of_lt hp.2.2⟩

/- The bridge is deliberately limited to zero cross terms. For this diagonal
   class, the two order-one minors suffice; the determinant minor is redundant.
   This is not a general nonsymmetric-matrix principal-minor criterion. -/
theorem diagonal_minor_criterion_to_psd_attempt (B : Fin 2 → Fin 2 → ℝ)
    (h01 : B 0 1 = 0) (h10 : B 1 0 = 0)
    (hp : PrincipalMinorCriterion B) : TailPSD B := by
  constructor
  · intro i j
    fin_cases i <;> fin_cases j <;> simp [h01, h10]
  · intro x
    have he : quadratic B x = B 0 0 * x 0 ^ 2 + B 1 1 * x 1 ^ 2 := by
      norm_num [quadratic, Fin.sum_univ_succ, h01, h10] <;> ring
    rw [he]
    exact add_nonneg (mul_nonneg hp.1 (sq_nonneg _))
      (mul_nonneg hp.2.1 (sq_nonneg _))

/- Connect the tail's principal-minor evidence to the existing explicit PSD
   predicate. No old kappa-norm bound or minimum-diagonal proof is repeated. -/
theorem tail_minor_psd_interface_attempt (z h m kappa : ℝ)
    (hk : 0 < kappa) (hm : 0 ≤ m) (hh : 0 ≤ h ^ 2) :
    StrictPrincipalMinors (explicitTail z h m kappa) ∧
    PrincipalMinorCriterion (explicitTail z h m kappa) ∧
    TailPSD (explicitTail z h m kappa) := by
  have hs := tail_principal_positive_attempt z h m kappa hk hm hh
  have hn := strict_to_nonnegative_attempt _ hs
  exact ⟨hs, hn, diagonal_minor_criterion_to_psd_attempt _ rfl rfl hn⟩

/- Actual body index 5 and ordered columns 3,4 are inherited from sourceTail.
   Retain center, source-weight and sign premises, including offset^2 >= 0. -/
theorem source_tail_minors_attempt (hc : CenterOffsetTarget)
    (m kappa : ℝ) (hw : SourceWeightsTarget m kappa)
    (hk : 0 < kappa) (hm : 0 ≤ m) (hh : 0 ≤ offset ^ 2) (q : Fin 6 → ℝ) :
    det2 (sourceTail q) =
      (kappa + m * offset ^ 2 * Real.sin (q 4) ^ 2) * (kappa + m * offset ^ 2) ∧
    StrictPrincipalMinors (sourceTail q) ∧
    PrincipalMinorCriterion (sourceTail q) ∧ TailPSD (sourceTail q) := by
  rw [source_tail_eq_attempt hc m kappa hw q]
  exact ⟨(tail_principal_formulas_attempt (q 4) offset m kappa).2.2,
    tail_minor_psd_interface_attempt (q 4) offset m kappa hk hm hh⟩

/- Only this tail principal block. No complete-body, eigenvalue, Fourier,
   coverage, compilation or registry admission claim is constructed. -/
end
end NEW_BODY6_SLICE_TAILMINORS20260907

import NEW_BODY6_SLICE_TAILSOLVECERT20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_ENTRYMARGIN20260907

noncomputable section

open NEW_BODY6_SLICE_SCHURMARGIN20260907 NEW_BODY6_SLICE_MARGINUNIFORM20260907
open NEW_BODY6_SLICE_EXACTSCHURCOEFF20260907 NEW_BODY6_SLICE_SOURCEBLOCKBIND20260907
open NEW_BODY6_SLICE_SELF3MASSBIND20260907 NEW_BODY6_SLICE_SELF3_Core20260907
open NEW_BODY6_SLICE_LEVER_Core20260907 NEW_BODY6_SLICE_MIXED_Core20260907
open NEW_BODY6_SLICE_MASSMIX_Core20260907 NEW_BODY6_SLICE_VGRAM_Source20260907
open NEW_BODY6_SLICE_MASSTAIL_Source20260907 NEW_BODY6_SLICE_SCHURREMAINDER20260907
open NEW_BODY6_SLICE_TAILSCHUR20260907 NEW_BODY6_SLICE_TAILINVERSE20260907

/- OPEN_UNCOMPILED. A sufficient nine-entry envelope: three diagonal lower
   inequalities and six ordered off-diagonal absolute bounds, plus symmetry.
   It is not a necessary test for a positive margin. -/
structure NineEntryLowerBound (R : FrontBlock) (mu beta : ℝ) : Prop where
  symmetric : ∀ i j, R i j = R j i
  muPositive : 0 < mu
  betaNonnegative : 0 ≤ beta
  diagonal : ∀ i, mu + 2 * beta ≤ R i i
  offDiagonal : ∀ i j, i ≠ j → |R i j| ≤ beta

theorem cross_pair_lower_attempt (x y r beta : ℝ) (hr : |r| ≤ beta) :
    -beta * (x ^ 2 + y ^ 2) ≤ 2 * r * x * y := by
  rcases abs_le.mp hr with ⟨hlo, hhi⟩
  have hn : 0 ≤ x ^ 2 + y ^ 2 := add_nonneg (sq_nonneg x) (sq_nonneg y)
  rcases le_total 0 r with hp | hm
  · have h1 := mul_nonneg hp (sq_nonneg (x + y))
    have h2 := mul_nonneg (sub_nonneg.mpr hhi) hn
    nlinarith only [h1, h2]
  · have h1 := mul_nonneg (neg_nonneg.mpr hm) (sq_nonneg (x - y))
    have hc : 0 ≤ beta + r := by linarith
    have h2 := mul_nonneg hc hn
    nlinarith only [h1, h2]

theorem nine_entries_to_margin_attempt (R : FrontBlock) (mu beta : ℝ)
    (he : NineEntryLowerBound R mu beta) : RemainderMargin R mu := by
  refine ⟨he.symmetric, le_of_lt he.muPositive, ?_⟩
  intro u
  have h01 := cross_pair_lower_attempt (u 0) (u 1) (R 0 1) beta (he.offDiagonal 0 1 (by decide))
  have h02 := cross_pair_lower_attempt (u 0) (u 2) (R 0 2) beta (he.offDiagonal 0 2 (by decide))
  have h12 := cross_pair_lower_attempt (u 1) (u 2) (R 1 2) beta (he.offDiagonal 1 2 (by decide))
  have hg : ∀ i : Fin 3, 0 ≤ (R i i - (mu + 2 * beta)) * u i ^ 2 :=
    fun i => mul_nonneg (sub_nonneg.mpr (he.diagonal i)) (sq_nonneg (u i))
  have hg0 := hg 0
  have hg1 := hg 1
  have hg2 := hg 2
  norm_num [frontAction, Fin.sum_univ_succ]
  rw [he.symmetric 1 0, he.symmetric 2 0, he.symmetric 2 1]
  nlinarith only [h01, h02, h12, hg0, hg1, hg2]

/- Source symmetry is available from exact source entries; the nine numerical
   inequality witnesses are independent inputs and are not inferred here. -/
theorem source_entry_envelope_attempt (q : Config) (m kappa mu beta : ℝ)
    (hmu : 0 < mu) (hbeta : 0 ≤ beta)
    (hd : ∀ i, mu + 2 * beta ≤ sourceCoefficient q m kappa i i)
    (ho : ∀ i j, i ≠ j → |sourceCoefficient q m kappa i j| ≤ beta) :
    NineEntryLowerBound (sourceCoefficient q m kappa) mu beta :=
  ⟨exact_entries_symmetric_attempt q m kappa (sourceCoefficient q m kappa) (fun _ _ => rfl),
    hmu, hbeta, hd, ho⟩

theorem exact_source_margin_from_entries_attempt (q : Config) (m kappa mu beta : ℝ)
    (A R : FrontBlock) (X : CrossX) (Y : CrossY)
    (hs : ExactSchurCoefficientContract q m kappa A X Y R)
    (he : NineEntryLowerBound (sourceCoefficient q m kappa) mu beta) : RemainderMargin R mu := by
  have hr : R = sourceCoefficient q m kappa := by
    funext i j
    exact hs.entries i j
  rw [hr]
  exact nine_entries_to_margin_attempt _ mu beta he

theorem uniform_source_entry_margin_attempt (D : Set Config) (m kappa mu : ℝ)
    (hmu : 0 < mu) (beta : Config → ℝ)
    (he : ∀ q ∈ D, NineEntryLowerBound (sourceCoefficient q m kappa) mu (beta q)) :
    0 < mu ∧ UniformMargin D (fun q => sourceCoefficient q m kappa) mu := by
  refine ⟨hmu, ?_⟩
  intro q hq
  exact nine_entries_to_margin_attempt _ mu (beta q) (he q hq)

/- Targeted exact source-formula obstruction: q=0, physical scalar weights.
   This is not sampled PSD; the canonical rational remainder has an exact null
   vector. Actual-source transfer below still requires center/weight witnesses. -/
def zeroDirection : Front := ![0, -19, 40]

def canonicalZeroR : FrontBlock :=
  schurRemainder 0 offset (3 / 20) (1 / 60)
    (explicitWeightedA (0 : Config) (3 / 20) (1 / 60))
    (mixedX (0 : Config) (3 / 20) (1 / 60)) (mixedY (0 : Config) (3 / 20) (1 / 60))

theorem canonical_zero_null_attempt : frontAction canonicalZeroR zeroDirection = 0 := by
  funext i
  fin_cases i <;>
    norm_num [frontAction, canonicalZeroR, zeroDirection, schurRemainder, schurCorrection,
      inverseTail, explicitWeightedA, mixedX, mixedY, explicitMixed, combinedWeight,
      coeffA, coeffB, coeffP, coeffR, coeffU, coeffV, lastX, lastY, lastZ,
      radial, reach, height, angleSum, projAlong, projAcross, offset, Fin.sum_univ_succ]

theorem source_zero_null_attempt (hc : CenterOffsetTarget)
    (hw : SourceWeightsTarget (3 / 20 : ℝ) (1 / 60 : ℝ)) :
    frontAction (sourceCoefficient (0 : Config) (3 / 20) (1 / 60)) zeroDirection = 0 := by
  have hb := explicit_A_mixed_source_binding_attempt hc (3 / 20) (1 / 60) hw (0 : Config)
  have he : sourceCoefficient (0 : Config) (3 / 20) (1 / 60) = canonicalZeroR := by
    funext i j
    exact (bound_remainder_coefficient_attempt (0 : Config) (3 / 20) (1 / 60)
      (explicitWeightedA (0 : Config) (3 / 20) (1 / 60))
      (mixedX (0 : Config) (3 / 20) (1 / 60)) (mixedY (0 : Config) (3 / 20) (1 / 60)) hb i j).symm
  rw [he]
  exact canonical_zero_null_attempt

theorem source_zero_no_positive_margin_attempt (hc : CenterOffsetTarget)
    (hw : SourceWeightsTarget (3 / 20 : ℝ) (1 / 60 : ℝ)) (mu : ℝ) (hmu : 0 < mu) :
    ¬ RemainderMargin (sourceCoefficient (0 : Config) (3 / 20) (1 / 60)) mu := by
  intro hm
  have hbound := hm.2.2 zeroDirection
  rw [source_zero_null_attempt hc hw] at hbound
  norm_num [zeroDirection, Fin.sum_univ_succ] at hbound
  nlinarith

theorem domain_contains_zero_obstruction_attempt (hc : CenterOffsetTarget)
    (hw : SourceWeightsTarget (3 / 20 : ℝ) (1 / 60 : ℝ))
    (D : Set Config) (hz : (0 : Config) ∈ D) (mu : ℝ) (hmu : 0 < mu) :
    ¬ UniformMargin D (fun q => sourceCoefficient q (3 / 20) (1 / 60)) mu := by
  intro hu
  exact source_zero_no_positive_margin_attempt hc hw mu hmu (hu 0 hz)

/- External entry inequalities/domain bounds remain required away from this
   obstruction. No full PSD, coverage, numerical admission or Lean verification. -/
end
end NEW_BODY6_SLICE_ENTRYMARGIN20260907

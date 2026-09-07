import NEW_BODY6_SLICE_MARGINUNIFORM20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_EXACTSCHURCOEFF20260907

noncomputable section

open NEW_BODY6_SLICE_MARGINUNIFORM20260907 NEW_BODY6_SLICE_SCHURMARGIN20260907
open NEW_BODY6_SLICE_SOURCEBLOCKBIND20260907 NEW_BODY6_SLICE_SCHURREMAINDER20260907
open NEW_BODY6_SLICE_TAILSCHUR20260907 NEW_BODY6_SLICE_TAILPSD20260907
open NEW_BODY6_SLICE_VGRAM_Source20260907 NEW_BODY6_SLICE_MASSTAIL_Source20260907

/- UNCOMPILED. Actual body-6 entry expression with ordered tail indices 3,4.
   B=sourceTail is the tail block; inverseTail is its conditional inverse D.
   The earlier solvedRight variable S means D*Y, not the tail block itself. -/
def sourceCoefficient (q : Config) (m kappa : ℝ) (i j : Fin 3) : ℝ :=
  sourceA q i j - sourceX q i 0 * sourceY q 0 j /
    (kappa + m * offset ^ 2 * Real.sin (q 4) ^ 2) -
      sourceX q i 1 * sourceY q 1 j / (kappa + m * offset ^ 2)

def ExactSourceEntries (q : Config) (m kappa : ℝ) (R : FrontBlock) : Prop :=
  ∀ i j, R i j = sourceCoefficient q m kappa i j

theorem exact_entries_iff_remainder_attempt (q : Config) (m kappa : ℝ)
    (A R : FrontBlock) (X : CrossX) (Y : CrossY) (hb : SourceBlockBinding q A X Y) :
    ExactSourceEntries q m kappa R ↔
      ∀ i j, R i j = schurRemainder (q 4) offset m kappa A X Y i j := by
  have he : ∀ i j, schurRemainder (q 4) offset m kappa A X Y i j = sourceCoefficient q m kappa i j :=
    bound_remainder_coefficient_attempt q m kappa A X Y hb
  constructor
  · intro hr i j
    exact (hr i j).trans (he i j).symm
  · intro hr i j
    exact (hr i j).trans (he i j)

/- Actual source symmetry supplies A=A^T and Y=X^T; no cross-block symmetry
   is inferred merely from RemainderMargin or from front SELF3 binding. -/
theorem exact_entries_symmetric_attempt (q : Config) (m kappa : ℝ) (R : FrontBlock)
    (he : ExactSourceEntries q m kappa R) (i j : Fin 3) : R i j = R j i := by
  have ha : sourceA q i j = sourceA q j i := source_mass_symmetric_attempt q _ _
  rw [he i j, he j i]
  unfold sourceCoefficient
  simp_rw [source_y_transpose_attempt]
  rw [ha]
  ring

structure ExactSchurCoefficientContract (q : Config) (m kappa : ℝ)
    (A : FrontBlock) (X : CrossX) (Y : CrossY) (R : FrontBlock) : Prop where
  sourceBinding : SourceBlockBinding q A X Y
  tailCore : SchurRemainderContract 3 3 (sourceTail q) (q 4) offset m kappa A X Y
  entries : ExactSourceEntries q m kappa R

theorem exact_source_contract_attempt (hc : CenterOffsetTarget)
    (q : Config) (m kappa : ℝ) (hw : SourceWeightsTarget m kappa)
    (hk : 0 < kappa) (hm : 0 ≤ m) (hh : 0 ≤ offset ^ 2)
    (A R : FrontBlock) (X : CrossX) (Y : CrossY) (hb : SourceBlockBinding q A X Y)
    (hr : ∀ i j, R i j = schurRemainder (q 4) offset m kappa A X Y i j) :
    ExactSchurCoefficientContract q m kappa A X Y R :=
  ⟨hb, source_remainder_contract_attempt hc m kappa hw hk hm hh q A X Y,
    (exact_entries_iff_remainder_attempt q m kappa A R X Y hb).mpr hr⟩

/- Uniform margin and exact entries are separate families of proof inputs. -/
theorem uniform_margin_with_exact_seam_attempt (D : Set Config) (m kappa mu : ℝ)
    (A R : Config → FrontBlock) (X : Config → CrossX) (Y : Config → CrossY)
    (he : ∀ q ∈ D, ExactSchurCoefficientContract q m kappa (A q) (X q) (Y q) (R q))
    (hu : UniformMargin D R mu) :
    ∀ q ∈ D, SourceSchurMarginContract q m kappa mu (A q) (X q) (Y q) (R q) := by
  intro q hq
  have hs := he q hq
  exact ⟨hs.sourceBinding, hs.tailCore,
    (exact_entries_iff_remainder_attempt q m kappa (A q) (R q) (X q) (Y q) hs.sourceBinding).mp hs.entries,
    hu q hq⟩

theorem coefficient_mismatch_rejects_attempt (q : Config) (m kappa : ℝ) (R : FrontBlock)
    (bad : ∃ i j, R i j ≠ sourceCoefficient q m kappa i j) : ¬ ExactSourceEntries q m kappa R := by
  intro he
  obtain ⟨i, j, hne⟩ := bad
  exact hne (he i j)

/- Abstract exact countermodel, NOT physical source data: A=I, X=Y=0.
   I and 2I share uniform margin 1 and symmetry, but 2I is not A-X*D*Y.
   Here kappa=1,m=h=z=0 only instantiate the abstract scalar inverse expression. -/
theorem uniform_margin_not_coefficient_identity_attempt :
    UniformMargin Set.univ (fun _ => scalarIdentity 1) 1 ∧
    UniformMargin Set.univ (fun _ => scalarIdentity 2) 1 ∧
    scalarIdentity 2 0 0 ≠ schurRemainder 0 0 0 1 (scalarIdentity 1)
      (fun (_ : Fin 3) (_ : Fin 2) => 0) (fun (_ : Fin 2) (_ : Fin 3) => 0) 0 0 := by
  have h1 := scalar_margin_attempt 1 (by norm_num)
  have h2 := margin_lowering_attempt (scalarIdentity 2) 2 1
    (scalar_margin_attempt 2 (by norm_num)) (by norm_num) (by norm_num)
  refine ⟨(fun _ _ => h1), (fun _ _ => h2), ?_⟩
  norm_num [schurRemainder, schurCorrection, scalarIdentity, Fin.sum_univ_succ]

/- No automatic source coefficients from margins, no invented robot cross
   data, full-matrix PSD, Fourier, coverage, Lean execution or registry change. -/
end
end NEW_BODY6_SLICE_EXACTSCHURCOEFF20260907

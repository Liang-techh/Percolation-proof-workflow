import NEW_BODY6_SLICE_SCHURMARGIN20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_MARGINUNIFORM20260907

noncomputable section

open NEW_BODY6_SLICE_SCHURMARGIN20260907 NEW_BODY6_SLICE_SOURCEBLOCKBIND20260907
open NEW_BODY6_SLICE_VGRAM_Source20260907 NEW_BODY6_SLICE_MASSTAIL_Source20260907
open NEW_BODY6_SLICE_SCHURREMAINDER20260907 NEW_BODY6_SLICE_TAILSCHUR20260907

abbrev Config := Fin 6 → ℝ

/- UNCOMPILED. One fixed mu over exactly D; no implicit extension beyond D. -/
def UniformMargin (D : Set Config) (R : Config → FrontBlock) (mu : ℝ) : Prop :=
  ∀ q ∈ D, RemainderMargin (R q) mu

theorem margin_lowering_attempt (R : FrontBlock) (rho mu : ℝ)
    (hr : RemainderMargin R rho) (hmu : 0 ≤ mu) (hle : mu ≤ rho) : RemainderMargin R mu := by
  refine ⟨hr.1, hmu, ?_⟩
  intro u
  exact le_trans (mul_le_mul_of_nonneg_right hle (Finset.sum_nonneg (fun i _ => sq_nonneg (u i))))
    (hr.2.2 u)

theorem uniform_from_floor_attempt (D : Set Config) (R : Config → FrontBlock)
    (rho : Config → ℝ) (mu : ℝ) (hmu : 0 ≤ mu)
    (hfloor : ∀ q ∈ D, mu ≤ rho q) (hpoint : ∀ q ∈ D, RemainderMargin (R q) (rho q)) :
    UniformMargin D R mu := by
  intro q hq
  exact margin_lowering_attempt (R q) (rho q) mu (hpoint q hq) hmu (hfloor q hq)

theorem uniform_restrict_attempt (D E : Set Config) (R : Config → FrontBlock) (mu : ℝ)
    (hsub : D ⊆ E) (hu : UniformMargin E R mu) : UniformMargin D R mu :=
  fun q hq => hu q (hsub hq)

/- Finite positive margins have a positive common floor. The empty case is
   vacuous; the insertion proof constructs a floor via min, capped at 1. -/
theorem finite_positive_floor_attempt (K : Finset Config) (rho : Config → ℝ)
    (hp : ∀ q ∈ K, 0 < rho q) : ∃ mu : ℝ, 0 < mu ∧ ∀ q ∈ K, mu ≤ rho q := by
  classical
  revert hp
  induction K using Finset.induction_on with
  | empty =>
      intro hp
      exact ⟨1, by norm_num, by simp⟩
  | @insert q K hq ih =>
      intro hp
      have hpK : ∀ t ∈ K, 0 < rho t := fun t ht => hp t (Finset.mem_insert_of_mem ht)
      obtain ⟨mu, hmu, hfloor⟩ := ih hpK
      refine ⟨min (rho q) mu, lt_min_iff.mpr ⟨hp q (Finset.mem_insert_self q K), hmu⟩, ?_⟩
      intro t ht
      rcases Finset.mem_insert.mp ht with heq | hmem
      · subst t
        exact min_le_left _ _
      · exact le_trans (min_le_right _ _) (hfloor t hmem)

theorem finite_uniform_attempt (K : Finset Config) (R : Config → FrontBlock) (rho : Config → ℝ)
    (hp : ∀ q ∈ K, 0 < rho q) (hpoint : ∀ q ∈ K, RemainderMargin (R q) (rho q)) :
    ∃ mu : ℝ, 0 < mu ∧ UniformMargin (↑K : Set Config) R mu := by
  obtain ⟨mu, hmu, hfloor⟩ := finite_positive_floor_attempt K rho hp
  exact ⟨mu, hmu, uniform_from_floor_attempt (↑K) R rho mu (le_of_lt hmu) hfloor hpoint⟩

/- Source families still require source binding, exact remainders and an
   external common-margin family. No positivity is inferred from bindings. -/
theorem uniform_source_contract_attempt (D : Set Config) (m kappa mu : ℝ)
    (hc : CenterOffsetTarget) (hw : SourceWeightsTarget m kappa)
    (hk : 0 < kappa) (hm : 0 ≤ m) (hh : 0 ≤ offset ^ 2)
    (A R : Config → FrontBlock) (X : Config → CrossX) (Y : Config → CrossY)
    (hb : ∀ q ∈ D, SourceBlockBinding q (A q) (X q) (Y q))
    (hR : ∀ q ∈ D, ∀ i j, R q i j = schurRemainder (q 4) offset m kappa (A q) (X q) (Y q) i j)
    (hu : UniformMargin D R mu) :
    ∀ q ∈ D, SourceSchurMarginContract q m kappa mu (A q) (X q) (Y q) (R q) := by
  intro q hq
  exact source_margin_contract_attempt hc m kappa mu hw hk hm hh q (A q) (X q) (Y q) (R q)
    (hb q hq) (hR q hq) (hu q hq)

theorem uniform_residual_consumer_attempt (D : Set Config) (m kappa mu : ℝ)
    (A R : Config → FrontBlock) (X : Config → CrossX) (Y : Config → CrossY)
    (hs : ∀ q ∈ D, SourceSchurMarginContract q m kappa mu (A q) (X q) (Y q) (R q)) :
    ∀ q ∈ D, ∀ u : Front, mu * (∑ i : Fin 3, u i ^ 2) ≤
      ∑ i : Fin 3, u i * frontResidual (A q) (X q) (solvedRight 3 (q 4) offset m kappa (Y q)) u i := by
  intro q hq u
  exact (source_residual_consumer_attempt q m kappa mu (A q) (X q) (Y q) (R q) (hs q hq) u).2.2

/- Exact abstract counterexample. These R(q) are NOT claimed to be body-6
   source remainders; no A/X/Y or physical counterexample is fabricated. -/
def scalarIdentity (d : ℝ) : FrontBlock := fun i j => if i = j then d else 0

theorem scalar_quadratic_attempt (d : ℝ) (u : Front) :
    (∑ i : Fin 3, u i * frontAction (scalarIdentity d) u i) = d * (∑ i : Fin 3, u i ^ 2) := by
  norm_num [frontAction, scalarIdentity, Fin.sum_univ_succ] <;> ring

theorem scalar_margin_attempt (d : ℝ) (hd : 0 < d) : RemainderMargin (scalarIdentity d) d := by
  refine ⟨?_, le_of_lt hd, ?_⟩
  · intro i j
    simp [scalarIdentity, eq_comm]
  · intro u
    rw [scalar_quadratic_attempt]

theorem scalar_margin_upper_attempt (d mu : ℝ) (hm : RemainderMargin (scalarIdentity d) mu) : mu ≤ d := by
  have he := hm.2.2 (![1, 0, 0] : Front)
  rw [scalar_quadratic_attempt] at he
  simpa [Fin.sum_univ_succ] using he

def counterConfig (n : ℕ) : Config := fun i => if i = 0 then (n : ℝ) else 0
def counterDomain : Set Config := Set.range counterConfig
def counterR (q : Config) : FrontBlock := scalarIdentity (1 / (q 0 + 1))

theorem counter_pointwise_positive_attempt :
    ∀ q ∈ counterDomain, ∃ rho : ℝ, 0 < rho ∧ RemainderMargin (counterR q) rho := by
  intro q hq
  rcases hq with ⟨n, rfl⟩
  have hp : 0 < (1 : ℝ) / ((n : ℝ) + 1) := by positivity
  exact ⟨1 / ((n : ℝ) + 1), hp, scalar_margin_attempt _ hp⟩

theorem counter_no_uniform_positive_attempt :
    ¬ ∃ mu : ℝ, 0 < mu ∧ UniformMargin counterDomain counterR mu := by
  rintro ⟨mu, hmu, hu⟩
  obtain ⟨n, hn⟩ := exists_nat_gt ((1 : ℝ) / mu)
  have hprod : (1 : ℝ) < (n : ℝ) * mu := (div_lt_iff₀ hmu).mp hn
  have hden : 0 < (n : ℝ) + 1 := by positivity
  have hsmall : (1 : ℝ) / ((n : ℝ) + 1) < mu := by
    apply (div_lt_iff₀ hden).2
    nlinarith
  have hb := scalar_margin_upper_attempt (1 / ((n : ℝ) + 1)) mu (hu (counterConfig n) ⟨n, rfl⟩)
  exact (not_le_of_gt hsmall) hb

/- Zero IS a common PSD margin; the failed implication concerns positive mu. -/
theorem counter_zero_uniform_attempt : UniformMargin counterDomain counterR 0 := by
  intro q hq
  obtain ⟨rho, hp, hm⟩ := counter_pointwise_positive_attempt q hq
  exact margin_lowering_attempt (counterR q) rho 0 hm (by norm_num) (le_of_lt hp)

/- No finite samples-to-continuum inference, cross-block data, automatic source
   margin, full-matrix PSD, coverage, Lean execution or registry admission. -/
end
end NEW_BODY6_SLICE_MARGINUNIFORM20260907

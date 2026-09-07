import NEW_BODY6_SLICE_ENTRYMARGIN20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_DOMAINREPAIR20260907

noncomputable section

open NEW_BODY6_SLICE_ENTRYMARGIN20260907 NEW_BODY6_SLICE_MARGINUNIFORM20260907
open NEW_BODY6_SLICE_SCHURMARGIN20260907 NEW_BODY6_SLICE_EXACTSCHURCOEFF20260907
open NEW_BODY6_SLICE_VGRAM_Source20260907 NEW_BODY6_SLICE_MASSTAIL_Source20260907

/- OPEN_UNCOMPILED. Request shape is distinct from a proved margin family.
   Nonstrict is permitted on either domain; strict requires exclusion of q=0. -/
inductive DomainMarginRequest (D : Set Config) (mu : ℝ) : Prop
  | nonstrict (hmu : mu = 0) : DomainMarginRequest D mu
  | strict (hmu : 0 < mu) (excludesZero : (0 : Config) ∉ D) : DomainMarginRequest D mu

def ExactPhysicalFamily (D : Set Config) (R : Config → FrontBlock) : Prop :=
  ∀ q ∈ D, ExactSourceEntries q (3 / 20) (1 / 60) (R q)

/- Preserve the actual null-vector obstruction through candidate R bindings.
   An existing PSD/margin family over a domain containing zero must use mu=0;
   this theorem does not manufacture that PSD family. -/
theorem contains_zero_forces_zero_margin_attempt (hc : CenterOffsetTarget)
    (hw : SourceWeightsTarget (3 / 20 : ℝ) (1 / 60 : ℝ))
    (D : Set Config) (R : Config → FrontBlock) (mu : ℝ) (hz : (0 : Config) ∈ D)
    (he : ExactPhysicalFamily D R) (hu : UniformMargin D R mu) : mu = 0 := by
  have hr : R 0 = sourceCoefficient (0 : Config) (3 / 20) (1 / 60) := by
    funext i j
    exact he 0 hz i j
  have hm := hu 0 hz
  rw [hr] at hm
  by_cases hp : 0 < mu
  · exact False.elim (source_zero_no_positive_margin_attempt hc hw mu hp hm)
  · exact le_antisymm (le_of_not_gt hp) hm.2.1

theorem positive_uniform_excludes_zero_attempt (hc : CenterOffsetTarget)
    (hw : SourceWeightsTarget (3 / 20 : ℝ) (1 / 60 : ℝ))
    (D : Set Config) (R : Config → FrontBlock) (mu : ℝ) (hp : 0 < mu)
    (he : ExactPhysicalFamily D R) (hu : UniformMargin D R mu) : (0 : Config) ∉ D := by
  intro hz
  have hzero := contains_zero_forces_zero_margin_attempt hc hw D R mu hz he hu
  linarith

structure SourceDomainMarginCertificate (D : Set Config) (R : Config → FrontBlock) (mu : ℝ) : Prop where
  center : CenterOffsetTarget
  weights : SourceWeightsTarget (3 / 20 : ℝ) (1 / 60 : ℝ)
  sourceEntries : ExactPhysicalFamily D R
  request : DomainMarginRequest D mu
  provedMargin : UniformMargin D R mu

theorem strict_domain_certificate_attempt (hc : CenterOffsetTarget)
    (hw : SourceWeightsTarget (3 / 20 : ℝ) (1 / 60 : ℝ))
    (D : Set Config) (R : Config → FrontBlock) (mu : ℝ)
    (hp : 0 < mu) (hz : (0 : Config) ∉ D)
    (he : ExactPhysicalFamily D R) (hu : UniformMargin D R mu) :
    SourceDomainMarginCertificate D R mu :=
  ⟨hc, hw, he, DomainMarginRequest.strict hp hz, hu⟩

theorem nonstrict_domain_certificate_attempt (hc : CenterOffsetTarget)
    (hw : SourceWeightsTarget (3 / 20 : ℝ) (1 / 60 : ℝ))
    (D : Set Config) (R : Config → FrontBlock)
    (he : ExactPhysicalFamily D R) (hpsd : UniformMargin D R 0) :
    SourceDomainMarginCertificate D R 0 :=
  ⟨hc, hw, he, DomainMarginRequest.nonstrict rfl, hpsd⟩

/- Puncturing the domain only changes membership. It preserves an already
   proved margin under restriction, never creates or increases a margin. -/
def punctured (D : Set Config) : Set Config := D \ {0}

theorem punctured_excludes_zero_attempt (D : Set Config) : (0 : Config) ∉ punctured D := by
  simp [punctured]

theorem existing_margin_restricts_attempt (D : Set Config) (R : Config → FrontBlock) (mu : ℝ)
    (hu : UniformMargin D R mu) : UniformMargin (punctured D) R mu :=
  uniform_restrict_attempt (punctured D) D R mu (fun _ hq => hq.1) hu

/- Counterexample to sufficiency of zero exclusion: an abstract family only,
   not body-6 source data. q_n now has first coordinate n+1, hence is never zero. -/
def awayCounterDomain : Set Config := Set.range (fun n : ℕ => counterConfig (n + 1))

theorem away_counter_excludes_zero_attempt : (0 : Config) ∉ awayCounterDomain := by
  rintro ⟨n, hn⟩
  have hv : (n : ℝ) + 1 = 0 := by
    simpa [counterConfig, Nat.cast_add, Nat.cast_one] using congrFun hn (0 : Fin 6)
  have hnn : 0 ≤ (n : ℝ) := Nat.cast_nonneg n
  linarith

theorem away_counter_pointwise_positive_attempt :
    ∀ q ∈ awayCounterDomain, ∃ rho : ℝ, 0 < rho ∧ RemainderMargin (counterR q) rho := by
  intro q hq
  rcases hq with ⟨n, rfl⟩
  exact counter_pointwise_positive_attempt (counterConfig (n + 1)) ⟨n + 1, rfl⟩

theorem away_counter_no_uniform_positive_attempt :
    ¬ ∃ mu : ℝ, 0 < mu ∧ UniformMargin awayCounterDomain counterR mu := by
  rintro ⟨mu, hp, hu⟩
  obtain ⟨n, hn⟩ := exists_nat_gt ((1 : ℝ) / mu)
  have hprod : (1 : ℝ) < (n : ℝ) * mu := (div_lt_iff₀ hp).mp hn
  have hden : 0 < (n : ℝ) + 1 + 1 := by positivity
  have hsmall : (1 : ℝ) / ((n : ℝ) + 1 + 1) < mu := by
    apply (div_lt_iff₀ hden).2
    nlinarith
  have hm : RemainderMargin (scalarIdentity (1 / ((n : ℝ) + 1 + 1))) mu := by
    simpa [counterR, counterConfig, Nat.cast_add, Nat.cast_one] using hu (counterConfig (n + 1)) ⟨n, rfl⟩
  exact (not_le_of_gt hsmall) (scalar_margin_upper_attempt _ mu hm)

/- Choosing the nonstrict request is not itself a PSD proof, even abstractly. -/
theorem zero_request_does_not_prove_psd_attempt : ¬ RemainderMargin (scalarIdentity (-1)) 0 := by
  intro hm
  have hbad := scalar_margin_upper_attempt (-1) 0 hm
  norm_num at hbad

/- Null-vector obstruction and source premises remain conditional. No domain
   exclusion-to-positive-margin implication, full PSD, coverage or admission. -/
end
end NEW_BODY6_SLICE_DOMAINREPAIR20260907

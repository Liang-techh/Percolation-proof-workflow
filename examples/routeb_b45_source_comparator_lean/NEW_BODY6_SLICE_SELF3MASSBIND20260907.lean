import NEW_BODY6_SLICE_SOURCEBLOCKBIND20260907
import NEW_BODY6_SLICE_SELF3_Source20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_SELF3MASSBIND20260907

noncomputable section

open NEW_BODY6_SLICE_LEVER_Source20260907 NEW_BODY6_SLICE_VGRAM_Source20260907
open NEW_BODY6_SLICE_AXIS_Core20260907 NEW_BODY6_SLICE_MASSTAIL_Source20260907
open NEW_BODY6_SLICE_SELF3_Core20260907 NEW_BODY6_SLICE_SELF3_Source20260907
open NEW_BODY6_SLICE_SOURCEBLOCKBIND20260907 RouteBO1PerBodyExactSource

/- UNCOMPILED: real mass = mass-weighted velocity Gram + scalar inertia Gram.
   All nine entries have typed front indices 0,1,2. No geometry is rederived. -/
def weightedA (q : Fin 6 → ℝ) (m kappa : ℝ) (i j : Fin 3) : ℝ :=
  m * selfVelocityEntry q offset i j + kappa * selfAxisEntry i j

def explicitWeightedA (q : Fin 6 → ℝ) (m kappa : ℝ) : Fin 3 → Fin 3 → ℝ :=
  let a := coeffA q offset
  let b := coeffB q offset
  let p := coeffP q offset
  let r := coeffR q offset
  let u := coeffU q offset
  let v := coeffV q offset
  ![![m * (a ^ 2 + b ^ 2) + kappa, -m * a * p, -m * a * u],
    ![-m * a * p, m * (p ^ 2 + r ^ 2) + kappa, m * (p * u + r * v) + kappa],
    ![-m * a * u, m * (p * u + r * v) + kappa, m * (u ^ 2 + v ^ 2) + kappa]]

theorem weighted_table_attempt (q : Fin 6 → ℝ) (m kappa : ℝ) (i j : Fin 3) :
    weightedA q m kappa i j = explicitWeightedA q m kappa i j := by
  fin_cases i <;> fin_cases j <;>
    norm_num [weightedA, explicitWeightedA, selfVelocityEntry, templateGram, selfAxisEntry] <;> ring

/- The mass law is an independent field: Gram identities alone cannot fill it. -/
structure SelfMassAdapter (m kappa : ℝ) : Prop where
  weightBinding : SourceWeightsTarget m kappa
  massLaw : ∀ q (i j : Fin 3), sourceA q i j =
    m * dot3 (sourceV q (firstJoint i)) (sourceV q (firstJoint j)) +
      kappa * dot3 (sourceZ q (firstJoint i)) (sourceZ q (firstJoint j))
  velocityGram : SelfVelocityTarget
  axisGram : SelfAxisTarget

theorem self_mass_adapter_attempt (hc : CenterOffsetTarget)
    (m kappa : ℝ) (hw : SourceWeightsTarget m kappa) : SelfMassAdapter m kappa := by
  refine ⟨hw, ?_, source_self_velocity_attempt hc, source_self_axis_attempt⟩
  have hm : (3 / 20 : ℝ) = m := by simpa [routeBMass] using hw.1
  have hk : (1 / 60 : ℝ) = kappa := by simpa [routeBInertiaScalar] using hw.2
  intro q i j
  unfold sourceA
  rw [source_mass_gram_attempt, hm, hk]

theorem weighted_A_binding_from_adapter_attempt (m kappa : ℝ)
    (he : SelfMassAdapter m kappa) (q : Fin 6 → ℝ) :
    FirstBlockBindingObligation q (weightedA q m kappa) := by
  intro i j
  have hlaw := he.massLaw q i j
  rw [he.velocityGram q i j, he.axisGram q i j] at hlaw
  exact hlaw.symm

theorem explicit_A_binding_attempt (hc : CenterOffsetTarget)
    (m kappa : ℝ) (hw : SourceWeightsTarget m kappa) (q : Fin 6 → ℝ) :
    FirstBlockBindingObligation q (explicitWeightedA q m kappa) := by
  have hb := weighted_A_binding_from_adapter_attempt m kappa (self_mass_adapter_attempt hc m kappa hw) q
  intro i j
  rw [← weighted_table_attempt q m kappa i j]
  exact hb i j

/- Remaining obligation for an independently supplied A; no candidate witness
   is manufactured from dimensions, raw velocity Gram, or numerical agreement. -/
def CandidateMassIdentity (q : Fin 6 → ℝ) (m kappa : ℝ) (A : Fin 3 → Fin 3 → ℝ) : Prop :=
  ∀ i j, A i j = weightedA q m kappa i j

theorem candidate_binding_iff_mass_identity_attempt (m kappa : ℝ)
    (he : SelfMassAdapter m kappa) (q : Fin 6 → ℝ) (A : Fin 3 → Fin 3 → ℝ) :
    FirstBlockBindingObligation q A ↔ CandidateMassIdentity q m kappa A := by
  have hb := weighted_A_binding_from_adapter_attempt m kappa he q
  constructor
  · intro ha i j
    exact (ha i j).trans (hb i j).symm
  · intro ha i j
    exact (ha i j).trans (hb i j)

theorem candidate_mismatch_rejects_attempt (m kappa : ℝ)
    (he : SelfMassAdapter m kappa) (q : Fin 6 → ℝ) (A : Fin 3 → Fin 3 → ℝ)
    (bad : ∃ i j, A i j ≠ weightedA q m kappa i j) : ¬ FirstBlockBindingObligation q A := by
  intro ha
  have hid := (candidate_binding_iff_mass_identity_attempt m kappa he q A).mp ha
  obtain ⟨i, j, hne⟩ := bad
  exact hne (hid i j)

/- Fill the previously open A field for this explicit table only. The source
   weight and center premises remain explicit; no Schur PSD is inferred. -/
theorem explicit_A_mixed_source_binding_attempt (hc : CenterOffsetTarget)
    (m kappa : ℝ) (hw : SourceWeightsTarget m kappa) (q : Fin 6 → ℝ) :
    SourceBlockBinding q (explicitWeightedA q m kappa) (mixedX q m kappa) (mixedY q m kappa) :=
  mixed_binding_from_A_attempt hc m kappa hw q (explicitWeightedA q m kappa)
    (explicit_A_binding_attempt hc m kappa hw q)

/- All nine canonical weighted entries are conditionally bound. Arbitrary A
   still needs CandidateMassIdentity. No unconditional center/weights, full
   matrix, Schur PSD, Fourier, coverage, Lean execution or registry admission. -/
end
end NEW_BODY6_SLICE_SELF3MASSBIND20260907

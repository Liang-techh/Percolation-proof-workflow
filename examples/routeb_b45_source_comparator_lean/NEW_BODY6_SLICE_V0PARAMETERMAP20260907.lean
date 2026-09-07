import NEW_BODY6_SLICE_COMPILEDLEDGERBINDING20260907

set_option autoImplicit false
open scoped BigOperators

namespace NEW_BODY6_SLICE_V0PARAMETERMAP20260907
noncomputable section
open NEW_BODY6_SLICE_COMPILEDLEDGERBINDING20260907

/- OPEN_UNCOMPILED. Exact scalar provenance, not a selected candidate. -/
def massUpper : ℝ := 163847401 / 96000000
def blockHessianUpper : ℝ := 24185409 / 40000000
def epsilon : ℝ := 1 / 1000
def initialRadius : ℝ := 3 / 20
def envelopeCoefficient : ℝ :=
  max (blockHessianUpper / 2) (massUpper / 2) + epsilon * massUpper / 2

theorem v0_generator_identity_attempt :
    envelopeCoefficient * initialRadius^2 = ledgerV0 := by
  norm_num [envelopeCoefficient, massUpper, blockHessianUpper, epsilon,
    initialRadius, ledgerV0]

theorem v0_base_plus_cross_budget_attempt :
    ledgerV0 = (491542203 / 25600000000 : ℝ) +
      (491542203 / 25600000000000 : ℝ) := by norm_num [ledgerV0]

/- A scalar match can be arranged for f=1,h=0 by inflating beta. It does
   not establish any equality of storage functions or select these values. -/
theorem scalar_match_only_attempt :
    (9/400 : ℝ)*(161451248401/192000000000) + 3/10000 = ledgerV0 := by
  norm_num [ledgerV0]

def normSq (v : Vec) : ℝ := ∑ i, (v i)^2
def massCross (M : Mat) (q v : Vec) : ℝ := ∑ i, q i * (∑ j, M i j * v j)

theorem targeted_gain_change_vanishes_on_block_initial_attempt (q : Vec)
    (hq2 : q 1 = 0) (hq3 : q 2 = 0) :
    (3 : ℝ)*(q 1)^2 + (q 2)^2 = 0 := by rw [hq2, hq3]; norm_num

theorem mass_cross_odd_attempt (M : Mat) (q v : Vec) :
    massCross M q (-v) = -massCross M q v := by
  simp [massCross, mul_neg, Finset.sum_neg_distrib]

theorem signed_kinetic_even_attempt (M : Mat) (v : Vec) :
    RouteBSignedGap.kinetic M (-v) = RouteBSignedGap.kinetic M v := by
  simp [RouteBSignedGap.kinetic, RouteBSignedGap.quad, RouteBSignedGap.dot,
    RouteBSignedGap.mv, mul_neg, Finset.sum_neg_distrib]

/- Concrete necessary structure: fixed f,p,h,H,M(q),U(q),Uzero,c cannot
   create an odd-in-velocity mass cross term in ActualStorage. -/
theorem actual_storage_even_attempt (f h U Uzero c : ℝ) (p q v : Vec) (H M : Mat) :
    RouteBActualEnergyStorage.storageV f p h H M U Uzero q (-v) c =
      RouteBActualEnergyStorage.storageV f p h H M U Uzero q v c := by
  simp only [RouteBActualEnergyStorage.storageV,
    RouteBActualEnergyStorage.W0_actual_energy, signed_kinetic_even_attempt]

theorem actual_shift_energy_even_attempt (M : Mat) (q v : Vec) :
    encodedShiftedEnergy M q (-v) = encodedShiftedEnergy M q v := by
  simp [encodedShiftedEnergy, RouteBShiftedStorage.kinetic, mul_neg,
    Finset.sum_neg_distrib]

/- This is a necessary identity condition, not another abstract counterexample.
   Apply at velocity-paired states in the SAME domain and SAME state map. -/
theorem same_candidate_requires_zero_cross_attempt (S E : Vec → ℝ)
    (M : Mat) (q v : Vec) (hS : S (-v) = S v) (hE : E (-v) = E v)
    (hplus : S v = E v + epsilon * massCross M q v)
    (hminus : S (-v) = E (-v) + epsilon * massCross M q (-v)) :
    massCross M q v = 0 := by
  rw [hS, hE, mass_cross_odd_attempt] at hminus
  norm_num [epsilon] at hplus hminus
  linarith

/- The scalar generator can become a bound only for an identified evaluator
   and a proved same-domain upper envelope. These are the minimal remaining
   inputs for consuming THIS bound; global storage equality is not required. -/
structure InitialEnvelopeBinding (X0 : Set (Vec × Vec))
    (V : Vec → Vec → ℝ) : Prop where
  radiusBound : ∀ x ∈ X0, normSq x.1 + normSq x.2 ≤ initialRadius^2
  storageEnvelope : ∀ x ∈ X0,
    V x.1 x.2 ≤ envelopeCoefficient * (normSq x.1 + normSq x.2)

theorem envelope_delivers_v0_attempt (X0 : Set (Vec × Vec))
    (V : Vec → Vec → ℝ) (h : InitialEnvelopeBinding X0 V) :
    ∀ x ∈ X0, V x.1 x.2 ≤ ledgerV0 := by
  intro x hx
  have hp : 0 ≤ envelopeCoefficient := by
    norm_num [envelopeCoefficient, massUpper, blockHessianUpper, epsilon]
  have hb := mul_le_mul_of_nonneg_left (h.radiusBound x hx) hp
  rw [v0_generator_identity_attempt] at hb
  exact (h.storageEnvelope x hx).trans hb

structure CandidateInitialBinding (X0 : Set (Vec × Vec))
    (Vexport Vledger : Vec → Vec → ℝ) : Prop where
  exportEnvelope : InitialEnvelopeBinding X0 Vexport
  sameInitialStorage : ∀ x ∈ X0, Vledger x.1 x.2 = Vexport x.1 x.2

theorem candidate_v0_transfer_attempt (X0 : Set (Vec × Vec))
    (Vexport Vledger : Vec → Vec → ℝ) (h : CandidateInitialBinding X0 Vexport Vledger) :
    ∀ x ∈ X0, Vledger x.1 x.2 ≤ ledgerV0 := by
  intro x hx
  rw [h.sameInitialStorage x hx]
  exact envelope_delivers_v0_attempt X0 Vexport h.exportEnvelope x hx

/- No current candidate identity, envelope, controller choice, source-to-flow
   binding, compilation or registry promotion is asserted. -/
end
end NEW_BODY6_SLICE_V0PARAMETERMAP20260907

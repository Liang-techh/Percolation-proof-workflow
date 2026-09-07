import NEW_KPATH_INTERFACE_Core

/-!
T-P5-029 -- UNCOMPILED SOURCE-INDEPENDENT PROOF SKELETON.
No Lean/Lake execution, no concrete K/source/kappa/gamma or SPN instance.
A/B below are ABSOLUTE CONE MAPS, not the upstream force-normalization map.
P5FeasibleConeSPN must resolve to the generic sidecar inherited by Core.
-/

set_option autoImplicit false

namespace RouteBP5SPNIncrement

open scoped BigOperators
open RouteBP5KPathInterface

abbrev ConeIndex := RouteBP5ConeIndex.ConeIndex
abbrev Representative := RouteBP5ConeIndex.Representative

noncomputable section

def mapVec {m n : ℕ} (A : Fin m → Fin n → ℝ) (u : Fin n → ℝ) : Fin m → ℝ :=
  fun i => ∑ j, A i j * u j

/-- B^T E A, with dimensions B:2x4, E:2x4, A:4x4. -/
def rawCorrection (A : Mat) (B E : Gain) : Mat :=
  fun i j => ∑ a, ∑ k, B a i * E a k * A k j

def correction (A : Mat) (B E : Gain) : Mat :=
  fun i j => (rawCorrection A B E i j + rawCorrection A B E j i) / 2

theorem correction_symmetric (A : Mat) (B E : Gain) (i j : Fin 4) :
    correction A B E i j = correction A B E j i := by
  unfold correction; ring

/-- Entrywise nonnegativity, not IsPSD and not a Loewner-order assertion. -/
theorem correction_nonnegative (A : Mat) (B E : Gain)
    (hA : ∀ i j, 0 ≤ A i j) (hB : ∀ a i, 0 ≤ B a i)
    (hE : ∀ a k, 0 ≤ E a k) : ∀ i j, 0 ≤ correction A B E i j := by
  have hM : ∀ i j, 0 ≤ rawCorrection A B E i j := by
    intro i j
    exact Finset.sum_nonneg (fun a _ => Finset.sum_nonneg (fun k _ =>
      mul_nonneg (mul_nonneg (hB a i) (hE a k)) (hA k j)))
  intro i j
  exact div_nonneg (add_nonneg (hM i j) (hM j i)) (by norm_num)

/-- Pure finite-sum algebra: valid for EVERY real u, without sign assumptions.
Identification with the actual absolute envelope is a separate orthant theorem. -/
theorem correction_quad (A : Mat) (B E : Gain) (u : Vec) :
    RouteBP5FeasibleConeSPN.quad (correction A B E) u =
      ∑ a, mapVec B u a * (∑ k, E a k * mapVec A u k) := by
  simp [RouteBP5FeasibleConeSPN.quad, correction, rawCorrection, mapVec,
    Fin.sum_univ_succ]
  <;> ring

def addGain (K E : NonnegativeGain) : NonnegativeGain where
  value a k := K.value a k + E.value a k
  nonnegative a k := add_nonneg (K.nonnegative a k) (E.nonnegative a k)

theorem envelope_add (K E : NonnegativeGain) (z : Vec) :
    RouteBP5FeasibleConeSPN.absEnvelope (addGain K E).value (channelSum z) z =
      RouteBP5FeasibleConeSPN.absEnvelope K.value (channelSum z) z +
      RouteBP5FeasibleConeSPN.absEnvelope E.value (channelSum z) z := by
  simp [addGain, RouteBP5FeasibleConeSPN.absEnvelope,
    RouteBP5FeasibleConeSPN.rowEnvelope, add_mul, mul_add, Finset.sum_add_distrib]

/-- Explicit geometry obligations; no concrete chart matrices supplied here.
Global-sign invariance of A/B is required for the updated 18-representative API. -/
structure AbsoluteConeMaps where
  A : ConeIndex → Mat
  B : ConeIndex → Gain
  a_nonnegative : ∀ c i j, 0 ≤ A c i j
  b_nonnegative : ∀ c a j, 0 ≤ B c a j
  state_abs : ∀ c u, RouteBP5ConeIndex.Orthant u → ∀ k,
    |RouteBP5ConeIndex.chart c u k| = mapVec (A c) u k
  channel_abs : ∀ c u, RouteBP5ConeIndex.Orthant u → ∀ a,
    |channelSum (RouteBP5ConeIndex.chart c u) a| = mapVec (B c) u a
  a_flip : ∀ c, A (RouteBP5ConeIndex.flip c) = A c
  b_flip : ∀ c, B (RouteBP5ConeIndex.flip c) = B c

theorem correction_envelope (maps : AbsoluteConeMaps) (E : NonnegativeGain)
    (c : ConeIndex) (u : Vec) (hu : RouteBP5ConeIndex.Orthant u) :
    RouteBP5FeasibleConeSPN.absEnvelope E.value
      (channelSum (RouteBP5ConeIndex.chart c u)) (RouteBP5ConeIndex.chart c u) =
      RouteBP5FeasibleConeSPN.quad (correction (maps.A c) (maps.B c) E.value) u := by
  rw [correction_quad]
  unfold RouteBP5FeasibleConeSPN.absEnvelope RouteBP5FeasibleConeSPN.rowEnvelope
  simp_rw [maps.state_abs c u hu, maps.channel_abs c u hu]

theorem quad_sub (H C : Mat) (u : Vec) :
    RouteBP5FeasibleConeSPN.quad (fun i j => H i j - C i j) u =
      RouteBP5FeasibleConeSPN.quad H u - RouteBP5FeasibleConeSPN.quad C u := by
  simp [RouteBP5FeasibleConeSPN.quad, mul_sub, sub_mul, Finset.sum_sub_distrib]

/-- Construct the CANONICAL updated gap H-C. Equality to a separately exported
H_plus matrix is not inferred merely from equality of quadratic forms. -/
def updatedGap {K : NonnegativeGain} {Q : Vec → ℝ} {mu : ℝ}
    (base : ConeGapBinding K Q mu) (maps : AbsoluteConeMaps) (E : NonnegativeGain) :
    ConeGapBinding (addGain K E) Q mu where
  H c i j := base.H c i j - correction (maps.A c) (maps.B c) E.value i j
  flip_eq c := by
    simp only [base.flip_eq, maps.a_flip, maps.b_flip]
  exact_gap c u hu := by
    rw [envelope_add, quad_sub, ← base.exact_gap c u hu,
      ← correction_envelope maps E c u hu]
    ring

/-- This is the exact condition for this FIXED N-only subtraction, not a
necessary condition for existence of another SPN decomposition. -/
theorem fixed_slack_iff (N C : Mat) :
    (∀ i j, 0 ≤ N i j - C i j) ↔ ∀ i j, C i j ≤ N i j := by
  simp only [sub_nonneg]

/-- Keep the same S and the same PSD proof. The subtraction algebra needs only
C<=N; positivity of the physical correction is established separately above. -/
def chargeN {H : Mat} (old : SPNWitness H) (C : Mat)
    (charge : ∀ i j, C i j ≤ old.N i j) :
    SPNWitness (fun i j => H i j - C i j) where
  S := old.S
  N i j := old.N i j - C i j
  decomposition i j := by rw [old.decomposition i j]; ring
  psd := old.psd
  entrywise i j := sub_nonneg.mpr (charge i j)

theorem chargeN_same_S {H : Mat} (old : SPNWitness H) (C : Mat)
    (charge : ∀ i j, C i j ≤ old.N i j) : (chargeN old C charge).S = old.S := rfl

/-- Representative-local slack checks produce all 18 updated certificates.
Existing liftSPN then supplies all 36 labels using updatedGap.flip_eq. -/
def updatedRepresentatives {K : NonnegativeGain} {Q : Vec → ℝ} {mu : ℝ}
    (base : ConeGapBinding K Q mu) (maps : AbsoluteConeMaps) (E : NonnegativeGain)
    (old : ∀ r : Representative,
      SPNWitness (base.H (RouteBP5ConeIndex.representativeCone r)))
    (charge : ∀ r i j,
      correction (maps.A (RouteBP5ConeIndex.representativeCone r))
        (maps.B (RouteBP5ConeIndex.representativeCone r)) E.value i j ≤ (old r).N i j) :
    ∀ r : Representative,
      SPNWitness ((updatedGap base maps E).H (RouteBP5ConeIndex.representativeCone r)) :=
  fun r => chargeN (old r)
    (correction (maps.A (RouteBP5ConeIndex.representativeCone r))
      (maps.B (RouteBP5ConeIndex.representativeCone r)) E.value) (charge r)

theorem updated_direct_envelope {K : NonnegativeGain} {Q : Vec → ℝ} {mu : ℝ}
    (base : ConeGapBinding K Q mu) (maps : AbsoluteConeMaps) (E : NonnegativeGain)
    (old : ∀ r : Representative,
      SPNWitness (base.H (RouteBP5ConeIndex.representativeCone r)))
    (charge : ∀ r i j,
      correction (maps.A (RouteBP5ConeIndex.representativeCone r))
        (maps.B (RouteBP5ConeIndex.representativeCone r)) E.value i j ≤ (old r).N i j) :
    ∀ z, RouteBP5FeasibleConeSPN.absEnvelope (addGain K E).value (channelSum z) z ≤
      mu * Q z :=
  direct_envelope (updatedGap base maps E) (updatedRepresentatives base maps E old charge)

def rankOne (kappa : Force) (gamma : Vec) : Gain := fun a k => kappa a * gamma k

def rankOneGain (kappa : Force) (gamma : Vec)
    (hk : ∀ a, 0 ≤ kappa a) (hg : ∀ k, 0 ≤ gamma k) : NonnegativeGain where
  value := rankOne kappa gamma
  nonnegative a k := mul_nonneg (hk a) (hg k)

def alpha (B : Gain) (kappa : Force) : Vec := fun i => ∑ a, B a i * kappa a
def beta (A : Mat) (gamma : Vec) : Vec := fun j => ∑ k, A k j * gamma k

theorem alpha_beta_nonnegative (A : Mat) (B : Gain) (kappa : Force) (gamma : Vec)
    (hA : ∀ i j, 0 ≤ A i j) (hB : ∀ a i, 0 ≤ B a i)
    (hk : ∀ a, 0 ≤ kappa a) (hg : ∀ k, 0 ≤ gamma k) :
    (∀ i, 0 ≤ alpha B kappa i) ∧ (∀ j, 0 ≤ beta A gamma j) := by
  constructor
  · intro i
    exact Finset.sum_nonneg (fun a _ => mul_nonneg (hB a i) (hk a))
  · intro j
    exact Finset.sum_nonneg (fun k _ => mul_nonneg (hA k j) (hg k))

theorem rankOne_raw (A : Mat) (B : Gain) (kappa : Force) (gamma : Vec) (i j : Fin 4) :
    rawCorrection A B (rankOne kappa gamma) i j = alpha B kappa i * beta A gamma j := by
  unfold rawCorrection rankOne alpha beta
  rw [Finset.sum_mul]
  apply Finset.sum_congr rfl
  intro a _
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro k _
  ring

theorem rankOne_correction (A : Mat) (B : Gain) (kappa : Force) (gamma : Vec)
    (i j : Fin 4) :
    correction A B (rankOne kappa gamma) i j =
      (alpha B kappa i * beta A gamma j + beta A gamma i * alpha B kappa j) / 2 := by
  unfold correction
  rw [rankOne_raw, rankOne_raw]
  ring

/-- Algebraic factorization for all real u; positivity of the two factors is
available on u>=0 when A,B,kappa,gamma are entrywise nonnegative. -/
theorem rankOne_quad (A : Mat) (B : Gain) (kappa : Force) (gamma : Vec) (u : Vec) :
    RouteBP5FeasibleConeSPN.quad (correction A B (rankOne kappa gamma)) u =
      (∑ i, alpha B kappa i * u i) * (∑ j, beta A gamma j * u j) := by
  simp [RouteBP5FeasibleConeSPN.quad, rankOne_correction, Fin.sum_univ_succ]
  <;> ring

/-- Division-free entrywise test; zero N entries are handled without ratios. -/
theorem rankOne_charge_iff (A : Mat) (B : Gain) (kappa : Force) (gamma : Vec)
    (N : Mat) (i j : Fin 4) :
    correction A B (rankOne kappa gamma) i j ≤ N i j ↔
      alpha B kappa i * beta A gamma j + beta A gamma i * alpha B kappa j ≤ 2 * N i j := by
  rw [rankOne_correction]
  constructor <;> intro h <;> linarith

def chargeRankOne {H : Mat} (old : SPNWitness H) (A : Mat) (B : Gain)
    (kappa : Force) (gamma : Vec)
    (charge : ∀ i j, alpha B kappa i * beta A gamma j +
      beta A gamma i * alpha B kappa j ≤ 2 * old.N i j) :
    SPNWitness (fun i j => H i j - correction A B (rankOne kappa gamma) i j) :=
  chargeN old _ (fun i j => (rankOne_charge_iff A B kappa gamma old.N i j).mpr (charge i j))

end

/-- Local candidate states only; not a registry status or automatic checker.
Insufficient fixed slack does not assert failure of another SPN/PSD decomposition. -/
inductive PendingReason where
  | missingBinding | missingOldWitness | missingSlackProof | fixedNSlackInsufficient
  | buildNotVerified

inductive ReuseAttempt (Hnew : Mat) where
  | pending : PendingReason → ReuseAttempt Hnew
  | witness : SPNWitness Hnew → ReuseAttempt Hnew

-- Future audit commands only; these have NOT been run in this round.
#print axioms correction_nonnegative
#print axioms correction_quad
#print axioms correction_envelope
#print axioms updatedGap
#print axioms chargeN
#print axioms chargeN_same_S
#print axioms updated_direct_envelope
#print axioms rankOne_raw
#print axioms rankOne_correction
#print axioms rankOne_quad
#print axioms chargeRankOne

end RouteBP5SPNIncrement

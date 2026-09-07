import NEW_KPATH_INTERFACE_RationalBinding

/-!
UNCOMPILED SOURCE-INDEPENDENT PROOF SKELETON.
No Lean/Lake run or kernel receipt for this file. No concrete gain instance.
The JSON checker does not construct EightComparisons or SlotBinding below:
checked rational data must be reflected as proofs, with exact real identities.
The inherited P5FeasibleConeSPN import must resolve to the GENERIC sidecar,
not the same-named file in this directory; see the companion review.
-/

set_option autoImplicit false

namespace RouteBP5KPathFinClosure

open scoped BigOperators
open RouteBP5KPathInterface

abbrev Slot := Fin 8
abbrev Entry := Fin 2 × Fin 4
abbrev ConeIndex := RouteBP5ConeIndex.ConeIndex
abbrev Representative := RouteBP5ConeIndex.Representative

/-- Checker traversal: force row first, then x4,x5,y4,y5 within that row. -/
def decode (s : Slot) : Entry :=
  ![(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3)] s

def encode (p : Entry) : Slot := ⟨4 * p.1.val + p.2.val, by omega⟩

@[simp] theorem encode_decode (s : Slot) : encode (decode s) = s := by
  revert s; decide

@[simp] theorem decode_encode (p : Entry) : decode (encode p) = p := by
  revert p; decide

def slotEquiv : Slot ≃ Entry where
  toFun := decode
  invFun := encode
  left_inv := encode_decode
  right_inv := decode_encode

/-- Reindex every slot exactly once; never identify slots by their values. -/
theorem sum_slots {A : Type*} [AddCommMonoid A] (f : Fin 2 → Fin 4 → A) :
    (∑ s : Slot, f (decode s).1 (decode s).2) = ∑ a, ∑ j, f a j := by
  calc
    _ = ∑ p : Entry, f p.1 p.2 := slotEquiv.sum_comp (fun p => f p.1 p.2)
    _ = _ := Fintype.sum_prod_type

/-- All eight rational obligations, not a list of flags or a cardinality test.
The exporter must retain the exact canonical input tables and row-major order. -/
structure EightComparisons where
  path : Slot → ℚ
  cert : Slot → ℚ
  path_nonnegative : ∀ s, 0 ≤ path s
  cert_nonnegative : ∀ s, 0 ≤ cert s
  comparison : ∀ s, path s ≤ cert s

/-- Exact semantic identification with the SAME real K and G used downstream.
K is intended to be transportedGain; no equality follows from a SHA or JSON flag. -/
structure SlotBinding (K G : NonnegativeGain) where
  eight : EightComparisons
  path_entry_eq : ∀ a j, K.value a j = (eight.path (encode (a, j)) : ℝ)
  cert_entry_eq : ∀ a j, G.value a j = (eight.cert (encode (a, j)) : ℝ)

def SlotBinding.toRationalBinding {K G : NonnegativeGain} (b : SlotBinding K G) :
    RouteBP5KPathRationalBinding.ExactComparisonBinding K G where
  pathTable a j := b.eight.path (encode (a, j))
  certTable a j := b.eight.cert (encode (a, j))
  path_nonnegative a j := b.eight.path_nonnegative (encode (a, j))
  cert_nonnegative a j := b.eight.cert_nonnegative (encode (a, j))
  comparison a j := b.eight.comparison (encode (a, j))
  path_entry_eq := b.path_entry_eq
  cert_entry_eq := b.cert_entry_eq

theorem SlotBinding.toComponentLE {K G : NonnegativeGain} (b : SlotBinding K G) :
    ComponentLE K.value G.value :=
  b.toRationalBinding.toComponentLE

noncomputable section

/-- An individual contribution to the power-envelope slack, not an H entry. -/
def slotSlack (K G : NonnegativeGain) (z : Vec) (s : Slot) : ℝ :=
  |channelSum z (decode s).1| *
    (G.value (decode s).1 (decode s).2 - K.value (decode s).1 (decode s).2) *
    |z (decode s).2|

theorem slotSlack_nonnegative {K G : NonnegativeGain} (b : SlotBinding K G)
    (z : Vec) (s : Slot) : 0 ≤ slotSlack K G z s := by
  exact mul_nonneg
    (mul_nonneg (abs_nonneg _)
      (sub_nonneg.mpr (b.toComponentLE (decode s).1 (decode s).2)))
    (abs_nonneg _)

/-- Expose the eight-term sum consumed by the existing finite-sum envelope. -/
theorem envelope_slack_sum (K G : NonnegativeGain) (z : Vec) :
    RouteBP5FeasibleConeSPN.absEnvelope G.value (channelSum z) z -
      RouteBP5FeasibleConeSPN.absEnvelope K.value (channelSum z) z =
      ∑ s : Slot, slotSlack K G z s := by
  unfold slotSlack
  rw [sum_slots]
  simp [RouteBP5FeasibleConeSPN.absEnvelope, RouteBP5FeasibleConeSPN.rowEnvelope,
    Finset.mul_sum, mul_sub, sub_mul, Finset.sum_sub_distrib, mul_assoc]

theorem envelope_slack_nonnegative {K G : NonnegativeGain} (b : SlotBinding K G)
    (z : Vec) :
    0 ≤ RouteBP5FeasibleConeSPN.absEnvelope G.value (channelSum z) z -
      RouteBP5FeasibleConeSPN.absEnvelope K.value (channelSum z) z := by
  rw [envelope_slack_sum]
  exact Finset.sum_nonneg (fun s _ => slotSlack_nonnegative b z s)

/-- The two finite index systems are independent: 36 cone labels, 8 entries.
Value coincidences (including all-zero gains) do not change these counts. -/
theorem cone_slot_counts :
    Fintype.card (ConeIndex × Slot) = 288 ∧
      Fintype.card (Representative × Slot) = 144 := by decide

/-- Retain both directions even for weights that are NOT flip-invariant.
This is a sum identity, not a replacement for a separate proof on EACH cone. -/
theorem cone_slot_sum_preserving (w : ConeIndex → Slot → ℝ) :
    (∑ c : ConeIndex, ∑ s : Slot, w c s) =
      ∑ r : Representative,
        ((∑ s : Slot, w (RouteBP5ConeIndex.representativeCone r) s) +
         (∑ s : Slot, w (RouteBP5ConeIndex.flip
            (RouteBP5ConeIndex.representativeCone r)) s)) :=
  RouteBP5ConeIndex.sum_preserving_multiplicity (fun c => ∑ s : Slot, w c s)

/-- Doubling requires an additional invariance proof; labels alone do not give it. -/
theorem cone_slot_sum_invariant (w : ConeIndex → Slot → ℝ)
    (hflip : ∀ c s, w (RouteBP5ConeIndex.flip c) s = w c s) :
    (∑ c : ConeIndex, ∑ s : Slot, w c s) =
      ∑ r : Representative, (2 : ℕ) •
        (∑ s : Slot, w (RouteBP5ConeIndex.representativeCone r) s) := by
  apply RouteBP5ConeIndex.sum_invariant
  intro c
  exact Finset.sum_congr rfl (fun s _ => hflip c s)

/-- Actual dependent certificate lifting along H(flip c)=H(c), not by matrix-value
deduplication. No claim that the lifted S/N data themselves have a canonical form. -/
def allConeWitnesses {G : NonnegativeGain} {Q : Vec → ℝ} {mu : ℝ}
    (gap : ConeGapBinding G Q mu)
    (cert : ∀ r : Representative,
      SPNWitness (gap.H (RouteBP5ConeIndex.representativeCone r))) :
    ∀ c : ConeIndex, SPNWitness (gap.H c) :=
  liftSPN gap cert

/-- Per-cone, per-vector nonnegativity is used; positivity of a SUM of cone
values would not suffice. The existing SPN theorem sums nonnegative N terms. -/
theorem every_cone_nonnegative {G : NonnegativeGain} {Q : Vec → ℝ} {mu : ℝ}
    (gap : ConeGapBinding G Q mu)
    (cert : ∀ r : Representative,
      SPNWitness (gap.H (RouteBP5ConeIndex.representativeCone r)))
    (c : ConeIndex) (u : Vec) (hu : RouteBP5ConeIndex.Orthant u) :
    0 ≤ RouteBP5FeasibleConeSPN.quad (gap.H c) u := by
  let witness := allConeWitnesses gap cert c
  exact RouteBP5FeasibleConeSPN.spn_quadratic_nonnegative_on_orthant
    (gap.H c) witness.S witness.N witness.decomposition witness.psd witness.entrywise u hu

/-- Smallest public consumer: eight exact comparisons, exact table identities,
same-domain component residual bound, gap binding and 18 proof-valued witnesses. -/
theorem typed_spn_power {X : Type*} {D : X → Prop}
    {z : X → Vec} {rc : X → Force} {K G : NonnegativeGain}
    {Q : Vec → ℝ} {mu : ℝ}
    (source : ComponentBinding D z rc K) (b : SlotBinding K G)
    (gap : ConeGapBinding G Q mu)
    (cert : ∀ r : Representative,
      SPNWitness (gap.H (RouteBP5ConeIndex.representativeCone r)))
    (x : X) (hx : D x) :
    |RouteBP5FeasibleConeSPN.residualPower (channelSum (z x)) (rc x)| ≤ mu * Q (z x) :=
  componentwise_spn_power source b.toComponentLE gap cert x hx

/-- Bind K syntactically to the EXISTING pathK through transportedGain.
Source/path premises are arguments, not supplied data or inferred coverage. -/
theorem path_spn_power {X : Type*} {R m n : ℕ}
    {D : X → Prop} {z : X → Vec} {rc : X → Force}
    {A : Fin 2 → Fin m → ℝ}
    {Hjac : Fin R → Fin m → Fin n → ℝ}
    {Scoord : Fin R → Fin n → Fin 4 → ℝ}
    {G : NonnegativeGain} {Q : Vec → ℝ} {mu : ℝ}
    (path : PathBinding D z rc A Hjac Scoord)
    (b : SlotBinding (transportedGain A Hjac Scoord path.hH path.hS) G)
    (gap : ConeGapBinding G Q mu)
    (cert : ∀ r : Representative,
      SPNWitness (gap.H (RouteBP5ConeIndex.representativeCone r)))
    (x : X) (hx : D x) :
    |RouteBP5FeasibleConeSPN.residualPower (channelSum (z x)) (rc x)| ≤ mu * Q (z x) :=
  typed_spn_power path.toComponentBinding b gap cert x hx

end

-- Audit commands for a FUTURE authorized build, not current verification output.
#print axioms slotEquiv
#print axioms sum_slots
#print axioms SlotBinding.toComponentLE
#print axioms envelope_slack_nonnegative
#print axioms cone_slot_counts
#print axioms cone_slot_sum_preserving
#print axioms cone_slot_sum_invariant
#print axioms allConeWitnesses
#print axioms every_cone_nonnegative
#print axioms typed_spn_power
#print axioms path_spn_power

end RouteBP5KPathFinClosure

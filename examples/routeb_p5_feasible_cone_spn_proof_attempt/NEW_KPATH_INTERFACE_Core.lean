import NEW_CONE_INDEX_Core
import P5FeasibleConeSPN
import P5PiecewiseTransport

/-!
Conditional, source-independent componentwise K_path binding.
P5FeasibleConeSPN here means the GENERIC sidecar in
examples/routeb_p5_feasible_cone_spn_lean, NOT the same-named proof attempt.
The companion verifier checks the three frozen sources and this file together
through Lean --stdin, without generating or changing dependency artifacts.
No concrete gain, source domain, source calculus, or SPN witness is supplied.
-/

set_option autoImplicit false

namespace RouteBP5KPathInterface

open scoped BigOperators

noncomputable section

abbrev Vec := Fin 4 → ℝ
abbrev Force := Fin 2 → ℝ
abbrev Gain := Fin 2 → Fin 4 → ℝ
abbrev Mat := Fin 4 → Fin 4 → ℝ

/-- State slots are x4,x5,y4,y5; force slots are block channels 4,5. -/
def channelSum (z : Vec) : Force := ![z 0 + z 2, z 1 + z 3]

structure NonnegativeGain where
  value : Gain
  nonnegative : ∀ a j, 0 ≤ value a j

def ComponentLE (K G : Gain) : Prop := ∀ a j, K a j ≤ G a j

theorem row_mono {K G : Gain} (h : ComponentLE K G) (z : Vec) (a : Fin 2) :
    RouteBP5FeasibleConeSPN.rowEnvelope K z a ≤ RouteBP5FeasibleConeSPN.rowEnvelope G z a := by
  exact Finset.sum_le_sum (fun j _ => mul_le_mul_of_nonneg_right (h a j) (abs_nonneg _))

theorem envelope_mono {K G : Gain} (h : ComponentLE K G) (z : Vec) :
    RouteBP5FeasibleConeSPN.absEnvelope K (channelSum z) z ≤ RouteBP5FeasibleConeSPN.absEnvelope G (channelSum z) z := by
  exact Finset.sum_le_sum (fun a _ =>
    mul_le_mul_of_nonneg_left (row_mono h z a) (abs_nonneg _))

/-- For all-state ROW envelopes this comparison is exact: coordinate basis
vectors recover each entry. No necessity for the weaker power-only test is claimed. -/
theorem component_le_iff_rows (K G : Gain) :
    ComponentLE K G ↔ ∀ z a,
      RouteBP5FeasibleConeSPN.rowEnvelope K z a ≤
        RouteBP5FeasibleConeSPN.rowEnvelope G z a := by
  constructor
  · exact fun h z a => row_mono h z a
  · intro h a j
    have hj := h (Pi.single j 1) a
    simpa [RouteBP5FeasibleConeSPN.rowEnvelope, Pi.single_apply, apply_ite, mul_ite] using hj

/-- D is a predicate on the full source witness (which may include time,
parameters and path data). Naming D does not prove it covers any trajectory.
This bound is on the centered residual only; no additive bias is absorbed. -/
structure ComponentBinding {X : Type*} (D : X → Prop)
    (z : X → Vec) (rc : X → Force) (K : NonnegativeGain) : Prop where
  bound : ∀ x, D x → ∀ a, |rc x a| ≤ RouteBP5FeasibleConeSPN.rowEnvelope K.value (z x) a

/-- A nonzero centered-at-origin defect cannot be hidden in any finite gain. -/
theorem ComponentBinding.zero_at_origin {X : Type*} {D : X → Prop}
    {z : X → Vec} {rc : X → Force} {K : NonnegativeGain}
    (b : ComponentBinding D z rc K) (x : X) (hx : D x) (hz : z x = 0) :
    rc x = 0 := by
  funext a
  have hzero : |rc x a| ≤ 0 := by
    simpa [hz, RouteBP5FeasibleConeSPN.rowEnvelope] using b.bound x hx a
  exact abs_eq_zero.mp (le_antisymm hzero (abs_nonneg _))

theorem ComponentBinding.weaken {X : Type*} {D : X → Prop}
    {z : X → Vec} {rc : X → Force} {K G : NonnegativeGain}
    (b : ComponentBinding D z rc K) (h : ComponentLE K.value G.value) :
    ComponentBinding D z rc G where
  bound x hx a := (b.bound x hx a).trans (row_mono h (z x) a)

/-- This uses the existing exact finite pathK formula, not a replacement table.
Hjac is a nonnegative increment/Jacobian budget; it is NOT the cone gap H. -/
def transportedGain {R m n : ℕ}
    (A : Fin 2 → Fin m → ℝ)
    (Hjac : Fin R → Fin m → Fin n → ℝ)
    (Scoord : Fin R → Fin n → Fin 4 → ℝ)
    (hH : ∀ s i j, 0 ≤ Hjac s i j)
    (hS : ∀ s j k, 0 ≤ Scoord s j k) : NonnegativeGain where
  value := RouteBP5PiecewiseTransport.pathK (fun a i => |A a i|) Hjac Scoord
  nonnegative a k := by
    apply Finset.sum_nonneg
    intro s _
    apply Finset.sum_nonneg
    intro i _
    apply Finset.sum_nonneg
    intro j _
    exact mul_nonneg (abs_nonneg _) (mul_nonneg (hH s i j) (hS s j k))

/-- Full same-witness premises required from the source/path lane.
A acts exactly once. force_eq concerns the actual centered residual and the
same increments de used in the local bound; no endpoint/path inference occurs. -/
structure PathBinding {X : Type*} {R m n : ℕ}
    (D : X → Prop) (z : X → Vec) (rc : X → Force)
    (A : Fin 2 → Fin m → ℝ)
    (Hjac : Fin R → Fin m → Fin n → ℝ)
    (Scoord : Fin R → Fin n → Fin 4 → ℝ) where
  dxi : X → Fin R → Fin n → ℝ
  de : X → Fin R → Fin m → ℝ
  hH : ∀ s i j, 0 ≤ Hjac s i j
  hS : ∀ s j k, 0 ≤ Scoord s j k
  state_bound : ∀ x, D x → ∀ s j,
    |dxi x s j| ≤ ∑ k, Scoord s j k * |z x k|
  increment_bound : ∀ x, D x → ∀ s i,
    |de x s i| ≤ ∑ j, Hjac s i j * |dxi x s j|
  force_eq : ∀ x, D x → ∀ a,
    rc x a = RouteBP5PiecewiseTransport.forceMap A (fun i => ∑ s, de x s i) a

theorem PathBinding.toComponentBinding {X : Type*} {R m n : ℕ}
    {D : X → Prop} {z : X → Vec} {rc : X → Force}
    {A : Fin 2 → Fin m → ℝ}
    {Hjac : Fin R → Fin m → Fin n → ℝ}
    {Scoord : Fin R → Fin n → Fin 4 → ℝ}
    (b : PathBinding D z rc A Hjac Scoord) :
    ComponentBinding D z rc (transportedGain A Hjac Scoord b.hH b.hS) where
  bound x hx := by
    apply RouteBP5PiecewiseTransport.piecewise_component_transport
      (fun a i => |A a i|) Hjac Scoord (b.dxi x) (z x) (b.de x) (rc x)
    · intro a i; exact abs_nonneg _
    · exact b.hH
    · exact b.state_bound x hx
    · exact b.increment_bound x hx
    · intro a
      rw [b.force_eq x hx a]
      exact RouteBP5PiecewiseTransport.forceMap_piecewise_abs_le A (b.de x) a

/-- An exact, indexed H/K_cert binding. Q and mu are shared by all cones.
The gap identity and matrix flip equality must be proved by the exporter;
neither is inferred from an H name, an index label, or a numerical table. -/
structure ConeGapBinding (G : NonnegativeGain) (Q : Vec → ℝ) (mu : ℝ) where
  H : RouteBP5ConeIndex.ConeIndex → Mat
  flip_eq : ∀ c, H (RouteBP5ConeIndex.flip c) = H c
  exact_gap : ∀ c u, RouteBP5ConeIndex.Orthant u →
    mu * Q (RouteBP5ConeIndex.chart c u) - RouteBP5FeasibleConeSPN.absEnvelope G.value (channelSum (RouteBP5ConeIndex.chart c u))
      (RouteBP5ConeIndex.chart c u) = RouteBP5FeasibleConeSPN.quad (H c) u

/-- The generic SPN consumer needs these three fields. Symmetry may be
enforced by an exact exporter; the consumer's quadratic implication does not
need an extra symmetry premise. No decomposition is instantiated here. -/
structure SPNWitness (M : Mat) where
  S : Mat
  N : Mat
  decomposition : ∀ i j, M i j = S i j + N i j
  psd : RouteBP5FeasibleConeSPN.IsPSD S
  entrywise : ∀ i j, 0 ≤ N i j

/-- Uses the existing DATA-valued 36-to-18 consumer, preserving all labels. -/
def liftSPN {G : NonnegativeGain} {Q : Vec → ℝ} {mu : ℝ}
    (b : ConeGapBinding G Q mu)
    (cert : ∀ r : RouteBP5ConeIndex.Representative, SPNWitness (b.H (RouteBP5ConeIndex.representativeCone r))) :
    ∀ c : RouteBP5ConeIndex.ConeIndex, SPNWitness (b.H c) :=
  RouteBP5ConeIndex.liftFamily b.H SPNWitness b.flip_eq cert

theorem direct_envelope {G : NonnegativeGain} {Q : Vec → ℝ} {mu : ℝ}
    (b : ConeGapBinding G Q mu)
    (cert : ∀ r : RouteBP5ConeIndex.Representative, SPNWitness (b.H (RouteBP5ConeIndex.representativeCone r))) :
    ∀ z, RouteBP5FeasibleConeSPN.absEnvelope G.value (channelSum z) z ≤ mu * Q z := by
  let all := liftSPN b cert
  apply RouteBP5FeasibleConeSPN.global_abs_envelope_of_spn RouteBP5ConeIndex.chart channelSum G.value Q mu b.H
    (fun c => (all c).S) (fun c => (all c).N)
  · intro z
    obtain ⟨c, u, hu, hz⟩ := RouteBP5ConeIndex.cone_cover z
    exact ⟨c, u, hu, hz.symm⟩
  · exact b.exact_gap
  · exact fun c => (all c).decomposition
  · exact fun c => (all c).psd
  · exact fun c => (all c).entrywise

/-- The final conditional comparison: certify the UPPER gain G and bound
the actual centered residual by K <= G, on the SAME source witness/domain. -/
theorem componentwise_spn_power {X : Type*} {D : X → Prop}
    {z : X → Vec} {rc : X → Force} {K G : NonnegativeGain}
    {Q : Vec → ℝ} {mu : ℝ}
    (source : ComponentBinding D z rc K)
    (comparison : ComponentLE K.value G.value)
    (gap : ConeGapBinding G Q mu)
    (cert : ∀ r : RouteBP5ConeIndex.Representative, SPNWitness (gap.H (RouteBP5ConeIndex.representativeCone r)))
    (x : X) (hx : D x) :
    |RouteBP5FeasibleConeSPN.residualPower (channelSum (z x)) (rc x)| ≤ mu * Q (z x) := by
  exact (RouteBP5FeasibleConeSPN.component_residual_power_bound G.value (channelSum (z x)) (rc x)
    (z x) ((source.weaken comparison).bound x hx)).trans (direct_envelope gap cert (z x))

/-- Bias is an explicit power term; no homogeneous or trajectory claim. -/
theorem pointwise_ledger {X : Type*} {D : X → Prop}
    {z : X → Vec} {rc : X → Force} {K G : NonnegativeGain}
    {Q : Vec → ℝ} {mu : ℝ}
    (source : ComponentBinding D z rc K)
    (comparison : ComponentLE K.value G.value)
    (gap : ConeGapBinding G Q mu)
    (cert : ∀ r : RouteBP5ConeIndex.Representative, SPNWitness (gap.H (RouteBP5ConeIndex.representativeCone r)))
    (x : X) (hx : D x) (Vdot biasPower : ℝ)
    (hdot : Vdot ≤ -Q (z x) + RouteBP5FeasibleConeSPN.residualPower (channelSum (z x)) (rc x) + biasPower) :
    Vdot ≤ -(1 - mu) * Q (z x) + biasPower := by
  have hp := componentwise_spn_power source comparison gap cert x hx
  have ha := le_abs_self (RouteBP5FeasibleConeSPN.residualPower (channelSum (z x)) (rc x))
  nlinarith

/-- Comparison of gains induces the REVERSE order of gaps on the orthant.
This does not assert entrywise or Loewner order of the gap matrices. -/
theorem cone_gap_antitone {K G : NonnegativeGain} {Q : Vec → ℝ} {mu : ℝ}
    (h : ComponentLE K.value G.value)
    (bK : ConeGapBinding K Q mu) (bG : ConeGapBinding G Q mu)
    (c : RouteBP5ConeIndex.ConeIndex) (u : Vec) (hu : RouteBP5ConeIndex.Orthant u) :
    RouteBP5FeasibleConeSPN.quad (bG.H c) u ≤ RouteBP5FeasibleConeSPN.quad (bK.H c) u := by
  rw [← bG.exact_gap c u hu, ← bK.exact_gap c u hu]
  exact sub_le_sub_left (envelope_mono h (RouteBP5ConeIndex.chart c u)) _

end

#print axioms row_mono
#print axioms envelope_mono
#print axioms component_le_iff_rows
#print axioms ComponentBinding.zero_at_origin
#print axioms ComponentBinding.weaken
#print axioms transportedGain
#print axioms PathBinding.toComponentBinding
#print axioms liftSPN
#print axioms direct_envelope
#print axioms componentwise_spn_power
#print axioms pointwise_ledger
#print axioms cone_gap_antitone

end RouteBP5KPathInterface

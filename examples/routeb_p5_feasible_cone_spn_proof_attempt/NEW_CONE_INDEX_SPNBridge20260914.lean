import NEW_CONE_INDEX_OrbitFiber20260914
import examples.routeb_p5_feasible_cone_spn_lean.P5FeasibleConeSPN

/-!
Conditional typed bridge to the GENERIC P5 sidecar, not the different
P5FeasibleConeSPN.lean in this proof_attempt directory.
The direct SPN path uses a signed gap identity, not a membership count.
The optional weighted path explicitly consumes OrbitFiber's count correction.
No concrete gain, source envelope, or representative SPN data is supplied.
-/

set_option autoImplicit false

namespace RouteBP5ConeIndexSPNBridge

open RouteBP5ConeIndex RouteBP5ConeIndexInverseCover RouteBP5ConeIndexOrbitFiber
open RouteBP5FeasibleConeSPN
open scoped BigOperators

noncomputable section

local instance (p : Prop) : Decidable p := Classical.propDecidable p

abbrev Mat := Fin 4 → Fin 4 → ℝ

def p5Gap (L : Vec → Fin 2 → ℝ) (K : Fin 2 → Fin 4 → ℝ)
    (Q : Vec → ℝ) (mu : ℝ) (z : Vec) : ℝ :=
  mu * Q z - absEnvelope K (L z) z

/-- Even storage and an odd output map suffice for scalar gap invariance.
No invariance of the residual r, of membership, or of K's source is inferred. -/
theorem p5_gap_even
    (L : Vec → Fin 2 → ℝ) (K : Fin 2 → Fin 4 → ℝ) (Q : Vec → ℝ) (mu : ℝ)
    (hQ : ∀ z, Q (-z) = Q z) (hL : ∀ z, L (-z) = -L z) :
    ∀ z, p5Gap L K Q mu (-z) = p5Gap L K Q mu z := by
  intro z
  unfold p5Gap
  rw [hQ, hL]
  exact congrArg (fun t : ℝ => mu * Q z - t)
    (absEnvelope_global_sign_invariant K (L z) z)

/-- Keep the same nonnegative u in both directions. Evenness of the scalar
gap, NOT uniqueness of a covering orientation, justifies this reuse. -/
theorem signed_gap_of_even (G : Vec → ℝ) (H : Representative → Mat)
    (heven : ∀ z, G (-z) = G z)
    (hrep : ∀ r u, Orthant u → G (chart (representativeCone r) u) = quad (H r) u) :
    ∀ r b u, Orthant u → G (chart (expand (r, b)) u) = quad (H r) u := by
  intro r b u hu
  rw [chart_expand]
  cases b
  · exact hrep r u hu
  · simpa only [Bool.true_eq, ↓reduceIte, heven] using hrep r u hu

/-- Shortest typed consumer: 18 matrices, two oriented charts, one exact
identity per oriented chart. No extra count or z!=0 hypothesis is needed. -/
theorem eighteen_spn_envelope
    (L : Vec → Fin 2 → ℝ) (K : Fin 2 → Fin 4 → ℝ) (Q : Vec → ℝ) (mu : ℝ)
    (H S N : Representative → Mat)
    (hgap : ∀ r b u, Orthant u →
      p5Gap L K Q mu (chart (expand (r, b)) u) = quad (H r) u)
    (hdecomp : ∀ r i j, H r i j = S r i j + N r i j)
    (hPSD : ∀ r, IsPSD (S r))
    (hN : ∀ r i j, 0 ≤ N r i j) :
    ∀ z, absEnvelope K (L z) z ≤ mu * Q z := by
  apply global_abs_envelope_of_spn
    (fun p : Representative × Bool => chart (expand p)) L K Q mu
    (fun p => H p.1) (fun p => S p.1) (fun p => N p.1)
  · intro z
    obtain ⟨r, b, u, hu, hz⟩ := signed_representative_cover z
    exact ⟨(r, b), u, hu, hz.symm⟩
  · intro p u hu
    exact hgap p.1 p.2 u hu
  · intro p i j
    exact hdecomp p.1 i j
  · intro p
    exact hPSD p.1
  · intro p i j
    exact hN p.1 i j

/-- The generic gap contract already includes u=0. It is a real obligation,
not a consequence of merely having 18 orbit labels at the origin. -/
theorem signed_gap_origin (G : Vec → ℝ) (H : Representative → Mat)
    (hgap : ∀ r b u, Orthant u → G (chart (expand (r, b)) u) = quad (H r) u) :
    G 0 = 0 := by
  have h := hgap (0, Cone.pp) false 0 (fun _ => le_refl 0)
  simpa [chart_zero, quad] using h

/-- Count each covering label, including BOTH orientations at the origin.
This theorem applies to a SAME-STATE scalar weight G z, not arbitrary w(c,u). -/
theorem weighted_gap_factor (G : Vec → ℝ) (z : Vec) :
    (∑ c : ConeIndex, if Member c z then G z else 0) =
      ((if z = 0 then 2 * (coveringRepresentatives z).card
        else (coveringRepresentatives z).card : ℕ) : ℝ) * G z := by
  classical
  have hw : ∀ c : ConeIndex, (if Member c z then G z else 0) =
      (membershipWeight c z : ℝ) * G z := by
    intro c
    by_cases hc : Member c z <;> simp [membershipWeight, hc]
  simp_rw [hw]
  rw [← Finset.sum_mul]
  have hc : (∑ c : ConeIndex, (membershipWeight c z : ℝ)) =
      (RouteBP5ConeIndex.multiplicity z : ℝ) := by
    exact (Nat.cast_sum Finset.univ (fun c : ConeIndex => membershipWeight c z)).symm
  rw [hc, exact_multiplicity_formula]

/-- Optional weighted aggregation interface. Coverage makes the corrected
coefficient positive, so no division by a possibly zero count is performed. -/
theorem weighted_gap_nonneg_iff (G : Vec → ℝ) (z : Vec) :
    (0 ≤ ∑ c : ConeIndex, if Member c z then G z else 0) ↔ 0 ≤ G z := by
  classical
  have hpos : 0 < RouteBP5ConeIndex.multiplicity z := by
    rw [← coveringLabels_card]
    exact Finset.card_pos.mpr (coveringLabels_nonempty z)
  have hreal : (0 : ℝ) < (RouteBP5ConeIndex.multiplicity z : ℝ) := by exact_mod_cast hpos
  rw [weighted_gap_factor, ← exact_multiplicity_formula]
  constructor
  · intro h
    exact nonneg_of_mul_nonneg_right h hreal
  · intro h
    exact mul_nonneg (le_of_lt hreal) h

/-- Actual P5-typed attachment of OrbitFiber to an optional weighted DAG lane.
The premise is still the sign of the sum; counts alone prove no positivity. -/
theorem envelope_iff_weighted_nonneg
    (L : Vec → Fin 2 → ℝ) (K : Fin 2 → Fin 4 → ℝ) (Q : Vec → ℝ) (mu : ℝ) :
    (∀ z, absEnvelope K (L z) z ≤ mu * Q z) ↔
      ∀ z, 0 ≤ ∑ c : ConeIndex, if Member c z then p5Gap L K Q mu z else 0 := by
  classical
  constructor
  · intro h z
    apply (weighted_gap_nonneg_iff (p5Gap L K Q mu) z).mpr
    exact sub_nonneg.mpr (h z)
  · intro h z
    exact sub_nonneg.mp ((weighted_gap_nonneg_iff (p5Gap L K Q mu) z).mp (h z))

/-- The residual envelope remains an explicit source-side premise. -/
theorem residual_power_of_envelope
    (L : Vec → Fin 2 → ℝ) (K : Fin 2 → Fin 4 → ℝ) (Q : Vec → ℝ) (mu : ℝ)
    (henvelope : ∀ z, absEnvelope K (L z) z ≤ mu * Q z)
    (z : Vec) (r : Fin 2 → ℝ)
    (hcomp : ∀ a, |r a| ≤ rowEnvelope K z a) :
    |residualPower (L z) r| ≤ mu * Q z :=
  (component_residual_power_bound K (L z) r z hcomp).trans (henvelope z)

end

#print axioms p5_gap_even
#print axioms signed_gap_of_even
#print axioms eighteen_spn_envelope
#print axioms signed_gap_origin
#print axioms weighted_gap_factor
#print axioms weighted_gap_nonneg_iff
#print axioms envelope_iff_weighted_nonneg
#print axioms residual_power_of_envelope

end RouteBP5ConeIndexSPNBridge

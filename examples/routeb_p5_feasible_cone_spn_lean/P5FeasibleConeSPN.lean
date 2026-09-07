import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# Route-B P5 feasible-cone SPN small-gain sidecar

This file formalizes the source-independent theorem decomposition from
`review-T-P5-026-guyuefangyuan-20260907T1031.md`.

The mathematical review improves the direct component-matrix `K_path` route in
two ways: it covers each physical `(x,y,x+y)` sign geometry by six feasible
cones, and it replaces global PSD on every sign matrix by nonnegativity only on
the nonnegative cone.  A checker-friendly sufficient representation is
`H = S + N`, where `S` has a globally nonnegative quadratic form and `N` is
entrywise nonnegative.

This sidecar proves the six-cone cover, a two-channel product cover, generic
finite-dimensional SPN nonnegativity, an exact cover-reduction theorem, the
component residual power triangle bound, and a generic feasible-cone SPN
small-gain consumer.  It intentionally does not bind a concrete `K_path`, Julia
or Float64 semantics, P8 coverage, ODE continuation, or registry admission.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP5FeasibleConeSPN

noncomputable section

/-- The six explicit closed cones for one physical channel.  The witness
parameters `a,b` are required separately to be nonnegative. -/
def ChannelConeForm (x y a b : ℝ) : Prop :=
  (x = a ∧ y = b) ∨
  (x = -a ∧ y = -b) ∨
  (x = a + b ∧ y = -a) ∨
  (x = a ∧ y = -a - b) ∨
  (x = -a ∧ y = a + b) ∨
  (x = -a - b ∧ y = a)

/-- Every pair `(x,y)` belongs to one of the six feasible cones determined by
`sign x`, `sign y`, and the necessarily compatible sign of `x+y`. -/
theorem channel_cone_cover (x y : ℝ) :
    ∃ a b : ℝ, 0 ≤ a ∧ 0 ≤ b ∧ ChannelConeForm x y a b := by
  by_cases hx : 0 ≤ x
  · by_cases hy : 0 ≤ y
    · exact ⟨x, y, hx, hy, Or.inl ⟨rfl, rfl⟩⟩
    · have hylt : y < 0 := lt_of_not_ge hy
      by_cases hs : 0 ≤ x + y
      · refine ⟨-y, x + y, ?_, hs, ?_⟩
        · linarith
        · exact Or.inr (Or.inr (Or.inl ⟨by ring, by ring⟩))
      · have hslt : x + y < 0 := lt_of_not_ge hs
        refine ⟨x, -(x + y), hx, ?_, ?_⟩
        · linarith
        · exact Or.inr (Or.inr (Or.inr (Or.inl ⟨by ring, by ring⟩)))
  · have hxlt : x < 0 := lt_of_not_ge hx
    by_cases hy : 0 ≤ y
    · by_cases hs : 0 ≤ x + y
      · refine ⟨-x, x + y, ?_, hs, ?_⟩
        · linarith
        · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl ⟨by ring, by ring⟩))))
      · have hslt : x + y < 0 := lt_of_not_ge hs
        refine ⟨y, -(x + y), hy, ?_, ?_⟩
        · linarith
        · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr ⟨by ring, by ring⟩))))
    · have hylt : y < 0 := lt_of_not_ge hy
      refine ⟨-x, -y, ?_, ?_, ?_⟩
      · linarith
      · linarith
      · exact Or.inr (Or.inl ⟨by ring, by ring⟩)

/-- Applying the one-channel cover independently to block channels 4 and 5
produces the exact 36-cone product cover before global-sign pairing. -/
theorem two_channel_cone_cover (x4 x5 y4 y5 : ℝ) :
    ∃ a4 b4 a5 b5 : ℝ,
      0 ≤ a4 ∧ 0 ≤ b4 ∧ 0 ≤ a5 ∧ 0 ≤ b5 ∧
      ChannelConeForm x4 y4 a4 b4 ∧
      ChannelConeForm x5 y5 a5 b5 := by
  rcases channel_cone_cover x4 y4 with ⟨a4, b4, ha4, hb4, hc4⟩
  rcases channel_cone_cover x5 y5 with ⟨a5, b5, ha5, hb5, hc5⟩
  exact ⟨a4, b4, a5, b5, ha4, hb4, ha5, hb5, hc4, hc5⟩

/-- Componentwise nonnegativity for a finite vector. -/
def NonnegVec {n : ℕ} (u : Fin n → ℝ) : Prop :=
  ∀ i, 0 ≤ u i

/-- Quadratic evaluation using explicit finite sums.  The checker may provide
`symmetric` matrices, but the nonnegativity lemmas below do not need symmetry as
an additional logical premise. -/
def quad {n : ℕ} (M : Fin n → Fin n → ℝ) (u : Fin n → ℝ) : ℝ :=
  ∑ i, ∑ j, u i * M i j * u j

/-- A minimal PSD-facing interface: global nonnegativity of the quadratic
form.  Exact rational LDL witnesses can discharge this premise upstream. -/
def IsPSD {n : ℕ} (M : Fin n → Fin n → ℝ) : Prop :=
  ∀ u, 0 ≤ quad M u

/-- Quadratic evaluation is additive in the matrix argument. -/
theorem quad_add {n : ℕ}
    (S N : Fin n → Fin n → ℝ) (u : Fin n → ℝ) :
    quad (fun i j => S i j + N i j) u = quad S u + quad N u := by
  unfold quad
  calc
    (∑ i, ∑ j, u i * (S i j + N i j) * u j) =
        ∑ i, ∑ j, (u i * S i j * u j + u i * N i j * u j) := by
          apply Finset.sum_congr rfl
          intro i hi
          apply Finset.sum_congr rfl
          intro j hj
          ring
    _ = ∑ i, ((∑ j, u i * S i j * u j) + (∑ j, u i * N i j * u j)) := by
          apply Finset.sum_congr rfl
          intro i hi
          exact Finset.sum_add_distrib
    _ = (∑ i, ∑ j, u i * S i j * u j) +
        (∑ i, ∑ j, u i * N i j * u j) := by
          exact Finset.sum_add_distrib

/-- An entrywise nonnegative matrix has a nonnegative quadratic form on the
nonnegative orthant. -/
theorem entrywise_nonnegative_quadratic_nonnegative {n : ℕ}
    (N : Fin n → Fin n → ℝ) (u : Fin n → ℝ)
    (hN : ∀ i j, 0 ≤ N i j)
    (hu : NonnegVec u) :
    0 ≤ quad N u := by
  unfold quad
  apply Finset.sum_nonneg
  intro i hi
  apply Finset.sum_nonneg
  intro j hj
  exact mul_nonneg (mul_nonneg (hu i) (hN i j)) (hu j)

/-- The checker-facing SPN consumer: if `H=S+N`, the `S` piece is globally PSD,
and the `N` piece is entrywise nonnegative, then `H` is nonnegative on every
nonnegative vector. -/
theorem spn_quadratic_nonnegative_on_orthant {n : ℕ}
    (H S N : Fin n → Fin n → ℝ)
    (hdecomp : ∀ i j, H i j = S i j + N i j)
    (hS : IsPSD S)
    (hN : ∀ i j, 0 ≤ N i j)
    (u : Fin n → ℝ)
    (hu : NonnegVec u) :
    0 ≤ quad H u := by
  have hmat : H = fun i j => S i j + N i j := by
    funext i j
    exact hdecomp i j
  calc
    0 ≤ quad S u + quad N u :=
      add_nonneg (hS u) (entrywise_nonnegative_quadratic_nonnegative N u hN hu)
    _ = quad (fun i j => S i j + N i j) u := (quad_add S N u).symm
    _ = quad H u := by rw [hmat]

/-- Global sign reversal does not change a quadratic form.  This is the basic
algebra behind pairing feasible cones related by simultaneous sign reversal. -/
theorem quad_global_sign_invariant {n : ℕ}
    (M : Fin n → Fin n → ℝ) (u : Fin n → ℝ) :
    quad M (fun i => -u i) = quad M u := by
  unfold quad
  apply Finset.sum_congr rfl
  intro i hi
  apply Finset.sum_congr rfl
  intro j hj
  ring

/-- One row of the component residual envelope. -/
def rowEnvelope {p k : ℕ}
    (K : Fin p → Fin k → ℝ) (z : Fin k → ℝ) (a : Fin p) : ℝ :=
  ∑ j, K a j * |z j|

/-- The direct absolute power majorant `|Lz|^T K |z|`. -/
def absEnvelope {p k : ℕ}
    (K : Fin p → Fin k → ℝ) (Lz : Fin p → ℝ) (z : Fin k → ℝ) : ℝ :=
  ∑ a, |Lz a| * rowEnvelope K z a

/-- Residual power `(Lz)^T r`. -/
def residualPower {p : ℕ} (Lz r : Fin p → ℝ) : ℝ :=
  ∑ a, Lz a * r a

/-- The direct absolute envelope is unchanged when both the state coordinates
and the corresponding `Lz` coordinates are globally sign-reversed. -/
theorem absEnvelope_global_sign_invariant {p k : ℕ}
    (K : Fin p → Fin k → ℝ) (Lz : Fin p → ℝ) (z : Fin k → ℝ) :
    absEnvelope K (fun a => -Lz a) (fun j => -z j) = absEnvelope K Lz z := by
  simp [absEnvelope, rowEnvelope]

/-- Component residual bounds imply the triangle majorant used by the direct
`K_path` route. -/
theorem component_residual_power_bound {p k : ℕ}
    (K : Fin p → Fin k → ℝ)
    (Lz r : Fin p → ℝ)
    (z : Fin k → ℝ)
    (hcomp : ∀ a, |r a| ≤ rowEnvelope K z a) :
    |residualPower Lz r| ≤ absEnvelope K Lz z := by
  have htri :=
    Finset.abs_sum_le_sum_abs (fun a : Fin p => Lz a * r a) Finset.univ
  calc
    |residualPower Lz r| ≤ ∑ a, |Lz a * r a| := by
      simpa [residualPower] using htri
    _ = ∑ a, |Lz a| * |r a| := by
      simp only [abs_mul]
    _ ≤ absEnvelope K Lz z := by
      unfold absEnvelope
      apply Finset.sum_le_sum
      intro a ha
      exact mul_le_mul_of_nonneg_left (hcomp a) (abs_nonneg (Lz a))

/-- Exact reduction from a global inequality to inequalities on a covering
family of nonnegative-coordinate cones.  `gap` may be a quadratic form, but the
equivalence itself only needs the cover and the exact per-cone identity. -/
theorem exact_feasible_cone_reduction {ι : Type} {m n : ℕ}
    (T : ι → (Fin n → ℝ) → (Fin m → ℝ))
    (lhs rhs : (Fin m → ℝ) → ℝ)
    (gap : ι → (Fin n → ℝ) → ℝ)
    (hcover : ∀ z, ∃ c u, NonnegVec u ∧ z = T c u)
    (hexact : ∀ c u, NonnegVec u →
      rhs (T c u) - lhs (T c u) = gap c u) :
    (∀ z, lhs z ≤ rhs z) ↔
      ∀ c u, NonnegVec u → 0 ≤ gap c u := by
  constructor
  · intro hglobal c u hu
    calc
      0 ≤ rhs (T c u) - lhs (T c u) := sub_nonneg.mpr (hglobal (T c u))
      _ = gap c u := hexact c u hu
  · intro hcones z
    rcases hcover z with ⟨c, u, hu, hz⟩
    have hgap : 0 ≤ gap c u := hcones c u hu
    have hdiff : 0 ≤ rhs (T c u) - lhs (T c u) := by
      rw [hexact c u hu]
      exact hgap
    rw [hz]
    exact sub_nonneg.mp hdiff

/-- SPN certificates on every member of a nonnegative-coordinate cone cover
imply the global direct absolute envelope.  This is the generic formal core of
the proposed 18-cone checker; the concrete finite cone enumeration and
`K_path` remain source/checker data. -/
theorem global_abs_envelope_of_spn {ι : Type} {p k n : ℕ}
    (T : ι → (Fin n → ℝ) → (Fin k → ℝ))
    (L : (Fin k → ℝ) → (Fin p → ℝ))
    (K : Fin p → Fin k → ℝ)
    (Q : (Fin k → ℝ) → ℝ)
    (mu : ℝ)
    (H S N : ι → Fin n → Fin n → ℝ)
    (hcover : ∀ z, ∃ c u, NonnegVec u ∧ z = T c u)
    (hexact : ∀ c u, NonnegVec u →
      mu * Q (T c u) - absEnvelope K (L (T c u)) (T c u) = quad (H c) u)
    (hdecomp : ∀ c i j, H c i j = S c i j + N c i j)
    (hPSD : ∀ c, IsPSD (S c))
    (hN : ∀ c i j, 0 ≤ N c i j) :
    ∀ z, absEnvelope K (L z) z ≤ mu * Q z := by
  intro z
  rcases hcover z with ⟨c, u, hu, hz⟩
  have hquad : 0 ≤ quad (H c) u :=
    spn_quadratic_nonnegative_on_orthant
      (H c) (S c) (N c) (hdecomp c) (hPSD c) (hN c) u hu
  have hdiff :
      0 ≤ mu * Q (T c u) - absEnvelope K (L (T c u)) (T c u) := by
    rw [hexact c u hu]
    exact hquad
  rw [hz]
  exact sub_nonneg.mp hdiff

/-- Final source-independent small-gain consumer.  A component residual envelope
plus SPN certificates for a feasible cone cover gives
`|(Lz)^T r| <= mu Q(z)`. -/
theorem spn_feasible_cone_small_gain {ι : Type} {p k n : ℕ}
    (T : ι → (Fin n → ℝ) → (Fin k → ℝ))
    (L : (Fin k → ℝ) → (Fin p → ℝ))
    (K : Fin p → Fin k → ℝ)
    (Q : (Fin k → ℝ) → ℝ)
    (mu : ℝ)
    (H S N : ι → Fin n → Fin n → ℝ)
    (hcover : ∀ z, ∃ c u, NonnegVec u ∧ z = T c u)
    (hexact : ∀ c u, NonnegVec u →
      mu * Q (T c u) - absEnvelope K (L (T c u)) (T c u) = quad (H c) u)
    (hdecomp : ∀ c i j, H c i j = S c i j + N c i j)
    (hPSD : ∀ c, IsPSD (S c))
    (hN : ∀ c i j, 0 ≤ N c i j)
    (z : Fin k → ℝ)
    (r : Fin p → ℝ)
    (hcomp : ∀ a, |r a| ≤ rowEnvelope K z a) :
    |residualPower (L z) r| ≤ mu * Q z := by
  exact (component_residual_power_bound K (L z) r z hcomp).trans
    (global_abs_envelope_of_spn T L K Q mu H S N
      hcover hexact hdecomp hPSD hN z)

#print axioms channel_cone_cover
#print axioms two_channel_cone_cover
#print axioms quad_add
#print axioms entrywise_nonnegative_quadratic_nonnegative
#print axioms spn_quadratic_nonnegative_on_orthant
#print axioms quad_global_sign_invariant
#print axioms absEnvelope_global_sign_invariant
#print axioms component_residual_power_bound
#print axioms exact_feasible_cone_reduction
#print axioms global_abs_envelope_of_spn
#print axioms spn_feasible_cone_small_gain

end

end RouteBP5FeasibleConeSPN

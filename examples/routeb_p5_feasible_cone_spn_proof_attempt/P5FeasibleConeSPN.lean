import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# T-P5-026: source-independent exact feasible cones and SPN

PROOF ATTEMPT ONLY. This source has not been run through Lean or Lake.
No elaboration, kernel, compilation, source binding, or admission receipt exists
for this target. The independent rational checker is not a Lean verifier.

State order: (x4,x5,y4,y5). Orthant order: (a4,a5,b4,b5).
The frozen P is copied explicitly from the T-P5-026 review. K is universally
quantified; there is deliberately no concrete K_path definition or instance.
-/

set_option autoImplicit false

namespace RouteBP5FeasibleConeSPN

noncomputable section

open scoped BigOperators

inductive Cone where
  | pp | nn | pnPos | pnNeg | npPos | npNeg
  deriving DecidableEq, Fintype

def cx : Cone → ℝ → ℝ → ℝ
  | .pp, a, _ => a
  | .nn, a, _ => -a
  | .pnPos, a, b => a + b
  | .pnNeg, a, _ => a
  | .npPos, a, _ => -a
  | .npNeg, a, b => -a - b

def cy : Cone → ℝ → ℝ → ℝ
  | .pp, _, b => b
  | .nn, _, b => -b
  | .pnPos, a, _ => -a
  | .pnNeg, a, b => -a - b
  | .npPos, a, b => a + b
  | .npNeg, a, _ => a

def sx : Cone → ℝ
  | .pp | .pnPos | .pnNeg => 1
  | .nn | .npPos | .npNeg => -1

def sy : Cone → ℝ
  | .pp | .npPos | .npNeg => 1
  | .nn | .pnPos | .pnNeg => -1

def ss : Cone → ℝ
  | .pp | .pnPos | .npPos => 1
  | .nn | .pnNeg | .npNeg => -1

def reverse : Cone → Cone
  | .pp => .nn
  | .nn => .pp
  | .pnPos => .npNeg
  | .pnNeg => .npPos
  | .npPos => .pnNeg
  | .npNeg => .pnPos

theorem channel_cone_cover (x y : ℝ) :
    ∃ c : Cone, ∃ a b : ℝ,
      0 ≤ a ∧ 0 ≤ b ∧ x = cx c a b ∧ y = cy c a b := by
  by_cases hx : 0 ≤ x
  · by_cases hy : 0 ≤ y
    · exact ⟨.pp, x, y, hx, hy, rfl, rfl⟩
    · by_cases hs : 0 ≤ x + y
      · refine ⟨.pnPos, -y, x + y, ?_, hs, ?_, ?_⟩ <;>
          dsimp [cx, cy] <;> linarith
      · refine ⟨.pnNeg, x, -(x + y), hx, ?_, rfl, ?_⟩ <;>
          dsimp [cy] <;> linarith
  · by_cases hy : 0 ≤ y
    · by_cases hs : 0 ≤ x + y
      · refine ⟨.npPos, -x, x + y, ?_, hs, ?_, ?_⟩ <;>
          dsimp [cx, cy] <;> linarith
      · refine ⟨.npNeg, y, -(x + y), hy, ?_, ?_, rfl⟩ <;>
          dsimp [cx] <;> linarith
    · refine ⟨.nn, -x, -y, ?_, ?_, ?_, ?_⟩ <;>
        dsimp [cx, cy] <;> linarith

/-- Weak signs include x=0, y=0, and x+y=0; no disjointness is asserted. -/
theorem channel_sign_identities (c : Cone) (a b : ℝ)
    (ha : 0 ≤ a) (hb : 0 ≤ b) :
    |cx c a b| = sx c * cx c a b ∧
    |cy c a b| = sy c * cy c a b ∧
    |cx c a b + cy c a b| = ss c * (cx c a b + cy c a b) := by
  cases c <;> dsimp [cx, cy, sx, sy, ss] <;>
    simp only [one_mul, neg_one_mul] <;>
    constructor
  all_goals
    first
    | (rw [abs_of_nonneg (by linarith)])
    | (rw [abs_of_nonpos (by linarith)])
    | (constructor <;>
        first
        | (rw [abs_of_nonneg (by linarith)])
        | (rw [abs_of_nonpos (by linarith)]))

theorem channel_x_linear (c : Cone) (a b : ℝ) :
    cx c a b = cx c 1 0 * a + cx c 0 1 * b := by
  cases c <;> simp [cx] <;> ring

theorem channel_y_linear (c : Cone) (a b : ℝ) :
    cy c a b = cy c 1 0 * a + cy c 0 1 * b := by
  cases c <;> simp [cy] <;> ring

@[simp] theorem reverse_reverse (c : Cone) : reverse (reverse c) = c := by
  cases c <;> rfl

@[simp] theorem cx_reverse (c : Cone) (a b : ℝ) :
    cx (reverse c) a b = -cx c a b := by
  cases c <;> simp [reverse, cx] <;> ring

@[simp] theorem cy_reverse (c : Cone) (a b : ℝ) :
    cy (reverse c) a b = -cy c a b := by
  cases c <;> simp [reverse, cy] <;> ring

@[simp] theorem sx_reverse (c : Cone) : sx (reverse c) = -sx c := by
  cases c <;> norm_num [reverse, sx]

@[simp] theorem sy_reverse (c : Cone) : sy (reverse c) = -sy c := by
  cases c <;> norm_num [reverse, sy]

@[simp] theorem ss_reverse (c : Cone) : ss (reverse c) = -ss c := by
  cases c <;> norm_num [reverse, ss]

theorem channel_unimodular (c : Cone) :
    (cx c 1 0 * cy c 0 1 - cx c 0 1 * cy c 1 0)^2 = 1 := by
  cases c <;> norm_num [cx, cy]

abbrev Vec := Fin 4 → ℝ
abbrev Mat := Fin 4 → Fin 4 → ℝ
abbrev Gain := Fin 2 → Fin 4 → ℝ
abbrev ProductCone := Cone × Cone
abbrev Representative := Fin 3 × Cone

def Orthant (u : Vec) : Prop := ∀ i, 0 ≤ u i

def interleave (c : ProductCone) (u : Vec) : Vec :=
  ![cx c.1 (u 0) (u 2), cx c.2 (u 1) (u 3),
    cy c.1 (u 0) (u 2), cy c.2 (u 1) (u 3)]

def T (c : ProductCone) : Mat :=
  ![![cx c.1 1 0, 0, cx c.1 0 1, 0],
    ![0, cx c.2 1 0, 0, cx c.2 0 1],
    ![cy c.1 1 0, 0, cy c.1 0 1, 0],
    ![0, cy c.2 1 0, 0, cy c.2 0 1]]

def sigma (c : ProductCone) : Vec := ![sx c.1, sx c.2, sy c.1, sy c.2]
def tau (c : ProductCone) : Fin 2 → ℝ := ![ss c.1, ss c.2]
def flip (c : ProductCone) : ProductCone := (reverse c.1, reverse c.2)

def representativeFirst (i : Fin 3) : Cone := ![.pp, .pnPos, .pnNeg] i
def representativeCone (r : Representative) : ProductCone :=
  (representativeFirst r.1, r.2)

theorem cone_counts : Fintype.card ProductCone = 36 ∧
    Fintype.card Representative = 18 := by decide

theorem representative_or_flip (c : ProductCone) :
    (∃ r : Representative, c = representativeCone r) ∨
    (∃ r : Representative, flip c = representativeCone r) := by
  rcases c with ⟨c4, c5⟩
  cases c4
  · exact Or.inl ⟨(0, c5), rfl⟩
  · exact Or.inr ⟨(0, reverse c5), rfl⟩
  · exact Or.inl ⟨(1, c5), rfl⟩
  · exact Or.inl ⟨(2, c5), rfl⟩
  · exact Or.inr ⟨(2, reverse c5), rfl⟩
  · exact Or.inr ⟨(1, reverse c5), rfl⟩

theorem two_channel_cone_cover (z : Vec) :
    ∃ c : ProductCone, ∃ u : Vec, Orthant u ∧ z = interleave c u := by
  obtain ⟨c4, a4, b4, ha4, hb4, hx4, hy4⟩ := channel_cone_cover (z 0) (z 2)
  obtain ⟨c5, a5, b5, ha5, hb5, hx5, hy5⟩ := channel_cone_cover (z 1) (z 3)
  refine ⟨(c4, c5), ![a4, a5, b4, b5], ?_, ?_⟩
  · intro i
    fin_cases i
    · simpa using ha4
    · simpa using ha5
    · simpa using hb4
    · simpa using hb5
  · funext i
    fin_cases i
    · simpa [interleave] using hx4
    · simpa [interleave] using hx5
    · simpa [interleave] using hy4
    · simpa [interleave] using hy5

def mapVec (M : Mat) (u : Vec) : Vec := fun i => ∑ j, M i j * u j
def quad {ι : Type*} [Fintype ι] (M : ι → ι → ℝ) (u : ι → ℝ) : ℝ :=
  ∑ i, ∑ j, u i * M i j * u j

def congruence (M U : Mat) : Mat :=
  fun p q => ∑ i, ∑ j, U i p * M i j * U j q

theorem interleave_eq_mapVec (c : ProductCone) (u : Vec) :
    interleave c u = mapVec (T c) u := by
  funext i
  fin_cases i
  · simpa [interleave, mapVec, T, Fin.sum_univ_succ] using
      channel_x_linear c.1 (u 0) (u 2)
  · simpa [interleave, mapVec, T, Fin.sum_univ_succ] using
      channel_x_linear c.2 (u 1) (u 3)
  · simpa [interleave, mapVec, T, Fin.sum_univ_succ] using
      channel_y_linear c.1 (u 0) (u 2)
  · simpa [interleave, mapVec, T, Fin.sum_univ_succ] using
      channel_y_linear c.2 (u 1) (u 3)

/-- Reorder four finite sums without a spectral or matrix positivity API. -/
theorem sum_pair_exchange (f : Fin 4 → Fin 4 → Fin 4 → Fin 4 → ℝ) :
    (∑ p, ∑ q, ∑ i, ∑ j, f p q i j) =
      ∑ i, ∑ j, ∑ p, ∑ q, f p q i j := by
  calc
    _ = ∑ p, ∑ i, ∑ q, ∑ j, f p q i j := by
      apply Finset.sum_congr rfl
      intro p hp
      exact Finset.sum_comm
    _ = ∑ i, ∑ p, ∑ q, ∑ j, f p q i j := Finset.sum_comm
    _ = ∑ i, ∑ p, ∑ j, ∑ q, f p q i j := by
      apply Finset.sum_congr rfl
      intro i hi
      apply Finset.sum_congr rfl
      intro p hp
      exact Finset.sum_comm
    _ = _ := by
      apply Finset.sum_congr rfl
      intro i hi
      exact Finset.sum_comm

theorem quad_congruence (M U : Mat) (u : Vec) :
    quad (congruence M U) u = quad M (mapVec U u) := by
  simp only [quad, congruence, mapVec]
  simp only [Finset.sum_mul]
  simp only [Finset.mul_sum]
  simp only [Finset.sum_mul]
  rw [sum_pair_exchange]
  apply Finset.sum_congr rfl
  intro i hi
  apply Finset.sum_congr rfl
  intro j hj
  apply Finset.sum_congr rfl
  intro p hp
  apply Finset.sum_congr rfl
  intro q hq
  ring

def L : Fin 2 → Fin 4 → ℝ := ![![1, 0, 1, 0], ![0, 1, 0, 1]]
def channelSum (z : Vec) : Fin 2 → ℝ := ![z 0 + z 2, z 1 + z 3]

def P : Mat :=
  ![![(3/4 : ℝ), -3/400, 0, 1/800],
    ![-3/400, 29/50, -1/800, 0],
    ![0, -1/800, 2049997/3000000, 0],
    ![1/800, 0, 0, 2399261/4000000]]

def Q (z : Vec) : ℝ := quad P z

theorem frozen_dissipation (z : Vec) :
    Q z = (3/4 : ℝ)*(z 0)^2 + (29/50 : ℝ)*(z 1)^2 -
      (3/200 : ℝ)*z 0*z 1 + (2049997/3000000 : ℝ)*(z 2)^2 +
      (2399261/4000000 : ℝ)*(z 3)^2 +
      (1/400 : ℝ)*z 0*z 3 - (1/400 : ℝ)*z 1*z 2 := by
  simp [Q, quad, P, Fin.sum_univ_succ]
  <;> ring

def absEnvelope (K : Gain) (z : Vec) : ℝ :=
  ∑ a, |channelSum z a| * (∑ j, K a j * |z j|)

def signedA (K : Gain) (c : ProductCone) : Mat :=
  fun i j => ∑ a, L a i * tau c a * K a j * sigma c j

def signedB (K : Gain) (c : ProductCone) : Mat :=
  fun i j => (signedA K c i j + signedA K c j i) / 2

def H (K : Gain) (mu : ℝ) (c : ProductCone) : Mat :=
  congruence (fun i j => mu * P i j - signedB K c i j) (T c)

theorem interleave_sign_identities (c : ProductCone) (u : Vec)
    (hu : Orthant u) :
    (∀ i, |interleave c u i| = sigma c i * interleave c u i) ∧
    (∀ a, |channelSum (interleave c u) a| =
      tau c a * channelSum (interleave c u) a) := by
  have h4 := channel_sign_identities c.1 (u 0) (u 2) (hu 0) (hu 2)
  have h5 := channel_sign_identities c.2 (u 1) (u 3) (hu 1) (hu 3)
  constructor
  · intro i
    fin_cases i
    · simpa [interleave, sigma] using h4.1
    · simpa [interleave, sigma] using h5.1
    · simpa [interleave, sigma] using h4.2.1
    · simpa [interleave, sigma] using h5.2.1
  · intro a
    fin_cases a
    · simpa [interleave, tau, channelSum] using h4.2.2
    · simpa [interleave, tau, channelSum] using h5.2.2

theorem signed_power_identity (K : Gain) (c : ProductCone) (z : Vec)
    (hz : ∀ i, |z i| = sigma c i * z i)
    (hs : ∀ a, |channelSum z a| = tau c a * channelSum z a) :
    absEnvelope K z = quad (signedB K c) z := by
  unfold absEnvelope
  simp_rw [hz, hs]
  simp [quad, signedB, signedA, channelSum, L, Fin.sum_univ_succ]
  <;> ring

theorem sign_fixed_power_identity (K : Gain) (c : ProductCone) (u : Vec)
    (hu : Orthant u) :
    absEnvelope K (interleave c u) =
      quad (congruence (signedB K c) (T c)) u := by
  obtain ⟨hz, hs⟩ := interleave_sign_identities c u hu
  rw [quad_congruence, ← interleave_eq_mapVec]
  exact signed_power_identity K c (interleave c u) hz hs

theorem cone_gap_identity (K : Gain) (mu : ℝ) (c : ProductCone)
    (u : Vec) (hu : Orthant u) :
    quad (H K mu c) u = mu * Q (interleave c u) - absEnvelope K (interleave c u) := by
  obtain ⟨hz, hs⟩ := interleave_sign_identities c u hu
  rw [signed_power_identity K c (interleave c u) hz hs]
  rw [H, quad_congruence, ← interleave_eq_mapVec]
  simp [Q, quad, Fin.sum_univ_succ]
  <;> ring

theorem T_flip (c : ProductCone) (i j : Fin 4) :
    T (flip c) i j = -T c i j := by
  fin_cases i <;> fin_cases j <;> simp [T, flip]

theorem sigma_flip (c : ProductCone) (i : Fin 4) :
    sigma (flip c) i = -sigma c i := by
  fin_cases i <;> simp [sigma, flip]

theorem tau_flip (c : ProductCone) (a : Fin 2) :
    tau (flip c) a = -tau c a := by
  fin_cases a <;> simp [tau, flip]

theorem signedB_flip (K : Gain) (c : ProductCone) :
    signedB K (flip c) = signedB K c := by
  funext i j
  simp [signedB, signedA, sigma_flip, tau_flip]

theorem H_flip (K : Gain) (mu : ℝ) (c : ProductCone) :
    H K mu (flip c) = H K mu c := by
  funext p q
  simp [H, congruence, T_flip, signedB_flip]

def Copositive (M : Mat) : Prop := ∀ u, Orthant u → 0 ≤ quad M u
def DirectEnvelope (K : Gain) (mu : ℝ) : Prop :=
  ∀ z, absEnvelope K z ≤ mu * Q z

/-- Exact domain reduction. Algebraically no sign assumption on K is needed. -/
theorem exact_feasible_cone_reduction (K : Gain) (mu : ℝ) :
    DirectEnvelope K mu ↔ ∀ c, Copositive (H K mu c) := by
  constructor
  · intro h c u hu
    rw [cone_gap_identity K mu c u hu]
    exact sub_nonneg.mpr (h (interleave c u))
  · intro h z
    obtain ⟨c, u, hu, hz⟩ := two_channel_cone_cover z
    have hgap := h c u hu
    rw [cone_gap_identity K mu c u hu, ← hz] at hgap
    exact sub_nonneg.mp hgap

/-- Exactly 18 indexed representatives suffice, even when matrices coincide
for special values of K. This does not assert 18 pairwise distinct matrices. -/
theorem exact_eighteen_cone_reduction (K : Gain) (mu : ℝ) :
    DirectEnvelope K mu ↔
      ∀ r : Representative, Copositive (H K mu (representativeCone r)) := by
  rw [exact_feasible_cone_reduction]
  constructor
  · intro h r
    exact h (representativeCone r)
  · intro h c
    rcases representative_or_flip c with ⟨r, hr⟩ | ⟨r, hr⟩
    · rw [hr]
      exact h r
    · have hc : H K mu c = H K mu (representativeCone r) := by
        rw [← hr, H_flip]
      rw [hc]
      exact h r

theorem entrywise_nonnegative_quadratic_nonnegative
    {ι : Type*} [Fintype ι] (N : ι → ι → ℝ) (u : ι → ℝ)
    (hN : ∀ i j, 0 ≤ N i j) (hu : ∀ i, 0 ≤ u i) :
    0 ≤ quad N u := by
  apply Finset.sum_nonneg
  intro i hi
  apply Finset.sum_nonneg
  intro j hj
  exact mul_nonneg (mul_nonneg (hu i) (hN i j)) (hu j)

/-- Analytic PSD interface: nonnegative quadratic on every real vector.
Symmetry is a separate field of the certificate. -/
def QuadraticPSD (S : Mat) : Prop := ∀ v, 0 ≤ quad S v
def Symmetric (M : Mat) : Prop := ∀ i j, M i j = M j i

structure SPNCertificate (M : Mat) where
  S : Mat
  N : Mat
  s_symmetric : Symmetric S
  n_symmetric : Symmetric N
  decomposition : ∀ i j, M i j = S i j + N i j
  psd : QuadraticPSD S
  entrywise : ∀ i j, 0 ≤ N i j

theorem quad_add (S N : Mat) (u : Vec) :
    quad (fun i j => S i j + N i j) u = quad S u + quad N u := by
  simp [quad, mul_add, add_mul, Finset.sum_add_distrib]

theorem spn_quadratic_nonnegative_on_orthant (M : Mat)
    (cert : SPNCertificate M) : Copositive M := by
  intro u hu
  have heq : M = fun i j => cert.S i j + cert.N i j := by
    funext i j
    exact cert.decomposition i j
  rw [heq, quad_add]
  exact add_nonneg (cert.psd u)
    (entrywise_nonnegative_quadratic_nonnegative cert.N u cert.entrywise hu)

def diagonal (d : Vec) : Mat := fun i j => if i = j then d i else 0

/-- Exact rational witnesses can be cast into this real identity; R need not
be triangular. The convention is S = R^T diag(d) R. -/
theorem diagonal_factor_psd (S R : Mat) (d : Vec)
    (hd : ∀ i, 0 ≤ d i) (hfactor : S = congruence (diagonal d) R) :
    QuadraticPSD S := by
  intro v
  rw [hfactor, quad_congruence]
  have hdiag : quad (diagonal d) (mapVec R v) =
      ∑ i, d i * (mapVec R v i)^2 := by
    simp [quad, diagonal]
    <;> apply Finset.sum_congr rfl
    <;> intro i hi
    <;> ring
  rw [hdiag]
  exact Finset.sum_nonneg (fun i _ => mul_nonneg (hd i) (sq_nonneg _))

/-- Constructor used by a future exact certificate exporter. No witness for
any concrete source-bound gain is instantiated here. -/
def spn_of_diagonal_factor (M S N R : Mat) (d : Vec)
    (hS : Symmetric S) (hN : Symmetric N)
    (hsum : ∀ i j, M i j = S i j + N i j)
    (hfactor : S = congruence (diagonal d) R)
    (hd : ∀ i, 0 ≤ d i) (hn : ∀ i j, 0 ≤ N i j) : SPNCertificate M where
  S := S
  N := N
  s_symmetric := hS
  n_symmetric := hN
  decomposition := hsum
  psd := diagonal_factor_psd S R d hd hfactor
  entrywise := hn

def ResidualEnvelope (K : Gain) (z : Vec) (r : Fin 2 → ℝ) : Prop :=
  ∀ a, |r a| ≤ ∑ j, K a j * |z j|

def coupling (z : Vec) (r : Fin 2 → ℝ) : ℝ :=
  ∑ a, channelSum z a * r a

theorem residual_power_le_absEnvelope (K : Gain) (z : Vec) (r : Fin 2 → ℝ)
    (hr : ResidualEnvelope K z r) : |coupling z r| ≤ absEnvelope K z := by
  calc
    |coupling z r| ≤ ∑ a, |channelSum z a * r a| :=
      Finset.abs_sum_le_sum_abs _ _
    _ = ∑ a, |channelSum z a| * |r a| := by simp only [abs_mul]
    _ ≤ absEnvelope K z := by
      apply Finset.sum_le_sum
      intro a ha
      exact mul_le_mul_of_nonneg_left (hr a) (abs_nonneg _)

theorem spn_feasible_cone_envelope (K : Gain) (mu : ℝ)
    (cert : ∀ r : Representative, SPNCertificate (H K mu (representativeCone r))) :
    DirectEnvelope K mu := by
  apply (exact_eighteen_cone_reduction K mu).mpr
  intro r
  exact spn_quadratic_nonnegative_on_orthant _ (cert r)

theorem spn_feasible_cone_small_gain (K : Gain) (mu : ℝ)
    (cert : ∀ c : Representative, SPNCertificate (H K mu (representativeCone c)))
    (z : Vec) (r : Fin 2 → ℝ) (hr : ResidualEnvelope K z r) :
    |coupling z r| ≤ mu * Q z := by
  exact le_trans (residual_power_le_absEnvelope K z r hr)
    (spn_feasible_cone_envelope K mu cert z)

/-- Typed nonnegative-gain wrapper for future source adapters. -/
structure ComponentGain where
  value : Gain
  nonnegative : ∀ a j, 0 ≤ value a j

theorem feasible_cone_direct_small_gain (K : ComponentGain) (mu : ℝ)
    (cert : ∀ c : Representative, SPNCertificate (H K.value mu (representativeCone c)))
    (z : Vec) (r : Fin 2 → ℝ) (hr : ResidualEnvelope K.value z r) :
    |coupling z r| ≤ mu * Q z :=
  spn_feasible_cone_small_gain K.value mu cert z r hr

/-- Pointwise ledger only; no trajectory or exponential-decay theorem. -/
theorem no_bias_ledger (z : Vec) (r : Fin 2 → ℝ) (mu Vdot : ℝ)
    (hpower : |coupling z r| ≤ mu * Q z)
    (hdot : Vdot ≤ -Q z + coupling z r) : Vdot ≤ -(1-mu)*Q z := by
  have habs := le_abs_self (coupling z r)
  nlinarith

/-- SPN contains global PSD as the special case N=0. -/
def spn_of_psd (M : Mat) (hM : Symmetric M) (hpsd : QuadraticPSD M) :
    SPNCertificate M where
  S := M
  N := fun _ _ => 0
  s_symmetric := hM
  n_symmetric := by intro i j; rfl
  decomposition := by intro i j; simp
  psd := hpsd
  entrywise := by intro i j; exact le_refl 0

def gapN : Mat := ![![0, 1, 0, 0], ![1, 0, 0, 0], ![0, 0, 0, 0], ![0, 0, 0, 0]]

def gapCertificate : SPNCertificate gapN where
  S := fun _ _ => 0
  N := gapN
  s_symmetric := by intro i j; rfl
  n_symmetric := by intro i j; fin_cases i <;> fin_cases j <;> norm_num [gapN]
  decomposition := by intro i j; simp
  psd := by intro v; simp [quad]
  entrywise := by intro i j; fin_cases i <;> fin_cases j <;> norm_num [gapN]

theorem spn_not_global_psd : Copositive gapN ∧ ¬ QuadraticPSD gapN := by
  constructor
  · exact spn_quadratic_nonnegative_on_orthant gapN gapCertificate
  · intro h
    have hbad := h ![1, -1, 0, 0]
    norm_num [quad, gapN, Fin.sum_univ_succ] at hbad

end

end RouteBP5FeasibleConeSPN

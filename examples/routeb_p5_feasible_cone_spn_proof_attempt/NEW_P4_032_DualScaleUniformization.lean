import NEW_P4_032_DualScaleComposition

/-!
OPEN_UNCOMPILED. Domain-uniform bounds above the existing local composition.
Finite bounds do not automatically discharge normalization or allocation.
No Lean/Lake run, registry mutation or source/coverage/PSD claim.
-/

set_option autoImplicit false

namespace RouteBP4032DualScaleUniformization

open RouteBP4032UniformParameterBridge
open RouteBP4032ResidualMarginConsumer
open RouteBP4032Body6SchurScalarAdapter
open RouteBP4032MinimalResidualBudgetAdapter
open RouteBP4032DualScaleComposition
open RouteBP4032DomainUniformContraction

noncomputable section

/-- Uniform evidence for the same functions and domain as local composition.
The extra nominal_realization is NOT implied by its nominal upper bound. -/
structure UniformData {X : Type*} (f : ParameterField X)
    (d : RemainderField X) (m : MarginField X) (s : ScaleFields X) where
  alphaFloor : ℝ
  frontFloor : ℝ
  offsetFloor : ℝ
  betaCap : ℝ
  gainCap : ℝ
  qCap : ℝ
  alphaFloor_nonnegative : 0 ≤ alphaFloor
  frontFloor_nonnegative : 0 ≤ frontFloor
  betaCap_nonnegative : 0 ≤ betaCap
  gainCap_nonnegative : 0 ≤ gainCap
  qCap_nonnegative : 0 ≤ qCap
  alpha_bound : ∀ x, f.domain x → alphaFloor ≤ (s.front x).value
  front_bound : ∀ x, f.domain x → frontFloor ≤ d.mu x * frontEnergy (d.front x)
  offset_bound : ∀ x, f.domain x → offsetFloor ≤ d.offset x
  beta_bound : ∀ x, f.domain x → (s.residual x).value ≤ betaCap
  gain_bound : ∀ x, f.domain x → m.gain x ≤ gainCap
  q_nonnegative : ∀ x, f.domain x → 0 ≤ f.residual x
  q_bound : ∀ x, f.domain x → f.residual x ≤ qCap
  nominal_realization : ∀ x, f.domain x →
    d.offset x + (s.front x).value * (d.mu x * frontEnergy (d.front x)) ≤ m.nominal x

/-- Pointwise qCap(x) needs its OWN same-domain upper bound before it can
be replaced by a single qCap. Finite bounds on unrelated samples do not suffice. -/
def capFromLocalBounds {X : Type*} (f : ParameterField X)
    (localCap : X → ℝ) (qCap : ℝ) (hc0 : 0 ≤ qCap)
    (hq0 : ∀ x, f.domain x → 0 ≤ f.residual x)
    (hq : ∀ x, f.domain x → f.residual x ≤ localCap x)
    (hc : ∀ x, f.domain x → localCap x ≤ qCap) : CapEvidence f qCap where
  cap_nonnegative := hc0
  residual_nonnegative := hq0
  bound := fun x hx => (hq x hx).trans (hc x hx)

def uniformCapEvidence {X : Type*} (f : ParameterField X)
    (d : RemainderField X) (m : MarginField X) (s : ScaleFields X)
    (u : UniformData f d m s) : CapEvidence f u.qCap where
  cap_nonnegative := u.qCap_nonnegative
  residual_nonnegative := u.q_nonnegative
  bound := u.q_bound

/-- Convert ONE uniform allocation to all the local allocations. Alpha
uses a lower bound; beta/gain use upper bounds and the identical qCap. -/
def uniformTargetAllocation {X : Type*} (f : ParameterField X)
    (d : RemainderField X) (m : MarginField X) (s : ScaleFields X)
    (b : CompositionContract f d m s) (u : UniformData f d m s)
    (target : ℝ)
    (ha : target + u.gainCap * (u.betaCap * u.qCap) ≤
      u.offsetFloor + u.alphaFloor * u.frontFloor) :
    TargetAllocation f m (residualValues s) u.qCap target where
  lower := by
    intro x hx
    have hfront := mul_le_mul (u.alpha_bound x hx) (u.front_bound x hx)
      u.frontFloor_nonnegative (b.front_nonnegative x hx)
    have hnominal := (add_le_add (u.offset_bound x hx) hfront).trans
      (u.nominal_realization x hx)
    have hbeta := mul_le_mul_of_nonneg_right (u.beta_bound x hx) u.qCap_nonnegative
    have hres := mul_le_mul (u.gain_bound x hx) hbeta
      (mul_nonneg (b.residual_nonnegative x hx) u.qCap_nonnegative) u.gainCap_nonnegative
    change target + m.gain x * ((s.residual x).value * u.qCap) ≤ m.nominal x
    linarith

/-- All local normalization premises remain in b. No local composition
proof is repeated; only its uniform inputs have been constructed. -/
theorem uniformized_scalar_margin {X : Type*} (f : ParameterField X)
    (d : RemainderField X) (m : MarginField X) (s : ScaleFields X)
    (b : CompositionContract f d m s) (u : UniformData f d m s)
    (target : ℝ)
    (ha : target + u.gainCap * (u.betaCap * u.qCap) ≤
      u.offsetFloor + u.alphaFloor * u.frontFloor) :
    ∀ x, f.domain x → target ≤ m.margin x :=
  composed_scalar_margin f u.qCap (uniformCapEvidence f d m s u) d m s b target
    (uniformTargetAllocation f d m s b u target ha)

/-- Every real-valued function on a fixed finite set has a finite upper
bound; choosing the empty-set bound 0 also makes this bound nonnegative. -/
theorem finite_upper {X : Type*} (cells : Finset X) (v : X → ℝ) :
    ∃ upper : ℝ, 0 ≤ upper ∧ ∀ x ∈ cells, v x ≤ upper := by
  classical
  induction cells using Finset.induction_on with
  | empty => exact ⟨0, le_rfl, by simp⟩
  | @insert a cells ha ih =>
      obtain ⟨upper, h0, hu⟩ := ih
      refine ⟨max (v a) upper, h0.trans (le_max_right _ _), ?_⟩
      intro x hx
      rcases Finset.mem_insert.mp hx with hxa | hxs
      · subst x
        exact le_max_left _ _
      · exact (hu x hxs).trans (le_max_right _ _)

theorem finite_lower_upper {X : Type*} (cells : Finset X) (v : X → ℝ) :
    ∃ lower upper : ℝ, ∀ x ∈ cells, lower ≤ v x ∧ v x ≤ upper := by
  obtain ⟨upper, _, hu⟩ := finite_upper cells v
  obtain ⟨negLower, _, hl⟩ := finite_upper cells (fun x => -v x)
  refine ⟨-negLower, upper, ?_⟩
  intro x hx
  exact ⟨by linarith [hl x hx], hu x hx⟩

/-- Simultaneous finite upper bound for the slots alpha,beta,gain,local qCap.
For nonnegative slots, 0 supplies their common nonnegative lower bound. -/
theorem finite_four_envelope {X : Type*} (cells : Finset X) (v : X → Fin 4 → ℝ)
    (h0 : ∀ x ∈ cells, ∀ i, 0 ≤ v x i) :
    ∃ upper : ℝ, 0 ≤ upper ∧ ∀ x ∈ cells, ∀ i, 0 ≤ v x i ∧ v x i ≤ upper := by
  classical
  obtain ⟨upper, hu0, hu⟩ := finite_upper (cells.product Finset.univ)
    (fun p : X × Fin 4 => v p.1 p.2)
  refine ⟨upper, hu0, ?_⟩
  intro x hx i
  exact ⟨h0 x hx i, hu (x, i) (Finset.mem_product.mpr ⟨hx, Finset.mem_univ i⟩)⟩

/-- A STRICTLY positive finite alpha floor requires pointwise positivity.
Reuse the earlier finite strict-majorant theorem rather than reprove min. -/
theorem finite_positive_floor {X : Type*} (cells : Finset X) (alpha : X → ℝ)
    (hpos : ∀ x ∈ cells, 0 < alpha x) :
    ∃ lower : ℝ, 0 < lower ∧ ∀ x ∈ cells, lower ≤ alpha x := by
  obtain ⟨r, hr, hb⟩ := finite_strict_majorant cells (fun x => 1 - alpha x)
    (by intro x hx; linarith [hpos x hx])
  refine ⟨1 - r, sub_pos.mpr hr, ?_⟩
  intro x hx
  linarith [hb x hx]

/-- Infinite-domain positive alpha_n=0.5^n has no positive uniform floor. -/
theorem no_positive_dyadic_floor :
    ¬ ∃ lower : ℝ, 0 < lower ∧ ∀ n : ℕ, lower ≤ dyadicGap n := by
  rintro ⟨lower, hpos, hb⟩
  apply no_dyadic_uniform_rho
  refine ⟨1 - lower, by linarith, ?_⟩
  intro n
  unfold dyadicRho
  linarith [hb n]

/-- beta_n, gain_n, or q_n may independently be 2^n: pointwise finite and
nonnegative does not imply a finite common cap on an infinite domain. -/
theorem no_dyadic_upper :
    ¬ ∃ upper : ℝ, ∀ n : ℕ, dyadicEnergy n ≤ upper := by
  rintro ⟨upper, hb⟩
  obtain ⟨n, hn⟩ := dyadic_exceeds upper
  exact (not_le_of_gt hn) (hb n)

/-- With alpha=L=Q=g=q=1 and beta_n=2^n, normalized margin=1-beta_n
obeys comparison exactly, but defeats every uniform target. The same
scalar expression results if gain or q is the growing slot instead. -/
theorem infinite_margin_counterexample (target : ℝ) :
    ∃ n : ℕ, 0 ≤ dyadicEnergy n ∧
      1 - 1 * (dyadicEnergy n * 1) < target := by
  obtain ⟨n, hn⟩ := dyadic_exceeds (1 - target)
  exact ⟨n, (dyadic_point n).1, by nlinarith⟩

end

-- Future audit commands only; NOT executed in this round.
#print axioms uniformTargetAllocation
#print axioms capFromLocalBounds
#print axioms uniformized_scalar_margin
#print axioms finite_upper
#print axioms finite_lower_upper
#print axioms finite_four_envelope
#print axioms finite_positive_floor
#print axioms no_positive_dyadic_floor
#print axioms no_dyadic_upper
#print axioms infinite_margin_counterexample

end RouteBP4032DualScaleUniformization

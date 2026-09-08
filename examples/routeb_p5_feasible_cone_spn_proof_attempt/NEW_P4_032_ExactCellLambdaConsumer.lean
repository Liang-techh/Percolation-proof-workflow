import NEW_P4_032_DHProducerBaseBridge
import examples.routeb_p4_rational_lambda_guard_lean.P4RationalLambdaGuard

/-!
OPEN_UNCOMPILED / pending. Exact same-source rational cell envelopes.
No Float64 input, sampling, source authentication, Lean/Lake execution,
physical DH closure, PSD conclusion or registry action.
-/
set_option autoImplicit false

namespace RouteBP4032ExactCellLambdaConsumer

open RouteBP4032SameSourceConsumerPacket RouteBP4RationalLambdaGuard
open RouteBP4032UniformParameterBridge RouteBP4032ResidualMarginConsumer
open RouteBP4032DualScaleComposition RouteBP4032MinimalResidualBudgetAdapter

noncomputable section

/-- A is a base-residual SQUARED charge, not the producer metric A_up.
P is an uninflated port squared charge; D reserves the positive target. -/
structure RationalCharges (ι : Type*) where
  A : ι → ℚ
  P : ι → ℚ
  D : ι → ℚ
  target : ℚ
  A_nonnegative : ∀ i, 0 ≤ A i
  P_nonnegative : ∀ i, 0 ≤ P i
  target_positive : 0 < target

/-- Every row refers to the same source functions, target and source domain.
The cover is a proof, not a finite list or sampling assertion. -/
structure SameSourceCharges {key : SourceKey} {X ι : Type*}
    (src : SourceFields key X) (c : RationalCharges ι) where
  cell : ι → X → Prop
  cover : ∀ x, src.domain x → ∃ i, cell i x
  A_upper : ∀ i x, src.domain x → cell i x → sqNorm (src.lBase x) ≤ (c.A i : ℝ)
  P_upper : ∀ i x, src.domain x → cell i x → sqNorm (src.port x) ≤ (c.P i : ℝ)
  D_lower : ∀ i x, src.domain x → cell i x →
    (c.target : ℝ) + (c.D i : ℝ) ≤ src.base x

/-- The DH producer bridge can supply e. Its rhoSq is used BEFORE the
theta=1 charge inflation; metric and residual remain distinct objects. -/
def chargesFromProducer {key : SourceKey} {X ι : Type*}
    (src : SourceFields key X) (row : RowInterpretation key)
    (e : RowSourceEvidence row src) (c : RationalCharges ι)
    (cell : ι → X → Prop) (cover : ∀ x, src.domain x → ∃ i, cell i x)
    (ha : ∀ i x, src.domain x → cell i x → sqNorm (src.lBase x) ≤ (c.A i : ℝ))
    (hp : ∀ i x, src.domain x → cell i x → row.rhoSq * metric src x ≤ (c.P i : ℝ))
    (hd : ∀ i x, src.domain x → cell i x →
      (c.target : ℝ) + (c.D i : ℝ) ≤ src.base x) : SameSourceCharges src c where
  cell := cell
  cover := cover
  A_upper := ha
  P_upper := fun i x hx hi => (e.port_bound x hx).trans (hp i x hx hi)
  D_lower := hd

/-- Division-free weighted Young identity. Its nonnegative defect is the
sum of (u_j-s*v_j)^2; positivity of s is needed later for envelopes/canceling. -/
theorem scaled_young (u v : Fin 2 → ℝ) (s : ℝ) :
    s * sqNorm (fun j => u j + v j) ≤
      (s + 1) * sqNorm u + s * (s + 1) * sqNorm v := by
  unfold sqNorm
  nlinarith [sq_nonneg (u 0 - s * v 0), sq_nonneg (u 1 - s * v 1)]

theorem guard_allocation_identity (A P D s : ℝ) :
    quadratic P (D - A - P) A s =
      (s + 1) * A + s * (s + 1) * P - s * D := by
  unfold quadratic
  ring

structure RationalGuard {ι : Type*} (c : RationalCharges ι) where
  lo : ℚ
  hi : ℚ
  lo_positive : 0 < lo
  ordered : lo ≤ hi
  left : ∀ i, c.P i * lo^2 - (c.D i - c.A i - c.P i) * lo + c.A i ≤ 0
  right : ∀ i, c.P i * hi^2 - (c.D i - c.A i - c.P i) * hi + c.A i ≤ 0

/-- Reuses the existing guard theorem; no roots, floats or grid search. -/
theorem guard_at_rational {ι : Type*} (c : RationalCharges ι) (g : RationalGuard c)
    (s : ℚ) (hl : g.lo ≤ s) (hh : s ≤ g.hi) :
    ∀ i, quadratic (c.P i : ℝ) ((c.D i : ℝ) - (c.A i : ℝ) - (c.P i : ℝ))
      (c.A i : ℝ) (s : ℝ) ≤ 0 := by
  apply common_lambda_interval (fun i => (c.P i : ℝ))
    (fun i => (c.D i : ℝ) - (c.A i : ℝ) - (c.P i : ℝ))
    (fun i => (c.A i : ℝ)) (g.lo : ℝ) (g.hi : ℝ) (s : ℝ)
  · intro i
    exact_mod_cast c.P_nonnegative i
  · exact_mod_cast g.ordered
  · exact_mod_cast hl
  · exact_mod_cast hh
  · intro i
    unfold quadratic
    exact_mod_cast g.left i
  · intro i
    unfold quadratic
    exact_mod_cast g.right i

theorem same_source_scalar_floor {key : SourceKey} {X ι : Type*}
    (src : SourceFields key X) (c : RationalCharges ι) (e : SameSourceCharges src c)
    (s : ℝ) (hs : 0 < s)
    (hg : ∀ i, quadratic (c.P i : ℝ) ((c.D i : ℝ) - (c.A i : ℝ) - (c.P i : ℝ))
      (c.A i : ℝ) s ≤ 0) :
    ∀ x, src.domain x → (c.target : ℝ) ≤ src.base x - totalSq src x := by
  intro x hx
  obtain ⟨i, hi⟩ := e.cover x hx
  have hsp : 0 ≤ s + 1 := by linarith
  have hprod : 0 ≤ s * (s + 1) := mul_nonneg (le_of_lt hs) hsp
  have hy := scaled_young (src.lBase x) (src.port x) s
  have ha := mul_le_mul_of_nonneg_left (e.A_upper i x hx hi) hsp
  have hp := mul_le_mul_of_nonneg_left (e.P_upper i x hx hi) hprod
  have hd := mul_le_mul_of_nonneg_left (e.D_lower i x hx hi) (le_of_lt hs)
  have hq := hg i
  rw [guard_allocation_identity] at hq
  have hscaled : s * ((c.target : ℝ) - (src.base x - totalSq src x)) ≤ 0 := by
    dsimp [totalSq]
    nlinarith
  by_contra hnot
  have hpos : 0 < s * ((c.target : ℝ) - (src.base x - totalSq src x)) :=
    mul_pos hs (sub_pos.mpr (lt_of_not_ge hnot))
  linarith

theorem rational_common_source_target {key : SourceKey} {X ι : Type*}
    (src : SourceFields key X) (c : RationalCharges ι) (e : SameSourceCharges src c)
    (g : RationalGuard c) (s : ℚ) (hl : g.lo ≤ s) (hh : s ≤ g.hi) :
    ∀ x, src.domain x → 0 < (c.target : ℝ) ∧
      (c.target : ℝ) ≤ src.base x - totalSq src x := by
  have hsQ : 0 < s := lt_of_lt_of_le g.lo_positive hl
  have hs : 0 < (s : ℝ) := by exact_mod_cast hsQ
  have hf := same_source_scalar_floor src c e (s : ℝ) hs (guard_at_rational c g s hl hh)
  intro x hx
  exact ⟨by exact_mod_cast c.target_positive, hf x hx⟩

/-- A general-lambda floor uses the same P4 normalization equalities, without
claiming that the stricter theta=1 Allocation record has been constructed. -/
theorem source_floor_to_P4 {key : SourceKey} {X Z : Type*}
    (src : SourceFields key X) (target : ℝ) (ht : 0 < target)
    (hf : ∀ x, src.domain x → target ≤ src.base x - totalSq src x)
    (f : ParameterField Z) (m : MarginField Z) (scales : ScaleFields Z)
    (embed : X → Z) (nu : ℝ) (hn : 0 < nu)
    (binding : P4Binding src f m scales embed nu)
    (comparison : ScaledComparison f m (residualValues scales)) :
    ∀ x, src.domain x → 0 < nu * target ∧ nu * target ≤ m.margin (embed x) := by
  intro x hx
  refine ⟨mul_pos hn ht, ?_⟩
  have hm := comparison.lower (embed x) (binding.covered x hx)
  simp only [residualValues, ← mul_assoc] at hm
  rw [binding.nominal_eq x hx, binding.residual_eq x hx, binding.gain_scale_eq x hx] at hm
  have hscaled := mul_le_mul_of_nonneg_left (hf x hx) (le_of_lt hn)
  nlinarith

/-- At lambda=2, the old theta=1 source cost is recovered. -/
theorem shift_one_identity (A P D : ℝ) :
    quadratic P (D - A - P) A 1 = 2 * A + 2 * P - D := by
  unfold quadratic
  ring

/-- Omitting target reservation makes a passing guard unsound for target=1.
u=v=(1,0), base=4: the actual residual-square charge is exactly 4. -/
theorem forgetting_target_counterexample :
    quadratic 1 (4 - 1 - 1) 1 1 = 0 ∧
    0 < quadratic 1 (3 - 1 - 1) 1 1 ∧
    ¬ (1 : ℝ) ≤ 4 - sqNorm (fun j : Fin 2 => if j = 0 then 2 else 0) := by
  norm_num [quadratic, sqNorm]

end
end RouteBP4032ExactCellLambdaConsumer

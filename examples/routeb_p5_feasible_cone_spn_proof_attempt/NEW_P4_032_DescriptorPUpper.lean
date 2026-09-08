import NEW_P4_032_DHAnalyticAUpper

/-!
OPEN_UNCOMPILED / pending. Full-descriptor RHS bound -> absolute port cap.
No concrete RHS/port/source bounds are assumed from a numeric receipt.
No Lean/Lake run, sampled maximum, physical or registry claim.
-/
set_option autoImplicit false

namespace RouteBP4032DescriptorPUpper

open RouteBP4032SameSourceConsumerPacket RouteBP4032BlockDefects
open scoped BigOperators

noncomputable section

def fullSq (a : Vec6) : ℝ := ∑ j, a j ^ 2
def dot6 (a b : Vec6) : ℝ := ∑ j, a j * b j

theorem square_difference_identity (mu : ℝ) (a rhs : Vec6) :
    (∑ j, (mu * a j - rhs j)^2) =
      mu^2 * fullSq a - 2 * mu * dot6 a rhs + fullSq rhs := by
  calc
    (∑ j, (mu * a j - rhs j)^2) =
        ∑ j, (mu^2 * a j^2 - (2 * mu) * (a j * rhs j) + rhs j^2) := by
      apply Finset.sum_congr rfl
      intro j _
      ring
    _ = mu^2 * fullSq a - 2 * mu * dot6 a rhs + fullSq rhs := by
      simp only [fullSq, dot6, Finset.sum_add_distrib, Finset.sum_sub_distrib,
        ← Finset.mul_sum]

/-- Coercivity and the FULL descriptor give a squared acceleration estimate
without a matrix inverse or a square root. -/
theorem full_descriptor_energy_bound (M : Mat6) (a rhs : Vec6) (mu : ℝ)
    (hmu : 0 ≤ mu) (hcoercive : mu * fullSq a ≤ dot6 a (M *ᵥ a))
    (heq : M *ᵥ a = rhs) : mu^2 * fullSq a ≤ fullSq rhs := by
  rw [heq] at hcoercive
  have hsq : 0 ≤ ∑ j, (mu * a j - rhs j)^2 :=
    Finset.sum_nonneg (fun j _ => sq_nonneg _)
  rw [square_difference_identity] at hsq
  have hscaled := mul_le_mul_of_nonneg_left hcoercive hmu
  nlinarith

def metricMax : ℝ := 1402217 / 12000000

/-- Exact producer metric bounded by the full six-acceleration square.
The component equalities prevent silently replacing the state acceleration. -/
theorem metric_le_full {key : SourceKey} {X : Type*}
    (src : SourceFields key X) (x : X) (a : Vec6)
    (h4 : src.acceleration x 0 = a 3) (h5 : src.acceleration x 1 = a 4) :
    metric src x ≤ metricMax * fullSq a := by
  unfold metric
  rw [h4, h5]
  simp [metricMax, fullSq, Fin.sum_univ_succ]
  nlinarith [sq_nonneg (a 0), sq_nonneg (a 1), sq_nonneg (a 2),
    sq_nonneg (a 3), sq_nonneg (a 4), sq_nonneg (a 5)]

/-- Scalar certificates are division-free: Bmax*H <= mu^2*K.
H and K may be rational envelopes cast to real; neither is invented here. -/
theorem descriptor_metric_cap {key : SourceKey} {X : Type*}
    (src : SourceFields key X) (x : X) (M : Mat6) (a rhs : Vec6)
    (mu H K : ℝ) (hmu : 0 < mu)
    (h4 : src.acceleration x 0 = a 3) (h5 : src.acceleration x 1 = a 4)
    (hcoercive : mu * fullSq a ≤ dot6 a (M *ᵥ a)) (heq : M *ᵥ a = rhs)
    (hrhs : fullSq rhs ≤ H) (hK : metricMax * H ≤ mu^2 * K) : metric src x ≤ K := by
  have he := full_descriptor_energy_bound M a rhs mu (le_of_lt hmu) hcoercive heq
  have hm := mul_le_mul_of_nonneg_left (metric_le_full src x a h4 h5) (sq_nonneg mu)
  have hH := mul_le_mul_of_nonneg_left (he.trans hrhs) (show 0 ≤ metricMax by norm_num [metricMax])
  have hscaled : mu^2 * metric src x ≤ mu^2 * K := by nlinarith
  have hmu2 : 0 < mu^2 := by positivity
  by_contra hn
  have hp : 0 < mu^2 * (metric src x - K) :=
    mul_pos hmu2 (sub_pos.mpr (lt_of_not_ge hn))
  nlinarith

/-- Direct P_upper field construction on any proved same cell. mu is the
full-mass coercivity constant, not the scalar margin normalization nu. -/
theorem same_cell_P_upper {key : SourceKey} {X ι : Type*}
    (src : SourceFields key X) (cell : ι → X → Prop)
    (mass : X → Mat6) (acc rhs : X → Vec6)
    (mu : ℝ) (rhoSq H K P : ι → ℚ) (hmu : 0 < mu)
    (hrho : ∀ i, 0 ≤ rhoSq i)
    (h4 : ∀ i x, src.domain x → cell i x → src.acceleration x 0 = acc x 3)
    (h5 : ∀ i x, src.domain x → cell i x → src.acceleration x 1 = acc x 4)
    (hcoercive : ∀ i x, src.domain x → cell i x →
      mu * fullSq (acc x) ≤ dot6 (acc x) (mass x *ᵥ acc x))
    (heq : ∀ i x, src.domain x → cell i x → mass x *ᵥ acc x = rhs x)
    (hH : ∀ i x, src.domain x → cell i x → fullSq (rhs x) ≤ (H i : ℝ))
    (hK : ∀ i, metricMax * (H i : ℝ) ≤ mu^2 * (K i : ℝ))
    (hport : ∀ i x, src.domain x → cell i x →
      sqNorm (src.port x) ≤ (rhoSq i : ℝ) * metric src x)
    (hP : ∀ i, rhoSq i * K i ≤ P i) :
    ∀ i x, src.domain x → cell i x → sqNorm (src.port x) ≤ (P i : ℝ) := by
  intro i x hx hi
  have hk := descriptor_metric_cap src x (mass x) (acc x) (rhs x) mu (H i : ℝ) (K i : ℝ)
    hmu (h4 i x hx hi) (h5 i x hx hi) (hcoercive i x hx hi) (heq i x hx hi)
    (hH i x hx hi) (hK i)
  have hr : 0 ≤ (rhoSq i : ℝ) := by exact_mod_cast hrho i
  have hp : (rhoSq i : ℝ) * (K i : ℝ) ≤ (P i : ℝ) := by exact_mod_cast hP i
  exact (hport i x hx hi).trans ((mul_le_mul_of_nonneg_left hk hr).trans hp)

/-- Even an exact positive scalar mass and full descriptor cannot bound
acceleration/port without an RHS/domain restriction. This is a scalar model,
not a claim that a corresponding unrestricted ray is physically admissible. -/
theorem missing_rhs_cap_obstruction (mu cap : ℝ) (_hmu : 0 < mu) (hc : 0 ≤ cap) :
    ∃ a rhs : ℝ, mu * a = rhs ∧ mu * a^2 = a * rhs ∧ cap < a^2 := by
  refine ⟨cap + 1, mu * (cap + 1), rfl, ?_, ?_⟩
  · ring
  · nlinarith [sq_nonneg cap]

end
end RouteBP4032DescriptorPUpper

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# P3 uniform strict slack consumer

This sidecar separates pointwise positivity from a domain-wide uniform gap.
The counterexample is exact-real and parameterized; the consumer accepts a
uniform lower bound as an external certificate and transfers it to capMax.
No prior family-level load witness or strict-slack theorem is rebuilt here.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullUniformSlack

noncomputable section

abbrev I6 := Fin 6

def counterexampleDomain (x : ℝ) : Prop := 0 ≤ x

def reciprocalGap (x : ℝ) : ℝ := 1 / (x + 1)

theorem reciprocalGap_pointwise_positive
    (x : ℝ) (hx : counterexampleDomain x) : 0 < reciprocalGap x := by
  unfold counterexampleDomain at hx
  unfold reciprocalGap
  have hden : 0 < x + 1 := by linarith
  positivity

theorem reciprocalGap_no_uniform_positive_lower_bound
    (ε : ℝ) (hε : 0 < ε) :
    ∃ x : ℝ, counterexampleDomain x ∧ reciprocalGap x < ε := by
  refine ⟨1 / ε, ?_, ?_⟩
  · unfold counterexampleDomain
    positivity
  · unfold reciprocalGap
    have hεne : ε ≠ 0 := ne_of_gt hε
    have hden : 0 < 1 + ε := by linarith
    calc
      1 / (1 / ε + 1) = ε / (1 + ε) := by
        field_simp [hεne, ne_of_gt hden]
      _ < ε := by
        apply (div_lt_iff₀ hden).2
        nlinarith [sq_nonneg ε]

theorem pointwise_positive_not_uniform
    : (∀ x : ℝ, counterexampleDomain x → 0 < reciprocalGap x) ∧
      (∀ ε : ℝ, 0 < ε →
        ∃ x : ℝ, counterexampleDomain x ∧ reciprocalGap x < ε) := by
  constructor
  · exact reciprocalGap_pointwise_positive
  · exact reciprocalGap_no_uniform_positive_lower_bound

/-! The uniform certificate is the only quantitative input of the consumer. -/

structure UniformGapCapCertificate (D : Type*) where
  domain : D → Prop
  weightedLoad : D → ℝ
  capLoad : D → ℝ
  capMaxLoad : D → ℝ
  uniformGap : ℝ
  uniformGap_positive : 0 < uniformGap
  uniform_gap_lower : ∀ x, domain x →
    uniformGap ≤ capLoad x - weightedLoad x
  cap_load_upper : ∀ x, domain x → capLoad x ≤ capMaxLoad x

theorem uniform_gap_capmax_margin
    {D : Type*} (C : UniformGapCapCertificate D) :
    ∀ x, C.domain x →
      C.weightedLoad x + C.uniformGap ≤ C.capMaxLoad x ∧
        C.weightedLoad x < C.capMaxLoad x := by
  intro x hx
  have hGapToCap :
      C.weightedLoad x + C.uniformGap ≤ C.capLoad x := by
    linarith [C.uniform_gap_lower x hx]
  have hMargin :
      C.weightedLoad x + C.uniformGap ≤ C.capMaxLoad x :=
    hGapToCap.trans (C.cap_load_upper x hx)
  constructor
  · exact hMargin
  · linarith [C.uniformGap_positive]

theorem uniform_gap_consumer_margin
    {D : Type*} (C : UniformGapCapCertificate D)
    (consumer : D → ℝ)
    (hConsumer : ∀ x, C.domain x → consumer x ≤ C.weightedLoad x) :
    ∀ x, C.domain x →
      consumer x + C.uniformGap ≤ C.capMaxLoad x ∧
        consumer x < C.capMaxLoad x := by
  intro x hx
  have hMargin := uniform_gap_capmax_margin C x hx
  constructor
  · linarith [hConsumer x hx, hMargin.1]
  · exact lt_of_le_of_lt (hConsumer x hx) hMargin.2

/-! Finite component families may expose the uniform lower bound upstream. -/

structure FiniteUniformGapCapCertificate6 (D : Type*)
    extends UniformGapCapCertificate D where
  pointwiseGap : I6 → D → ℝ
  finite_gap_lower : ∀ i x, domain x → uniformGap ≤ pointwiseGap i x

theorem finite_uniform_gap_capmax_margin6
    {D : Type*} (C : FiniteUniformGapCapCertificate6 D) :
    ∀ x, C.domain x →
      C.weightedLoad x + C.uniformGap ≤ C.capMaxLoad x ∧
        C.weightedLoad x < C.capMaxLoad x := by
  intro x hx
  exact uniform_gap_capmax_margin C.toUniformGapCapCertificate x hx

end

end RouteBP3CentralFDHullUniformSlack

#print axioms RouteBP3CentralFDHullUniformSlack.reciprocalGap_pointwise_positive
#print axioms RouteBP3CentralFDHullUniformSlack.reciprocalGap_no_uniform_positive_lower_bound
#print axioms RouteBP3CentralFDHullUniformSlack.uniform_gap_capmax_margin
#print axioms RouteBP3CentralFDHullUniformSlack.finite_uniform_gap_capmax_margin6

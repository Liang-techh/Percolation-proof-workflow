import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

/-!
# P3 interval-enclosure strict-slack consumer

This sidecar gives the smallest exact interface needed after box coverage:
each listed box has a positive gap lower bound, a cap-load upper chain, and an
explicit rounding/interval soundness premise.  The theorem consumes those
premises at a coverage witness; it does not manufacture interval certificates
from solver, sample, or grid data.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullIntervalEnclosure

noncomputable section

structure IntervalEnclosureCertificate (D B : Type*) [DecidableEq B] where
  domain : D → Prop
  boxes : Finset B
  region : B → D → Prop
  weightedLoad : D → ℝ
  capLoad : D → ℝ
  capLoadUpper : B → ℝ
  capMaxLoad : D → ℝ
  gapLower : B → ℝ
  rounding_interval_sound : B → Prop
  soundness : ∀ b, b ∈ boxes → rounding_interval_sound b
  gap_lower_sound : ∀ b, b ∈ boxes → rounding_interval_sound b →
    ∀ x, region b x → gapLower b ≤ capLoad x - weightedLoad x
  cap_load_upper_sound : ∀ b, b ∈ boxes → rounding_interval_sound b →
    ∀ x, region b x → capLoad x ≤ capLoadUpper b
  cap_upper_to_capMax : ∀ b, b ∈ boxes → rounding_interval_sound b →
    ∀ x, region b x → capLoadUpper b ≤ capMaxLoad x
  gap_lower_positive : ∀ b, b ∈ boxes → rounding_interval_sound b →
    0 < gapLower b
  coverage : ∀ x, domain x → ∃ b, b ∈ boxes ∧ region b x

theorem interval_enclosure_strict_slack
    {D B : Type*} [DecidableEq B]
    (C : IntervalEnclosureCertificate D B) :
    ∀ x, C.domain x →
      ∃ b, b ∈ C.boxes ∧ C.region b x ∧
        C.rounding_interval_sound b ∧
        C.weightedLoad x + C.gapLower b ≤ C.capMaxLoad x ∧
        C.weightedLoad x < C.capMaxLoad x := by
  intro x hx
  rcases C.coverage x hx with ⟨b, hb, hRegion⟩
  have hSound : C.rounding_interval_sound b := C.soundness b hb
  have hGapPos : 0 < C.gapLower b := C.gap_lower_positive b hb hSound
  have hGapLower :
      C.gapLower b ≤ C.capLoad x - C.weightedLoad x :=
    C.gap_lower_sound b hb hSound x hRegion
  have hCapUpper : C.capLoad x ≤ C.capLoadUpper b :=
    C.cap_load_upper_sound b hb hSound x hRegion
  have hCapMax : C.capLoadUpper b ≤ C.capMaxLoad x :=
    C.cap_upper_to_capMax b hb hSound x hRegion
  have hGapToCap :
      C.weightedLoad x + C.gapLower b ≤ C.capLoadUpper b := by
    linarith
  have hMargin :
      C.weightedLoad x + C.gapLower b ≤ C.capMaxLoad x :=
    hGapToCap.trans hCapMax
  refine ⟨b, hb, hRegion, hSound, hMargin, ?_⟩
  linarith [hGapPos]

theorem interval_enclosure_consumer_strict
    {D B : Type*} [DecidableEq B]
    (C : IntervalEnclosureCertificate D B)
    (consumer : D → ℝ)
    (hConsumer : ∀ x, C.domain x → consumer x ≤ C.weightedLoad x) :
    ∀ x, C.domain x → consumer x < C.capMaxLoad x := by
  intro x hx
  rcases interval_enclosure_strict_slack C x hx with
    ⟨b, hb, hRegion, hSound, hMargin, hStrict⟩
  exact lt_of_le_of_lt (hConsumer x hx) hStrict

/-! Exact-real sample/solver positivity is not interval soundness. -/

def sampledGap : Bool → ℝ
  | false => 1
  | true => -1

theorem sample_without_interval_soundness_not_global :
    0 < sampledGap false ∧ ∃ x, sampledGap x ≤ 0 := by
  constructor
  · norm_num [sampledGap]
  · exact ⟨true, by norm_num [sampledGap]⟩

end

end RouteBP3CentralFDHullIntervalEnclosure

#print axioms RouteBP3CentralFDHullIntervalEnclosure.interval_enclosure_strict_slack
#print axioms RouteBP3CentralFDHullIntervalEnclosure.interval_enclosure_consumer_strict
#print axioms RouteBP3CentralFDHullIntervalEnclosure.sample_without_interval_soundness_not_global

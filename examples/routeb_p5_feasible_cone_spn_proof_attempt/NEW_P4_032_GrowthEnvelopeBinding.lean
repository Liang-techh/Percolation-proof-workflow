import NEW_P4_032_DescriptorPUpper

/-!
OPEN_UNCOMPILED / pending. Conditional consumer of the external exact-real
DH growth envelope. Constants are transcribed candidates, not authenticated
source bounds. No Lean/Lake run or registry admission accompanies this file.
-/
set_option autoImplicit false

namespace RouteBP4032GrowthEnvelopeBinding

open RouteBP4032SameSourceConsumerPacket RouteBP4032BlockDefects
open RouteBP4032DescriptorPUpper
open scoped BigOperators

noncomputable section

def growthMu : ℚ := 9401 / 1000000
def growthR : ℚ := 73439445001755279 / 320000000000000
def growthH : ℚ := 6 * growthR ^ 2
def growthK : ℚ := (1402217 / 12000000) * growthH / growthMu ^ 2

/-- Six component inequalities imply the Euclidean squared-force envelope.
The input is the full descriptor RHS, not the two-channel port residual. -/
theorem component_to_full (rhs : Vec6) (R : ℝ)
    (hR : ∀ j, rhs j ^ 2 ≤ R ^ 2) : fullSq rhs ≤ 6 * R ^ 2 := by
  calc
    fullSq rhs ≤ ∑ _j : Fin 6, R ^ 2 := by
      exact Finset.sum_le_sum (fun j _ => hR j)
    _ = 6 * R ^ 2 := by simp

theorem growth_scalar_certificate :
    metricMax * (growthH : ℝ) = (growthMu : ℝ)^2 * (growthK : ℝ) := by
  norm_num [metricMax, growthH, growthK, growthMu, growthR]

/-- To instantiate this result, prove all hypotheses for one and the same
mass/controller/C/G/disturbance source and state. In particular the growth
CSV does not supply hR on the target cell merely by existing on disk. -/
theorem source_metric_cap {key : SourceKey} {X : Type*}
    (src : SourceFields key X) (x : X) (M : Mat6) (a rhs : Vec6)
    (h4 : src.acceleration x 0 = a 3) (h5 : src.acceleration x 1 = a 4)
    (hcoercive : (growthMu : ℝ) * fullSq a ≤ dot6 a (M *ᵥ a))
    (heq : M *ᵥ a = rhs)
    (hR : ∀ j, rhs j ^ 2 ≤ (growthR : ℝ)^2) :
    metric src x ≤ (growthK : ℝ) := by
  apply descriptor_metric_cap src x M a rhs (growthMu : ℝ)
    (growthH : ℝ) (growthK : ℝ)
  · norm_num [growthMu]
  · exact h4
  · exact h5
  · exact hcoercive
  · exact heq
  · have h := component_to_full rhs (growthR : ℝ) hR
    simpa [growthH] using h
  · exact le_of_eq growth_scalar_certificate

end
end RouteBP4032GrowthEnvelopeBinding

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P5 signed-sum interval transport companion

Complementary source-independent Lean adapter for
`agent_review_inbox/review-T-P5-045-liuguanyi-20260907T2108.md`.

苏梦辰 concurrently owns the main determinant/bias/gate formalization in
`examples/routeb_p5_robust_correlated_interval_lean/`.  This file therefore
intentionally does not duplicate those theorems.  It freezes only the missing
entrywise signed-interval seam: add the signed `k45`/`k54` intervals first,
then derive the pointwise interval and absolute cap for
`sigma = k45 + k54`.  It also freezes the exact skew cancellation boundary.
-/

set_option autoImplicit false

namespace RouteBP5SignedSumIntervalTransport

noncomputable section

/-- Entrywise signed intervals plus endpoint bounds on their sum transport to
one pointwise interval for `sigma = k45 + k54`.  No absolute value is taken
before the signed addition. -/
theorem signed_sum_interval_transport
    (k45 k54 k45L k45U k54L k54U Q : ℝ)
    (h45L : k45L ≤ k45) (h45U : k45 ≤ k45U)
    (h54L : k54L ≤ k54) (h54U : k54 ≤ k54U)
    (hQL : -Q ≤ k45L + k54L)
    (hQU : k45U + k54U ≤ Q) :
    -Q ≤ k45 + k54 ∧ k45 + k54 ≤ Q := by
  constructor <;> linarith

/-- The signed interval transport feeds exactly the absolute-value premise
`|sigma| <= Q` consumed by the correlated determinant/bias sidecar. -/
theorem signed_sum_abs_transport
    (k45 k54 k45L k45U k54L k54U Q : ℝ)
    (h45L : k45L ≤ k45) (h45U : k45 ≤ k45U)
    (h54L : k54L ≤ k54) (h54U : k54 ≤ k54U)
    (hQL : -Q ≤ k45L + k54L)
    (hQU : k45U + k54U ≤ Q) :
    |k45 + k54| ≤ Q := by
  exact abs_le.mpr
    (signed_sum_interval_transport
      k45 k54 k45L k45U k54L k54U Q
      h45L h45U h54L h54U hQL hQU)

/-- Exact skew family from T-P5-045: the energy-visible symmetric cross
coordinate vanishes before any absolute scalarization. -/
theorem skew_family_signed_sum_zero (M : ℝ) :
    M + (-M) = 0 := by
  ring

/-- Consequently the correctly formed absolute cap of the skew family is zero. -/
theorem skew_family_signed_sum_abs_zero (M : ℝ) :
    |M + (-M)| = 0 := by
  simp

#print axioms signed_sum_interval_transport
#print axioms signed_sum_abs_transport
#print axioms skew_family_signed_sum_zero
#print axioms skew_family_signed_sum_abs_zero

end

end RouteBP5SignedSumIntervalTransport

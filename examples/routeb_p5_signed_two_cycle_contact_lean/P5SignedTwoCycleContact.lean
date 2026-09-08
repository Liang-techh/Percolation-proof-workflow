import Mathlib

noncomputable section

namespace RouteBP5SignedTwoCycleContact

/-- Scalar composition appearing after eliminating the second contact coordinate. -/
def cyclePhi (outer inner : ℝ → ℝ) (eta x : ℝ) : ℝ :=
  outer (eta + inner x)

/-- One-dimensional cyclic inverse map `Id - Phi`. -/
def cycleG (outer inner : ℝ → ℝ) (eta x : ℝ) : ℝ :=
  x - cyclePhi outer inner eta x

/-- Increasing outer root graph composed with a decreasing inner graph is antitone. -/
theorem cyclePhi_antitone_of_monotone_antitone
    (outer inner : ℝ → ℝ)
    (hOuter : Monotone outer)
    (hInner : Antitone inner)
    (eta : ℝ) :
    Antitone (cyclePhi outer inner eta) := by
  intro s t hst
  apply hOuter
  exact add_le_add_left (hInner hst) eta

/-- Decreasing outer root graph composed with an increasing inner graph is antitone. -/
theorem cyclePhi_antitone_of_antitone_monotone
    (outer inner : ℝ → ℝ)
    (hOuter : Antitone outer)
    (hInner : Monotone inner)
    (eta : ℝ) :
    Antitone (cyclePhi outer inner eta) := by
  intro s t hst
  apply hOuter
  exact add_le_add_left (hInner hst) eta

/-- `Id - Phi` is strongly monotone whenever `Phi` is antitone. -/
theorem sub_antitone_strongMono_one
    (Phi : ℝ → ℝ)
    (hanti : Antitone Phi) :
    StrongMono (fun x => x - Phi x) := by
  intro s t hst
  have hPhi : Phi t ≤ Phi s := hanti (le_of_lt hst)
  linarith

/-- Exact unit absolute coercivity of `Id - Phi`. -/
theorem sub_antitone_abs_coercive_one
    (Phi : ℝ → ℝ)
    (hanti : Antitone Phi)
    (s t : ℝ) :
    |t - s| ≤ |(t - Phi t) - (s - Phi s)| := by
  rcases le_total s t with hst | hts
  · have hPhi : Phi t ≤ Phi s := hanti hst
    have hBase : 0 ≤ t - s := sub_nonneg.mpr hst
    have hFull : 0 ≤ (t - Phi t) - (s - Phi s) := by
      linarith
    rw [abs_of_nonneg hBase, abs_of_nonneg hFull]
    linarith
  · have hPhi : Phi s ≤ Phi t := hanti hts
    have hBase : t - s ≤ 0 := sub_nonpos.mpr hts
    have hFull : (t - Phi t) - (s - Phi s) ≤ 0 := by
      linarith
    rw [abs_of_nonpos hBase, abs_of_nonpos hFull]
    linarith

/-- Antitone feedback gives injectivity with no small-gain assumption. -/
theorem sub_antitone_injective
    (Phi : ℝ → ℝ)
    (hanti : Antitone Phi) :
    Function.Injective (fun x => x - Phi x) :=
  (sub_antitone_strongMono_one Phi hanti).injective

/--
A generic inverse perturbation lemma: unit coercivity plus a pointwise change in
`G` transports directly to an inverse-coordinate bound.
-/
theorem coercive_inverse_perturbation
    (G G' : ℝ → ℝ)
    (x x' xi xi' E : ℝ)
    (hcoer : ∀ s t, |t - s| ≤ |G t - G s|)
    (hx : G x = xi)
    (hx' : G' x' = xi')
    (hpert : |G x' - G' x'| ≤ E) :
    |x - x'| ≤ |xi - xi'| + E := by
  have hCoer := hcoer x' x
  have hAdd := abs_add_le (G x - G' x') (G' x' - G x')
  have hDecomp :
      (G x - G' x') + (G' x' - G x') = G x - G x' := by
    ring
  rw [hDecomp] at hAdd
  have hTri :
      |G x - G x'| ≤ |xi - xi'| + |G' x' - G x'| := by
    simpa [hx, hx'] using hAdd
  have hPert' : |G' x' - G x'| ≤ E := by
    simpa [abs_sub_comm] using hpert
  exact hCoer.trans (hTri.trans (add_le_add_left hPert' _))

/--
One-coordinate negative-feedback inverse estimate.  The outer Lipschitz charge
appears, but there is no denominator and no product-smallness hypothesis.
-/
theorem negative_feedback_coordinate_bound
    (outer inner : ℝ → ℝ)
    (a x x' eta eta' xi xi' : ℝ)
    (hanti : ∀ e, Antitone (cyclePhi outer inner e))
    (hLipOuter : ∀ u v, |outer u - outer v| ≤ a * |u - v|)
    (hx : cycleG outer inner eta x = xi)
    (hx' : cycleG outer inner eta' x' = xi') :
    |x - x'| ≤ |xi - xi'| + a * |eta - eta'| := by
  have hCoer : ∀ s t, |t - s| ≤
      |cycleG outer inner eta t - cycleG outer inner eta s| := by
    intro s t
    simpa [cycleG] using
      sub_antitone_abs_coercive_one (cyclePhi outer inner eta) (hanti eta) s t
  have hLip := hLipOuter (eta + inner x') (eta' + inner x')
  have hArg :
      (eta + inner x') - (eta' + inner x') = eta - eta' := by
    ring
  rw [hArg] at hLip
  have hPert :
      |cycleG outer inner eta x' - cycleG outer inner eta' x'| ≤
        a * |eta - eta'| := by
    have hEq :
        cycleG outer inner eta x' - cycleG outer inner eta' x' =
          outer (eta' + inner x') - outer (eta + inner x') := by
      simp [cycleG, cyclePhi]
      ring
    rw [hEq]
    simpa [abs_sub_comm] using hLip
  exact coercive_inverse_perturbation
    (cycleG outer inner eta) (cycleG outer inner eta')
    x x' xi xi' (a * |eta - eta'|) hCoer hx hx' hPert

/--
Fixed-base two-cycle inverse budget for the orientation
`rho1` monotone / `rho2` antitone.
-/
theorem two_cycle_negative_feedback_inverse_bound_monotone_antitone
    (rho1 rho2 : ℝ → ℝ)
    (a b : ℝ)
    (hMono1 : Monotone rho1)
    (hAnti2 : Antitone rho2)
    (hLip1 : ∀ u v, |rho1 u - rho1 v| ≤ a * |u - v|)
    (hLip2 : ∀ u v, |rho2 u - rho2 v| ≤ b * |u - v|)
    (x1 x2 x1' x2' xi1 xi2 xi1' xi2' : ℝ)
    (h11 : x1 - rho1 x2 = xi1)
    (h12 : x2 - rho2 x1 = xi2)
    (h21 : x1' - rho1 x2' = xi1')
    (h22 : x2' - rho2 x1' = xi2') :
    |x1 - x1'| ≤ |xi1 - xi1'| + a * |xi2 - xi2'| ∧
      |x2 - x2'| ≤ |xi2 - xi2'| + b * |xi1 - xi1'| := by
  have hComp1 : ∀ e, Antitone (cyclePhi rho1 rho2 e) := by
    intro e
    exact cyclePhi_antitone_of_monotone_antitone rho1 rho2 hMono1 hAnti2 e
  have hComp2 : ∀ e, Antitone (cyclePhi rho2 rho1 e) := by
    intro e
    exact cyclePhi_antitone_of_antitone_monotone rho2 rho1 hAnti2 hMono1 e
  have hx2 : x2 = xi2 + rho2 x1 := by
    linarith
  have hx2' : x2' = xi2' + rho2 x1' := by
    linarith
  have hx1 : x1 = xi1 + rho1 x2 := by
    linarith
  have hx1' : x1' = xi1' + rho1 x2' := by
    linarith
  have hG1 : cycleG rho1 rho2 xi2 x1 = xi1 := by
    rw [cycleG, cyclePhi, ← hx2]
    exact h11
  have hG1' : cycleG rho1 rho2 xi2' x1' = xi1' := by
    rw [cycleG, cyclePhi, ← hx2']
    exact h21
  have hG2 : cycleG rho2 rho1 xi1 x2 = xi2 := by
    rw [cycleG, cyclePhi, ← hx1]
    exact h12
  have hG2' : cycleG rho2 rho1 xi1' x2' = xi2' := by
    rw [cycleG, cyclePhi, ← hx1']
    exact h22
  constructor
  · exact negative_feedback_coordinate_bound
      rho1 rho2 a x1 x1' xi2 xi2' xi1 xi1'
      hComp1 hLip1 hG1 hG1'
  · exact negative_feedback_coordinate_bound
      rho2 rho1 b x2 x2' xi1 xi1' xi2 xi2'
      hComp2 hLip2 hG2 hG2'

/-- Symmetric fixed-base inverse budget for `rho1` antitone / `rho2` monotone. -/
theorem two_cycle_negative_feedback_inverse_bound_antitone_monotone
    (rho1 rho2 : ℝ → ℝ)
    (a b : ℝ)
    (hAnti1 : Antitone rho1)
    (hMono2 : Monotone rho2)
    (hLip1 : ∀ u v, |rho1 u - rho1 v| ≤ a * |u - v|)
    (hLip2 : ∀ u v, |rho2 u - rho2 v| ≤ b * |u - v|)
    (x1 x2 x1' x2' xi1 xi2 xi1' xi2' : ℝ)
    (h11 : x1 - rho1 x2 = xi1)
    (h12 : x2 - rho2 x1 = xi2)
    (h21 : x1' - rho1 x2' = xi1')
    (h22 : x2' - rho2 x1' = xi2') :
    |x1 - x1'| ≤ |xi1 - xi1'| + a * |xi2 - xi2'| ∧
      |x2 - x2'| ≤ |xi2 - xi2'| + b * |xi1 - xi1'| := by
  have hComp1 : ∀ e, Antitone (cyclePhi rho1 rho2 e) := by
    intro e
    exact cyclePhi_antitone_of_antitone_monotone rho1 rho2 hAnti1 hMono2 e
  have hComp2 : ∀ e, Antitone (cyclePhi rho2 rho1 e) := by
    intro e
    exact cyclePhi_antitone_of_monotone_antitone rho2 rho1 hMono2 hAnti1 e
  have hx2 : x2 = xi2 + rho2 x1 := by
    linarith
  have hx2' : x2' = xi2' + rho2 x1' := by
    linarith
  have hx1 : x1 = xi1 + rho1 x2 := by
    linarith
  have hx1' : x1' = xi1' + rho1 x2' := by
    linarith
  have hG1 : cycleG rho1 rho2 xi2 x1 = xi1 := by
    rw [cycleG, cyclePhi, ← hx2]
    exact h11
  have hG1' : cycleG rho1 rho2 xi2' x1' = xi1' := by
    rw [cycleG, cyclePhi, ← hx2']
    exact h21
  have hG2 : cycleG rho2 rho1 xi1 x2 = xi2 := by
    rw [cycleG, cyclePhi, ← hx1]
    exact h12
  have hG2' : cycleG rho2 rho1 xi1' x2' = xi2' := by
    rw [cycleG, cyclePhi, ← hx1']
    exact h22
  constructor
  · exact negative_feedback_coordinate_bound
      rho1 rho2 a x1 x1' xi2 xi2' xi1 xi1'
      hComp1 hLip1 hG1 hG1'
  · exact negative_feedback_coordinate_bound
      rho2 rho1 b x2 x2' xi1 xi1' xi2 xi2'
      hComp2 hLip2 hG2 hG2'

/--
Pure division-free elimination for the unsigned source-cleared two-cycle.
Strict reserve is not needed to derive the inequalities themselves.
-/
theorem two_cycle_small_gain_cleared
    (mu1 mu2 C12 C21 L1 L2 X1 X2 Z1 Z2 D : ℝ)
    (hmu1 : 0 ≤ mu1)
    (hmu2 : 0 ≤ mu2)
    (hC12 : 0 ≤ C12)
    (hC21 : 0 ≤ C21)
    (h1 : mu1 * X1 ≤ mu1 * Z1 + C12 * X2 + L1 * D)
    (h2 : mu2 * X2 ≤ mu2 * Z2 + C21 * X1 + L2 * D) :
    (mu1 * mu2 - C12 * C21) * X1 ≤
        mu1 * mu2 * Z1 + C12 * mu2 * Z2 + (mu2 * L1 + C12 * L2) * D ∧
      (mu1 * mu2 - C12 * C21) * X2 ≤
        C21 * mu1 * Z1 + mu1 * mu2 * Z2 + (C21 * L1 + mu1 * L2) * D := by
  have h1m := mul_le_mul_of_nonneg_left h1 hmu2
  have h2c := mul_le_mul_of_nonneg_left h2 hC12
  have h2m := mul_le_mul_of_nonneg_left h2 hmu1
  have h1c := mul_le_mul_of_nonneg_left h1 hC21
  constructor <;> nlinarith

/-- The strict unsigned small-gain gate is exactly positivity of the cleared reserve. -/
theorem two_cycle_small_gain_cleared_with_reserve
    (mu1 mu2 C12 C21 L1 L2 X1 X2 Z1 Z2 D : ℝ)
    (hmu1 : 0 ≤ mu1)
    (hmu2 : 0 ≤ mu2)
    (hC12 : 0 ≤ C12)
    (hC21 : 0 ≤ C21)
    (h1 : mu1 * X1 ≤ mu1 * Z1 + C12 * X2 + L1 * D)
    (h2 : mu2 * X2 ≤ mu2 * Z2 + C21 * X1 + L2 * D)
    (hDelta : C12 * C21 < mu1 * mu2) :
    0 < mu1 * mu2 - C12 * C21 ∧
      ((mu1 * mu2 - C12 * C21) * X1 ≤
          mu1 * mu2 * Z1 + C12 * mu2 * Z2 + (mu2 * L1 + C12 * L2) * D ∧
        (mu1 * mu2 - C12 * C21) * X2 ≤
          C21 * mu1 * Z1 + mu1 * mu2 * Z2 + (C21 * L1 + mu1 * L2) * D) := by
  constructor
  · linarith
  · exact two_cycle_small_gain_cleared
      mu1 mu2 C12 C21 L1 L2 X1 X2 Z1 Z2 D
      hmu1 hmu2 hC12 hC21 h1 h2

/-- Cross-up signed source motion forces the root graph in the opposite direction. -/
theorem root_antitone_of_active_increasing_cross_up
    (oldFiber newFiber : ℝ → ℝ)
    (rOld rNew : ℝ)
    (hOldRoot : oldFiber rOld = 0)
    (hNewRoot : newFiber rNew = 0)
    (hNewStrict : StrictMono newFiber)
    (hCrossUp : ∀ s, oldFiber s ≤ newFiber s) :
    rNew ≤ rOld := by
  by_contra hnot
  have hlt : rOld < rNew := lt_of_not_ge hnot
  have hStrict := hNewStrict hlt
  have hCross := hCrossUp rOld
  rw [hNewRoot] at hStrict
  rw [hOldRoot] at hCross
  linarith

/-- Cross-down signed source motion forces the root graph to move upward. -/
theorem root_monotone_of_active_increasing_cross_down
    (oldFiber newFiber : ℝ → ℝ)
    (rOld rNew : ℝ)
    (hOldRoot : oldFiber rOld = 0)
    (hNewRoot : newFiber rNew = 0)
    (hOldStrict : StrictMono oldFiber)
    (hCrossDown : ∀ s, newFiber s ≤ oldFiber s) :
    rOld ≤ rNew := by
  by_contra hnot
  have hlt : rNew < rOld := lt_of_not_ge hnot
  have hStrict := hOldStrict hlt
  have hCross := hCrossDown rNew
  rw [hOldRoot] at hStrict
  rw [hNewRoot] at hCross
  linarith

/-- At the unsigned boundary `a*b=1`, the identity two-cycle is noninjective. -/
theorem identity_two_cycle_boundary_nonunique :
    ∃ x1 x2 x1' x2' : ℝ,
      x1 ≠ x1' ∧
      x1 - x2 = x1' - x2' ∧
      x2 - x1 = x2' - x1' := by
  refine ⟨0, 0, 1, 1, ?_, ?_, ?_⟩ <;> norm_num

/-- The `99/100` positive-feedback example attains both cleared inverse bounds exactly. -/
theorem small_gain_near_boundary_sharp_99_100 :
    ((1 : ℝ) - 1 * (99 / 100 : ℝ)) * 1 = (1 / 100 : ℝ) + 1 * 0 ∧
      ((1 : ℝ) - 1 * (99 / 100 : ℝ)) * (99 / 100 : ℝ) =
        (99 / 100 : ℝ) * (1 / 100 : ℝ) + 0 := by
  norm_num

#print axioms cyclePhi_antitone_of_monotone_antitone
#print axioms cyclePhi_antitone_of_antitone_monotone
#print axioms sub_antitone_strongMono_one
#print axioms sub_antitone_abs_coercive_one
#print axioms sub_antitone_injective
#print axioms coercive_inverse_perturbation
#print axioms negative_feedback_coordinate_bound
#print axioms two_cycle_negative_feedback_inverse_bound_monotone_antitone
#print axioms two_cycle_negative_feedback_inverse_bound_antitone_monotone
#print axioms two_cycle_small_gain_cleared
#print axioms two_cycle_small_gain_cleared_with_reserve
#print axioms root_antitone_of_active_increasing_cross_up
#print axioms root_monotone_of_active_increasing_cross_down
#print axioms identity_two_cycle_boundary_nonunique
#print axioms small_gain_near_boundary_sharp_99_100

end RouteBP5SignedTwoCycleContact

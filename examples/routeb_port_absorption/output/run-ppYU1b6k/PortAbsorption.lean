import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

/-!
Finite-dimensional real Euclidean port absorption, with explicit hypotheses.
`sqNorm` is the sum of coordinate squares, NOT the default Pi sup norm.
`rhoSq` denotes the source's squared-radius parameter rho^2 (not its square root).
No source/model identification, interval enclosure, or SOS feasibility is assumed
as an axiom. The port enclosure and Phi nonnegativity remain theorem premises.
-/

open scoped BigOperators

namespace RouteBPortAbsorption

noncomputable section

variable {ι : Type*} [Fintype ι]

def sqNorm (v : ι → ℝ) : ℝ := ∑ i, (v i)^2

def dot (h r : ι → ℝ) : ℝ := ∑ i, h i * r i

def full (Dbase sRes : ℝ) (h r : ι → ℝ) : ℝ :=
  Dbase + sRes * sqNorm r + dot h r

def phi (Dbase sRes nu rhoSq AB : ℝ) (h : ι → ℝ) : ℝ :=
  Dbase - nu * rhoSq * AB - sqNorm h / (4 * (sRes + nu))

theorem sqNorm_nonneg (v : ι → ℝ) : 0 ≤ sqNorm v :=
  Finset.sum_nonneg (fun i _ => sq_nonneg (v i))

/-- Exact completion; positivity is needed for the lower bound, not this identity. -/
theorem quadratic_completion (a : ℝ) (ha : a ≠ 0) (h r : ι → ℝ) :
    a * sqNorm r + dot h r =
      -sqNorm h / (4 * a) + a * sqNorm (fun i => r i + h i / (2 * a)) := by
  have coordinate (x y : ℝ) :
      a * x^2 + y * x = -y^2 / (4 * a) + a * (x + y / (2 * a))^2 := by
    field_simp
    <;> nlinarith [ha]
  calc
    a * sqNorm r + dot h r = ∑ i, (a * (r i)^2 + h i * r i) := by
      simp only [sqNorm, dot, Finset.mul_sum, Finset.sum_add_distrib]
    _ = ∑ i, (-(h i)^2 / (4 * a) + a * (r i + h i / (2 * a))^2) := by
      apply Finset.sum_congr rfl
      intro i _
      exact coordinate (r i) (h i)
    _ = _ := by
      simp only [sqNorm, Finset.sum_add_distrib, div_eq_mul_inv, Finset.sum_mul,
        Finset.sum_neg_distrib, Finset.mul_sum]

theorem quadratic_lower_bound (a : ℝ) (ha : 0 < a) (h r : ι → ℝ) :
    -sqNorm h / (4 * a) ≤ a * sqNorm r + dot h r := by
  rw [quadratic_completion a (ne_of_gt ha)]
  exact le_add_of_nonneg_right (mul_nonneg ha.le (sqNorm_nonneg _))

/-- The bound is attained at -h/(2a), so its constant and scaling are sharp. -/
theorem quadratic_minimizer (a : ℝ) (ha : a ≠ 0) (h : ι → ℝ) :
    a * sqNorm (fun i => -(h i / (2 * a))) +
      dot h (fun i => -(h i / (2 * a))) = -sqNorm h / (4 * a) := by
  rw [quadratic_completion a ha]
  simp [sqNorm]

/-- Exact S-procedure slack, with the positive port slack on the RHS. -/
theorem port_completion (Dbase sRes nu rhoSq AB : ℝ) (h r : ι → ℝ)
    (ha : sRes + nu ≠ 0) :
    full Dbase sRes h r = phi Dbase sRes nu rhoSq AB h +
      (sRes + nu) * sqNorm (fun i => r i + h i / (2 * (sRes + nu))) +
      nu * (rhoSq * AB - sqNorm r) := by
  have hc := quadratic_completion (sRes + nu) ha h r
  rw [neg_div] at hc
  dsimp [full, phi]
  nlinarith [hc]

/-- Sharp for the unconstrained fixed-nu augmented quadratic. This is not
an equivalence between constrained positivity and existence of a multiplier. -/
theorem fixed_nu_certificate_iff (Dbase sRes nu rhoSq AB : ℝ) (h : ι → ℝ)
    (ha : 0 < sRes + nu) :
    0 ≤ phi Dbase sRes nu rhoSq AB h ↔
      ∀ r : ι → ℝ, 0 ≤ full Dbase sRes h r - nu * (rhoSq * AB - sqNorm r) := by
  constructor
  · intro hphi r
    rw [port_completion Dbase sRes nu rhoSq AB h r (ne_of_gt ha)]
    have hs := mul_nonneg ha.le
      (sqNorm_nonneg (fun i => r i + h i / (2 * (sRes + nu))))
    linarith
  · intro hpos
    specialize hpos (fun i => -(h i / (2 * (sRes + nu))))
    rw [port_completion Dbase sRes nu rhoSq AB h _ (ne_of_gt ha)] at hpos
    simpa [sqNorm] using hpos

/-- Conditional absorption, with a quantitative Phi lower bound. No separate
sign assumptions on sRes, rhoSq, or AB are needed for this implication. -/
theorem conditional_absorption_bound (Dbase sRes nu rhoSq AB : ℝ) (h r : ι → ℝ)
    (hnu : 0 ≤ nu) (ha : 0 < sRes + nu)
    (hport : sqNorm r ≤ rhoSq * AB) :
    phi Dbase sRes nu rhoSq AB h ≤ full Dbase sRes h r := by
  rw [port_completion Dbase sRes nu rhoSq AB h r (ne_of_gt ha)]
  have hs := mul_nonneg ha.le
    (sqNorm_nonneg (fun i => r i + h i / (2 * (sRes + nu))))
  have hp := mul_nonneg hnu (sub_nonneg.mpr hport)
  linarith

/-- The requested finite-vector fixed-nu port implication. -/
theorem conditional_absorption (Dbase sRes nu rhoSq AB : ℝ) (h r : ι → ℝ)
    (hnu : 0 ≤ nu) (ha : 0 < sRes + nu)
    (hport : sqNorm r ≤ rhoSq * AB)
    (hphi : 0 ≤ phi Dbase sRes nu rhoSq AB h) :
    0 ≤ full Dbase sRes h r :=
  hphi.trans (conditional_absorption_bound Dbase sRes nu rhoSq AB h r hnu ha hport)

/-- Source scaling nu=1, sRes=5, hence denominator 24. Still conditional. -/
theorem conditional_absorption_nu1_sres5 (Dbase rhoSq AB : ℝ) (h r : ι → ℝ)
    (hport : sqNorm r ≤ rhoSq * AB)
    (hphi : 0 ≤ Dbase - rhoSq * AB - sqNorm h / 24) :
    0 ≤ Dbase + 5 * sqNorm r + dot h r := by
  apply conditional_absorption Dbase 5 1 rhoSq AB h r (by norm_num) (by norm_num) hport
  norm_num [phi] at ⊢
  exact hphi

end

#print axioms sqNorm_nonneg
#print axioms quadratic_completion
#print axioms quadratic_lower_bound
#print axioms quadratic_minimizer
#print axioms port_completion
#print axioms fixed_nu_certificate_iff
#print axioms conditional_absorption_bound
#print axioms conditional_absorption
#print axioms conditional_absorption_nu1_sres5

end RouteBPortAbsorption

import Mathlib

noncomputable section

namespace RouteBP5BernsteinCell

/-- Degree-2 polynomial in monomial coordinates. -/
def quadPoly (a0 a1 a2 t : ℝ) : ℝ :=
  a0 + a1 * t + a2 * t ^ 2

/-- Degree-3 polynomial in monomial coordinates. -/
def cubicPoly (c0 c1 c2 c3 t : ℝ) : ℝ :=
  c0 + c1 * t + c2 * t ^ 2 + c3 * t ^ 3

/-- Degree-2 Bernstein form on `[0,1]`. -/
def quadBern (b0 b1 b2 t : ℝ) : ℝ :=
  b0 * (1 - t) ^ 2 + 2 * b1 * t * (1 - t) + b2 * t ^ 2

/-- Degree-3 Bernstein form on `[0,1]`. -/
def cubicBern (g0 g1 g2 g3 t : ℝ) : ℝ :=
  g0 * (1 - t) ^ 3
    + 3 * g1 * t * (1 - t) ^ 2
    + 3 * g2 * t ^ 2 * (1 - t)
    + g3 * t ^ 3

/-- Exact degree-2 monomial-to-Bernstein conversion. -/
theorem quad_bernstein_identity
    (a0 a1 a2 t : ℝ) :
    quadPoly a0 a1 a2 t =
      quadBern a0 (a0 + a1 / 2) (a0 + a1 + a2) t := by
  dsimp [quadPoly, quadBern]
  ring

/-- Exact degree-3 monomial-to-Bernstein conversion. -/
theorem cubic_bernstein_identity
    (c0 c1 c2 c3 t : ℝ) :
    cubicPoly c0 c1 c2 c3 t =
      cubicBern
        c0
        (c0 + c1 / 3)
        (c0 + 2 * c1 / 3 + c2 / 3)
        (c0 + c1 + c2 + c3)
        t := by
  dsimp [cubicPoly, cubicBern]
  ring

/-- The three quadratic Bernstein weights sum to one. -/
theorem quad_bernstein_weights_sum (t : ℝ) :
    (1 - t) ^ 2 + 2 * t * (1 - t) + t ^ 2 = 1 := by
  ring

/-- The four cubic Bernstein weights sum to one. -/
theorem cubic_bernstein_weights_sum (t : ℝ) :
    (1 - t) ^ 3
      + 3 * t * (1 - t) ^ 2
      + 3 * t ^ 2 * (1 - t)
      + t ^ 3 = 1 := by
  ring

/-- Nonnegative degree-2 Bernstein controls certify the whole cell. -/
theorem quadBern_nonneg_of_controls
    (b0 b1 b2 t : ℝ)
    (hb0 : 0 ≤ b0) (hb1 : 0 ≤ b1) (hb2 : 0 ≤ b2)
    (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    0 ≤ quadBern b0 b1 b2 t := by
  have h1t : 0 ≤ 1 - t := by
    linarith
  have hterm0 : 0 ≤ b0 * (1 - t) ^ 2 :=
    mul_nonneg hb0 (sq_nonneg (1 - t))
  have hterm1 : 0 ≤ 2 * b1 * t * (1 - t) :=
    mul_nonneg
      (mul_nonneg (mul_nonneg (by norm_num) hb1) ht0)
      h1t
  have hterm2 : 0 ≤ b2 * t ^ 2 :=
    mul_nonneg hb2 (sq_nonneg t)
  dsimp [quadBern]
  exact add_nonneg (add_nonneg hterm0 hterm1) hterm2

/-- Nonnegative degree-3 Bernstein controls certify the whole cell. -/
theorem cubicBern_nonneg_of_controls
    (g0 g1 g2 g3 t : ℝ)
    (hg0 : 0 ≤ g0) (hg1 : 0 ≤ g1) (hg2 : 0 ≤ g2) (hg3 : 0 ≤ g3)
    (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    0 ≤ cubicBern g0 g1 g2 g3 t := by
  have h1t : 0 ≤ 1 - t := by
    linarith
  have hterm0 : 0 ≤ g0 * (1 - t) ^ 3 :=
    mul_nonneg hg0 (pow_nonneg h1t 3)
  have hterm1 : 0 ≤ 3 * g1 * t * (1 - t) ^ 2 :=
    mul_nonneg
      (mul_nonneg (mul_nonneg (by norm_num) hg1) ht0)
      (sq_nonneg (1 - t))
  have hterm2 : 0 ≤ 3 * g2 * t ^ 2 * (1 - t) :=
    mul_nonneg
      (mul_nonneg (mul_nonneg (by norm_num) hg2) (sq_nonneg t))
      h1t
  have hterm3 : 0 ≤ g3 * t ^ 3 :=
    mul_nonneg hg3 (pow_nonneg ht0 3)
  dsimp [cubicBern]
  exact add_nonneg (add_nonneg (add_nonneg hterm0 hterm1) hterm2) hterm3

/-- Monomial quadratic coefficients can be consumed directly through their exact controls. -/
theorem quadPoly_nonneg_of_controls
    (a0 a1 a2 t : ℝ)
    (h0 : 0 ≤ a0)
    (h1 : 0 ≤ a0 + a1 / 2)
    (h2 : 0 ≤ a0 + a1 + a2)
    (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    0 ≤ quadPoly a0 a1 a2 t := by
  rw [quad_bernstein_identity]
  exact quadBern_nonneg_of_controls
    a0 (a0 + a1 / 2) (a0 + a1 + a2) t h0 h1 h2 ht0 ht1

/-- Monomial cubic coefficients can be consumed directly through their exact controls. -/
theorem cubicPoly_nonneg_of_controls
    (c0 c1 c2 c3 t : ℝ)
    (h0 : 0 ≤ c0)
    (h1 : 0 ≤ c0 + c1 / 3)
    (h2 : 0 ≤ c0 + 2 * c1 / 3 + c2 / 3)
    (h3 : 0 ≤ c0 + c1 + c2 + c3)
    (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    0 ≤ cubicPoly c0 c1 c2 c3 t := by
  rw [cubic_bernstein_identity]
  exact cubicBern_nonneg_of_controls
    c0
    (c0 + c1 / 3)
    (c0 + 2 * c1 / 3 + c2 / 3)
    (c0 + c1 + c2 + c3)
    t h0 h1 h2 h3 ht0 ht1

/-- Exact quadratic de Casteljau identity for the left dyadic half. -/
theorem quad_decasteljau_left_half
    (b0 b1 b2 u : ℝ) :
    quadBern b0 b1 b2 (u / 2) =
      quadBern
        b0
        ((b0 + b1) / 2)
        ((b0 + 2 * b1 + b2) / 4)
        u := by
  dsimp [quadBern]
  ring

/-- Exact quadratic de Casteljau identity for the right dyadic half. -/
theorem quad_decasteljau_right_half
    (b0 b1 b2 u : ℝ) :
    quadBern b0 b1 b2 ((1 + u) / 2) =
      quadBern
        ((b0 + 2 * b1 + b2) / 4)
        ((b1 + b2) / 2)
        b2
        u := by
  dsimp [quadBern]
  ring

/-- Exact cubic de Casteljau identity for the left dyadic half. -/
theorem cubic_decasteljau_left_half
    (g0 g1 g2 g3 u : ℝ) :
    cubicBern g0 g1 g2 g3 (u / 2) =
      cubicBern
        g0
        ((g0 + g1) / 2)
        ((g0 + 2 * g1 + g2) / 4)
        ((g0 + 3 * g1 + 3 * g2 + g3) / 8)
        u := by
  dsimp [cubicBern]
  ring

/-- Exact cubic de Casteljau identity for the right dyadic half. -/
theorem cubic_decasteljau_right_half
    (g0 g1 g2 g3 u : ℝ) :
    cubicBern g0 g1 g2 g3 ((1 + u) / 2) =
      cubicBern
        ((g0 + 3 * g1 + 3 * g2 + g3) / 8)
        ((g1 + 2 * g2 + g3) / 4)
        ((g2 + g3) / 2)
        g3
        u := by
  dsimp [cubicBern]
  ring

/-- Nonnegative quadratic controls remain nonnegative after left-half subdivision. -/
theorem quad_left_controls_nonneg
    (b0 b1 b2 : ℝ)
    (h0 : 0 ≤ b0) (h1 : 0 ≤ b1) (h2 : 0 ≤ b2) :
    0 ≤ b0 ∧
      0 ≤ (b0 + b1) / 2 ∧
      0 ≤ (b0 + 2 * b1 + b2) / 4 := by
  constructor
  · exact h0
  constructor
  · nlinarith
  · nlinarith

/-- Nonnegative quadratic controls remain nonnegative after right-half subdivision. -/
theorem quad_right_controls_nonneg
    (b0 b1 b2 : ℝ)
    (h0 : 0 ≤ b0) (h1 : 0 ≤ b1) (h2 : 0 ≤ b2) :
    0 ≤ (b0 + 2 * b1 + b2) / 4 ∧
      0 ≤ (b1 + b2) / 2 ∧
      0 ≤ b2 := by
  constructor
  · nlinarith
  constructor
  · nlinarith
  · exact h2

/-- Nonnegative cubic controls remain nonnegative after left-half subdivision. -/
theorem cubic_left_controls_nonneg
    (g0 g1 g2 g3 : ℝ)
    (h0 : 0 ≤ g0) (h1 : 0 ≤ g1) (h2 : 0 ≤ g2) (h3 : 0 ≤ g3) :
    0 ≤ g0 ∧
      0 ≤ (g0 + g1) / 2 ∧
      0 ≤ (g0 + 2 * g1 + g2) / 4 ∧
      0 ≤ (g0 + 3 * g1 + 3 * g2 + g3) / 8 := by
  constructor
  · exact h0
  constructor
  · nlinarith
  constructor
  · nlinarith
  · nlinarith

/-- Nonnegative cubic controls remain nonnegative after right-half subdivision. -/
theorem cubic_right_controls_nonneg
    (g0 g1 g2 g3 : ℝ)
    (h0 : 0 ≤ g0) (h1 : 0 ≤ g1) (h2 : 0 ≤ g2) (h3 : 0 ≤ g3) :
    0 ≤ (g0 + 3 * g1 + 3 * g2 + g3) / 8 ∧
      0 ≤ (g1 + 2 * g2 + g3) / 4 ∧
      0 ≤ (g2 + g3) / 2 ∧
      0 ≤ g3 := by
  constructor
  · nlinarith
  constructor
  · nlinarith
  constructor
  · nlinarith
  · exact h3

/-- Endpoint positivity alone is unsound for a correlated polynomial cell gate. -/
theorem endpoint_only_unsound_regression :
    quadPoly 1 (-5) 5 0 = 1 ∧
      quadPoly 1 (-5) 5 1 = 1 ∧
      quadPoly 1 (-5) 5 (1 / 2) = -(1 / 4 : ℝ) := by
  norm_num [quadPoly]

/-- A coarse negative Bernstein control need not mean that the polynomial is negative. -/
theorem negative_control_positive_polynomial_identity
    (t : ℝ) :
    quadPoly (7 / 20) (-1) 1 t = (t - 1 / 2) ^ 2 + 1 / 10 := by
  dsimp [quadPoly]
  ring

/-- The previous regression polynomial is uniformly positive despite its negative middle control. -/
theorem negative_control_positive_polynomial_lower_bound
    (t : ℝ) :
    (1 / 10 : ℝ) ≤ quadPoly (7 / 20) (-1) 1 t := by
  rw [negative_control_positive_polynomial_identity]
  nlinarith [sq_nonneg (t - 1 / 2)]

/-- Its middle quadratic Bernstein control is exactly negative. -/
theorem negative_control_positive_polynomial_middle_control :
    (7 / 20 : ℝ) + (-1 : ℝ) / 2 = -(3 / 20 : ℝ) := by
  norm_num

/--
Typed adapter: two certified cubic Bernstein packets can feed an already-proved
same-point two-remainder consumer.  This theorem deliberately does not reprove
the branch-free 2x2 completion; the caller supplies that established consumer.
-/
theorem cubic_packets_feed_two_remainder_consumer
    (P : Prop)
    (Rtr Rdet t : ℝ)
    (tr0 tr1 tr2 tr3 det0 det1 det2 det3 : ℝ)
    (ht0 : 0 ≤ t) (ht1 : t ≤ 1)
    (hRtr : Rtr = cubicBern tr0 tr1 tr2 tr3 t)
    (hRdet : Rdet = cubicBern det0 det1 det2 det3 t)
    (htr0 : 0 ≤ tr0) (htr1 : 0 ≤ tr1) (htr2 : 0 ≤ tr2) (htr3 : 0 ≤ tr3)
    (hdet0 : 0 ≤ det0) (hdet1 : 0 ≤ det1) (hdet2 : 0 ≤ det2) (hdet3 : 0 ≤ det3)
    (hconsumer : 0 ≤ Rtr → 0 ≤ Rdet → P) :
    P := by
  apply hconsumer
  · rw [hRtr]
    exact cubicBern_nonneg_of_controls tr0 tr1 tr2 tr3 t htr0 htr1 htr2 htr3 ht0 ht1
  · rw [hRdet]
    exact cubicBern_nonneg_of_controls det0 det1 det2 det3 t hdet0 hdet1 hdet2 hdet3 ht0 ht1

#print axioms quad_bernstein_identity
#print axioms cubic_bernstein_identity
#print axioms quad_bernstein_weights_sum
#print axioms cubic_bernstein_weights_sum
#print axioms quadBern_nonneg_of_controls
#print axioms cubicBern_nonneg_of_controls
#print axioms quadPoly_nonneg_of_controls
#print axioms cubicPoly_nonneg_of_controls
#print axioms quad_decasteljau_left_half
#print axioms quad_decasteljau_right_half
#print axioms cubic_decasteljau_left_half
#print axioms cubic_decasteljau_right_half
#print axioms quad_left_controls_nonneg
#print axioms quad_right_controls_nonneg
#print axioms cubic_left_controls_nonneg
#print axioms cubic_right_controls_nonneg
#print axioms endpoint_only_unsound_regression
#print axioms negative_control_positive_polynomial_identity
#print axioms negative_control_positive_polynomial_lower_bound
#print axioms negative_control_positive_polynomial_middle_control
#print axioms cubic_packets_feed_two_remainder_consumer

end RouteBP5BernsteinCell

import Mathlib

namespace RouteBP5SimilarityNormalization

/-- Symmetric 2x2 quadratic form with entries `a,b,c`, representing
`[[a,b],[b,c]]`. -/
def qform2 (a b c x y : ℝ) : ℝ :=
  a * x ^ 2 + 2 * b * x * y + c * y ^ 2

/-- Bilinear form associated with the same symmetric 2x2 matrix. -/
def bilinear2 (a b c u1 u2 v1 v2 : ℝ) : ℝ :=
  a * u1 * v1 + b * u1 * v2 + b * u2 * v1 + c * u2 * v2

/-- Diagonal coordinate scaling transports a symmetric quadratic form by
congruence. This is the checker-facing `W_z = Sᵀ W_x S` identity for
`S = diag(s1,s2)`, with no inverse or square root. -/
theorem quadraticForm_congruence
    (a b c s1 s2 x y : ℝ) :
    qform2 (a * s1 ^ 2) (b * s1 * s2) (c * s2 ^ 2) x y
      = qform2 a b c (s1 * x) (s2 * y) := by
  simp [qform2]
  ring

/-- Bilinear companion to `quadraticForm_congruence`. -/
theorem bilinear_congruence
    (a b c s1 s2 u1 u2 v1 v2 : ℝ) :
    bilinear2 (a * s1 ^ 2) (b * s1 * s2) (c * s2 ^ 2)
        u1 u2 v1 v2
      = bilinear2 a b c (s1 * u1) (s2 * u2) (s1 * v1) (s2 * v2) := by
  simp [bilinear2]
  ring

/-- Pointwise strong-monotonicity gate is exactly invariant when state and
residual differences are transported covariantly by the same diagonal chart.
The numerical constant `mu` is unchanged. -/
theorem strongMonotone_similarity_iff
    (a b c s1 s2 mu fz1 fz2 dz1 dz2 fx1 fx2 dx1 dx2 : ℝ)
    (hfx1 : fx1 = s1 * fz1)
    (hfx2 : fx2 = s2 * fz2)
    (hdx1 : dx1 = s1 * dz1)
    (hdx2 : dx2 = s2 * dz2) :
    bilinear2 (a * s1 ^ 2) (b * s1 * s2) (c * s2 ^ 2)
        fz1 fz2 dz1 dz2
        ≥ mu * qform2 (a * s1 ^ 2) (b * s1 * s2) (c * s2 ^ 2) dz1 dz2
      ↔ bilinear2 a b c fx1 fx2 dx1 dx2 ≥ mu * qform2 a b c dx1 dx2 := by
  subst fx1
  subst fx2
  subst dx1
  subst dx2
  rw [bilinear_congruence, quadraticForm_congruence]

/-- Pointwise squared-Lipschitz gate is exactly invariant under the same
covariant state/residual transport. The numerical constant `Lambda` is
unchanged. -/
theorem sqLipschitz_similarity_iff
    (a b c s1 s2 Lambda fz1 fz2 dz1 dz2 fx1 fx2 dx1 dx2 : ℝ)
    (hfx1 : fx1 = s1 * fz1)
    (hfx2 : fx2 = s2 * fz2)
    (hdx1 : dx1 = s1 * dz1)
    (hdx2 : dx2 = s2 * dz2) :
    qform2 (a * s1 ^ 2) (b * s1 * s2) (c * s2 ^ 2) fz1 fz2
        ≤ Lambda * qform2 (a * s1 ^ 2) (b * s1 * s2) (c * s2 ^ 2) dz1 dz2
      ↔ qform2 a b c fx1 fx2 ≤ Lambda * qform2 a b c dx1 dx2 := by
  subst fx1
  subst fx2
  subst dx1
  subst dx2
  rw [quadraticForm_congruence, quadraticForm_congruence]

/-- Exact damped-corrector conjugacy. The affine offset cancels and the scalar
step `h` is not rescaled. -/
theorem corrector_step_similarity
    (c1 c2 s1 s2 h z1 z2 fz1 fz2 : ℝ) :
    (c1 + s1 * (z1 - h * fz1)
        = (c1 + s1 * z1) - h * (s1 * fz1))
      ∧ (c2 + s2 * (z2 - h * fz2)
        = (c2 + s2 * z2) - h * (s2 * fz2)) := by
  constructor <;> ring

/-- Symmetric Jacobian quadratic packet `v ↦ <Jv,v>_W + <v,Jv>_W`. -/
def jacobianSymQuadratic2
    (a b c j11 j12 j21 j22 x y : ℝ) : ℝ :=
  let u1 := j11 * x + j12 * y
  let u2 := j21 * x + j22 * y
  bilinear2 a b c u1 u2 x y + bilinear2 a b c x y u1 u2

/-- If the Jacobian actions satisfy the multiplication-only intertwining
`J_x S v = S J_z v`, the T-P5-074 symmetric quadratic packet transforms by the
same congruence. -/
theorem jacobian_sym_congruence
    (a b c s1 s2 jx11 jx12 jx21 jx22 jz11 jz12 jz21 jz22 x y : ℝ)
    (h1 : jx11 * (s1 * x) + jx12 * (s2 * y)
      = s1 * (jz11 * x + jz12 * y))
    (h2 : jx21 * (s1 * x) + jx22 * (s2 * y)
      = s2 * (jz21 * x + jz22 * y)) :
    jacobianSymQuadratic2
        (a * s1 ^ 2) (b * s1 * s2) (c * s2 ^ 2)
        jz11 jz12 jz21 jz22 x y
      = jacobianSymQuadratic2
          a b c jx11 jx12 jx21 jx22 (s1 * x) (s2 * y) := by
  simp only [jacobianSymQuadratic2]
  rw [h1, h2]
  rw [bilinear_congruence, bilinear_congruence]

/-- Weighted Jacobian Gram quadratic packet `v ↦ Q_W(Jv)`. -/
def jacobianGramQuadratic2
    (a b c j11 j12 j21 j22 x y : ℝ) : ℝ :=
  qform2 a b c (j11 * x + j12 * y) (j21 * x + j22 * y)

/-- The T-P5-076 weighted Gram quadratic packet transforms by congruence from
the same multiplication-only Jacobian intertwining. -/
theorem jacobian_gram_congruence
    (a b c s1 s2 jx11 jx12 jx21 jx22 jz11 jz12 jz21 jz22 x y : ℝ)
    (h1 : jx11 * (s1 * x) + jx12 * (s2 * y)
      = s1 * (jz11 * x + jz12 * y))
    (h2 : jx21 * (s1 * x) + jx22 * (s2 * y)
      = s2 * (jz21 * x + jz22 * y)) :
    jacobianGramQuadratic2
        (a * s1 ^ 2) (b * s1 * s2) (c * s2 ^ 2)
        jz11 jz12 jz21 jz22 x y
      = jacobianGramQuadratic2
          a b c jx11 jx12 jx21 jx22 (s1 * x) (s2 * y) := by
  simp only [jacobianGramQuadratic2]
  rw [h1, h2]
  exact quadraticForm_congruence a b c s1 s2
    (jz11 * x + jz12 * y) (jz21 * x + jz22 * y)

/-- Exact regression from柳冠一's obstruction: after `S=diag(3,1)`, freezing the
metric at the Euclidean identity makes the symmetric Jacobian quadratic
negative at `(1,1)`. -/
theorem frozen_metric_monotonicity_counterexample :
    (2 : ℝ) * 1 ^ 2
        + 2 * ((1 / 3 : ℝ) + (-3 : ℝ)) * 1 * 1
        + 2 * 1 ^ 2
      = (-4 / 3 : ℝ) := by
  norm_num

/-- With the correct transported metric `diag(9,1)`, the same normalized
Jacobian has the exact strong-monotonicity packet `A_z = 2 W_z` at quadratic
form level. -/
theorem transported_metric_sym_regression (x y : ℝ) :
    jacobianSymQuadratic2
        (9 : ℝ) 0 1
        1 (1 / 3 : ℝ) (-3 : ℝ) 1 x y
      = 2 * qform2 (9 : ℝ) 0 1 x y := by
  simp [jacobianSymQuadratic2, bilinear2, qform2]
  ring

/-- The same exact example has weighted squared gain `Lambda = 2` in the
transported metric. -/
theorem transported_metric_gram_regression (x y : ℝ) :
    jacobianGramQuadratic2
        (9 : ℝ) 0 1
        1 (1 / 3 : ℝ) (-3 : ℝ) 1 x y
      = 2 * qform2 (9 : ℝ) 0 1 x y := by
  simp [jacobianGramQuadratic2, qform2]
  ring

#print axioms quadraticForm_congruence
#print axioms bilinear_congruence
#print axioms strongMonotone_similarity_iff
#print axioms sqLipschitz_similarity_iff
#print axioms corrector_step_similarity
#print axioms jacobian_sym_congruence
#print axioms jacobian_gram_congruence
#print axioms frozen_metric_monotonicity_counterexample
#print axioms transported_metric_sym_regression
#print axioms transported_metric_gram_regression

end RouteBP5SimilarityNormalization

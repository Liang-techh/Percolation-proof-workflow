import Mathlib

noncomputable section

namespace RouteBP5RelativeRemainderAbsorption

/-- Exact algebraic recombination when nominal and remainder terms share the same monomial. -/
theorem same_monomial_exact_factorization
    (mon u e g r : ℝ)
    (hg : g = mon * u)
    (hr : r = mon * e) :
    g + r = mon * (u + e) := by
  rw [hg, hr]
  ring

/--
The signed unit packet survives an additive normalized remainder whose absolute
charge is strictly smaller than the certified unit margin.  `abs sigma = 1`
is the typed replacement for the informal `sigma ∈ {+1,-1}` convention.
-/
theorem same_monomial_remainder_absorption
    (sigma u e m M eps : ℝ)
    (hsigma : abs sigma = 1)
    (hlower : m ≤ sigma * u)
    (hupper : sigma * u ≤ M)
    (heps : abs e ≤ eps)
    (hgate : eps < m) :
    m - eps ≤ sigma * (u + e) ∧
      sigma * (u + e) ≤ M + eps := by
  have hscaled : abs (sigma * e) ≤ eps := by
    rw [abs_mul, hsigma, one_mul]
    exact heps
  have hscaledLower : -eps ≤ sigma * e := by
    have h1 : -abs (sigma * e) ≤ sigma * e := neg_abs_le (sigma * e)
    have h2 : -eps ≤ -abs (sigma * e) := neg_le_neg hscaled
    exact le_trans h2 h1
  have hscaledUpper : sigma * e ≤ eps :=
    le_trans (le_abs_self (sigma * e)) hscaled
  constructor
  · calc
      m - eps ≤ sigma * u + sigma * e := by linarith
      _ = sigma * (u + e) := by ring
  · calc
      sigma * (u + e) = sigma * u + sigma * e := by ring
      _ ≤ M + eps := by linarith

/-- Strict positivity of the perturbed signed unit margin. -/
theorem absorbed_unit_has_strict_sign
    (sigma u e m M eps : ℝ)
    (hsigma : abs sigma = 1)
    (hm : 0 < m)
    (hlower : m ≤ sigma * u)
    (hupper : sigma * u ≤ M)
    (heps : abs e ≤ eps)
    (hgate : eps < m) :
    0 < sigma * (u + e) := by
  have hbounds :=
    same_monomial_remainder_absorption
      sigma u e m M eps hsigma hlower hupper heps hgate
  linarith

/--
Interface lemma for a higher-order normalized remainder.  The finite-product
monomial estimate is deliberately supplied as `abs monS ≤ Hcharge` rather than
reimplemented here.
-/
theorem higher_order_normalized_charge
    (monS v B Hcharge : ℝ)
    (hH : 0 ≤ Hcharge)
    (hmon : abs monS ≤ Hcharge)
    (hv : abs v ≤ B) :
    abs (monS * v) ≤ B * Hcharge := by
  rw [abs_mul]
  calc
    abs monS * abs v ≤ Hcharge * B :=
      mul_le_mul hmon hv (abs_nonneg v) hH
    _ = B * Hcharge := by ring

/--
Division-free higher-order cell gate.  A certified bound `B*Hcharge < m`
produces the exact new unit margin `m - B*Hcharge > 0`.
-/
theorem higher_order_remainder_unit_margin
    (sigma u monS v m M B Hcharge : ℝ)
    (hsigma : abs sigma = 1)
    (hm : 0 < m)
    (hlower : m ≤ sigma * u)
    (hupper : sigma * u ≤ M)
    (hH : 0 ≤ Hcharge)
    (hmon : abs monS ≤ Hcharge)
    (hv : abs v ≤ B)
    (hgate : B * Hcharge < m) :
    0 < m - B * Hcharge ∧
      (m - B * Hcharge ≤ sigma * (u + monS * v) ∧
        sigma * (u + monS * v) ≤ M + B * Hcharge) := by
  have hcharge : abs (monS * v) ≤ B * Hcharge :=
    higher_order_normalized_charge monS v B Hcharge hH hmon hv
  constructor
  · linarith
  · exact
      same_monomial_remainder_absorption
        sigma u (monS * v) m M (B * Hcharge)
        hsigma hlower hupper hcharge hgate

/-- Relative remainder below 100% is strictly smaller than the nominal factor. -/
theorem relative_remainder_abs_lt
    (g r alpha : ℝ)
    (hg : g ≠ 0)
    (halpha0 : 0 ≤ alpha)
    (halpha1 : alpha < 1)
    (hrel : abs r ≤ alpha * abs g) :
    abs r < abs g := by
  have hgabs : 0 < abs g := abs_pos.mpr hg
  have hscale : alpha * abs g < 1 * abs g :=
    mul_lt_mul_of_pos_right halpha1 hgabs
  exact lt_of_le_of_lt hrel (by simpa using hscale)

/--
Division-free sign-stability form: the perturbed and nominal factors have a
strictly positive product, hence the same nonzero sign on the punctured domain.
-/
theorem relative_remainder_same_sign
    (g r alpha : ℝ)
    (hg : g ≠ 0)
    (halpha0 : 0 ≤ alpha)
    (halpha1 : alpha < 1)
    (hrel : abs r ≤ alpha * abs g) :
    0 < (g + r) * g := by
  have hrlt : abs r < abs g :=
    relative_remainder_abs_lt g r alpha hg halpha0 halpha1 hrel
  have hrlower : -abs g < r := (abs_lt.mp hrlt).1
  have hrupper : r < abs g := (abs_lt.mp hrlt).2
  by_cases hgpos : 0 < g
  · rw [abs_of_pos hgpos] at hrlower
    have hsum : 0 < g + r := by linarith
    exact mul_pos hsum hgpos
  · have hgle : g ≤ 0 := le_of_not_gt hgpos
    have hgneg : g < 0 := lt_of_le_of_ne hgle hg
    rw [abs_of_neg hgneg] at hrupper
    have hsum : g + r < 0 := by linarith
    exact mul_pos_of_neg_of_neg hsum hgneg

/-- `alpha = 1` is a sharp cancellation boundary: the actual factor may vanish. -/
theorem alpha_one_cancellation_boundary :
    abs (-1 : ℝ) ≤ (1 : ℝ) * abs (1 : ℝ) ∧
      (1 : ℝ) + (-1 : ℝ) = 0 := by
  norm_num

/-- Lower-order contamination regression from the mathematical review. -/
theorem lower_order_contamination_factorization
    (eps z : ℝ) :
    z ^ 2 + eps * z = z * (z + eps) := by
  ring

/--
Additive regularity budget for normalized remainders, stated as a scalar
difference estimate so no additional topological source structure is assumed.
-/
theorem additive_normalized_remainder_difference_budget
    (u1 u2 e1 e2 Lu Le d : ℝ)
    (hu : abs (u1 - u2) ≤ Lu * d)
    (he : abs (e1 - e2) ≤ Le * d) :
    abs ((u1 + e1) - (u2 + e2)) ≤ (Lu + Le) * d := by
  have htri :
      abs ((u1 - u2) + (e1 - e2)) ≤
        abs (u1 - u2) + abs (e1 - e2) :=
    abs_add_le (u1 - u2) (e1 - e2)
  calc
    abs ((u1 + e1) - (u2 + e2)) =
        abs ((u1 - u2) + (e1 - e2)) := by
          congr 1
          ring
    _ ≤ abs (u1 - u2) + abs (e1 - e2) := htri
    _ ≤ (Lu + Le) * d := by linarith

/--
Same-domain pointwise adapter.  A caller cannot splice unit and remainder
certificates from different source cells because every premise carries `D z`.
-/
theorem source_family_same_monomial_absorption
    {Z : Type*}
    (D : Z → Prop)
    (sigma u e : Z → ℝ)
    (m M eps : ℝ)
    (hsigma : ∀ z, D z → abs (sigma z) = 1)
    (hlower : ∀ z, D z → m ≤ sigma z * u z)
    (hupper : ∀ z, D z → sigma z * u z ≤ M)
    (heps : ∀ z, D z → abs (e z) ≤ eps)
    (hgate : eps < m) :
    ∀ z, D z →
      m - eps ≤ sigma z * (u z + e z) ∧
        sigma z * (u z + e z) ≤ M + eps := by
  intro z hz
  exact
    same_monomial_remainder_absorption
      (sigma z) (u z) (e z) m M eps
      (hsigma z hz) (hlower z hz) (hupper z hz) (heps z hz) hgate

#print axioms same_monomial_exact_factorization
#print axioms same_monomial_remainder_absorption
#print axioms absorbed_unit_has_strict_sign
#print axioms higher_order_normalized_charge
#print axioms higher_order_remainder_unit_margin
#print axioms relative_remainder_abs_lt
#print axioms relative_remainder_same_sign
#print axioms alpha_one_cancellation_boundary
#print axioms lower_order_contamination_factorization
#print axioms additive_normalized_remainder_difference_budget
#print axioms source_family_same_monomial_absorption

end RouteBP5RelativeRemainderAbsorption

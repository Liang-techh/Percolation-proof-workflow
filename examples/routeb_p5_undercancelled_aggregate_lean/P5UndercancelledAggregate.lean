import Mathlib

noncomputable section

namespace RouteBP5UndercancelledAggregate

/-- Integer-valued net contact order: numerator order minus denominator order. -/
def netOrder (A B : ℕ) : ℤ := (A : ℤ) - (B : ℤ)

/-- Exact monomial aggregate away from the contact point. -/
def aggregateMonomial (A B : ℕ) (x : ℝ) : ℝ := x ^ A / x ^ B

/-- Polynomial extension used when the aggregate net order is nonnegative. -/
def aggregateExtension (A B : ℕ) (x : ℝ) : ℝ := x ^ (A - B)

/-- Exact two-term principal model for additive cancellation at a contact. -/
def principalPair (a b x : ℝ) : ℝ := a / x + b / x

/-- Global boundedness of the exact principal pair.  For a pure `1/x` principal model
this is equivalent to boundedness near the contact and avoids choosing a neighbourhood radius. -/
def PrincipalPairBounded (a b : ℝ) : Prop :=
  ∃ C : ℝ, 0 ≤ C ∧ ∀ x : ℝ, x ≠ 0 → |principalPair a b x| ≤ C

/-- Nonnegative integer net order is exactly the natural inequality `B ≤ A`. -/
theorem net_order_nonnegative_iff
    (A B : ℕ) :
    0 ≤ netOrder A B ↔ B ≤ A := by
  simp [netOrder]

/-- Negative integer net order is exactly the natural inequality `A < B`. -/
theorem net_order_negative_iff
    (A B : ℕ) :
    netOrder A B < 0 ↔ A < B := by
  simp [netOrder]

/-- Division-free cancellation of common contact powers when the aggregate excess is nonnegative. -/
theorem aggregate_integer_excess_identity
    (A B : ℕ)
    (x : ℝ)
    (hBA : B ≤ A)
    (hx : x ≠ 0) :
    aggregateMonomial A B x = x ^ (A - B) := by
  have hpowB : x ^ B ≠ 0 := pow_ne_zero B hx
  dsimp [aggregateMonomial]
  calc
    x ^ A / x ^ B = (x ^ (A - B) * x ^ B) / x ^ B := by
      congr 1
      rw [← pow_add, Nat.sub_add_cancel hBA]
    _ = x ^ (A - B) := by
      field_simp [hpowB]

/-- The canonical polynomial extension agrees with the original quotient off contact. -/
theorem aggregate_extension_agrees_off_contact
    (A B : ℕ)
    (hBA : B ≤ A)
    (x : ℝ)
    (hx : x ≠ 0) :
    aggregateExtension A B x = aggregateMonomial A B x := by
  symm
  exact aggregate_integer_excess_identity A B x hBA hx

/-- Kernel-facing contact-safety gate: nonnegative aggregate net order admits a continuous extension. -/
theorem aggregate_contact_safe_of_net_nonnegative
    (A B : ℕ)
    (hnet : 0 ≤ netOrder A B) :
    ∃ f : ℝ → ℝ,
      Continuous f ∧
      ∀ x : ℝ, x ≠ 0 → f x = aggregateMonomial A B x := by
  have hBA : B ≤ A := (net_order_nonnegative_iff A B).1 hnet
  refine ⟨aggregateExtension A B, ?_, ?_⟩
  · exact continuous_id.pow (A - B)
  · intro x hx
    exact aggregate_extension_agrees_off_contact A B hBA x hx

/-- Zero net order has the finite nonzero monomial scale `1` off contact. -/
theorem zero_net_order_finite_scale
    (A : ℕ)
    (x : ℝ)
    (hx : x ≠ 0) :
    aggregateMonomial A A x = 1 := by
  dsimp [aggregateMonomial]
  exact div_self (pow_ne_zero A hx)

/-- Strictly positive net order makes the canonical aggregate extension vanish at contact. -/
theorem positive_net_order_zero_extension
    (A B : ℕ)
    (hBA : B < A) :
    aggregateExtension A B 0 = 0 := by
  dsimp [aggregateExtension]
  exact zero_pow (Nat.sub_ne_zero_iff_lt.mpr hBA)

/-- Negative net order is exactly a reciprocal positive power away from contact. -/
theorem negative_net_order_reciprocal_form
    (A B : ℕ)
    (hAB : A < B)
    (x : ℝ)
    (hx : x ≠ 0) :
    aggregateMonomial A B x = 1 / x ^ (B - A) := by
  have hA : A ≤ B := Nat.le_of_lt hAB
  have hpowA : x ^ A ≠ 0 := pow_ne_zero A hx
  have hpowD : x ^ (B - A) ≠ 0 := pow_ne_zero (B - A) hx
  have hsplit : x ^ B = x ^ A * x ^ (B - A) := by
    rw [← pow_add, Nat.add_sub_of_le hA]
  dsimp [aggregateMonomial]
  rw [hsplit]
  field_simp [hpowA, hpowD]

/-- Every positive reciprocal power is unbounded along positive points approaching the contact. -/
theorem reciprocal_power_unbounded_right
    (d : ℕ)
    (hd : 0 < d) :
    ∀ K : ℝ, 0 ≤ K →
      ∃ x : ℝ, 0 < x ∧ x ≤ 1 ∧ K < 1 / x ^ d := by
  intro K hK
  let y : ℝ := K + 2
  have hy1 : 1 < y := by
    dsimp [y]
    linarith
  have hy0 : 0 < y := lt_trans zero_lt_one hy1
  have hyone : 1 ≤ y := le_of_lt hy1
  have hpow_ge_one : ∀ n : ℕ, 1 ≤ y ^ n := by
    intro n
    induction n with
    | zero => simp
    | succ n ih =>
        rw [pow_succ]
        nlinarith
  let x : ℝ := 1 / y
  have hxpos : 0 < x := by
    dsimp [x]
    exact one_div_pos.mpr hy0
  have hxle : x ≤ 1 := by
    dsimp [x]
    apply (div_le_iff₀ hy0).2
    nlinarith
  cases d with
  | zero => simp at hd
  | succ n =>
      have hpow1 : 1 ≤ y ^ n := hpow_ge_one n
      have hlarge : K < y ^ (n + 1) := by
        rw [pow_succ]
        dsimp [y] at hy1 hy0 hyone ⊢
        nlinarith
      have hrecip : 1 / x ^ (n + 1) = y ^ (n + 1) := by
        dsimp [x]
        simp [one_div, inv_pow]
      refine ⟨x, hxpos, hxle, ?_⟩
      rw [hrecip]
      exact hlarge

/-- A negative aggregate net order is genuinely unbounded; no factorwise rescue is available. -/
theorem negative_net_order_unbounded
    (A B : ℕ)
    (hnet : netOrder A B < 0) :
    ∀ K : ℝ, 0 ≤ K →
      ∃ x : ℝ, 0 < x ∧ x ≤ 1 ∧ K < aggregateMonomial A B x := by
  have hAB : A < B := (net_order_negative_iff A B).1 hnet
  have hd : 0 < B - A := Nat.sub_pos_of_lt hAB
  intro K hK
  obtain ⟨x, hxpos, hxle, hlarge⟩ := reciprocal_power_unbounded_right (B - A) hd K hK
  refine ⟨x, hxpos, hxle, ?_⟩
  rw [negative_net_order_reciprocal_form A B hAB x (ne_of_gt hxpos)]
  exact hlarge

/-- Exact rescue example: a factor that looks undercancelled in isolation is harmless in the aggregate. -/
theorem undercancelled_product_exact_rescue
    (a₁ a₂ x : ℝ)
    (hx : x ≠ 0) :
    ((a₁ * x ^ 2) * (a₂ * x)) / x ^ 2 = (a₁ * a₂) * x := by
  field_simp [hx]
  ring

/-- Zero-net-order regression: the aggregate is finite even though each quotient need not be inspected separately. -/
theorem zero_net_order_exact_example
    (a₁ a₂ x : ℝ)
    (hx : x ≠ 0) :
    ((a₁ * x ^ 2) * (a₂ * x)) / x ^ 3 = a₁ * a₂ := by
  field_simp [hx]
  ring

/-- Negative-net-order regression: two first-order factors over a third-order denominator leave a pole. -/
theorem negative_net_order_exact_example
    (a₁ a₂ x : ℝ)
    (hx : x ≠ 0) :
    ((a₁ * x) * (a₂ * x)) / x ^ 3 = (a₁ * a₂) / x := by
  field_simp [hx]
  ring

/-- Monomial pullback transports contact exponents multiplicatively. -/
theorem monomial_pullback_exponent_transport
    (lambda y : ℝ)
    (p M : ℕ) :
    (lambda * y ^ p) ^ M = lambda ^ M * y ^ (p * M) := by
  rw [mul_pow, pow_mul]

/-- In the exact principal model `a/x + b/x`, boundedness is equivalent to coefficient cancellation. -/
theorem additive_cancellation_bounded_iff
    (a b : ℝ) :
    PrincipalPairBounded a b ↔ a + b = 0 := by
  constructor
  · rintro ⟨C, hC, hbound⟩
    by_contra hsum
    have hcabspos : 0 < |a + b| := abs_pos.mpr hsum
    let D : ℝ := C + 1
    have hDpos : 0 < D := by
      dsimp [D]
      linarith
    let x : ℝ := |a + b| / D
    have hxpos : 0 < x := by
      dsimp [x]
      exact div_pos hcabspos hDpos
    have hxne : x ≠ 0 := ne_of_gt hxpos
    have hvalue : |principalPair a b x| = D := by
      dsimp [principalPair]
      rw [← add_div, abs_div, abs_of_pos hxpos]
      dsimp [x]
      field_simp [ne_of_gt hcabspos, ne_of_gt hDpos]
    have hle := hbound x hxne
    rw [hvalue] at hle
    dsimp [D] at hle
    linarith
  · intro hsum
    refine ⟨0, le_rfl, ?_⟩
    intro x hx
    have hzero : principalPair a b x = 0 := by
      dsimp [principalPair]
      rw [← add_div, hsum]
      simp
    rw [hzero, abs_zero]

/-- Failure of additive principal-part cancellation rules out any bounded principal model. -/
theorem additive_noncancellation_unbounded
    (a b : ℝ)
    (hsum : a + b ≠ 0) :
    ¬ PrincipalPairBounded a b := by
  intro hbounded
  exact hsum ((additive_cancellation_bounded_iff a b).1 hbounded)

/-- Exact vanishing-atom regression: if `mu = kappa^2`, then `mu^2/kappa = kappa^3`. -/
theorem exact_vanishing_atom_rescue
    (kappa : ℝ)
    (hkappa : kappa ≠ 0) :
    (kappa ^ 2) ^ 2 / kappa = kappa ^ 3 := by
  field_simp [hkappa]
  ring

#print axioms net_order_nonnegative_iff
#print axioms net_order_negative_iff
#print axioms aggregate_integer_excess_identity
#print axioms aggregate_extension_agrees_off_contact
#print axioms aggregate_contact_safe_of_net_nonnegative
#print axioms zero_net_order_finite_scale
#print axioms positive_net_order_zero_extension
#print axioms negative_net_order_reciprocal_form
#print axioms reciprocal_power_unbounded_right
#print axioms negative_net_order_unbounded
#print axioms undercancelled_product_exact_rescue
#print axioms zero_net_order_exact_example
#print axioms negative_net_order_exact_example
#print axioms monomial_pullback_exponent_transport
#print axioms additive_cancellation_bounded_iff
#print axioms additive_noncancellation_unbounded
#print axioms exact_vanishing_atom_rescue

end RouteBP5UndercancelledAggregate

import Mathlib.Data.Real.Basic
import Mathlib.Data.Fin.VecNotation
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic

/-!
  B45-2: an isolated exact-real / conditional-Float64 seam.

  This file deliberately does not import a deployed-source comparator, a
  workflow state, or a theorem registry.  Every machine result is an
  interpreted real value supplied through hypotheses.  The exact model keeps
  six-dimensional q and dq, the centered samples q plus/minus h e_k, h=1/100000,
  and the mass regularizer mu=1/1000000 explicit.

  The final budget retains the cross terms: an exact FD defect and a runtime
  Float64 defect are added before squaring.  This is an interface theorem, not
  a claim that the hypotheses have already been established for Julia.
-/

open scoped BigOperators

namespace RouteBB45Float64Seam

noncomputable section

abbrev I6 := Fin 6
abbrev Q := I6 → ℝ
abbrev Matrix6 := I6 → I6 → ℝ

def h : ℝ := 1 / 100000
def mu : ℝ := 1 / 1000000

theorem h_pos : 0 < h := by norm_num [h]
theorem mu_pos : 0 < mu := by norm_num [mu]

/- The source call uses the same six coordinates for q, dq, and every FD
   sample.  qShift is intentionally coordinate-wise rather than a lifted
   circle variable: q plus/minus h e_k remains visible in the type. -/
def qShift (q : Q) (k : I6) (s : ℝ) : Q :=
  fun i => if i = k then q i + s else q i

def qPlus (q : Q) (k : I6) : Q := qShift q k h
def qMinus (q : Q) (k : I6) : Q := qShift q k (-h)

theorem qPlus_is_q_shift (q : Q) (k : I6) : qPlus q k = qShift q k h := rfl
theorem qMinus_is_q_shift (q : Q) (k : I6) : qMinus q k = qShift q k (-h) := rfl

/- The regularizer is recorded independently of any mass reconstruction. -/
def regularizedMass (M : Matrix6) : Matrix6 :=
  fun i j => M i j + if i = j then mu else 0

theorem regularizer_value : mu = (1 / 1000000 : ℝ) := by rfl

/- Minimal explicit IEEE-754 binary64 interface.  This is the usual relative
   rounding model for a finite normal result; `ieee64Round` is a premise, not
   an assertion that every deployed operation is normal or overflow-free. -/
def ieee64UnitRoundoff : ℝ := 1 / 2 ^ 53

def ieee64Round (x xhat : ℝ) : Prop :=
  |xhat - x| ≤ ieee64UnitRoundoff * |x|

theorem ieee64UnitRoundoff_nonneg : 0 ≤ ieee64UnitRoundoff := by
  norm_num [ieee64UnitRoundoff]

theorem ieee64_round_abs_enclosure
    (x xhat B : ℝ) (hx : |x| ≤ B)
    (hround : ieee64Round x xhat) :
    |xhat - x| ≤ ieee64UnitRoundoff * B := by
  dsimp [ieee64Round] at hround
  exact hround.trans (mul_le_mul_of_nonneg_left hx ieee64UnitRoundoff_nonneg)

theorem ieee64_step_abs_enclosure (hhat : ℝ) (hround : ieee64Round h hhat) :
    |hhat - h| ≤ ieee64UnitRoundoff * |h| := by
  dsimp [ieee64Round] at hround
  simpa [abs_sub_comm] using hround

/- Exact-real centered potential gradient.  U is abstract here on purpose:
   identifying it with the deployed DH source belongs to the separate source
   comparator obligation. -/
def gradientFD (U : Q → ℝ) (q : Q) (k : I6) : ℝ :=
  (U (qPlus q k) - U (qMinus q k)) / (2 * h)

def floatGradient (Uhat : Q → ℝ) (q : Q) (k : I6) : ℝ :=
  (Uhat (qPlus q k) - Uhat (qMinus q k)) / (2 * h)

theorem potential_value_enclosure
    (U Uhat : Q → ℝ) (x : Q) (eps : ℝ)
    (hvalue : |Uhat x - U x| ≤ eps) :
    |Uhat x| ≤ |U x| + eps := by
  calc
    |Uhat x| = |(Uhat x - U x) + U x| := by ring_nf
    _ ≤ |Uhat x - U x| + |U x| := abs_add_le _ _
    _ ≤ eps + |U x| := add_le_add hvalue le_rfl
    _ = |U x| + eps := by ring

theorem gradient_float64_enclosure
    (U Uhat : Q → ℝ) (q : Q) (k : I6) (epsPlus epsMinus : ℝ)
    (hplus_value : |Uhat (qPlus q k) - U (qPlus q k)| ≤ epsPlus)
    (hminus_value : |Uhat (qMinus q k) - U (qMinus q k)| ≤ epsMinus) :
    |floatGradient Uhat q k - gradientFD U q k| ≤
      (epsPlus + epsMinus) / (2 * h) := by
  have hden : 0 < 2 * h := by norm_num [h]
  let ep : ℝ := Uhat (qPlus q k) - U (qPlus q k)
  let em : ℝ := Uhat (qMinus q k) - U (qMinus q k)
  have he : |ep - em| ≤ epsPlus + epsMinus := by
    calc
      |ep - em| ≤ |ep| + |em| := abs_sub _ _
      _ ≤ epsPlus + epsMinus := add_le_add hplus_value hminus_value
  have hrewrite :
      floatGradient Uhat q k - gradientFD U q k = (ep - em) / (2 * h) := by
    dsimp [floatGradient, gradientFD, ep, em]
    ring
  rw [hrewrite, abs_div, abs_of_pos hden]
  exact div_le_div_of_nonneg_right he (le_of_lt hden)

/- A second form admits a rounded denominator hhat.  The exact sample points
  above remain q plus/minus h e_k; only the interpreted Float64 denominator varies. -/
def floatGradientWithStep (Uhat : Q → ℝ) (q : Q) (k : I6) (hhat : ℝ) : ℝ :=
  (Uhat (qPlus q k) - Uhat (qMinus q k)) / (2 * hhat)

theorem gradient_float64_step_enclosure
    (U Uhat : Q → ℝ) (q : Q) (k : I6)
    (hhat epsH epsPlus epsMinus aBound : ℝ)
    (hhhat : 0 < hhat)
    (ha : 0 ≤ aBound)
    (hstep : |hhat - h| ≤ epsH)
    (hamp : |U (qPlus q k) - U (qMinus q k)| ≤ aBound)
    (hplus_value : |Uhat (qPlus q k) - U (qPlus q k)| ≤ epsPlus)
    (hminus_value : |Uhat (qMinus q k) - U (qMinus q k)| ≤ epsMinus) :
    |floatGradientWithStep Uhat q k hhat - gradientFD U q k| ≤
      (epsPlus + epsMinus) / (2 * hhat) +
        aBound * epsH / (2 * hhat * h) := by
  have hh : 0 < h := h_pos
  have hden : 0 < 2 * hhat := by linarith
  let ahat : ℝ := Uhat (qPlus q k) - Uhat (qMinus q k)
  let a : ℝ := U (qPlus q k) - U (qMinus q k)
  let delta : ℝ := ahat - a
  have hdelta : |delta| ≤ epsPlus + epsMinus := by
    have hform : delta =
        (Uhat (qPlus q k) - U (qPlus q k)) -
          (Uhat (qMinus q k) - U (qMinus q k)) := by
      dsimp [delta, ahat, a]
      ring
    rw [hform]
    calc
      |(Uhat (qPlus q k) - U (qPlus q k)) -
          (Uhat (qMinus q k) - U (qMinus q k))| ≤
          |Uhat (qPlus q k) - U (qPlus q k)| +
            |Uhat (qMinus q k) - U (qMinus q k)| := abs_sub _ _
      _ ≤ epsPlus + epsMinus := add_le_add hplus_value hminus_value
  have hsplit :
      ahat / (2 * hhat) - a / (2 * h) =
        delta / (2 * hhat) + a * (h - hhat) / (2 * hhat * h) := by
    dsimp [delta]
    field_simp
    ring
  rw [show floatGradientWithStep Uhat q k hhat - gradientFD U q k =
      ahat / (2 * hhat) - a / (2 * h) by rfl, hsplit]
  calc
    |delta / (2 * hhat) + a * (h - hhat) / (2 * hhat * h)| ≤
        |delta / (2 * hhat)| + |a * (h - hhat) / (2 * hhat * h)| := by
      exact abs_add_le _ _
    _ = |delta| / (2 * hhat) +
        |a| * |h - hhat| / (2 * hhat * h) := by
      simp only [abs_div, abs_mul, abs_of_pos hden, abs_of_pos hh]
    _ ≤ (epsPlus + epsMinus) / (2 * hhat) +
        aBound * epsH / (2 * hhat * h) := by
      have hstep' : |h - hhat| ≤ epsH := by simpa [abs_sub_comm] using hstep
      have hfirst := div_le_div_of_nonneg_right hdelta (le_of_lt hden)
      have hsecond :
          |a| * |h - hhat| / (2 * hhat * h) ≤
            aBound * epsH / (2 * hhat * h) := by
        have hden' : 0 ≤ 2 * hhat * h := le_of_lt (mul_pos hden hh)
        have hnum : |a| * |h - hhat| ≤ aBound * epsH := by
          exact mul_le_mul hamp hstep' (abs_nonneg _) ha
        exact div_le_div_of_nonneg_right hnum hden'
      exact add_le_add hfirst hsecond

/- Direct FD-9 bridge: exact-real bounds on the two potential values plus
   explicit finite-normal binary64 rounding premises imply the gradient bound.
   No source-comparator equality is used. -/
theorem gradient_ieee64_sample_enclosure
    (U Uhat : Q → ℝ) (q : Q) (k : I6)
    (BPlus BMinus : ℝ)
    (hplus_exact : |U (qPlus q k)| ≤ BPlus)
    (hminus_exact : |U (qMinus q k)| ≤ BMinus)
    (hplus_round : ieee64Round (U (qPlus q k)) (Uhat (qPlus q k)))
    (hminus_round : ieee64Round (U (qMinus q k)) (Uhat (qMinus q k))) :
    |floatGradient Uhat q k - gradientFD U q k| ≤
      (ieee64UnitRoundoff * BPlus + ieee64UnitRoundoff * BMinus) / (2 * h) := by
  apply gradient_float64_enclosure U Uhat q k
  · exact ieee64_round_abs_enclosure _ _ _ hplus_exact hplus_round
  · exact ieee64_round_abs_enclosure _ _ _ hminus_exact hminus_round

/- Christoffel contraction.  dM is the six-dimensional derivative tensor
   supplied by the exact-real or interpreted runtime layer. -/
def christoffel (dM : I6 → I6 → I6 → ℝ) (i j k : I6) : ℝ :=
  (dM i j k + dM i k j - dM j k i) / 2

def cContract (dM : I6 → I6 → I6 → ℝ) (dq : Q) (i : I6) : ℝ :=
  ∑ j, ∑ k, christoffel dM i j k * dq j * dq k

def cContractErrorBound (dE : I6 → I6 → I6 → ℝ) (dq : Q) (i : I6) : ℝ :=
  ∑ j, ∑ k,
    (dE i j k + dE i k j + dE j k i) / 2 * |dq j| * |dq k|

theorem c_contract_error_enclosure
    (dM dMhat : I6 → I6 → I6 → ℝ)
    (dE : I6 → I6 → I6 → ℝ) (dq : Q)
    (hderiv : ∀ i j k, |dMhat i j k - dM i j k| ≤ dE i j k)
    :
    |cContract dMhat dq i - cContract dM dq i| ≤
      cContractErrorBound dE dq i := by
  have hterm : ∀ j k,
      |christoffel dMhat i j k - christoffel dM i j k| ≤
        (dE i j k + dE i k j + dE j k i) / 2 := by
    intro j k
    have h1 := hderiv i j k
    have h2 := hderiv i k j
    have h3 := hderiv j k i
    have hsum := add_le_add (add_le_add h1 h2) h3
    have hform :
        christoffel dMhat i j k - christoffel dM i j k =
          ((dMhat i j k - dM i j k) +
            (dMhat i k j - dM i k j) -
            (dMhat j k i - dM j k i)) / 2 := by
      dsimp [christoffel]
      ring
    rw [hform, abs_div, abs_of_pos (by norm_num : (0 : ℝ) < 2)]
    have habs :
        |(dMhat i j k - dM i j k) +
          (dMhat i k j - dM i k j) -
          (dMhat j k i - dM j k i)| ≤
        |dMhat i j k - dM i j k| +
          |dMhat i k j - dM i k j| +
          |dMhat j k i - dM j k i| := by
      calc
        _ ≤ |(dMhat i j k - dM i j k) +
              (dMhat i k j - dM i k j)| +
              |dMhat j k i - dM j k i| := abs_sub _ _
        _ ≤ (|dMhat i j k - dM i j k| +
              |dMhat i k j - dM i k j|) +
              |dMhat j k i - dM j k i| :=
          by
            have hadd :
                |(dMhat i j k - dM i j k) +
                  (dMhat i k j - dM i k j)| ≤
                |dMhat i j k - dM i j k| +
                  |dMhat i k j - dM i k j| := abs_add_le _ _
            simpa [add_comm, add_left_comm, add_assoc] using
              (add_le_add_right hadd |dMhat j k i - dM j k i|)
        _ = _ := by ring
    have hsum' :
        |dMhat i j k - dM i j k| +
          |dMhat i k j - dM i k j| +
          |dMhat j k i - dM j k i| ≤
        dE i j k + dE i k j + dE j k i := by
      linarith
    exact le_trans (div_le_div_of_nonneg_right habs (by norm_num))
      (div_le_div_of_nonneg_right hsum' (by norm_num))
  have hrewrite :
      cContract dMhat dq i - cContract dM dq i =
        ∑ j, ∑ k, (christoffel dMhat i j k - christoffel dM i j k) *
          dq j * dq k := by
    dsimp [cContract]
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro j hj
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro k hk
    ring
  rw [hrewrite]
  dsimp [cContractErrorBound]
  calc
    |∑ j, ∑ k, (christoffel dMhat i j k - christoffel dM i j k) *
        dq j * dq k| ≤
      ∑ j, ∑ k, |christoffel dMhat i j k - christoffel dM i j k| *
        |dq j| * |dq k| := by
          calc
            |∑ j, ∑ k, (christoffel dMhat i j k - christoffel dM i j k) *
                dq j * dq k| ≤
              ∑ j, |∑ k, (christoffel dMhat i j k - christoffel dM i j k) *
                dq j * dq k| := by
              simpa using
                (Finset.abs_sum_le_sum_abs
                  (fun j => ∑ k, (christoffel dMhat i j k - christoffel dM i j k) *
                    dq j * dq k) Finset.univ)
            _ ≤ ∑ j, ∑ k,
                |christoffel dMhat i j k - christoffel dM i j k| *
                  |dq j| * |dq k| := by
              apply Finset.sum_le_sum
              intro j hj
              calc
                |∑ k, (christoffel dMhat i j k - christoffel dM i j k) *
                    dq j * dq k| ≤
                  ∑ k, |(christoffel dMhat i j k - christoffel dM i j k) *
                    dq j * dq k| := by
                  simpa using
                    (Finset.abs_sum_le_sum_abs
                      (fun k => (christoffel dMhat i j k - christoffel dM i j k) *
                        dq j * dq k) Finset.univ)
                _ = ∑ k, |christoffel dMhat i j k - christoffel dM i j k| *
                    |dq j| * |dq k| := by
                  apply Finset.sum_congr rfl
                  intro k hk
                  simp [abs_mul]
    _ ≤ ∑ j, ∑ k,
        ((dE i j k + dE i k j + dE j k i) / 2) *
          |dq j| * |dq k| := by
      apply Finset.sum_le_sum
      intro j hj
      apply Finset.sum_le_sum
      intro k hk
      exact mul_le_mul_of_nonneg_right
        (mul_le_mul_of_nonneg_right (hterm j k) (abs_nonneg _))
        (abs_nonneg _)

/- The source comparator is not used here.  These definitions only describe
   the algebraic decomposition between exact analytic, exact FD, and runtime
   interpreted values. -/
def exactFDDefect (cAnalytic cFD gAnalytic gFD : I6 → ℝ) (i : I6) : ℝ :=
  (cAnalytic i - cFD i) + (gAnalytic i - gFD i)

def runtimeDefect (cFD cFloat gFD gFloat : I6 → ℝ) (i : I6) : ℝ :=
  (cFD i - cFloat i) + (gFD i - gFloat i)

def totalDefect
    (cAnalytic cFD cFloat gAnalytic gFD gFloat : I6 → ℝ) (i : I6) : ℝ :=
  exactFDDefect cAnalytic cFD gAnalytic gFD i +
    runtimeDefect cFD cFloat gFD gFloat i

theorem total_defect_decomposition
    (cAnalytic cFD cFloat gAnalytic gFD gFloat : I6 → ℝ) (i : I6) :
    totalDefect cAnalytic cFD cFloat gAnalytic gFD gFloat i =
      (cAnalytic i - cFloat i) + (gAnalytic i - gFloat i) := by
  dsimp [totalDefect, exactFDDefect, runtimeDefect]
  ring

def weightedBudget (D exactErr runtimeErr : I6 → ℝ) : ℝ :=
  ∑ i, (exactErr i + runtimeErr i) ^ 2 / (2 * D i)

theorem weighted_force_budget
    (D : I6 → ℝ) (e exactErr runtimeErr : I6 → ℝ)
    (hD : ∀ i, 0 < D i)
    (hexact : ∀ i, 0 ≤ exactErr i)
    (hruntime : ∀ i, 0 ≤ runtimeErr i)
    (herror : ∀ i, |e i| ≤ exactErr i + runtimeErr i) :
    ∑ i, e i ^ 2 / (2 * D i) ≤ weightedBudget D exactErr runtimeErr := by
  dsimp [weightedBudget]
  apply Finset.sum_le_sum
  intro i hi
  have hb : 0 ≤ exactErr i + runtimeErr i := add_nonneg (hexact i) (hruntime i)
  have heLower : -(exactErr i + runtimeErr i) ≤ e i :=
    (abs_le.mp (herror i)).1
  have heUpper : e i ≤ exactErr i + runtimeErr i :=
    (abs_le.mp (herror i)).2
  have hsq : e i ^ 2 ≤ (exactErr i + runtimeErr i) ^ 2 := by
    nlinarith [sq_nonneg (e i + (exactErr i + runtimeErr i)),
      sq_nonneg (e i - (exactErr i + runtimeErr i))]
  exact div_le_div_of_nonneg_right hsq
    (le_of_lt (mul_pos (by norm_num : (0 : ℝ) < 2) (hD i)))

theorem exact_plus_runtime_budget
    (D : I6 → ℝ) (e exactErr runtimeErr : I6 → ℝ)
    (hD : ∀ i, 0 < D i)
    (hexact : ∀ i, 0 ≤ exactErr i)
    (hruntime : ∀ i, 0 ≤ runtimeErr i)
    (herror : ∀ i, |e i| ≤ exactErr i + runtimeErr i) :
    ∑ i, e i ^ 2 / (2 * D i) ≤
      ∑ i, (exactErr i ^ 2 + 2 * exactErr i * runtimeErr i +
        runtimeErr i ^ 2) / (2 * D i) := by
  have hmain := weighted_force_budget D e exactErr runtimeErr hD hexact hruntime herror
  calc
    ∑ i, e i ^ 2 / (2 * D i) ≤ weightedBudget D exactErr runtimeErr := hmain
    _ = ∑ i, (exactErr i ^ 2 + 2 * exactErr i * runtimeErr i +
        runtimeErr i ^ 2) / (2 * D i) := by
      apply Finset.sum_congr rfl
      intro i hi
      congr 1
      ring

#print axioms h_pos
#print axioms mu_pos
#print axioms regularizer_value
#print axioms ieee64UnitRoundoff_nonneg
#print axioms ieee64_round_abs_enclosure
#print axioms ieee64_step_abs_enclosure
#print axioms potential_value_enclosure
#print axioms gradient_float64_enclosure
#print axioms gradient_float64_step_enclosure
#print axioms gradient_ieee64_sample_enclosure
#print axioms c_contract_error_enclosure
#print axioms total_defect_decomposition
#print axioms weighted_force_budget
#print axioms exact_plus_runtime_budget

end
end RouteBB45Float64Seam

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P5 incremental parameter-tube gain sidecar

This file formalizes the source-independent algebra from
`agent_review_inbox/review-T-P5-030-honglianmozun-20260907T1205.md`.

The kernel statements cover:

* the exact rank-one outer-product increment identity;
* a fully anisotropic entrywise absolute bound;
* its common-radius/common-anchor specialization;
* the two-component row-sum force bound, including the exact `k_E = 1/10`
  factor used by the current source model;
* homogeneous gain inflation from an anchor residual plus a parameter-tube
  drift term; and
* the pure algebraic finite-cover target implication.

No theorem here authenticates Julia source coefficients, checker output,
parameter-cell coverage, ODE/flowpipe coverage, P5/P8/M4 closure, provenance,
or registry admission.
-/

set_option autoImplicit false

namespace RouteBP5ParameterTubeGain

/-- Exact scalar entry of
`(cStar + delta)(cStar + delta)^T - cStar*cStar^T`. -/
theorem outerProductIncrementIdentity
    (ci cj ciStar cjStar di dj : ℝ)
    (hci : ci = ciStar + di)
    (hcj : cj = cjStar + dj) :
    ci * cj - ciStar * cjStar =
      di * cjStar + ciStar * dj + di * dj := by
  rw [hci, hcj]
  ring

/-- Anisotropic entrywise envelope for the rank-one outer-product increment.
The four absolute-value hypotheses themselves imply every sign fact needed by
multiplication monotonicity, so no redundant nonnegativity assumptions are
exported. -/
theorem outerProductEntryAbsBound
    (di dj ciStar cjStar ri rj Ci Cj : ℝ)
    (hdi : |di| ≤ ri)
    (hdj : |dj| ≤ rj)
    (hci : |ciStar| ≤ Ci)
    (hcj : |cjStar| ≤ Cj) :
    |di * cjStar + ciStar * dj + di * dj| ≤
      ri * Cj + Ci * rj + ri * rj := by
  have hri : 0 ≤ ri := le_trans (abs_nonneg di) hdi
  have hCi : 0 ≤ Ci := le_trans (abs_nonneg ciStar) hci
  have h1 : |di * cjStar| ≤ ri * Cj := by
    rw [abs_mul]
    exact mul_le_mul hdi hcj (abs_nonneg cjStar) hri
  have h2 : |ciStar * dj| ≤ Ci * rj := by
    rw [abs_mul]
    exact mul_le_mul hci hdj (abs_nonneg dj) hCi
  have h3 : |di * dj| ≤ ri * rj := by
    rw [abs_mul]
    exact mul_le_mul hdi hdj (abs_nonneg dj) hri
  calc
    |di * cjStar + ciStar * dj + di * dj| ≤
        |di * cjStar + ciStar * dj| + |di * dj| := abs_add_le _ _
    _ ≤ (|di * cjStar| + |ciStar * dj|) + |di * dj| := by
      exact add_le_add_right (abs_add_le _ _) _
    _ ≤ ri * Cj + Ci * rj + ri * rj := by linarith

/-- Common tube radius `rho` and common anchor coordinate envelope `CStar`
produce the exact polynomial `2*rho*CStar + rho^2`. -/
theorem outerProductEntryAbsBoundIsotropic
    (di dj ciStar cjStar rho CStar : ℝ)
    (hdi : |di| ≤ rho)
    (hdj : |dj| ≤ rho)
    (hci : |ciStar| ≤ CStar)
    (hcj : |cjStar| ≤ CStar) :
    |di * cjStar + ciStar * dj + di * dj| ≤
      2 * rho * CStar + rho ^ 2 := by
  have h := outerProductEntryAbsBound
    di dj ciStar cjStar rho rho CStar CStar hdi hdj hci hcj
  calc
    |di * cjStar + ciStar * dj + di * dj| ≤
        rho * CStar + CStar * rho + rho * rho := h
    _ = 2 * rho * CStar + rho ^ 2 := by ring

/-- Two entries in one matrix row, each bounded by `E`, acting on a two-vector
whose coordinates are bounded by `AD`, cost at most `2*E*AD`. -/
theorem twoComponentRowSumBound
    (d1 d2 a1 a2 E AD : ℝ)
    (hd1 : |d1| ≤ E)
    (hd2 : |d2| ≤ E)
    (ha1 : |a1| ≤ AD)
    (ha2 : |a2| ≤ AD) :
    |d1 * a1 + d2 * a2| ≤ 2 * E * AD := by
  have hE : 0 ≤ E := le_trans (abs_nonneg d1) hd1
  have h1 : |d1 * a1| ≤ E * AD := by
    rw [abs_mul]
    exact mul_le_mul hd1 ha1 (abs_nonneg a1) hE
  have h2 : |d2 * a2| ≤ E * AD := by
    rw [abs_mul]
    exact mul_le_mul hd2 ha2 (abs_nonneg a2) hE
  calc
    |d1 * a1 + d2 * a2| ≤ |d1 * a1| + |d2 * a2| := abs_add_le _ _
    _ ≤ E * AD + E * AD := add_le_add h1 h2
    _ = 2 * E * AD := by ring

/-- Scaling the two-entry row by a nonnegative coefficient `k` preserves the
row-sum bound with the exact factor `2*k`. -/
theorem twoComponentScaledRowSumBound
    (k d1 d2 a1 a2 E AD : ℝ)
    (hk : 0 ≤ k)
    (hd1 : |d1| ≤ E)
    (hd2 : |d2| ≤ E)
    (ha1 : |a1| ≤ AD)
    (ha2 : |a2| ≤ AD) :
    |k * d1 * a1 + k * d2 * a2| ≤ 2 * k * E * AD := by
  have hrow := twoComponentRowSumBound d1 d2 a1 a2 E AD hd1 hd2 ha1 ha2
  have hscaled : k * |d1 * a1 + d2 * a2| ≤ k * (2 * E * AD) :=
    mul_le_mul_of_nonneg_left hrow hk
  calc
    |k * d1 * a1 + k * d2 * a2| = k * |d1 * a1 + d2 * a2| := by
      rw [show k * d1 * a1 + k * d2 * a2 = k * (d1 * a1 + d2 * a2) by ring]
      rw [abs_mul, abs_of_nonneg hk]
    _ ≤ k * (2 * E * AD) := hscaled
    _ = 2 * k * E * AD := by ring

/-- Exact current-source specialization `k_E = 1/10`, hence row factor
`2*k_E = 1/5`. -/
theorem kEOneTenthRowSumBound
    (d1 d2 a1 a2 E AD : ℝ)
    (hd1 : |d1| ≤ E)
    (hd2 : |d2| ≤ E)
    (ha1 : |a1| ≤ AD)
    (ha2 : |a2| ≤ AD) :
    |(1 / 10 : ℝ) * d1 * a1 + (1 / 10 : ℝ) * d2 * a2| ≤
      (1 / 5 : ℝ) * E * AD := by
  have h := twoComponentScaledRowSumBound
    (1 / 10 : ℝ) d1 d2 a1 a2 E AD (by norm_num) hd1 hd2 ha1 ha2
  convert h using 1 <;> ring

/-- Direct current-source consequence for one row of the rank-one mass-block
increment.  This is the exact homogeneous polynomial force coefficient quoted
in `T-P5-030`:
`(1/5) * (2*rho*CStar + rho^2) * AD`. -/
theorem kEOneTenthOuterProductRowBound
    (di dj1 dj2 ciStar cj1Star cj2Star a1 a2 rho CStar AD : ℝ)
    (hdi : |di| ≤ rho)
    (hdj1 : |dj1| ≤ rho)
    (hdj2 : |dj2| ≤ rho)
    (hci : |ciStar| ≤ CStar)
    (hcj1 : |cj1Star| ≤ CStar)
    (hcj2 : |cj2Star| ≤ CStar)
    (ha1 : |a1| ≤ AD)
    (ha2 : |a2| ≤ AD) :
    |(1 / 10 : ℝ) *
          (di * cj1Star + ciStar * dj1 + di * dj1) * a1 +
      (1 / 10 : ℝ) *
          (di * cj2Star + ciStar * dj2 + di * dj2) * a2| ≤
      (1 / 5 : ℝ) * (2 * rho * CStar + rho ^ 2) * AD := by
  have hd1 := outerProductEntryAbsBoundIsotropic
    di dj1 ciStar cj1Star rho CStar hdi hdj1 hci hcj1
  have hd2 := outerProductEntryAbsBoundIsotropic
    di dj2 ciStar cj2Star rho CStar hdi hdj2 hci hcj2
  exact kEOneTenthRowSumBound
    (di * cj1Star + ciStar * dj1 + di * dj1)
    (di * cj2Star + ciStar * dj2 + di * dj2)
    a1 a2 (2 * rho * CStar + rho ^ 2) AD hd1 hd2 ha1 ha2

/-- Homogeneous centered-force gain inflation.  Crucially, the parameter-tube
correction retains the same state factor `S`; no additive bias is introduced. -/
theorem tubeGainInflation
    (r rStar K0 L rho S : ℝ)
    (hAnchor : |rStar| ≤ K0 * S)
    (hDrift : |r - rStar| ≤ L * rho * S) :
    |r| ≤ (K0 + L * rho) * S := by
  have hr : r = rStar + (r - rStar) := by ring
  calc
    |r| = |rStar + (r - rStar)| := by rw [hr]
    _ ≤ |rStar| + |r - rStar| := abs_add_le _ _
    _ ≤ K0 * S + L * rho * S := add_le_add hAnchor hDrift
    _ = (K0 + L * rho) * S := by ring

/-- Algebraic target step for a finite anchor cover: once the checker supplies
an envelope for `Keff` and a tube radius whose polynomial inflation is below
the remaining gain gap, the target gain follows strictly. -/
theorem finiteCoverGainTarget
    (Keff KAnchor C1 C2 rho KTarget : ℝ)
    (hEnvelope : Keff ≤ KAnchor + C1 * rho + C2 * rho ^ 2)
    (hTube : C1 * rho + C2 * rho ^ 2 < KTarget - KAnchor) :
    Keff < KTarget := by
  linarith

/-- A square-root-free sufficient reduction for the tube polynomial.  On a
unit-radius tube, a linear budget for `(C1+C2)*rho` controls
`C1*rho + C2*rho^2`.  This is useful when constructing rational covers. -/
theorem quadraticTubeCostLtOfUnitRadius
    (C1 C2 rho gap : ℝ)
    (hC1 : 0 ≤ C1)
    (hC2 : 0 ≤ C2)
    (hrho0 : 0 ≤ rho)
    (hrho1 : rho ≤ 1)
    (hLinear : (C1 + C2) * rho < gap) :
    C1 * rho + C2 * rho ^ 2 < gap := by
  have hsquare : rho ^ 2 ≤ rho := by nlinarith
  have hquad : C2 * rho ^ 2 ≤ C2 * rho :=
    mul_le_mul_of_nonneg_left hsquare hC2
  nlinarith

#print axioms outerProductIncrementIdentity
#print axioms outerProductEntryAbsBound
#print axioms outerProductEntryAbsBoundIsotropic
#print axioms twoComponentRowSumBound
#print axioms twoComponentScaledRowSumBound
#print axioms kEOneTenthRowSumBound
#print axioms kEOneTenthOuterProductRowBound
#print axioms tubeGainInflation
#print axioms finiteCoverGainTarget
#print axioms quadraticTubeCostLtOfUnitRadius

end RouteBP5ParameterTubeGain

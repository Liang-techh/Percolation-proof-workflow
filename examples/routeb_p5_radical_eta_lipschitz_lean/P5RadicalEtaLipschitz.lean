import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P5 radical eta-Lipschitz algebraic bridge

Source-independent Lean decomposition of the radical-free squared route from
`review-T-P5-056-honglianmozun-20260908T0100.md`.

The file deliberately represents square roots and reciprocal differences by a
small typed root packet (`r^2 = A`, nonnegative roots, and the exact reciprocal
relation) instead of importing source CSE, Float64, MVT/FTC, or deployed
coverage.  This isolates the checker-friendly polynomial core that current P5
squared-residual consumers can use once source constants are bound.
-/

set_option autoImplicit false

namespace RouteBP5RadicalEtaLipschitz

noncomputable section

/-- If nonnegative roots both have squared margin `m`, their product has margin `m`. -/
theorem root_product_margin
    (m r s : ℝ)
    (hm : 0 ≤ m) (hr : 0 ≤ r) (hs : 0 ≤ s)
    (hmr : m ≤ r ^ 2) (hms : m ≤ s ^ 2) :
    m ≤ r * s := by
  have hsq : m ^ 2 ≤ (r * s) ^ 2 := by
    calc
      m ^ 2 = m * m := by ring
      _ ≤ (r ^ 2) * (s ^ 2) := by
        exact mul_le_mul hmr hms hm (sq_nonneg r)
      _ = (r * s) ^ 2 := by ring
  have hrs : 0 ≤ r * s := mul_nonneg hr hs
  nlinarith

/-- Radical-free two-point square-root charge, expressed through exact root identities. -/
theorem sqrt_two_point_sq_from_roots
    (m r s A B : ℝ)
    (hm : 0 ≤ m) (hr : 0 ≤ r) (hs : 0 ≤ s)
    (hmr : m ≤ r ^ 2) (hms : m ≤ s ^ 2)
    (hrA : r ^ 2 = A) (hsB : s ^ 2 = B) :
    4 * m * (r - s) ^ 2 ≤ (A - B) ^ 2 := by
  have hmprod : m ≤ r * s :=
    root_product_margin m r s hm hr hs hmr hms
  have hfour : 4 * m ≤ (r + s) ^ 2 := by
    nlinarith [sq_nonneg (r - s)]
  have hmul :
      4 * m * (r - s) ^ 2 ≤ (r + s) ^ 2 * (r - s) ^ 2 := by
    exact mul_le_mul_of_nonneg_right hfour (sq_nonneg (r - s))
  calc
    4 * m * (r - s) ^ 2 ≤ (r + s) ^ 2 * (r - s) ^ 2 := hmul
    _ = (A - B) ^ 2 := by
      rw [← hrA, ← hsB]
      ring

/--
Transport a square-root difference charge to the reciprocal-root difference.
`h` is the exact reciprocal-difference packet satisfying `r*s*h = s-r`.
-/
theorem inverse_root_charge_from_relation
    (m r s h DA deta : ℝ)
    (hm : 0 ≤ m)
    (hmr : m ≤ r ^ 2) (hms : m ≤ s ^ 2)
    (hrel : r * s * h = s - r)
    (hroot : 4 * m * (r - s) ^ 2 ≤ DA ^ 2 * deta ^ 2) :
    4 * m ^ 3 * h ^ 2 ≤ DA ^ 2 * deta ^ 2 := by
  have hmsq : m ^ 2 ≤ (r * s) ^ 2 := by
    calc
      m ^ 2 = m * m := by ring
      _ ≤ (r ^ 2) * (s ^ 2) := by
        exact mul_le_mul hmr hms hm (sq_nonneg r)
      _ = (r * s) ^ 2 := by ring
  have hmul : m ^ 2 * h ^ 2 ≤ (r * s) ^ 2 * h ^ 2 :=
    mul_le_mul_of_nonneg_right hmsq (sq_nonneg h)
  have hcore : m ^ 2 * h ^ 2 ≤ (r - s) ^ 2 := by
    calc
      m ^ 2 * h ^ 2 ≤ (r * s) ^ 2 * h ^ 2 := hmul
      _ = (r * s * h) ^ 2 := by ring
      _ = (r - s) ^ 2 := by
        rw [hrel]
        ring
  have hscaled :
      (4 * m) * (m ^ 2 * h ^ 2) ≤ (4 * m) * (r - s) ^ 2 := by
    exact mul_le_mul_of_nonneg_left hcore (by positivity)
  calc
    4 * m ^ 3 * h ^ 2 = (4 * m) * (m ^ 2 * h ^ 2) := by ring
    _ ≤ (4 * m) * (r - s) ^ 2 := hscaled
    _ = 4 * m * (r - s) ^ 2 := by ring
    _ ≤ DA ^ 2 * deta ^ 2 := hroot

/-- Numerator variation divided by a root, encoded without division. -/
theorem numerator_over_root_charge
    (m r a dG DG deta : ℝ)
    (hmr : m ≤ r ^ 2)
    (hrel : r * a = dG)
    (hdG : dG ^ 2 ≤ DG ^ 2 * deta ^ 2) :
    m * a ^ 2 ≤ DG ^ 2 * deta ^ 2 := by
  calc
    m * a ^ 2 ≤ r ^ 2 * a ^ 2 :=
      mul_le_mul_of_nonneg_right hmr (sq_nonneg a)
    _ = (r * a) ^ 2 := by ring
    _ = dG ^ 2 := by rw [hrel]
    _ ≤ DG ^ 2 * deta ^ 2 := hdG

/-- Multiply an inverse-root charge by a bounded numerator amplitude. -/
theorem bias_inverse_root_charge
    (m h b G0 MG DA deta : ℝ)
    (hm : 0 ≤ m)
    (hrel : b = G0 * h)
    (hG : G0 ^ 2 ≤ MG ^ 2)
    (hinv : 4 * m ^ 3 * h ^ 2 ≤ DA ^ 2 * deta ^ 2) :
    4 * m ^ 3 * b ^ 2 ≤ MG ^ 2 * DA ^ 2 * deta ^ 2 := by
  have hcharge_nonneg : 0 ≤ 4 * m ^ 3 * h ^ 2 := by positivity
  have hAmp :
      G0 ^ 2 * (4 * m ^ 3 * h ^ 2) ≤
        MG ^ 2 * (4 * m ^ 3 * h ^ 2) :=
    mul_le_mul_of_nonneg_right hG hcharge_nonneg
  have hInvScaled :
      MG ^ 2 * (4 * m ^ 3 * h ^ 2) ≤
        MG ^ 2 * (DA ^ 2 * deta ^ 2) :=
    mul_le_mul_of_nonneg_left hinv (sq_nonneg MG)
  calc
    4 * m ^ 3 * b ^ 2 = G0 ^ 2 * (4 * m ^ 3 * h ^ 2) := by
      rw [hrel]
      ring
    _ ≤ MG ^ 2 * (4 * m ^ 3 * h ^ 2) := hAmp
    _ ≤ MG ^ 2 * (DA ^ 2 * deta ^ 2) := hInvScaled
    _ = MG ^ 2 * DA ^ 2 * deta ^ 2 := by ring

/-- Exact denominator-free Young identity for the fused two-term difference. -/
theorem weighted_two_term_square_identity
    (theta a b : ℝ) :
    (1 + theta) * (theta * a ^ 2 + b ^ 2) -
        theta * (a + b) ^ 2 =
      (theta * a - b) ^ 2 := by
  ring

/-- The corresponding weighted two-term square bound, valid for every real `theta`. -/
theorem weighted_two_term_square_bound
    (theta a b : ℝ) :
    theta * (a + b) ^ 2 ≤
      (1 + theta) * (theta * a ^ 2 + b ^ 2) := by
  have hid := weighted_two_term_square_identity theta a b
  nlinarith [sq_nonneg (theta * a - b)]

/--
Checker-friendly fused squared certificate from the two atomic charges.
This is the algebraic core of the review's radical-free normalized primitive.
-/
theorem normalized_radical_sq_from_atomic_charges
    (m theta a b DG MG DA deta : ℝ)
    (hm : 0 ≤ m) (htheta : 0 ≤ theta)
    (ha : m * a ^ 2 ≤ DG ^ 2 * deta ^ 2)
    (hb : 4 * m ^ 3 * b ^ 2 ≤ MG ^ 2 * DA ^ 2 * deta ^ 2) :
    4 * theta * m ^ 3 * (a + b) ^ 2 ≤
      (1 + theta) *
        (4 * theta * m ^ 2 * DG ^ 2 + MG ^ 2 * DA ^ 2) * deta ^ 2 := by
  have hw := weighted_two_term_square_bound theta a b
  have hscale : 0 ≤ 4 * m ^ 3 := by positivity
  have hwscaled :
      (4 * m ^ 3) * (theta * (a + b) ^ 2) ≤
        (4 * m ^ 3) * ((1 + theta) * (theta * a ^ 2 + b ^ 2)) :=
    mul_le_mul_of_nonneg_left hw hscale
  have ha' :
      4 * theta * m ^ 3 * a ^ 2 ≤
        4 * theta * m ^ 2 * DG ^ 2 * deta ^ 2 := by
    have hfac : 0 ≤ 4 * theta * m ^ 2 := by positivity
    have htmp := mul_le_mul_of_nonneg_left ha hfac
    calc
      4 * theta * m ^ 3 * a ^ 2 =
          (4 * theta * m ^ 2) * (m * a ^ 2) := by ring
      _ ≤ (4 * theta * m ^ 2) * (DG ^ 2 * deta ^ 2) := htmp
      _ = 4 * theta * m ^ 2 * DG ^ 2 * deta ^ 2 := by ring
  have hsum :
      4 * theta * m ^ 3 * a ^ 2 + 4 * m ^ 3 * b ^ 2 ≤
        4 * theta * m ^ 2 * DG ^ 2 * deta ^ 2 +
          MG ^ 2 * DA ^ 2 * deta ^ 2 :=
    add_le_add ha' hb
  have hone : 0 ≤ 1 + theta := by linarith
  have hsumscaled := mul_le_mul_of_nonneg_left hsum hone
  calc
    4 * theta * m ^ 3 * (a + b) ^ 2 =
        (4 * m ^ 3) * (theta * (a + b) ^ 2) := by ring
    _ ≤ (4 * m ^ 3) * ((1 + theta) * (theta * a ^ 2 + b ^ 2)) := hwscaled
    _ = (1 + theta) *
          (4 * theta * m ^ 3 * a ^ 2 + 4 * m ^ 3 * b ^ 2) := by ring
    _ ≤ (1 + theta) *
          (4 * theta * m ^ 2 * DG ^ 2 * deta ^ 2 +
            MG ^ 2 * DA ^ 2 * deta ^ 2) := hsumscaled
    _ = (1 + theta) *
          (4 * theta * m ^ 2 * DG ^ 2 + MG ^ 2 * DA ^ 2) * deta ^ 2 := by ring

/--
End-to-end polynomial root-packet consumer.  Source-side work only has to bind
this packet to its actual CSE nodes and exact variation/amplitude constants.
-/
theorem normalized_radical_sq_from_root_packet
    (m theta r s A B h a b uDiff dG G0 DG MG DA deta : ℝ)
    (hm : 0 ≤ m) (htheta : 0 ≤ theta)
    (hr : 0 ≤ r) (hs : 0 ≤ s)
    (hmr : m ≤ r ^ 2) (hms : m ≤ s ^ 2)
    (hrA : r ^ 2 = A) (hsB : s ^ 2 = B)
    (hA : (A - B) ^ 2 ≤ DA ^ 2 * deta ^ 2)
    (hrecip : r * s * h = s - r)
    (haRel : r * a = dG)
    (hdG : dG ^ 2 ≤ DG ^ 2 * deta ^ 2)
    (hbRel : b = G0 * h)
    (hG : G0 ^ 2 ≤ MG ^ 2)
    (hu : uDiff = a + b) :
    4 * theta * m ^ 3 * uDiff ^ 2 ≤
      (1 + theta) *
        (4 * theta * m ^ 2 * DG ^ 2 + MG ^ 2 * DA ^ 2) * deta ^ 2 := by
  have hsqrt : 4 * m * (r - s) ^ 2 ≤ (A - B) ^ 2 :=
    sqrt_two_point_sq_from_roots m r s A B hm hr hs hmr hms hrA hsB
  have hroot : 4 * m * (r - s) ^ 2 ≤ DA ^ 2 * deta ^ 2 :=
    le_trans hsqrt hA
  have hinv : 4 * m ^ 3 * h ^ 2 ≤ DA ^ 2 * deta ^ 2 :=
    inverse_root_charge_from_relation m r s h DA deta hm hmr hms hrecip hroot
  have haCharge : m * a ^ 2 ≤ DG ^ 2 * deta ^ 2 :=
    numerator_over_root_charge m r a dG DG deta hmr haRel hdG
  have hbCharge : 4 * m ^ 3 * b ^ 2 ≤ MG ^ 2 * DA ^ 2 * deta ^ 2 :=
    bias_inverse_root_charge m h b G0 MG DA deta hm hbRel hG hinv
  have hfused := normalized_radical_sq_from_atomic_charges
    m theta a b DG MG DA deta hm htheta haCharge hbCharge
  rw [hu]
  exact hfused

#print axioms RouteBP5RadicalEtaLipschitz.root_product_margin
#print axioms RouteBP5RadicalEtaLipschitz.sqrt_two_point_sq_from_roots
#print axioms RouteBP5RadicalEtaLipschitz.inverse_root_charge_from_relation
#print axioms RouteBP5RadicalEtaLipschitz.numerator_over_root_charge
#print axioms RouteBP5RadicalEtaLipschitz.bias_inverse_root_charge
#print axioms RouteBP5RadicalEtaLipschitz.weighted_two_term_square_identity
#print axioms RouteBP5RadicalEtaLipschitz.weighted_two_term_square_bound
#print axioms RouteBP5RadicalEtaLipschitz.normalized_radical_sq_from_atomic_charges
#print axioms RouteBP5RadicalEtaLipschitz.normalized_radical_sq_from_root_packet

end

end RouteBP5RadicalEtaLipschitz

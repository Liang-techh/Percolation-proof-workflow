import NEW_BODY6_SLICE_TAILMINORS20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_TAILINVERSE20260907

noncomputable section

open NEW_BODY6_SLICE_MASSTAIL_Core20260907 NEW_BODY6_SLICE_MASSTAIL_Source20260907
open NEW_BODY6_SLICE_VGRAM_Source20260907 NEW_BODY6_SLICE_TAILPSD20260907
open NEW_BODY6_SLICE_TAILMINORS20260907

/- UNCOMPILED: explicit reciprocal block only, ordered actual columns {3,4}.
   No Matrix.inv API, Schur-complement theorem or full-body inverse is claimed. -/
def inverseTail (z h m kappa : ℝ) : Fin 2 → Fin 2 → ℝ :=
  ![![1 / (kappa + m * h ^ 2 * Real.sin z ^ 2), 0],
    ![0, 1 / (kappa + m * h ^ 2)]]

def product2 (B C : Fin 2 → Fin 2 → ℝ) (i j : Fin 2) : ℝ :=
  ∑ t : Fin 2, B i t * C t j

def identity2 (i j : Fin 2) : ℝ := if i = j then 1 else 0

def action2 (B : Fin 2 → Fin 2 → ℝ) (x : Fin 2 → ℝ) (i : Fin 2) : ℝ :=
  ∑ j : Fin 2, B i j * x j

def inverseApply (z h m kappa : ℝ) (x : Fin 2 → ℝ) : Fin 2 → ℝ :=
  ![x 0 / (kappa + m * h ^ 2 * Real.sin z ^ 2),
    x 1 / (kappa + m * h ^ 2)]

/- Consume the existing positive order-one minors; do not reprove them. -/
theorem denominators_positive_attempt (z h m kappa : ℝ)
    (hk : 0 < kappa) (hm : 0 ≤ m) (hh : 0 ≤ h ^ 2) :
    0 < kappa + m * h ^ 2 * Real.sin z ^ 2 ∧ 0 < kappa + m * h ^ 2 := by
  have hp := tail_principal_positive_attempt z h m kappa hk hm hh
  constructor
  · simpa [explicitTail] using hp.1
  · simpa [explicitTail] using hp.2.1

theorem inverse_two_sided_attempt (z h m kappa : ℝ)
    (hk : 0 < kappa) (hm : 0 ≤ m) (hh : 0 ≤ h ^ 2) :
    (∀ i j, product2 (explicitTail z h m kappa) (inverseTail z h m kappa) i j = identity2 i j) ∧
    (∀ i j, product2 (inverseTail z h m kappa) (explicitTail z h m kappa) i j = identity2 i j) := by
  rcases denominators_positive_attempt z h m kappa hk hm hh with ⟨hp, hr⟩
  have hp0 := ne_of_gt hp
  have hr0 := ne_of_gt hr
  constructor <;> intro i j <;> fin_cases i <;> fin_cases j <;>
    norm_num [product2, identity2, explicitTail, inverseTail, Fin.sum_univ_succ,
      one_div, hp0, hr0]

theorem inverse_entries_nonnegative_attempt (z h m kappa : ℝ)
    (hk : 0 < kappa) (hm : 0 ≤ m) (hh : 0 ≤ h ^ 2) (i j : Fin 2) :
    0 ≤ inverseTail z h m kappa i j := by
  rcases denominators_positive_attempt z h m kappa hk hm hh with ⟨hp, hr⟩
  have hpInv : 0 ≤ (1 : ℝ) / (kappa + m * h ^ 2 * Real.sin z ^ 2) :=
    div_nonneg (by norm_num) (le_of_lt hp)
  have hrInv : 0 ≤ (1 : ℝ) / (kappa + m * h ^ 2) :=
    div_nonneg (by norm_num) (le_of_lt hr)
  fin_cases i <;> fin_cases j
  · simpa [inverseTail] using hpInv
  · norm_num [inverseTail]
  · norm_num [inverseTail]
  · simpa [inverseTail] using hrInv

/- Exact inverse action for arbitrary real right-hand sides, without sign
   assumptions on x. The solve identity below is the elimination interface. -/
theorem inverse_action_formula_attempt (z h m kappa : ℝ) (x : Fin 2 → ℝ) :
    action2 (inverseTail z h m kappa) x = inverseApply z h m kappa x := by
  funext i
  fin_cases i <;> norm_num [action2, inverseTail, inverseApply, Fin.sum_univ_succ] <;> ring

theorem inverse_solves_attempt (z h m kappa : ℝ)
    (hk : 0 < kappa) (hm : 0 ≤ m) (hh : 0 ≤ h ^ 2) (x : Fin 2 → ℝ) :
    action2 (explicitTail z h m kappa) (inverseApply z h m kappa x) = x := by
  rcases denominators_positive_attempt z h m kappa hk hm hh with ⟨hp, hr⟩
  have hp0 := ne_of_gt hp
  have hr0 := ne_of_gt hr
  funext i
  fin_cases i <;>
    norm_num [action2, explicitTail, inverseApply, Fin.sum_univ_succ, div_eq_mul_inv] <;>
    field_simp [hp0, hr0] <;> ring

/- Actual-source transfer retains center, actual weights, and all sign premises.
   h is fixed to the inherited physical offset only at this source seam. -/
theorem source_tail_inverse_interface_attempt (hc : CenterOffsetTarget)
    (m kappa : ℝ) (hw : SourceWeightsTarget m kappa)
    (hk : 0 < kappa) (hm : 0 ≤ m) (hh : 0 ≤ offset ^ 2) (q : Fin 6 → ℝ) :
    (∀ i j, product2 (sourceTail q) (inverseTail (q 4) offset m kappa) i j = identity2 i j) ∧
    (∀ i j, product2 (inverseTail (q 4) offset m kappa) (sourceTail q) i j = identity2 i j) ∧
    (∀ i j, 0 ≤ inverseTail (q 4) offset m kappa i j) ∧
    (∀ x, action2 (sourceTail q) (inverseApply (q 4) offset m kappa x) = x) := by
  rw [source_tail_eq_attempt hc m kappa hw q]
  have hi := inverse_two_sided_attempt (q 4) offset m kappa hk hm hh
  exact ⟨hi.1, hi.2, inverse_entries_nonnegative_attempt (q 4) offset m kappa hk hm hh,
    inverse_solves_attempt (q 4) offset m kappa hk hm hh⟩

/- No PSD/minimum/principal-minor rederivation; no eigenvalue, full-body,
   Fourier, coverage, compilation or registry admission claim. -/
end
end NEW_BODY6_SLICE_TAILINVERSE20260907

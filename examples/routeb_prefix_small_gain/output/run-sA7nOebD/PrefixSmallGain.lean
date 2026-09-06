import Mathlib.Tactic
import Mathlib.Analysis.Real.Sqrt

set_option autoImplicit false

namespace RouteBPrefixSmallGain

/- Scalar gates only. Continuity, first hitting time, integration and source
   estimates are proved/stated analytically in DERIVATION.md, not imported as
   axioms here. All analytic inequalities used below are explicit premises. -/

theorem amplitude_bound {X b k : ℝ}
    (hk : k < 1) (hfeedback : X ≤ b + k * X) :
    X ≤ b / (1 - k) := by
  apply (le_div_iff₀ (by linarith : 0 < 1 - k)).mpr
  nlinarith

theorem strict_margin {b k : ℝ}
    (hb : 0 ≤ b) (hk : k < 1) (hgate : b + k < 1) :
    0 ≤ b / (1 - k) ∧ b / (1 - k) < 1 := by
  have hd : 0 < 1 - k := by linarith
  constructor
  · exact div_nonneg hb hd.le
  · apply (div_lt_iff₀ hd).mpr
    linarith

theorem prefix_scalar_gate {X b k : ℝ}
    (hb : 0 ≤ b) (hk0 : 0 ≤ k) (hk : k < 1)
    (hgate : b + k < 1) (hfeedback : X ≤ b + k * X) :
    X ≤ b / (1 - k) ∧ X < 1 := by
  have hbound := amplitude_bound hk hfeedback
  have hmargin := strict_margin hb hk hgate
  have hden : 1 - k ≤ 1 := by linarith
  exact ⟨hbound, hbound.trans_lt hmargin.2⟩

/- Once continuity has passed the prefix bound to a proposed exit value,
   this scalar theorem rules that exit out. It does not prove continuity. -/
theorem first_exit_value_excluded {Xexit b k : ℝ}
    (hb : 0 ≤ b) (hk : k < 1) (hgate : b + k < 1)
    (hlimit : Xexit ≤ b / (1 - k)) : Xexit ≠ 1 := by
  exact ne_of_lt (hlimit.trans_lt (strict_margin hb hk hgate).2)

theorem sqrt_energy_gate {J b k : ℝ}
    (hJ0 : 0 ≤ J) (hb : 0 ≤ b) (hk0 : 0 ≤ k) (hk : k < 1)
    (hgate : b + k < 1)
    (hfeedback : Real.sqrt J ≤ b + k * Real.sqrt J) :
    J ≤ (b / (1 - k)) ^ 2 ∧ J < 1 := by
  have hs := prefix_scalar_gate hb hk0 hk hgate hfeedback
  have hsq := Real.sq_sqrt hJ0
  have hnonneg := Real.sqrt_nonneg J
  have hc := (strict_margin hb hk hgate).1
  constructor <;> nlinarith

/- Two genuinely distinct estimates: state response Y <= g X and nonlinear
   force R <= b0 + ell Y. The resolvent/error bound is X <= R + eps. -/
theorem compose_source_state_loop {X Y R b0 eps ell g : ℝ}
    (hell : 0 ≤ ell)
    (hstate : Y ≤ g * X)
    (hsource : R ≤ b0 + ell * Y)
    (hresolvent : X ≤ R + eps) :
    X ≤ (b0 + eps) + (ell * g) * X := by
  have hm := mul_le_mul_of_nonneg_left hstate hell
  nlinarith

theorem forcing_amplitude_gate {X b0 eps k : ℝ}
    (hb0 : 0 ≤ b0) (heps : 0 ≤ eps)
    (hk0 : 0 ≤ k) (hk : k < 1)
    (hgate : b0 + eps + k < 1)
    (hfeedback : X ≤ b0 + eps + k * X) :
    X ≤ (b0 + eps) / (1 - k) ∧ X < 1 := by
  exact prefix_scalar_gate (add_nonneg hb0 heps) hk0 hk hgate hfeedback

/- Eeta is a bound on integral eta' Q eta; its contribution is sqrt(Eeta),
   not Eeta. The hypothesis below admits any nonnegative outward root eps. -/
theorem forcing_energy_gate {J Eeta b0 eps k : ℝ}
    (hJ0 : 0 ≤ J) (hb0 : 0 ≤ b0) (heps : 0 ≤ eps)
    (hk0 : 0 ≤ k) (hk : k < 1)
    (hE : Eeta ≤ eps ^ 2) (hgate : b0 + eps + k < 1)
    (hfeedback : Real.sqrt J ≤ b0 + Real.sqrt Eeta + k * Real.sqrt J) :
    J ≤ ((b0 + eps) / (1 - k)) ^ 2 ∧ J < 1 := by
  have he := Real.sqrt_le_iff.mpr ⟨heps, hE⟩
  apply sqrt_energy_gate hJ0 (add_nonneg hb0 heps) hk0 hk hgate
  linarith

/- Per-cell alternative: F bounds the energy density, not an amplitude.
   The prefix integral inequality remains an explicit analytic premise. -/
theorem cell_initial_strict_gate {b F cap t0 t1 : ℝ}
    (hF : 0 ≤ F) (ht : t0 ≤ t1)
    (hgate : b + (t1 - t0) * F < cap) : b < cap := by
  have hp := mul_nonneg (sub_nonneg.mpr ht) hF
  linarith

theorem cell_prefix_strict_gate {J b F cap t t0 t1 : ℝ}
    (hF : 0 ≤ F) (ht : t ≤ t1)
    (hprefix : J ≤ b + (t - t0) * F)
    (hgate : b + (t1 - t0) * F < cap) :
    J ≤ b + (t1 - t0) * F ∧ J < cap := by
  have hp := mul_le_mul_of_nonneg_right (sub_le_sub_right ht t0) hF
  constructor <;> linarith

theorem cell_integral_strict_gate {J J0 I b F cap t t0 t1 : ℝ}
    (hF : 0 ≤ F) (ht : t ≤ t1) (hprevious : J0 ≤ b)
    (hsplit : J ≤ J0 + I) (hintegral : I ≤ (t - t0) * F)
    (hgate : b + (t1 - t0) * F < cap) :
    J ≤ b + (t1 - t0) * F ∧ J < cap := by
  apply cell_prefix_strict_gate hF ht (by linarith) hgate

/- Continuity supplies hlimit at the proposed first hit. No requirement to
   evaluate a nonlinear source estimate after its validity region is left. -/
theorem cell_first_exit_excluded {Jexit b F cap t0 t1 : ℝ}
    (hgate : b + (t1 - t0) * F < cap)
    (hlimit : Jexit ≤ b + (t1 - t0) * F) : Jexit ≠ cap := by
  exact ne_of_lt (hlimit.trans_lt hgate)

/- Exact arithmetic from the last passed cell (index 65) of the read-only
   run-20260905T200606Z-34dbb987 receipt. This verifies neither source F nor
   previous J, and does not assert that the next cell's gate is impossible. -/
theorem supplied_last_cell_arithmetic :
    (66 / 128 : ℝ) = 33 / 64 ∧
    (32377921103 / 250000000000 : ℝ) +
      (33 / 64 - 65 / 128) * (11304860080329 / 1000000000000) =
      (5576471137013 / 25600000000000 : ℝ) ∧
    (5576471137013 / 25600000000000 : ℝ) <
      (108921350211 / 500000000000 : ℝ) ∧
    (5576471137013 / 25600000000000 : ℝ) ≤
      (21783090379 / 100000000000 : ℝ) ∧
    (21783090379 / 100000000000 : ℝ) < 1 := by
  norm_num

/- These are the current bridge's rounded original-output formulas, conditional
   on an amplitude envelope c. No source-derived numerical b0 or k is asserted. -/
theorem original_output_envelopes {P T X c : ℝ}
    (hX0 : 0 ≤ X) (hX : X ≤ c) (hc : c ≤ 1)
    (hP : P ≤ ((43 / 100 : ℝ) + (9 / 5 : ℝ) * X) ^ 2)
    (hT : T ≤ ((13 / 20 : ℝ) + (14 / 5 : ℝ) * X) ^ 2) :
    P ≤ ((43 / 100 : ℝ) + (9 / 5 : ℝ) * c) ^ 2 ∧
    T ≤ ((13 / 20 : ℝ) + (14 / 5 : ℝ) * c) ^ 2 ∧
    P < (28 / 5 : ℝ) ∧ T < 12 := by
  have hc0 : 0 ≤ c := hX0.trans hX
  have hPmon : ((43 / 100 : ℝ) + (9 / 5 : ℝ) * X) ^ 2 ≤
      ((43 / 100 : ℝ) + (9 / 5 : ℝ) * c) ^ 2 := by nlinarith
  have hTmon : ((13 / 20 : ℝ) + (14 / 5 : ℝ) * X) ^ 2 ≤
      ((13 / 20 : ℝ) + (14 / 5 : ℝ) * c) ^ 2 := by nlinarith
  have hPcap : ((43 / 100 : ℝ) + (9 / 5 : ℝ) * c) ^ 2 ≤
      (223 / 100 : ℝ) ^ 2 := by nlinarith
  have hTcap : ((13 / 20 : ℝ) + (14 / 5 : ℝ) * c) ^ 2 ≤
      (69 / 20 : ℝ) ^ 2 := by nlinarith
  exact ⟨hP.trans hPmon, hT.trans hTmon,
    (hP.trans (hPmon.trans hPcap)).trans_lt (by norm_num),
    (hT.trans (hTmon.trans hTcap)).trans_lt (by norm_num)⟩

#print axioms amplitude_bound
#print axioms strict_margin
#print axioms prefix_scalar_gate
#print axioms first_exit_value_excluded
#print axioms sqrt_energy_gate
#print axioms compose_source_state_loop
#print axioms forcing_amplitude_gate
#print axioms forcing_energy_gate
#print axioms cell_initial_strict_gate
#print axioms cell_prefix_strict_gate
#print axioms cell_integral_strict_gate
#print axioms cell_first_exit_excluded
#print axioms supplied_last_cell_arithmetic
#print axioms original_output_envelopes

end RouteBPrefixSmallGain

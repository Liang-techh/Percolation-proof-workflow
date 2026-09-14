import Mathlib

namespace RouteBP5InvariantPathSheetCoverage

/-- One coordinate of the straight connector between two base states. -/
def affineCoord (s a b : ℝ) : ℝ := (1 - s) * a + s * b

/-- Scalar tangent-energy toy used only to keep the base-state/tangent-state
semantic boundary explicit. -/
def tangentEnergy1 (w xi : ℝ) : ℝ := w * xi ^ 2

/-- Algebraic vertical component of the smooth endpoint-only obstruction
`u' = 0`, `v' = 1-u^2`, starting from `v(0)=0`. -/
def endpointCounterV (u t : ℝ) : ℝ := t * (1 - u ^ 2)

/-- Re-centering commutes exactly with the affine connector. -/
theorem affine_center_identity (s x y c : ℝ) :
    affineCoord s x y - c = affineCoord s (x - c) (y - c) := by
  simp only [affineCoord]
  ring

/-- A coordinate interval is convex: if both centered endpoint coordinates have
absolute value at most `r`, every straight interpolation does too. -/
theorem affine_abs_le_of_endpoint_abs_le
    (r s a b : ℝ)
    (hs0 : 0 ≤ s) (hs1 : s ≤ 1)
    (ha : |a| ≤ r) (hb : |b| ≤ r) :
    |affineCoord s a b| ≤ r := by
  have h1s : 0 ≤ 1 - s := sub_nonneg.mpr hs1
  calc
    |affineCoord s a b|
        ≤ |(1 - s) * a| + |s * b| := by
          simpa only [affineCoord] using abs_add_le ((1 - s) * a) (s * b)
    _ = (1 - s) * |a| + s * |b| := by
          rw [abs_mul, abs_mul, abs_of_nonneg h1s, abs_of_nonneg hs0]
    _ ≤ (1 - s) * r + s * r :=
          add_le_add
            (mul_le_mul_of_nonneg_left ha h1s)
            (mul_le_mul_of_nonneg_left hb hs0)
    _ = r := by ring

/-- Finite-dimensional, pointwise version of straight-segment membership in an
axis-aligned inner box. -/
theorem straight_segment_mem_box
    {ι : Type*}
    (c r x y : ι → ℝ) (s : ℝ)
    (hs0 : 0 ≤ s) (hs1 : s ≤ 1)
    (hx : ∀ i, |x i - c i| ≤ r i)
    (hy : ∀ i, |y i - c i| ≤ r i) :
    ∀ i, |affineCoord s (x i) (y i) - c i| ≤ r i := by
  intro i
  rw [affine_center_identity]
  exact affine_abs_le_of_endpoint_abs_le
    (r i) s (x i - c i) (y i - c i) hs0 hs1 (hx i) (hy i)

/-- Pure Route-A margin consumer.  The analytic integration theorem is kept
outside this leaf: once it supplies `|x(t)-x(0)| ≤ t B`, the exact box margin
`r+hB≤H` closes the coordinate bound. -/
theorem outer_abs_of_inner_and_displacement
    (c x0 xt r H B t h : ℝ)
    (hinner : |x0 - c| ≤ r)
    (hdisp : |xt - x0| ≤ t * B)
    (hth : t ≤ h) (hB : 0 ≤ B)
    (hmargin : r + h * B ≤ H) :
    |xt - c| ≤ H := by
  have htb : t * B ≤ h * B := mul_le_mul_of_nonneg_right hth hB
  calc
    |xt - c| = |(xt - x0) + (x0 - c)| := by
      congr 1
      ring
    _ ≤ |xt - x0| + |x0 - c| := abs_add_le _ _
    _ ≤ t * B + r := add_le_add hdisp hinner
    _ ≤ h * B + r := by
      simpa [add_comm] using (add_le_add_right htb r)
    _ = r + h * B := by ring
    _ ≤ H := hmargin

/-- Coordinatewise Route-A consumer for a finite or infinite typed index set.
All ODE/calculus work is represented only by the displacement premise. -/
theorem pointwise_outer_box_of_inner_and_displacement
    {ι : Type*}
    (c x0 xt r H B : ι → ℝ) (t h : ℝ)
    (hinner : ∀ i, |x0 i - c i| ≤ r i)
    (hdisp : ∀ i, |xt i - x0 i| ≤ t * B i)
    (hth : t ≤ h)
    (hB : ∀ i, 0 ≤ B i)
    (hmargin : ∀ i, r i + h * B i ≤ H i) :
    ∀ i, |xt i - c i| ≤ H i := by
  intro i
  exact outer_abs_of_inner_and_displacement
    (c i) (x0 i) (xt i) (r i) (H i) (B i) t h
    (hinner i) (hdisp i) hth (hB i) (hmargin i)

/-- Radical-free speed producer: a square bound plus a nonnegative rational
candidate cap implies the corresponding absolute-value cap. -/
theorem abs_le_of_sq_le_aux_sq
    (x S B : ℝ)
    (hB : 0 ≤ B)
    (hxs : x ^ 2 ≤ S)
    (hSB : S ≤ B ^ 2) :
    |x| ≤ B := by
  have hs : x ^ 2 ≤ B ^ 2 := le_trans hxs hSB
  rw [abs_le]
  constructor
  · by_contra hnot
    have hxlt : x < -B := lt_of_not_ge hnot
    have h1 : x + B < 0 := by linarith
    have h2 : x - B < 0 := by linarith
    have hp : 0 < (x + B) * (x - B) := mul_pos_of_neg_of_neg h1 h2
    nlinarith
  · by_contra hnot
    have hxgt : B < x := lt_of_not_ge hnot
    have h1 : 0 < x - B := by linarith
    have h2 : 0 < x + B := by linarith
    have hp : 0 < (x - B) * (x + B) := mul_pos h1 h2
    nlinarith

/-- Pointwise square-only producer for component speed caps. -/
theorem pointwise_abs_speed_cap_of_square_packet
    {ι : Type*}
    (v S B : ι → ℝ)
    (hB : ∀ i, 0 ≤ B i)
    (hvs : ∀ i, (v i) ^ 2 ≤ S i)
    (hSB : ∀ i, S i ≤ (B i) ^ 2) :
    ∀ i, |v i| ≤ B i := by
  intro i
  exact abs_le_of_sq_le_aux_sq (v i) (S i) (B i) (hB i) (hvs i) (hSB i)

/-- Logically tiny final Route-A/Route-B sheet lift: if every initial path point
is in the invariant inner set, a pointwise forward-invariance theorem already
quantifies over the full continuum of path labels. -/
theorem flowed_path_sheet_mem_of_initial_path_mem_and_forward_invariant
    {ι τ X : Type*}
    (KIn KOut : X → Prop)
    (gamma0 : ι → X) (Phi : τ → X → X)
    (hinit : ∀ s, KIn (gamma0 s))
    (hinv : ∀ x, KIn x → ∀ t, KOut (Phi t x)) :
    ∀ t s, KOut (Phi t (gamma0 s)) := by
  intro t s
  exact hinv (gamma0 s) (hinit s) t

/-- Division-free Route-B algebra: the defect gate
`E ≤ nu^2 R_in` converts the base-storage differential packet into a shifted
one.  The integrating-factor/Gronwall step is intentionally a separate analytic
leaf. -/
theorem robust_storage_shift_deriv_algebra
    (nu Rin E U dU : ℝ)
    (hE : E ≤ nu ^ 2 * Rin)
    (hderiv : nu * dU ≤ -(nu ^ 2) * U + E) :
    nu * dU ≤ -(nu ^ 2) * (U - Rin) := by
  nlinarith

/-- The inner storage level sits strictly inside the outer certified collar. -/
theorem inner_level_strictly_inside_outer
    (U Rin Rout : ℝ)
    (hgap : Rin < Rout)
    (hinner : U ≤ Rin) :
    U < Rout := by
  exact lt_of_le_of_lt hinner hgap

/-- Shifted storage is nonpositive exactly on the inner sublevel. -/
theorem storage_shift_nonpos_iff
    (U Rin : ℝ) :
    U - Rin ≤ 0 ↔ U ≤ Rin := by
  constructor <;> intro h <;> linarith

/-- The endpoint-only obstruction has stationary vertical endpoint traces at
`u=±1`. -/
theorem endpoint_counter_endpoints_zero (t : ℝ) :
    endpointCounterV (-1) t = 0 ∧ endpointCounterV 1 t = 0 := by
  constructor <;> norm_num [endpointCounterV]

/-- The same obstruction sends the midpoint `u=0` to vertical coordinate `t`. -/
theorem endpoint_counter_midpoint (t : ℝ) :
    endpointCounterV 0 t = t := by
  simp [endpointCounterV]

/-- At horizon two the midpoint lies outside the unit vertical box even though
both endpoint vertical traces are zero. -/
theorem endpoint_counter_midpoint_exits_unit_box :
    ¬ |endpointCounterV 0 2| ≤ (1 : ℝ) := by
  norm_num [endpointCounterV]

/-- Zero tangent energy is available at every base point; this identity is why
a variational energy cannot by itself be used as a base-state tube witness. -/
theorem zero_tangent_energy_everywhere (w : ℝ) :
    tangentEnergy1 w 0 = 0 := by
  simp [tangentEnergy1]

/-- Concrete semantic regression: zero tangent energy coexists with a base point
strictly outside the unit state box. -/
theorem zero_tangent_energy_does_not_certify_base_box :
    tangentEnergy1 1 0 = 0 ∧ ¬ |(2 : ℝ)| ≤ 1 := by
  norm_num [tangentEnergy1]

#print axioms affine_center_identity
#print axioms affine_abs_le_of_endpoint_abs_le
#print axioms straight_segment_mem_box
#print axioms outer_abs_of_inner_and_displacement
#print axioms pointwise_outer_box_of_inner_and_displacement
#print axioms abs_le_of_sq_le_aux_sq
#print axioms pointwise_abs_speed_cap_of_square_packet
#print axioms flowed_path_sheet_mem_of_initial_path_mem_and_forward_invariant
#print axioms robust_storage_shift_deriv_algebra
#print axioms inner_level_strictly_inside_outer
#print axioms storage_shift_nonpos_iff
#print axioms endpoint_counter_endpoints_zero
#print axioms endpoint_counter_midpoint
#print axioms endpoint_counter_midpoint_exits_unit_box
#print axioms zero_tangent_energy_everywhere
#print axioms zero_tangent_energy_does_not_certify_base_box

end RouteBP5InvariantPathSheetCoverage

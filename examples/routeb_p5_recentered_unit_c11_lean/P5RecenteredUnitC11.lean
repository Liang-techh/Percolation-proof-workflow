import Mathlib

noncomputable section

namespace RouteBP5RecenteredUnitC11

open MeasureTheory Set
open intervalIntegral

/-- Canonical segment-average representation used by the recentered C1,1 bridge. -/
noncomputable def segmentAverage (g : ℝ → ℝ) (r x : ℝ) : ℝ :=
  ∫ t in (0 : ℝ)..1, g (r + t * (x - r))

/-- Canonical divided-difference unit with the derivative value inserted at the root. -/
noncomputable def recenteredUnit (h g : ℝ → ℝ) (r x : ℝ) : ℝ :=
  if x = r then g r else h x / (x - r)

/-- The segment argument difference is exactly scaled by the interpolation parameter. -/
theorem segment_argument_sub
    (r x y t : ℝ) :
    (r + t * (x - r)) - (r + t * (y - r)) = t * (x - y) := by
  ring

/-- Absolute segment separation for nonnegative interpolation parameter. -/
theorem abs_segment_argument_sub
    (r x y t : ℝ)
    (ht : 0 ≤ t) :
    abs ((r + t * (x - r)) - (r + t * (y - r))) = t * abs (x - y) := by
  rw [segment_argument_sub, abs_mul, abs_of_nonneg ht]

/-- The segment average at the root is the root value. -/
theorem segmentAverage_at_root
    (g : ℝ → ℝ) (r : ℝ) :
    segmentAverage g r r = g r := by
  simp [segmentAverage]

/-- Multiplication by a fixed sign commutes exactly with the segment average. -/
theorem sigma_mul_segmentAverage
    (sigma : ℝ) (g : ℝ → ℝ) (r x : ℝ) :
    sigma * segmentAverage g r x =
      segmentAverage (fun z => sigma * g z) r x := by
  simp [segmentAverage, intervalIntegral.integral_const_mul]

/-- Pointwise lower/upper bounds are preserved by the unit-interval segment average. -/
theorem segment_average_bounds
    (g : ℝ → ℝ) (r x lo hi : ℝ)
    (hint : IntervalIntegrable (fun t : ℝ => g (r + t * (x - r))) volume 0 1)
    (hlo : ∀ t ∈ Set.Icc (0 : ℝ) 1, lo ≤ g (r + t * (x - r)))
    (hhi : ∀ t ∈ Set.Icc (0 : ℝ) 1, g (r + t * (x - r)) ≤ hi) :
    lo ≤ segmentAverage g r x ∧ segmentAverage g r x ≤ hi := by
  constructor
  · have h := intervalIntegral.integral_mono_on
      (f := fun _ : ℝ => lo) (g := fun t : ℝ => g (r + t * (x - r)))
      zero_le_one intervalIntegrable_const hint hlo
    simpa [segmentAverage] using h
  · have h := intervalIntegral.integral_mono_on
      (f := fun t : ℝ => g (r + t * (x - r))) (g := fun _ : ℝ => hi)
      zero_le_one hint intervalIntegrable_const hhi
    simpa [segmentAverage] using h

/-- Signed derivative amplitude bounds pass to the averaged recentered unit without loss. -/
theorem segment_average_signed_bounds
    (sigma : ℝ) (g : ℝ → ℝ) (r x mu M : ℝ)
    (hint : IntervalIntegrable
      (fun t : ℝ => sigma * g (r + t * (x - r))) volume 0 1)
    (hlower : ∀ t ∈ Set.Icc (0 : ℝ) 1,
      mu ≤ sigma * g (r + t * (x - r)))
    (hupper : ∀ t ∈ Set.Icc (0 : ℝ) 1,
      sigma * g (r + t * (x - r)) ≤ M) :
    mu ≤ sigma * segmentAverage g r x ∧
      sigma * segmentAverage g r x ≤ M := by
  have hbounds := segment_average_bounds
    (fun z => sigma * g z) r x mu M hint hlower hupper
  simpa [sigma_mul_segmentAverage] using hbounds

/--
Sharp C1,1 transport for the averaged derivative.  The conclusion is stored in
multiplication-only form: `2 |Δv| ≤ L2 |Δx|`.
-/
theorem segment_average_lipschitz_twice
    (g : ℝ → ℝ) (r x y L2 : ℝ)
    (hL2 : 0 ≤ L2)
    (hx : IntervalIntegrable (fun t : ℝ => g (r + t * (x - r))) volume 0 1)
    (hy : IntervalIntegrable (fun t : ℝ => g (r + t * (y - r))) volume 0 1)
    (hlip : ∀ a b : ℝ, abs (g a - g b) ≤ L2 * abs (a - b)) :
    2 * abs (segmentAverage g r x - segmentAverage g r y) ≤
      L2 * abs (x - y) := by
  have hboundInt : IntervalIntegrable
      (fun t : ℝ => L2 * t * abs (x - y)) volume 0 1 :=
    Continuous.intervalIntegrable (by fun_prop) 0 1
  have hnorm :
      abs (∫ t in (0 : ℝ)..1,
        (g (r + t * (x - r)) - g (r + t * (y - r)))) ≤
        ∫ t in (0 : ℝ)..1, L2 * t * abs (x - y) := by
    simpa [Real.norm_eq_abs] using
      (intervalIntegral.norm_integral_le_of_norm_le zero_le_one
        (show ∀ᵐ t ∂MeasureTheory.volume.restrict (Set.uIoc (0 : ℝ) 1),
            ‖g (r + t * (x - r)) - g (r + t * (y - r))‖ ≤
              L2 * t * abs (x - y) by
          filter_upwards with t ht
          have ht0 : 0 ≤ t := ht.1.le
          calc
            ‖g (r + t * (x - r)) - g (r + t * (y - r))‖ =
                abs (g (r + t * (x - r)) - g (r + t * (y - r))) := by
                  rw [Real.norm_eq_abs]
            _ ≤ L2 * abs ((r + t * (x - r)) - (r + t * (y - r))) :=
              hlip _ _
            _ = L2 * (t * abs (x - y)) := by
              rw [abs_segment_argument_sub r x y t ht0]
            _ = L2 * t * abs (x - y) := by ring)
        hboundInt)
  have hdiff :
      segmentAverage g r x - segmentAverage g r y =
        ∫ t in (0 : ℝ)..1,
          (g (r + t * (x - r)) - g (r + t * (y - r))) := by
    simp only [segmentAverage]
    rw [intervalIntegral.integral_sub hx hy]
  have hlinear :
      (∫ t in (0 : ℝ)..1, L2 * t * abs (x - y)) =
        L2 * abs (x - y) / 2 := by
    calc
      (∫ t in (0 : ℝ)..1, L2 * t * abs (x - y)) =
          ∫ t in (0 : ℝ)..1, t ^ (1 : ℕ) * (L2 * abs (x - y)) := by
            congr 1
            funext t
            ring
      _ = (∫ t in (0 : ℝ)..1, t ^ (1 : ℕ)) * (L2 * abs (x - y)) := by
            rw [intervalIntegral.integral_mul_const]
      _ = L2 * abs (x - y) / 2 := by
            rw [integral_pow]
            ring
  rw [← hdiff] at hnorm
  rw [hlinear] at hnorm
  nlinarith [abs_nonneg (segmentAverage g r x - segmentAverage g r y),
    mul_nonneg hL2 (abs_nonneg (x - y))]

/-- Exact factorization of the canonical divided-difference unit, including the root. -/
theorem recentered_unit_exact_factorization
    (h g : ℝ → ℝ) (r x : ℝ)
    (hroot : h r = 0) :
    h x = (x - r) * recenteredUnit h g r x := by
  by_cases hx : x = r
  · subst x
    simp [recenteredUnit, hroot]
  · rw [recenteredUnit, if_neg hx]
    field_simp [sub_ne_zero.mpr hx]

/--
Minimal FTC seam: once a caller supplies the segment increment identity, the
piecewise divided difference is exactly the canonical segment average.
-/
theorem recentered_unit_eq_segmentAverage_of_increment
    (h g : ℝ → ℝ) (r x : ℝ)
    (hroot : h r = 0)
    (hincrement : h x = (x - r) * segmentAverage g r x) :
    recenteredUnit h g r x = segmentAverage g r x := by
  by_cases hx : x = r
  · subst x
    simp [recenteredUnit, segmentAverage_at_root]
  · rw [recenteredUnit, if_neg hx]
    apply (div_eq_iff (sub_ne_zero.mpr hx)).2
    simpa [mul_comm] using hincrement

/-- Division-free conversion of the T-P5-066 root-graph packet into a chosen rational slope. -/
theorem root_graph_division_free_to_lipschitz
    (mu Lp Lr d r1 r2 : ℝ)
    (hmu : 0 < mu)
    (hd : 0 ≤ d)
    (hroot : mu * abs (r1 - r2) ≤ Lp * d)
    (hchoice : Lp ≤ mu * Lr) :
    abs (r1 - r2) ≤ Lr * d := by
  apply (mul_le_mul_left hmu).mp
  calc
    mu * abs (r1 - r2) ≤ Lp * d := hroot
    _ ≤ (mu * Lr) * d := mul_le_mul_of_nonneg_right hchoice hd
    _ = mu * (Lr * d) := by ring

/-- Pointwise triangular-chart distance estimate before averaging. -/
theorem parameterized_segment_argument_bound
    (r1 r2 xi1 xi2 Lr d t : ℝ)
    (ht : 0 ≤ t)
    (hr : abs (r1 - r2) ≤ Lr * d) :
    abs ((r1 + t * xi1) - (r2 + t * xi2)) ≤
      Lr * d + t * abs (xi1 - xi2) := by
  have htri :
      abs ((r1 - r2) + t * (xi1 - xi2)) ≤
        abs (r1 - r2) + abs (t * (xi1 - xi2)) :=
    abs_add_le (r1 - r2) (t * (xi1 - xi2))
  calc
    abs ((r1 + t * xi1) - (r2 + t * xi2)) =
        abs ((r1 - r2) + t * (xi1 - xi2)) := by
          congr 1
          ring
    _ ≤ abs (r1 - r2) + abs (t * (xi1 - xi2)) := htri
    _ = abs (r1 - r2) + t * abs (xi1 - xi2) := by
          rw [abs_mul, abs_of_nonneg ht]
    _ ≤ Lr * d + t * abs (xi1 - xi2) := by linarith

/-- Quadratic family attaining the factor `1/2` exactly. -/
theorem sharp_half_quadratic_regression
    (a L2 x y : ℝ) :
    ((a + (L2 / 2) * x) - (a + (L2 / 2) * y)) =
      (L2 / 2) * (x - y) := by
  ring

#print axioms segment_argument_sub
#print axioms abs_segment_argument_sub
#print axioms segmentAverage_at_root
#print axioms sigma_mul_segmentAverage
#print axioms segment_average_bounds
#print axioms segment_average_signed_bounds
#print axioms segment_average_lipschitz_twice
#print axioms recentered_unit_exact_factorization
#print axioms recentered_unit_eq_segmentAverage_of_increment
#print axioms root_graph_division_free_to_lipschitz
#print axioms parameterized_segment_argument_bound
#print axioms sharp_half_quadratic_regression

end RouteBP5RecenteredUnitC11

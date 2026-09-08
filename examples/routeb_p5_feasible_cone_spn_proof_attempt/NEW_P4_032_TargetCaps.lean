import NEW_P4_032_GrowthEnvelopeBinding

/-!
OPEN_UNCOMPILED / pending. Distinct exact domain inclusions: full ellipsoid,
coercive full energy, and local boxes. No target-source equality or coverage
is inferred from a label. Saved block storage has a separate counterexample.
-/
set_option autoImplicit false

namespace RouteBP4032TargetCaps

open RouteBP4032BlockDefects RouteBP4032DescriptorPUpper
open scoped BigOperators

noncomputable section

structure State where
  q velocity : Vec6
  disturbance time : ℝ

structure GrowthCaps (x : State) : Prop where
  q_cap : ∀ j, |x.q j| ≤ 5 / 2
  velocity_cap : ∀ j, |x.velocity j| ≤ 15
  disturbance_cap : |x.disturbance| ≤ 2

def fullP (x : State) : ℝ := (3 / 2) * fullSq x.q + (4 / 5) * fullSq x.velocity

theorem component_square_le (v : Vec6) (j : Fin 6) : v j ^ 2 ≤ fullSq v := by
  exact Finset.single_le_sum (fun k _ => sq_nonneg (v k)) (Finset.mem_univ j)

theorem abs_cap_of_square (z cap : ℝ) (hc : 0 ≤ cap) (hz : z^2 ≤ cap^2) :
    |z| ≤ cap := by
  by_contra hn
  have hgt : cap < |z| := lt_of_not_ge hn
  have hp : 0 < (|z| - cap) * (|z| + cap) :=
    mul_pos (sub_pos.mpr hgt) (by linarith)
  nlinarith [sq_abs z]

/-- The coverage driver's FULL six-coordinate ellipsoid, not p45. -/
theorem full_ellipsoid_caps (x : State) (hp : fullP x ≤ 28 / 5)
    (hw : x.disturbance^2 ≤ 3) : GrowthCaps x := by
  have hq0 : 0 ≤ fullSq x.q := Finset.sum_nonneg (fun j _ => sq_nonneg _)
  have hv0 : 0 ≤ fullSq x.velocity := Finset.sum_nonneg (fun j _ => sq_nonneg _)
  unfold fullP at hp
  constructor
  · intro j
    apply abs_cap_of_square _ _ (by norm_num)
    have hj := component_square_le x.q j
    nlinarith
  · intro j
    apply abs_cap_of_square _ _ (by norm_num)
    have hj := component_square_le x.velocity j
    nlinarith
  · apply abs_cap_of_square _ _ (by norm_num)
    nlinarith

/-- V is supplied with TWO full-state lower inequalities. V<=1 alone is
insufficient, and energy does not bound the external disturbance. -/
theorem coercive_energy_caps (x : State) (V : ℝ) (hV : V ≤ 1)
    (hq : (1 / 5) * fullSq x.q ≤ V)
    (hv : (9401 / 2000000) * fullSq x.velocity ≤ V)
    (hw : x.disturbance^2 ≤ 3) : GrowthCaps x := by
  constructor
  · intro j
    apply abs_cap_of_square _ _ (by norm_num)
    have hj := component_square_le x.q j
    nlinarith
  · intro j
    apply abs_cap_of_square _ _ (by norm_num)
    have hj := component_square_le x.velocity j
    nlinarith
  · apply abs_cap_of_square _ _ (by norm_num)
    nlinarith

theorem box_caps (x : State) (qr vr : Vec6)
    (hq : ∀ j, |x.q j| ≤ qr j) (hv : ∀ j, |x.velocity j| ≤ vr j)
    (hqr : ∀ j, qr j ≤ 5 / 2) (hvr : ∀ j, vr j ≤ 15)
    (hw : |x.disturbance| ≤ 2) : GrowthCaps x :=
  ⟨fun j => (hq j).trans (hqr j), fun j => (hv j).trans (hvr j), hw⟩

theorem ramp_disturbance_cap (c t : ℝ) (hc : c^2 ≤ 3) (ht0 : 0 ≤ t)
    (ht1 : t ≤ 1) : (c * t)^2 ≤ 3 := by
  have ht : t^2 ≤ 1 := by nlinarith
  have h := mul_le_mul_of_nonneg_left ht (sq_nonneg c)
  nlinarith [sq_nonneg c]

/-- A same-source embedding still must supply the full-domain inclusion.
Additional cell restrictions are harmless; no cover is asserted. -/
theorem target_cell_caps {X ι : Type*} (D : X → Prop) (cell : ι → X → Prop)
    (embed : X → State)
    (hp : ∀ i x, D x → cell i x → fullP (embed x) ≤ 28 / 5)
    (hw : ∀ i x, D x → cell i x → (embed x).disturbance^2 ≤ 3) :
    ∀ i x, D x → cell i x → GrowthCaps (embed x) := by
  intro i x hx hi
  exact full_ellipsoid_caps (embed x) (hp i x hx hi) (hw i x hx hi)

def savedAt (V : (Fin 4 → ℝ) → ℝ → ℝ) (x : State) : ℝ :=
  V ![x.q 3, x.q 4, x.velocity 3, x.velocity 4] x.time

def remotePoint : State where
  q := fun j => if j = 0 then 3 else 0
  velocity := fun j => if j = 0 then 16 else 0
  disturbance := 0
  time := 0

/-- This is conditional on the exact CSV origin-value transcription; it is
not a Lean CSV import or a claim that remotePoint is on a reachable flow. -/
theorem saved_storage_counterexample (V : (Fin 4 → ℝ) → ℝ → ℝ)
    (hzero : V ![0, 0, 0, 0] 0 = -(5852960231758441 / 50000000000000000 : ℝ)) :
    savedAt V remotePoint ≤ 0 ∧ ¬ GrowthCaps remotePoint := by
  constructor
  · simpa [savedAt, remotePoint, hzero] using
      (show -(5852960231758441 / 50000000000000000 : ℝ) ≤ 0 by norm_num)
  · intro h
    have hq := h.q_cap 0
    norm_num [remotePoint] at hq

end
end RouteBP4032TargetCaps

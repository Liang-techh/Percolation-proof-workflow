import NEW_P4_032_TargetCaps

/-!
OPEN_UNCOMPILED. Target-cell and evaluation-stencil inclusion candidates.
No Lean/Lake execution, source authentication, trajectory or coverage claim.
All source/target/cell predicates are supplied explicitly; old files unchanged.
-/
set_option autoImplicit false

namespace RouteBP4032TargetCellInclusion20260908

open RouteBP4032TargetCaps RouteBP4032DescriptorPUpper RouteBP4032BlockDefects
open scoped BigOperators

noncomputable section

/-- Extra slack available from the full ellipsoid, before relaxing to GrowthCaps. -/
theorem full_ellipsoid_tight_caps (x : State) (hp : fullP x ≤ 28 / 5) :
    (∀ j, |x.q j| ≤ 2) ∧ (∀ j, |x.velocity j| ≤ 3) := by
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

def perturbAngles (x : State) (delta : Vec6) : State :=
  { x with q := fun j => x.q j + delta j }

/-- Includes every segment q+s*e_k, |s|<=h, if h<=1/2.
This does NOT put the perturbed point back in the original ellipsoid. -/
theorem full_ellipsoid_stencil_caps (x : State) (delta : Vec6)
    (hp : fullP x ≤ 28 / 5) (hw : x.disturbance^2 ≤ 3)
    (hd : ∀ j, |delta j| ≤ 1 / 2) : GrowthCaps (perturbAngles x delta) := by
  have ht := full_ellipsoid_tight_caps x hp
  have hc := full_ellipsoid_caps x hp hw
  constructor
  · intro j
    change |x.q j + delta j| ≤ 5 / 2
    have ha := abs_add (x.q j) (delta j)
    have hq := ht.1 j
    have he := hd j
    linarith
  · exact hc.velocity_cap
  · exact hc.disturbance_cap

theorem centered_coordinate_cap (z center radius cap : ℝ)
    (hz : |z - center| ≤ radius) (hr : |center| + radius ≤ cap) : |z| ≤ cap := by
  have heq : z = (z - center) + center := by ring
  calc
    |z| = |(z - center) + center| := congrArg abs heq
    _ ≤ |z - center| + |center| := abs_add _ _
    _ ≤ cap := by linarith

/-- Center offsets count. A radius-only test is valid only at center zero.
The q budget includes the whole finite-difference segment, not only its center. -/
theorem centered_box_stencil_caps (x : State) (qc vc qr vr delta : Vec6) (h : ℝ)
    (hq : ∀ j, |x.q j - qc j| ≤ qr j)
    (hv : ∀ j, |x.velocity j - vc j| ≤ vr j)
    (hqr : ∀ j, |qc j| + qr j + h ≤ 5 / 2)
    (hvr : ∀ j, |vc j| + vr j ≤ 15)
    (hd : ∀ j, |delta j| ≤ h) (hw : |x.disturbance| ≤ 2) :
    GrowthCaps (perturbAngles x delta) := by
  constructor
  · intro j
    change |x.q j + delta j| ≤ 5 / 2
    have hqj : |x.q j| ≤ |qc j| + qr j :=
      centered_coordinate_cap _ _ _ _ (hq j) (le_refl _)
    have ha := abs_add (x.q j) (delta j)
    have hdj := hd j
    have hrj := hqr j
    linarith
  · intro j
    exact centered_coordinate_cap _ _ _ _ (hv j) (hvr j)
  · exact hw

/-- These are authoritative-coordinate accessor slots, not a source-hash certificate. -/
structure RampCoordinates (X : Type*) where
  q velocity : X → Vec6
  amplitude time : X → ℝ

def rampState {X : Type*} (c : RampCoordinates X) (x : X) : State :=
  ⟨c.q x, c.velocity x, c.amplitude x * c.time x, c.time x⟩

/-- Pull back one explicit cover to one coordinate map. Coverage is required,
not manufactured by adding an ellipsoid restriction to the target domain. -/
theorem covered_ramp_target_caps {X I : Type*} (c : RampCoordinates X)
    (D : X → Prop) (cell : I → X → Prop)
    (cover : ∀ x, D x → ∃ i, cell i x)
    (hp : ∀ i x, D x → cell i x → fullP (rampState c x) ≤ 28 / 5)
    (hc : ∀ x, D x → (c.amplitude x)^2 ≤ 3)
    (ht0 : ∀ x, D x → 0 ≤ c.time x) (ht1 : ∀ x, D x → c.time x ≤ 1) :
    ∀ x, D x → ∃ i, cell i x ∧ GrowthCaps (rampState c x) ∧
      ∀ delta : Vec6, (∀ j, |delta j| ≤ 1 / 2) →
        GrowthCaps (perturbAngles (rampState c x) delta) := by
  intro x hx
  obtain ⟨i, hi⟩ := cover x hx
  have hw : (rampState c x).disturbance^2 ≤ 3 :=
    ramp_disturbance_cap (c.amplitude x) (c.time x) (hc x hx) (ht0 x hx) (ht1 x hx)
  refine ⟨i, hi, full_ellipsoid_caps _ (hp i x hx hi) hw, ?_⟩
  intro delta hd
  exact full_ellipsoid_stencil_caps _ delta (hp i x hx hi) hw hd

theorem ramp_outer_interval (c t u : ℝ) (hu : 0 ≤ u) (hu2 : 3 ≤ u^2)
    (hc : c^2 ≤ 3) (ht0 : 0 ≤ t) (ht1 : t ≤ 1) : |c * t| ≤ u := by
  exact abs_cap_of_square _ _ hu
    ((ramp_disturbance_cap c t hc ht0 ht1).trans hu2)

def boundaryState : State := ⟨0, ![2, 1, 1, 1, 0, 0], 0, 0⟩

/-- Exact rational boundary point: p_full=28/5. Any nonzero FD step exits it.
This is an evaluation-domain obstruction, not a physical trajectory. -/
theorem ellipsoid_not_stencil_closed (s : ℝ) (hs : s ≠ 0) :
    fullP boundaryState = 28 / 5 ∧
      28 / 5 < fullP (perturbAngles boundaryState (fun j => if j = 0 then s else 0)) := by
  constructor
  · norm_num [fullP, fullSq, boundaryState, Fin.sum_univ_succ]
  · have hs2 : 0 < s^2 := sq_pos_of_ne_zero hs
    norm_num [fullP, fullSq, boundaryState, perturbAngles, Fin.sum_univ_succ]
    nlinarith

def outsideSmallBoxes : State := ⟨fun j => if j = 0 then 1 else 0, 0, 0, 0⟩

/-- Any bank with first-angle absolute cap <=7/20 misses a point of the
full ellipsoid. This does not refute a separate reachable-set inclusion. -/
theorem small_boxes_do_not_cover_full_ellipsoid {I : Type*} (cell : I → State → Prop)
    (hbox : ∀ i x, cell i x → |x.q 0| ≤ 7 / 20) :
    fullP outsideSmallBoxes ≤ 28 / 5 ∧ ∀ i, ¬cell i outsideSmallBoxes := by
  constructor
  · norm_num [fullP, fullSq, outsideSmallBoxes, Fin.sum_univ_succ]
  · intro i hi
    have hb := hbox i outsideSmallBoxes hi
    norm_num [outsideSmallBoxes] at hb

/-- Conditional endpoint diagnostic. No identification with an executed
Julia sqrt result is claimed. This exact dyadic cutoff is too small. -/
def dyadicCutoff : ℝ := 3900231685776981 / 2251799813685248

theorem undersized_disturbance_root :
    ∃ c : ℝ, c^2 ≤ 3 ∧ dyadicCutoff < c := by
  refine ⟨31201853486215849 / 18014398509481984, ?_, ?_⟩ <;>
    norm_num [dyadicCutoff]

end
end RouteBP4032TargetCellInclusion20260908

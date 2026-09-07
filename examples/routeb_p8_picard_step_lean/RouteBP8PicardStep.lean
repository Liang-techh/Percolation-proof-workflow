import Mathlib.Data.Fin.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

/-!
# P8: one full-X0/ramp Picard step

This is a small, exact-real interface for the next Route-B flowpipe leaf.  It
does not define the deployed Julia RHS.  Instead, a concrete RHS must later
provide the explicitly named interval and ramp premises below.

The coordinate order is
`q₁ … q₆, dq₁ … dq₆, w, c`, hence the lifted state is genuinely 14
dimensional.  The proofs in this file are order-theoretic; no sampled or
floating-point probe is used as evidence.
-/

namespace RouteBP8PicardStep

noncomputable section

set_option autoImplicit false

abbrev State14 := Fin 14 → ℝ
abbrev BaseState12 := Fin 12 → ℝ
abbrev VectorField := State14 → State14

def qSlot (i : Fin 6) : Fin 14 := ⟨i.val, by omega⟩

def dqSlot (i : Fin 6) : Fin 14 := ⟨6 + i.val, by omega⟩

def wSlot : Fin 14 := 12

def cSlot : Fin 14 := 13

def rampLift (x : BaseState12) (c t : ℝ) : State14 := fun i =>
  match i.val with
  | 0 => x ⟨0, by omega⟩
  | 1 => x ⟨1, by omega⟩
  | 2 => x ⟨2, by omega⟩
  | 3 => x ⟨3, by omega⟩
  | 4 => x ⟨4, by omega⟩
  | 5 => x ⟨5, by omega⟩
  | 6 => x ⟨6, by omega⟩
  | 7 => x ⟨7, by omega⟩
  | 8 => x ⟨8, by omega⟩
  | 9 => x ⟨9, by omega⟩
  | 10 => x ⟨10, by omega⟩
  | 11 => x ⟨11, by omega⟩
  | 12 => c * t
  | 13 => c
  | _ => 0

theorem rampLift_w (x : BaseState12) (c t : ℝ) :
    rampLift x c t wSlot = c * t := by
  rfl

theorem rampLift_c (x : BaseState12) (c t : ℝ) :
    rampLift x c t cSlot = c := by
  rfl

def mechanicalEnergy (z : State14) : ℝ :=
  ∑ i : Fin 6, ((z (qSlot i)) ^ 2 + (z (dqSlot i)) ^ 2)

/- The exact full initial contract used by the Route-B flowpipe obligation. -/
def FullX0 (z : State14) : Prop :=
  mechanicalEnergy z ≤ (9 : ℝ) / 400 ∧
    z wSlot = 0 ∧
    (z cSlot) ^ 2 ≤ 3

def InitialBox (z : State14) : Prop :=
  (∀ i : Fin 6, -(3 : ℝ) / 20 ≤ z (qSlot i) ∧ z (qSlot i) ≤ 3 / 20) ∧
    (∀ i : Fin 6, -(3 : ℝ) / 20 ≤ z (dqSlot i) ∧ z (dqSlot i) ≤ 3 / 20) ∧
    z wSlot = 0 ∧
    -(2 : ℝ) ≤ z cSlot ∧ z cSlot ≤ 2

lemma q_term_le_energy (z : State14) (i : Fin 6) :
    (z (qSlot i)) ^ 2 ≤ mechanicalEnergy z := by
  classical
  unfold mechanicalEnergy
  calc
    (z (qSlot i)) ^ 2 ≤
        (z (qSlot i)) ^ 2 + (z (dqSlot i)) ^ 2 := by
          nlinarith [sq_nonneg (z (dqSlot i))]
    _ ≤ ∑ j : Fin 6, ((z (qSlot j)) ^ 2 + (z (dqSlot j)) ^ 2) := by
      have hs := Finset.single_le_sum
        (s := (Finset.univ : Finset (Fin 6)))
        (f := fun j : Fin 6 => (z (qSlot j)) ^ 2 + (z (dqSlot j)) ^ 2)
        (a := i) (by
          intro j hj
          positivity) (Finset.mem_univ i)
      simpa using hs

lemma dq_term_le_energy (z : State14) (i : Fin 6) :
    (z (dqSlot i)) ^ 2 ≤ mechanicalEnergy z := by
  classical
  unfold mechanicalEnergy
  calc
    (z (dqSlot i)) ^ 2 ≤
        (z (qSlot i)) ^ 2 + (z (dqSlot i)) ^ 2 := by
          nlinarith [sq_nonneg (z (qSlot i))]
    _ ≤ ∑ j : Fin 6, ((z (qSlot j)) ^ 2 + (z (dqSlot j)) ^ 2) := by
      have hs := Finset.single_le_sum
        (s := (Finset.univ : Finset (Fin 6)))
        (f := fun j : Fin 6 => (z (qSlot j)) ^ 2 + (z (dqSlot j)) ^ 2)
        (a := i) (by
          intro j hj
          positivity) (Finset.mem_univ i)
      simpa using hs

lemma abs_le_of_sq_le_three_over_four_hundred {x : ℝ}
    (h : x ^ 2 ≤ (9 : ℝ) / 400) : |x| ≤ 3 / 20 := by
  rw [abs_le]
  constructor <;> nlinarith [sq_nonneg (x - 3 / 20), sq_nonneg (x + 3 / 20)]

lemma abs_le_two_of_sq_le_three {x : ℝ} (h : x ^ 2 ≤ 3) :
    -2 ≤ x ∧ x ≤ 2 := by
  constructor <;> nlinarith [sq_nonneg (x - 2), sq_nonneg (x + 2)]

/- The full-X0 set is contained in the explicit finite initial box. -/
theorem fullX0_subset_initialBox {z : State14} (hz : FullX0 z) :
    InitialBox z := by
  rcases hz with ⟨henergy, hw, hc⟩
  refine ⟨?_, ?_, hw, abs_le_two_of_sq_le_three hc⟩
  · intro i
    have hi := q_term_le_energy z i
    have habs := abs_le_of_sq_le_three_over_four_hundred (le_trans hi henergy)
    simpa [neg_div] using (abs_le.mp habs)
  · intro i
    have hi := dq_term_le_energy z i
    have habs := abs_le_of_sq_le_three_over_four_hundred (le_trans hi henergy)
    simpa [neg_div] using (abs_le.mp habs)

/- Abstract replacement for the deployed `full_rhs!`.  Keeping the RHS as an
   explicit parameter prevents a numerical probe from becoming a theorem. -/
def full_rhs! (F : VectorField) : VectorField := F

def RampRhsPremise (F : VectorField) : Prop :=
  ∀ z : State14,
    full_rhs! F z wSlot = z cSlot ∧ full_rhs! F z cSlot = 0

def Box (lo hi : State14) (z : State14) : Prop :=
  ∀ i : Fin 14, lo i ≤ z i ∧ z i ≤ hi i

def RhsIntervalPremise (F : VectorField) (B : State14 → Prop)
    (lo hi : State14) : Prop :=
  ∀ y, B y → ∀ i : Fin 14, lo i ≤ full_rhs! F y i ∧ full_rhs! F y i ≤ hi i

def picardImage (F : VectorField) (z₀ : State14) (h : ℝ)
    (B : State14 → Prop) (z : State14) : Prop :=
  ∃ y, B y ∧ ∀ i : Fin 14, z i = z₀ i + h * full_rhs! F y i

def picardStepBox (z₀ lo hi : State14) (h : ℝ) (z : State14) : Prop :=
  Box (fun i => z₀ i + h * lo i) (fun i => z₀ i + h * hi i) z

def rampPicardCoordinates (z₀ : State14) (h : ℝ)
    (B : State14 → Prop) (z : State14) : Prop :=
  ∃ y, B y ∧
    z wSlot = z₀ wSlot + h * y cSlot ∧
    z cSlot = z₀ cSlot

theorem picard_coordinate_bounds
    {F : VectorField} {z₀ y z : State14} {h : ℝ}
    {lo hi : State14}
    (hh : 0 ≤ h)
    (hpic : ∀ i : Fin 14, z i = z₀ i + h * full_rhs! F y i)
    (hrhs : ∀ i : Fin 14,
      lo i ≤ full_rhs! F y i ∧ full_rhs! F y i ≤ hi i) :
    ∀ i : Fin 14,
      z₀ i + h * lo i ≤ z i ∧ z i ≤ z₀ i + h * hi i := by
  intro i
  rcases hrhs i with ⟨hlo, hhi⟩
  rw [hpic i]
  constructor <;> nlinarith

theorem picard_image_inclusion
    {F : VectorField} {z₀ z : State14} {h : ℝ}
    {B : State14 → Prop} {lo hi : State14}
    (hh : 0 ≤ h)
    (hrhs : RhsIntervalPremise F B lo hi)
    (hz : picardImage F z₀ h B z) :
    picardStepBox z₀ lo hi h z := by
  rcases hz with ⟨y, hy, hpic⟩
  intro i
  exact (picard_coordinate_bounds (F := F) (z₀ := z₀) (y := y) (z := z)
    (h := h) hh hpic (hrhs y hy)) i

theorem picard_image_ramp_coordinates
    {F : VectorField} {z₀ z : State14} {h : ℝ}
    {B : State14 → Prop}
    (hramp : RampRhsPremise F)
    (hz : picardImage F z₀ h B z) :
    rampPicardCoordinates z₀ h B z := by
  rcases hz with ⟨y, hy, hpic⟩
  have hwy := (hramp y).1
  have hcy := (hramp y).2
  refine ⟨y, hy, ?_, ?_⟩
  · rw [hpic wSlot, hwy]
  · rw [hpic cSlot, hcy]
    simp

/- The minimal P8 decomposition: a full-X0 start is placed in the initial
   box, and one abstract interval RHS certificate closes one Picard image
   inclusion.  The concrete RHS and interval receipts remain an open leaf. -/
theorem fullX0_ramp_picard_step_decomposition
    {F : VectorField} {z₀ z : State14} {h : ℝ}
    {lo hi : State14}
    (hz₀ : FullX0 z₀)
    (hh : 0 ≤ h)
    (hramp : RampRhsPremise F)
    (hbox : ∀ y, InitialBox y →
      ∀ i : Fin 14, lo i ≤ full_rhs! F y i ∧ full_rhs! F y i ≤ hi i)
    (hz : picardImage F z₀ h InitialBox z) :
    InitialBox z₀ ∧ picardStepBox z₀ lo hi h z ∧
      rampPicardCoordinates z₀ h InitialBox z := by
  refine ⟨fullX0_subset_initialBox hz₀, ?_, ?_⟩
  · exact picard_image_inclusion hh hbox hz
  · exact picard_image_ramp_coordinates hramp hz

#print axioms rampLift_w
#print axioms rampLift_c
#print axioms fullX0_subset_initialBox
#print axioms picard_coordinate_bounds
#print axioms picard_image_inclusion
#print axioms picard_image_ramp_coordinates
#print axioms fullX0_ramp_picard_step_decomposition

end
end RouteBP8PicardStep

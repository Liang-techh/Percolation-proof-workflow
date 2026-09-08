import ActualStorage
import ActualShift

set_option autoImplicit false
open scoped BigOperators

namespace NEW_BODY6_SLICE_ACTUALSTORAGEALIGN20260907
noncomputable section
abbrev Vec := Fin 6 → ℝ
abbrev Mat := Fin 6 → Fin 6 → ℝ
def shiftB : ℝ := 4079979/400000

/- OPEN_UNCOMPILED. An explicit specialization, not a selection of the
   active candidate: f=1, h=0, fixed p,H,Uzero, and the same q/v coordinates. -/
def actualBase (H : Mat) (M : Vec → Mat) (U : Vec → ℝ)
    (Uzero : ℝ) (p q v : Vec) : ℝ :=
  RouteBActualEnergyStorage.storageV 1 p 0 H (M q) (U q) Uzero q v 0

def remainder (H : Mat) (U : Vec → ℝ) (Uzero : ℝ) (p q : Vec) : ℝ :=
  U q - Uzero - RouteBSignedGap.kinetic H q + (7/75)*(q 3)^2 + ∑ i, p i*(q i)^2

def encodedBase (M : Vec → Mat) (q v : Vec) : ℝ :=
  RouteBShiftedStorage.kinetic (M q) v + RouteBPotentialSlice.W q

def encodedShifted (M : Vec → Mat) (q v : Vec) : ℝ := encodedBase M q v + shiftB

theorem kinetic_definitions_agree_attempt (A : Mat) (v : Vec) :
    RouteBSignedGap.kinetic A v = RouteBShiftedStorage.kinetic A v := by rfl

theorem actual_base_decomposition_attempt (H : Mat) (M : Vec → Mat)
    (U : Vec → ℝ) (Uzero : ℝ) (p q v : Vec) :
    actualBase H M U Uzero p q v =
      RouteBShiftedStorage.kinetic (M q) v + remainder H U Uzero p q := by
  unfold remainder
  simp only [actualBase, RouteBActualEnergyStorage.storageV,
    RouteBActualEnergyStorage.W0_actual_energy, kinetic_definitions_agree_attempt]
  ring

/- Minimal value identity after explicit common-coordinate specialization. -/
structure Alignment (Q : Set Vec) (H : Mat) (Mactual Mencoded : Vec → Mat)
    (U : Vec → ℝ) (Uzero : ℝ) (p : Vec) : Prop where
  sameMass : ∀ q ∈ Q, Mactual q = Mencoded q
  sameRemainder : ∀ q ∈ Q, remainder H U Uzero p q = RouteBPotentialSlice.W q

/- A more source-readable way to discharge the remainder field. It keeps
   normalization and quadratic compensation separate, on exactly Q. -/
theorem remainder_from_source_fields_attempt (Q : Set Vec) (H : Mat)
    (U : Vec → ℝ) (Uzero : ℝ) (p : Vec)
    (hU : ∀ q ∈ Q, U q - Uzero = RouteBPotentialSlice.potential q -
      RouteBPotentialSlice.potential ![0,0,0,0,0,0])
    (hQuad : ∀ q ∈ Q, (∑ i, p i*(q i)^2) + (7/75)*(q 3)^2 =
      RouteBSignedGap.kinetic H q + RouteBPotentialSlice.proportionalEnergy q) :
    ∀ q ∈ Q, remainder H U Uzero p q = RouteBPotentialSlice.W q := by
  intro q hq
  have hquadratic := hQuad q hq
  unfold remainder RouteBPotentialSlice.W
  rw [hU q hq]
  linarith

theorem aligned_base_identity_attempt (Q : Set Vec) (H : Mat)
    (Ma Me : Vec → Mat) (U : Vec → ℝ) (Uzero : ℝ) (p : Vec)
    (h : Alignment Q H Ma Me U Uzero p) (q v : Vec) (hq : q ∈ Q) :
    actualBase H Ma U Uzero p q v = encodedBase Me q v := by
  rw [actual_base_decomposition_attempt, h.sameMass q hq, h.sameRemainder q hq]
  rfl

theorem aligned_shifted_identity_attempt (Q : Set Vec) (H : Mat)
    (Ma Me : Vec → Mat) (U : Vec → ℝ) (Uzero : ℝ) (p : Vec)
    (h : Alignment Q H Ma Me U Uzero p) (q v : Vec) (hq : q ∈ Q) :
    actualBase H Ma U Uzero p q v + shiftB = encodedShifted Me q v := by
  rw [aligned_base_identity_attempt Q H Ma Me U Uzero p h q v hq]
  rfl

/- Source-domain inclusion is an INPUT at each path point. The additive
   shift is charged to the cap, even after base-storage identity is proved. -/
theorem aligned_path_cap_transfer_attempt (Q : Set Vec) (H : Mat)
    (Ma Me : Vec → Mat) (U : Vec → ℝ) (Uzero : ℝ) (p : Vec)
    (h : Alignment Q H Ma Me U Uzero p) (q v : ℝ → Vec) (cap bar : ℝ)
    (hPath : ∀ t ∈ Set.Icc (0 : ℝ) 1, q t ∈ Q)
    (hSource : ∀ t ∈ Set.Icc (0 : ℝ) 1, actualBase H Ma U Uzero p (q t) (v t) ≤ cap)
    (hBudget : cap + shiftB ≤ bar) :
    ∀ t ∈ Set.Icc (0 : ℝ) 1, encodedShifted Me (q t) (v t) ≤ bar := by
  intro t ht
  rw [← aligned_shifted_identity_attempt Q H Ma Me U Uzero p h (q t) (v t) (hPath t ht)]
  exact (add_le_add_right (hSource t ht) shiftB).trans hBudget

theorem encoded_W_origin_attempt : RouteBPotentialSlice.W (0 : Vec) = 0 := by
  have hz : (![0,0,0,0,0,0] : Vec) = 0 := by
    funext i
    fin_cases i <;> rfl
  simp [RouteBPotentialSlice.W, hz, RouteBPotentialSlice.proportionalEnergy]

/- Exact counterexample using the actual definitions, not scalar metadata:
   at the origin the normalized ActualStorage specialization is zero,
   whereas the ActualShift comparison energy is B>1. H,p,M are arbitrary. -/
theorem actual_origin_value_attempt (H : Mat) (M : Vec → Mat) (p : Vec) :
    actualBase H M RouteBPotentialSlice.potential
      (RouteBPotentialSlice.potential 0) p 0 0 = 0 := by
  rw [actual_base_decomposition_attempt]
  simp [remainder, RouteBShiftedStorage.kinetic, RouteBSignedGap.kinetic,
    RouteBSignedGap.quad, RouteBSignedGap.dot, RouteBSignedGap.mv]

theorem actual_origin_fixed_bar_counterexample_attempt (H : Mat) (M : Vec → Mat) (p : Vec) :
    actualBase H M RouteBPotentialSlice.potential
      (RouteBPotentialSlice.potential 0) p 0 0 ≤ 1 ∧
    ¬ encodedShifted M 0 0 ≤ 1 := by
  constructor
  · rw [actual_origin_value_attempt]
    norm_num
  · norm_num [encodedShifted, encodedBase, encoded_W_origin_attempt,
      RouteBShiftedStorage.kinetic, shiftB]

/- No active candidate Alignment instance, positivity/gap bound, actual
   trajectory, source-to-Float64 binding or compiled receipt is asserted. -/
end
end NEW_BODY6_SLICE_ACTUALSTORAGEALIGN20260907

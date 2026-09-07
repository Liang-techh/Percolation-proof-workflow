import NEW_BODY6_SLICE_SCHURREMAINDER20260907
import NEW_BODY6_SLICE_MASSMIX_Source20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_SOURCEBLOCKBIND20260907

noncomputable section

open NEW_BODY6_SLICE_LEVER_Source20260907 NEW_BODY6_SLICE_VGRAM_Source20260907
open NEW_BODY6_SLICE_MASSTAIL_Core20260907 NEW_BODY6_SLICE_MASSTAIL_Source20260907
open NEW_BODY6_SLICE_MASSMIX_Core20260907 NEW_BODY6_SLICE_TAILPSD20260907
open NEW_BODY6_SLICE_SCHURREMAINDER20260907 RouteBO1PerBodyExactSource

/- UNCOMPILED. Fixed front indices 0,1,2 and ordered tail indices 3,4.
   These definitions reference actual body-6 entries; they are not numeric tables. -/
def sourceA (q : Fin 6 → ℝ) (i j : Fin 3) : ℝ :=
  sourceBodyMass q (5 : Fin 6) (firstJoint i) (firstJoint j)

def sourceX (q : Fin 6 → ℝ) (i : Fin 3) (a : Fin 2) : ℝ :=
  sourceBodyMass q (5 : Fin 6) (firstJoint i) (tailJoint a)

def sourceY (q : Fin 6 → ℝ) (a : Fin 2) (j : Fin 3) : ℝ :=
  sourceBodyMass q (5 : Fin 6) (tailJoint a) (firstJoint j)

def FirstBlockBindingObligation (q : Fin 6 → ℝ) (A : Fin 3 → Fin 3 → ℝ) : Prop :=
  ∀ i j, A i j = sourceA q i j

structure SourceBlockBinding (q : Fin 6 → ℝ) (A : Fin 3 → Fin 3 → ℝ)
    (X : Fin 3 → Fin 2 → ℝ) (Y : Fin 2 → Fin 3 → ℝ) : Prop where
  bindA : FirstBlockBindingObligation q A
  bindX : ∀ i a, X i a = sourceX q i a
  bindY : ∀ a j, Y a j = sourceY q a j

/- Reflexive source references do not validate an independently supplied table. -/
theorem raw_source_binding_attempt (q : Fin 6 → ℝ) :
    SourceBlockBinding q (sourceA q) (sourceX q) (sourceY q) :=
  ⟨fun _ _ => rfl, fun _ _ => rfl, fun _ _ => rfl⟩

theorem source_y_transpose_attempt (q : Fin 6 → ℝ) (a : Fin 2) (j : Fin 3) :
    sourceY q a j = sourceX q j a :=
  source_mass_symmetric_attempt q (tailJoint a) (firstJoint j)

def mixedX (q : Fin 6 → ℝ) (m kappa : ℝ) : Fin 3 → Fin 2 → ℝ :=
  explicitMixed q offset m kappa

def mixedY (q : Fin 6 → ℝ) (m kappa : ℝ) (a : Fin 2) (j : Fin 3) : ℝ :=
  mixedX q m kappa j a

/- The two existing weight targets and tail maps have identical definitions.
   Conversion preserves actual body, source constants, and index ordering. -/
theorem mixed_x_binding_attempt (hc : CenterOffsetTarget)
    (m kappa : ℝ) (hw : SourceWeightsTarget m kappa) (q : Fin 6 → ℝ) (i : Fin 3) (a : Fin 2) :
    mixedX q m kappa i a = sourceX q i a := by
  have hwMixed : NEW_BODY6_SLICE_MASSMIX_Source20260907.SourceWeightsTarget m kappa := hw
  simpa [mixedX, sourceX, tailJoint, NEW_BODY6_SLICE_MIXED_Core20260907.tailJoint] using
    (NEW_BODY6_SLICE_MASSMIX_Source20260907.source_weighted_mixed_attempt hc m kappa hwMixed q i a).symm

theorem mixed_binding_from_A_attempt (hc : CenterOffsetTarget)
    (m kappa : ℝ) (hw : SourceWeightsTarget m kappa) (q : Fin 6 → ℝ)
    (A : Fin 3 → Fin 3 → ℝ) (hA : FirstBlockBindingObligation q A) :
    SourceBlockBinding q A (mixedX q m kappa) (mixedY q m kappa) := by
  refine ⟨hA, mixed_x_binding_attempt hc m kappa hw q, ?_⟩
  intro a j
  unfold mixedY
  rw [mixed_x_binding_attempt hc m kappa hw q j a, source_y_transpose_attempt]

/- An absent A witness stays an obligation. Only an actual mismatch refutes it. -/
theorem A_mismatch_rejects_binding_attempt (q : Fin 6 → ℝ)
    (A : Fin 3 → Fin 3 → ℝ) (X : Fin 3 → Fin 2 → ℝ) (Y : Fin 2 → Fin 3 → ℝ)
    (bad : ∃ i j, A i j ≠ sourceA q i j) : ¬ SourceBlockBinding q A X Y := by
  intro hb
  obtain ⟨i, j, hne⟩ := bad
  exact hne (hb.bindA i j)

theorem bound_remainder_coefficient_attempt (q : Fin 6 → ℝ) (m kappa : ℝ)
    (A : Fin 3 → Fin 3 → ℝ) (X : Fin 3 → Fin 2 → ℝ) (Y : Fin 2 → Fin 3 → ℝ)
    (hb : SourceBlockBinding q A X Y) (i j : Fin 3) :
    schurRemainder (q 4) offset m kappa A X Y i j = sourceA q i j -
      sourceX q i 0 * sourceY q 0 j / (kappa + m * offset ^ 2 * Real.sin (q 4) ^ 2) -
      sourceX q i 1 * sourceY q 1 j / (kappa + m * offset ^ 2) := by
  rw [remainder_coefficient_attempt, hb.bindA i j, hb.bindX i 0, hb.bindY 0 j,
    hb.bindX i 1, hb.bindY 1 j]

/- Conditional inverse/solve contract plus actual-entry coefficient binding.
   No source witness for an arbitrary candidate A is synthesized. -/
theorem bound_source_remainder_attempt (hc : CenterOffsetTarget)
    (m kappa : ℝ) (hw : SourceWeightsTarget m kappa)
    (hk : 0 < kappa) (hm : 0 ≤ m) (hh : 0 ≤ offset ^ 2) (q : Fin 6 → ℝ)
    (A : Fin 3 → Fin 3 → ℝ) (X : Fin 3 → Fin 2 → ℝ) (Y : Fin 2 → Fin 3 → ℝ)
    (hb : SourceBlockBinding q A X Y) :
    SchurRemainderContract 3 3 (sourceTail q) (q 4) offset m kappa A X Y ∧
    (∀ i j, schurRemainder (q 4) offset m kappa A X Y i j = sourceA q i j -
      sourceX q i 0 * sourceY q 0 j / (kappa + m * offset ^ 2 * Real.sin (q 4) ^ 2) -
      sourceX q i 1 * sourceY q 1 j / (kappa + m * offset ^ 2)) :=
  ⟨source_remainder_contract_attempt hc m kappa hw hk hm hh q A X Y,
    bound_remainder_coefficient_attempt q m kappa A X Y hb⟩

/- Source-binding obligations only. No full-matrix/Schur PSD, Fourier, coverage,
   Lean execution, unconditional geometry witness, or registry admission. -/
end
end NEW_BODY6_SLICE_SOURCEBLOCKBIND20260907

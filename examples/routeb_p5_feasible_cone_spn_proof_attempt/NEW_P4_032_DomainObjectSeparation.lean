import BlockTargets
import NEW_BODY6_SLICE_SCHURMARGIN20260907

/-!
OPEN_UNCOMPILED. Distinct domains and mass objects, with explicit bridges.
No Lean/Lake execution or identification of saved storage with mechanical
energy. CSV point binding is an external premise, not a kernel-checked import.
-/

set_option autoImplicit false

namespace RouteBP4032DomainObjectSeparation

open scoped BigOperators

noncomputable section

abbrev Config := Fin 6 → ℝ
abbrev Matrix6 := Fin 6 → Fin 6 → ℝ
abbrev Matrix3 := Fin 3 → Fin 3 → ℝ

structure State where
  q : Config
  velocity : Config
  time : ℝ

def blockP (x : State) : ℝ := RouteBBlockTargets.p
  (x.q 3) (x.q 4) (x.velocity 3) (x.velocity 4)

/-- Storage depends on the four selected block coordinates and time.
Its coefficient/source identity must be supplied independently. -/
structure SavedBlockStorage where
  value : (Fin 4 → ℝ) → ℝ → ℝ

def storageAt (V : SavedBlockStorage) (x : State) : ℝ :=
  V.value ![x.q 3, x.q 4, x.velocity 3, x.velocity 4] x.time

structure BlockRegion (x : State) : Prop where
  bound : blockP x ≤ (28 / 5 : ℝ)

structure StorageOneRegion (V : SavedBlockStorage) (x : State) : Prop where
  bound : storageAt V x ≤ 1

structure StorageTube (V : SavedBlockStorage) (x : State) : Prop where
  time_nonnegative : 0 ≤ x.time
  time_le_one : x.time ≤ 1
  bound : storageAt V x ≤ x.time^2

theorem tube_in_storage_one (V : SavedBlockStorage) (x : State)
    (h : StorageTube V x) : StorageOneRegion V x := by
  have ht0 := h.time_nonnegative
  have ht1 := h.time_le_one
  have hv := h.bound
  exact ⟨by nlinarith⟩

/-- A source-bound localization certificate is REQUIRED for tube -> block.
Positive multiplier and the correct time threshold cannot be omitted. -/
structure TubeLocalization (V : SavedBlockStorage) (D : State → Prop) where
  multiplier : State → ℝ
  positive : ∀ x, D x → 0 < multiplier x
  bound : ∀ x, D x → multiplier x * (blockP x - (28 / 5 : ℝ)) ≤
    storageAt V x - x.time^2

theorem tube_in_block (V : SavedBlockStorage) (D : State → Prop)
    (loc : TubeLocalization V D) (x : State) (hx : D x)
    (tube : StorageTube V x) : BlockRegion x := by
  have hp := loc.positive x hx
  have hl := loc.bound x hx
  have hv := tube.bound
  refine ⟨?_⟩
  nlinarith

/-- V<=1 requires its OWN localization, distinct from V<=time^2. -/
structure StorageOneLocalization (V : SavedBlockStorage) (D : State → Prop) where
  multiplier : State → ℝ
  positive : ∀ x, D x → 0 < multiplier x
  bound : ∀ x, D x → multiplier x * (blockP x - (28 / 5 : ℝ)) ≤ storageAt V x - 1

theorem storage_one_in_block (V : SavedBlockStorage) (D : State → Prop)
    (loc : StorageOneLocalization V D) (x : State) (hx : D x)
    (hv : StorageOneRegion V x) : BlockRegion x := by
  have hp := loc.positive x hx
  have hl := loc.bound x hx
  have hb := hv.bound
  exact ⟨by nlinarith⟩

/-- A block-only sublevel imposes no bound on remote velocity 0. -/
theorem block_region_remote_unbounded (cap : ℝ) :
    ∃ x : State, BlockRegion x ∧ cap < x.velocity 0 := by
  let x : State := ⟨fun _ => 0, fun i => if i = 0 then max 0 cap + 1 else 0, 0⟩
  refine ⟨x, ⟨?_⟩, ?_⟩
  · norm_num [blockP, RouteBBlockTargets.p, x]
  · have h := le_max_right (0 : ℝ) cap
    dsimp [x]
    simp only [ite_true]
    linarith

def savedPoint : State :=
  ⟨fun _ => 0, fun i => if i = 3 then (5 / 2 : ℝ) else 0, 1⟩

/-- Conditional CSV binding. The exact rational point value was separately
checked from the frozen decimal CSV; no Lean reification proof is claimed. -/
theorem saved_point_not_storage_one (V : SavedBlockStorage)
    (hvalue : storageAt V savedPoint =
      (10124753406335225920259294819898769 : ℝ) /
        4000000000000000000000000000000000) :
    BlockRegion savedPoint ∧ ¬ StorageOneRegion V savedPoint := by
  constructor
  · exact ⟨by norm_num [blockP, RouteBBlockTargets.p, savedPoint]⟩
  · intro h
    have hb := h.bound
    rw [hvalue] at hb
    norm_num at hb

/-- Abstract counterexample to any automatic reverse-domain inclusion:
V=0 is not claimed to be the saved CSV. -/
theorem arbitrary_V_does_not_imply_block :
    ∃ (V : SavedBlockStorage) (x : State), StorageOneRegion V x ∧ ¬ BlockRegion x := by
  let V : SavedBlockStorage := ⟨fun _ _ => 0⟩
  let x : State := ⟨fun i => if i = 3 then 2 else 0, fun _ => 0, 0⟩
  refine ⟨V, x, ⟨by simp [storageAt, V]⟩, ?_⟩
  intro h
  have hb := h.bound
  norm_num [blockP, RouteBBlockTargets.p, x] at hb

/-- Full six-body interpreted dynamics. Cforce is the six-vector C*dq,
not a 3x3 remainder or automatically an analytic Christoffel matrix. -/
structure FullRegularizedMCG where
  mass : Config → Matrix6
  Cforce : Config → Config → Config
  gravity : Config → Config
  regularizer : ℝ
  fdStep : ℝ

structure Body6UnregularizedMass where
  value : Config → Matrix6

structure Body6UnregularizedRemainder where
  value : Config → Matrix3

/-- Body identity, six-body accumulation and regularizer are separate
premises. C/G semantics are NOT inferred from this mass-only binding. -/
structure MassObjectBinding (full : FullRegularizedMCG) (body6 : Body6UnregularizedMass) where
  otherFive : Config → Matrix6
  body6_source : ∀ q, body6.value q = RouteBO1PerBodyExactSource.sourceBodyMass q (5 : Fin 6)
  full_assembly : ∀ q i j, full.mass q i j = body6.value q i j + otherFive q i j +
    if i = j then full.regularizer else 0
  regularizer_exact : full.regularizer = (1 / 1000000 : ℝ)
  fdStep_exact : full.fdStep = (1 / 100000 : ℝ)
  other_five_source : ∀ q i j, otherFive q i j =
    ∑ k : Fin 5, RouteBO1PerBodyExactSource.sourceBodyMass q
      (⟨k.val, by omega⟩ : Fin 6) i j

/-- No implicit cast identifies this 3x3 object with the full 6x6 M.
Even its BODY6 Schur formula is a separate explicit source binding. -/
structure RemainderObjectBinding (r : Body6UnregularizedRemainder)
    (mass inertia : ℝ) : Prop where
  formula : ∀ q i j, r.value q i j =
    NEW_BODY6_SLICE_SCHURREMAINDER20260907.schurRemainder
      (q 4) NEW_BODY6_SLICE_VGRAM_Source20260907.offset mass inertia
      (NEW_BODY6_SLICE_SOURCEBLOCKBIND20260907.sourceA q)
      (NEW_BODY6_SLICE_SOURCEBLOCKBIND20260907.sourceX q)
      (NEW_BODY6_SLICE_SOURCEBLOCKBIND20260907.sourceY q) i j

/-- Positive regularizer plus nonnegative other-body diagonal already
prevents equality of full M and the unregularized single-body mass. -/
theorem full_mass_diagonal_strict (full : FullRegularizedMCG)
    (body6 : Body6UnregularizedMass) (b : MassObjectBinding full body6)
    (q : Config) (i : Fin 6) (hother : 0 ≤ b.otherFive q i i) :
    body6.value q i i < full.mass q i i := by
  have h := b.full_assembly q i i
  simp only [ite_true, b.regularizer_exact] at h
  linarith

/-- Schur elimination is not additive over body contributions. Each
scalar block has a=2,d=1 and x=y=+1 or -1; the sum has tail inverse 0.5. -/
theorem schur_sum_counterexample :
    (2 - 1 * 1 * 1 : ℝ) + (2 - (-1) * 1 * (-1)) ≠
      (2 + 2) - (1 + (-1)) * 0.5 * (1 + (-1)) := by
  norm_num

/-- Regularizing the entire block changes the eliminated tail inverse;
it is not equivalent to adding the regularizer after Schur elimination. -/
theorem schur_regularizer_counterexample :
    (3 - 1 * 0.5 * 1 : ℝ) ≠ (2 - 1 * 1 * 1) + 1 := by
  norm_num

end

-- Future audit commands only; NOT executed in this round.
#print axioms tube_in_storage_one
#print axioms tube_in_block
#print axioms storage_one_in_block
#print axioms block_region_remote_unbounded
#print axioms saved_point_not_storage_one
#print axioms arbitrary_V_does_not_imply_block
#print axioms full_mass_diagonal_strict
#print axioms schur_sum_counterexample
#print axioms schur_regularizer_counterexample

end RouteBP4032DomainObjectSeparation

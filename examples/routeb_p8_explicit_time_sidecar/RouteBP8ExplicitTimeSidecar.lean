import RouteBP8PicardStep
import Mathlib.Data.Fin.Basic
import Mathlib.Tactic

/-!
# P8 explicit-time 13-state sidecar

This file freezes the smallest explicit-time interface for the deployed
13-state source.  It does not alter the authoritative `RouteBP8PicardStep`
target, and it does not claim a flowpipe, solution existence theorem, or
source binding.

The interface keeps `c` external to the state vector.  The sidecar records:

* the 13-state coordinate order `q₁…q₆, dq₁…dq₆, w`;
* an explicit parameter `c` for the source family;
* an initial projection from the 14-state parent to the 13-state family;
* a terminal-transfer predicate that rewrites the `w` coordinate using `c`.

The theorems below are intentionally minimal: they only package the assumptions
needed by a later source-authenticated child theorem.
-/

namespace RouteBP8ExplicitTimeSidecar

set_option autoImplicit false

open RouteBP8PicardStep

abbrev State13 := Fin 13 → ℝ
abbrev TimeVectorField13 := ℝ → ℝ → State13 → State13

def forgetTail13 (z : State14) : State13 := fun i => z ⟨i.val, by omega⟩

def wSlot13 : Fin 13 := 12

def explicitInitial13 (x : State13) (c : ℝ) : Prop :=
  (∑ i : Fin 6, (x ⟨i.val, by omega⟩ ^ 2 + x ⟨6 + i.val, by omega⟩ ^ 2)) ≤
    (9 : ℝ) / 400 ∧
    x wSlot13 = 0 ∧
    c ^ 2 ≤ 3

def initialProjection13 (z : State14) : Prop :=
  explicitInitial13 (forgetTail13 z) (z cSlot)

def explicitTerminal13 (y : State13) (c : ℝ) : Prop :=
  y wSlot13 = c

def terminalTransfer13 (y : State13) (c : ℝ) : Prop :=
  explicitTerminal13 y c

def sourceFamily13 (F13 : TimeVectorField13) (c : ℝ) : Prop :=
  ∀ t x, F13 t c x = F13 t c x

theorem explicitInitial13_of_fullX0
    (z : State14) (hz : FullX0 z) :
    initialProjection13 z := by
  rcases hz with ⟨henergy, hw, hc⟩
  refine ⟨?_, ?_, hc⟩
  · simpa [initialProjection13, explicitInitial13, forgetTail13, mechanicalEnergy,
      qSlot, dqSlot] using henergy
  · simpa [initialProjection13, explicitInitial13, forgetTail13, wSlot, wSlot13] using hw

theorem initialProjection13_from_fullX0
    (z : State14) (hz : FullX0 z) :
    initialProjection13 z := by
  exact explicitInitial13_of_fullX0 z hz

theorem explicitTerminal13_transfer
    (y : State13) (c : ℝ) :
    explicitTerminal13 y c ↔ y wSlot13 = c := by
  rfl

theorem explicitTerminal13_lift
    (y : State13) (c : ℝ) :
    terminalTransfer13 y c →
      y wSlot13 = c := by
  intro hy
  exact hy

theorem explicitTimeContract_assumptions
    (F13 : TimeVectorField13) (c : ℝ) :
    sourceFamily13 F13 c ∧
      (∀ z : State14, initialProjection13 z → initialProjection13 z) ∧
      (∀ y : State13, terminalTransfer13 y c → terminalTransfer13 y c) := by
  refine ⟨?_, ?_, ?_⟩
  · intro t x
    rfl
  · intro z hz
    exact hz
  · intro y hy
    exact hy

#print axioms explicitInitial13_of_fullX0
#print axioms initialProjection13_from_fullX0
#print axioms explicitTerminal13_transfer
#print axioms explicitTerminal13_lift

end RouteBP8ExplicitTimeSidecar

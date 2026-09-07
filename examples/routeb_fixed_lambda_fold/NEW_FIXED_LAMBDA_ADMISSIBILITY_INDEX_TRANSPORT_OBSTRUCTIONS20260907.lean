import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaIndexTransportObstructions

noncomputable section

/-!
These are finite exact counterexamples to unsafe aggregate transport.  They
show why the positive index adapter must retain injectivity, surjectivity, and
total-equality premises as separate fields.
-/

def sourceSum (s : Finset Nat) (load : Nat → ℚ) : ℚ :=
  ∑ i in s, load i

def targetSum (t : Finset Nat) (load : Nat → ℚ) : ℚ :=
  ∑ i in t, load i

def mapInjectiveOn
    (source target : Finset Nat) (rowMap : Nat → Nat) : Prop :=
  ∀ {i j : Nat}, i ∈ source → j ∈ source →
    rowMap i = rowMap j → i = j

def mapSurjectiveOnto
    (source target : Finset Nat) (rowMap : Nat → Nat) : Prop :=
  ∀ j ∈ target, ∃ i ∈ source, rowMap i = j

/- Missing injectivity: two source rows collapse to one target row. -/
def noninjectiveSource : Finset Nat := {0, 1}
def noninjectiveTarget : Finset Nat := {0}
def noninjectiveMap (_ : Nat) : Nat := 0
def unitLoad (_ : Nat) : ℚ := 1

theorem noninjective_map_has_membership
    (i : Nat) (hi : i ∈ noninjectiveSource) :
    noninjectiveMap i ∈ noninjectiveTarget := by
  simp [noninjectiveMap, noninjectiveTarget]

theorem noninjective_map_is_not_injective :
    ¬ mapInjectiveOn noninjectiveSource noninjectiveTarget
      noninjectiveMap := by
  intro h
  have h01 := h (i := 0) (j := 1) (by simp [noninjectiveSource])
    (by simp [noninjectiveSource]) (by rfl)
  norm_num at h01

theorem noninjective_sum_mismatch :
    sourceSum noninjectiveSource unitLoad = 2 ∧
      targetSum noninjectiveTarget unitLoad = 1 ∧
      sourceSum noninjectiveSource unitLoad ≠
        targetSum noninjectiveTarget unitLoad := by
  norm_num [sourceSum, targetSum, noninjectiveSource,
    noninjectiveTarget, unitLoad]

/- Missing surjectivity: a target row has no source preimage. -/
def nonsurjectiveSource : Finset Nat := {0}
def nonsurjectiveTarget : Finset Nat := {0, 1}
def identityMap (i : Nat) : Nat := i

theorem identity_map_is_injective_on_nonsurjective_example :
    mapInjectiveOn nonsurjectiveSource nonsurjectiveTarget identityMap := by
  intro i j _ _ hij
  exact hij

theorem identity_map_is_not_surjective_on_nonsurjective_example :
    ¬ mapSurjectiveOnto nonsurjectiveSource nonsurjectiveTarget identityMap := by
  intro h
  rcases h 1 (by simp [nonsurjectiveTarget]) with ⟨i, hi, himage⟩
  simp [nonsurjectiveSource] at hi
  subst i
  norm_num [identityMap] at himage

theorem nonsurjective_sum_mismatch :
    sourceSum nonsurjectiveSource unitLoad = 1 ∧
      targetSum nonsurjectiveTarget unitLoad = 2 ∧
      sourceSum nonsurjectiveSource unitLoad ≠
        targetSum nonsurjectiveTarget unitLoad := by
  norm_num [sourceSum, targetSum, nonsurjectiveSource,
    nonsurjectiveTarget, unitLoad]

/- Missing total equality: even a bijective row map does not identify the
   payload values without an explicit total equality (or row-value equality). -/
def equalIndexSource : Finset Nat := {0}
def equalIndexTarget : Finset Nat := {0}
def sourcePayload (_ : Nat) : ℚ := 1
def targetPayload (_ : Nat) : ℚ := 2

theorem equal_index_map_is_bijective :
    mapInjectiveOn equalIndexSource equalIndexTarget identityMap ∧
      mapSurjectiveOnto equalIndexSource equalIndexTarget identityMap := by
  constructor
  · intro i j _ _ hij
    exact hij
  · intro j hj
    refine ⟨j, ?_, rfl⟩
    simpa [equalIndexTarget] using hj

theorem equal_index_payload_sum_mismatch :
    sourceSum equalIndexSource sourcePayload = 1 ∧
      targetSum equalIndexTarget targetPayload = 2 ∧
      sourceSum equalIndexSource sourcePayload ≠
        targetSum equalIndexTarget targetPayload := by
  norm_num [sourceSum, targetSum, equalIndexSource,
    equalIndexTarget, sourcePayload, targetPayload]

/-!
Obstruction summary: each missing premise admits a finite exact mismatch, so a
transport theorem must keep all three premise families explicit.
-/
theorem transport_is_not_derivable_without_all_premises :
    sourceSum noninjectiveSource unitLoad ≠
        targetSum noninjectiveTarget unitLoad ∧
      sourceSum nonsurjectiveSource unitLoad ≠
        targetSum nonsurjectiveTarget unitLoad ∧
      sourceSum equalIndexSource sourcePayload ≠
        targetSum equalIndexTarget targetPayload := by
  exact ⟨noninjective_sum_mismatch.2.2,
    nonsurjective_sum_mismatch.2.2,
    equal_index_payload_sum_mismatch.2.2⟩

/- Admission boundary: these are finite obstruction witnesses only.  They do
   not identify any project artifact or physical cell domain. -/

#print axioms noninjective_map_is_not_injective
#print axioms identity_map_is_not_surjective_on_nonsurjective_example
#print axioms equal_index_payload_sum_mismatch
#print axioms transport_is_not_derivable_without_all_premises

end
end RouteBFixedLambdaIndexTransportObstructions

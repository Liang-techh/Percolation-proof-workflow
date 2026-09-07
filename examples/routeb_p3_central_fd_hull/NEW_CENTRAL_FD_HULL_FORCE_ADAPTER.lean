import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# P3 four-layer derivative-first force adapter

This file is an exact-real proof skeleton for the boundary between a
derivative-first Christoffel contraction and a source-force output.  It does
not prove the external source equality; that equality is a typed premise of
the contract.  Once supplied, the four remainder layers are linearized under
the same force map and the resulting error vector is ready for the existing
Fin 6 weighted power consumer.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP3CentralFDHullForceAdapter

noncomputable section

abbrev I6 := Fin 6
abbrev Tensor6 := I6 → I6 → I6 → ℝ
abbrev Vector6 := I6 → ℝ

/-- The derivative-first Christoffel contraction used by the consumer. -/
def christoffelContraction6
    (T : Tensor6) (v : Vector6) (i : I6) : ℝ :=
  ∑ j, ∑ k,
    ((T k i j + T j i k - T i j k) / 2) * v j * v k

/-- The four named remainder layers are kept as independent tensors. -/
structure FourLayerRemainders6 where
  machineLift : Tensor6
  centralFD : Tensor6
  derivativeHull : Tensor6
  exportCenter : Tensor6

def FourLayerRemainders6.total
    (R : FourLayerRemainders6) : Tensor6 :=
  fun k i j => R.machineLift k i j + R.centralFD k i j +
    R.derivativeHull k i j + R.exportCenter k i j

/-- Explicit external boundary premises.  Each proposition is carried with its
own proof and is not inferred from the algebra below. -/
structure BoundaryPremises6 where
  sourceBinding : Prop
  sourceBinding_ok : sourceBinding
  roundingContract : Prop
  roundingContract_ok : roundingContract
  exportContract : Prop
  exportContract_ok : exportContract
  coverageContract : Prop
  coverageContract_ok : coverageContract

/-- Source-force adapter contract.

`source_force_eq` is the only source-force equality used by the exact algebra;
it is deliberately a premise.  The reference tensor and all four remainder
layers are otherwise arbitrary exact-real data. -/
structure SourceForceContract6 where
  referenceTensor : Tensor6
  remainders : FourLayerRemainders6
  sourceForce : Vector6 → Vector6
  premises : BoundaryPremises6
  source_force_eq : ∀ v i,
    sourceForce v i =
      christoffelContraction6
        (fun k i j => referenceTensor k i j +
          remainders.total k i j) v i

theorem christoffelContraction6_add4
    (T R₀ R₁ R₂ R₃ : Tensor6) (v : Vector6) (i : I6) :
    christoffelContraction6
        (fun k i j => T k i j + R₀ k i j + R₁ k i j +
          R₂ k i j + R₃ k i j) v i =
      christoffelContraction6 T v i +
        christoffelContraction6 R₀ v i +
        christoffelContraction6 R₁ v i +
        christoffelContraction6 R₂ v i +
        christoffelContraction6 R₃ v i := by
  unfold christoffelContraction6
  apply Finset.sum_congr rfl
  intro j hj
  apply Finset.sum_congr rfl
  intro k hk
  ring

theorem four_layer_contraction_split
    (T : Tensor6) (R : FourLayerRemainders6) (v : Vector6) (i : I6) :
    christoffelContraction6 (fun k i j => T k i j + R.total k i j) v i =
      christoffelContraction6 T v i +
        christoffelContraction6 R.machineLift v i +
        christoffelContraction6 R.centralFD v i +
      christoffelContraction6 R.derivativeHull v i +
        christoffelContraction6 R.exportCenter v i := by
  unfold FourLayerRemainders6.total
  simpa [add_assoc] using
    (christoffelContraction6_add4 T R.machineLift R.centralFD
      R.derivativeHull R.exportCenter v i)

/-- The source-force equality, decomposed into the reference force and four
remainder-force contributions. -/
theorem source_force_four_layer_decomposition
    (C : SourceForceContract6) (v : Vector6) (i : I6) :
    C.sourceForce v i =
      christoffelContraction6 C.referenceTensor v i +
        christoffelContraction6 C.remainders.machineLift v i +
        christoffelContraction6 C.remainders.centralFD v i +
        christoffelContraction6 C.remainders.derivativeHull v i +
        christoffelContraction6 C.remainders.exportCenter v i := by
  rw [C.source_force_eq]
  exact four_layer_contraction_split C.referenceTensor C.remainders v i

def sourceForceError6
    (C : SourceForceContract6) (v : Vector6) : Vector6 :=
  fun i => C.sourceForce v i -
    christoffelContraction6 C.referenceTensor v i

/-- The error vector exposed to the existing Fin 6 power consumer. -/
theorem source_force_error_power_input
    (C : SourceForceContract6) (v : Vector6) (i : I6) :
    sourceForceError6 C v i =
      christoffelContraction6 C.remainders.machineLift v i +
      christoffelContraction6 C.remainders.centralFD v i +
      christoffelContraction6 C.remainders.derivativeHull v i +
      christoffelContraction6 C.remainders.exportCenter v i := by
  unfold sourceForceError6
  rw [source_force_four_layer_decomposition C v i]
  ring

theorem source_force_error_vector_eq
    (C : SourceForceContract6) (v : Vector6) :
    sourceForceError6 C v =
      fun i =>
        christoffelContraction6 C.remainders.machineLift v i +
        christoffelContraction6 C.remainders.centralFD v i +
        christoffelContraction6 C.remainders.derivativeHull v i +
        christoffelContraction6 C.remainders.exportCenter v i := by
  funext i
  exact source_force_error_power_input C v i

/-! A radius-side four-term split, kept separate from the source equality. -/

def Radius6 := Tensor6

def radiusAdd4
    (mu₀ mu₁ mu₂ mu₃ : Radius6) : Radius6 :=
  fun k i j => mu₀ k i j + mu₁ k i j + mu₂ k i j + mu₃ k i j

theorem four_layer_radius_contract
    (R : FourLayerRemainders6)
    (mu₀ mu₁ mu₂ mu₃ : Radius6)
    (h₀ : ∀ k i j, |R.machineLift k i j| ≤ mu₀ k i j)
    (h₁ : ∀ k i j, |R.centralFD k i j| ≤ mu₁ k i j)
    (h₂ : ∀ k i j, |R.derivativeHull k i j| ≤ mu₂ k i j)
    (h₃ : ∀ k i j, |R.exportCenter k i j| ≤ mu₃ k i j)
    (k i j : I6) :
    |R.total k i j| ≤ radiusAdd4 mu₀ mu₁ mu₂ mu₃ k i j := by
  unfold FourLayerRemainders6.total radiusAdd4
  calc
    |R.machineLift k i j + R.centralFD k i j +
        R.derivativeHull k i j + R.exportCenter k i j| ≤
        |R.machineLift k i j| + |R.centralFD k i j| +
          |R.derivativeHull k i j| + |R.exportCenter k i j| := by
      calc
        |R.machineLift k i j + R.centralFD k i j +
            R.derivativeHull k i j + R.exportCenter k i j| ≤
            |R.machineLift k i j + R.centralFD k i j +
              R.derivativeHull k i j| + |R.exportCenter k i j| :=
          abs_add_le _ _
        _ ≤ (|R.machineLift k i j + R.centralFD k i j| +
            |R.derivativeHull k i j|) + |R.exportCenter k i j| := by
          gcongr
          exact abs_add_le _ _
        _ ≤ (|R.machineLift k i j| + |R.centralFD k i j|) +
            |R.derivativeHull k i j| + |R.exportCenter k i j| := by
          gcongr
          exact abs_add_le _ _
    _ ≤ mu₀ k i j + mu₁ k i j + mu₂ k i j + mu₃ k i j := by
      gcongr
      · exact h₀ k i j
      · exact h₁ k i j
      · exact h₂ k i j
      · exact h₃ k i j

end

end RouteBP3CentralFDHullForceAdapter

#print axioms RouteBP3CentralFDHullForceAdapter.christoffelContraction6_add4
#print axioms RouteBP3CentralFDHullForceAdapter.source_force_four_layer_decomposition
#print axioms RouteBP3CentralFDHullForceAdapter.source_force_error_power_input
#print axioms RouteBP3CentralFDHullForceAdapter.four_layer_radius_contract

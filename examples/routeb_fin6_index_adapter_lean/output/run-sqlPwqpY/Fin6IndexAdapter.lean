import Mathlib

namespace RouteBFin6IndexAdapter

/-!
  A deliberately small source-order adapter for Route-B.

  `Fin 6` is the Lean/zero-based side.  `JuliaIndex` is the Julia/one-based
  side.  This file proves only the finite index correspondence and the
  declared block partition.  It does not define or verify a Julia `Float64`
  transform, a DH function, a mass function, or a COM/Jacobian convention.
-/

noncomputable section

abbrev ZeroIndex := Fin 6

def JuliaIndex := {n : Nat // 1 ≤ n ∧ n ≤ 6}

def toJulia (i : ZeroIndex) : JuliaIndex :=
  ⟨i.val + 1, by constructor <;> omega⟩

def fromJulia (j : JuliaIndex) : ZeroIndex :=
  ⟨j.val - 1, by omega⟩

theorem toJulia_offset (i : ZeroIndex) : (toJulia i).val = i.val + 1 := by
  rfl

theorem fromJulia_offset (j : JuliaIndex) : (fromJulia j).val + 1 = j.val := by
  dsimp [fromJulia]
  omega

theorem fromJulia_toJulia (i : ZeroIndex) : fromJulia (toJulia i) = i := by
  apply Fin.ext
  simp [fromJulia, toJulia]

theorem toJulia_fromJulia (j : JuliaIndex) : toJulia (fromJulia j) = j := by
  apply Subtype.ext
  dsimp [toJulia, fromJulia]
  omega

def fin6JuliaEquiv : ZeroIndex ≃ JuliaIndex where
  toFun := toJulia
  invFun := fromJulia
  left_inv := fromJulia_toJulia
  right_inv := toJulia_fromJulia

theorem fin6JuliaEquiv_bijective : Function.Bijective fin6JuliaEquiv := by
  exact fin6JuliaEquiv.bijective

/- The six source positions in source order, represented on the zero-based
   side.  The corresponding Julia values are obtained only by `toJulia`. -/
def sourceOrderFin : List ZeroIndex := [0, 1, 2, 3, 4, 5]

def sourceOrder0 : List Nat := sourceOrderFin.map Fin.val

def sourceOrderJulia : List JuliaIndex := sourceOrderFin.map toJulia

def sourceOrder1 : List Nat := sourceOrderJulia.map Subtype.val

theorem sourceOrder0_exact : sourceOrder0 = [0, 1, 2, 3, 4, 5] := by
  rfl

theorem sourceOrder1_exact : sourceOrder1 = [1, 2, 3, 4, 5, 6] := by
  rfl

theorem sourceOrder1_is_offset :
    sourceOrder1 = sourceOrder0.map (fun n => n + 1) := by
  rfl

/- The block labels below use the one-based Julia convention from the source:
     B = (4,5), D = (1,2,3,6).
   Their zero-based Lean representatives are therefore B = (3,4) and
   D = (0,1,2,5). -/
def blockBZero : List ZeroIndex := [3, 4]

def blockDZero : List ZeroIndex := [0, 1, 2, 5]

def blockBJulia : List JuliaIndex := blockBZero.map toJulia

def blockDJulia : List JuliaIndex := blockDZero.map toJulia

def blockBZeroValues : List Nat := blockBZero.map Fin.val

def blockDZeroValues : List Nat := blockDZero.map Fin.val

def blockBJuliaValues : List Nat := blockBJulia.map Subtype.val

def blockDJuliaValues : List Nat := blockDJulia.map Subtype.val

theorem blockBZero_exact : blockBZeroValues = [3, 4] := by
  rfl

theorem blockDZero_exact : blockDZeroValues = [0, 1, 2, 5] := by
  rfl

theorem blockBJulia_exact : blockBJuliaValues = [4, 5] := by
  rfl

theorem blockDJulia_exact : blockDJuliaValues = [1, 2, 3, 6] := by
  rfl

theorem blockBJulia_is_offset :
    blockBJuliaValues = blockBZeroValues.map (fun n => n + 1) := by
  rfl

theorem blockDJulia_is_offset :
    blockDJuliaValues = blockDZeroValues.map (fun n => n + 1) := by
  rfl

theorem source_order_contains_exactly_six :
    sourceOrder0 = List.range 6 := by
  rfl

theorem blocks_cover_source_order :
    (blockBZeroValues ++ blockDZeroValues).mergeSort (· ≤ ·) =
      [0, 1, 2, 3, 4, 5] := by
  rfl

theorem blocks_are_disjoint :
    List.Pairwise (· ≠ ·) blockBZeroValues ∧
    List.Pairwise (· ≠ ·) blockDZeroValues ∧
    ∀ b ∈ blockBZeroValues, ∀ d ∈ blockDZeroValues, b ≠ d := by
  decide

#print axioms toJulia_offset
#print axioms fromJulia_offset
#print axioms fromJulia_toJulia
#print axioms toJulia_fromJulia
#print axioms fin6JuliaEquiv_bijective
#print axioms sourceOrder0_exact
#print axioms sourceOrder1_exact
#print axioms sourceOrder1_is_offset
#print axioms blockBZero_exact
#print axioms blockDZero_exact
#print axioms blockBJulia_exact
#print axioms blockDJulia_exact
#print axioms blockBJulia_is_offset
#print axioms blockDJulia_is_offset
#print axioms source_order_contains_exactly_six
#print axioms blocks_cover_source_order
#print axioms blocks_are_disjoint

end
end RouteBFin6IndexAdapter

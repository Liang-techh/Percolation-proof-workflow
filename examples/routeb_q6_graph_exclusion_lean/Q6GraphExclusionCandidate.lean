import Mathlib.Algebra.Module.Equiv.Defs
import Mathlib.Algebra.Module.Pi

/-!
GH-LEAN-P4-Q6-GRAPH-EXCLUSION: OPEN_UNCOMPILED / pending.
Abstract linear block equations only. No physical source import or admission.
No Lean/Lake execution accompanied these candidate proof bodies.
-/
set_option autoImplicit false

namespace Q6GraphExclusionCandidate

section AbstractBlocks

variable {K D C : Type*} [Semiring K]
variable [AddCommMonoid D] [AddCommMonoid C] [Module K D] [Module K C]

/-- Only injectivity of the eliminated block is needed for this implication. -/
theorem zero_C_forces_zero_D
    (M_DD : D →ₗ[K] D) (M_DC : C →ₗ[K] D)
    (alpha_D : D) (alpha_C : C) (R_D : D)
    (hDD : Function.Injective M_DD)
    (hD : M_DD alpha_D + M_DC alpha_C = R_D)
    (hRD : R_D = 0) (hAC : alpha_C = 0) : alpha_D = 0 := by
  have hz : M_DD alpha_D = 0 := by
    simpa only [hAC, hRD, map_zero, add_zero] using hD
  apply hDD
  exact hz.trans (map_zero M_DD).symm

/-- Both block rows refer to the same pair of vectors. -/
theorem zero_C_forces_zero_rhs
    (M_DD : D →ₗ[K] D) (M_DC : C →ₗ[K] D)
    (M_CD : D →ₗ[K] C) (M_CC : C →ₗ[K] C)
    (alpha_D : D) (alpha_C R_C : C) (R_D : D)
    (hDD : Function.Injective M_DD)
    (hD : M_DD alpha_D + M_DC alpha_C = R_D)
    (hC : M_CD alpha_D + M_CC alpha_C = R_C)
    (hRD : R_D = 0) (hAC : alpha_C = 0) : R_C = 0 := by
  have hAD := zero_C_forces_zero_D M_DD M_DC alpha_D alpha_C R_D hDD hD hRD hAC
  simpa only [hAD, hAC, map_zero, zero_add] using hC.symm

theorem nonzero_rhs_forces_nonzero_C
    (M_DD : D →ₗ[K] D) (M_DC : C →ₗ[K] D)
    (M_CD : D →ₗ[K] C) (M_CC : C →ₗ[K] C)
    (alpha_D : D) (alpha_C R_C : C) (R_D : D)
    (hDD : Function.Injective M_DD)
    (hD : M_DD alpha_D + M_DC alpha_C = R_D)
    (hC : M_CD alpha_D + M_CC alpha_C = R_C)
    (hRD : R_D = 0) (hRC : R_C ≠ 0) : alpha_C ≠ 0 := by
  intro hAC
  exact hRC (zero_C_forces_zero_rhs M_DD M_DC M_CD M_CC
    alpha_D alpha_C R_C R_D hDD hD hC hRD hAC)

end AbstractBlocks

section ThreeByThree

variable {K : Type*} [Semiring K]

abbrev Vec3 (K : Type*) := Fin 3 → K

/-- A linear equivalence supplies invertibility of the 3-by-3 D block. -/
theorem fin3_zero_C_forces_zero_rhs
    (M_DD : Vec3 K ≃ₗ[K] Vec3 K)
    (M_DC M_CD M_CC : Vec3 K →ₗ[K] Vec3 K)
    (alpha_D alpha_C R_D R_C : Vec3 K)
    (hD : M_DD alpha_D + M_DC alpha_C = R_D)
    (hC : M_CD alpha_D + M_CC alpha_C = R_C)
    (hRD : R_D = 0) (hAC : alpha_C = 0) : R_C = 0 := by
  exact zero_C_forces_zero_rhs M_DD.toLinearMap M_DC M_CD M_CC
    alpha_D alpha_C R_C R_D M_DD.injective hD hC hRD hAC

theorem fin3_nonzero_rhs_forces_nonzero_C
    (M_DD : Vec3 K ≃ₗ[K] Vec3 K)
    (M_DC M_CD M_CC : Vec3 K →ₗ[K] Vec3 K)
    (alpha_D alpha_C R_D R_C : Vec3 K)
    (hD : M_DD alpha_D + M_DC alpha_C = R_D)
    (hC : M_CD alpha_D + M_CC alpha_C = R_C)
    (hRD : R_D = 0) (hRC : R_C ≠ 0) : alpha_C ≠ 0 := by
  intro hAC
  exact hRC (fin3_zero_C_forces_zero_rhs M_DD M_DC M_CD M_CC
    alpha_D alpha_C R_D R_C hD hC hRD hAC)

end ThreeByThree

end Q6GraphExclusionCandidate

import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.Tactic

-- Lean 4.32 / pinned Mathlib no longer exports the legacy matrix-vector notation
-- used by this source-independent skeleton. Restore it locally without changing
-- any matrix/vector semantics.
infixl:72 " *ᵥ " => Matrix.mulVec

/-!
T-P4-032 -- UNCOMPILED SOURCE-INDEPENDENT TYPED SKELETON.
No Lean/Lake execution, deployed solve identity, source binding or coverage.
Ordered physical split B=(4,5), D=(1,2,3,6); internal Fin indices are zero-based.
This standalone file does not import or change the old O1 candidate.
-/

set_option autoImplicit false

namespace RouteBP4032BlockDefects

open scoped BigOperators

abbrev Vec6 := Fin 6 → ℝ
abbrev BVec := Fin 2 → ℝ
abbrev DVec := Fin 4 → ℝ
abbrev Mat6 := Matrix (Fin 6) (Fin 6) ℝ
abbrev BB := Matrix (Fin 2) (Fin 2) ℝ
abbrev BD := Matrix (Fin 2) (Fin 4) ℝ
abbrev DB := Matrix (Fin 4) (Fin 2) ℝ
abbrev DD := Matrix (Fin 4) (Fin 4) ℝ

def bIdx : Fin 2 → Fin 6 := ![3, 4]
def dIdx : Fin 4 → Fin 6 := ![0, 1, 2, 5]

theorem bIdx_injective : Function.Injective bIdx := by decide
theorem dIdx_injective : Function.Injective dIdx := by decide
theorem blocks_disjoint : ∀ i j, bIdx i ≠ dIdx j := by decide
theorem blocks_cover : ∀ k : Fin 6, (∃ j, dIdx j = k) ∨ (∃ i, bIdx i = k) := by decide

def projB (x : Vec6) : BVec := fun i => x (bIdx i)
def projD (x : Vec6) : DVec := fun i => x (dIdx i)
def blockBB (M : Mat6) : BB := fun i j => M (bIdx i) (bIdx j)
def blockBD (M : Mat6) : BD := fun i j => M (bIdx i) (dIdx j)
def blockDB (M : Mat6) : DB := fun i j => M (dIdx i) (bIdx j)
def blockDD (M : Mat6) : DD := fun i j => M (dIdx i) (dIdx j)

/-- Exact finite-sum partition, including axis 6 as the LAST D coordinate. -/
theorem sum_partition (f : Fin 6 → ℝ) :
    (∑ k, f k) = (∑ j : Fin 4, f (dIdx j)) + (∑ i : Fin 2, f (bIdx i)) := by
  simp [Fin.sum_univ_succ, bIdx, dIdx]
  ring

noncomputable section

theorem projD_mulVec (M : Mat6) (a : Vec6) :
    projD (M *ᵥ a) = blockDD M *ᵥ projD a + blockDB M *ᵥ projB a := by
  funext i
  simpa only [projD, projB, blockDD, blockDB, Matrix.mulVec, dotProduct, Pi.add_apply]
    using sum_partition (fun j => M (dIdx i) j * a j)

theorem projB_mulVec (M : Mat6) (a : Vec6) :
    projB (M *ᵥ a) = blockBB M *ᵥ projB a + blockBD M *ᵥ projD a := by
  funext i
  simpa only [projD, projB, blockBD, blockBB, Matrix.mulVec, dotProduct,
    Pi.add_apply, add_comm]
    using sum_partition (fun j => M (bIdx i) j * a j)

/-- The SAME aB must occur in actual and reference balances. Differences in
reference block acceleration require another explicit defect term. -/
theorem distal_difference_identity (MDD M0DD : DD) (MDB M0DB : DB)
    (aD aD0 : DVec) (aB : BVec) (FD F0D : DVec)
    (hAct : MDD *ᵥ aD + MDB *ᵥ aB = FD)
    (hRef : M0DD *ᵥ aD0 + M0DB *ᵥ aB = F0D) :
    MDD *ᵥ (aD - aD0) + (MDB - M0DB) *ᵥ aB =
      (FD - F0D) - (MDD - M0DD) *ᵥ aD0 := by
  funext i
  have hA := congrFun hAct i
  have hR := congrFun hRef i
  simp only [Matrix.mulVec_sub, Matrix.sub_mulVec, Pi.add_apply, Pi.sub_apply] at hA hR ⊢
  linarith

def canonicalDistalDefect (M M0 : Mat6) (a0 F F0 : Vec6) : DVec :=
  (projD F - projD F0) - (blockDD M - blockDD M0) *ᵥ projD a0

/-- Full six-axis equations are hypotheses, NOT consequences of a Float64 solve. -/
theorem projected_distal_defect (M M0 : Mat6) (a a0 F F0 : Vec6)
    (hAct : M *ᵥ a = F) (hRef : M0 *ᵥ a0 = F0)
    (hSameB : projB a0 = projB a) :
    blockDD M *ᵥ (projD a - projD a0) +
      (blockDB M - blockDB M0) *ᵥ projB a = canonicalDistalDefect M M0 a0 F F0 := by
  have hA := congrArg projD hAct
  have hR := congrArg projD hRef
  rw [projD_mulVec] at hA hR
  rw [hSameB] at hR
  exact distal_difference_identity (blockDD M) (blockDD M0) (blockDB M) (blockDB M0)
    (projD a) (projD a0) (projB a) (projD F) (projD F0) hA hR

theorem zero_distal_of_compatibility (MDD M0DD : DD) (MDB M0DB : DB)
    (aD aD0 : DVec) (aB : BVec) (FD F0D : DVec)
    (hAct : MDD *ᵥ aD + MDB *ᵥ aB = FD)
    (hRef : M0DD *ᵥ aD0 + M0DB *ᵥ aB = F0D)
    (hCompatible : FD - F0D = (MDD - M0DD) *ᵥ aD0) :
    MDD *ᵥ (aD - aD0) + (MDB - M0DB) *ᵥ aB = 0 := by
  rw [distal_difference_identity MDD M0DD MDB M0DB aD aD0 aB FD F0D hAct hRef,
    hCompatible, sub_self]

/-- Right-associated matrix product, with its forced leading minus sign.
No commutation of factors, inverse construction, symmetry or PSD assumption. -/
def Rport (MBD : BD) (MDDinv : DD) (DeltaMDB : DB) : BB :=
  -(MBD * (MDDinv * DeltaMDB))

theorem port_identity_with_defects (MDD MDDinv : DD) (DeltaMDB : DB) (MBD : BD)
    (delta_a_D eD : DVec) (aB rB eB : BVec)
    (hInv : MDDinv * MDD = (1 : DD))
    (hD : MDD *ᵥ delta_a_D + DeltaMDB *ᵥ aB = eD)
    (hB : rB - MBD *ᵥ delta_a_D = eB) :
    rB = Rport MBD MDDinv DeltaMDB *ᵥ aB + (MBD * MDDinv) *ᵥ eD + eB := by
  have hDleft := congrArg (fun x : DVec => MDDinv *ᵥ x) hD
  have hsolve : delta_a_D + (MDDinv * DeltaMDB) *ᵥ aB = MDDinv *ᵥ eD := by
    simpa only [Matrix.mulVec_add, Matrix.mulVec_mulVec, hInv, Matrix.one_mulVec] using hDleft
  have hPort := congrArg (fun x : DVec => MBD *ᵥ x) hsolve
  have hPort' : MBD *ᵥ delta_a_D + (MBD * (MDDinv * DeltaMDB)) *ᵥ aB =
      (MBD * MDDinv) *ᵥ eD := by
    simpa only [Matrix.mulVec_add, Matrix.mulVec_mulVec] using hPort
  funext i
  have hp := congrFun hPort' i
  have hb := congrFun hB i
  simp only [Rport, Matrix.neg_mulVec, Pi.neg_apply, Pi.add_apply, Pi.sub_apply] at hp hb ⊢
  linarith

theorem zero_defect_port_identity (MDD MDDinv : DD) (DeltaMDB : DB) (MBD : BD)
    (delta_a_D : DVec) (aB rB : BVec)
    (hInv : MDDinv * MDD = (1 : DD))
    (hD : MDD *ᵥ delta_a_D + DeltaMDB *ᵥ aB = 0)
    (hB : rB - MBD *ᵥ delta_a_D = 0) : rB = Rport MBD MDDinv DeltaMDB *ᵥ aB := by
  simpa only [Matrix.mulVec_zero, add_zero] using
    port_identity_with_defects MDD MDDinv DeltaMDB MBD delta_a_D 0 aB rB 0 hInv hD hB

/-- Full conditional source-to-port algebra, with the canonical distal defect
kept intact. F/F0 may contain all controller, ramp and distal-force differences. -/
theorem full_equations_to_port (M M0 : Mat6) (MDDinv : DD)
    (a a0 F F0 : Vec6) (rB eB : BVec)
    (hAct : M *ᵥ a = F) (hRef : M0 *ᵥ a0 = F0)
    (hSameB : projB a0 = projB a)
    (hInv : MDDinv * blockDD M = (1 : DD))
    (hB : rB - blockBD M *ᵥ (projD a - projD a0) = eB) :
    rB = Rport (blockBD M) MDDinv (blockDB M - blockDB M0) *ᵥ projB a +
      (blockBD M * MDDinv) *ᵥ canonicalDistalDefect M M0 a0 F F0 + eB :=
  port_identity_with_defects (blockDD M) MDDinv (blockDB M - blockDB M0) (blockBD M)
    (projD a - projD a0) (canonicalDistalDefect M M0 a0 F F0) (projB a) rB eB hInv
    (projected_distal_defect M M0 a a0 F F0 hAct hRef hSameB) hB

/- Distinct wrappers prevent automatic substitution based on equal vector sizes.
They do NOT authenticate the physical units or source origin of wrapped values. -/
structure BlockAcceleration where
  value : BVec
structure DistalAccelerationCorrection where
  value : DVec
structure DistalGeneralizedForce where
  value : DVec
structure PortGeneralizedForce where
  value : BVec
structure RawPMIForce where
  value : BVec

def pmiForceMap : BB := ![![(1 / 5 : ℝ), 0], ![0, (1 / 10 : ℝ)]]

/-- One explicit upstream conversion. A PortGeneralizedForce is NOT an input
to this function. Mass-block actions and Rport never apply this map again. -/
def normalizeRawPMI (raw : RawPMIForce) : PortGeneralizedForce :=
  ⟨pmiForceMap *ᵥ raw.value⟩

def portFromAcceleration (MBD : BD) (daD : DistalAccelerationCorrection) :
    PortGeneralizedForce := ⟨MBD *ᵥ daD.value⟩

theorem normalization_components (raw : RawPMIForce) :
    (normalizeRawPMI raw).value 0 = raw.value 0 / 5 ∧
    (normalizeRawPMI raw).value 1 = raw.value 1 / 10 := by
  constructor <;> simp [normalizeRawPMI, pmiForceMap, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

theorem typed_port_identity (MDD MDDinv : DD) (DeltaMDB : DB) (MBD : BD)
    (daD : DistalAccelerationCorrection) (aB : BlockAcceleration)
    (eD : DistalGeneralizedForce) (rB eB : PortGeneralizedForce)
    (hInv : MDDinv * MDD = (1 : DD))
    (hD : MDD *ᵥ daD.value + DeltaMDB *ᵥ aB.value = eD.value)
    (hB : rB.value - (portFromAcceleration MBD daD).value = eB.value) :
    rB.value = Rport MBD MDDinv DeltaMDB *ᵥ aB.value +
      (MBD * MDDinv) *ᵥ eD.value + eB.value :=
  port_identity_with_defects MDD MDDinv DeltaMDB MBD daD.value eD.value
    aB.value rB.value eB.value hInv hD hB

end

-- Future audit commands only; NOT executed in this round.
#print axioms blocks_cover
#print axioms sum_partition
#print axioms projD_mulVec
#print axioms projB_mulVec
#print axioms distal_difference_identity
#print axioms projected_distal_defect
#print axioms zero_distal_of_compatibility
#print axioms port_identity_with_defects
#print axioms zero_defect_port_identity
#print axioms full_equations_to_port
#print axioms normalization_components
#print axioms typed_port_identity

end RouteBP4032BlockDefects

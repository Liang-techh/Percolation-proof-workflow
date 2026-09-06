import SignedGap
import GravityTwistFloor
import Mathlib.Tactic.FinCases

set_option autoImplicit false
open scoped BigOperators

namespace RouteBActualEnergyStorage
noncomputable section
open RouteBSignedGap

/-- Literal entries of coupled reference run-20260905T192654Z-3dbe159f.
    Fin indices 0,...,5 correspond to physical axes 1,...,6. -/
def M0 : Mat 6 := ![
  ![2355503/3000000, -1481/80000, -103/16000, 7/60, -21/80000, 1/60],
  ![-1481/80000, 6986497/12000000, 677771/2400000, 0, 41827/800000, 0],
  ![-103/16000, 677771/2400000, 3064417/12000000, 0, 8189/160000, 0],
  ![7/60, 0, 0, 350003/3000000, 0, 1/60],
  ![-21/80000, 41827/800000, 8189/160000, 0, 200739/4000000, 0],
  ![1/60, 0, 0, 1/60, 0, 50003/3000000]]

def H0 : Mat 6 := ![
  ![0,0,0,0,0,0],
  ![0,-2029689/400000,-101043/80000,0,-20601/400000,0],
  ![0,-101043/80000,-101043/80000,0,-20601/400000,0],
  ![0,0,0,0,0,0],
  ![0,-20601/400000,-20601/400000,0,-20601/400000,0],
  ![0,0,0,0,0,0]]

def normSq (v : Vec 6) : ℝ := ∑ i, v i ^ 2
def rowAbs (i : Fin 6) : ℝ := ∑ j, |M0 i j|

theorem M0_symmetric : Symmetric M0 := by
  intro i j
  fin_cases i <;> fin_cases j <;> norm_num [M0]

theorem H0_symmetric : Symmetric H0 := by
  intro i j
  fin_cases i <;> fin_cases j <;> norm_num [H0]

/-- Every absolute row sum is strictly below one, checked in exact rationals. -/
theorem rowAbs_lt_one (i : Fin 6) : rowAbs i < 1 := by
  fin_cases i <;> norm_num [rowAbs, M0, Fin.sum_univ_succ]

def offDiagonalSquares (v : Vec 6) : ℝ :=
    (1481/80000) * (v 0 + v 1)^2
  + (103/16000) * (v 0 + v 2)^2
  + (7/60) * (v 0 - v 3)^2
  + (21/80000) * (v 0 + v 4)^2
  + (1/60) * (v 0 - v 5)^2
  + (677771/2400000) * (v 1 - v 2)^2
  + (41827/800000) * (v 1 - v 4)^2
  + (8189/160000) * (v 2 - v 4)^2
  + (1/60) * (v 3 - v 5)^2

/-- An exact DSOS certificate for I-M0, retaining every off-diagonal entry. -/
theorem M0_dsos_identity (v : Vec 6) :
    normSq v - quad M0 v =
      (∑ i, (1-rowAbs i) * v i^2) + offDiagonalSquares v := by
  norm_num [normSq, quad, dot, mv, rowAbs, M0, offDiagonalSquares,
    Fin.sum_univ_succ]
  <;> ring

theorem M0_le_identity (v : Vec 6) : quad M0 v ≤ normSq v := by
  have hd : 0 ≤ ∑ i, (1-rowAbs i) * v i^2 :=
    Finset.sum_nonneg (fun i _ => mul_nonneg (sub_nonneg.mpr (rowAbs_lt_one i).le)
      (sq_nonneg (v i)))
  have ho : 0 ≤ offDiagonalSquares v := by
    unfold offDiagonalSquares
    positivity
  linarith [M0_dsos_identity v]

theorem kinetic_M0_upper (v : Vec 6) : kinetic M0 v ≤ normSq v / 2 := by
  unfold kinetic
  linarith [M0_le_identity v]

theorem normSq_nonneg (q : Vec 6) : 0 ≤ normSq q :=
  Finset.sum_nonneg (fun i _ => sq_nonneg (q i))

theorem coordinate_sq_le (q : Vec 6) (i : Fin 6) : q i^2 ≤ normSq q :=
  Finset.single_le_sum (fun j _ => sq_nonneg (q j)) (Finset.mem_univ i)

def referencePotential (q : Vec 6) : ℝ :=
  RouteBGravityTwistFloor.realFourierPotential (q 1) (q 1+q 2) (q 3) (q 4)

def referenceR (q : Vec 6) : ℝ :=
  RouteBGravityTwistFloor.R (q 1) (q 1+q 2) (q 3) (q 4)

theorem H0_kinetic (q : Vec 6) : kinetic H0 q =
    -(RouteBGravityTwistFloor.A * q 1^2 + RouteBGravityTwistFloor.B * (q 1+q 2)^2 +
      RouteBGravityTwistFloor.C * (q 1+q 2+q 4)^2) / 2 := by
  norm_num [kinetic, quad, dot, mv, H0, Fin.sum_univ_succ,
    RouteBGravityTwistFloor.A, RouteBGravityTwistFloor.B, RouteBGravityTwistFloor.C]
  <;> ring

theorem reference_remainder (q : Vec 6) :
    referencePotential q - RouteBGravityTwistFloor.U0 - kinetic H0 q = referenceR q := by
  rw [H0_kinetic]
  simpa only [sub_neg_eq_add] using
    RouteBGravityTwistFloor.fourier_remainder_identity (q 1) (q 1+q 2) (q 3) (q 4)

theorem referenceR_floor (q : Vec 6) : -(q 3^4)/40 ≤ referenceR q :=
  RouteBGravityTwistFloor.gravity_twist_floor (q 1) (q 1+q 2) (q 3) (q 4)

end
end RouteBActualEnergyStorage

#print axioms RouteBActualEnergyStorage.rowAbs_lt_one
#print axioms RouteBActualEnergyStorage.M0_dsos_identity
#print axioms RouteBActualEnergyStorage.M0_le_identity
#print axioms RouteBActualEnergyStorage.kinetic_M0_upper
#print axioms RouteBActualEnergyStorage.reference_remainder
#print axioms RouteBActualEnergyStorage.referenceR_floor

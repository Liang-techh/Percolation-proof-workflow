import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.Tactic.Linarith

noncomputable section

abbrev DVec (d : Nat) := Fin d → ℝ
abbrev BVec (b : Nat) := Fin b → ℝ

def R_port {d b : Nat}
    (M_BD : Matrix (Fin b) (Fin d) ℝ)
    (M_DD_inv : Matrix (Fin d) (Fin d) ℝ)
    (DeltaM_DB : Matrix (Fin d) (Fin b) ℝ) :
    Matrix (Fin b) (Fin b) ℝ :=
  -(M_BD * M_DD_inv * DeltaM_DB)

theorem routeB_port_identity {d b : Nat}
    (M_DD : Matrix (Fin d) (Fin d) ℝ)
    (M_DD_inv : Matrix (Fin d) (Fin d) ℝ)
    (DeltaM_DB : Matrix (Fin d) (Fin b) ℝ)
    (M_BD : Matrix (Fin b) (Fin d) ℝ)
    (v : DVec d) (a_B : BVec b) (r_B : BVec b)
    (h_inv_left : M_DD_inv * M_DD = (1 : Matrix (Fin d) (Fin d) ℝ))
    (h_D : M_DD.mulVec v + DeltaM_DB.mulVec a_B = 0)
    (h_B : r_B - M_BD.mulVec v = 0) :
    (R_port M_BD M_DD_inv DeltaM_DB).mulVec a_B = r_B := by
  have hD_left := congrArg
    (fun x : DVec d => M_DD_inv *ᵥ x) h_D

  have hsolve :
      v + M_DD_inv *ᵥ (DeltaM_DB *ᵥ a_B) = 0 := by
    simpa only [Matrix.mulVec_add, Matrix.mulVec_zero,
      Matrix.mulVec_mulVec, h_inv_left, Matrix.one_mulVec] using hD_left

  have hB_left :
      M_BD *ᵥ v +
        (M_BD * M_DD_inv * DeltaM_DB) *ᵥ a_B = 0 := by
    have h := congrArg
      (fun x : DVec d => M_BD *ᵥ x) hsolve
    simpa only [Matrix.mulVec_add, Matrix.mulVec_zero,
      Matrix.mulVec_mulVec, Matrix.mul_assoc] using h

  have hremote :
      M_BD *ᵥ v =
        -((M_BD * M_DD_inv * DeltaM_DB) *ᵥ a_B) := by
    funext i
    linarith [congrFun hB_left i]

  have hresidual : r_B = M_BD *ᵥ v := by
    funext i
    linarith [congrFun h_B i]

  calc
    (R_port M_BD M_DD_inv DeltaM_DB).mulVec a_B =
        -((M_BD * M_DD_inv * DeltaM_DB) *ᵥ a_B) := by
      rw [R_port, Matrix.neg_mulVec]
    _ = M_BD *ᵥ v := hremote.symm
    _ = r_B := hresidual

import NEW_P4_032_BlockDefects

/-!
UNCOMPILED source-independent Schur elimination skeleton.
No Lean/Lake run, matrix inverse construction, source solve or coverage claim.
Uses only the explicit LEFT inverse, with the inherited ordered B/D blocks.
No symmetry/PSD and no defect norm or quadratic-load argument.
-/

set_option autoImplicit false

namespace RouteBP4032SchurElimination

open RouteBP4032BlockDefects

noncomputable section

/-- T:D-force -> B-force. Multiplication order is fixed. -/
def transfer (M : Mat6) (MDDinv : DD) : BD := blockBD M * MDDinv

/-- Right-associated Schur coefficient, with shapes (2x4)(4x4)(4x2). -/
def schur (M : Mat6) (MDDinv : DD) : BB :=
  blockBB M - blockBD M * (MDDinv * blockDB M)

def eliminate (M : Mat6) (MDDinv : DD) (x : Vec6) : BVec :=
  projB x - transfer M MDDinv *ᵥ projD x

/-- The requested finite-dimensional identity; the imported projections fix
B=(4,5), D=(1,2,3,6). Matrix association is normalized, never commuted. -/
theorem schur_projection_identity (M : Mat6) (MDDinv : DD) (a : Vec6)
    (hInv : MDDinv * blockDD M = (1 : DD)) :
    projB (M *ᵥ a) - (blockBD M * MDDinv) *ᵥ projD (M *ᵥ a) =
      schur M MDDinv *ᵥ projB a := by
  have hD : (blockBD M * MDDinv) *ᵥ projD (M *ᵥ a) =
      blockBD M *ᵥ projD a +
        (blockBD M * (MDDinv * blockDB M)) *ᵥ projB a := by
    rw [projD_mulVec]
    simp only [Matrix.mulVec_add, Matrix.mulVec_mulVec, Matrix.mul_assoc,
      hInv, Matrix.mul_one]
  rw [hD, projB_mulVec]
  unfold schur
  rw [Matrix.sub_mulVec]
  funext i
  simp only [Pi.add_apply, Pi.sub_apply]
  ring

/-- Public statement in left-associated coefficient notation, matching the
usual MBB-MBD*MDDinv*MDB display. Only associativity relates the two forms. -/
theorem schur_projection_left_associated (M : Mat6) (MDDinv : DD) (a : Vec6)
    (hInv : MDDinv * blockDD M = (1 : DD)) :
    projB (M *ᵥ a) - (blockBD M * MDDinv) *ᵥ projD (M *ᵥ a) =
      (blockBB M - blockBD M * MDDinv * blockDB M) *ᵥ projB a := by
  simpa only [schur, Matrix.mul_assoc] using schur_projection_identity M MDDinv a hInv

theorem eliminate_add (M : Mat6) (MDDinv : DD) (x y : Vec6) :
    eliminate M MDDinv (x + y) = eliminate M MDDinv x + eliminate M MDDinv y := by
  have hB : projB (x + y) = projB x + projB y := rfl
  have hD : projD (x + y) = projD x + projD y := rfl
  unfold eliminate
  rw [hB, hD, Matrix.mulVec_add]
  funext i
  simp only [Pi.add_apply, Pi.sub_apply]
  ring

/-- Full exact balance with a retained force defect: M*a=F+e.
No backslash/Float64 equation is inferred by this theorem. -/
theorem forcing_with_defect (M : Mat6) (MDDinv : DD) (a F e : Vec6)
    (hInv : MDDinv * blockDD M = (1 : DD)) (hBalance : M *ᵥ a = F + e) :
    schur M MDDinv *ᵥ projB a =
      (projB F - transfer M MDDinv *ᵥ projD F) +
      (projB e - transfer M MDDinv *ᵥ projD e) := by
  calc
    schur M MDDinv *ᵥ projB a = eliminate M MDDinv (M *ᵥ a) :=
      (schur_projection_identity M MDDinv a hInv).symm
    _ = eliminate M MDDinv (F + e) := by rw [hBalance]
    _ = _ := eliminate_add M MDDinv F e

/-- Defect-free forcing corollary remains conditional on the exact full balance. -/
theorem forcing_identity (M : Mat6) (MDDinv : DD) (a F : Vec6)
    (hInv : MDDinv * blockDD M = (1 : DD)) (hBalance : M *ᵥ a = F) :
    schur M MDDinv *ᵥ projB a = projB F - transfer M MDDinv *ᵥ projD F := by
  calc
    schur M MDDinv *ᵥ projB a = eliminate M MDDinv (M *ᵥ a) :=
      (schur_projection_identity M MDDinv a hInv).symm
    _ = eliminate M MDDinv F := by rw [hBalance]
    _ = _ := rfl

/-- A canonical algebraic defect can always be retained; this definition does
not measure or bound a deployed numerical solve error. -/
def balanceDefect (M : Mat6) (a F : Vec6) : Vec6 := M *ᵥ a - F

theorem canonical_forcing_defect (M : Mat6) (MDDinv : DD) (a F : Vec6)
    (hInv : MDDinv * blockDD M = (1 : DD)) :
    schur M MDDinv *ᵥ projB a = eliminate M MDDinv F +
      eliminate M MDDinv (balanceDefect M a F) := by
  have hBalance : M *ᵥ a = F + balanceDefect M a F := by
    unfold balanceDefect
    abel
  exact forcing_with_defect M MDDinv a F (balanceDefect M a F) hInv hBalance

/-- Blockwise forcing convention is explicit: both defects are ADDED on the
force side. Consequently the condensed defect is eB-T*eD, not eB+T*eD. -/
theorem block_forcing_with_defects (M : Mat6) (MDDinv : DD)
    (aB FB eB : BVec) (aD FD eD : DVec)
    (hInv : MDDinv * blockDD M = (1 : DD))
    (hB : blockBB M *ᵥ aB + blockBD M *ᵥ aD = FB + eB)
    (hD : blockDD M *ᵥ aD + blockDB M *ᵥ aB = FD + eD) :
    schur M MDDinv *ᵥ aB =
      (FB - transfer M MDDinv *ᵥ FD) + (eB - transfer M MDDinv *ᵥ eD) := by
  have hApply := congrArg (fun x : DVec => transfer M MDDinv *ᵥ x) hD
  have hElim : blockBD M *ᵥ aD +
      (blockBD M * (MDDinv * blockDB M)) *ᵥ aB =
        transfer M MDDinv *ᵥ FD + transfer M MDDinv *ᵥ eD := by
    simpa only [transfer, Matrix.mulVec_add, Matrix.mulVec_mulVec,
      Matrix.mul_assoc, hInv, Matrix.mul_one] using hApply
  unfold schur
  rw [Matrix.sub_mulVec]
  funext i
  have hb := congrFun hB i
  have hd := congrFun hElim i
  simp only [Pi.add_apply, Pi.sub_apply] at hb hd ⊢
  linarith

end

-- Future audit commands only; NOT executed in this round.
#print axioms schur_projection_identity
#print axioms schur_projection_left_associated
#print axioms eliminate_add
#print axioms forcing_with_defect
#print axioms forcing_identity
#print axioms canonical_forcing_defect
#print axioms block_forcing_with_defects

end RouteBP4032SchurElimination

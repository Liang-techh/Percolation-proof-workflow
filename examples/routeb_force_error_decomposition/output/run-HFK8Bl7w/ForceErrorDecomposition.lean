import DHPowerBinding
import BlockPotential

open scoped BigOperators

namespace RouteBForceErrorDecomposition

noncomputable section

open RouteBDHPowerBinding

abbrev Block := Fin 2
abbrev Remote := Fin 4
abbrev BlockMat := Block → Block → ℝ

def blockIndex : Block → Fin 6 := ![3, 4]
def remoteIndex : Remote → Fin 6 := ![0, 1, 2, 5]

def referenceAction (R : BlockMat) (a : Vec) (i : Block) : ℝ :=
  ∑ j, R i j * a (blockIndex j)

def actualBlockAction (M : Mat) (a : Vec) (i : Block) : ℝ :=
  ∑ j : Block, M (blockIndex i) (blockIndex j) * a (blockIndex j)

def remoteAction (M : Mat) (a : Vec) (i : Block) : ℝ :=
  ∑ j : Remote, M (blockIndex i) (remoteIndex j) * a (remoteIndex j)

def massMismatch (R : BlockMat) (M : Mat) (a : Vec) (i : Block) : ℝ :=
  ∑ j, (R i j - M (blockIndex i) (blockIndex j)) * a (blockIndex j)

def controlLoad (kp q v : Vec) (w : ℝ) (i : Block) : ℝ :=
  kp (blockIndex i) * q (blockIndex i) +
  RouteBSupplyCore.damping (blockIndex i) * v (blockIndex i) -
  RouteBSupplyCore.disturbance (blockIndex i) * w

def referenceForce (R : BlockMat) (kp q v a : Vec) (w : ℝ) (i : Block) : ℝ :=
  referenceAction R a i + controlLoad kp q v w i

theorem full_mass_block_split (M : Mat) (a : Vec) (i : Block) :
    matVec M a (blockIndex i) = actualBlockAction M a i + remoteAction M a i := by
  norm_num [matVec, actualBlockAction, remoteAction, blockIndex, remoteIndex,
    Fin.sum_univ_six, Fin.sum_univ_two, Fin.sum_univ_four,
    Matrix.cons_val_two, Matrix.cons_val_three, Matrix.vecHead, Matrix.vecTail]
  ring

theorem mass_mismatch_action (R : BlockMat) (M : Mat) (a : Vec) (i : Block) :
    massMismatch R M a i = referenceAction R a i - actualBlockAction M a i := by
  simp only [massMismatch, referenceAction, actualBlockAction,
    sub_mul, Finset.sum_sub_distrib]

/- Generic indexed block identity; eta may be zero or an implementation defect. -/
theorem reference_force_of_balance
    (R : BlockMat) (M : Mat) (kp q v a g0 c grav : Vec) (w : ℝ)
    (eta : Block → ℝ) (i : Block)
    (h : matVec M a (blockIndex i) + c (blockIndex i) + grav (blockIndex i) =
      controller kp q v g0 w (blockIndex i) + eta i) :
    referenceForce R kp q v a w i =
      massMismatch R M a i - remoteAction M a i -
      c (blockIndex i) - grav (blockIndex i) + g0 (blockIndex i) + eta i := by
  have hs := full_mass_block_split M a i
  rw [mass_mismatch_action]
  unfold referenceForce controlLoad
  unfold controller at h
  linarith

theorem implemented_reference_force
    (R : BlockMat) (Ma Mi : Mat) (kp q v a g0 tauI cA cI gA gI : Vec)
    (w : ℝ) (i : Block) :
    referenceForce R kp q v a w i =
      massMismatch R Ma a i - remoteAction Ma a i -
      cA (blockIndex i) - gA (blockIndex i) + g0 (blockIndex i) +
      forceError Ma Mi a (controller kp q v g0 w) tauI cA cI gA gI (blockIndex i) := by
  apply reference_force_of_balance
  exact implemented_force_identity Ma Mi a (controller kp q v g0 w)
    tauI cA cI gA gI (blockIndex i)

def oldTotal (R : BlockMat) (a : Vec) (nominalForce port : Block → ℝ)
    (i : Block) : ℝ := nominalForce i - referenceAction R a i + port i

def nominalOffset (kp q v : Vec) (w : ℝ) (nominalForce : Block → ℝ)
    (i : Block) : ℝ := nominalForce i + controlLoad kp q v w i

theorem new_error_from_old_total
    (R : BlockMat) (kp q v a : Vec) (w : ℝ)
    (nominalForce port : Block → ℝ) (i : Block) :
    referenceForce R kp q v a w i =
      nominalOffset kp q v w nominalForce i + port i - oldTotal R a nominalForce port i := by
  unfold referenceForce nominalOffset oldTotal
  ring

/- No triangle/Young/Cauchy split: preserve all correlations exactly. -/
theorem exact_squared_error_identity
    (R : BlockMat) (kp q v a : Vec) (w : ℝ)
    (nominalForce port : Block → ℝ) (i : Block) :
    referenceForce R kp q v a w i ^ 2 =
      nominalOffset kp q v w nominalForce i ^ 2 + port i ^ 2 +
      oldTotal R a nominalForce port i ^ 2 +
      2 * nominalOffset kp q v w nominalForce i * port i -
      2 * nominalOffset kp q v w nominalForce i * oldTotal R a nominalForce port i -
      2 * port i * oldTotal R a nominalForce port i := by
  rw [new_error_from_old_total]
  ring

def gravityScale : ℝ := 20601 / 400000
def gravity4 (s x y : ℝ) : ℝ := gravityScale * Real.sin s * Real.sin x * Real.sin y
def gravity5 (s x y : ℝ) : ℝ :=
  -gravityScale * (Real.cos s * Real.sin y + Real.sin s * Real.cos x * Real.cos y)

theorem gravity_at_block_origin (s : ℝ) :
    gravity4 s 0 0 = 0 ∧ gravity5 s 0 0 = -gravityScale * Real.sin s := by
  simp [gravity4, gravity5]

end

#print axioms full_mass_block_split
#print axioms mass_mismatch_action
#print axioms reference_force_of_balance
#print axioms implemented_reference_force
#print axioms new_error_from_old_total
#print axioms exact_squared_error_identity
#print axioms gravity_at_block_origin

end RouteBForceErrorDecomposition

import NEW_P4_032_BlockDefects
import Mathlib.Analysis.InnerProductSpace.PiL2

/-!
UNCOMPILED source-independent defect norm-budget skeleton.
No Lean/Lake run, source instance, numeric operator estimate or solve claim.
All norms below are explicitly Euclidean l2, not the default Pi sup norm.
The imported block-identity skeleton is also still uncompiled.
-/

set_option autoImplicit false

namespace RouteBP4032DefectNormBudget

open RouteBP4032BlockDefects

noncomputable section

def norm2 {n : ℕ} (v : Fin n → ℝ) : ℝ :=
  ‖(WithLp.toLp 2 v : EuclideanSpace ℝ (Fin n))‖

theorem norm2_nonnegative {n : ℕ} (v : Fin n → ℝ) : 0 ≤ norm2 v := norm_nonneg _

theorem norm2_add {n : ℕ} (v w : Fin n → ℝ) :
    norm2 (v + w) ≤ norm2 v + norm2 w := by
  simpa only [norm2, WithLp.toLp_add] using
    norm_add (WithLp.toLp 2 v : EuclideanSpace ℝ (Fin n)) (WithLp.toLp 2 w)

/-- First seam: keep all three actual force terms, with no zero-defect premise. -/
theorem defect_triangle (R : BB) (T : BD) (aB rB eB : BVec) (eD : DVec)
    (identity : rB = R *ᵥ aB + T *ᵥ eD + eB) :
    norm2 rB ≤ norm2 (R *ᵥ aB) + norm2 (T *ᵥ eD) + norm2 eB := by
  rw [identity]
  exact (norm2_add (R *ᵥ aB + T *ᵥ eD) eB).trans
    (add_le_add_right (norm2_add (R *ᵥ aB) (T *ᵥ eD)) (norm2 eB))

/-- Direct scalar caps on the three force terms; caps are external evidence. -/
theorem direct_budget (R : BB) (T : BD) (aB rB eB : BVec) (eD : DVec)
    (portCap distalForceCap localForceCap : ℝ)
    (identity : rB = R *ᵥ aB + T *ᵥ eD + eB)
    (hPort : norm2 (R *ᵥ aB) ≤ portCap)
    (hDistal : norm2 (T *ᵥ eD) ≤ distalForceCap)
    (hLocal : norm2 eB ≤ localForceCap) :
    norm2 rB ≤ portCap + distalForceCap + localForceCap :=
  (defect_triangle R T aB rB eB eD identity).trans
    (add_le_add (add_le_add hPort hDistal) hLocal)

/-- A supplied induced-norm upper bound, expressed as a quantified action law.
No equality to an operator norm, numerical spectral calculation, or inverse
conditioning estimate is inferred from the name or value of gain. -/
structure ActionBound {m n : ℕ} (M : Matrix (Fin m) (Fin n) ℝ) (gain : ℝ) : Prop where
  nonnegative : 0 ≤ gain
  bound : ∀ v : Fin n → ℝ, norm2 (M *ᵥ v) ≤ gain * norm2 v

/-- Optional composition of supplied bounds; the direct bound on B*D can be sharper. -/
theorem ActionBound.comp {m n k : ℕ}
    {B : Matrix (Fin m) (Fin n) ℝ} {D : Matrix (Fin n) (Fin k) ℝ}
    {beta eta : ℝ} (hB : ActionBound B beta) (hD : ActionBound D eta) :
    ActionBound (B * D) (beta * eta) where
  nonnegative := mul_nonneg hB.nonnegative hD.nonnegative
  bound v := by
    calc
      norm2 ((B * D) *ᵥ v) = norm2 (B *ᵥ (D *ᵥ v)) := by rw [Matrix.mulVec_mulVec]
      _ ≤ beta * norm2 (D *ᵥ v) := hB.bound _
      _ ≤ beta * (eta * norm2 v) := mul_le_mul_of_nonneg_left (hD.bound v) hB.nonnegative
      _ = (beta * eta) * norm2 v := by ring

/-- Propagate nonzero distal/local defects using an external bound for T.
portCap may come from any certified pointwise port estimate. -/
theorem transported_defect_budget (R : BB) (T : BD) (aB rB eB : BVec) (eD : DVec)
    (portCap tau deltaD deltaB : ℝ)
    (identity : rB = R *ᵥ aB + T *ᵥ eD + eB)
    (hPort : norm2 (R *ᵥ aB) ≤ portCap)
    (hT : ActionBound T tau)
    (hD : norm2 eD ≤ deltaD) (hB : norm2 eB ≤ deltaB) :
    norm2 rB ≤ portCap + tau * deltaD + deltaB := by
  apply direct_budget R T aB rB eB eD portCap (tau * deltaD) deltaB identity hPort
  · exact (hT.bound eD).trans (mul_le_mul_of_nonneg_left hD hT.nonnegative)
  · exact hB

/-- Fully propagated budget. rho and tau are independent supplied action bounds;
alpha,deltaD,deltaB bound different physical quantities and are not interchangeable. -/
theorem operator_budget (R : BB) (T : BD) (aB rB eB : BVec) (eD : DVec)
    (rho tau alpha deltaD deltaB : ℝ)
    (identity : rB = R *ᵥ aB + T *ᵥ eD + eB)
    (hR : ActionBound R rho) (hT : ActionBound T tau)
    (hA : norm2 aB ≤ alpha) (hD : norm2 eD ≤ deltaD) (hB : norm2 eB ≤ deltaB) :
    norm2 rB ≤ rho * alpha + tau * deltaD + deltaB := by
  apply transported_defect_budget R T aB rB eB eD (rho * alpha) tau deltaD deltaB identity
  · exact (hR.bound aB).trans (mul_le_mul_of_nonneg_left hA hR.nonnegative)
  · exact hT
  · exact hD
  · exact hB

/-- Safe squaring keeps the cross terms in the squared total budget. -/
theorem square_budget {n : ℕ} (v : Fin n → ℝ) (cap : ℝ) (h : norm2 v ≤ cap) :
    (norm2 v)^2 ≤ cap^2 := by
  have hn := norm2_nonnegative v
  have hc : 0 ≤ cap := hn.trans h
  have hp := mul_nonneg (sub_nonneg.mpr h) (add_nonneg hc hn)
  nlinarith

/-- O1-specific adapter: R=Rport and T=MBD*MDDinv, with the same defects as
the algebraic identity. Left-inverse evidence is still an external premise. -/
theorem port_defect_norm_budget (MDD MDDinv : DD) (DeltaMDB : DB) (MBD : BD)
    (delta_a_D eD : DVec) (aB rB eB : BVec)
    (rho tau alpha deltaD deltaB : ℝ)
    (hInv : MDDinv * MDD = (1 : DD))
    (hDistal : MDD *ᵥ delta_a_D + DeltaMDB *ᵥ aB = eD)
    (hPort : rB - MBD *ᵥ delta_a_D = eB)
    (hR : ActionBound (Rport MBD MDDinv DeltaMDB) rho)
    (hT : ActionBound (MBD * MDDinv) tau)
    (hA : norm2 aB ≤ alpha) (hD : norm2 eD ≤ deltaD) (hB : norm2 eB ≤ deltaB) :
    norm2 rB ≤ rho * alpha + tau * deltaD + deltaB ∧
      (norm2 rB)^2 ≤ (rho * alpha + tau * deltaD + deltaB)^2 := by
  have hid := port_identity_with_defects MDD MDDinv DeltaMDB MBD
    delta_a_D eD aB rB eB hInv hDistal hPort
  have hb := operator_budget (Rport MBD MDDinv DeltaMDB) (MBD * MDDinv)
    aB rB eB eD rho tau alpha deltaD deltaB hid hR hT hA hD hB
  exact ⟨hb, square_budget rB _ hb⟩

/-- Domain wrapper: every budget refers to the SAME x and external predicate D.
No membership, nonemptiness, trajectory coverage or uniform estimate is constructed. -/
theorem on_domain_budget {X : Type*} (D : X → Prop)
    (R : X → BB) (T : X → BD) (aB rB eB : X → BVec) (eD : X → DVec)
    (rho tau alpha deltaD deltaB : ℝ)
    (identity : ∀ x, D x → rB x = R x *ᵥ aB x + T x *ᵥ eD x + eB x)
    (hR : ∀ x, D x → ActionBound (R x) rho)
    (hT : ∀ x, D x → ActionBound (T x) tau)
    (hA : ∀ x, D x → norm2 (aB x) ≤ alpha)
    (hD : ∀ x, D x → norm2 (eD x) ≤ deltaD)
    (hB : ∀ x, D x → norm2 (eB x) ≤ deltaB) :
    ∀ x, D x → norm2 (rB x) ≤ rho * alpha + tau * deltaD + deltaB := by
  intro x hx
  exact operator_budget (R x) (T x) (aB x) (rB x) (eB x) (eD x)
    rho tau alpha deltaD deltaB (identity x hx) (hR x hx) (hT x hx)
    (hA x hx) (hD x hx) (hB x hx)

end

-- Future audit commands only; NOT executed in this round.
#print axioms norm2_add
#print axioms defect_triangle
#print axioms direct_budget
#print axioms ActionBound.comp
#print axioms transported_defect_budget
#print axioms operator_budget
#print axioms square_budget
#print axioms port_defect_norm_budget
#print axioms on_domain_budget

end RouteBP4032DefectNormBudget

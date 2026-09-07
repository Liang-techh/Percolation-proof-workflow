import NEW_P4_032_SchurElimination

/-!
UNCOMPILED source-independent convention adapter.
No Lean/Lake execution, numerical example, PSD, norm or source/coverage claim.
Distinct types prevent implicit identification of same-named defects.
Reference acceleration and reference DB block below are explicit parameters;
they are not asserted to be any deployed reference model.
-/

set_option autoImplicit false

namespace RouteBP4032DefectConvention

open RouteBP4032BlockDefects
open RouteBP4032SchurElimination

structure ForceSideDefects where
  distal : DVec
  port : BVec

structure O1Defects where
  distal : DVec
  port : BVec

structure O1Variables where
  delta_aD : DVec
  deltaMDB : DB
  rB : BVec
  defects : O1Defects

noncomputable section

def ForceBalances (M : Mat6) (aB FB : BVec) (aD FD : DVec) (f : ForceSideDefects) : Prop :=
  (blockBB M *ᵥ aB + blockBD M *ᵥ aD = FB + f.port) ∧
  (blockDD M *ᵥ aD + blockDB M *ᵥ aB = FD + f.distal)

def O1Balances (M : Mat6) (aB : BVec) (o : O1Variables) : Prop :=
  (blockDD M *ᵥ o.delta_aD + o.deltaMDB *ᵥ aB = o.defects.distal) ∧
  (o.rB - blockBD M *ᵥ o.delta_aD = o.defects.port)

/-- BALANCE adapter, not a mere sign flip of the two defects.
eD_O1 = FD+epsilonD-MDD*aD0-MDB0*aB; eB_O1 = -epsilonB.
The port variable and acceleration/mass differences change at the same time. -/
def adapt (M : Mat6) (aB FB : BVec) (aD aD0 FD : DVec)
    (MDB0 : DB) (f : ForceSideDefects) : O1Variables where
  delta_aD := aD - aD0
  deltaMDB := blockDB M - MDB0
  rB := FB - blockBB M *ᵥ aB - blockBD M *ᵥ aD0
  defects := {
    distal := FD + f.distal - blockDD M *ᵥ aD0 - MDB0 *ᵥ aB
    port := -f.port }

/-- Exact two-way equivalence of the two BALANCE equations under adapt.
No inverse is needed for this change of variables alone. -/
theorem balances_iff (M : Mat6) (aB FB : BVec) (aD aD0 FD : DVec)
    (MDB0 : DB) (f : ForceSideDefects) :
    ForceBalances M aB FB aD FD f ↔ O1Balances M aB (adapt M aB FB aD aD0 FD MDB0 f) := by
  constructor
  · rintro ⟨hB, hD⟩
    constructor
    · funext i
      have h := congrFun hD i
      simp only [adapt, Matrix.mulVec_sub, Matrix.sub_mulVec,
        Pi.add_apply, Pi.sub_apply, Pi.neg_apply] at h ⊢
      linarith
    · funext i
      have h := congrFun hB i
      simp only [adapt, Matrix.mulVec_sub, Matrix.sub_mulVec,
        Pi.add_apply, Pi.sub_apply, Pi.neg_apply] at h ⊢
      linarith
  · rintro ⟨hD, hB⟩
    constructor
    · funext i
      have h := congrFun hB i
      simp only [adapt, Matrix.mulVec_sub, Matrix.sub_mulVec,
        Pi.add_apply, Pi.sub_apply, Pi.neg_apply] at h ⊢
      linarith
    · funext i
      have h := congrFun hD i
      simp only [adapt, Matrix.mulVec_sub, Matrix.sub_mulVec,
        Pi.add_apply, Pi.sub_apply, Pi.neg_apply] at h ⊢
      linarith

def forceRHS (M : Mat6) (J : DD) (FB : BVec) (FD : DVec) (f : ForceSideDefects) : BVec :=
  (FB - transfer M J *ᵥ FD) + (f.port - transfer M J *ᵥ f.distal)

def o1RHS (M : Mat6) (J : DD) (aB : BVec) (o : O1Variables) : BVec :=
  Rport (blockBD M) J o.deltaMDB *ᵥ aB +
    transfer M J *ᵥ o.defects.distal + o.defects.port

/-- A stronger equality of residuals, before either balance is assumed.
Only J*MDD=I cancels the explicit reference acceleration. Matrix actions are
expanded in their given order; scalar ring is used only after taking components. -/
theorem condensed_residual_identity (M : Mat6) (J : DD) (aB FB : BVec)
    (aD aD0 FD : DVec) (MDB0 : DB) (f : ForceSideDefects)
    (hInv : J * blockDD M = (1 : DD)) :
    (adapt M aB FB aD aD0 FD MDB0 f).rB -
      o1RHS M J aB (adapt M aB FB aD aD0 FD MDB0 f) =
      forceRHS M J FB FD f - schur M J *ᵥ aB := by
  have hCancel : J *ᵥ (blockDD M *ᵥ aD0) = aD0 := by
    rw [Matrix.mulVec_mulVec, hInv, Matrix.one_mulVec]
  simp only [adapt, o1RHS, forceRHS, Rport, schur, transfer,
    Matrix.neg_mulVec, Matrix.sub_mulVec, ← Matrix.mulVec_mulVec,
    Matrix.mulVec_sub, Matrix.mulVec_add, hCancel]
  funext i
  simp only [Pi.add_apply, Pi.sub_apply, Pi.neg_apply]
  ring

/-- Condensed identities are equivalent only with these explicit variable
bindings (and the supplied left inverse). No balance proof is presumed here. -/
theorem condensed_iff (M : Mat6) (J : DD) (aB FB : BVec)
    (aD aD0 FD : DVec) (MDB0 : DB) (f : ForceSideDefects)
    (hInv : J * blockDD M = (1 : DD)) :
    schur M J *ᵥ aB = forceRHS M J FB FD f ↔
      (adapt M aB FB aD aD0 FD MDB0 f).rB =
        o1RHS M J aB (adapt M aB FB aD aD0 FD MDB0 f) := by
  have hid := condensed_residual_identity M J aB FB aD aD0 FD MDB0 f hInv
  constructor
  · intro hForce
    apply sub_eq_zero.mp
    rw [hid, hForce, sub_self]
  · intro hO1
    have hz := sub_eq_zero.mpr hO1
    rw [hid] at hz
    exact (sub_eq_zero.mp hz).symm

/-- An independently named O1 record must be explicitly identified with the
adapter output; matching field names or dimensions is not such a proof. -/
theorem identified_condensed_iff (M : Mat6) (J : DD) (aB FB : BVec)
    (aD aD0 FD : DVec) (MDB0 : DB) (f : ForceSideDefects) (o : O1Variables)
    (hInv : J * blockDD M = (1 : DD))
    (hVariables : o = adapt M aB FB aD aD0 FD MDB0 f) :
    schur M J *ᵥ aB = forceRHS M J FB FD f ↔ o.rB = o1RHS M J aB o := by
  rw [hVariables]
  exact condensed_iff M J aB FB aD aD0 FD MDB0 f hInv

/-- Actual invocation of the existing O1 theorem after the balance adapter.
The conclusion concerns the newly defined rB, not an arbitrary deployed residual. -/
theorem o1_from_force_balances (M : Mat6) (J : DD) (aB FB : BVec)
    (aD aD0 FD : DVec) (MDB0 : DB) (f : ForceSideDefects)
    (hInv : J * blockDD M = (1 : DD)) (hForce : ForceBalances M aB FB aD FD f) :
    (adapt M aB FB aD aD0 FD MDB0 f).rB =
      o1RHS M J aB (adapt M aB FB aD aD0 FD MDB0 f) := by
  have hO := (balances_iff M aB FB aD aD0 FD MDB0 f).mp hForce
  exact port_identity_with_defects (blockDD M) J
    (adapt M aB FB aD aD0 FD MDB0 f).deltaMDB (blockBD M)
    (adapt M aB FB aD aD0 FD MDB0 f).delta_aD
    (adapt M aB FB aD aD0 FD MDB0 f).defects.distal aB
    (adapt M aB FB aD aD0 FD MDB0 f).rB
    (adapt M aB FB aD aD0 FD MDB0 f).defects.port hInv hO.1 hO.2

/-- Optional source-reference interpretation of the adapted distal defect.
Reference forcing and reference defect must both be supplied; neither vanishes
merely because a reference acceleration was selected. -/
theorem adapted_distal_with_reference (M : Mat6) (MDD0 : DD) (MDB0 : DB)
    (aB FB : BVec) (aD aD0 FD FD0 epsilonD0 : DVec) (f : ForceSideDefects)
    (hRef : MDD0 *ᵥ aD0 + MDB0 *ᵥ aB = FD0 + epsilonD0) :
    (adapt M aB FB aD aD0 FD MDB0 f).defects.distal =
      (FD - FD0) + (f.distal - epsilonD0) - (blockDD M - MDD0) *ᵥ aD0 := by
  funext i
  have hr := congrFun hRef i
  simp only [adapt, Matrix.sub_mulVec, Pi.add_apply, Pi.sub_apply] at hr ⊢
  linarith

/- Correction-only comparison: this does NOT convert full balance equations. -/
def forceCorrection (T : BD) (f : ForceSideDefects) : BVec := f.port - T *ᵥ f.distal
def o1Correction (T : BD) (o : O1Defects) : BVec := T *ᵥ o.distal + o.port

/-- Necessary AND sufficient relation for arbitrary separately supplied defects
to have equal corrections while keeping T fixed. Kernel cancellation is allowed. -/
theorem corrections_equal_iff (T : BD) (f : ForceSideDefects) (o : O1Defects) :
    forceCorrection T f = o1Correction T o ↔
      T *ᵥ (f.distal + o.distal) = f.port - o.port := by
  constructor <;> intro h <;> funext i
  all_goals
    have hi := congrFun h i
    simp only [forceCorrection, o1Correction, Matrix.mulVec_add,
      Pi.add_apply, Pi.sub_apply] at hi ⊢
    linarith

def correctionOnlySignFlip (f : ForceSideDefects) : O1Defects :=
  ⟨-f.distal, f.port⟩

/-- This sign flip matches only the correction vector, not adapt's residual,
reference, or balance identities; it must not be used as a substitute for adapt. -/
theorem correctionOnlySignFlip_eq (T : BD) (f : ForceSideDefects) :
    forceCorrection T f = o1Correction T (correctionOnlySignFlip f) := by
  simp only [forceCorrection, o1Correction, correctionOnlySignFlip, Matrix.mulVec_neg]
  funext i
  simp only [Pi.add_apply, Pi.sub_apply, Pi.neg_apply]
  ring

/-- Copying both defect values unchanged is valid for the corrections exactly
when T*epsilonD=0, not merely when the names/shapes of the defects agree. -/
theorem unchanged_values_iff (T : BD) (f : ForceSideDefects) :
    forceCorrection T f = o1Correction T ⟨f.distal, f.port⟩ ↔ T *ᵥ f.distal = 0 := by
  constructor <;> intro h <;> funext i
  all_goals
    have hi := congrFun h i
    simp only [forceCorrection, o1Correction, Pi.add_apply, Pi.sub_apply, Pi.zero_apply] at hi ⊢
    linarith

end

-- Future audit commands only; NOT executed in this round.
#print axioms balances_iff
#print axioms condensed_residual_identity
#print axioms condensed_iff
#print axioms identified_condensed_iff
#print axioms o1_from_force_balances
#print axioms adapted_distal_with_reference
#print axioms corrections_equal_iff
#print axioms correctionOnlySignFlip_eq
#print axioms unchanged_values_iff

end RouteBP4032DefectConvention

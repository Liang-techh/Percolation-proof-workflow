import NEW_SOURCE_JACOBIAN_20260908_BODY4_PORTS

set_option autoImplicit false

namespace RouteBO1Body4QuotientPort20260914

noncomputable section

open RouteBO1PerBodyExactSource RouteBO1Body4SourceGramTargets
open RouteBBodySemanticCore RouteBSourceContractAdapter
open RouteBO1Body4SourceJacobianPorts20260908

/-!
CONDITIONAL_QUOTIENT_INTERFACE_UNCOMPILED; admission=pending.
Imports an existing uncompiled candidate, not authenticated evidence.
Source equality and domain coverage are explicit inputs. No Julia readout,
export, Float64 equality, geometry inhabitant or compiler receipt is supplied.
The vector kernel field has three stored components but rank two; the paired
review/manifest specifies the eight independent transverse scalar equations.
-/

def sourceDisp (q : Q6) (j : Fin 4) : V3 :=
  fun a => bodyCom (sourceContract q).origins body4 a -
    (sourceContract q).origins (prevOrigin (activeJoint j)) a

def JacobiansOn (D : Q6 → Prop) : Prop :=
  (∀ q, D q → ∀ a j,
    bodyJv (sourceContract q).origins (sourceContract q).axes body4 a j =
      vcol q j a) ∧
  (∀ q, D q → ∀ a j,
    bodyJw (sourceContract q).axes body4 a j = wcol q j a)

/-- Along-axis displacement is intentionally not fixed. -/
structure QuotientWitness (D : Q6 → Prop) : Prop where
  axes : ∀ q, D q → ∀ j : Fin 4,
    (sourceContract q).axes (activeJoint j) = prefixZ q j
  transverse : ∀ q, D q → ∀ j : Fin 4,
    cross3 (prefixZ q j)
      (fun a => sourceDisp q j a - displacement q j a) = 0

theorem cross_sub (u v w : V3) :
    cross3 u (fun a => v a - w a) =
      (fun a => cross3 u v a - cross3 u w a) := by
  funext a
  fin_cases a <;> simp [cross3] <;> ring

theorem cross_eq_iff_kernel (u v w : V3) :
    cross3 u v = cross3 u w ↔
      cross3 u (fun a => v a - w a) = 0 := by
  constructor
  · intro h
    rw [cross_sub, h]
    funext a
    simp
  · intro h
    funext a
    have ha := congrFun h a
    rw [cross_sub] at ha
    change cross3 u v a - cross3 u w a = 0 at ha
    exact sub_eq_zero.mp ha

theorem wcol_active (q : Q6) (j : Fin 4) :
    wcol q (activeJoint j) = prefixZ q j := by
  fin_cases j <;> rfl

theorem jacobians_of_quotient (D : Q6 → Prop) (h : QuotientWitness D) :
    JacobiansOn D := by
  constructor
  · intro q hq a j
    by_cases hj : j.val < 4
    · let k : Fin 4 := ⟨j.val, hj⟩
      have hd := (cross_eq_iff_kernel (prefixZ q k)
        (sourceDisp q k) (displacement q k)).mpr (h.transverse q hq k)
      have hv : bodyJv (sourceContract q).origins (sourceContract q).axes
          body4 a (activeJoint k) = vcol q (activeJoint k) a := by
        rw [bodyJv_active_formula _ _ _ _ _ (active_guard k)]
        change cross3 ((sourceContract q).axes (activeJoint k))
          (sourceDisp q k) a = _
        rw [h.axes q hq k, hd, active_cross_columns]
      have hk : activeJoint k = j := activeJoint_roundtrip j hj
      simpa only [hk] using hv
    · have hi : 3 < j.val := by omega
      rw [(inactive q a j hi).1]
      fin_cases j <;> norm_num [vcol] at hj ⊢
  · intro q hq a j
    by_cases hj : j.val < 4
    · let k : Fin 4 := ⟨j.val, hj⟩
      have hw : bodyJw (sourceContract q).axes body4 a (activeJoint k) =
          wcol q (activeJoint k) a := by
        rw [bodyJw_active_formula _ _ _ _ (active_guard k), h.axes q hq k]
        exact (congrFun (wcol_active q k) a).symm
      have hk : activeJoint k = j := activeJoint_roundtrip j hj
      simpa only [hk] using hw
    · have hi : 3 < j.val := by omega
      rw [(inactive q a j hi).2]
      fin_cases j <;> norm_num [wcol] at hj ⊢

/-- Necessity concerns the imported ideal Jacobians, not source provenance. -/
theorem quotient_of_jacobians (D : Q6 → Prop) (h : JacobiansOn D) :
    QuotientWitness D := by
  have ha : ∀ q, D q → ∀ j : Fin 4,
      (sourceContract q).axes (activeJoint j) = prefixZ q j := by
    intro q hq j
    funext a
    have hw := h.2 q hq a (activeJoint j)
    rw [bodyJw_active_formula _ _ _ _ (active_guard j)] at hw
    exact hw.trans (congrFun (wcol_active q j) a)
  refine ⟨ha, ?_⟩
  intro q hq j
  apply (cross_eq_iff_kernel (prefixZ q j)
    (sourceDisp q j) (displacement q j)).mp
  funext a
  have hv := h.1 q hq a (activeJoint j)
  rw [bodyJv_active_formula _ _ _ _ _ (active_guard j)] at hv
  change cross3 ((sourceContract q).axes (activeJoint j))
    (sourceDisp q j) a = vcol q (activeJoint j) a at hv
  rw [ha q hq j] at hv
  exact hv.trans (congrFun (active_cross_columns q j) a).symm

theorem quotient_iff_jacobians (D : Q6 → Prop) :
    QuotientWitness D ↔ JacobiansOn D :=
  ⟨jacobians_of_quotient D, quotient_of_jacobians D⟩

/-- Local source witnesses do not manufacture their own cover. -/
theorem quotient_of_cover {ι : Type*} (D : Q6 → Prop) (cell : ι → Q6 → Prop)
    (cover : ∀ q, D q → ∃ i, cell i q)
    (localWitness : ∀ i, QuotientWitness (fun q => D q ∧ cell i q)) :
    QuotientWitness D := by
  constructor
  · intro q hq j
    obtain ⟨i, hi⟩ := cover q hq
    exact (localWitness i).axes q ⟨hq, hi⟩ j
  · intro q hq j
    obtain ⟨i, hi⟩ := cover q hq
    exact (localWitness i).transverse q ⟨hq, hi⟩ j

/-- Only an all-real witness reaches the original global target types. -/
theorem global_targets_of_quotient (h : QuotientWitness (fun _ => True)) :
    Body4JvTarget ∧ Body4JwTarget := by
  have hJ := jacobians_of_quotient (fun _ => True) h
  exact ⟨fun q a j => hJ.1 q trivial a j, fun q a j => hJ.2 q trivial a j⟩

-- No sourceBodyMass/Gram/Fourier/runtime theorem is claimed.
-- No #print command or compiler was run for this candidate.

end
end RouteBO1Body4QuotientPort20260914

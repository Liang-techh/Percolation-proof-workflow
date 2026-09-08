/-
Copyright (c) 2025 Salvatore Mercuri.
Authors: Salvatore Mercuri, Kevin Buzzard, Pietro Monticone.
Apache-2.0; preserve LICENSE, NOTICE and ATTRIBUTION.md from the local intake.

Adapted from Imperial College London FLT staging:
  FLT/Mathlib/Topology/Algebra/Module/Quotient.lean
via anthropics/fermats-last-theorem, commit
  aa2d8b34692b16c70f699536de0d8e75b9a3e9ef,
  Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean.
Current-pin API adaptation follows the local FLTTransportPairingSmoke.lean.
Changes: fresh namespace, targeted imports, explicit inverse continuity proof,
and omission of the separate representative lemma with undeclared parameters.

Target: Lean v4.33.1 / Mathlib 0df444a360eaa60ab8c11dca51a86af692955474.
OPEN_UNCOMPILED: this file has not been compiled, elaborated or axiom-audited.
-/
import Mathlib.LinearAlgebra.Quotient.Pi
import Mathlib.Topology.Algebra.Module.Equiv

set_option autoImplicit false

namespace FLTQuotientCLMAPIRepair

def quotientContinuousLinearEquiv {R : Type*} [Ring R] (G H : Type*)
    [AddCommGroup G] [Module R G] [AddCommGroup H] [Module R H]
    [TopologicalSpace G] [TopologicalSpace H]
    (G' : Submodule R G) (H' : Submodule R H) (e : G ≃L[R] H)
    (h : Submodule.map e.toLinearMap G' = H') :
    (G ⧸ G') ≃L[R] (H ⧸ H') where
  toLinearEquiv := Submodule.Quotient.equiv G' H' e.toLinearEquiv (by simp [h])
  continuous_toFun := by
    apply continuous_quot_lift
    simp only [LinearMap.toAddMonoidHom_coe, LinearMap.coe_comp]
    exact Continuous.comp continuous_quot_mk e.continuous
  continuous_invFun := by
    apply continuous_quot_lift
    simp only [LinearMap.toAddMonoidHom_coe, LinearMap.coe_comp]
    exact Continuous.comp continuous_quot_mk e.continuous_invFun

def quotientPiContinuousLinearEquiv {R ι : Type*} [CommRing R] {G : ι → Type*}
    [(i : ι) → AddCommGroup (G i)] [(i : ι) → Module R (G i)]
    [(i : ι) → TopologicalSpace (G i)]
    [(i : ι) → IsTopologicalAddGroup (G i)] [Fintype ι] [DecidableEq ι]
    (p : (i : ι) → Submodule R (G i)) :
    (((i : ι) → G i) ⧸ Submodule.pi Set.univ p) ≃L[R]
      ((i : ι) → G i ⧸ p i) where
  toLinearEquiv := Submodule.quotientPi p
  continuous_toFun := by
    apply Continuous.quotient_lift
    exact continuous_pi (fun i => Continuous.comp continuous_quot_mk (continuous_apply _))
  continuous_invFun := by
    change Continuous (Submodule.quotientPi_aux.invFun p)
    simp only [Submodule.quotientPi_aux.invFun, Submodule.piQuotientLift,
      LinearMap.lsum_apply, LinearMap.coe_sum, LinearMap.coe_comp, LinearMap.coe_proj]
    have hsum : Continuous (fun a : (i : ι) → G i ⧸ p i =>
        ∑ i, ((p i).mapQ (Submodule.pi Set.univ p) (LinearMap.single R G i)
          (Submodule.le_comap_single_pi p)) (a i)) := by
      refine continuous_finsetSum (ι := ι)
        (M := ((i : ι) → G i) ⧸ Submodule.pi Set.univ p)
        (X := (i : ι) → G i ⧸ p i) Finset.univ (fun i _ => ?_)
      apply Continuous.comp ?_ (continuous_apply _)
      apply Continuous.quotient_lift <|
        Continuous.comp continuous_quot_mk (continuous_single _)
    convert hsum using 1
    funext a
    simp [Function.comp_apply, Finset.sum_apply]

end FLTQuotientCLMAPIRepair

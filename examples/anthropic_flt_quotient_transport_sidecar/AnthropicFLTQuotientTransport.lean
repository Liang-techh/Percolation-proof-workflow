import Mathlib

set_option autoImplicit false

/-!
Minimal non-number-theoretic transport sidecar adapted from the Anthropic FLT
staging file.  The declarations are intentionally kept isolated: successful
compilation is an API candidate, not a Route-B theorem or registry entry.

Provenance:
  repository: https://github.com/anthropics/fermats-last-theorem
  commit: aa2d8b34692b16c70f699536de0d8e75b9a3e9ef
  source: Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean:5-37
  upstream toolchain: Lean 4.33.1
  upstream Mathlib revision: db584cd6d46c92f209a44c0f1c829460d327499d
-/

namespace AnthropicFLTQuotientTransport

def quotientContinuousLinearEquiv {R G H : Type*} [Ring R]
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

def quotientPiContinuousLinearEquiv {R ι : Type*} [CommRing R]
    {G : ι → Type*}
    [(i : ι) → AddCommGroup (G i)] [(i : ι) → Module R (G i)]
    [(i : ι) → TopologicalSpace (G i)]
    [(i : ι) → IsTopologicalAddGroup (G i)]
    [Fintype ι] [DecidableEq ι]
    (p : (i : ι) → Submodule R (G i)) :
    (((i : ι) → G i) ⧸ Submodule.pi Set.univ p)
      ≃L[R] ((i : ι) → G i ⧸ p i) where
  toLinearEquiv := Submodule.quotientPi p
  continuous_toFun := by
    apply Continuous.quotient_lift
    exact continuous_pi (fun i =>
      Continuous.comp continuous_quot_mk (continuous_apply _))
  continuous_invFun := by
    rw [show (Submodule.quotientPi p).invFun =
      fun a => (Submodule.quotientPi p).invFun a from rfl]
    simp only [Submodule.quotientPi, Submodule.quotientPi_aux.toFun,
      Submodule.quotientPi_aux.invFun, Submodule.piQuotientLift,
      LinearMap.lsum_apply, LinearMap.coe_sum, LinearMap.coe_comp,
      LinearMap.coe_proj, LinearEquiv.invFun_eq_symm,
      LinearEquiv.coe_symm_mk, Finset.sum_apply, Function.comp_apply,
      Function.eval]
    refine continuous_finsetSum _ (fun i _ => ?_)
    apply Continuous.comp ?_ (continuous_apply _)
    apply Continuous.quotient_lift
      (Continuous.comp continuous_quot_mk (continuous_single _))

theorem quotient_transport_mk {R G H : Type*} [Ring R]
    [AddCommGroup G] [Module R G] [AddCommGroup H] [Module R H]
    [TopologicalSpace G] [TopologicalSpace H]
    (G' : Submodule R G) (H' : Submodule R H) (e : G ≃L[R] H)
    (h : Submodule.map e.toLinearMap G' = H') (g : G) :
    quotientContinuousLinearEquiv G' H' e h (Submodule.Quotient.mk g) =
      Submodule.Quotient.mk (e g) := by
  rfl

#print axioms quotientContinuousLinearEquiv
#print axioms quotientPiContinuousLinearEquiv
#print axioms quotient_transport_mk

end AnthropicFLTQuotientTransport

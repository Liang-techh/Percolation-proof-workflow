import Mathlib

/-!
# Anthropic FLT additive-to-integer-continuous-linear adapter

This sidecar records the audited generic transport construction
`ContinuousAddEquiv.toIntContinuousLinearEquiv`.  The construction is
additive/topological infrastructure only: its scalar ring is fixed to `ℤ`.
It does not manufacture an `R`-linear map for a PDE scalar field and it does
not establish any FLT arithmetic or registry admission claim.

Provenance:
  repository: upstream/anthropics-fermats-last-theorem
  commit: aa2d8b34692b16c70f699536de0d8e75b9a3e9ef
  source: Definitions/Def_Mathlib_Topology_Algebra_ContinuousMonoidHom.lean
  source blob: 7829c8e30b406c8bb1dcbddf8e8d49745ec5c8ea
-/

set_option autoImplicit false

namespace AnthropicFLTAdditiveLinearAdapter

/--
Exact typed wrapper for the upstream construction.  The output is an
integer-linear continuous equivalence, not a polymorphic scalar transport.
-/
def toIntContinuousLinearEquiv {M M₂ : Type*} [AddCommGroup M]
    [TopologicalSpace M] [AddCommGroup M₂] [TopologicalSpace M₂]
    (e : M ≃ₜ+ M₂) : M ≃L[ℤ] M₂ where
  __ := e.toIntLinearEquiv
  continuous_toFun := e.continuous
  continuous_invFun := e.continuous_invFun

theorem toIntContinuousLinearEquiv_apply {M M₂ : Type*} [AddCommGroup M]
    [TopologicalSpace M] [AddCommGroup M₂] [TopologicalSpace M₂]
    (e : M ≃ₜ+ M₂) (x : M) :
    toIntContinuousLinearEquiv e x = e x := by
  rfl

theorem toIntContinuousLinearEquiv_symm_apply {M M₂ : Type*} [AddCommGroup M]
    [TopologicalSpace M] [AddCommGroup M₂] [TopologicalSpace M₂]
    (e : M ≃ₜ+ M₂) (y : M₂) :
    (toIntContinuousLinearEquiv e).symm y = e.symm y := by
  rfl

end AnthropicFLTAdditiveLinearAdapter

#print axioms AnthropicFLTAdditiveLinearAdapter.toIntContinuousLinearEquiv_apply
#print axioms AnthropicFLTAdditiveLinearAdapter.toIntContinuousLinearEquiv_symm_apply

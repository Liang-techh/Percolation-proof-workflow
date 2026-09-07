import Lake
open Lake DSL

require mathlib from "../anthropic_flt_reusable_lean/.lake/packages/mathlib"
package anthropic_flt_spectral_predicate_sidecar where
  leanOptions := #[⟨`autoImplicit, false⟩]

@[default_target]
lean_lib AnthropicFLTSpectralPredicateSidecar where
  roots := #[`AnthropicFLTSpectralPredicateSidecar]

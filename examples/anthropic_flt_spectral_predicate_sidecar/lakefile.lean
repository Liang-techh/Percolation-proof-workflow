import Lake
open Lake DSL

package anthropic_flt_spectral_predicate_sidecar where
  leanOptions := #[⟨`autoImplicit, false⟩]

@[default_target]
lean_lib AnthropicFLTSpectralPredicateSidecar where
  roots := #[`AnthropicFLTSpectralPredicateSidecar]

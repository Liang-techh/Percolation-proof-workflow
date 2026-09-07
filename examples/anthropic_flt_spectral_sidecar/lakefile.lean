import Lake
open Lake DSL

package anthropic_flt_spectral_sidecar where
  leanOptions := #[⟨`autoImplicit, false⟩]

@[default_target]
lean_lib AnthropicFLTSpectralSidecar where
  roots := #[`AnthropicFLTSpectralSidecar]

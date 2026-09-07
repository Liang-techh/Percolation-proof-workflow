import Lake
open Lake DSL

package anthropic_flt_quotient_transport_sidecar where
  leanOptions := #[⟨`autoImplicit, false⟩]

@[default_target]
lean_lib AnthropicFLTQuotientTransport where
  roots := #[`AnthropicFLTQuotientTransport]

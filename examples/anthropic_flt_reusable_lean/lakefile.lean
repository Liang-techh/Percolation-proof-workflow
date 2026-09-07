import Lake
open Lake DSL

package anthropic_flt_reusable_lean where
  leanOptions := #[⟨`autoImplicit, false⟩]

@[default_target]
lean_lib AnthropicFLTReusable where
  roots := #[`AnthropicFLTReusable]

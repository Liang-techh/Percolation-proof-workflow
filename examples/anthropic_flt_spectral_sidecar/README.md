# Anthropic FLT Spectral Sidecar

This directory is a focused spectral sidecar for `T-FLT-SPECTRAL-SIDECAR`.

Scope:

- First-choice reuse target from the review: `Submodule.exists_injective_linearMap_baseChange_torsionBySet_range_eq_eigenspace`
- Fallback implemented here: a minimal abstract eigenspace/range bridge
- Explicitly not included: a direct upstream theorem proof, any number-theoretic development, or any state/registry/task-queue mutation

Provenance:

- review source: `agent_review_inbox/review-T-FLT-spectral-linear.md`
- upstream commit: `aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`

Files in this sidecar:

- `AnthropicFLTSpectralSidecar.lean`
- `lakefile.lean`
- `lean-toolchain`
- `verify.sh`

The Lean file is intentionally conservative. It compiles a small abstract bridge
and keeps `#print axioms` in place so any assumptions remain visible.

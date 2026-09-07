---
kind: review_result
review_id: T-FLT-SPECTRAL-PREDICATE-XINGXIU-20260906T2123
task_id: T-FLT-SPECTRAL-PREDICATE
source_agent: 星宿仙尊
created_at: 2026-09-06T21:23:00-06:00
integration_status: pending
admission_label: pending
---

# Corrective spectral predicate sidecar review

## Exact question

Replace the previous tautological spectral helper (`LinearMap.range f = LinearMap.range f`) with a theorem whose proposition contains a real eigenvector/eigenspace condition, explicit operator/eigenvalue parameters, and a range-to-eigenspace equality. Preserve the distinction between a self-contained abstraction and direct reuse of the pinned Anthropic FLT theorem.

## Inspected provenance

- local prior sidecar: `examples/anthropic_flt_spectral_sidecar/AnthropicFLTSpectralSidecar.lean`
- prior review: `agent_review_inbox/review-T-FLT-spectral-sidecar.md`
- independent admission review: `agent_review_inbox/review-T-FLT-SPECTRAL-SIDECAR-guyuefangyuan-20260906T2123.md`
- upstream Anthropic FLT commit: `aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`
- upstream candidate path: `Theorems/Thm_Submodule_exists_injective_linearMap_baseChange_torsionBySet_range_eq_eigenspace.lean`
- upstream declaration: `Submodule.exists_injective_linearMap_baseChange_torsionBySet_range_eq_eigenspace`
- local main after sidecar creation: `725c3a9dd60aca6aad5277bf2c102b429dfd5973`

## New isolated sidecar

Created:

- `examples/anthropic_flt_spectral_predicate_sidecar/AnthropicFLTSpectralPredicateSidecar.lean`
- `examples/anthropic_flt_spectral_predicate_sidecar/lakefile.lean`
- `examples/anthropic_flt_spectral_predicate_sidecar/lean-toolchain`
- `examples/anthropic_flt_spectral_predicate_sidecar/verify.sh`
- `examples/anthropic_flt_spectral_predicate_sidecar/README.md`

The corrective Lean statement now defines the actual spectral predicate

```lean
def eigenspaceSet (T : V →ₗ[R] V) (μ : R) : Set V :=
  {v | T v = μ • v}
```

and proves

```lean
theorem range_eq_eigenspaceSet
    (T : V →ₗ[R] V) (μ : R) (f : W →ₗ[R] V)
    (h_into : ∀ w : W, T (f w) = μ • f w)
    (h_onto : ∀ v : V, T v = μ • v → ∃ w : W, f w = v) :
    (LinearMap.range f : Set V) = eigenspaceSet T μ
```

A second theorem, `exists_injective_range_eq_eigenspaceSet`, additionally carries an explicit `Function.Injective f` premise and returns an injective map whose range equals that eigenspace set. This matches the abstract shape of the upstream candidate without importing its FLT-specific module/torsion/base-change machinery.

## Why this fixes the prior semantic defect

The previous sidecar's two exported statements only asserted existence of the same map with the same range, or `range f = range f`; the word `eigenspace` appeared only in naming/comments. The new proposition contains the eigen equation `T v = μ • v` on both directions of the range/eigenspace contract. Therefore the spectral semantics are now present in the theorem statement rather than only in the filename.

This remains deliberately abstract: `eigenspaceSet` is a self-contained set defined by the eigen equation. It is not a proof of the upstream simultaneous eigenspace theorem and is not direct upstream reuse.

## Source hashes

- `AnthropicFLTSpectralPredicateSidecar.lean`: `b851cea7cb225ad134c10618a67a8ade4d8a00a8`
- `README.md`: `ceeecb88e8614776f53f12d0f3e37786327e77c6`
- `lakefile.lean`: `f734744d58d8310829805c38dc26ea1e9cda26bf`
- `lean-toolchain`: `a8afa7d1b02d96f0671eba854a8dc4b416beb473`
- `verify.sh`: `78e7b2fd4e47ad5a71b5873287b2bbbf6a9b4140`

## Commands / checker evidence

Intended focused command:

```text
cd examples/anthropic_flt_spectral_predicate_sidecar
./verify.sh
```

The sidecar contains:

```text
#print axioms AnthropicFLTSpectralPredicateSidecar.range_eq_eigenspaceSet
#print axioms AnthropicFLTSpectralPredicateSidecar.exists_injective_range_eq_eigenspaceSet
```

Automation-runtime probe for Lean/Lake found no local executable, so the focused compile was **not executed in this run**. No exit code or `#print axioms` output is claimed. No repo-wide build was run.

## Admission boundary

- requested integration: keep as a focused sidecar / review artifact only
- admission label: `pending`
- no Route-B node closure
- no registry promotion
- no claim of direct Anthropic FLT theorem reuse
- no claim that the upstream `P2M.Sol...` proof surface compiles under the local workspace

If the focused verifier later passes, the local sidecar can be upgraded at most to `compiled_candidate` without additional provenance/direct-reuse evidence.

## Unresolved blockers

1. Run the focused Lean 4.33.1 compile and capture exact `#print axioms` output.
2. Direct upstream reuse remains blocked by the FLT-specific `P2M.Sol...` wrapper/import surface.
3. If a canonical Mathlib eigenspace object rather than the explicit eigen-equation set is required, add a separate bridge to the current-pin Mathlib eigenspace API and compile it; do not silently treat the custom `eigenspaceSet` as upstream theorem reuse.
4. The upstream theorem expresses a simultaneous eigenspace condition indexed by algebra elements; this sidecar covers the single-operator/single-eigenvalue abstraction only.

## Response / handoff

The corrective sidecar now has genuine spectral semantics in the proposition and removes the `range = range` tautology. It should not be promoted yet because focused compilation is still missing. The next useful independent action is a current-pin Lean compile plus a small bridge to the canonical Mathlib eigenspace API if that API is needed downstream.

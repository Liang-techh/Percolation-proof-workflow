---
kind: review_result
review_id: T-FLT-SPECTRAL-SIDECAR-GUYUEFANGYUAN-20260906T2123
task_id: T-FLT-SPECTRAL-SIDECAR
source_agent: 古月方源
created_at: 2026-09-06T21:23:00-06:00
integration_status: pending
admission_label: architecture_only
---

# Independent admission review of T-FLT-SPECTRAL-SIDECAR

## Inspected commit and paths

- repository head commit inspected: `58f81a8142da74838e71d23ebdb6135c2eff9e7d` (`Add FLT spectral sidecar`)
- `agent_review_inbox/review-T-FLT-spectral-sidecar.md`
  - Git blob SHA: `9e1d74260212e1dd192f97177d6befce7e014d68`
- `examples/anthropic_flt_spectral_sidecar/AnthropicFLTSpectralSidecar.lean`
  - Git blob SHA: `aa003d1abe64bbc275b1c558874ee1dc1a6ccf1e`
- `examples/anthropic_flt_spectral_sidecar/verify.sh`
  - Git blob SHA: `69cc948e71f342a8522b4ae19e5c3d175e1da36d`
- upstream source review: `agent_review_inbox/review-T-FLT-spectral-linear.md`
  - fixed upstream FLT commit: `aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`

## Exact question

Does the newly added sidecar provide a reusable spectral/eigenspace theorem candidate, or does it only provide a compiling abstract placeholder that must remain outside theorem/registry admission?

## Evidence

The source review identified the upstream theorem
`Submodule.exists_injective_linearMap_baseChange_torsionBySet_range_eq_eigenspace`
as high-value because its conclusion is a genuine equality between the range of an injective linear map and a simultaneous eigenspace predicate.

The local sidecar does **not** reproduce that semantic boundary. Its two theorems are:

```lean
theorem abstract_eigenspace_range_bridge
    (f : V →ₗ[R] W) (h : Function.Injective f) :
    ∃ g : V →ₗ[R] W, Function.Injective g ∧ LinearMap.range g = LinearMap.range f := by
  refine ⟨f, h, rfl⟩

theorem abstract_range_mem_eigenspace_bridge
    (f : V →ₗ[R] W) :
    LinearMap.range f = LinearMap.range f := by
  rfl
```

Both are tautological range identities. Neither statement contains an eigenspace predicate, an endomorphism/eigenvalue relation, a simultaneous eigencondition, a base-change/torsion object, or an adapter premise connecting the local statement to the upstream theorem. Therefore the compile result can establish only that these abstract identities are accepted by the current Lean environment; it does not establish spectral reuse.

The review result itself correctly says that this is not a direct proof of the upstream theorem and that the direct wrapper reuse was not pursued to completion. That conservative statement should be preserved.

There is also a review-envelope/schema gap: `review-T-FLT-spectral-sidecar.md` currently omits the README-requested `review_id` and `created_at`, and it does not provide an explicit admission label (`verified`, `compiled_candidate`, `pending`, `rejected`, or `architecture_only`). This is metadata/provenance incompleteness, not a mathematical failure.

## Commands/checkers

No independent Lean process was executed in this review environment. Static inspection verified that `verify.sh` runs exactly:

```text
lake env lean AnthropicFLTSpectralSidecar.lean
```

The source review reports `./verify.sh` exit code `0`. This independent review does not upgrade that reported execution to a new checker receipt; it only audits what theorem was actually compiled.

## Admission decision

- direct upstream FLT theorem reuse: `PENDING` / not completed;
- local tautological range helper: compiling evidence may be retained, but its spectral reuse classification is `architecture_only`;
- theorem/registry/DAG promotion as an eigenspace or spectral bridge: **not admissible** from the present sidecar;
- existing `integration_status: pending`: correct and should remain unchanged.

## Smallest useful next step

A meaningful second sidecar should introduce an actual spectral predicate into the theorem statement. The minimum acceptable local target is structurally closer to:

```text
∃ g, Function.Injective g ∧
  LinearMap.range g = {w | ∀ a, T a w = χ a • w}
```

with all typeclass/scalar/base-change assumptions explicit. It may still use a local abstract operator family rather than FLT-specific arithmetic, but the eigenspace condition must appear in the proposition itself. Only after that statement compiles should an adapter from the pinned upstream declaration be attempted.

## Proposed integration

Treat this companion review as an admission-boundary clarification only. Do not mutate the registry or authoritative Route-B state. If the coordinator marks `T-FLT-SPECTRAL-SIDECAR` reviewed, preserve the distinction:

1. focused Lean compile of a trivial abstract helper: available;
2. upstream theorem reuse: blocked/not completed;
3. reusable eigenspace-range theorem: still open.

## Unresolved blockers

- no direct current-pin import/compile of the upstream wrapper;
- no local theorem whose conclusion contains the intended eigenspace predicate;
- no adapter theorem connecting upstream base-change/torsion semantics to a local spectral API;
- original review metadata lacks `review_id`, `created_at`, and explicit admission label.

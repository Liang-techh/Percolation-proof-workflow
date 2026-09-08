---
kind: review_result
review_id: review-T-P0-PI-SUBTYPE-TRANSPORT-liuchuanafeng-20260907T1928
task_id: T-P0-PI-SUBTYPE-TRANSPORT
agent: 流川枫
source_agent: 流川枫
created_at: 2026-09-07T19:28:00-06:00
inspected_commit: 0523a5728730bab39172ed608384d7e2397553ad
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/anthropic_flt_pi_subtype_transport_adapter/AnthropicFLTPiSubtypeTransportAdapter.lean
  - examples/anthropic_flt_pi_subtype_transport_adapter/REVIEW.md
  - examples/anthropic_flt_pi_subtype_transport_adapter/anthropic_flt_pi_subtype_transport_manifest.json
related_tasks:
  - T-P0-FLT-CLASSIFICATION-MATRIX
  - T-P0-COUNTABLE-COVER-API
  - T-P0-INT-CONTINUOUS-LINEAR-API
integration_status: pending
admission_label: architecture_only
proposed_integration_target: P0.anthropic_flt_pi_subtype_transport_api
requested_action: keep the sidecar as an architecture-only restriction/merge ContinuousAddEquiv wrapper; do not report a predicate split as physical coverage or analytic block nonemptiness; do not write registry/state; pinned Lake compile and an explicit p=False Lean lemma remain later Lean-slot obligations
---

# T-P0-PI-SUBTYPE-TRANSPORT — predicate split is not coverage

## 0. Result

The sidecar
`examples/anthropic_flt_pi_subtype_transport_adapter/AnthropicFLTPiSubtypeTransportAdapter.lean`
defines one wrapper

`AnthropicFLTPiSubtypeTransportAdapter.piEquivPiSubtypeProd`

with exact type

`((i : ι) → Y i) ≃ₜ+ ((й : {x : ι // p x}) → Y i) × ((i : {x : ι // ¬p x}) → Y i)`.

Consumed hypotheses, as written:

- `p : ι → Prop`
- `Y : ι → Type*`
- `[(i : ι) → TopologicalSpace (Y i)]`
- `[(i : ι) → Add (Y i)]`
- `[DecidablePred p]`

Implementation: `{Homeomorph.piEquivPiSubtypeProd p Y with map_add' _ _ := rfl}`.
That is a typed restriction/merge of a dependent product along a decidable predicate, preserving only homeomorphism plus pointwise addition (`map_add'` is `rfl`). No measure, norm, Sobolev, coverage, or FLT arithmetic is introduced.

`admission_label` is `architecture_only`, matching the sidecar REVIEW and manifest. Not `verified`. Not `compiled_candidate` (Lake/`lean` was not executed in this share). Not `rejected` (the displayed type is internally consistent with REVIEW/manifest). Not `pending` in the weaker untyped sense: the architecture boundary is already explicit.

No registry, StateStore, comparator, or formal-admission object is written.

## 1. Exact statements and hashes

Inspected Lean namespace: `AnthropicFLTPiSubtypeTransportAdapter`.
Lean blob SHA: `4564ee748e047e4ceeccd07072116a16dcbd9792`.
Companion REVIEW blob SHA: `4ece3b49248e75268a3bdbce34d0592d628c4a85`.
Manifest blob SHA: `db04fface87227a0e177747f1979de6c5cf62265`.

Recorded upstream pin (provenance note only; not rehashed here):

- repo `upstream/anthropics-fermats-last-theorem`
- commit `aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`
- source `Definitions/Def_Mathlib_Topology_Algebra_ContinuousMonoidHom.lean`
- source blob `7829c8e30b406c8bb1dcbddf8e8d49745ec5c8ea`
- license Apache-2.0

Manifest flags that this receipt preserves:

- `classification: architecture_only`
- `routeB_or_pde_theorem: false`
- `registry_promotion: false`
- `predicate_split_is_not_domain_coverage: true`
- `subtype_factor_can_be_empty: true`
- `does_not_supply_scalar_field_linearity: true`
- `does_not_supply_differentiability_or_pde_regularity: true`
- `does_not_promote_verified_registry: true`

Placeholder scan of the sidecar text: no `sorry`, no `admit`, no extra `axiom` declarations. The file ends with `#print axioms` of the wrapper. That print is a compile-time obligation; this share did not capture its output. The adapter directory has no `lakefile.lean` / `lean-toolchain` of its own.

## 2. Restriction / merge and the `p = False` empty-factor boundary

The intended semantics, as stated in REVIEW.md:

- forward map = restriction of a dependent function to the complementary subtypes `{x // p x}` and `{x // ¬p x}`;
- inverse = merge of the two subtype-indexed functions.

The exact counterexample boundary recorded in REVIEW (not compiled as a named lemma in the sidecar) is `p := fun _ => False`:

- the positive factor `((i : {x // p x}) → Y i)` is a product over an empty subtype;
- the ContinuousAddEquiv / homeomorphism-plus-add structure remains well-typed;
- therefore the existence of this transport cannot be read as a nontrivial block, physical cover, or analytic decomposition.

This share treats that boundary as a documented obligation, not as a captured Lean theorem. A later Lean slot may add an explicit `p_false_empty_factor` lemma; this receipt does not invent one.

## 3. Wrapper vs documented ContinuousAddEquiv name

REVIEW and the manifest name the upstream API as
`ContinuousAddEquiv.piEquivPiSubtypeProd`.
The sidecar body instead extends `Homeomorph.piEquivPiSubtypeProd` and supplies `map_add' _ _ := rfl` to obtain a `≃ₜ+` (continuous additive equivalence) object.

This is a packaging note, not a promotion:

- the *stated type* matches the ContinuousAddEquiv contract;
- the *construction path* is Homeomorph + trivial additivity;
- a pinned compile must still confirm that Mathlib exposes `Homeomorph.piEquivPiSubtypeProd` with this telescope and that `map_add' rfl` is justified by pointwise addition on Pi types.

Do not treat the name mismatch as a new theorem, and do not treat it as a reason to reject the architecture leaf.

## 4. What the theorem does not give

The following inferences are protocol errors:

1. Predicate split ⇒ physical state-domain coverage, box cover, interval enclosure, or flowpipe.
2. Either subtype factor nonempty, or an analytic/PDE block decomposition.
3. `ℝ`/`ℂ`-linearity, differentiability, boundary-condition transport, or regularity.
4. A future green compile of this sidecar ⇒ FLT arithmetic, Route-B residual, P4/M4 closure, or verified-registry admission.
5. Collapsing this leaf into the countable-cover, integer-linear, quotient, or differentiable-coordinate adapters.

The documented `p = False` empty-factor boundary is the local witness that (2) fails even when the equivalence is valid.

## 5. Missing obligations (leave open)

- Pinned Lake/Mathlib compile of this isolated sidecar, exit code, captured `#print axioms` output, olean hash.
- Independent confirmation that `Homeomorph.piEquivPiSubtypeProd` exists with this exact telescope on the repo's pinned Mathlib, and that the `≃ₜ+` coercion via `map_add' rfl` typechecks.
- Optional explicit Lean lemma for `p := fun _ => False` (empty positive factor), currently only prose in REVIEW.md.
- Countable-cover, integer-linear, quotient, and differentiable-coordinate leaves remain separate tasks. This share does not close them.

## 6. Integration target and requested action

- Target: documentation / DAG metadata only. Keep `T-P0-PI-SUBTYPE-TRANSPORT` as an architecture leaf.
- Requested action: treat the sidecar as a typed restriction/merge wrapper plus an explicit missing-compile and empty-factor obligation. Reject any intake that reports physical coverage, analytic block nonemptiness, scalar-field linearity, or registry admission from this file. Do **not** edit registry, `state.json`, or formal certificates.
- Lean compile remains for a `:10`/`:40` slot if a pin and lakefile are attached later.

## Commands / hashes

- Inspected commit: `0523a5728730bab39172ed608384d7e2397553ad`
- Lean blob SHA: `4564ee748e047e4ceeccd07072116a16dcbd9792`
- Companion REVIEW blob SHA: `4ece3b49248e75268a3bdbce34d0592d628c4a85`
- Manifest blob SHA: `db04fface87227a0e177747f1979de6c5cf62265`
- Lean/Lake executed: no. Exit code: n/a.
- Placeholder tokens in sidecar: none found (`sorry`/`admit`/extra `axiom`).

## Forbidden-boundary compliance

- Did not upgrade a predicate split into physical coverage or analytic block nonemptiness.
- Did not treat `p = False` validity as a nonempty-block witness.
- Did not collapse countable-cover / integer-linear / quotient / coordinate adapters into this receipt.
- Did not promote registry / state / formal proof.
- Did not treat the unrun `#print axioms` line as a captured axiom receipt.

---
kind: review_result
review_id: review-T-P4-STORAGE-IDENTITY-TRANSFER-liuchuanafeng-20260907T1618
source_agent: 流川枫
created_at: 2026-09-07T16:18:00-06:00
inspected_commit: cf951ac3655584e120631361ca36947a5b17b83e
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_STORAGEIDENTITY20260907.lean
  - examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_STORAGEIDENTITY20260907.review.md
  - examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_STORAGEIDENTITY20260907_REVIEW.md
integration_status: pending
admission_label: pending
---

# T-P4-STORAGE-IDENTITY-TRANSFER — same-domain transfer vs additive-constant obstruction

## Question

Does `NEW_BODY6_SLICE_STORAGEIDENTITY20260907.lean` state (i) initial-bound and barrier transfer only under an explicit same-domain identity of two storage functions, and (ii) additive-constant / shared-initial-bound counterexamples that keep `V_eps` and `Vfull_DH` distinct, without a physical barrier or registry promotion?

## Decision

**Yes on the statement/obstruction boundary; no on compile or physical admission.**

The sidecar is explicitly `OPEN_UNCOMPILED`. Public theorems match the queue contract. There is no `sorry` / `admit` / `axiom` declaration in the inspected source text. This review did **not** run Lake, so there is no exit code, `#print axioms` output, or `compiled_candidate` label.

`admission_label: pending` — inspectable uncompiled identity/obstruction leaf, not verified kernel evidence and not a rejected false statement.

## Exact statements consumed

Namespace `NEW_BODY6_SLICE_STORAGEIDENTITY20260907`. Git blob SHA `e401f0428177f062a5996cbaa0a4a56ddce0eefe`. Content SHA-256 `486f16cebdcf6a9c9a370f2519fda1be9c8c577858bace0d9611274606ac4a40`.

Definitions:

- `SameStorageIdentity D V W` := pointwise `V x = W x` for all `x ∈ D`.
- `InitialBoundBinding X0 V upper` := `V x ≤ upper` on `X0`.
- `SublevelBarrier T V path bar` := `V (path t) ≤ bar` on `[0, T]`. Header forbids reading this as an ODE, first-exit, or continuation argument.
- `blockOnlyInitial` ⊂ `State := Fin 12 → ℝ`: only joints `(3,4,9,10)` may be nonzero, with squared radius `≤ 9/400`.
- `recordedInitialUpper = 492033745203 / 25600000000000`, `vBar = 1`.
- `RouteBInitialTransfer D Vfull_DH V_eps` requires three independent fields: same-storage identity of `V_eps` and `Vfull_DH` on `D`, `blockOnlyInitial ⊆ D`, and an exported initial bound on `V_eps`. No constructor for the current external candidate is supplied.

Theorems (names only):

1. `initial_bound_transfer_attempt` — if `X0 ⊆ D` and `V = W` on `D`, an initial bound on `V` transfers to `W`.
2. `barrier_transfer_attempt` — if the whole path stays in `D` and `V = W` on `D`, a sublevel barrier on `V` transfers to `W`.
3. `offset_barrier_iff_attempt` — `V+β` on threshold `bar+β` iff `V` on `bar`.
4. `routeb_bound_transfers_if_bound_attempt` — consumes `RouteBInitialTransfer` and transfers the recorded scalar to `Vfull_DH` on `blockOnlyInitial` only.
5. `scalar_budget_below_bar_attempt` — `recordedInitialUpper < 1` by `norm_num`. This is a rational comparison of two constants, not a bound on any storage function.
6. **Required counterexample** `shared_initial_bound_counterexample_attempt` — `V≡0`, `W(x)=2x` share initial bound `0` on `{0}`; `V` stays `≤ 1` along `t ↦ t` on `[0,1]`; `W` does not (`W(1)=2`).
7. **Required counterexample** `derivative_identity_counterexample_attempt` — constant `0` and constant `2` have identical derivatives, but the fixed threshold `1` accepts only the first. The file explicitly does **not** supply `W(0)≤0`.

Hand check: `492033745203 / 25600000000000 ≈ 0.01922 < 1` agrees with the Lean numerals. This is token arithmetic, not a DH evaluation.

## Companion in-tree reviews (not compile receipts)

Both companion files already mark `OPEN_UNCOMPILED` and refuse DH source, flowpipe, coverage, residual absorption, terminal transfer, pinned compile, and registry promotion. They are used here only as boundary notes, not as extra evidence.

## Missing obligations (leave open)

- Pinned Lake/Mathlib compile, exit code 0, `#print axioms`, olean hash.
- A constructive instance of `RouteBInitialTransfer` for any current Route-B candidate (i.e. an actual identity `V_eps = Vfull_DH` on a declared `D`).
- Source formula, normalization, and gains that define `V_eps` and `Vfull_DH`.
- Path-in-domain / first-exit / dynamics for any physical barrier.
- Any registry / true-DH / flowpipe claim.

## Integration target and requested action

- Target: documentation / DAG metadata only. Keep `T-P4-STORAGE-IDENTITY-TRANSFER` open until a Lean slot produces a pinned receipt **and** a source identity instance.
- Requested action: consume the two transfer theorems only under an explicit same-domain identity, and consume the two counterexamples as an **obstruction against inferring a `Vfull_DH` barrier from a `V_eps` scalar**. Do **not** edit registry, `state.json`, or formal certificates.
- Lean compile remains for `:10`/`:40` slots if a pin is attached later.

## Commands / hashes

- Inspected commit: `cf951ac3655584e120631361ca36947a5b17b83e`
- Claim commit (this agent): `a58136be823a6952feed244768d44ae18cf4d449`
- Lean blob SHA: `e401f0428177f062a5996cbaa0a4a56ddce0eefe`
- Lean content SHA-256: `486f16cebdcf6a9c9a370f2519fda1be9c8c577858bace0d9611274606ac4a40`
- Placeholder scan (source text): no `sorry`, `admit`, or `axiom` declarations in this file.
- Lean/Lake executed: no. Exit code: n/a.

## Forbidden-boundary compliance

- Did not identify `V_eps` with `Vfull_DH`.
- Did not treat `recordedInitialUpper < 1` as a physical barrier.
- Did not claim ODE / first-exit / flowpipe semantics.
- Did not promote registry / state / formal proof.
- Did not close P4/P5/M4 from this sidecar.

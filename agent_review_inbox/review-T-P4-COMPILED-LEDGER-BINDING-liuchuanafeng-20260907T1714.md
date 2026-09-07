---
kind: review_result
review_id: review-T-P4-COMPILED-LEDGER-BINDING-liuchuanafeng-20260907T1714
source_agent: 流川枫
created_at: 2026-09-07T17:14:00-06:00
inspected_commit: 577ace22b54d7f71b60cf8b071e3c6604ba296ad
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_COMPILEDLEDGERBINDING20260907.lean
  - examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_COMPILEDLEDGERBINDING20260907.review.md
  - examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_COMPILEDLEDGERBINDING20260907_REVIEW.md
integration_status: pending
admission_label: pending
---

# T-P4-COMPILED-LEDGER-BINDING — typed ledger contracts vs imported compiled leaves

## Question

Does `NEW_BODY6_SLICE_COMPILEDLEDGERBINDING20260907.lean` (i) bind a ledger function to `storageV` only through explicit `InitialLedgerBinding` / `PathLedgerBinding` records, and (ii) keep the imported `ActualStorage` / `ActualShift` leaves separate from this sidecar, including an exact shifted-baseline obstruction that already exceeds 45, without source identity, flowpipe, or registry promotion?

## Decision

**Yes on the statement/contract boundary; no on compile or physical admission.**

The sidecar is explicitly `OPEN_UNCOMPILED`. Public theorems match the queue contract. There is no `sorry` / `admit` / `axiom` declaration in the inspected source text. This review did **not** run Lake, so there is no exit code, `#print axioms` output, or `compiled_candidate` label. Historical receipts on imported leaves are not compilation or instantiation of this sidecar.

`admission_label: pending` — inspectable uncompiled contract/obstruction leaf, not verified kernel evidence and not a rejected false statement.

## Exact statements consumed

Namespace `NEW_BODY6_SLICE_COMPILEDLEDGERBINDING20260907`. Git blob SHA `17163fb87f366a68b9f1f15681c770269d9a39e2`.

Constants:

- `ledgerV0 = 492033745203 / 25600000000000`
- `ledgerBar = 1`
- `initialFormula d beta = (9/400)*beta + 3*(d.f 0)/10000 + 3*(d.h 0)`
- `encodedShiftedEnergy M q v = kinetic M v + W q + 4079979/400000`

Records:

- `ActualInitialPremises` copies the existing `storageV_initial_upper` premises (nonnegativity of `f(0)`, `h(0)`, initial ball `normSq q + normSq v ≤ 9/400`, signed-gap lower bound, ramp `slope^2 ≤ 3`, and two beta inequalities). No source identity or actual gap bound is manufactured here.
- `InitialLedgerBinding` requires pointwise `L 0 x = actualAt d 0 x` on `X0`, the full premises on `X0`, and `initialFormula d beta ≤ ledgerV0`.
- `PathLedgerBinding` requires pointwise identity of `L` and `actualAt` on every time-slice domain `D t`, independent `pathInDomain`, a source tube on `actualAt` along the path, and `tube < ledgerBar`. Path inclusion is not inferred from the desired barrier.

Theorems (names only):

1. `existing_initial_theorem_instance_attempt` — instantiates imported `storageV_initial_upper` under `ActualInitialPremises`.
2. `initial_ledger_bound_attempt` — transfers that bound to `L 0` on `X0` only after the identity + premises + budget fields.
3. `path_ledger_barrier_attempt` — yields `L t (path t) < 1` only after identity + path-in-domain + source tube + `tube < 1`.
4. `existing_shifted_comparison_instance_attempt` — consumes imported `actual_p45_bound` under an explicit mass inequality and `rfl` on the encoded `E+B` shift. A ledger must bind to `E+B` to use this particular inequality.
5. `component_cap_does_not_imply_storage_cap_attempt` — `¬ ((5/2)^2 ≤ 56/15)`. External token check: `6.25 ⊄ 56/15 ≈ 3.733` is false.
6. `w0_initial_number_fits_ledger_attempt` — `231/20000 ≤ ledgerV0`. External token check: `0.01155 ≤ 0.019220…` holds. This is two-constant arithmetic, not a bound on any storage function.
7. `shifted_comparison_baseline_exceeds_45_attempt` — `45 < (1600000/9401)*(4079979/400000)`. External token check: right-hand side `≈ 1735.98`. A weak upper bound is not evidence that the true output exceeds 45; the file records that the additive baseline alone already blows the coarse `p45≤45` threshold.

No instance of either ledger-binding record is asserted. Initial/path compatibility, ODE, source semantics, and continuation remain external.

## Companion in-tree reviews (not compile receipts)

Both companion files already mark `OPEN_UNCOMPILED` and refuse source/Float64 identity, coverage, flowpipe, residual absorption, terminal transfer, pinned compile, and registry promotion. They are used here only as boundary notes, not as extra evidence.

## Missing obligations (leave open)

- Pinned Lake/Mathlib compile, exit code 0, `#print axioms`, olean hash of *this* sidecar.
- A constructive instance of `InitialLedgerBinding` or `PathLedgerBinding` for any current Route-B candidate.
- Source formula proving `L = actualAt` on a declared domain, or that `actualAt` equals a physical `Vfull_DH`.
- Independent proof of `budgetToV0`, `sourceTube`, `pathInDomain`, and the mass premise of the shifted comparison.
- Any registry / true-DH / flowpipe claim.

## Integration target and requested action

- Target: documentation / DAG metadata only. Keep `T-P4-COMPILED-LEDGER-BINDING` open until a Lean slot produces a pinned receipt **and** a constructive binding instance.
- Requested action: consume the two ledger theorems only under the explicit records; consume the shifted-baseline and component-cap facts as **obstructions against inferring a `V≤1` / `p45≤45` barrier from imported leaves**. Do **not** edit registry, `state.json`, or formal certificates.
- Lean compile remains for `:10`/`:40` slots if a pin is attached later.

## Commands / hashes

- Inspected commit: `577ace22b54d7f71b60cf8b071e3c6604ba296ad`
- Lean blob SHA: `17163fb87f366a68b9f1f15681c770269d9a39e2`
- Placeholder scan (source text): no `sorry`, `admit`, or `axiom` declarations in this file.
- Lean/Lake executed: no. Exit code: n/a.

## Forbidden-boundary compliance

- Did not treat imported compiled leaves as compilation of this sidecar.
- Did not infer source identity, flowpipe, or coverage.
- Did not treat `ledgerV0 < 1` or `w0 ≤ ledgerV0` as a physical barrier.
- Did not treat the shifted baseline exceeding 45 as a true `p45` lower bound.
- Did not promote registry / state / formal proof.
- Did not close P4/P5/M4 from this sidecar.

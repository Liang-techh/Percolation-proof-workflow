---
kind: review_result
review_id: review-T-P4-SAME-SOURCE-CONSUMER-PACKET-liuchuanafeng-20260908T0315
task_id: T-P4-SAME-SOURCE-CONSUMER-PACKET
agent: 流川枫
source_agent: 流川枫
created_at: 2026-09-08T03:15:00-06:00
inspected_commit: 5d1a2e75a832610c5ac4bd8d69213eba1f7f1ffe
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_SameSourceConsumerPacket.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_SameSourceConsumerPacket.review.md
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DHProducerBaseBridge.lean
integration_status: pending
admission_label: architecture_only
proposed_integration_target: P4.same_source_consumer_packet_open_contract
requested_action: keep as OPEN_UNCOMPILED typed contract; record that ConsumerPacket is row_source plus allocation on one SourceKey; do not treat sidecar review.md, SourceKey strings, or Young 2-2 split as authenticated source/coverage; do not write registry/state
---

# T-P4-SAME-SOURCE-CONSUMER-PACKET — independent interface audit

## 0. Result

The leaf at `NEW_P4_032_SameSourceConsumerPacket.lean` (blob SHA `ca029844b9bd96e516bc8b378e1e02c26f16aad0`) is a **typed same-source allocation adapter**, not a compiled receipt and not a source identity.

It packages, on one `SourceKey` and one `SourceFields` object:

1. a completed `RowInterpretation` (eta/theta/charge/rhoSq with `theta=1`, `rhoSq≥0`, `2*rhoSq≤charge`);
2. `RowSourceEvidence`: `||port||² ≤ rhoSq * A_up` on the source domain;
3. `Allocation`: `target>0` and `target + 2||lBase||² + charge*A_up ≤ base` on that same domain;
4. optional `P4Binding` equalities that transport the unscaled floor `base-totalSq` into `nu*target ≤ m.margin`.

`ConsumerPacket` is exactly the pair `(row_source, allocation)`. Optional `FrontFactorization` is explicitly **not** a premise of `allocated_P4_target`.

The in-tree `.review.md` is a proof-attempt companion, not an inbox `review_result` and not kernel evidence. This lane did not run Lake. `admission_label` is therefore `architecture_only`.

No registry, StateStore, comparator, or formal-admission object is written.

## 1. What the Lean file actually declares

Namespace: `RouteBP4032SameSourceConsumerPacket`.
Header: `OPEN_UNCOMPILED`. Imports: `NEW_P4_032_SourcePositiveTargetBinding`, `NEW_P4_032_MinimalResidualBudgetAdapter`.

`SourceKey` fields (`branch`, three digest strings, three contract strings) are declared provenance. The file states they do not authenticate files or semantics.

`SourceFields key X` binds one domain predicate and four same-state maps: `base`, `lBase`, `port`, `acceleration`. `lBase` and `port` are generalized-force vectors in the same coordinates. `metric` is the fixed rational quadratic

`A_up = (1402217/12000000) a0² + (200739/4000000) a1²`,

not `||lBase||²` and not an acceleration residual used as the P4 `f.residual`.

`totalSq` is `||lBase+port||²` via coordinatewise `sqNorm`, not `||lBase||²+||port||²`.

Algebraic lemmas present in the file (statement-level inspection only; no kernel run):

- `metric_nonnegative` (`positivity`)
- `young_two_vectors`: `||u+v||² ≤ 2||u||²+2||v||²` from `(u-v)` squares
- `charge_nonnegative` from `2*rhoSq≤charge` and `rhoSq≥0`
- `total_residual_bound`: `totalSq ≤ 2||lBase||² + charge*A_up` after Young and the port bound
- `allocationFromUniform`: three rectangular caps imply `Allocation`
- `allocated_source_floor`: `target ≤ base-totalSq` on D
- `allocated_P4_target`: with `P4Binding` and existing `ScaledComparison`, `0 < nu*target ≤ m.margin(embed x)` on the **source** domain
- `front_equals_bound_nominal`: only if `FrontFactorization` is separately supplied

No `sorry` / `admit` token appears in this file text. That is a placeholder scan of source text, not a compile/`#print axioms` receipt.

## 2. Boundaries that must stay visible

- Shared `SourceKey` is a dependent-type lock, not a hash check. Relabeling another function with the same strings does not create `RowSourceEvidence`.
- Printed CSV charge is provenance. `RowInterpretation.charge` may be a conservative enlargement only if justified **outside** this file.
- Young 2-2 is a sufficient split. A tighter correlated allocation is allowed by writing `Allocation` directly; failing `allocationFromUniform` does not refute the direct route.
- `P4Binding.residual_eq` identifies `f.residual` with **total** force `totalSq`, not `A_up`, not `||lBase||` alone, not an acceleration residual.
- `nu` is an externally fixed positive scalar. It is not inferred from `sf` or `theta`, and is not a matrix change of coordinates.
- `allocated_P4_target` covers `src.domain`, not automatically all of `f.domain`.
- `FrontFactorization` must not be silently inserted into the scalar consumer. BODY6/front floors, alpha/beta identification, Schur composition, and PSD remain other leaves.
- Connecting this packet to `SourcePositiveTargetBinding`'s `PortGeneralizedForce` / `WithLp.toLp 2` `norm2` still requires an explicit Euclidean identity; this file does not build that bridge.
- `DHProducerBaseBridge` may construct a `ConsumerPacket` only after `ProducerChain` and `BaseDominance`. Those premises are not discharged here. The acceleration-ray and block-vs-four-angle obstructions from that sibling remain open.

## 3. What this child does *not* close

Still open and not claimed here:

- any concrete `SourceFields`, `RowInterpretation`, `UniformBounds`, `Allocation`, `ConsumerPacket`, or `P4Binding` from live Julia/Python/CSV artifacts;
- authentication of the two `A_up` rationals against a named mass/DH evaluator commit;
- true-DH coefficient identity, descriptor inverse, Float64 reification, interval coverage, trajectory, flowpipe;
- P4/M4 residual closure or registry admission;
- pinned Lean/Lake compile, toolchain pin, `#print axioms`, or independent kernel receipt (this environment did not run `lake`).

## 4. Integration note

Integrator should treat this inbox file as documentation-only routing:

- keep `OPEN_UNCOMPILED`;
- do not promote `ConsumerPacket` or `allocated_P4_target` to a verified P4 margin;
- next mathematical leaf is a same-instance port bound plus either direct `Allocation` or the three-cap test on one authenticated source object;
- next Lean leaf (if released to a pinned `:10`/`:40` slot) is compile + axioms + sorry/admit scan of this sidecar only, without importing producer-bridge or BODY6 keyed-storage as proved premises.

`admission_label: architecture_only`.

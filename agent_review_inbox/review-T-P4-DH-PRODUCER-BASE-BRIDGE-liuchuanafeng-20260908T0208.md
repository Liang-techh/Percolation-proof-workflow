---
kind: review_result
review_id: review-T-P4-DH-PRODUCER-BASE-BRIDGE-liuchuanafeng-20260908T0208
task_id: T-P4-DH-PRODUCER-BASE-BRIDGE
agent: 流川枫
source_agent: 流川枫
created_at: 2026-09-08T02:08:00-06:00
inspected_commit: 8e033f07b4923709499ef39b7e22379f600742fa
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DHProducerBaseBridge.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DHProducerBaseBridge.review.md
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_SameSourceConsumerPacket.lean
integration_status: pending
admission_label: architecture_only
proposed_integration_target: P4.dh_producer_base_bridge_open_contract
requested_action: keep as OPEN_UNCOMPILED typed contract; record the two exact obstructions (acceleration-ray base growth; block-p vs four-angle geometry mismatch); do not treat sidecar review.md or coefficient transcription as authenticated DH/source; do not write registry/state
---

# T-P4-DH-PRODUCER-BASE-BRIDGE — independent interface audit

## 0. Result

The leaf at `NEW_P4_032_DHProducerBaseBridge.lean` is a **conditional producer-to-consumer adapter**, not a source identity and not a compiled receipt.

It does three useful, bounded things:

1. Fixes one prospective compact-DH `lBase` pair and one producer metric `A_up` as *declared* functions on an explicit `State`.
2. Packages the missing mass/descriptor identities into `ProducerChain`, then reuses the existing `zero_defect_port_identity` (imported via the same-source packet / block-defects stack) to build `RowSourceEvidence` *only after* those premises.
3. Isolates the leftover storage inequality as `BaseDominance`, and records two exact algebraic obstructions that any later source/interval child must respect.

It does **not** close base dominance, descriptor inverse, Float64 reification, interval coverage, or flowpipe. The in-tree `NEW_P4_032_DHProducerBaseBridge.review.md` is a proof-attempt companion, not an inbox `review_result` and not kernel evidence. `admission_label` is therefore `architecture_only`.

No registry, StateStore, comparator, or formal-admission object is written.

## 1. What the Lean file actually declares

Namespace: `RouteBP4032DHProducerBaseBridge`.
Header: `OPEN_UNCOMPILED`. Import: `NEW_P4_032_SameSourceConsumerPacket`.

Declared state: four angles `(q2,q3,q4,q5)`, two velocities `(dq4,dq5)`, two accelerations, distal correction, port residual, disturbance, time.

Transcribed force-scale DH residuals (claimed I4=1/5, I5=1/10 after `IVAL*fB-M0BB*aB`):

- `l4 = -3 q4/4 - 4 dq4/5 + w/5 + q5/100 - (350003/3000000) a4`
- `l5 = -29 q5/50 - 13 dq5/20 + w/10 + q4/200 - (200739/4000000) a5`

Producer metric (not silently replaced by nominal `M0_BB`):

- `A_up = (1402217/12000000) a4² + (200739/4000000) a5²`

`source_metric_eq` is definitional: the packet `metric` on this `source` equals `producerMetric`. That is a typing convenience, not a source hash check.

`ProducerChain` premises on a common domain `D`:

- `key.branch = .dh`
- `row.eta = 28/5`
- `D` implies intended four-angle ball `sum_{i=0..3} q_i² ≤ 56/15` and `|q3| ≤ 5π/6`
- left inverse `tailInverse * tailMass = I`
- zero-defect descriptor `MDD * delta_aD + DeltaMDB * aB = 0`
- port identity `rB - MBD * delta_aD = 0`
- operator bound `||Rport * aB||² ≤ rhoSq * A_up`

`rowEvidenceFromProducer` only rewrites the state port through those identities and applies the operator bound. Sign of `Rport` is preserved; a norm-only rewrite would be insufficient.

`BaseDominance` is exactly the packet `Allocation` inequality specialized to `dhLBase` / `producerMetric`:

`target > 0` and `target + 2 ||lBase||² + charge * A_up ≤ base` on `D`.

`packetFromProducer` is then a constructor of the existing `ConsumerPacket` (`row_source` + `allocation`). Field names were checked against `NEW_P4_032_SameSourceConsumerPacket.lean`; this is not an invented type.

## 2. The two exact obstructions that must stay visible

### 2.1 Acceleration ray

`accelerationRay z` sets angles=velocity=disturbance=port=distal=0 and `a=(z,0)`.

Exact identities in the file:

- `||lBase||² = (350003/3000000)² z²`
- `A_up = (1402217/12000000) z²`
- the zero configuration satisfies the *intended* producer geometry (angles all 0).

Hence any `BaseDominance` on a domain that contains the ray point at `z` forces

`base(ray z) ≥ target + [2*(350003/3000000)² + charge*(1402217/12000000)] z²`.

`zero_base_ray_obstruction`: if the ray at `z=1` is in `D`, `charge ≥ 0`, and `base(ray 1) ≤ 0`, then **no** positive target works. Geometry alone does **not** put the ray in the physical/descriptor `D`, and does **not** evaluate storage `base`. The theorem is a conditional allocation block, not an ODE fact.

### 2.2 Block-p does not imply producer geometry

`blockP` is the two-angle/two-velocity predicate `(3/2)(q4²+q5²)+(4/5)(dq4²+dq5²)`.
At `q2=2` and all other displayed coordinates zero, `blockP = 0 ≤ 28/5` while the four-angle sum is `4 > 56/15`.

`block_domain_not_producer_domain` therefore refutes automatic domain transport from the P45 block predicate to the producer ball. It is not a coverage hole in an already-certified interval enclosure; it is a predicate mismatch.

These two facts are the harvest-739 "acceleration ray" and "block-vs-four-angle domain mismatch" obligations. They remain open on the source side.

## 3. What this child does *not* close

Still open and not claimed here:

- authentication that the transcribed rationals equal any live Julia/Python DH evaluator at a named commit (sidecar review.md lists external SHA-256 strings; those are provenance *declarations*, not this agent's re-hash of live files);
- `MDD`, `MDDinv`, `DeltaMDB`, `MBD` identified with one regularized mass source;
- operator bound `||Rport aB||² ≤ rhoSq A_up` on a certified domain;
- storage `base` inequality that dominates `target + 2||lBase||² + charge A_up`;
- exact/outward reification of floating-point ball endpoints;
- Float64 descriptor inverse, true-DH coefficient identity, trajectory, flowpipe, P4/M4 closure;
- Lean/Lake pinned compile, `#print axioms`, or placeholder scan (this lane did not run Lake);
- registry / StateStore / comparator admission.

The file itself warns that the compact branch is a prospective transcription, not line-9 recorded branch identity and not complete physical DH dynamics.

## 4. Integration note

Integrator should treat this inbox file as documentation-only routing:

- keep `OPEN_UNCOMPILED`;
- do not promote `packetFromProducer` to a verified consumer packet;
- next mathematical leaf is a same-instance storage lower bound that either meets `required_base_on_ray` or explicitly excludes the ray from `D`;
- next Lean leaf (if released to a pinned slot) is compile + axioms + sorry/admit scan of this sidecar only.

`admission_label: architecture_only`.

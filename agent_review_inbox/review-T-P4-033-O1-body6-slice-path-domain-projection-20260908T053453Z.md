---
kind: review_result
review_id: review-T-P4-033-O1-body6-slice-path-domain-projection-20260908T053453Z
task_id: T-P4-033-O1-body6-slice
source_agent: codex-body6-math-lane
created_at: 2026-09-08T05:34:53Z
integration_status: pending
status: OPEN_UNCOMPILED
compile_status: OPEN_UNCOMPILED
lean_receipt_status: missing
admission_label: pending
proposed_integration_target: metadata_only
requested_action: review_path_projection_and_shift_accounting_then_obtain_independent_Lean_receipt
artifact_path: examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.lean
artifact_sha256: c3d0432fb2b53815bb9e23271ecadfa871e5526a96b9bf7b533efe392d2aa6ac
companion_path: examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.review.md
companion_sha256: 7b97517e6b27751ed9985e0fc0675bf44f46bd1192c0e5f7f876a38953afda02
---

# BODY6 lane: full-state path projection and shift accounting

This is an independent mathematical companion under the existing BODY6
task `T-P4-033-O1-body6-slice`. It does not create a new node, prove global
h_body_6 or close the parent task. No collector command, registry/state
write or processed marker was issued by this submission.

## Typed result and required inputs

For full-state type X, configuration type C and actual projection
`project : X -> C`, the leaf separately types:

```text
forall t in [0,1], forall x in D(t), project(x) in Q;
forall t in [0,1], path(t) in D(t).
```

Their composition yields `project(path(t)) in Q` at every relevant time.
The projection must match the source coordinates and state/lift map.
Configuration membership alone does not certify all the other constraints
in D(t). Initial membership is separately typed and yields only an initial
projected point.

Exact counterexample: D(t)=(-infinity,0], path(t)=t. Initial membership holds,
but whole-path membership fails at t=1. This is a smooth abstract path,
not an asserted DH solution.

## Shift B is charged exactly once

The storage input is `G(t,x)=F(t,x)+B` on projected configurations in Q.
It must be supplied by the separate source/alignment proof; Alignment is
neither imported nor reproved here. Both path consumers first use the full
state-domain projection before applying this identity.

- From F<=cap and cap+B<=bar, the first consumer gives G<=bar.
- From the already shifted inequality F+B<=cap, the second gives G<=cap
  without another B.

For exact B=4079979/400000 and F=0,G=B, the correct cap B holds but 2B<=B
is false. Double counting can reject a valid shifted bound unnecessarily.
Dropping B is different: F<=1 holds while G<=1 is false, so a fixed-threshold
transfer without the shift is unsound.

## Boundaries and remaining receipt

No concrete domain projection, whole-path membership, source shifted-value
identity, integrated cap, ODE/kinematic relation, ramp/circle invariance or
continuation instance is asserted. In particular, path inclusion is not
deduced from the very barrier being transferred. Later initial/flow proofs
must use the same state map, path, domain and storage normalization.

The sidecar imports only Mathlib and has no new Lean receipt. Existing
compiled ActualStorage/ActualShift receipts do not cover this file. Static
review and artifact hashes are the only new validation; no Lean/Lake or
broad regression ran. Keep integration pending and status OPEN_UNCOMPILED
until independent elaboration/axiom receipts and the required instantiations
are supplied. No theorem/registry promotion is authorized by this envelope.

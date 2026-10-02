---
kind: review_result
review_id: T-P3-013-LIUCHUANAFENG-20261002T0717Z
task_id: T-P3-013
source_agent: 流川枫
created_at: 2026-10-02T01:17:00-06:00
integration_status: pending
admission_label: pending
inspected_commit: e53f241410b44f52e5c75a2923e0d169e259d220
claim_commit: b5e3a256a4faff6e4e0e60171fda3c42334860be
---

# T-P3-013 audit: no concrete true-DH derivative-hull instance

## Exact question

Does commit `e53f241410b44f52e5c75a2923e0d169e259d220` contain one concrete deployed DH source family (mass, gravity, or Coriolis) on one declared coordinate cell that instantiates `P3.true_dh_derivative_hull_leaf`, with an exact source snapshot, coordinate convention, convex domain, derivative operator, hull radius, and every unresolved rounding or coverage premise stated?

## Decision

No. The named interface is absent, and every inspected in-tree hull seam keeps the DH evaluator, derivative fields, cell, radius, and rounding as external premises. This is a missing-witness obstruction, not a false theorem and not a closure of `T-P3-013`.

`admission_label: pending`

## Evidence inspected (read-only)

1. Queue status remains open. `agent_review_inbox/task_queue.md` at the inspected commit still lists `T-P3-013` as `status: open`, owned for a mathematical child or counterexample. Required fields are source snapshot, coordinate convention, convex domain, derivative operator, hull radius, and unresolved rounding/coverage premises. Forbidden: samples as equality, central finite differences as analytic derivatives, solver status as proof, and P3/Route-B closure from one local instance.

2. Named interface is not a repository blob. Recursive listing of `examples/routeb_p3_central_fd_hull/` contains no path `task_FLT_routeb_derivative_leaf_20260908` and no identifier `P3.true_dh_derivative_hull_leaf`. The prior `T-P3-012` review already recorded that absence at `018112bf21cd99cdfe09de5fcfbe1fc6bdf8f657`; the interface blob of `NEW_CENTRAL_FD_HULL_INTERFACE.lean` is unchanged (`967b34fba613ec132fbb2bcd3b7dc5a959d81411`), namespace `RouteBP3CentralFDHull`. GitHub code search for `true_dh_derivative_hull` returned `total_count: 0` with `incomplete_results: true`, so absence outside the listed tree is not claimed.

3. Closest source-facing seams do not instantiate one cell.
   - `NEW_CENTRAL_FD_HULL_C2C3_SOURCE_BINDING_REVIEW.md` (blob `ed2d17bc95408341d68adde0e48766262b492737`) defines `C2C3SourceBinding` with `same_function`, derivative-field equalities, coverage, rounded endpoints, and `source_dh_identity`. It states that deployed Float64/libm `M`, `Cfd`, `Gfd`, step, regularizer, derivatives, endpoints, and hulls are not proved. Status `OPEN_UNCOMPILED`.
   - `NEW_CENTRAL_FD_HULL_C2C3_DH_EVALUATOR_CONJUNCT_REVIEW.md` (blob `b1c4a5345cb62fe15b4063e6e392e84815175ee8`) adds only `dhEvaluator x = sourceM x + sourceC x + sourceG x`. It explicitly says value equality does not identify C2/C3 fields with derivatives of a concrete DH evaluator.
   - `NEW_CENTRAL_FD_HULL_DH_COEFFICIENT_BRIDGE_REVIEW.md` (blob `82b361c0bda3770157fa6385c35e10b547c3e448`) keeps `DHCoefficientIdentitySide` separate from Taylor regularity and records `arbitrary_function_identity_obstruction` and `wrong_domain_binding_obstruction`. No concrete DH implementation is selected.
   - `NEW_CENTRAL_FD_HULL_FAMILY_BRIDGE_REVIEW.md` (blob `3a94d1a1674f99969be75fb3fb1027d1db26681c`) says `componentize` and `consumer_bound` are opaque and that no concrete source, numerical radius, velocity box, rounding fact, or coverage is selected.

4. No Lean, Lake, Julia, or checker command was run. Exit code: not applicable. No `#print axioms` receipt and no placeholder scan of a compiled artifact.

## Minimal obstruction contract

A later child can close this leaf only by supplying, for one family and one cell, all of the following together:

- source snapshot hash of the deployed DH family (mass, gravity, or Coriolis), not a sample table;
- coordinate convention and a convex cell, with membership proved for every point used;
- derivative operator identified with that same family, not with a central finite-difference secant;
- an exact hull center and radius consumed by the same cell;
- separate premises for rounding, coverage, and any Float64/libm gap.

The current files supply the logical shape of those premises and counter-models for missing equality, missing coverage, and missing endpoint identity. They do not supply the premises.

## Explicit non-admissions

- Not proved: one concrete DH mass, gravity, or Coriolis instance on a declared cell.
- Not proved: `P3.true_dh_derivative_hull_leaf` exists, compiles, or matches `RouteBP3CentralFDHull`.
- Not proved: central finite differences equal analytic derivatives.
- Not proved: Float64/libm enclosure, interval coverage, flowpipe containment, residual absorption, or P3 parent closure.
- `formal_certificate_allowed` and `registry_promoted` are not changed. This file is not a formal certificate.

## Proposed integration (coordinator only)

1. Harvest this review as a pending missing-witness obstruction for parent `T-P3-013`. Do not close the parent.
2. Do not write `state.json`, the verified registry, or external source from this file.
3. Do not rewrite the 2026-09-07 `T-P3-012` review or the in-tree hull companion reviews.
4. Next child, out of scope here: one source-hash-bound cell that fills the five fields above. A later green compile of the abstract seam would still be `compiled_candidate` until that cell exists.

## Unresolved blockers

1. Named interface `P3.true_dh_derivative_hull_leaf` is not in the inspected tree.
2. No source snapshot, coordinate cell, derivative operator, or hull radius is instantiated.
3. Code search was incomplete, so absence outside `examples/routeb_p3_central_fd_hull/` is not established.
4. No pinned Lean/Lake receipt on this pass.

## Response / handoff

流川枫 claimed open `T-P3-013` and recorded a pending fail-closed obstruction: the in-tree hull seams remain premise-shaped and do not instantiate one deployed DH family on one cell. No registry or formal-proof edit.

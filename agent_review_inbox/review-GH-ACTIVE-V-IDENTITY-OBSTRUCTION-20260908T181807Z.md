---
kind: review_result
review_id: review-GH-ACTIVE-V-IDENTITY-OBSTRUCTION-20260908T181807Z
task_id: GH-ACTIVE-V-FUNCTION-IDENTITY-TAKEOVER
source_agent: Godel the 6th
created_at: 2026-09-08T18:18:07Z
integration_status: pending
admission_label: pending
status: EXACT_FINITE_SAMESTORAGE_OBSTRUCTION_SAME_RUN_INITIAL_BINDING_ABSENT
source_binding_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
julia_execution: false
ideal_raw_obstruction_recomputed: false
state_mutation: false
registry_mutation: false
threshold_mutation: false
requested_action: consume the finite functional only to block the false certificate-to-energy identity; request a certificate-indexed initial witness and explicit consumer selection separately
---

# Minimal consumable active-V obstruction

This continues the retired lane without altering historical provenance or
task_queue. The current queue describes the missing function-indexed initial
binding, not a completed identity theorem. The predecessor source map is
`agent_review_inbox/review-GH-ACTIVE-V-EXACT-SOURCE-MAP-20260908T180822Z.md`,
freshly checked SHA256
`a6d3e0d8fe71d65445e33c597ddbfafebb7e8acecce448bfde6f87c91e0751fd7`.
No previous ideal raw-energy obstruction was recomputed.

## 1. A five-coordinate finite witness, not a numerical trajectory test

Keep the predecessor's K and X0. At t=0, set q4=s and all other q/v
coordinates zero. The following five rational s values all lie in X0:

```text
s = (-3/20, -3/40, 0, 3/40, 3/20)
w = (1, -4, 6, -4, 1)
Lambda(P) = sum_i w_i P(s_i)
```

The exact moments of Lambda on powers 0..4 are
`(0,0,0,0,243/320000)`. Thus Lambda annihilates every cubic, including every
quadratic plus arbitrary constant or linear compensation. For the 46-row
pinned certificate CSV, the restricted polynomial has degree 4 and a nonzero
q4^4 coefficient; duplicate exponents are combined exactly by the checker.

For the literal-decimal rational polynomial:

```text
c4 = 7549816188904203/125000000000000000
Lambda(P) = 1834605333903721329/40000000000000000000000 != 0.
```

For the polynomial with coefficients decoded by Python binary64 parsing:

```text
c4 = 8704345440016565/144115188075855872
Lambda(P) = 423031188384805059/9223372036854775808000 != 0.
```

The latter is explicitly a Python decode candidate, not an observed Julia
parse or rounded execution. No monomial evaluation in Julia was performed.
This witness is exact finite algebra on coefficients and moments, not sampling
offered as universal proof. Equality of two functions at ALL five points would
force equality of their Lambda values, giving the finite contradiction.

The independently inspected source-expression premise from the predecessor is:
on this entire X0 slice, current Vfull/Vshift/cross and their constant-centered
variants have degree at most two. Velocities are zero, so kinetic/cross terms
vanish; q2=q3=q5=0 fixes U; only q4's quadratic controller term remains.
The checker does not pretend to prove that source premise or parse Julia.

Consequently at least one of these five states refutes exact equality to any
of those energy conventions, independent of the convention's constant anchor.
This is a smaller consumer input than an entire raw envelope or a full source
polynomial expansion. It does NOT identify which point fails without specifying
the comparison polynomial, nor claim a rounded runtime counterexample.

## 2. Consumer rule and status boundary

Given (a) this pinned coefficient interpretation, (b) the same state/time map,
and (c) the energy slice degree<=2 premise, the proposition
`forall x in X0, P(0,x)=Energy_K(x)` is false. A future checked consumer must
refuse THAT sameStorage edge. Adding a constant, flipping a linear sign, or
removing tiny odd coefficients cannot repair the nonzero quartic obstruction.
No coefficients were changed, including small ones.

This is not a rejection of the certificate's own initial inequality. Distinct
functions can share an upper bound. Nor does this install a rejection rule into
the workflow: overall admission remains pending; no registry/state changes.

## 3. Same-run initial_storage_upper is still unbound

Read current external sources under
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`:

- routeB_certificate_manifest.toml binds certificate source, CSV and exporter;
  routeB_export_manifest.toml binds the same CSV to the exporter. These links
  matched current bytes in the predecessor inspection.
- Neither inspected manifest binds the energy-storage producer or its
  initial_storage_upper output. The two manifest timestamps are distinct and
  cannot authenticate a shared run with that independent producer.
- routeB_compact_energy_storage_to_block_audit.py declares its own scalars and
  writes a three-column metric CSV. The CSV has no certificate function hash,
  evaluator hash, run identifier, or function-indexed initial proof reference.
- routeB_compact_block_energy_barrier_audit.py reads that scalar, but neither
  chooses nor evaluates the certificate polynomial. Reading the same scalar
  value elsewhere is not a same-function or same-run relation.

This establishes absence of the link in the bounded inspected chain, not that
the files could never have been produced in one session. File times or matching
radius tokens would not fill the semantic link even if they coincided.

## 4. Shortest viable path now, without forcing identity

If the consumer is explicitly intended to use the CERTIFICATE polynomial:

1. Bind exact coefficient interpretation and evaluator to the CSV hash, and
   bind the consumer's V to that function on the required domain.
2. Supply a checked same-polynomial initial certificate. Existing producer
   syntax pinit=-P(0)+s4p*r0 with r0<=0 would yield P(0)<=0 if pinit>=0 and
   s4p>=0 were genuinely proved after coefficient conversion/reconstruction.
   The source writes a numerical candidate; neither OPTIMAL nor the CSV proves
   those positivity/reconstruction obligations.
3. Then prove 0<=u and bind that u token to this consumer's same-run input
   manifest. P(0)<=0<=u is a valid route WITHOUT a mechanical-energy identity.
   No initial certificate or budget theorem is supplied by this review.

If the consumer is intended to use an ENERGY convention, retain its distinct
function identifier and require its own initial theorem or an independently
proved signed comparison with P. The forbidden exact identity cannot be used.
Any later derivative/tube theorem must be indexed by the selected function;
the present witness claims only the initial identity obstruction.

Minimum missing fields:
`run_key`, `consumer_hash`, `active_function_id`, `certificate_hash`,
`coefficient/evaluator_semantics`, `K`, `X0_embed`, `time0`,
`initial_proof_artifact`, `initial_upper_artifact_hash`, `upper_token`, and
an explicit producer-to-consumer input binding. A run key alone proves none
of the mathematical fields. Do not update the threshold to bypass them.

## 5. New artifacts and actual checks

```text
examples/routeb_active_v_function_envelope/NEW_CONVENTION_identity_obstruction.py
a9101a8f05f48c3efae97f6cf74a9f43b09f926a833be6fb44f73e7a04fc5b62
examples/routeb_active_v_function_envelope/NEW_CONVENTION_identity_obstruction.json
43827e8e52c0bafd33d4bb9982c92a68ffbb0e6ae5ab30f2442b0078579c5bb6
```

The script only reads the pinned CSV and prints JSON. Python -B exited 0 for
exact coefficient/moment assertions. A second focused check confirmed saved
JSON equals the live result and an in-memory changed CSV hash rejects. It did
not run any old envelope, producer, runtime, solver, Lean/Lake or regression.
Only these two NEW_CONVENTION_* files and this review were added.

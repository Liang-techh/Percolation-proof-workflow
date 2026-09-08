---
kind: review_result
review_id: review-GH-CERTIFICATE-INITIAL-WITNESS-HANDOFF-20260908T185035Z
task_id: GH-MATH-P4-CERTIFICATE-INDEXED-INITIAL-WITNESS
source_agent: Godel the 6th
created_at: 2026-09-08T18:50:35Z
immutable: true
status: pending
integration_status: pending
admission_label: pending
receipt_kind: ideal_polynomial_conditional_initial_witness_handoff
proof_status: paper_uniform_inequality_and_exact_coefficient_arithmetic_not_kernel_verified
source_binding_proven: false
runtime_initial_bound_proven: false
registry_eligible: false
formal_certificate_allowed: false
is_runtime_execution_receipt: false
historical_producer_function_binding: null
same_run_event_binding: null
consumer_function_identity: null
runtime_evaluation_observation: null
lean_compile_status: not_run
julia_execution: false
full_regression: false
state_mutation: false
registry_mutation: false
threshold_mutation: false
candidate_path: examples/routeb_active_v_function_envelope/NEW_CONVENTION_initial_witness.py
candidate_sha256: c7e7ba7386eccd5165b82d818d80389c820239586531e5f7b8d24b6b56decc0f
result_path: examples/routeb_active_v_function_envelope/NEW_CONVENTION_initial_witness.json
result_sha256: ff0af76ef94adeb9ded4e4a50d45cdb03ee6ac5503b94283f4893b971c581f34
requested_action: consume only the specified ideal initial witness after independent verification; keep runtime source refinement and consumer function selection open
---

# Immutable handoff: certificate-indexed ideal initial bound

This new envelope freezes existing artifacts; no old source, script, output or
review was modified. The script hash, output hash and all six source pins were
freshly checked at handoff. The full derivation is in
`review-GH-CERTIFICATE-INITIAL-WITNESS-BREAKTHROUGH-20260908T184854Z.md`.

## Six pinned source hashes

All paths in this table are under
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`.

| File | SHA256 |
|---|---|
| routeB_certificate_V.csv | cab4a5182981bccbde18ace2d26ece5c0d7b7d3c3cf4a5a7e02e7fcda9b80601 |
| routeB_export_traj.jl | 35ebe806a46273068af1af937c0c0152378d6889024ec5586bf3c7aabd30eccf |
| routeB_pmi_certificate.jl | 235f4876ed1a3343f6d84f83c0079b4d279886585dc36aeb55b9fc0289177a77 |
| routeB_compact_energy_storage_to_block_audit.py | 80795ef4fcbe0da4fb6d491f040e69196323fc09b01cf5739cb197343ef766b9 |
| routeB_compact_energy_storage_to_block_audit.csv | 8d37219ea1b6189ec84e2eec16aa4fe29e2ee4bd263b946a639fafb7692b2bf1 |
| routeB_compact_block_energy_barrier_audit.py | 62972f8b2049be3351616e25837db722731744f8e3b219d2ddf90fd817026927 |

## Domain, interpretation and selector contract

- Polynomial variable order: (q4,q5,v4,v5,t).
- CSV exponent columns: (e_qa,e_qb,e_dqa,e_dqb,e_t), in that order.
- Exact initial time: t0=0, substituted before polynomial evaluation.
- X0: q4^2+q5^2+v4^2+v5^2<=9/400, all other physical q/v coordinates zero.
- Runtime source variable map: qv[4],qv[5],dqv[4],dqv[5],tv in evalV_fast.
- Upper artifact: routeB_compact_energy_storage_to_block_audit.csv, hash above.
- Unique metric selector: initial_storage_upper.
- Selected exact upper u: 492033745203/25600000000000.
- Consumer source: routeB_compact_block_energy_barrier_audit.py, hash above;
  exact source selector is `V0 = frac(storage["initial_storage_upper"])`.
- Consumer threshold remains its unchanged `V_BAR = Q(1)`; this envelope does
  not choose its V function or supply its source/domain/growth identities.

## Output summary bound to the saved JSON hash

| Exact coefficient interpretation | Assembled all-X0 upper |
|---|---|
| Decimal tokens interpreted as rationals | -204425232114270201852797865697329551/4000000000000000000000000000000000000 |
| Python binary64 values decoded to rationals | -1326795613140222765930326078920268719/25961484292674138142652481646100480000 |

Both upper values are strictly below -1/20. Thus each explicitly specified
ideal polynomial satisfies P(x,0)<=-1/20<0<u for every x in X0.

Proof mechanism: exact t0 restriction, symmetric quadratic reconstruction,
lambda=max(0,max_i(Aii+sum_(j!=i)|Aij|)), and absolute monomial bounds for
degrees 1,3,4. Then
P<=c0+lambda*(9/400)+l1*(3/20)+l3*(3/20)^3+l4*(3/20)^4.
The saved JSON includes all coefficients, matrix entries, losses and margins.
No numerical eigenvalue, optimization, sampling, pinit/SOS success flag or
old obstruction calculation is used.

## Execution and admission boundary

The preceding actual Python -B run returned exit 0 and saved/live output equality
was checked. An in-memory false-upper mutation was rejected. This handoff only
rehashes files and reads the saved summary; it does not claim another producer
run. The user's reported independent run is not fabricated into a new log or
runtime receipt here.

Python binary64 decoding is not proof of Julia parsing or rounded evalV_fast.
The ideal polynomial witness does not retroactively bind the historical upper
producer to this certificate, select the consumer's active function, establish
a common run-id, or prove a trajectory/barrier theorem. A runtime error bound
and evaluator/consumer refinement would still be needed for actual execution.

Status remains pending. This is an ideal polynomial conditional initial witness,
not a source admission, runtime initial-bound theorem, or runtime execution receipt.
All four required flags remain false: source_binding_proven,
runtime_initial_bound_proven, registry_eligible, formal_certificate_allowed.

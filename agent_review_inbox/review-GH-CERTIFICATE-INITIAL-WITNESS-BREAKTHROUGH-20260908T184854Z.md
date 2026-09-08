---
kind: review_result
review_id: review-GH-CERTIFICATE-INITIAL-WITNESS-BREAKTHROUGH-20260908T184854Z
task_id: GH-MATH-P4-CERTIFICATE-INDEXED-INITIAL-WITNESS
source_agent: Godel the 6th
created_at: 2026-09-08T18:48:54Z
immutable: true
status: pending
integration_status: pending
admission_label: pending
result: EXACT_IDEAL_CERTIFICATE_INITIAL_UPPER_CONSTRUCTED
proof_status: paper_uniform_inequality_and_exact_coefficient_arithmetic_not_kernel_verified
ideal_initial_witness_constructed: true
source_binding_proven: false
runtime_initial_bound_proven: false
historical_producer_function_binding: null
same_run_event_binding: null
consumer_function_identity: null
is_runtime_execution_receipt: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
julia_execution: false
old_obstruction_recomputed: false
state_mutation: false
registry_mutation: false
threshold_mutation: false
candidate_path: examples/routeb_active_v_function_envelope/NEW_CONVENTION_initial_witness.py
candidate_sha256: c7e7ba7386eccd5165b82d818d80389c820239586531e5f7b8d24b6b56decc0f
result_path: examples/routeb_active_v_function_envelope/NEW_CONVENTION_initial_witness.json
result_sha256: ff0af76ef94adeb9ded4e4a50d45cdb03ee6ac5503b94283f4893b971c581f34
requested_action: independently verify this explicit certificate-indexed ideal initial witness; then bind the actual evaluator and selected consumer without inferring historical execution
---

# New certificate-indexed initial witness, not another obstruction audit

There is a direct exact initial proof for the current certificate polynomial.
It needs no new SOS solve or positivity claim about the old pinit certificate:

```text
For all x in the fixed block-only X0,
P(q4,q5,v4,v5,0) <= -1/20 < 0 < initial_storage_upper.
```

This holds separately for (i) the literal CSV decimal-rational coefficient
function and (ii) the polynomial whose coefficients are Python-parsed binary64
values decoded exactly to rationals. Neither interpretation is silently
identified with actual Julia parsing/rounded evaluation.

## Fixed inputs and directly checkable source map

All mathematical source inputs were read from the current external directory
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`.
The new script pins and verifies six files:

```text
routeB_certificate_V.csv
cab4a5182981bccbde18ace2d26ece5c0d7b7d3c3cf4a5a7e02e7fcda9b80601
routeB_export_traj.jl
35ebe806a46273068af1af937c0c0152378d6889024ec5586bf3c7aabd30eccf
routeB_pmi_certificate.jl
235f4876ed1a3343f6d84f83c0079b4d279886585dc36aeb55b9fc0289177a77
routeB_compact_energy_storage_to_block_audit.py
80795ef4fcbe0da4fb6d491f040e69196323fc09b01cf5739cb197343ef766b9
routeB_compact_energy_storage_to_block_audit.csv
8d37219ea1b6189ec84e2eec16aa4fe29e2ee4bd263b946a639fafb7692b2bf1
routeB_compact_block_energy_barrier_audit.py
62972f8b2049be3351616e25837db722731744f8e3b219d2ddf90fd817026927
```

K here freezes that inspected source/configuration bundle, coefficient
interpretation and state/time map; it does NOT merge the certificate function
with mechanical energy or adopt another gain/regularizer convention. This
initial polynomial proof needs no new physical M, U or controller assumptions.

The CSV header/order is exactly coeff,e_qa,e_qb,e_dqa,e_dqb,e_t. The exporter
reads this file at lines 66-78 and evalV_fast binds its variables to
qv[4],qv[5],dqv[4],dqv[5],tv at lines 114-123. Time is fixed to t0=0; every
positive-time-power term vanishes under exact substitution. No small
coefficient is discarded. Equal monomials are combined exactly.

X0 remains q4^2+q5^2+v4^2+v5^2<=9/400, with all other physical q/v coordinates
zero. This is not the runtime full-state Monte Carlo sample distribution.

The upper is read by the unique metric selector initial_storage_upper from
the pinned energy CSV, giving u=492033745203/25600000000000>0. The barrier's
line 54 reads exactly that selector; the script also checks this source token.
These are a source-level file/selector/variable-order map, not proof of a
historical read event or evidence that the barrier selects the polynomial P.

## Exact uniform proof

Write x=(q4,q5,v4,v5) and r=3/20. After t0 substitution, decompose the complete
polynomial as P(x)=c0+P1(x)+x^T A x+P3(x)+P4(x), with symmetric rational A.
Each mixed quadratic coefficient is split equally between Aij and Aji; every
quadratic coefficient is checked against its reconstructed matrix entry.

Define

```text
lambda = max(0, max_i (Aii + sum_(j!=i) |Aij|))
l_d = sum_(|alpha|=d) |c_alpha|,  d=1,3,4.
```

For each off-diagonal pair, 2*Aij*xi*xj<=|Aij|*(xi^2+xj^2), by the two square
inequalities (xi-xj)^2>=0 and (xi+xj)^2>=0. Therefore x^T A x<=lambda*||x||^2.
This is a direct quadratic-form upper proof, not a numerical eigenvalue or
unproved mass norm claim. Since ||x||^2<=r^2 gives |xi|<=r, every higher/lower
monomial satisfies |x^alpha|<=r^|alpha|. Hence uniformly on the whole X0:

```text
P(x) <= Ucert := c0 + lambda*r^2 + l1*r + l3*r^3 + l4*r^4.
```

All coefficients, the reconstructed matrix, row bounds, absolute coefficient
sums, losses and rational margins are included in NEW_CONVENTION_initial_witness.json.
The two exact assembled upper bounds are:

```text
decimal-token Real:
-204425232114270201852797865697329551 / 4000000000000000000000000000000000000

Python binary64-decoded Real:
-1326795613140222765930326078920268719 / 25961484292674138142652481646100480000
```

Both are <=-1/20, checked with exact integer/Fraction arithmetic. Since the
selected u is positive, P<=-1/20<u follows. The auxiliary -1/20 bound is only
a newly proved conservative initial upper, NOT an edited consumer threshold.
No raw/shifted-energy envelope, finite-difference nonidentity calculation,
origin shortcut, numerical optimization, sampling, or old producer was used.

## What this changes and what it cannot retroactively establish

Previously a certificate-indexed ideal initial theorem was missing. The
explicit proof above now supplies a finite, independently reproducible witness
for those two specified coefficient interpretations. It does not depend on
whether the original scalar/SOS solve's pinit positivity was sound, because it
directly bounds the final exported coefficient function.

It remains incorrect to say that the historical energy producer proved this
bound for P. The new proof is an independent certificate-indexed producer,
not a reconstruction of the historical run. Equal selected scalar values and
source filenames do not establish a common execution event.

The minimal remaining mathematical/source gap for actual runtime initial use:

1. Bind Julia's coefficient decoding to the selected exact interpretation and
   prove the same variable map and evaluator semantics. If only a uniform
   execution upper error epsilon is available, require
   evalV_fast(0,x)<=P(0,x)+epsilon and epsilon<=u+1/20 on X0. No epsilon is
   generated here; binary64 coefficient parsing is not arithmetic evaluation.
2. Prove the actual consumer's V is THIS function (or explicitly bound runtime
   evaluator), rather than the distinct Vfull/Vshift/cross/ActualStorage family.
3. Record the new witness's input hashes and output hash in a genuine future
   producer/consumer event chain. Preserve the historical run IDs, if supplied;
   no fabricated retrospective run_id can fill this gap.

If only an ideal initial-set theorem is being consumed, item 1's runtime layer
is unnecessary, but the exact interpretation, X0 and function identity still
must be explicit. A trajectory/barrier theorem additionally needs the matching
growth, domain coverage and threshold consumer; none follows from this initial
bound. Registry admission and independent proof verification remain separate.

## Executable witness and actual validation

From the workflow root:

```powershell
python -B examples/routeb_active_v_function_envelope/NEW_CONVENTION_initial_witness.py
```

This read-only script checks source hashes, CSV shape, integer exponents,
degree, t0 substitution, quadratic reconstruction, exact upper arithmetic,
unique upper selector and source variable/selector tokens; it writes stdout
only. It exited 0. A focused second check confirmed saved/live equality and
rejection after an in-memory false-bound mutation changed the constant to 1.
The temporary mutation was never written to a source or witness file.

Only the two new NEW_CONVENTION_initial_witness files and this inbox review
were created. No external source, state, registry, threshold or shared script
was changed. No local Lean/Lake, Julia, producer, solver or full regression ran.
Status remains pending; this is not a runtime execution or admitted theorem receipt.

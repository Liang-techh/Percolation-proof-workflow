---
kind: review_result
review_id: review-GH-ACTIVE-V-CERTIFICATE-INITIAL-CONTRACT-20260908T183316Z
task_id: GH-ACTIVE-V-CERTIFICATE-INDEXED-INITIAL-BINDING
source_agent: Godel the 6th
created_at: 2026-09-08T18:33:16Z
immutable: true
status: pending
integration_status: pending
admission_label: pending
result: NO_CERTIFICATE_INDEXED_INITIAL_PRODUCER_CONSUMER_RUN_BINDING_FOUND
source_binding_proven: false
initial_bound_binding_proven: false
runtime_execution_proven: false
registry_eligible: false
formal_certificate_allowed: false
is_initial_bound_receipt: false
is_runtime_execution_receipt: false
obstruction_recomputed: false
lean_compile_status: not_run
julia_execution: false
state_mutation: false
registry_mutation: false
threshold_mutation: false
requested_action: obtain the explicit certificate-indexed initial proof and producer-consumer input event chain; use the proposed finite contract only after separate implementation review
---

# Certificate-indexed initial upper: bounded search and decidable contract

No real producer/consumer/run binding was found in the inspected chain. This
does not claim nonexistence outside the bounded source search. No finite-
difference or ideal raw obstruction was rerun. Only this new review is written.

External source root E:
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`.

## Additional paths checked and why they do not close the link

| Located path | Actual behavior | Missing edge |
|---|---|---|
| certificate/export manifests | bind certificate CSV and exporter bytes; certificate manifest has initial_radius | neither has certificate-indexed upper artifact/proof or producer-consumer run_id |
| routeB_export_manifest.jl:11-39 | reads already existing trajectory/state/V files, counts rows, writes hashes and Dates.now() | can be run after export; timestamp is manifest creation, not authenticated execution continuity |
| energy_storage_to_block_audit.py:44-51,78 | independently calculates a scalar from declared bounds and radius | no input certificate, coefficient interpretation, evaluator or initial proof binding |
| block_energy_barrier_audit.py:54 | reads that metric CSV's initial_storage_upper | no certificate function selected or same-run initial proof reference |
| energy_global_barrier_audit.py:17,30,65 | propagates the same metric CSV upper | another numeric consumer, no new function binding |
| energy_finite_time_budget_audit.py:24 | hardcodes the same rational upper | copied number is not a producer/input binding |
| energy_semantic_bridge.py | reads power/FD/global-barrier/pointwise/mass ledgers; reconstructs a conditional tube | never reads certificate V; source-locked flags do not supply its value/initial identity |
| scripts/record_routeb_storage_progress.py:155-173 | reads an LP candidate, checks beta/coefficient arithmetic, records a different conditional initial budget | different function family/candidate; J1 and uniform gate remain explicitly unproved |

The semantic bridge's full-state branch explicitly rejects when its historical
global barrier is not closed. Its other branch is still conditional and cannot
serve as certificate-polynomial initial evidence. No producer was executed.

The existing scalar auxiliary export in pmi_certificate:422-445 contains
Float64 polynomial terms, including pinit and numbered multipliers. The entry
named V there is aux.V=V0s, whereas routeB_certificate_V.csv is the complete
Vn including A1/A2 velocity and kinetic terms. A consumer must not equate these
two V labels. The verify CSV's mc_min_pinit is sampled evidence, not exact
positivity or reconstruction. A separate scalar solve's terms are not proved
by a PMI Gram export merely sharing alpha_selected.

## Current field-level gaps

Fresh TOML parsing found only initial_radius among initial/storage/run_id fields
in the certificate manifest, and none in the export manifest. The energy CSV
contains exactly one initial_storage_upper row with value
492033745203/25600000000000, but only metric/value/note columns.

Absent or unproved fields are:

- selected consumer function definition and its certificate-indexed evaluator;
- exact coefficient semantics and the value-refinement theorem for that evaluator;
- one K/X0/time0 binding shared by the proof and consumer (block-only embedding);
- proof that THIS decoded certificate polynomial is initially <= THIS upper;
- input/output artifact hashes linking that proof/upper producer to the consumer;
- actual execution-event association, including whether an artifact is reused
  from an earlier producer run, not simply an equal run_id string;
- independently checked proof-verifier/runner provenance, where execution or
  theorem-verification claims are made.

## Minimal decidable candidate contract (proposed, not installed)

Use one closed immutable sidecar with exact field sets and two distinct layers.

### A. Finite mathematical binding

1. `function`: certificate bytes hash, explicit coefficient interpretation,
   canonical exponent-vector polynomial, variable order (q4,q5,v4,v5,t),
   t0=0, and exact embedding into the fixed block-only X0. Interpret decoded
   binary64 coefficients as exact dyadics only via a reviewed parser/decoder.
   Literal-decimal and decoded-binary64 functions must have different keys.
2. `domain`: rational g(x)=9/400-(q4^2+q5^2+v4^2+v5^2)>=0, remote coordinates
   zero. Additional domain constraints must be explicit and X0 containment
   proved; an arbitrary smaller proof box cannot replace X0.
3. `upper`: artifact hash, exact unique metric selector and canonical rational
   token u. Reject duplicate metric rows, even if equal, and do not silently
   parse a stale alternate output file. Preserve the consumer's current threshold.
4. `initial_witness`: a finite rational SOS representation
   `u-P(x,0) = z0^T Q0 z0 + g(x)*z1^T Q1 z1`.
   A smaller useful alternative is a witness for `-P(x,0)` plus exact 0<=u.
   Each Gram matrix uses exact rational entries and a finite PSD witness,
   for example Q=L*diag(d)*L^T with every d>=0. Explicit monomial bases and
   full coefficient equality are mandatory. No floating tolerance or eigenvalue
   sample is accepted. This is a sufficient certificate language, not a claim
   that every true initial inequality has a witness in the chosen language.
5. `consumer_identity`: the consumer's function must be this canonical P, or a
   separately checked exact value adapter must connect its definition to P.
   A free-form function name/hash string alone is not an identity proof. For an
   arbitrary Julia evaluator, a semantic theorem or bounded execution-error
   refinement remains separately required. If |V_runtime-P|<=epsilon is used,
   initial arithmetic must prove P<=u-epsilon, not merely P<=u.

A finite verifier can decode the rows, reject malformed/nonfinite data, combine
monomials exactly, substitute t0, check all coefficient identities and PSD
factorizations, and compare rational budgets. Existing pinit/multiplier terms
may be candidate inputs to this process, but no exact SOS witness was acquired
or reconstructed in this task. The prior nonidentity obstruction is not needed
to run these initial checks.

### B. Producer-consumer execution association

Require content-addressed `producer_event` and `consumer_event` records:

```text
producer_event:
  event_id, runner/environment identity, command/source hash,
  input artifact hashes (certificate, K/X0, proof inputs),
  output hashes (upper, initial witness), execution record reference
consumer_event:
  event_id, consumer/source hash, selected function key,
  input hashes equal to the exact producer outputs,
  producer_event reference, unchanged upper selector/threshold
```

If the producer output is reused, preserve its original event ID and add a
consumer input reference. Do not invent a common fresh run ID. A declared
single-run bundle needs a real event chain showing the producer output exists
before consumption and that the bytes consumed are those hashed outputs.
stdout/stderr hashes and exit zero alone do not authenticate this association.
Whether the runner actually executed or the source read the stated inputs is
an independent trusted-runner/instrumentation obligation; finite JSON equality
can establish only record consistency. No schema can decide arbitrary program
semantics merely from names and logs.

### Status rules

- Missing evidence or unsupported semantic/proof-verifier bridge: pending.
- Present hash drift, duplicate keys/rows, wrong X0/function/upper, failed exact
  polynomial identity or PSD witness: reject that candidate binding.
- All finite checks pass: candidate-consistent only; source/runner verification
  and admission remain explicit separate gates. No automatic registry promotion.

Thus the contract is mechanically decidable for its finite certificate language
without pretending that source correctness or historical execution is decidable
from a manifest. It cannot repair the historical run by manufacturing IDs.

## Fresh artifact hashes and validation boundary

```text
routeB_certificate_manifest.toml d9ae90af1860364eae950649b3ffbf1810d78583383781ec9fa6949fdd24f495
routeB_export_manifest.toml 5b61d624f4f6060da8c33a51fa7982bef8206d2c3924babb512440defad89187
routeB_export_manifest.jl 56f19ff1ed46bafe7ba98a313b2939d16cab9b7ff3d29c84bb4941e784cf443e
routeB_certificate_V.csv cab4a5182981bccbde18ace2d26ece5c0d7b7d3c3cf4a5a7e02e7fcda9b80601
routeB_certificate_multipliers.csv 3ef17b77e7e368d1d980e6c79659cf55de795746788d2221cb288cf8c58d84e7
routeB_certificate_verify.csv 54e98bbbf6e78d0f2c2b703f36eed172c6c00f5458c1df6b13ee0b4b20ca0ea7
routeB_compact_energy_storage_to_block_audit.py 80795ef4fcbe0da4fb6d491f040e69196323fc09b01cf5739cb197343ef766b9
routeB_compact_energy_storage_to_block_audit.csv 8d37219ea1b6189ec84e2eec16aa4fe29e2ee4bd263b946a639fafb7692b2bf1
routeB_compact_block_energy_barrier_audit.py 62972f8b2049be3351616e25837db722731744f8e3b219d2ddf90fd817026927
```

Python -B performed hashes, TOML field inspection and unique upper-row checking,
exit 0. It did not execute any inspected script. This review is neither an
initial-bound nor runtime execution receipt. Registry eligibility remains false.

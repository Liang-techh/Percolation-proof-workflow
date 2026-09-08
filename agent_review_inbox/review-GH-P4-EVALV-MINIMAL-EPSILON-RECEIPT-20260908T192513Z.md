---
kind: review_result
review_id: review-GH-P4-EVALV-MINIMAL-EPSILON-RECEIPT-20260908T192513Z
task_id: GH-MATH-P4-EVALV-ACTUAL-ERROR-BOTTLENECK
source_agent: Godel the 6th
created_at: 2026-09-08T19:25:13Z
immutable: true
status: pending
integration_status: pending
admission_label: pending
result: ACTUAL_LOWERING_PARSER_AND_LIFETIME_BINDINGS_NOT_FOUND
proof_status: minimal_receipt_contract_and_nonentailment_audit
epsilon_generated: false
certified_epsilon: null
parser_coefficient_bits: null
loaded_exponent_table: null
operation_graph_artifact: null
lowering_semantic_witness: null
lifetime_witness: null
runtime_error_witness: null
source_binding_proven: false
runtime_initial_bound_proven: false
registry_eligible: false
formal_certificate_allowed: false
julia_execution: false
lean_compile_status: not_run
state_mutation: false
registry_mutation: false
requested_action: require the semantic fields below before consuming any one-sided epsilon; a design cap is not a receipt
---

# Actual evalV error bottleneck: minimum one-sided receipt

This is an immutable review of what a future epsilon receipt must contain,
NOT an epsilon receipt asserting a proved runtime bound. No Julia, Lean,
producer, initial-bound audit, old obstruction or full regression was run.
Only this new review is written; prior artifacts are unchanged.

## Bounded search result

Read and searched the current external Route-B directory
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`
for evalV_fast/V_coeffs/V_exps in Julia, Python, JSON, TOML, LLVM and text files.
Searched workspace examples/src/scripts for code_typed, code_llvm, code_lowered,
lowered_ir, operation_graph, parser_bits, coefficient_bits and evalV references;
also searched artifact/example filenames for evaluator/lowering/parser packets.

The only external evalV implementation located was routeB_export_traj.jl.
The workspace source match was its historical snapshot. No actual evalV-bound
operation graph, loaded coefficient bits/exponent table, or source/lowering
refinement witness was found in this bounded search. This is not a claim about
unsearched locations, other hosts or hidden Julia runtime state.

Static source confirms:

- lines 67-76: String CSV reader, Float64 coefficient parsing and exponent
  parse(Float64)->round->Int, paired pushes into mutable global arrays;
- lines 112-121: q4,q5,v4,v5,t order, row-indexed power/product expression,
  sequential source accumulation and @inbounds access;
- no source operation trace establishing the concrete power implementation,
  variadic multiplication dispatch, optimized lowering or backend rounding.

The saved ideal initial witness explicitly leaves historical producer binding,
consumer identity, same-run association and runtime evaluation null. The
conservative kappa design does not fill any of those fields.

## One mathematical target, six indispensable receipt objects

Let P_star be ONE hash-bound coefficient interpretation from the existing
initial witness. For finite binary64 inputs whose decoded block state x lies
in X0 and whose decoded time is zero, the requested conclusion is

```text
the call terminates normally with finite y,
Decode(y) - P_star(x,0) <= epsilon,
epsilon <= u + 1/20,
u = the exact selected initial_storage_upper token.
```

Together with P_star<=-1/20 this gives Decode(y)<=u. The minimum receipt needs
the following six objects; field values alone are not proofs.

| Object | Required content and evidence | Current state |
|---|---|---|
| function/domain key | source and coefficient hashes, exact interpretation, row/variable order, t0, decoded-input X0, selected upper artifact/hash/unique selector | static candidates exist; runtime mapping unproved |
| reader packet | ordered actual coefficient bits and exponent integers linked to raw row cells, or a verified parser semantics theorem deriving them | absent |
| lowering packet | concrete call types and semantics for power/product/accumulation, graph/body and loop correspondence, compiler/backend arithmetic policy | absent |
| lifetime packet | valid lengths/types and preservation of coefficient/exponent arrays and arguments through the relevant evaluation | absent |
| uniform error proof | finite ranges, parser discrepancy and execution discrepancy with one-sided final bound over ALL specified inputs | absent |
| consumption packet | same function/upper selector at actual consumer, input/event association, independently checked proof dependencies | absent |

The top-level arithmetic epsilon may be nonnegative for a simple sufficient
contract, although a genuinely proved signed upper error could be negative.
The budget and all proof references must use one identical function/domain key;
accepting a correctly formatted hash without reading/binding its bytes is not
sufficient. No arbitrary non-null 'verified' field is a proof verifier.

## Minimal error split, without double counting

Let P_J be the unrounded polynomial using actual Julia-loaded coefficient bits
and the proved exponent tuples. Require uniform one-sided bounds

```text
P_J(x,0) - P_star(x,0) <= epsilon_parse
Decode(evalV_fast(...)) - P_J(x,0) <= epsilon_ops
epsilon_parse + epsilon_ops <= u + 1/20.
```

This is the entire mathematical composition; no extra coefficient charge is
added if the operation proof already measures error directly from P_star.
Exponent equality is a discrete precondition, not an epsilon_parse allowance.
Changing exponents can change the function by order one or invalidate powers
at zero. A certificate for one interpretation cannot be reused for another
without the corresponding coefficient comparison.

The reader packet must retain row order even if P_star merges duplicate
monomials. The runtime evaluates every row, including positive time powers;
ideal t0 substitution does not justify skipping runtime operations. The error
proof must either keep them or justify finite power/product and zero rules.

For decoded inputs already in X0, input-conversion error is zero by definition.
For rounded arbitrary real inputs it is a separate third bridge and may need
expanded domain coverage; it cannot silently be assigned zero.

## What qualifies as an operation/lowering witness

A genuine code_typed/code_llvm dump, if later supplied, would still be only
candidate data. It must be tied to the source, call signature, method world,
compiler/settings and final executed semantics. A graph from another signature
or a trace at one input is not a uniform error theorem.

An actual graph is NOT logically indispensable: a verified implementation-
semantics theorem covering every permitted lowering can replace it. Thus the
strict blocker is the absence of BOTH an actual graph with refinement and a
covering semantics theorem, not the absence of one favored dump format.

The packet must resolve or bound integer powers 0..4, variadic product lowering,
row accumulation, allowed fusion/reassociation, rounding/subnormal policy,
overflow/nonfinite exclusions and memory/index safety. The @inbounds source
requires the aligned-length invariants; the signature itself is generic.

The kappa design assumed particular power accuracy and a five-multiplication
fold followed by 46 additions. Its conditional local caps cannot establish
that Julia used that fold or satisfies its errors. An alternative lowering
may have a valid bound, but that bound must be proved rather than copied from
the design. All actual local/error fields remain null in this review.

## Strict field-level obstruction: existing facts do not imply the receipt

1. File hashes plus parser source do not imply loaded bits. Either a parser
   correctness theorem or an authentic loaded-state binding is missing. Python
   decoding is a different implementation, not that missing identity theorem.
2. Even genuine post-read bits are insufficient without preservation. The
   arrays are mutable; an unexcluded later NaN write yields no finite returned
   Real value despite unchanged CSV and source hashes. This is a countermodel
   to the incomplete contract, not an assertion that the deployed run did so.
3. Array snapshots plus source arithmetic text do not prove a local rounding
   theorem. Without concrete lowering or covering semantics, epsilon_ops has
   no verified producer. Filling it with kappa or a multiple of kappa is circular.
4. A finite trace at one point cannot discharge the all-X0 quantifier. Inputs
   include zeros/subnormals, so normal-only relative arithmetic assumptions
   cannot be inferred from ordinary sampled values.
5. Even a valid evalV epsilon does not select the independent energy consumer's
   V. Consumer identity is a separate final premise, not numerical budget slack.

These establish nonentailment from the available evidence, not impossibility
of proving a runtime bound once the missing semantics are supplied.

## Status/admission rules for a future receipt

Absent semantic or evidence component => pending. Present mismatched source,
exponent table, domain, selector, graph/refinement binding or failed finite
error inequality => reject that candidate receipt. Syntactic consistency alone
never implies source_binding_proven or runtime_initial_bound_proven. Independent
verification and registry admission remain separate; no runtime epsilon has
been generated by this task.

## Fresh content bindings

```text
E/routeB_export_traj.jl
35ebe806a46273068af1af937c0c0152378d6889024ec5586bf3c7aabd30eccf
E/routeB_certificate_V.csv
cab4a5182981bccbde18ace2d26ece5c0d7b7d3c3cf4a5a7e02e7fcda9b80601
examples/routeb_active_v_function_envelope/NEW_CONVENTION_initial_witness.json
ff0af76ef94adeb9ded4e4a50d45cdb03ee6ac5503b94283f4893b971c581f34
```

E denotes the external root above; the examples path is in the workflow
workspace. Hashes were checked read-only. No epsilon output, runtime evidence,
state/registry change or admission promotion is represented by this envelope.

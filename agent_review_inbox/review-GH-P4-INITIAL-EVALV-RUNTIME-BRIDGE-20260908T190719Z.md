---
kind: review_result
review_id: review-GH-P4-INITIAL-EVALV-RUNTIME-BRIDGE-20260908T190719Z
task_id: GH-MATH-P4-INITIAL-WITNESS-EVALV-RUNTIME-BRIDGE
source_agent: Godel the 6th
created_at: 2026-09-08T19:07:19Z
immutable: true
status: pending
integration_status: pending
admission_label: pending
result: SOURCE_MAP_CHECKED_MINIMAL_ONE_SIDED_EPSILON_CONTRACT_SPECIFIED
proof_status: conditional_semantic_error_bridge_design_not_runtime_verification
source_binding_proven: false
runtime_initial_bound_proven: false
registry_eligible: false
formal_certificate_allowed: false
runtime_execution_observation: null
generated_epsilon: null
same_run_event_binding: null
consumer_function_identity: null
is_runtime_execution_receipt: false
julia_execution: false
lean_compile_status: not_run
full_regression: false
state_mutation: false
registry_mutation: false
threshold_mutation: false
requested_action: provide the parser/loaded-array and operation-semantics witnesses, then verify a same-domain one-sided epsilon budget before claiming runtime initial upper
---

# evalV_fast: final ideal-to-runtime initial bridge

This bounded task only read source files, saved witness text and hashes. It
did not rerun the initial polynomial audit, the old obstruction, Julia, Lean,
or a regression suite. Only this new immutable review is written.

## Source facts now checked

External root E:
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`.

| Source in routeB_export_traj.jl | Concrete behavior | Remaining semantic condition |
|---|---|---|
| 66-78 | readdlm reads routeB_certificate_V.csv as String cells; first-character c rows are skipped; coeff parses as Float64 | loaded table must match the pinned bytes and contain only the intended header plus rows |
| 73-76 | exponent cells parse as Float64, then round and Int; coefficient/exponent arrays are appended together | exact correspondence to the intended nonnegative integer tuples, concrete Int width and parser behavior |
| 68-69 | V_coeffs is Float64[], V_exps is NTuple{5,Int}[] | equal lengths, order and no intervening mutation before use |
| 112-120 | x1..x5=qv[4],qv[5],dqv[4],dqv[5],tv; total starts at 0.0; each row is evaluated and accumulated | concrete Float64 dispatch, input lengths, power/multiply/add semantics, lowering and arithmetic environment |
| 96-97 | first qs/dqs columns copy initial q/dq | no stronger X0 membership proof follows from copying |
| 164-167 | first displayed time uses k=1 and tk=(k-1)*0.005, then evalV_fast | prove the concrete first-call value decodes to exact zero; 0.005 need not itself be exact |

The polynomial object named V built on line 77 is not subsequently evaluated
by evalV_fast; its numeric arrays are the actual inputs. A proof about symbolic
subs(V,...) alone is therefore insufficient. There is no @fastmath, explicit
muladd/fma or rounding-mode setter in the inspected file, but their absence is
not a proof of compiler/backend semantics. The source does not pin an executed
power implementation or operation DAG.

The only writes to V_coeffs/V_exps visible in this file are initialization and
push!. They remain mutable globals; a source-local search is not an execution
noninterference proof. The @inbounds loop specifically needs valid aligned
array lengths and input indices. No loaded arrays or bits were observed here.

## What t0=0 does, and what it does not do

The ideal witness substitutes t0=0 and drops positive-time-power terms. The
Julia evaluator instead executes all row expressions, including the other
powers/products before multiplication by x5^e5. Removing those rows from a
runtime model requires proving:

- exact exponent tuples and power identities for exponent zero versus positive;
- finite, non-NaN intermediate values (in particular no infinity times zero);
- the effect of signed zero and its addition on the real-decoded output.

These can be proved for a bound, without requiring identical zero sign bits.
Alternatively keep every row in the operation-error certificate. Do not assume
the source loop skips those rows because the ideal polynomial does.

## Minimal contract sufficient for the existing initial witness

Choose ONE exact coefficient interpretation P_star from the pinned initial
witness. Quantify over finite binary64 inputs qhat,vhat with

```text
x = (Decode(qhat[4]), Decode(qhat[5]), Decode(vhat[4]), Decode(vhat[5]))
sum_i x_i^2 <= 9/400; all remote decoded q/v entries zero;
Decode(that)=0.
```

The ideal witness already gives P_star(x,0)<=-1/20 on this X0. Let u be the
same exact selected token 492033745203/25600000000000. The smallest additional
mathematical premise is a uniform ONE-SIDED error bound and finite result:

```text
Decode(evalV_fast(qhat,vhat,that)) - P_star(x,0) <= epsilon,
0 <= epsilon <= u + 1/20.
```

Then Decode(evalV_fast)<=-1/20+epsilon<=u. This is only substitution and order
transitivity. An absolute error bound is sufficient but stronger than necessary.
Using the saved tighter assembled upper Ucert instead permits epsilon<=u-Ucert;
this review does not calculate or claim either runtime epsilon.

The four false admission/runtime flags remain false until the uniform error
premise, result finiteness and selected consumer identity are independently
verified. The scalar gate does not itself identify the consumer's V.

## A finite, exact error certificate that could discharge the premise

### A. Parsing/loaded coefficient bridge

For each CSV row, bind its raw cells, row index and intended exponent tuple to
the actual loaded coefficient bits and exponent values, or to a verified Julia
parser theorem. Decode coefficient bits as exact dyadics. A Python float decode
does not prove Julia chose the same bits. Decimal rounding boundaries/ties,
overflow and nonfinite tokens must be handled by the parser contract.

Write P_J for the unrounded Real polynomial with the actual Julia-loaded
coefficients and the proved exponent tuples. If those coefficients equal the
chosen binary64 interpretation, P_J=P_star by finite coefficient equality.
Otherwise retain the coefficient bridge. A simple rational uniform estimate is

```text
|P_J(x,0)-P_star(x,0)|
 <= sum_(rows with e_t=0) |c_J-c_star| * (3/20)^(e_q4+e_q5+e_v4+e_v5).
```

This is evaluated rowwise before combining duplicates and is conservative.
Wrong exponents are not coefficient errors: they require rejection or a new
function comparison. The current table's valid integer exponent tokens alone
do not prove the deployed parse/round/Int path.

### B. Arithmetic bridge, preserving the actual evaluation

Bind the actual power implementations and multiply/add lowering, including row
order. Do not infer a multiplication count or power algorithm from the string
x^e, or silently use the ideal checker's reordered/combined monomials. Either
verify the chosen lowering or prove bounds covering every allowed lowering.

For each operation node, use exact rational magnitude bounds |a_star|<=B_a and
absolute propagated errors |a_machine-a_star|<=E_a. With a verified local
rounding bound rho for the operation on its actual operand ranges:

```text
add: E_out <= E_a + E_b + rho
mul: E_out <= B_a*E_b + B_b*E_a + E_a*E_b + rho.
```

For powers, either expand the PINNED executed algorithm with these rules or
provide a separately checked local power-error theorem; exponent zero is an
explicit case. Any fused operation needs its own justified local rule.
Magnitude/operand-range propagation must use B+E, not ideal B alone.

For example, a verified binary64 round-to-nearest, gradual-underflow model can
use the conservative absolute local rule
`|RN(z)-z| <= 2^(-53)*|z| + 2^(-1074)` for finite nonoverflowing exact z.
This is a proposed arithmetic model, not an observed setting. A verifier must
first discharge overflow/nonfinite exclusions and pin the subnormal policy;
a normal-only relative gamma_n formula is not justified when inputs may be
zero or subnormal. FTZ/DAZ or other rounding modes need different rules.

These recurrences yield a finite rational execution upper E_exec for every
decoded x in the fixed domain. Combine the parser bridge E_parse with it once:
`epsilon=E_parse+E_exec`. Keeping signed interval errors can improve this bound,
but is not necessary for the contract. No epsilon or local rho data is invented
in this review, and no synthetic runtime trace is generated.

### C. Input interpretation and consumer scope

For the decoded-input quantifier above, input conversion error is zero by
definition. If the intended claim starts from arbitrary Real x in X0 and
rounds it to binary64, rounding can leave the closed ball. Require an expanded
domain proof or a separately proved input-conversion error bound; do not reuse
the same X0 witness at an unproved outside point. The runtime Monte Carlo
generator does not establish either universal input contract.

The defect/error certificate and consumer must reference the same coefficient
file, evaluator, parsed arrays, domain, time and scalar selector. Proving this
runtime evaluator's initial bound still does not prove that the independent
energy-barrier consumer uses it, nor close its later growth/tube obligations.

## Minimal missing evidence fields

1. actual reader/parser/dispatch environment, source/binary identities and
   coefficient-bit/exponent table correspondence;
2. call types/shapes, immutable-or-preserved arrays, first-call time-zero and
   decoded X0 membership contract;
3. power/multiply/add lowering or a verified covering model; rounding,
   overflow, subnormal and fusion policy;
4. nodewise exact rational ranges/error witnesses and the final epsilon gate;
5. actual consumer function identity and a genuine event/input binding.

Observed static fields are closed only as source-text/hash facts: filename,
column order, source variable map, loop text and first-time expression.
No parsed bit table, runtime semantics, numerical epsilon, source identity or
runtime initial bound is closed by this inspection.

## Fresh hash bindings

```text
E/routeB_export_traj.jl
35ebe806a46273068af1af937c0c0152378d6889024ec5586bf3c7aabd30eccf
E/routeB_certificate_V.csv
cab4a5182981bccbde18ace2d26ece5c0d7b7d3c3cf4a5a7e02e7fcda9b80601
E/routeB_export_manifest.toml
5b61d624f4f6060da8c33a51fa7982bef8206d2c3924babb512440defad89187
examples/routeb_active_v_function_envelope/NEW_CONVENTION_initial_witness.py
c7e7ba7386eccd5165b82d818d80389c820239586531e5f7b8d24b6b56decc0f
examples/routeb_active_v_function_envelope/NEW_CONVENTION_initial_witness.json
ff0af76ef94adeb9ded4e4a50d45cdb03ee6ac5503b94283f4893b971c581f34
```

The saved export manifest reports Julia 1.12.6 and empirical Monte Carlo
evidence. That is historical metadata, not a newly verified executed Julia
environment. No execution/source admission is inferred from the manifest.

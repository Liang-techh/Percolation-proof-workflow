---
kind: review_result
review_id: review-GH-P4-EVALV-CONSERVATIVE-BUDGET-DESIGN-20260908T191317Z
task_id: GH-MATH-P4-EVALV-CONSERVATIVE-ERROR-BUDGET-DESIGN
source_agent: Godel the 6th
created_at: 2026-09-08T19:13:17Z
immutable: true
status: pending
integration_status: pending
admission_label: pending
result: CONSERVATIVE_LOCAL_CAPS_SUFFICE_CONDITIONALLY_RUNTIME_PREMISES_ABSENT
proof_status: paper_conditional_error_budget_design
epsilon_generated: false
certified_epsilon: null
runtime_error_witness: null
source_binding_proven: false
runtime_initial_bound_proven: false
registry_eligible: false
formal_certificate_allowed: false
julia_execution: false
lean_compile_status: not_run
full_regression: false
state_mutation: false
registry_mutation: false
threshold_mutation: false
requested_action: verify parser/exponent/lifetime and concrete operation semantics against the proposed local-cap contract; do not treat the design budget as a generated runtime epsilon
---

# A conservative design fits the margin; no runtime epsilon is generated

Only source/table text and hashes were read. No initial-bound or nonidentity
audit was rerun, and no Julia, Lean, numerical simulation or full regression
was executed. Only this new review is written.

The available -1/20 ideal initial margin is large enough for the explicit
conditional design below. The remaining obstacle is a verified semantics/lifetime
packet, not absence of a plausible finite arithmetic design. No value below is
claimed as an observed or certified runtime epsilon.

## Fixed data and interpretations

The pinned certificate table has 46 rows, exponent tuples with entries in
{0,1,2,3,4} and total degree at most four. Its listed coefficients have absolute
value less than 4. Use the full 46-row sum, including positive time powers, so
there is no unjustified removal of runtime row evaluations at t0=0.

Choose one P_star already covered by the initial witness: decimal-token Real
or Python-binary64-decoded Real. The latter remains only a candidate match to
Julia parsing. The following derivation works for either interpretation with
a separate coefficient discrepancy bound. Decoded input x is in the same X0,
so |q4|,|q5|,|v4|,|v5|<=3/20<1, and decoded tv=0. Exact powers have magnitude
at most 1, including the explicitly interpreted exponent-zero case.

Input conversion is excluded by quantifying directly over decoded Float64
inputs in X0. Starting from arbitrary real inputs and then rounding requires
a separate enlarged-domain/conversion proof and cannot use this budget unchanged.

## Rowwise split: parser errors are not rounding-operation errors

For row i let c_i be the chosen exact coefficient, cJi the actual decoded
Julia-loaded coefficient, and a_ij=x_j^e_ij the five exact power factors.
Let aHat_ij be the decoded outputs of the actual power implementation.

Require the following UNVERIFIED design premises uniformly over X0:

| Layer | Required rowwise premise |
|---|---|
| CSV/header/order | exactly the intended 46 rows, paired coefficients/exponents, no extra skipped data |
| Coefficient parser | |cJi-c_i|<=delta_i; finite loaded coefficient |
| Exponent parser | loaded integer tuple equals the intended tuple EXACTLY |
| Powers | |aHat_ij-a_ij|<=eta_ij; finite power outputs |
| Multiplication | an identified five-multiplication fold over cJi and the five power factors, each with absolute local error <=rho_mul |
| Accumulator | exactly the intended row sum, starting at real-decoded zero, each of 46 additions with absolute local error <=rho_add |
| Lifetime | arrays, concrete types, bounds and values preserved from reader to call |

The five-multiplication fold is an explicit TARGET SEMANTICS premise, not an
inference about Julia's variadic multiplication dispatch or compiler lowering.
If the actual lowering differs, prove it satisfies the same bound or construct
its own local recurrence. Fused arithmetic needs a justified covering rule.

An exponent mismatch is not a small delta_i. Even 0 versus 1 changes x^e by
order one near x=0; a negative exponent at zero can destroy finiteness. Reject
such mismatch or introduce a separate function comparison. Do not charge it
as a coefficient-rounding perturbation.

## Explicit sufficient local-cap design

Introduce the DESIGN parameter kappa=2^(-20). It is a proposed cap to prove,
not an exported measurement or a generated runtime epsilon. Suppose

```text
delta_i <= kappa,  eta_ij <= kappa,
rho_mul <= kappa, rho_add <= kappa.
```

Since kappa<=1/16, put a=1+kappa. Then a^5<2 and
S5=sum_(j=0..4) a^j<10. A row's coefficient-and-power discrepancy, before
multiplication rounding, is at most

```text
delta_i*a^5 + |c_i|*(a^5-1).
```

The product-difference formula proves this without relative errors or division
by a coefficient/power; zero, tiny and signed terms are allowed. The five
local multiplication errors propagate with total charge at most rho_mul*S5.
Since a^5-1=kappa*S5 and |c_i|<4, the whole row error is bounded by

```text
delta_i*a^5 + 4*kappa*S5 + rho_mul*S5 <= 52*kappa.
```

Summing all 46 row errors and 46 local accumulation errors gives the
CONDITIONAL implication

```text
all design premises => |Decode(evalV_fast)-P_star| <= 46*53*kappa < 1/20.
```

The last strict comparison follows from 20*46*53=48760<2^20. Thus if the
premises are independently verified, the already proved P_star<=-1/20 yields
Decode(evalV_fast)<0<u. No separate parse charge is added afterward: delta_i
is already included in each row, so doing so would double count it.

This argument does not claim exact equality between the evaluator and either
polynomial interpretation. It does not assign a certified epsilon. It proves
that a concrete family of readily checkable local bounds would fit the margin.

## Why the local caps are compatible with a conservative IEEE design

This subsection is also conditional on an independently verified arithmetic
model; no actual compiler/platform property is inferred from it.

Under the design premises, any partial row product has magnitude less than
(4+kappa)*a^5+kappa*S5<9. Partial sums have magnitude less than
46*9+46*kappa<512. These are range bounds for the proposed fold, allowing a
noncircular local proof: induct over nodes, establish operand/exact-result
range, apply the local rounding theorem, and then extend the error invariant.

A verified binary64 round-to-nearest/gradual-underflow operation model can use
|RN(z)-z|<=2^(-53)|z|+2^(-1074) on finite nonoverflowing results. On |z|<=512,
this is strictly below kappa. The additive underflow allowance is essential:
the domain includes zero and arbitrarily small binary64 inputs, so a pure
normal-only relative-error formula is insufficient.

For powers with exponents 0..4, a verified implementation using at most three
multiplications for positive powers can support the power cap by a tiny
separate induction; exponent zero needs its exact-one rule. But the source
x^e alone DOES NOT identify that executed implementation. A proof of Julia's
actual selected method, or another verified bound for it, is still required.
Likewise, coefficient parse rounding needs an independent correct-rounding or
error-bound theorem; Python decoding cannot substitute for that theorem.

No overflow is predicted by this design, but finiteness must be proved for
the actual operations. FTZ/DAZ, alternate rounding, reassociation, exceptional
power behavior or a different call type require their own justified rules.

## Minimal missing fields and failure boundary

To turn this design into an epsilon witness, supply:

1. pinned reader/parser semantics or actual coefficient bits plus exact exponent
   tuples, bound to CSV row bytes, header handling and order;
2. concrete Float64 input/array types, valid dimensions, decoded X0/time-zero
   premises and no intervening mutation of the mutable global arrays;
3. a verified power and product/sum operation graph, or a semantics theorem
   covering the actual lowering, with rounding/subnormal/fusion policy;
4. finite rational local-error/range witnesses satisfying the stated caps;
5. exact consumer function identity and actual input/event association.

Without those semantics/lifetime premises, source hashes alone imply no useful
finite real-valued error theorem. For example, the source arrays are mutable:
an unexcluded later write of NaN to a coefficient makes a finite decoded-output
inequality unavailable despite unchanged CSV/source hashes. An unexcluded
order-one perturbation of the constant coefficient can already exceed the
initial slack. These are countermodels to an INSUFFICIENT contract, not claims
that the actual run mutated its arrays or returned NaN.

The static source has no explicit @fastmath/fma call, but that is not a proof
of any operation graph. Historical Julia version metadata does not fill the
method/compiler/rounding fields. None of the required runtime bounds or bits
was supplied in this task, so certified_epsilon remains null and status pending.

## Hash bindings

External root:
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`.

```text
routeB_certificate_V.csv
cab4a5182981bccbde18ace2d26ece5c0d7b7d3c3cf4a5a7e02e7fcda9b80601
routeB_export_traj.jl
35ebe806a46273068af1af937c0c0152378d6889024ec5586bf3c7aabd30eccf
examples/routeb_active_v_function_envelope/NEW_CONVENTION_initial_witness.json
ff0af76ef94adeb9ded4e4a50d45cdb03ee6ac5503b94283f4893b971c581f34
```

The last path is under the workflow workspace and identifies the existing ideal
initial witness consumed by reference, not a new runtime result. No old artifact,
state, registry, threshold or shared script was modified. No admission promotion.

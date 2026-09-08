---
kind: review_result
review_id: review-GH-MATH-P4-ACTIVE-ENERGY-NORMALIZATION-20260908T165726Z
task_id: GH-MATH-P4-ACTIVE-ENERGY-NORMALIZATION
source_agent: codex-active-energy-normalization
created_at: 2026-09-08T16:57:26Z
integration_status: pending
admission_label: pending
status: EXACT_EXPRESSION_DIFFERENCES_IDENTIFIED_INITIAL_BINDING_OPEN
proof_status: paper_source_expression_algebra_only
source_binding_proven: false
initial_bound_binding_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
julia_execution: false
full_regression: false
generated_numeric_values: false
state_mutation: false
registry_mutation: false
requested_action: retain nonconstant gain, compensation and cross-term differences in any initial-storage transfer
---

# Active-energy normalization: exact expression alignment and missing value bound

Only this new review is written. No old artifact or other agent file is
modified. No new numerical constant/upper bound, source export or execution
evidence is generated. No local Lean/Lake, producer, solver or regression runs.
The identities below are exact paper algebra on inspected source expressions,
not a compiled theorem or actual source admission.

External source directory E:
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`.

## 1. Same-expression matching that can be made explicitly

The current Ugrav_DH assignment in dh_gain_descriptor_regeneration and Ugrav
assignment in energy_power_rewrite have identical coefficient declarations
and identical c/s monomials. Therefore, when instantiated on the same c/s
variables, they are the SAME value polynomial, not merely potentials sharing
a derivative. No gravity offset is needed BETWEEN THESE TWO audit expressions.
This does not identify either raw potential with dhport's midpoint-height
potential; that external source bridge remains separate.

Both routes import the Fourier mass M with its declared diagonal regularizer
added once. Kfull and Kfull_DH both use the identical expression
K=(1/2)*v^T M(q) v. Current code therefore identifies their value-level kinetic
expressions under one common import/configuration. A historical run with
different loaded source/parameters would still require provenance binding.

Use U for the matched audit potential, g for the common analytic origin
gravity, and Qp for the diagonal original Kp. The full-energy source explicitly
defines

```text
W = Vfull_DH = K+U+(1/2)*q^T Qp q+g^T q.
Z = Vshift_DH = W+b,
b = GRAVITY_SHIFT_DH+controller_linear_shift.
```

b remains the EXISTING symbolic source expression and is not numerically
evaluated. Neither W nor Z subtracts U(0).

## 2. Origin normalization removes a constant, not a linear/cross term

On the physical lift c_j=cos(q_j), s_j=sin(q_j),

```text
W(0,0)=U(0),
Z(0,0)=U(0)+b,
Z(q,v)-Z(0,0)=W(q,v)-W(0,0)
             =K+[U(q)-U(0)]+(1/2)*q^T Qp q+g^T q.
```

These are value identities. The kinetic and controller origin terms vanish
without assuming g=0. But g^T q survives normalization away from the origin.
An actual g=0 witness for the same analytic source is needed to remove it;
an origin VALUE equality does not provide that witness. A reported analytic
g0_exact_zero flag is not runtime FD-origin compensation refinement.

The linear sign is explicit: W uses +g^T q; the targeted source controller
potential uses -g^T q. Do not reconcile those by silently replacing g or its
sign. If an independently proved common-source g=0 is supplied, the sign
difference vanishes for that configuration only.

## 3. Exact difference with the initial-envelope storage expression

The targeted strictification source's report line explicitly states the
expression `V_eps=K+U_g+U_ctrl_target+eps*q'*M(q)*v`. Its actual source
definitions set U_ctrl_target=(1/2)*q^T(Qp+DeltaQ)q-g^T q, with DeltaQ supported
only at joints2/3, and Wmass=q^T Mv. Denote that stated value expression by T.
This notation does NOT assert that the scalar initial producer is bound to T.

Under the same M,U,g,state and parameter interpretation, direct subtraction gives

```text
T-W = (1/2)*q^T DeltaQ q - 2*g^T q + eps*q^T M(q)*v,
T-Z = (1/2)*q^T DeltaQ q - 2*g^T q + eps*q^T M(q)*v - b.
```

Each term follows from a value-level definition. No Hessian or derivative
flag is used. These identities precisely locate what a transfer must retain.
They close an expression-comparison subproblem only, not the actual initial
bound leaf, source-to-DH equality, or a verified storage theorem.

At the origin T and W have the same value, but their difference away from
the origin need not be constant. On the existing block-only X0, DeltaQ's
contribution vanishes because q2=q3=0. With B=(4,5), the remaining difference is

```text
(T-W)|X0 = -2*g_B^T q_B + eps*q_B^T M_BB(q)*v_B.
```

Even if g_B=0 is proved, the mass cross term remains. X0 permits both velocity
signs, so an unproved sign assumption cannot justify W<=T or T<=W uniformly.
No new counterexample, value or bound is generated. A signed identity may
support a later comparison proof, but that proof is not supplied by the
quadratic-only CSV scalar.

## 4. Regularizer bookkeeping

Changing only M from M_base+mu I to M_base+mu' I changes W by
`(mu'-mu)*||v||^2/2`. For the same cross-term family T, the change is

```text
(mu'-mu)*||v||^2/2 + eps*(mu'-mu)*q^T v.
```

These are state-dependent differences; both vanish at the origin, so origin
agreement does not authenticate regularizer matching. Normalization cannot
remove them. The source currently adds its declared regularizer once; an
initial mass bound must reference that same M, including its contribution to
both kinetic and cross terms. No alternative regularizer or numerical change
is proposed here.

## 5. Active initial scalar remains unbound

The consumer still reads initial_storage_upper into V0 and sets V_BAR=1.
The initial producer's mass/Hessian/cross-term envelope is an arithmetic
construction, not a proved function-indexed bound for raw W, shifted Z or
even the fully anchored T. A Hessian upper bound controls an anchored Taylor
remainder, not U(q) with its origin constant silently omitted.

Minimum sufficient next evidence is either:

- a direct same-source statement `forall x in X0, W(x)<=u` (or Z, if that
  is the explicitly bound target), including its raw value anchor; or
- a genuine initial bound on the selected source storage T and a proved
  X0 comparison to W/Z using the complete differences above, with its
  corresponding upper/threshold budget.

For a constant shift, initial upper and barrier threshold must move together
or an explicit tighter budget must be proved. For the nonconstant difference,
a domain-local comparison is required. Matching origin values, shared
derivatives, matching numeric CSV fields or a quadratic/Hessian envelope
cannot replace these functional statements.

No actual initial-storage binding is established. Status remains pending,
with no registry promotion or VERIFIED claim.

## Fresh SHA256 (filenames relative to E)

| Source | SHA256 |
|---|---|
| routeB_compact_dh_full_energy_supply_split_audit.jl | d6d9bd3131d73fddf946f8652458b04c628f76471d497b2a52a49f0335b30632 |
| routeB_compact_dh_storage_shift_audit.jl | aa3957f714f86c631a55fb8e7cc190fc98918a9cc04d148adcd7a28141cb9fec |
| routeB_compact_targeted_nonlinear_strictification_audit.jl | 41dd63be6fab08b3398913490cb90d5f3571cce2e3ea833c52e9d1b97674f5b1 |
| routeB_compact_energy_power_rewrite_audit.jl | 7a75dbb4cc4297e6d66e1a0d50077d24ce129c5b6e71406e68694c61cd8ae6bf |
| routeB_compact_dh_gain_descriptor_regeneration_audit.jl | 04b764434601dd0c11b2a6554156fd4d948cf742dbf33472b960e0d54e8235c9 |

Current source snippets were read and hashes computed. No prior execution or
formal receipt is authenticated by this textual/paper audit.

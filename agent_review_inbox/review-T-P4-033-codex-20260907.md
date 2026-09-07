---
kind: review_result
task_id: T-P4-033
source_agent: Codex
created_at: 2026-09-07
integration_status: pending
review_status: OPEN_MATH_CLOSURE_PREMISES
---

# O0 regularizer semantics: minimal Schur/resolvent closure

## Bottom line

The scalar fact is already closed: with

```text
mu_f = 4722366482869645 / 4722366482869645213696
mu_r = 1 / 1000000
delta = mu_r - mu_f
      = 3339 / 73786976294838206464000000 > 0,
```

we have `mu_f < mu_r`. This fact alone does not close O0 for an inverse or a
Schur/port consumer. The current registry node
`P4.true_dh_regularizer_semantics_bridge` is correctly still open: its
missing mathematical content is not another scalar rounding lemma, but a
common-base/block binding and a metric-compatible resolvent-to-port transfer.

## Minimal child-lemma decomposition

### O0.1 — literal order (already a fact)

Record the exact dyadic `mu_f`, exact `mu_r`, `delta > 0`, and the direction
`M_f = M_r - delta I` only after the common-base premise below is supplied.
The decimal text `1e-6` must not be promoted to the exact rational
`1/1000000` on the deployed side.

### O0.2 — common base or quantitative base error

For every covered state/angle `q`, choose one of these two premises:

```text
(A) M_f^0(q) = M_r^0(q),
```

or, in a genuinely rounded evaluator bridge,

```text
(B) ||M_f^0(q) - M_r^0(q)|| <= epsilon_0(q).
```

Under (A), for `A_s = M_DD,s` and the declared `B=(4,5)`,
`D=(1,2,3,6)`,

```text
A_f = A_r - delta I_D,
B_f = B_r,
C_f = C_r,
```

where `B_s=M_BD,s` and `C_s=DeltaM_DB,s`. The diagonal shift gives no
off-diagonal `BD`/`DB` shift. Under (B), the correct D-block perturbation is
not just `delta`: define

```text
epsilon_A >= ||A_f - A_r||,
```

which must account for both base-evaluator error and the regularizer delta.
The current helper proves only the special common-base case; it does not
prove (A) for deployed Float64 DH/frame/mass evaluation.

### O0.3 — D-block resolvent lemma

The minimum inverse premise is:

```text
A_r is invertible,
||A_r^(-1)|| <= K,
epsilon_A * K < 1.
```

Then the Neumann/resolvent conclusion is

```text
||A_f^(-1)|| <= K / (1 - epsilon_A*K),
||A_f^(-1) - A_r^(-1)||
    <= epsilon_A*K^2 / (1 - epsilon_A*K).
```

For common base, `epsilon_A=delta`. Equivalently, a source-side child may
provide `A_r ⪰ alpha I_D` with `alpha>0` and use `K=1/alpha` in the spectral
norm, provided symmetry and the exact domain binding are included. A positive
regularizer by itself is not an inverse witness unless a lower bound on the
unregularized D block is also known.

### O0.4 — port perturbation lemma

With `R_s = -B_s A_s^(-1) C_s`, the general three-term estimate is

```text
||R_f-R_r|| <=
    ||B_f-B_r|| * ||A_f^(-1)|| * ||C_f||
  + ||B_r|| * ||A_f^(-1)-A_r^(-1)|| * ||C_f||
  + ||B_r|| * ||A_r^(-1)|| * ||C_f-C_r||.
```

In the common-base case the first and third terms vanish, yielding the
current helper's conditional expression

```text
||R_f-R_r|| <= ||M_BD|| * ||DeltaM_DB||
                * delta*K^2/(1-delta*K).
```

This is only an unweighted operator-norm difference. To consume the existing
port ledger, which is expressed as
`||R a_B||_2^2 <= rho^2 (a_B^T B_up a_B)`, one further needs either

```text
||(R_f-R_r) B_up^(-1/2)|| <= epsilon_R,
```

directly, or an exact metric conversion such as
`B_up ⪰ beta I` with `epsilon_R <= ||R_f-R_r||/sqrt(beta)`. The current
O0 helper does not provide this weighted conversion.

### O0.5 — Schur-budget consumer

An inverse perturbation is not itself a Schur bound. The consumer must provide
a baseline weighted port gain `rho_r` for the same source/state key and a
weighted perturbation `epsilon_R`, so that

```text
rho_f <= rho_r + epsilon_R.
```

If the recorded Young parameter is `theta`, the additional mathematical
closure condition is the exact budget inequality

```text
(1 + 1/theta) * ((rho_r + epsilon_R)^2 - rho_r^2)
    <= remaining_schur_margin.
```

Equivalently, one may supply a single conservative `rho_f` and prove the
existing combined-Schur premise with `rho_f^2`. The current Frobenius ledger
records baseline `rho^2`, charge, and margin, but the O0 artifact does not yet
identify that baseline as `R_r` or `R_f`, nor does it reserve a delta-induced
weighted margin. Therefore the ledger cannot yet consume O0's resolvent
difference as a closed true-DH port bound.

## Concrete counterexamples

1. **Regularizer positivity does not imply a resolvent.** In one dimension,
   take a common base `M^0=-mu_f`. Then `A_f=0` although `mu_f>0`; no
   `A_f^(-1)` or port map exists. Thus O0 needs D-block coercivity/invertibility
   (or the explicit `K` premise), not merely the positive literal.

2. **Scalar delta without common-base binding is unusable.** Let
   `A_r=1` and choose an unrelated deployed base so that `A_f=0`. The same
   `mu_r-mu_f=delta` still holds, but the inverse perturbation is singular.
   A common base equality or a quantitative `epsilon_A` is logically necessary.

3. **A small inverse difference does not create a port bound.** With
   `A_f=A_r=1`, `B_f=B_r=N`, `C_f=C_r=1`, the regularizer difference is zero
   while `R=-N` is arbitrarily large. A baseline `R_r`/coupling bound is a
   separate premise.

4. **Unweighted and energy-weighted gains are not interchangeable.** In one
   dimension, take `B_up=epsilon`, `R_f-R_r=1`. The unweighted difference is
   one, but the weighted gain is `1/sqrt(epsilon)`, unbounded as epsilon tends
   to zero. A positive metric lower bound or a direct weighted operator bound
   is required.

## What the current registry/parent still lacks

For O0 itself, the open mathematical premises are:

- authoritative evaluator choice: exact-real authority with a full rebind, or
  deployed Float64 authority with a common-base/operation-level enclosure;
- common `M^0(q)` binding, or an explicit `epsilon_A`, `epsilon_B`, and
  `epsilon_C` over the covered domain;
- exact D-block invertibility/coercivity and a norm-compatible `K`;
- same-key `M_BD` and `DeltaM_DB` bounds, plus conversion to the `B_up`
  weighted port metric;
- a baseline `rho_r` and a strict Young/Schur margin that survives the added
  `epsilon_R` charge.

The parent `P4.true_dh_residual_map_coefficient_binding` additionally still
needs the separate O1 identity `R_port*a_B=r_B`, the force-scale decision, and
the exact same `mu`/FD/source semantics on both sides. Its registry closure
requires O0/O1/O2 children plus a typed parent receipt; O0 cannot discharge
the O1 source equality or O2 box coverage. The current state also records the
controller-damping-vector mismatch and the unsupported `q5/100`, `q4/200`
force-scale terms; these are parent source premises/obstructions, not facts
that can be repaired by changing `delta`.

## Recommended executable next child

The smallest useful mathematical child is:

```text
O0-R1: For every covered q, prove
       A_f=A_r-delta I_D, B_f=B_r, C_f=C_r,
       A_r invertible, ||A_r^(-1)||<=K, delta*K<1.
       Return K_f and DeltaR in the same norm as the port ledger.

O0-R2: Bind the returned DeltaR to B_up and prove
       ||(R_f-R_r) B_up^(-1/2)|| <= epsilon_R.

O0-R3: Consume the existing baseline rho_r and prove the exact
       Young/Schur margin inequality for rho_f=rho_r+epsilon_R.
```

If O0-R1 cannot establish a common base, the correct result is an obstruction
with `epsilon_A` (and the three-term port estimate), not a claim that the
scalar delta alone closes the port bound. If exact-real evaluation is selected
as authoritative instead, O0-R2/R3 may be run entirely on the exact side, but
the deployed Float64 parent must then be explicitly re-scoped rather than
silently identified with it.

## Evidence boundary

Read-only inputs were the O0 report/receipt, the coordinator regularizer
helper and documentation, and the current `state.json` nodes for O0, the
port Frobenius ledger, the combined Schur adapter, and the true-DH parent.
No Lean/Lake, Julia, solver, broad regression, registry mutation, or state
write was performed. This result is a mathematical child decomposition and
obstruction analysis, not a compiled or admitted certificate.

Input hashes at review time:

- O0 report: `A47DF33CE52AF11DE2C4E9C3C81F40F77BAA436F894AC2D0DDA1A058B49F8A18F`.
- O0 receipt: `68CB17A5FE83FB2C01777355D2F08C78AC4D0AC64198A4F6FD21A8670220574E`.
- Helper: `2C218C9958B5AC1252112F14A1FDFF9492756F216E0E0F4BCFF92BE3168DEE9B`.
- O0 documentation: `BE9DC310E44E4A6BAB4F96C14938A8C5FD5ADAED0A433B888219124BAA5078D2`.
- State snapshot: `86E17CAD6FA5DD42C2201D2DE9422AA51BDCC4E2DFCC9D4F288719586149A933`.

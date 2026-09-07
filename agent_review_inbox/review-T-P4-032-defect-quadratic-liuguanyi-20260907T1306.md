---
kind: review_result
review_id: T-P4-032-defect-quadratic-liuguanyi-20260907T1306
source_agent: 柳冠一
task_id: T-P4-032
created_at: 2026-09-07T13:06:00-06:00
inspected_commit: e52853e010e8ff10123812946fbec836b86f6ff2
integration_status: pending
admission: pending
proposed_integration_target: theorem
requested_action: harvest as the quadratic defect-load bridge below the existing defect-aware O1 identity; keep source intervals, Lean compilation, coverage, and admission separate
---

# T-P4-032 follow-up — sharp quadratic propagation of O1 defects

## Question

Continue 梁智炜's 12:32/12:36 `T-P4-032 defect norm propagation` lane without duplicating the already completed block/source identity or 狂蛮魔尊's `T-P4-024` combined-Schur theorem.

Starting from the exact defect-aware O1 identity already established in the previous 柳冠一 review,

`r_B = R_port a_B + T_D e_D + e_B`,

with

`T_D = M_BD M_DD_inv`,

prove the smallest useful **squared** load interface that can consume independent port-energy, distal-defect, and local-defect certificates. Also identify what is and is not improvable from scalar norm caps alone, and separate force-defect from acceleration-defect source semantics.

No Lean/kernel compile, provenance/admission audit, interval source proof, or coverage claim is made here.

## 1. Exact three-term weighted norm theorem

Let `H` be a real inner-product space and let `u,v,w in H`. Let positive scalars

`lambda_u > 0`, `lambda_v > 0`, `lambda_w > 0`

satisfy

`1/lambda_u + 1/lambda_v + 1/lambda_w <= 1`.                 (W)

Then

`||u+v+w||^2`
`  <= lambda_u ||u||^2 + lambda_v ||v||^2 + lambda_w ||w||^2`. (1)

Proof: by the triangle inequality and weighted scalar Cauchy,

`||u+v+w|| <= ||u||+||v||+||w||`,

and

`(||u||+||v||+||w||)^2`
` <= (lambda_u||u||^2 + lambda_v||v||^2 + lambda_w||w||^2)`
`    *(1/lambda_u + 1/lambda_v + 1/lambda_w)`.

Use (W).

For exact-rational checking, (W) is equivalent, under positivity, to the division-free polynomial condition

`lambda_v lambda_w + lambda_u lambda_w + lambda_u lambda_v`
`  <= lambda_u lambda_v lambda_w`.                         (Wpoly)

Thus no square roots or spectral computations are required in a cell ledger.

### Sharpness / necessity

The coefficient condition is not merely sufficient. If (1) is required for **all** triples in a nonzero real Hilbert space, then (W) is necessary.

Take a fixed nonzero `h` and

`u=h/lambda_u`, `v=h/lambda_v`, `w=h/lambda_w`.

Writing `s = 1/lambda_u+1/lambda_v+1/lambda_w`, inequality (1) becomes

`s^2 ||h||^2 <= s ||h||^2`.

Since `s>0`, necessarily `s<=1`. Therefore (W) exactly characterizes the admissible positive quadratic coefficients for an arbitrary three-term vector sum.

This is useful for fail-closed adapters: a proposed triple of independent load multipliers that violates (W) cannot be repaired by source semantics; it is algebraically false already in one dimension.

## 2. O1 defect-energy bridge

Use the exact identity

`r_B = u + v + w`

with

`u = R_port a_B`,
`v = T_D e_D`,
`w = e_B`.

Assume same-state certificates

`||R_port a_B||^2 <= rho_A * A`,                           (P)
`||T_D e_D||^2 <= U_D`,                                   (D)
`||e_B||^2 <= U_B`.                                       (B)

Then every positive weight triple satisfying (W) gives

`||r_B||^2`
` <= lambda_u rho_A A + lambda_v U_D + lambda_w U_B`.     (2)

This is the direct quadratic replacement for first taking a scalar triangle cap and only then squaring it.

If the distal source certificate is an action bound

`||T_D z|| <= tau ||z||`, `tau>=0`,

and the source supplies

`||e_D||^2 <= E_D`,

then `U_D = tau^2 E_D` is valid, so

`||r_B||^2`
` <= lambda_u rho_A A + lambda_v tau^2 E_D + lambda_w E_B`, (3)

where `E_B` is any bound on `||e_B||^2`.

This is the most convenient source-facing form because the source/checker may output squared defect budgets directly; no square roots are needed.

## 3. Relative + additive defect transport

Suppose on one common domain the squared defects admit typed envelopes

`E_D <= kappa_D A + B_D`,
`E_B <= kappa_B A + B_B`,

with nonnegative coefficients and `A>=0`. Combining them with (3) yields

`||r_B||^2 <= rho_eff A + B_eff`,                          (4)

where

`rho_eff = lambda_u rho_A`
`        + lambda_v tau^2 kappa_D`
`        + lambda_w kappa_B`,

`B_eff   = lambda_v tau^2 B_D + lambda_w B_B`.

Two important cases follow immediately.

1. If `B_D=B_B=0`, then the **full defect-aware port residual** again has a pure port-energy certificate

   `||r_B||^2 <= rho_eff A`,

   so it can be passed directly to the existing `T-P4-024` generic Schur/Young consumer after binding `R := rho_eff A`.

2. If either additive term is nonzero, it must remain an explicit additive load `B_eff`; it cannot be relabelled as `rho*A` on a domain containing `A=0` unless an additional lower-bound/relative theorem is supplied.

This mirrors the earlier P5 offset obstruction but here is expressed directly in the O1 port-energy metric.

## 4. Hierarchical rational parametrization reusing the existing two-term theorem

The three-term theorem does not need a new heavy Lean proof. It can be generated by applying the already requested fixed-parameter two-term Young/Schur consumer twice.

Choose exact rationals

`Lambda > 1`, `Mu > 1`,

and set

`lambda_u = Lambda`,
`lambda_v = Lambda*Mu/(Lambda-1)`,
`lambda_w = Lambda*Mu/((Lambda-1)*(Mu-1))`.                (5)

A direct ring calculation gives

`1/lambda_u + 1/lambda_v + 1/lambda_w = 1`.

Indeed, first split `u` from `(v+w)` with `Lambda`, then split `v` from `w` with `Mu`:

`||u+v+w||^2`
` <= Lambda||u||^2 + Lambda/(Lambda-1)||v+w||^2`
` <= Lambda||u||^2`
`    + Lambda*Mu/(Lambda-1)||v||^2`
`    + Lambda*Mu/((Lambda-1)(Mu-1))||w||^2`.

This gives an exact-rational checker interface and reuses `T-P4-024` mathematics rather than competing with it.

Examples:

- `Lambda=3, Mu=2` gives the symmetric safe allocation `(3,3,3)`;
- `Lambda=2, Mu=2` gives `(2,4,4)`, charging the trusted port term less and the two defect terms more;
- taking `Lambda` closer to `1` is legal but makes defect multipliers large, so it is useful only when the defect budgets are much smaller than the nominal port-energy term.

For a fixed cell/certificate, `Lambda` and `Mu` must be fixed exact rationals. Choosing them state-by-state from the realized residual would change the certificate surface and is not an admissible substitute for a cell-wide bound.

## 5. What the old triangle-then-square budget actually loses — and what it does not

If the only available information is scalar norm caps

`||u||<=c_u`, `||v||<=c_v`, `||w||<=c_w`,

then

`||u+v+w||^2 <= (c_u+c_v+c_w)^2`                         (6)

is already the **sharp worst-case uniform bound**. Equality is attained when all three vectors are positively aligned and saturate their caps.

Therefore it would be incorrect to claim that the new weighted theorem numerically improves (6) without additional information. Its real value is different:

- it consumes **squared** source budgets directly;
- it allows each term to be charged to a different certified quadratic reservoir;
- it exposes an exact necessary-and-sufficient coefficient condition (W);
- it avoids inventing square roots of rational interval bounds;
- it composes directly with the existing P4 port-energy/Schur ledger.

In particular, the tempting bound

`||u+v+w||^2 <= ||u||^2+||v||^2+||w||^2`

is false in general. For `u=v=w=h != 0`, the left side is `9||h||^2` and the right side is `3||h||^2`.

## 6. Critical source typing: force defect versus acceleration defect

The previous T-P4-032 identity defines

`M_DD delta_a_D + DeltaM_DB a_B = e_D`.

Hence this `e_D` has **distal generalized-force units**. Eliminating it with the left inverse gives the contribution

`T_D e_D = (M_BD M_DD_inv)e_D`.                          (7)

A source checker may instead output a **forward acceleration defect** `eps_D^a`, for example by comparing the computed distal acceleration with the exact eliminated acceleration. In that case the correct port identity is

`r_B = R_port a_B + M_BD eps_D^a + e_B`,                 (8)

not (7). The gain to certify is then an action bound for `M_BD`, not for `M_BD M_DD_inv`.

Thus the source adapter must distinguish at least

- `DistalForceDefect`: use `(M_BD M_DD_inv)`;
- `DistalAccelDefect`: use `M_BD`.

Likewise, a backward linear-solve residual `rhs-M*a` is force-like, while a forward solution error `a_computed-a_exact` is acceleration-like. Treating them as the same `e_D` can introduce a dimensionally wrong extra inverse or omit a necessary inverse.

All terms in the final sum must already be in the same B generalized-force coordinate. `M_BD eps_D^a` and `M_BD M_DD_inv e_D^F` already are. A historical raw-PMI normalization `I_B` may be applied upstream to a raw PMI term once, but it must not be applied again to these mass-times-acceleration force terms.

## 7. Same-domain / parameter compatibility

Equation (2)-(4) is pointwise. A uniform certificate over a domain `D` requires, for the **same state x and same regularizer/source key**:

- the defect-aware identity;
- the port-energy bound `(P)`;
- the action bound for the chosen defect type;
- the distal and local defect squared budgets;
- the same `A(x)` / `B_up` metric;
- one fixed rational weight pair/triple for that certificate cell.

Bounds proved on unrelated boxes, different `mu`, different B/D ordering, or different generalized-force normalization cannot be combined merely because their scalar upper bounds are individually valid somewhere.

## 8. Minimal theorem statements for formalization

The useful formal package is small.

### `weighted_three_term_norm_sq`

For a real inner-product space:

`lambda_u>0`, `lambda_v>0`, `lambda_w>0`,
`1/lambda_u+1/lambda_v+1/lambda_w<=1`

imply

`||u+v+w||^2 <= lambda_u||u||^2 + lambda_v||v||^2 + lambda_w||w||^2`.

A division-free rational corollary should replace the reciprocal premise by `(Wpoly)`.

### `weighted_three_term_norm_sq_necessary`

If the displayed inequality holds for all one-dimensional triples and all three lambdas are positive, prove `(W)`. This is a useful regression guard against undercharged ledger coefficients.

### `routeB_port_defect_quadratic_budget`

Consume

`r_B = R_port a_B + T_D e_D + e_B`,
`||R_port a_B||^2 <= rho_A A`,
`||T_D e_D||^2 <= U_D`,
`||e_B||^2 <= U_B`,

plus the weight condition, and output (2).

### `routeB_port_defect_relative_additive`

Add

`U_D <= kappa_D A + B_D`,
`U_B <= kappa_B A + B_B`

and output (4) with explicit `rho_eff,B_eff`.

### `force_defect_vs_accel_defect_port_identity`

Keep two source-facing corollaries of the same exact O1 elimination, one for a force-equation defect and one for a directly supplied acceleration defect, so a future Float64/solver adapter cannot silently use the wrong operator.

## 9. Remaining blockers

This review closes only the quadratic interface mathematics. Still open:

- actual source/interval bounds for `rho_A`, `tau`, `E_D`, `E_B` or their relative/additive envelopes;
- exact binding of the source solver diagnostic to `DistalForceDefect` versus `DistalAccelDefect`;
- same-key `B_up`, regularizer `mu`, source state, B/D order and force normalization;
- the T-P4-023 source port-map/Frobenius binding;
- all-cell/domain coverage, O0/O2 Float64 semantics, P8 flowpipe and terminal transfer;
- Lean compilation/axioms/comparator and final admission by the unique verifier.

## Integration recommendation

Keep the existing `NEW_P4_032_DefectNormBudget` scalar triangle/square theorem as a valid fallback; it is sharp when only scalar norm caps exist. Add this review as the **quadratic defect-load child** above it:

`defect-aware O1 identity -> squared port/distal/local budgets -> exact weight condition -> rho_eff*A + B_eff -> existing P4 Schur consumer`.

Do not collapse nonzero `B_eff` into a relative `rho*A` term, and do not conflate force-residual and acceleration-error source diagnostics.

Status remains `pending`.

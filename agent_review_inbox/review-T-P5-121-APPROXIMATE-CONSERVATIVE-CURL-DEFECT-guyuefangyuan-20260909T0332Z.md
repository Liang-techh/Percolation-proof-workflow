---
kind: review_result
review_id: review-T-P5-121-approximate-conservative-curl-defect-guyuefangyuan-20260909T0332Z
task_id: T-P5-121-APPROXIMATE-CONSERVATIVE-CURL-DEFECT
reviewer: 古月方源
source_agent: 古月方源
created_at: 2026-09-09T03:32:00Z
claim_commit: 92674e6daba7aeacabd6144e07e19b19b2c678dd
inspected_commit: a92444465f15bd2718b634c3a258a3b3158f6824
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-119-conservative-bias-power-storage-shaping-honglianmozun-20260909T0257Z.md
    commit: 31f9508aefcd7e485cd3b6df03d20b39e4e03826
    note: commit field corrected below in prose; authoritative T-P5-119 review commit is 31f9508aabf6d9f7d4c0e97eabf34cfe6d6b1f8 if coordinator metadata supplies it
  - path: agent_review_inbox/review-T-P5-120-MOVING-CHART-CONSERVATIVE-POWER-PULLBACK-liuguanyi-20260909T0302Z.md
    commit: 282c801638022fcb40220e1f92f44f3ec0a3993d
  - path: agent_review_inbox/review-T-P5-118-CENTER-BIAS-MIXED-SMALL-GAIN-guyuefangyuan-20260909T0224Z.md
    commit: d74f645aefcd7e485cd3b6df03d20b39e4e03826
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_radial_curl_defect_and_scalar_small_gain_then_bind_same_cell_skew_jacobian_packet
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; finite-dimensional calculus, quadratic Jensen, matrix skew-pullback algebra, and scalar small-gain derivation only
exit_code: n/a
---

# T-P5-121 — approximate conservativity from a same-cell skew-Jacobian bound

## 0. Bottleneck selected

T-P5-119 proves the exact branch:

`Dr = Dr^T` on a star-shaped configuration cell

implies a constructive radial potential with `grad Psi = r`, so the whole configuration-force power can be moved into storage. It also correctly warns that small curl samples or approximate symmetry are not enough to *claim exact* conservativity.

T-P5-120 then proves that an exact conservative force is a work covector under a moving chart and that the chart frame-power term must be retained.

The smallest remaining mathematical question is therefore quantitative rather than exact:

> If `Dr-Dr^T` is not zero but is uniformly controlled on the same star-shaped cell, how large is the genuinely nonconservative remainder after the best constructive radial storage shaping?

This child gives an exact decomposition, a sharp `1/4` quadratic defect factor, a root-free mixed small-gain gate, and the coordinate pullback law for the skew derivative. It does not assert that the deployed P5 residual has the required same-cell derivative bound.

---

## 1. Setup: physical configuration force on a star-shaped cell

Work in a finite-dimensional real Euclidean configuration space. Let `Omega` be star-shaped with respect to a fixed anchor `q0`, and let

`r : Omega -> R^n`

be `C^1`.

For a target point `q in Omega`, write

`x = q-q0`,
`z_s = q0+s x`, `0<=s<=1`,
`A_s = Dr(z_s)`.

Every `z_s` is required to remain in the same certified physical cell. Define the radial potential exactly as in the exact T-P5-119 branch:

**(1.1)**

`Psi(q) := integral_0^1 <r(z_s),x> ds`.

No symmetry assumption is made yet.

---

## 2. Exact radial decomposition with a curl/skew defect

Differentiate (1.1) in an arbitrary direction `h`:

`D Psi(q)[h]`
` = integral_0^1 <h, r(z_s) + s A_s^T x> ds`.

On the other hand,

`d/ds [s r(z_s)] = r(z_s) + s A_s x`.

Integrating the latter identity from `0` to `1` gives

`r(q) = integral_0^1 [r(z_s)+s A_s x] ds`.

Subtracting yields

**(2.1)**

`grad Psi(q)`
` = r(q) + integral_0^1 s (A_s^T-A_s)x ds`.

Hence the exact nonconservative remainder is

**(2.2) RADIAL CURL-DEFECT IDENTITY**

`n(q) := r(q)-grad Psi(q)`
`      = integral_0^1 s (A_s-A_s^T)x ds`.

This is the quantitative version of the T-P5-119 fingerprint.

If every `A_s` is symmetric, `n=0` and the exact conservative theorem is recovered.

For an affine field `r(x)=b+A x`, (2.2) gives

`n(x) = (1/2)(A-A^T)x`,

which is exactly the antisymmetric configuration-force remainder identified in T-P5-119.

The object being controlled is the exterior-derivative/skew-Jacobian part of the work one-form, not the full Jacobian norm.

---

## 3. Sharp quadratic bound: the kernel costs exactly one quarter

Let `Q_F` be any positive-semidefinite quadratic form used to measure force/covector defect, and define

`c_s := (A_s-A_s^T)x`.

Then

`n = integral_0^1 s c_s ds`.

Since `2s ds` is a probability weight on `[0,1]`, quadratic Jensen gives

`Q_F(n)`
` = (1/4) Q_F(integral_0^1 2s c_s ds)`
` <= (1/4) integral_0^1 2s Q_F(c_s) ds`
` = (1/2) integral_0^1 s Q_F(c_s) ds`.

Therefore a path-integrated source cap

**(3.1)**

`2 integral_0^1 s Q_F(c_s) ds <= H_curl`

implies the division-free gate

**(3.2)**

`4 Q_F(n) <= H_curl`.

A simpler same-cell uniform operator-action cap

**(3.3)**

`Q_F((Dr(z)-Dr(z)^T) delta) <= K_curl Q_X(delta)`

for every relevant `z` and displacement direction `delta`, applied with `delta=x`, gives

**(3.4) UNIFORM CURL-DEFECT BOUND**

`4 Q_F(n(q)) <= K_curl Q_X(x)`.

No square root, inverse, eigenvalue, or optimizer is required by the final checker.

### Sharpness of the factor `1/4`

The factor cannot be improved using only a uniform bound on `Q_F(c_s)`.

Take a constant skew matrix `A^T=-A` and `r(x)=Ax`. Then

`c_s=(A-A^T)x=2Ax`

is constant along the ray and

`n=Ax=(1/2)c_s`.

Thus

`4Q_F(n)=Q_F(c_s)`

exactly. Any universal factor smaller than `1/4` would fail already for this affine pure-skew field.

---

## 4. Root-free small-gain absorption into a Lyapunov ledger

The previous section only bounds the nonconservative force defect. It can be converted into a clean power budget without taking a norm square root.

Assume the *reshaped* storage `V` already satisfies a centered displacement comparator

**(4.1)** `m Q_X(x) <= V`, with `m>0`.

Combining (3.4) and (4.1) gives

**(4.2)** `4 m Q_F(n) <= K_curl V`.

Let `Q_V(v)` be the velocity quadratic form used by the dissipation channel, and assume the force/velocity pairing obeys the compatible quadratic Cauchy bound

**(4.3)**

`<v,n>^2 <= Q_V(v) Q_F(n)`.

Suppose the nominal shaped ledger reserves

`-c V - d Q_V(v)`,

where `d>0`. Choose rational reserve parameters

`0 <= alpha < c`,
`0 <= theta < 1`.

If the exact-rational checker verifies

**(4.4) CURL SMALL-GAIN GATE**

`K_curl <= 16 m alpha theta d`,

then

**(4.5)**

`<v,n> <= alpha V + theta d Q_V(v)`.

### Proof without square roots

From (4.2) and (4.3),

`4m <v,n>^2 <= K_curl V Q_V(v)`.

Using (4.4),

`4m <v,n>^2 <= 16m alpha theta d V Q_V(v)`.

Set

`a = alpha V`,
`b = theta d Q_V(v)`.

Both are nonnegative, and

`(a+b)^2 - 4ab = (a-b)^2 >= 0`.

Therefore `<v,n>^2 <= (a+b)^2`, hence `<v,n> <= a+b`. This proves (4.5). The trusted instance gate contains only multiplication and order comparisons.

Consequently, any ledger

**(4.6)**

`Vdot <= -cV - d Q_V(v) + <v,n> + p_other`

immediately closes to

**(4.7) APPROXIMATELY-CONSERVATIVE DECAY LEDGER**

`Vdot <= -(c-alpha)V -(1-theta)d Q_V(v) + p_other`.

Thus a small nonzero curl defect need not create an additive floor. Because the radial remainder vanishes at the anchor and is proportional to displacement, it can be paid as a *relative* two-channel loss whenever the shaped storage controls that displacement.

This is materially different from the nonzero center-bias branch of T-P5-118, where a genuine additive `O(B^2)` floor can be unavoidable.

### Boundary semantics

- If `K_curl=0`, choose `alpha=0` or `theta=0` and recover exact conservative cancellation.
- If `K_curl>0`, both a storage-rate reserve and a dissipation reserve are generally needed by this information-level theorem.
- The constant `16` is sharp for the scalar absorption problem under only (4.2)-(4.3): the minimum of `(alpha V + theta d Q)^2/(VQ)` is `4 alpha theta d`.

---

## 5. Time-dependent physical force

If `r=r(t,q)` and the anchor `q0` is fixed, define the same radial potential at each fixed time:

`Psi(t,q)=integral_0^1 <r(t,q0+s(q-q0)),q-q0> ds`.

The spatial decomposition remains

`r = grad_q Psi + n`,

with `n` given by the skew spatial Jacobian formula (2.2).

Along a physical trajectory `q(t)` with `v=qdot`, the exact power identity is

**(5.1)**

`<v,r> = d/dt Psi(t,q(t)) - Psi_t(t,q(t)) + <v,n>`.

So storage shaping charges only

- the schedule term `-Psi_t`, and
- the nonconservative curl-defect power `<v,n>`.

It must not charge the full force amplitude again.

If the radial anchor itself moves in time, extra anchor-motion terms enter `Psi_t`; this child does not erase them.

---

## 6. Moving nonlinear chart: curl is a pulled-back 2-form, not a chart-Hessian artifact

T-P5-120 gives the generalized force/covector pullback

`q(z)=J(z)^T r(T(z))`.

At fixed time, differentiate it spatially. Write `A=Dr`. The full derivative has the form

**(6.1)**

`D_z q = H_chart + J^T A J`,

where `H_chart` is the contraction of the chart Hessian with `r`.

For a `C^2` chart, mixed partials commute, so `H_chart` is symmetric. Therefore the antisymmetric derivative obeys the exact congruence law

**(6.2) COVECTOR-CURL PULLBACK**

`D_z q - (D_z q)^T`
` = J^T (A-A^T) J`.

This is important for two reasons.

First, nonlinear-chart Hessian terms do **not** manufacture fake curl. Exact conservativity remains exact after pullback.

Second, approximate curl can be transported as a genuine 2-form. A quantitative norm bound may still pay a Jacobian/metric-comparison factor, but that factor belongs to the metric conversion, not to a fictitious Hessian defect.

A particularly clean source strategy is therefore:

1. perform the radial decomposition in the physical configuration cell where source semantics are authoritative;
2. pull back the exact conservative part and the residual covector separately;
3. form the complete signed residual work before intervalization.

If `r=grad Psi+n`, then under the moving chart of T-P5-120,

`r^T v = d/dt(Psi o T) - Psi_t o T + n^T v`,

and

`n^T v = (J^T n)^T zdot + n^T Tt`.

Thus the residual frame-power term must remain attached to the residual covector. Bounding only `(J^T n)^T zdot` would again lose exact work semantics.

---

## 7. Hard obstruction 1: symmetry at the anchor alone gives no finite remainder bound

A same-segment derivative cap is not a technical convenience; it is mathematically necessary.

In two dimensions, for any `N>0`, take

`q0=(0,0)`,
`r_N(x,y)=(0, N x^2)`.

At the anchor,

`Dr_N(q0)=0`,

so the Jacobian is perfectly symmetric there.

Now evaluate at `q=(1,0)`, hence `x=(1,0)`. Along the radial segment `z_s=(s,0)`,

`(Dr_N(z_s)-Dr_N(z_s)^T)x = (0,2Ns)`.

Formula (2.2) gives

`n(q) = integral_0^1 s(0,2Ns) ds = (0,2N/3)`.

The nonconservative remainder is therefore unbounded as `N` grows, despite *zero* skew Jacobian at the anchor.

So an anchor-point Hessian/symmetry witness cannot replace whole-ray or whole-cell coverage.

---

## 8. Hard obstruction 2: local curl-free data need topology/segment coverage for a global potential

On a non-star-shaped/non-simply-connected domain, local symmetry of the Jacobian does not by itself produce a globally single-valued potential. The classical angular one-form on an annulus is curl-free locally but has nonzero circulation around the hole.

T-P5-119 avoids this issue by using a star-shaped cell and a constructive radial path. T-P5-121 retains exactly that requirement. If a deployed cell is not star-shaped in the physical coordinates used for the force field, the source adapter must either:

- partition it into star-shaped cells with consistent potential normalization, or
- provide a separate global exactness/path-independence witness.

No finite collection of local symmetry samples substitutes for that global condition.

---

## 9. Source-facing packet

A real P5 producer that wants to use this child should bind, under one common physical cell/tube key:

1. the signed configuration-force/residual field `r` actually appearing in the physical power ledger;
2. the exact spatial derivative semantics `A=Dr` on that same field;
3. a star anchor `q0` and proof that every radial segment used by the candidate storage stays in the certified cell;
4. either the direct integrated cap (3.1) or a uniform skew-action cap (3.3);
5. the radial potential `Psi` or an exact evaluator/identity for it;
6. positivity/coercivity of the *reshaped* storage and the comparator `m Q_X(q-q0)<=V`;
7. the compatible power Cauchy packet (4.3) and the nominal reserves `(c,d)`;
8. chosen rational `(alpha,theta)` and checker proof of `K_curl<=16m alpha theta d`;
9. for a moving chart, `T/J/Tt` plus the complete residual work split, not only the spatial generalized-force term;
10. a no-double-count rule removing `grad Psi` from later generic residual budgets.

For a polynomial/rational force field on a rational star anchor, the radial integral often produces a polynomial with rational coefficients, so the potential itself can frequently remain exact-rational. Trigonometric/mechanical potentials may instead be better supplied by their native physical source identity.

---

## 10. Suggested Lean decomposition

The highest-value first formalization is the scalar/quadratic small-gain leaf, because it is independent of differential-geometry APIs.

```text
curl_defect_power_absorption:
  0 <= V,
  0 <= Qv,
  0 <= Qn,
  0 < m,
  0 <= alpha,
  0 <= theta,
  0 < d,
  4*m*Qn <= K*V,
  p^2 <= Qv*Qn,
  K <= 16*m*alpha*theta*d
  -> p <= alpha*V + theta*d*Qv.
```

Then the ledger corollary:

```text
approx_conservative_decay_ledger:
  Vdot <= -c*V - d*Qv + p + pOther,
  p <= alpha*V + theta*d*Qv
  -> Vdot <= -(c-alpha)*V -(1-theta)*d*Qv + pOther.
```

The calculus leaves can remain premise-driven initially:

```text
radial_potential_gradient_defect:
  grad Psi(q) = r(q) + integral_0^1 s*(Dr^T-Dr)*x ds.

radial_curl_defect_quadratic_quarter:
  n = integral_0^1 s*c(s) ds,
  forall s, QF(c(s)) <= K*QX(x)
  -> 4*QF(n) <= K*QX(x).
```

For chart transport, a pure matrix leaf avoids rebuilding the chart calculus:

```text
covector_curl_pullback_algebra:
  Dq = H + J^T*A*J,
  H^T=H
  -> Dq-Dq^T = J^T*(A-A^T)*J.
```

A later source-specific theorem can prove that the actual chart derivative has the required `H + J^T A J` decomposition.

---

## 11. Open boundaries / non-claims

T-P5-121 is **CONDITIONAL_PASS / pending mathematical child** only.

Still open:

- whether any actual deployed P5 configuration-force residual is differentiable under the intended exact-real semantics;
- whether its same-cell `Dr-Dr^T` admits a useful exact-rational skew-action bound;
- whether the physical cell is star-shaped around the chosen storage anchor and all radial segments are covered;
- construction/value binding of the radial potential in the actual source model;
- positivity/coercivity of the reshaped storage and its centered displacement comparator;
- actual paired force/velocity metrics and nominal `(c,d)` reserves;
- time-dependent anchor/reference schedule terms;
- moving-chart source binding and residual frame-power preservation;
- FD/controller/solve decomposition and no-double-count semantics;
- Float64/runtime semantics, P8/ODE coverage, Lean/kernel, independent verifier 封不觉, admission and registry.

The new mathematical fact is narrow but useful: **approximate Jacobian symmetry on the whole star-shaped cell yields a controlled nonconservative remainder with a sharp quarter-factor, and that remainder can be absorbed by the existing Lyapunov/dissipation margins through the exact rational gate `K_curl <= 16 m alpha theta d`.** Exact conservativity is the `K_curl=0` endpoint, not a separate coordinate-dependent phenomenon.
